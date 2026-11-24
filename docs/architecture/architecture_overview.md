# ALLINA – Platform Architecture Overview

## Executive Summary
ALLINA is a multi-tenant, AI-powered IT operations platform built across 7 architectural layers (L1–L7). It combines a central orchestrator, 12 specialist agents (A1–A12), 45 IT automation use cases, shared intelligence services, and cross-cutting governance to interact safely with enterprise infrastructure (the ELYSIUM estate).

## Core Principle
**AI plans, policy authorises, people approve when needed, tested automation executes, everything is recorded.**
- Agents decide and coordinate.
- Governance authorises.
- Automation executes.
- Integrations connect to existing IT systems.
- Agents NEVER access production systems directly. All changes traverse:
  `Policy check -> Approval (if required) -> Tool/MCP gateway -> Deterministic automation -> Verification -> Audit`

## Architectural Layers
- **L1: Entry Points (`api/` + `frontend/` + channels)**: Web UI, APIs, Teams, Slack, Mobile, Voice.
- **L2: Central Orchestrator (`orchestration/`)**: Intent classification, context building, agent routing, task planning.
- **L3: Specialist Agents (`agents/`)**: 12 specialist AI agents (A1–A12).
- **L4: Shared Intelligence (`shared_services/`)**: Knowledge retrieval (RAG + pgvector), CMDB service graph, LLM gateway, telemetry.
- **L5: Trust & Governance (`governance/`)**: Tenant isolation, OPA/Rego policy engine (T0–T3), human approvals, audit trail.
- **L6: Governed Automation (`automation/`)**: Tool gateway, MCP client, workflow engine (Temporal), Ansible/Terraform executors.
- **L7: ELYSIUM Integrations (`integrations/`)**: Enterprise connectors (ITSM, Active Directory, Entra ID, Cloud, Networks, Servers).
