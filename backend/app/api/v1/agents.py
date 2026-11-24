"""Specialist agent status and management endpoints placeholder (L1 API)."""
from fastapi import APIRouter

router = APIRouter(prefix="/agents", tags=["Agents"])

@router.get("/")
def list_agents():
    return {"agents": [], "message": "Agent registry endpoints will be connected in subsequent phases."}
