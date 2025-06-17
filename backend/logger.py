# ─────────────────────────────────────────────
# 📝 logger.py — Central Logging Configuration
# ─────────────────────────────────────────────

import logging
from logging.handlers import RotatingFileHandler
import os

# ─────────────────────────────────────────────
# 🌍 Load configuration from environment
# ─────────────────────────────────────────────
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_FILE = os.getenv("LOG_FILE", "logs/app.log")

# ─────────────────────────────────────────────
# 📁 Ensure log directory exists
# ─────────────────────────────────────────────
log_dir = os.path.dirname(LOG_FILE)
if log_dir and not os.path.exists(log_dir):
    os.makedirs(log_dir)

# ─────────────────────────────────────────────
# 🧱 Create root logger
# ─────────────────────────────────────────────
logger = logging.getLogger("app")
logger.setLevel(LOG_LEVEL)

# ─────────────────────────────────────────────
# 📤 Console Handler
# ─────────────────────────────────────────────
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter(
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
))
logger.addHandler(console_handler)

# ─────────────────────────────────────────────
# 💾 Rotating File Handler
# ─────────────────────────────────────────────
file_handler = RotatingFileHandler(
    LOG_FILE,
    maxBytes=5 * 1024 * 1024,  # 5 MB
    backupCount=3
)
file_handler.setFormatter(logging.Formatter(
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
))
logger.addHandler(file_handler)
