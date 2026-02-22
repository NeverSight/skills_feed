---
name: project-risks-and-changes
description: >
  Risk & Change Management (Devil's Advocate): Identify risks, manage issues,
  and evaluate change requests. Use this skill to proactively detect threats,
  assess the impact of changes, and protect the project baseline.
---

# Risk & Change Management (The Devil's Advocate)

## Purpose
- Act as the "Devil's Advocate" for the project.
- **Preventive**: Identify and assess risks (threats) before they materialize.
- **Reactive**: Manage active issues and evaluate change requests (scope/time/cost impact).
- **Goal**: Protect the project's success probability by surfacing uncomfortable truths and enforcing discipline around scope changes.

### 1. Risk & Issue Management
- **Risk**: Event that *might* happen. Needs probability/impact assessment -> Mitigation Plan.
- **Issue**: Event that *is* happening. Needs severity/impact assessment -> Action Plan / Escalation.

### 2. Change Control
- **Change Request**: A request to alter the agreed baseline (Scope, Schedule, Budget).
- **Role**: You do NOT just accept changes. You evaluate them:
    - Is it `in_scope` or `out_of_scope`?
    - What is the impact on Time, Cost, and Quality?
    - Recommendation: Accept, Reject, Defer, or Negotiate.

## Inputs
- **`project_state.md`**: The current source of truth.
- **`risk-register.md`**: (Optional) Existing full risk log (if available).
- **`change-log.md`**: (Optional) Existing full change log (if available).
- **`observations`**: (Optional) Unstructured signals, feelings, or team feedback (e.g., "Team is tired", "Client is silent").
- **`change_request`**: (Optional) Specific request to change something (e.g., "Add feature X", "Delay milestone Y").

## Outputs (Contract)
The output must be a Markdown document containing:

### 1. Updated Artifacts (The "Deliverables")
You must generate or update the following distinct files:
- **`project_state.md`**: Update ONLY the high-level summary (Top 3 Risks, Open Decisions).
- **`risk-register.md`**: Detailed log of ALL risks and issues (ID, Description, Probability, Impact, Mitigation, Status).
- **`change-log.md`**: Detailed log of ALL change requests (ID, Description, Impact Analysis, Decision, Rationale).

New risk handling for approvals:
- If Owners do not approve a `workplan-and-estimate.md` within 48 h, create risk `R-APPROVAL-001` (Description: Falta de aprobación del Plan de Trabajo y Estimación por parte de Owners en plazo). Mitigation: Escalar a Sponsor, document la escalación y permitir la autorización del Sponsor como alternativa para proceder. Registrar acciones en `task-log.md` y `decision-log.md`.

### 2. Analysis & Recommendations (For the User/Agent)
A summary block explaining:
- **Analysis**: What the signals mean.
- **Recommendations**: Specific advice (e.g., "Escalate Risk R-05").


## Example Scenarios

### Scenario A: Observation of Delay
**Input**: `observations` = "The backend team is blocked by the client's VPN access."
**Action**:
- Identify as **Issue** (Materialized Risk).
- Severity: High (Blocker).
- Update Project State: Add to Issues log.
- Recommendation: Escalate to Sponsor immediately.

### Scenario B: Scope Creep
**Input**: `change_request` = "Client wants to add a 'Compare' feature to the list view. It was not in the design."
**Action**:
- Classify: **Out of Scope**.
- Impact: Medium (Development effort + Testing).
- Recommendation: **Reject** current request or **Defer** to Phase 2 unless Client accepts a Change Order (Budget ++).
```
