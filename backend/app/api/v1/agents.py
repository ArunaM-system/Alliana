"""Specialist Agent discovery and inspection endpoints (L1 API)."""
from typing import Any, Dict, List
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from app.agents.base.agent_identity import AgentIdentity
from app.agents.registry import agent_registry

router = APIRouter(prefix="/agents", tags=["Agents"])

class AgentListResponse(BaseModel):
    agents: List[AgentIdentity]
    total: int

@router.get("/", response_model=AgentListResponse)
def list_agents():
    """Retrieve metadata and capabilities for all registered Specialist Agents."""
    agents = agent_registry.list_agents()
    return AgentListResponse(agents=agents, total=len(agents))

@router.get("/{agent_id}", response_model=AgentIdentity)
def get_agent(agent_id: str):
    """Retrieve detailed identity and capability profile for a specific agent."""
    agent = agent_registry.get(agent_id)
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Specialist agent '{agent_id}' not found."
        )
    return agent.identity
