# ALLINA – 12 Specialist Agents Architecture

| Agent ID | Name | Primary Domain | Core Use Cases |
| :--- | :--- | :--- | :--- |
| **A1** | Service Desk | L1/L2 Support & Service Requests | UC-02, UC-04, UC-07, UC-08, UC-09, UC-24 (shared), UC-25, UC-26, UC-27, UC-43 (shared) |
| **A2** | Knowledge | Grounded Q&A and Knowledge Articles | UC-05 |
| **A3** | Triage | Alert Enrichment & Incident Classification | UC-01, UC-16, UC-28, UC-34 |
| **A4** | Investigation (AI SRE) | Deep Diagnosis & Root Cause Analysis | UC-03, UC-35, UC-42 |
| **A5** | Identity & Access | Password Resets & Lifecycle Management | UC-11, UC-12 |
| **A6** | Provisioning & Config | VM Provisioning & Infrastructure IaC | UC-13, UC-15, UC-29, UC-30, UC-31, UC-44 |
| **A7** | Remediation | Governed Runbook Execution | UC-20, UC-21, UC-22, UC-23, UC-33 |
| **A8** | Patch & Security Posture | Upgrades, Patching & CIS Baselines | UC-18, UC-19, UC-32 |
| **A9** | Capacity & FinOps | Workload Auto-Scaling & Cost Governance | UC-17, UC-36, UC-37 |
| **A10** | Data & Reporting | NL-to-SQL Queries & Operational Reports | UC-10, UC-14, UC-38 |
| **A11** | DevOps & Platform | Developer Self-Service & CI/CD Pipelines | UC-24 (shared), UC-39, UC-40, UC-41, UC-45 |
| **A12** | Employee Services | Enterprise Services & Travel Management | UC-06, UC-43 (shared) |

### Shared Use Cases Policy
- **UC-24**: Shared by A1 (Service Desk) and A11 (DevOps & Platform). Implemented once in shared workflows and reused.
- **UC-43**: Shared by A1 (Service Desk) and A12 (Employee Services). Implemented once in shared workflows and reused.
