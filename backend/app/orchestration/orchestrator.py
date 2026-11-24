"""
Central ALLINA Orchestrator (Layer 2).
Coordinates intent classification, context building, agent routing, and governance checks.
"""
from typing import Any, Dict, Optional
from pydantic import BaseModel

from app.agents.base.agent_context import AgentContext
from app.agents.base.base_agent import AgentResponse
from app.agents.registry import agent_registry
from app.governance.policy.policy_engine import policy_engine
from app.orchestration.agent_router import AgentRouter
from app.orchestration.intent_classifier import IntentClassifier, IntentClassificationResult

class OrchestratorResponse(BaseModel):
    """Final unified response delivered to L1 Entry Points."""
    success: bool
    agent_id: Optional[str] = None
    use_case_id: Optional[str] = None
    response_text: str
    requires_approval: bool = False
    manifest_id: Optional[str] = None
    plan_hash: Optional[str] = None
    metadata: Dict[str, Any] = {}

class AllinaOrchestrator:
    """
    Core platform coordinator.
    Traverses the lifecycle: User Request -> Intent -> Specialist Agent -> Governance -> Response.
    """

    def __init__(
        self,
        classifier: Optional[IntentClassifier] = None,
        router: Optional[AgentRouter] = None,
    ):
        self.classifier = classifier or IntentClassifier()
        self.router = router or AgentRouter()

    async def handle_request(
        self,
        query: str,
        context: AgentContext
    ) -> OrchestratorResponse:
        """Execute end-to-end orchestration for an incoming user request."""
        # Step 1: Classify user intent
        intent: IntentClassificationResult = self.classifier.classify(query)

        # Step 2: Route to appropriate specialist agent
        agent = self.router.route(intent)
        if not agent:
            return OrchestratorResponse(
                success=True,
                agent_id=intent.target_agent_id,
                use_case_id=intent.use_case_id,
                response_text=(
                    f"Request classified under intent '{intent.detected_intent}' (Use Case: {intent.use_case_id}). "
                    f"Agent '{intent.target_agent_id}' is scheduled for implementation in this phase."
                ),
                metadata={"confidence": intent.confidence}
            )

        # Step 3: Execute cognitive reasoning on specialist agent
        await agent.pre_reason(context)
        agent_res: AgentResponse = await agent.reason(
            context=context,
            input_text=query,
            use_case_id=intent.use_case_id
        )
        agent_res = await agent.post_reason(agent_res, context)

        # Step 4: If agent produced an action plan, evaluate through L5 Governance
        requires_approval = False
        manifest_id = None
        plan_hash = None

        if agent_res.action_manifest:
            manifest = policy_engine.evaluate_manifest(agent_res.action_manifest, context)
            requires_approval = manifest.requires_human_approval
            manifest_id = manifest.manifest_id
            plan_hash = manifest.plan_hash

        return OrchestratorResponse(
            success=True,
            agent_id=agent.agent_id,
            use_case_id=intent.use_case_id,
            response_text=agent_res.response_text,
            requires_approval=requires_approval,
            manifest_id=manifest_id,
            plan_hash=plan_hash,
            metadata=agent_res.metadata
        )

# Global singleton orchestrator
orchestrator = AllinaOrchestrator()
