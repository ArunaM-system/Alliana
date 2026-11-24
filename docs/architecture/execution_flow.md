# ALLINA – Execution Flow

The end-to-end execution flow for every request:
1. **Request Received**: Incoming event from Web UI, Teams, Slack, Mobile, Voice, or monitoring webhooks.
2. **Identity & Context Assembly**: Authenticated user identity validated; tenant context established from credentials (never arbitrary headers); environment retrieved.
3. **Orchestrator Routing**: Intent classified, task broken down, and routed to the appropriate specialist agent (A1–A12).
4. **Knowledge & Analysis**: Specialist agent retrieves relevant context from RAG knowledge, CMDB topology, and runbooks.
5. **Policy & Risk Validation**: Action proposed to L5 Governance. OPA evaluates policies, assigns risk tier (T0–T3), and determines if approval is needed.
6. **Human Approval**: If policy mandates human intervention (e.g. T2/T3), execution suspends pending approval via Temporal workflow.
7. **Governed Automation**: Upon authorization, L6 Tool Gateway triggers deterministic automation (Ansible, Terraform, API).
8. **Verification & Audit**: Automation post-checks confirm outcome; full immutable audit record written; ITSM ticket updated.
9. **Feedback**: Consolidated response returned to ALLINA Orchestrator and delivered to the original user/channel.
