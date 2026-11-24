"""Unit and agent-level tests for A1 Service Desk Agent (UC-02)."""
import pytest
from app.agents.A1_service_desk.agent import ServiceDeskAgent
from app.agents.base.agent_context import AgentContext, TenantContext, UserContext
from app.governance.action_manifest import RiskTier


@pytest.fixture
def agent():
    return ServiceDeskAgent()


@pytest.fixture
def context():
    return AgentContext(
        tenant=TenantContext(tenant_id="tenant-corp"),
        user=UserContext(
            user_id="usr-100",
            username="Sarah Connor",
            email="sconnor@corp.internal"
        )
    )


@pytest.mark.asyncio
async def test_agent_capabilities(agent):
    assert agent.agent_id == "A1_service_desk"
    assert agent.can_handle("UC-02") is True
    assert agent.can_handle("UC-04") is True
    assert agent.can_handle("UC-99") is False


@pytest.mark.asyncio
async def test_reason_informational_guidance(agent, context):
    query = "How do I connect to the office VPN?"
    res = await agent.reason(context, query)

    assert res.agent_id == "A1_service_desk"
    assert res.use_case_id == "UC-02"
    assert res.handoff_required is False
    assert "Sarah Connor" in res.response_text


@pytest.mark.asyncio
async def test_reason_escalation_detection(agent, context):
    query = "Major production database down, critical crash!"
    res = await agent.reason(context, query)

    assert res.handoff_required is True
    assert "escalation" in res.response_text.lower()


@pytest.mark.asyncio
async def test_plan_standard_ticket_creation(agent, context):
    query = "Please open an incident ticket for my mouse issue"
    manifest = await agent.plan(context, query, "UC-02")

    assert manifest.tenant_id == "tenant-corp"
    assert manifest.overall_risk_tier == RiskTier.T1
    assert manifest.requires_human_approval is False
    assert len(manifest.steps) == 1
    assert manifest.steps[0].tool_name == "itsm_create_ticket"
    assert manifest.plan_hash != ""


@pytest.mark.asyncio
async def test_plan_service_remediation_approval(agent, context):
    query = "Please restart print spooler service on my laptop"
    manifest = await agent.plan(context, query, "UC-02")

    assert manifest.overall_risk_tier == RiskTier.T2
    assert manifest.requires_human_approval is True
    assert any(s.tool_name == "endpoint_restart_service" for s in manifest.steps)
    assert manifest.plan_hash != ""