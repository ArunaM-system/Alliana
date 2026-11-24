"""Action Manifest schemas and Risk Tier definitions (L5 Governance)."""
from datetime import datetime, timezone
from enum import Enum
import hashlib
import json
from typing import Any, Dict, List, Optional
import uuid
from pydantic import BaseModel, Field

def get_utc_now() -> datetime:
    return datetime.now(timezone.utc)

class RiskTier(str, Enum):
    """
    Risk Tiers defining governance and human-approval boundaries.
    T0: Read-Only / Autonomous query (no approval needed).
    T1: Low Risk / Standard idempotent change (auto-approved, audit logged).
    T2: Medium Risk (requires single human approval before execution).
    T3: High Risk / Critical Infrastructure (requires CAB/multi-party approval).
    """
    T0 = "T0"
    T1 = "T1"
    T2 = "T2"
    T3 = "T3"

class ActionStep(BaseModel):
    """Single discrete execution step within an agent's proposed plan."""
    step_id: str = Field(default_factory=lambda: f"step-{uuid.uuid4().hex[:8]}")
    tool_name: str
    parameters: Dict[str, Any] = Field(default_factory=dict)
    description: str = ""
    target_system: str = "ELYSIUM"
    rollback_tool: Optional[str] = None
    rollback_parameters: Optional[Dict[str, Any]] = None
    risk_tier: RiskTier = RiskTier.T0

class ActionManifest(BaseModel):
    """
    Standardized execution plan produced by specialist agents (L3)
    and authorized by governance (L5) before execution by automation (L6).
    """
    manifest_id: str = Field(default_factory=lambda: f"manifest-{uuid.uuid4().hex[:12]}")
    agent_id: str
    tenant_id: str
    use_case_id: str
    description: str
    overall_risk_tier: RiskTier = RiskTier.T0
    requires_human_approval: bool = False
    approval_token: Optional[str] = None
    steps: List[ActionStep] = Field(default_factory=list)
    plan_hash: str = ""
    created_at: datetime = Field(default_factory=get_utc_now)

    def compute_plan_hash(self) -> str:
        """
        Compute SHA-256 cryptographic hash over execution parameters to prevent tampering.
        Binds steps, tool names, and parameter payloads.
        """
        canonical_representation = [
            {
                "tool_name": step.tool_name,
                "parameters": step.parameters,
                "target_system": step.target_system,
                "risk_tier": step.risk_tier.value,
            }
            for step in self.steps
        ]
        serialized = json.dumps(canonical_representation, sort_keys=True)
        computed_hash = hashlib.sha256(serialized.encode("utf-8")).hexdigest()
        self.plan_hash = computed_hash
        return computed_hash
