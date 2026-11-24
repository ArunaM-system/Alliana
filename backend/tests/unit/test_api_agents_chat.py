"""Unit tests for API endpoints: /api/v1/agents and /api/v1/chat."""
import pytest
from app.agents.base.agent_identity import AgentIdentity
from app.agents.registry import agent_registry

def test_api_agents_endpoint(client):
    response = client.get("/api/v1/agents/")
    assert response.status_code == 200
    data = response.json()
    assert "agents" in data
    assert "total" in data

def test_api_chat_status(client):
    response = client.get("/api/v1/chat/status")
    assert response.status_code == 200
    assert response.json()["status"] == "operational"

def test_api_chat_message(client):
    payload = {
        "message": "I need help with my workstation issue",
        "channel": "web",
        "username": "tester",
        "email": "tester@example.com"
    }
    response = client.post(
        "/api/v1/chat/message",
        json=payload,
        headers={"x-tenant-id": "tenant-corp"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "response_text" in data
