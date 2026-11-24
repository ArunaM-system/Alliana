"""Unit tests for Tool Gateway and Governed Automation (L6)."""
import pytest
from app.automation.tool_gateway.contracts import ToolContract, ToolParameter
from app.automation.tool_gateway.gateway import ToolGateway
from app.automation.tool_gateway.registry import ToolRegistry, tool
from app.governance.action_manifest import RiskTier


@pytest.mark.asyncio
async def test_tool_registry_and_gateway():
    registry = ToolRegistry()
    gateway = ToolGateway(registry=registry)

    # Register tool via contract
    contract = ToolContract(
        name="lookup_kb",
        description="Search knowledge base articles",
        parameters=[ToolParameter(name="query", required=True)]
    )
    registry.register(contract, lambda query: f"Articles for '{query}'")

    assert registry.get("lookup_kb") is not None
    assert registry.validate_parameters("lookup_kb", {"query": "VPN issue"}) is True
    assert registry.validate_parameters("lookup_kb", {}) is False

    # Execute tool through gateway
    result = await gateway.execute(
        tool_name="lookup_kb",
        parameters={"query": "VPN issue"},
        tenant_id="tenant-1"
    )
    assert result["status"] == "success"
    assert result["result"] == "Articles for 'VPN issue'"

@pytest.mark.asyncio
async def test_tool_decorators():
    # 1. Test instance-level decorator (@registry.tool)
    registry = ToolRegistry()

    @registry.tool(
        name="ping_server_instance",
        description="Ping target hostname on custom registry",
        parameters=[ToolParameter(name="host", required=True)],
        risk_tier=RiskTier.T0
    )
    def ping_inst(host: str):
        return f"pong from {host}"

    assert hasattr(ping_inst, "contract")
    assert ping_inst.contract.name == "ping_server_instance"
    assert registry.get("ping_server_instance") is not None

    # 2. Test global module-level decorator (@tool)
    @tool(
        name="ping_server_global",
        description="Ping target hostname on global registry",
        parameters=[ToolParameter(name="host", required=True)],
        risk_tier=RiskTier.T0
    )
    def ping_global(host: str):
        return f"global pong from {host}"

    assert hasattr(ping_global, "contract")
    assert ping_global.contract.name == "ping_server_global"
