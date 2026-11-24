"""Intent classification engine for L2 Central Orchestrator."""
import re
from typing import Dict, Optional, Tuple
from pydantic import BaseModel

class IntentClassificationResult(BaseModel):
    """Result of classifying user intent against use cases and agents."""
    use_case_id: Optional[str] = None
    target_agent_id: Optional[str] = None
    confidence: float = 1.0
    detected_intent: str = "general_inquiry"

class IntentClassifier:
    """
    Classifies user inputs to select the specialist domain agent (A1 through A12)
    and specific use case (UC-01 through UC-45).
    """

    KEYWORD_MAPPINGS = [
        # A1: Service Desk
        (r"(support|ticket|issue|help desk|laptop|printer|service request)", "UC-02", "A1_service_desk"),
        # A2: Knowledge
        (r"(documentation|article|kb|how do i|search knowledge|sop)", "UC-05", "A2_knowledge"),
        # A3: Triage
        (r"(alert|metric spike|pagerduty|datadog|noise reduction|high cpu alert)", "UC-01", "A3_triage"),
        # A4: Investigation
        (r"(root cause|rca|outage diagnosis|investigate crash|deep dive)", "UC-03", "A4_investigation"),
        # A5: Identity & Access
        (r"(password reset|unlock account|mfa|access request|onboard user)", "UC-11", "A5_identity_access"),
        # A6: Provisioning & Config
        (r"(provision vm|create server|snapshot|golden image|terraform plan)", "UC-13", "A6_provisioning_config"),
        # A7: Remediation
        (r"(restart service|clear disk space|kill process|restart server|heal)", "UC-33", "A7_remediation"),
        # A8: Patch & Security
        (r"(patch|cve|vulnerability|security baseline|upgrade kernel)", "UC-19", "A8_patch_security"),
        # A9: Capacity & FinOps
        (r"(scale up|cost optimization|aws bill|idle resources|finops)", "UC-17", "A9_capacity_finops"),
        # A10: Data & Reporting
        (r"(generate report|kpi report|sql query|analytics dashboard)", "UC-10", "A10_data_reporting"),
        # A11: DevOps & Platform
        (r"(ci/cd|deploy pipeline|release build|developer portal)", "UC-40", "A11_devops_platform"),
        # A12: Employee Services
        (r"(flight booking|hotel reservation|travel request|corporate travel)", "UC-06", "A12_employee_services"),
    ]

    def classify(self, text: str) -> IntentClassificationResult:
        """Analyze text and determine use case ID and specialist agent."""
        text_lower = text.lower()
        for pattern, uc_id, agent_id in self.KEYWORD_MAPPINGS:
            if re.search(pattern, text_lower):
                return IntentClassificationResult(
                    use_case_id=uc_id,
                    target_agent_id=agent_id,
                    confidence=0.95,
                    detected_intent=pattern
                )

        # Default fallback to A1 Service Desk
        return IntentClassificationResult(
            use_case_id="UC-02",
            target_agent_id="A1_service_desk",
            confidence=0.5,
            detected_intent="general_support"
        )
