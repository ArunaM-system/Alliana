"""Unit tests for Base Agent framework and Registry (L3)."""
import pytest
from typing import Optional
from app.agents.base.agent_context import AgentContext, TenantContext, UserContext
from app.agents.base.agent_identity import AgentIdentity
from app.agents.base.base_agent import BaseAgent, AgentResponse
from app.agents.base.agent_registry import AgentRegistry
from app.governance.action_manifest import ActionManifest

class DummyAgent(BaseAgent):
    """Concrete agent for unit testing BaseAgent lifecycle."""

    async def reason(
        self,
        context: AgentContext,
        input_text: str,
        use_case_id: Optional[str] = None,
        **kwargs
    ) -> AgentResponse:
        return AgentResponse(
            agent_id=self.agent_id,
            use_case_id=use_case_id or "UC-02",
            response_text=f"Processed query: {input_text}"
        )

    async def plan(
        self,
        context: AgentContext,
        input_text: str,
        use_case_id: str,
        **kwargs
    ) -> ActionManifest:
        return ActionManifest(
            agent_id=self.agent_id,
            tenant_id=context.tenant.tenant_id,
            use_case_id=use_case_id,
            description=f"Plan for {input_text}"
        )

@pytest.fixture
def agent_identity():
    return AgentIdentity(
        agent_id="test_agent",
        name="Test Specialist Agent",
        domain="IT Operations",
        role="Testing",
        description="Agent for test verification",
        supported_use_cases=["UC-02", "UC-04"],
        service_principal_id="sp-test-01"
    )

@pytest.fixture
def sample_context():
    return AgentContext(
        tenant=TenantContext(tenant_id="tenant-acme"),
        user=UserContext(
            user_id="user-1",
            username="alex",
            email="alex@acme.com"
        )
    )

@pytest.mark.asyncio
async def test_base_agent_lifecycle(agent_identity, sample_context):
    agent = DummyAgent(identity=agent_identity)
    assert agent.agent_id == "test_agent"
    assert agent.can_handle("UC-02") is True
    assert agent.can_handle("UC-99") is False

    response = await agent.reason(sample_context, "Need help with printer")
    assert response.agent_id == "test_agent"
    assert "printer" in response.response_text

    manifest = await agent.plan(sample_context, "Fix printer", "UC-02")
    assert manifest.tenant_id == "tenant-acme"

def test_agent_registry(agent_identity):
    registry = AgentRegistry()
    agent = DummyAgent(identity=agent_identity)

    registry.register(agent)
    assert registry.get("test_agent") is agent
    assert registry.resolve_for_use_case("UC-02") is agent
    assert registry.resolve_for_use_case("UC-99") is None

    agents = registry.list_agents()
    assert len(agents) == 1
    assert agents[0].agent_id == "test_agent"

    registry.clear()
    assert registry.get("test_agent") is None
