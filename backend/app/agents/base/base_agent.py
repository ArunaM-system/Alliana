"""
Abstract Base Agent contract for all ALLINA Specialist Agents (A1 through A12).
Enforces the fundamental architectural boundary:
'Agents decide and plan; Governance authorizes; Automation executes.'
"""
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Dict, List, Optional
from pydantic import BaseModel, Field

from app.agents.base.agent_context import AgentContext
from app.agents.base.agent_identity import AgentIdentity
from app.governance.action_manifest import ActionManifest

if TYPE_CHECKING:
    from app.automation.tool_gateway.contracts import ToolContract

class AgentResponse(BaseModel):
    """Standardized response produced by an agent after reasoning or planning."""
    agent_id: str
    use_case_id: Optional[str] = None
    response_text: str
    action_manifest: Optional[ActionManifest] = None
    confidence: float = 1.0
    suggested_next_steps: List[str] = Field(default_factory=list)
    handoff_required: bool = False
    metadata: Dict[str, Any] = Field(default_factory=dict)

class BaseAgent(ABC):
    """
    Abstract Base Class for all 12 Specialist Agents in ALLINA.
    Provides standard lifecycle hooks, tool registration, and planning interfaces.
    """

    def __init__(
        self,
        identity: AgentIdentity,
        tools: Optional[List[Any]] = None,
    ):
        self.identity = identity
        self.tools: Dict[str, Any] = {t.name: t for t in (tools or [])}

    @property
    def agent_id(self) -> str:
        return self.identity.agent_id

    @property
    def name(self) -> str:
        return self.identity.name

    @property
    def supported_use_cases(self) -> List[str]:
        return self.identity.supported_use_cases

    def can_handle(self, use_case_id: str) -> bool:
        """Verify whether this agent is authorized and capable of handling a use case."""
        return use_case_id in self.supported_use_cases

    def get_tool(self, tool_name: str) -> Optional[Any]:
        """Retrieve a registered tool specification by name."""
        return self.tools.get(tool_name)

    async def pre_reason(self, context: AgentContext) -> None:
        """Lifecycle hook executed prior to cognitive reasoning or planning."""
        pass

    async def post_reason(
        self,
        response: AgentResponse,
        context: AgentContext
    ) -> AgentResponse:
        """Lifecycle hook executed immediately after response generation."""
        return response

    @abstractmethod
    async def reason(
        self,
        context: AgentContext,
        input_text: str,
        use_case_id: Optional[str] = None,
        **kwargs
    ) -> AgentResponse:
        """
        Primary conversational & diagnostic reasoning entrypoint.
        Produces user responses, diagnostics, or proposed execution plans.
        """
        pass

    @abstractmethod
    async def plan(
        self,
        context: AgentContext,
        input_text: str,
        use_case_id: str,
        **kwargs
    ) -> ActionManifest:
        """
        Generates a structured ActionManifest representing an authorized operational plan.
        The plan will be evaluated by Governance (L5) before execution.
        """
        pass
