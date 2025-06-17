# ─────────────────────────────────────────────
# 🛠️ routes/admin.py — Admin Dashboard Landing
# ─────────────────────────────────────────────

from fastapi import APIRouter, Depends
from auth import admin_required
from logger import logger

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

# 📄 GET /admin → Landing page (admin only)
@router.get("/", dependencies=[Depends(admin_required)])
def admin_home():
    """
    Welcome page for authenticated admin.

    Protected by JWT token.
    """
    logger.info("📥 Admin accessed dashboard home.")
    return {"message": "Welcome to the Multi-Service admin dashboard!"}
