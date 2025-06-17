# ─────────────────────────────────────────────
# 🔐 auth/admin.py — JWT-Based Admin Verification
# ─────────────────────────────────────────────

import os
from fastapi import Request, HTTPException, status
from jose import jwt, JWTError
from logger import logger

SECRET_KEY = os.getenv("SECRET_KEY") or "supersecret"
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")

def admin_required(request: Request):
    """
    Dependency for protected admin routes.

    Verifies the presence of a valid JWT token in the HttpOnly cookie
    and ensures the token belongs to the authorized admin.

    Raises:
        401 Unauthorized — if token is missing or invalid
        403 Forbidden — if the email is not the admin's
    """
    if not ADMIN_EMAIL:
        logger.critical("❌ ADMIN_EMAIL not set in environment variables")
        raise RuntimeError("ADMIN_EMAIL not set in environment variables")

    token = request.cookies.get("access_token")
    if not token:
        logger.warning("🚫 Missing access token cookie.")
        raise HTTPException(status_code=401, detail="Missing authentication token")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        email = payload.get("sub")

        if email != ADMIN_EMAIL:
            logger.warning(f"⚠️ Access denied — token email '{email}' is not authorized.")
            raise HTTPException(status_code=403, detail="Access denied: not an authorized admin")

        logger.info(f"🔐 Admin token verified for {email}")
        return email

    except JWTError as e:
        logger.error(f"❌ Invalid or expired token: {e}")
        raise HTTPException(status_code=401, detail="Invalid or expired authentication token")
