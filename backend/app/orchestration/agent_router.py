"""Dynamic agent routing service (L2 Central Orchestrator)."""
from typing import Optional
from app.agents.base.base_agent import BaseAgent
from app.agents.registry import agent_registry
from app.orchestration.intent_classifier import IntentClassificationResult

class AgentRouter:
    """Routes classified requests to registered Specialist Agents."""

    def __init__(self, registry=agent_registry):
        self.registry = registry

    def route(self, intent: IntentClassificationResult) -> Optional[BaseAgent]:
        """Resolve the target agent from intent classification."""
        if intent.target_agent_id:
            agent = self.registry.get(intent.target_agent_id)
            if agent:
                return agent

        if intent.use_case_id:
            agent = self.registry.resolve_for_use_case(intent.use_case_id)
            if agent:
                return agent

        # Fallback to A1 Service Desk if registered
        return self.registry.get("A1_service_desk")
