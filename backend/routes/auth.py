# ─────────────────────────────────────────────
# 🔐 routes/auth.py — Google OAuth2 Login Flow
# ─────────────────────────────────────────────

import os
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Request, HTTPException, status
from fastapi.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth
from dotenv import load_dotenv
from jose import jwt

from logger import logger

# ─────────────────────────────────────────────
# 🌍 Load environment variables (safe if reloaded)
# ─────────────────────────────────────────────
load_dotenv()

# ─────────────────────────────────────────────
# 📦 Define router
# ─────────────────────────────────────────────
router = APIRouter(tags=["Auth"])

# ─────────────────────────────────────────────
# 🔐 OAuth2 / JWT configuration
# ─────────────────────────────────────────────
GOOGLE_CLIENT_ID     = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
ADMIN_EMAIL          = os.getenv("ADMIN_EMAIL")
SECRET_KEY           = os.getenv("SECRET_KEY") or "supersecret"
JWT_EXPIRY_HOURS     = int(os.getenv("JWT_EXPIRY_HOURS", 8))

# 🔥 Validate critical credentials at startup
if not all([GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, ADMIN_EMAIL]):
    logger.critical("❌ Missing required Google OAuth environment variables.")
    raise RuntimeError("Missing GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, or ADMIN_EMAIL.")

# ─────────────────────────────────────────────
# 🧩 Configure OAuth2 (Google)
# ─────────────────────────────────────────────
oauth = OAuth()
oauth.register(
    name="google",
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email"},
)

# 🔗 GET /auth/login → Redirect to Google login
@router.get("/auth/login")
async def login(request: Request):
    """
    Start OAuth2 login via Google.

    Redirects the user to Google's login page.
    """
    redirect_uri = request.url_for("auth_callback")
    logger.info(f"🔄 Initiating Google OAuth login (redirect_uri={redirect_uri})")
    return await oauth.google.authorize_redirect(request, redirect_uri)

# 🚪 GET /auth/logout → Clears JWT cookie
@router.get("/auth/logout")
def logout():
    """
    Logs out the user by clearing the JWT cookie.
    """
    response = RedirectResponse(url="/")
    response.delete_cookie("access_token")
    logger.info("👋 Admin logged out.")
    return response

# 🎯 GET /auth/callback → OAuth2 callback
@router.get("/auth/callback")
async def auth_callback(request: Request):
    """
    Handle Google's OAuth2 callback.

    Issues a JWT as an HttpOnly cookie if the user is authorized.
    """
    try:
        token = await oauth.google.authorize_access_token(request)
        user_info = token.get("userinfo") or token.get("id_token_claims")
        email = user_info.get("email")
    except Exception as e:
        logger.error(f"❌ OAuth callback failed: {e}")
        raise HTTPException(status_code=400, detail="OAuth authentication failed")

    if not email:
        logger.warning("⚠️ No email found in token payload.")
        raise HTTPException(status_code=400, detail="Email not found in token")

    if email.lower() != ADMIN_EMAIL.lower():
        logger.warning(f"⛔ Unauthorized access attempt by: {email}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: only the admin can log in"
        )

    # ✅ Construct JWT payload
    jwt_payload = {
        "sub": email,
        "exp": datetime.now(timezone.utc) + timedelta(hours=JWT_EXPIRY_HOURS),
        "iss": "multi-service-backend"
    }

    # ✅ Encode JWT using secret key
    jwt_token = jwt.encode(jwt_payload, SECRET_KEY, algorithm="HS256")

    # 🍪 Store JWT in secure HttpOnly cookie
    response = RedirectResponse(url="/admin")
    response.set_cookie(
        key="access_token",
        value=jwt_token,
        httponly=True,
        secure=False,  # ⚠️ Use True in production with HTTPS
        samesite="Lax",
        max_age=JWT_EXPIRY_HOURS * 3600
    )

    logger.info(f"✅ Admin login successful for {email}. JWT issued.")
    return response
