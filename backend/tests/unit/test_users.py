"""
Unit tests for user endpoints and models using isolated in-memory SQLite.
"""
import os
import sys

# Ensure backend directory is in sys.path for IDE analysis and standalone test runs
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from app.database.models.user import User

def test_list_users_empty(client):
    response = client.get("/api/v1/users/")
    assert response.status_code == 200
    assert response.json() == []

def test_create_and_list_user(client, db_session):
    user = User(name="Test Admin", email="admin@allina.local")
    db_session.add(user)
    db_session.commit()

    response = client.get("/api/v1/users/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Test Admin"
    assert data[0]["email"] == "admin@allina.local"

def test_legacy_users_endpoint(client):
    response = client.get("/users/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
