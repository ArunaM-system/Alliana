"""
Pytest configuration and shared test fixtures for ALLINA.
Uses SQLite in-memory database with StaticPool for isolated, lightning-fast unit tests.
"""
import os
import sys

# Ensure pure-Python mode for SQLAlchemy to avoid Windows AppLocker DLL blocking
os.environ["DISABLE_SQLALCHEMY_CEXT"] = "1"
# Ensure tests use in-memory SQLite by default
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

# Ensure backend directory is in sys.path
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

import pytest
from starlette.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database.base import Base
import app.database.models  # Register all models on Base.metadata
from app.core.dependencies import get_db
from app.main import app

# In-memory SQLite engine with StaticPool to retain tables across sessions
engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """Create all database tables for the test session."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session():
    """Provide a clean database session for each test."""
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()

@pytest.fixture
def client(db_session):
    """Provide FastAPI test client with overridden database dependency."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
