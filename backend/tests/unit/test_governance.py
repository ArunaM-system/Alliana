"""Unit tests for Trust & Governance (L5), ActionManifest, and Risk Tiers."""
import pytest
from app.governance.action_manifest import ActionManifest, ActionStep, RiskTier
from app.governance.policy.policy_engine import PolicyEngine
from app.governance.approvals.token_validator import create_approval_token, verify_approval_token

def test_action_manifest_hash_integrity():
    manifest = ActionManifest(
        agent_id="A1_service_desk",
        tenant_id="tenant-test",
        use_case_id="UC-02",
        description="Restart print spooler"
    )
    manifest.steps.append(
        ActionStep(
            tool_name="restart_service",
            parameters={"service_name": "spooler"},
            risk_tier=RiskTier.T1
        )
    )

    hash1 = manifest.compute_plan_hash()
    assert hash1 is not None and len(hash1) == 64

    # Modifying parameters must produce a different hash
    manifest.steps[0].parameters["service_name"] = "critical_daemon"
    hash2 = manifest.compute_plan_hash()
    assert hash1 != hash2

def test_policy_engine_risk_tiering():
    engine = PolicyEngine()

    # T0 plan
    m_t0 = ActionManifest(
        agent_id="A2_knowledge",
        tenant_id="tenant-1",
        use_case_id="UC-05",
        description="Search KB"
    )
    m_t0.steps.append(ActionStep(tool_name="search_kb", risk_tier=RiskTier.T0))
    res_t0 = engine.evaluate_manifest(m_t0)
    assert res_t0.overall_risk_tier == RiskTier.T0
    assert res_t0.requires_human_approval is False

    # T2 plan requires approval
    m_t2 = ActionManifest(
        agent_id="A7_remediation",
        tenant_id="tenant-1",
        use_case_id="UC-33",
        description="Restart database"
    )
    m_t2.steps.append(ActionStep(tool_name="restart_service", risk_tier=RiskTier.T2))
    res_t2 = engine.evaluate_manifest(m_t2)
    assert res_t2.overall_risk_tier == RiskTier.T2
    assert res_t2.requires_human_approval is True

def test_approval_token_verification():
    manifest = ActionManifest(
        agent_id="A7_remediation",
        tenant_id="tenant-enterprise",
        use_case_id="UC-33",
        description="Emergency server reboot"
    )
    manifest.steps.append(ActionStep(tool_name="reboot_server", risk_tier=RiskTier.T2))
    manifest.compute_plan_hash()

    token = create_approval_token(
        manifest_id=manifest.manifest_id,
        plan_hash=manifest.plan_hash,
        approver_id="manager-42",
        tenant_id="tenant-enterprise"
    )

    assert verify_approval_token(token, manifest) is True

    # Tampered plan hash must fail verification
    manifest.steps[0].parameters["force"] = True
    manifest.compute_plan_hash()
    assert verify_approval_token(token, manifest) is False
