"""Tool contracts for AI Service Desk Agent (UC-02)"""
from app.automation.tool_gateway.contracts import ToolContract, ToolParameter
from app.automation.tool_gateway.registry import tool_registry
from app.governance.action_manifest import RiskTier

#1.Ticket Creation
ITSM_CREATE_TICKET = ToolContract(
    name="itsm_create_ticket",
    description="Create a new incident or service request in ServiceNow / Jira.",
    target_system="ELYSIUM_ITSM",
    is_read_only=False,
    risk_tier=RiskTier.T1,
    parameters=[
        ToolParameter(name="caller_id", type="string",description="User Id or email of caller"),
        ToolParameter(name="short_description", type="string", description="Brief summary of the issue"),
        ToolParameter(name="category", type="string", description="Issue category (e.g., Software, Hardware, Network)"),
        ToolParameter(name="urgency", type="string", description="Urgency: Low, Medium, High", default="Medium"),
    ],
)

# 2. Ticket Status Check
ITSM_GET_TICKET = ToolContract(
    name="itsm_get_ticket",
    description="Fetches current status and work notes of an ITSM ticket.",
    target_system="ELYSIUM_ITSM",
    is_read_only=True,
    risk_tier=RiskTier.T0,
    parameters=[
        ToolParameter(name="ticket_id", type="string", description="Incident or Request ID (e.g. INC0012345)"),
    ],
)

# 3. Endpoint Service Diagnostic Check
ENDPOINT_CHECK_SERVICE = ToolContract(
    name="endpoint_check_service",
    description="Checks the running status of a local client service (e.g., spooler, VPN client).",
    target_system="ELYSIUM_ENDPOINT",
    is_read_only=True,
    risk_tier=RiskTier.T0,
    parameters=[
        ToolParameter(name="endpoint_id", type="string", description="Target computer CI or hostname"),
        ToolParameter(name="service_name", type="string", description="Name of the OS service"),
    ],
)

# 4. Endpoint Service Remediation
ENDPOINT_RESTART_SERVICE = ToolContract(
    name="endpoint_restart_service",
    description="Restarts an endpoint client service with health pre/post-checks.",
    target_system="ELYSIUM_ENDPOINT",
    is_read_only=False,
    risk_tier=RiskTier.T2,
    parameters=[
        ToolParameter(name="endpoint_id", type="string", description="Target computer CI or hostname"),
        ToolParameter(name="service_name", type="string", description="Name of the OS service to restart"),
    ],
)
SERVICE_DESK_TOOLS = [
    ITSM_CREATE_TICKET,
    ITSM_GET_TICKET,
    ENDPOINT_CHECK_SERVICE,
    ENDPOINT_RESTART_SERVICE,
]
def register_service_desk_tools():
    """Registers A1 tools with the global tool registry."""
    for tool in SERVICE_DESK_TOOLS:
        tool_registry.register(tool)