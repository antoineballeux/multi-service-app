# ─────────────────────────────────────────────
# 📄 main.py — App Entry Point for Multi-Services
# ─────────────────────────────────────────────

from dotenv import load_dotenv
load_dotenv()  # ✅ Must be called first!

import os
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware

from database import init_db
from routes import services, bookings, auth, admin  # These may access env vars
from logger import logger

# ─────────────────────────────────────────────
# ⚙️ Custom startup/shutdown lifespan handler
# ─────────────────────────────────────────────
async def lifespan(app: FastAPI):
    logger.info("🔧 Initializing database...")
    init_db()
    yield
    logger.info("🧹 Shutting down app...")

# ─────────────────────────────────────────────
# 🚀 Create FastAPI instance
# ─────────────────────────────────────────────
app = FastAPI(
    title="Multi-Services API",
    description="An API to manage Multi-Services offerings and customer bookings",
    version="1.0.0",
    lifespan=lifespan
)

# ─────────────────────────────────────────────
# 🗝️ Add Session Middleware (required for OAuth)
# ─────────────────────────────────────────────
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SECRET_KEY") # Ensure SECRET_KEY is set in .env or environment variables
)

# ─────────────────────────────────────────────
# 🌐 CORS Configuration (adjust origins as needed)
# ─────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─────────────────────────────────────────────
# 📦 Include Routers
# ─────────────────────────────────────────────
app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(services.router)
app.include_router(bookings.router)
