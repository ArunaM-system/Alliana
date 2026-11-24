"""Concrete A1 Service Desk Agent implementing UC-02."""
from typing import Any, Dict, List, Optional

from app.agents.base.agent_context import AgentContext
from app.agents.base.agent_identity import AgentIdentity
from app.agents.base.base_agent import AgentResponse, BaseAgent
from app.agents.A1_service_desk.prompts import SERVICE_DESK_SYSTEM_PROMPT
from app.agents.A1_service_desk.tools import SERVICE_DESK_TOOLS, register_service_desk_tools
from app.governance.action_manifest import ActionManifest, ActionStep, RiskTier


class ServiceDeskAgent(BaseAgent):
    """Specialist Agent A1: Level 1 / Level 2 IT Support (UC-02)."""

    def __init__(self, tools: Optional[List[Any]] = None):
        identity = AgentIdentity(
            agent_id="A1_service_desk",
            name="Service Desk Agent",
            domain="IT Operations",
            role="L1/L2 IT Support & Triage",
            description="First-contact resolution, triage, and standard user support workflows.",
            supported_use_cases=[
                "UC-02",  # Level 1 / Level 2 Support
                "UC-04",  # End-User Support
                "UC-07",  # Service Management
                "UC-08",  # Request Management
                "UC-09",  # IT Support
                "UC-24",  # Self-Service Application Management (shared with A11)
                "UC-25",  # Mobile Self-Service
                "UC-26",  # Voice Self-Service
                "UC-27",  # Voice-Assisted ITSM
                "UC-43",  # Integrated Service Management (shared with A12)
            ],
            service_principal_id="sp-a1-servicedesk"
        )
        register_service_desk_tools()
        super().__init__(identity=identity, tools=tools or SERVICE_DESK_TOOLS)

    async def reason(
        self,
        context: AgentContext,
        input_text: str,
        use_case_id: Optional[str] = None,
        **kwargs
    ) -> AgentResponse:
        """
        Cognitive reasoning for user support queries.
        Evaluates symptom, determines self-service guidance, or drafts an action plan.
        """
        text_lower = input_text.lower()
        use_case = use_case_id or "UC-02"

        if any(w in text_lower for w in ["database down", "prod crash", "server outage", "data breach"]):
            return AgentResponse(
                agent_id=self.agent_id,
                use_case_id=use_case,
                response_text=(
                    "This issue appears to be a critical infrastructure incident exceeding standard Level 1/2 scope. "
                    "I am flagging this for immediate escalation to Level 3 / Incident Investigation."
                ),
                confidence=0.95,
                handoff_required=True,
                suggested_next_steps=["Escalate to A4 Investigation Agent", "Notify on-call SRE lead"]
            )

        action_manifest = None
        if any(w in text_lower for w in ["ticket", "incident", "restart", "fix", "repair"]):
            action_manifest = await self.plan(context, input_text, use_case)

        response_text = (
            f"Hello {context.user.username}, I am your Service Desk Assistant. "
            f"I have reviewed your request regarding: '{input_text}'. "
        )
        if action_manifest:
            response_text += f"I have formulated an action plan ({action_manifest.manifest_id}) with risk tier {action_manifest.overall_risk_tier.value}."
        else:
            response_text += "Please verify your network connection or try restarting the affected application."

        return AgentResponse(
            agent_id=self.agent_id,
            use_case_id=use_case,
            response_text=response_text,
            action_manifest=action_manifest,
            confidence=0.90,
            suggested_next_steps=[
                "Check endpoint service status",
                "Log ITSM incident ticket"
            ]
        )

    async def plan(
        self,
        context: AgentContext,
        input_text: str,
        use_case_id: str,
        **kwargs
    ) -> ActionManifest:
        """
        Builds a structured ActionManifest with deterministic steps and risk tiers.
        """
        text_lower = input_text.lower()
        manifest = ActionManifest(
            agent_id=self.agent_id,
            tenant_id=context.tenant.tenant_id,
            use_case_id=use_case_id,
            description=f"Service desk support plan for: {input_text}"
        )

        if "restart" in text_lower or "spooler" in text_lower:
            manifest.steps.append(
                ActionStep(
                    tool_name="endpoint_check_service",
                    parameters={"endpoint_id": "ws-client-01", "service_name": "spooler"},
                    description="Check Print Spooler service status on user workstation",
                    target_system="ELYSIUM_ENDPOINT",
                    risk_tier=RiskTier.T0
                )
            )
            manifest.steps.append(
                ActionStep(
                    tool_name="endpoint_restart_service",
                    parameters={"endpoint_id": "ws-client-01", "service_name": "spooler"},
                    description="Restart Print Spooler service",
                    target_system="ELYSIUM_ENDPOINT",
                    risk_tier=RiskTier.T2,  # T2 requires human approval
                    rollback_tool="endpoint_check_service",
                    rollback_parameters={"endpoint_id": "ws-client-01", "service_name": "spooler"}
                )
            )
            manifest.overall_risk_tier = RiskTier.T2
            manifest.requires_human_approval = True
        else:
            manifest.steps.append(
                ActionStep(
                    tool_name="itsm_create_ticket",
                    parameters={
                        "caller_id": context.user.email,
                        "short_description": input_text,
                        "category": "Service Desk",
                        "urgency": "Medium"
                    },
                    description="Create ITSM incident ticket for user request",
                    target_system="ELYSIUM_ITSM",
                    risk_tier=RiskTier.T1  
                )
            )
            manifest.overall_risk_tier = RiskTier.T1
            manifest.requires_human_approval = False

        manifest.compute_plan_hash()
        return manifest