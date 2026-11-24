"""Specialist Agent Registry and dynamic discovery service (L3)."""
from typing import Dict, List, Optional
from app.agents.base.agent_identity import AgentIdentity
from app.agents.base.base_agent import BaseAgent

class AgentRegistry:
    """
    Central repository for registering, retrieving, and discovering specialist agents.
    Provides resolution by Agent ID and by Use Case ID.
    """

    def __init__(self):
        self._agents: Dict[str, BaseAgent] = {}

    def register(self, agent: BaseAgent) -> None:
        """Register a specialist agent instance."""
        self._agents[agent.agent_id] = agent

    def get(self, agent_id: str) -> Optional[BaseAgent]:
        """Retrieve an agent by its unique ID (e.g., 'A1_service_desk')."""
        return self._agents.get(agent_id)

    def get_or_raise(self, agent_id: str) -> BaseAgent:
        """Retrieve an agent or raise a KeyError if not found."""
        agent = self.get(agent_id)
        if not agent:
            raise KeyError(f"Specialist agent '{agent_id}' is not registered.")
        return agent

    def list_agents(self) -> List[AgentIdentity]:
        """List identities of all currently registered agents."""
        return [agent.identity for agent in self._agents.values()]

    def resolve_for_use_case(self, use_case_id: str) -> Optional[BaseAgent]:
        """Find the specialist agent registered to handle a given use case ID."""
        for agent in self._agents.values():
            if agent.can_handle(use_case_id):
                return agent
        return None

    def clear(self) -> None:
        """Clear all registered agents (primarily for testing purposes)."""
        self._agents.clear()
