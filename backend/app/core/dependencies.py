"""
Core FastAPI dependencies.
Provides database session lifecycle management.
"""
from typing import Generator
from sqlalchemy.orm import Session
from app.database.session import SessionLocal

def get_db() -> Generator[Session, None, None]:
    """Provide a transactional database session."""
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
