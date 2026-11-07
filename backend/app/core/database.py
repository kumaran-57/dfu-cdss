"""
Database connection and session management for DFU-XAI.
Supports SQLite (zero-config local dev & testing) and PostgreSQL.
"""

from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from backend.app.core.config import settings

# Configure connection args (e.g. check_same_thread for SQLite)
connect_args = {}
if settings.DATABASE_URL.startswith("sqlite"):
    connect_args["check_same_thread"] = False

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    echo=False,
    future=True,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    future=True,
)

Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    """Dependency that provides a transactional database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db(target_engine=None):
    """Creates all database tables based on registered models."""
    from backend.app import models  # noqa: F401 ensure models are registered
    eng = target_engine or engine
    Base.metadata.create_all(bind=eng)
