"""Agent execution context and multi-tenant metadata models (L3)."""
from typing import Any, Dict, List, Optional
import uuid
from pydantic import BaseModel, Field

class UserContext(BaseModel):
    """Authenticated user context initiating or targeted by an operation."""
    user_id: str
    username: str
    email: str
    roles: List[str] = Field(default_factory=list)
    organization: Optional[str] = None

class TenantContext(BaseModel):
    """Validated multi-tenant execution partition."""
    tenant_id: str
    tenant_name: str = "Default Organization"
    environment: str = "production"

class AgentContext(BaseModel):
    """
    Complete contextual environment provided to an agent during reasoning.
    Carries verified tenant identity, session tracking, and conversation history.
    """
    session_id: str = Field(default_factory=lambda: f"sess-{uuid.uuid4().hex[:10]}")
    request_id: str = Field(default_factory=lambda: f"req-{uuid.uuid4().hex[:10]}")
    tenant: TenantContext
    user: UserContext
    channel: str = "api"  # "api", "web", "teams", "slack", "mobile", "voice"
    conversation_history: List[Dict[str, str]] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    state: Dict[str, Any] = Field(default_factory=dict)
