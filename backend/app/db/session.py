"""Legacy redirect shim for app.db.session."""
from app.database.session import SessionLocal, engine

__all__ = ["SessionLocal", "engine"]
