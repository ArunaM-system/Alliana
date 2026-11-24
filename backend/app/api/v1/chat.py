"""Conversational chat and orchestrator entrypoint (L1 API)."""
from typing import Any, Dict, Optional
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from app.agents.base.agent_context import AgentContext, TenantContext, UserContext
from app.core.dependencies import get_tenant_id
from app.orchestration.orchestrator import OrchestratorResponse, orchestrator

router = APIRouter(prefix="/chat", tags=["Chat"])

class ChatMessageRequest(BaseModel):
    message: str
    channel: str = "web"
    session_id: Optional[str] = None
    user_id: str = "user-default"
    username: str = "IT User"
    email: str = "user@example.com"

@router.post("/message", response_model=OrchestratorResponse)
async def send_chat_message(
    req: ChatMessageRequest,
    tenant_id: str = Depends(get_tenant_id)
):
    """
    Primary conversational endpoint:
    Traverses L1 (Ingress) -> L2 (Orchestrator) -> L3 (Agent) -> L5 (Governance).
    """
    context = AgentContext(
        session_id=req.session_id or "sess-default",
        tenant=TenantContext(tenant_id=tenant_id),
        user=UserContext(
            user_id=req.user_id,
            username=req.username,
            email=req.email
        ),
        channel=req.channel
    )
    return await orchestrator.handle_request(req.message, context)

@router.get("/status")
def chat_status():
    """Operational status of the chat orchestration layer."""
    return {"status": "operational", "layer": "L2 Orchestrator"}
