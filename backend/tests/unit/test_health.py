"""
Unit tests for Health Check & Status endpoints (L1 API).
"""
import os
import sys

# Ensure backend directory is in sys.path for IDE analysis and standalone test runs
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

def test_health_check_endpoint(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "service" in data
    assert "version" in data
    assert data["environment"] == "development"

def test_legacy_hello_endpoint(client):
    response = client.get("/hello")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, world!"}
