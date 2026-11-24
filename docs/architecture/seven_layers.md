# ALLINA – Seven Architectural Layers

| Layer | Name | Description | Key Modules |
| :--- | :--- | :--- | :--- |
| **L1** | Entry Points | User interfaces, public REST APIs, and chat/voice channels | `api/v1/`, `frontend/`, channels |
| **L2** | ALLINA Orchestrator | Central coordinator for intent classification, planning, and agent routing | `orchestration/` |
| **L3** | Specialist Agents | 12 dedicated IT operations AI agents (A1 to A12) | `agents/` |
| **L4** | Shared Intelligence & Context | Knowledge retrieval, CMDB topology, runbooks, and LLM gateway | `shared_services/` |
| **L5** | Trust & Governance | Identity, RBAC/ABAC, OPA policies, approvals, audit, and tenant isolation | `governance/` |
| **L6** | Governed Automation | MCP client, tool gateway, durable workflows (Temporal), and execution engines | `automation/` |
| **L7** | ELYSIUM Environment | External enterprise integrations (ITSM, AD, AWS, Azure, GCP, Networks, DBs) | `integrations/` |
