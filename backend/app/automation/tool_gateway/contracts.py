"""Tool definition contracts and parameters for Governed Automation (L6)."""
import os
import sys
from typing import Any

# Ensure backend root directory is in sys.path for direct terminal execution
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from pydantic import BaseModel, Field

from app.governance.action_manifest import RiskTier


class ToolParameter(BaseModel):
    """Parameter schema specification for an automation tool."""
    name: str
    type: str = "string"
    description: str = ""
    required: bool = True
    default: Any = None

class ToolContract(BaseModel):
    """Specification of an authorized deterministic tool callable by agents."""
    name: str
    description: str
    parameters: list[ToolParameter] = Field(default_factory=list)
    required_permissions: list[str] = Field(default_factory=list)
    target_system: str = "ELYSIUM"
    is_read_only: bool = True
    risk_tier: RiskTier = RiskTier.T0
