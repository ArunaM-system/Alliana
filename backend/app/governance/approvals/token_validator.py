"""Cryptographic approval token generator and validator (L5 Governance)."""
import base64
import hashlib
import hmac
import json
import time
from typing import Dict, Any, Optional
from app.governance.action_manifest import ActionManifest

DEFAULT_SECRET = "allina-governance-hmac-secret-key-v1"

def create_approval_token(
    manifest_id: str,
    plan_hash: str,
    approver_id: str,
    tenant_id: str,
    secret_key: str = DEFAULT_SECRET,
    expires_in_seconds: int = 900
) -> str:
    """
    Generate a cryptographically signed approval token binding the plan hash.
    Ensures that any change in execution parameters invalidates the approval.
    """
    payload = {
        "manifest_id": manifest_id,
        "plan_hash": plan_hash,
        "approver_id": approver_id,
        "tenant_id": tenant_id,
        "exp": int(time.time()) + expires_in_seconds
    }
    payload_json = json.dumps(payload, sort_keys=True)
    payload_b64 = base64.urlsafe_b64encode(payload_json.encode()).decode().rstrip("=")
    signature = hmac.new(
        secret_key.encode(),
        payload_b64.encode(),
        hashlib.sha256
    ).hexdigest()
    return f"{payload_b64}.{signature}"

def verify_approval_token(
    token: str,
    manifest: ActionManifest,
    secret_key: str = DEFAULT_SECRET
) -> bool:
    """
    Verify the cryptographic signature, expiration, and plan hash binding.
    Returns True only if token matches and is unexpired and parameters are unaltered.
    """
    if not token or "." not in token:
        return False

    payload_b64, signature = token.split(".", 1)
    expected_sig = hmac.new(
        secret_key.encode(),
        payload_b64.encode(),
        hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(signature, expected_sig):
        return False

    # Decode payload
    padding = "=" * (4 - len(payload_b64) % 4)
    try:
        payload_bytes = base64.urlsafe_b64decode(payload_b64 + padding)
        payload = json.loads(payload_bytes.decode())
    except Exception:
        return False

    # Check expiration
    if time.time() > payload.get("exp", 0):
        return False

    # Check tenant and plan hash match
    current_hash = manifest.plan_hash or manifest.compute_plan_hash()
    if payload.get("plan_hash") != current_hash:
        return False

    if payload.get("tenant_id") != manifest.tenant_id:
        return False

    return True
