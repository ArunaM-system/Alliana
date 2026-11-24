"""Specialist Agent identity, domain scope, and role metadata (L3)."""
from typing import List
from pydantic import BaseModel, Field

class AgentIdentity(BaseModel):
    """
    Cryptographically and functionally scoped identity for an AI Specialist Agent.
    Limits operational scope and permissions in accordance with least privilege.
    """
    agent_id: str               # e.g., "A1_service_desk"
    name: str                   # e.g., "Service Desk Agent"
    domain: str                 # e.g., "IT Support & Service Management"
    role: str                   # e.g., "Level 1/2 Support, Ticket Fulfillment"
    description: str
    supported_use_cases: List[str] = Field(default_factory=list)
    permissions: List[str] = Field(default_factory=list)
    max_risk_tier: str = "T2"
    service_principal_id: str   # Bound IAM identity for external service interactions
