"""Unit tests for Central Orchestration (L2), Intent Classification, and Agent Routing."""
import pytest
from app.agents.base.agent_context import AgentContext, TenantContext, UserContext
from app.agents.base.agent_identity import AgentIdentity
from app.agents.base.agent_registry import AgentRegistry
from app.agents.base.base_agent import AgentResponse, BaseAgent
from app.governance.action_manifest import ActionManifest, ActionStep, RiskTier
from app.orchestration.agent_router import AgentRouter
from app.orchestration.intent_classifier import (
    IntentClassificationResult,
    IntentClassifier,
)
from app.orchestration.orchestrator import AllinaOrchestrator


class MockServiceDeskAgent(BaseAgent):
    """Mock agent simulating L1/L2 service desk responses."""

    async def reason(
        self,
        context: AgentContext,
        input_text: str,
        use_case_id: str | None = None,
        **kwargs
    ) -> AgentResponse:
        manifest = None
        if "restart" in input_text.lower():
            manifest = await self.plan(context, input_text, use_case_id or "UC-02")

        return AgentResponse(
            agent_id=self.agent_id,
            use_case_id=use_case_id or "UC-02",
            response_text=f"Service desk assisting with: {input_text}",
            action_manifest=manifest
        )

    async def plan(
        self,
        context: AgentContext,
        input_text: str,
        use_case_id: str,
        **kwargs
    ) -> ActionManifest:
        manifest = ActionManifest(
            agent_id=self.agent_id,
            tenant_id=context.tenant.tenant_id,
            use_case_id=use_case_id,
            description=f"Action plan for {input_text}"
        )
        manifest.steps.append(
            ActionStep(
                tool_name="restart_service",
                parameters={"service_name": "spooler"},
                risk_tier=RiskTier.T2
            )
        )
        return manifest

def test_intent_classifier():
    classifier = IntentClassifier()

    r1 = classifier.classify("I need a password reset for my account")
    assert r1.target_agent_id == "A5_identity_access"
    assert r1.use_case_id == "UC-11"

    r2 = classifier.classify("My laptop screen is broken, please open a support ticket")
    assert r2.target_agent_id == "A1_service_desk"
    assert r2.use_case_id == "UC-02"

    r3 = classifier.classify("Where is the documentation for VPN setup?")
    assert r3.target_agent_id == "A2_knowledge"
    assert r3.use_case_id == "UC-05"

    r4 = classifier.classify("Hello there, good morning!")
    assert r4.target_agent_id == "A1_service_desk"
    assert r4.use_case_id == "UC-02"

def test_agent_router():
    registry = AgentRegistry()
    router = AgentRouter(registry=registry)

    agent_identity = AgentIdentity(
        agent_id="A1_service_desk",
        name="Service Desk Agent",
        domain="IT Support",
        role="Service Desk",
        description="L1/L2 Support",
        supported_use_cases=["UC-02", "UC-04"],
        service_principal_id="sp-a1"
    )
    agent = MockServiceDeskAgent(identity=agent_identity)
    registry.register(agent)

    # Route by target_agent_id
    intent_by_id = IntentClassificationResult(
        target_agent_id="A1_service_desk",
        use_case_id="UC-02"
    )
    assert router.route(intent_by_id) is agent

    # Route by use_case_id
    intent_by_uc = IntentClassificationResult(
        target_agent_id="unregistered_agent",
        use_case_id="UC-04"
    )
    assert router.route(intent_by_uc) is agent

    # Unmatched falls back to A1_service_desk
    unmatched_intent = IntentClassificationResult(
        target_agent_id="unknown_agent",
        use_case_id="UC-99"
    )
    assert router.route(unmatched_intent) is agent

@pytest.mark.asyncio
async def test_full_orchestration_flow():
    registry = AgentRegistry()
    agent_identity = AgentIdentity(
        agent_id="A1_service_desk",
        name="Service Desk Agent",
        domain="IT Support",
        role="Service Desk",
        description="L1/L2 Support",
        supported_use_cases=["UC-02"],
        service_principal_id="sp-a1"
    )
    agent = MockServiceDeskAgent(identity=agent_identity)
    registry.register(agent)

    router = AgentRouter(registry=registry)
    orchestrator = AllinaOrchestrator(router=router)

    context = AgentContext(
        tenant=TenantContext(tenant_id="tenant-test"),
        user=UserContext(user_id="u1", username="testuser", email="test@test.com")
    )

    # Standard query without action plan
    response = await orchestrator.handle_request(
        query="I have an issue with my office laptop",
        context=context
    )
    assert response.success is True
    assert response.agent_id == "A1_service_desk"
    assert "Service desk assisting" in response.response_text
    assert response.requires_approval is False

    # Query triggering an ActionManifest with T2 risk (requires approval)
    response_with_plan = await orchestrator.handle_request(
        query="Please restart the print spooler service",
        context=context
    )
    assert response_with_plan.success is True
    assert response_with_plan.requires_approval is True
    assert response_with_plan.manifest_id is not None
    assert response_with_plan.plan_hash is not None
