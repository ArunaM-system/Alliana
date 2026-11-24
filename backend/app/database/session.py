"""
Database engine and session management.
Reads connection parameters from environment settings.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings

def get_engine_url(url: str) -> str:
    """Normalize postgresql:// to postgresql+psycopg2:// if driver is omitted."""
    if url.startswith("postgresql://"):
        return url.replace("postgresql://", "postgresql+psycopg2://", 1)
    return url

# Engine configured from environment settings; no hardcoded credentials
engine = create_engine(get_engine_url(settings.DATABASE_URL))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
