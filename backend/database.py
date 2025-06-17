from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.exc import SQLAlchemyError

from logger import logger

# ─────────────────────────────────────────────
# 🗃️ Database configuration
# ─────────────────────────────────────────────

# SQLite path — switch to PostgreSQL later by replacing the URI
DATABASE_URL = "sqlite:///database.db"

# Create the engine (manages the DB connection pool)
engine = create_engine(
    DATABASE_URL,
    echo=True  # Set to False in production to hide raw SQL queries
)

# ─────────────────────────────────────────────
# 📦 Initialize the database (create tables)
# ─────────────────────────────────────────────

def init_db() -> None:
    """
    Initializes the database by creating all tables defined in SQLModel models.
    Use this at app startup. Fails loudly if DB is misconfigured.
    """
    try:
        SQLModel.metadata.create_all(engine)
        logger.info("✅ Database initialized successfully.")
    except SQLAlchemyError as e:
        logger.error(f"❌ Database initialization failed: {e}")
        raise

# ─────────────────────────────────────────────
# 🔁 Provide a DB session (used in API routes)
# ─────────────────────────────────────────────

def get_session():
    """
    FastAPI dependency that yields a database session.
    Ensures automatic cleanup (open → yield → close).
    """
    with Session(engine) as session:
        yield session
