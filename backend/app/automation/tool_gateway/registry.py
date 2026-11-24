"""Tool registry and validation services for Governed Automation (L6)."""
import os
import sys
from collections.abc import Callable
from typing import Any

# Ensure backend root directory is in sys.path for direct terminal execution
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from app.automation.tool_gateway.contracts import ToolContract, ToolParameter
from app.governance.action_manifest import RiskTier


class ToolRegistry:
    """
    Registry maintaining authorized tools, their input schemas,
    and their underlying execution callable handlers.
    """

    def __init__(self):
        self._contracts: dict[str, ToolContract] = {}
        self._handlers: dict[str, Callable] = {}

    def register(
        self,
        contract: ToolContract,
        handler: Callable | None = None
    ) -> None:
        """Register a tool contract with an optional execution handler."""
        self._contracts[contract.name] = contract
        if handler:
            self._handlers[contract.name] = handler

    def get(self, tool_name: str) -> ToolContract | None:
        """Retrieve a registered tool contract by name."""
        return self._contracts.get(tool_name)

    def get_handler(self, tool_name: str) -> Callable | None:
        """Retrieve the registered execution handler for a tool."""
        return self._handlers.get(tool_name)

    def list_tools(self) -> list[ToolContract]:
        """List all registered tool contracts."""
        return list(self._contracts.values())

    def validate_parameters(
        self,
        tool_name: str,
        parameters: dict[str, Any]
    ) -> bool:
        """Verify that provided parameters conform to the tool contract requirements."""
        contract = self.get(tool_name)
        if not contract:
            return False

        for param in contract.parameters:
            if param.required and param.default is None and param.name not in parameters:
                return False
        return True

    def tool(
        self,
        name: str,
        description: str,
        parameters: list[ToolParameter] | None = None,
        required_permissions: list[str] | None = None,
        target_system: str = "ELYSIUM",
        is_read_only: bool = True,
        risk_tier: RiskTier = RiskTier.T0
    ):
        """Decorator method to register a Python callable on this ToolRegistry instance."""
        def decorator(fn: Callable):
            contract = ToolContract(
                name=name,
                description=description,
                parameters=parameters or [],
                required_permissions=required_permissions or [],
                target_system=target_system,
                is_read_only=is_read_only,
                risk_tier=risk_tier
            )
            self.register(contract, fn)
            fn.contract = contract
            return fn
        return decorator

    def clear(self) -> None:
        """Clear all registered tools and handlers."""
        self._contracts.clear()
        self._handlers.clear()

# Global singleton tool registry
tool_registry = ToolRegistry()

# Module-level tool decorator bound to global singleton tool_registry
tool = tool_registry.tool

if __name__ == "__main__":
    print(f"ToolRegistry ready. Registered tools count: {len(tool_registry.list_tools())}")
