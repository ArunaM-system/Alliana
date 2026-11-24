"""
Integration test for PostgreSQL connectivity.
MOCK/SAFETY: Reads database URL from configuration settings, never hardcoded.
Skipped automatically if no live database connection is available.
"""
import pytest
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from app.database.session import SessionLocal

def test_database_connection():
    try:
        db = SessionLocal()
        result = db.execute(text("SELECT 1")).scalar()
        assert result == 1
        db.close()
    except OperationalError:
        pytest.skip("PostgreSQL service not reachable for live integration test.")
