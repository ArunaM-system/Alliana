# ALLINA – Unified AI-Powered IT Operations Platform

## Overview
ALLINA is an enterprise-grade, multi-tenant AI platform designed for automated IT operations across 7 architectural layers:
- **L1: Entry Points**: REST APIs (`backend/app/api/v1/`) and modern React UI (`frontend/`)
- **L2: Central Orchestrator**: Intent classification, context construction, and dynamic agent routing (`backend/app/orchestration/`)
- **L3: Specialist Agents**: 12 dedicated AI agents (A1 Service Desk through A12 Employee Services) (`backend/app/agents/`)
- **L4: Shared Intelligence**: RAG knowledge base, CMDB service topology, and LLM gateway (`backend/app/shared_services/`)
- **L5: Trust & Governance**: Multi-tenant isolation, OPA policy engine, approval matrix, and immutable audit logs (`backend/app/governance/`)
- **L6: Governed Automation**: MCP client, Temporal durable workflows, and execution runners (`backend/app/automation/`)
- **L7: ELYSIUM Integrations**: Enterprise connectors for ITSM, Active Directory, Cloud, and Infrastructure (`backend/app/integrations/`)

---

## Getting Started

### 1. Environment Configuration
Copy the template configuration:
```bash
cp .env.example .env
```

### 2. Running Services with Docker Compose
```bash
docker compose up --build
```
- **Backend API**: [http://localhost:8000](http://localhost:8000)
- **API Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Frontend Dashboard**: [http://localhost:5173](http://localhost:5173)

### 3. Database Migrations
```bash
cd backend
alembic upgrade head
```

### 4. Running Automated Tests
```bash
pytest backend/tests
```
