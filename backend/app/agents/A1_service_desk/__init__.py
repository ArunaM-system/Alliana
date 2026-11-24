"""A1 Service Desk Agent package."""
from app.agents.A1_service_desk.agent import ServiceDeskAgent

service_desk_agent = ServiceDeskAgent()

__all__ = ["ServiceDeskAgent", "service_desk_agent"]