"""Policy Engine and Risk Tier evaluation service (L5 Governance)."""
from typing import TYPE_CHECKING, Optional
from app.governance.action_manifest import ActionManifest, RiskTier

if TYPE_CHECKING:
    from app.agents.base.agent_context import AgentContext

class PolicyEngine:
    """
    Evaluates proposed action plans against organizational rules,
    least-privilege boundaries, and risk tiers (T0-T3).
    """

    def evaluate_manifest(
        self,
        manifest: ActionManifest,
        context: Optional["AgentContext"] = None
    ) -> ActionManifest:
        """
        Evaluate an ActionManifest:
        1. Computes the cryptographic plan hash.
        2. Derives overall risk tier (T0-T3) from the highest-risk step.
        3. Enforces human-approval gates for T2 and T3 tiers.
        """
        # Ensure cryptographic hash binding
        manifest.compute_plan_hash()

        # Determine highest risk tier across all proposed steps
        highest_tier = RiskTier.T0
        tier_hierarchy = {RiskTier.T0: 0, RiskTier.T1: 1, RiskTier.T2: 2, RiskTier.T3: 3}

        for step in manifest.steps:
            if tier_hierarchy[step.risk_tier] > tier_hierarchy[highest_tier]:
                highest_tier = step.risk_tier

        manifest.overall_risk_tier = highest_tier

        # Tier 2 and Tier 3 strictly require human approval
        if highest_tier in (RiskTier.T2, RiskTier.T3):
            manifest.requires_human_approval = True
        else:
            manifest.requires_human_approval = False

        return manifest

# Global singleton policy engine
policy_engine = PolicyEngine()
