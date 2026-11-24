"""Central Specialist Agent Registry instance for ALLINA platform."""
from app.agents.base.agent_registry import AgentRegistry
from app.agents.A1_service_desk import service_desk_agent

agent_registry = AgentRegistry()

# Register A1 Service Desk Agent
agent_registry.register(service_desk_agent)
