---
name: project-intake-and-charter
description: >
  Project Intake & Charter: transform an ambiguous project request into a
  clear, structured project foundation for consulting engagements. Use when a
  project is in the **Initiation** phase or when a PM needs to clarify objectives,
  scope, stakeholders, assumptions, initial risks and open questions without
  performing detailed planning or estimations.
---

# Project Intake & Charter (Initiation Phase)

Purpose
- Transform an ambiguous project request into a clear, structured project
  foundation that the PM Core Agent and downstream skills can rely on.
- This skill does NOT plan, estimate in detail, or make final decisions. Its
  job is to make implicit information explicit.

Scope: What this skill does and does not do
- This skill WILL:
  - Clarify the real problem being solved
  - Identify business objectives (distinct from solutions)
  - Define measurable success criteria
  - Explicitly state in-scope and out-of-scope items
  - Surface assumptions and constraints
  - Identify key stakeholders
  - Identify initial project risks
  - Detect critical information gaps and create clarifying questions
  - Produce, when requested or when the project will include cutover/production work, a high-level `workplan-and-estimate.md` (WBS + hours + cost estimate) to be used for Owner approval prior to execution.

- This skill WILL NOT:
  - Produce detailed plans
  - Provide fine-grained estimates
  - Make final business decisions or negotiate with stakeholders
  - Send formal external communications

Inputs

- **project_state.md**: A Markdown document following the template in `project-state.md`.
- **user_input**: Fragmented or ambiguous project request.

Notes
- `project-state.md` may be incomplete or partially populated.
- `user_input` may be informal, fragmented, or ambiguous.
- The skill must tolerate ambiguity and avoid inventing facts.

Outputs (contract)
1. **New File**: `project-charter.md` (The human-readable Project Definition).
2. **Updated File**: `project-state.md` (The operational context).

# Output 1: Project Charter (`project-charter.md`)
Follows standard Project Charter format:
- **Project Name & Metadata**
- **Problem Statement** & **Business Objectives**
- **Scope** (In/Out)
- **Key Stakeholders**
- **High-Level Risks**
- **Approval Sign-off Section**

# Output 2: Updated Project State (`project-state.md`)
Updates specific sections of the state to reflect the new definition:
- `## Objectives` (Synced from Charter)
- `## Scope` (Synced from Charter)
- `## Execution Log`:
  - `history_summary`: Added "Project Charter created."
  - `current_action`: "Reviewing Charter with stakeholders."
  - `next_actions`: "Obtain approval", "Initiate High-Level Planning."
- `## active_questions`: (If any)

If a `workplan-and-estimate.md` is generated, the Execution Log must record its creation and the approval request; add a `next_action`: "Await Owner approval (48 h)".

---

Guardrails (must follow)
1. **Charter != Plan**: The Charter defines *what* and *why*. It does NOT define *how* (detailed plan) or *when* (schedule).
2. **State = Brain**: Do not put the full narrative in the state. Put the structural facts needed for decision making.
3. If information is missing for the Charter, ask Clarifying Questions instead of inventing it.

Skill prompt (use this prompt when invoking the skill)
```
You are a Project Intake & Charter skill.

Task:
1. Analyze `project_state.md` and `user_input`.
2. Generate a valid `project-charter.md` file content defined as the Project Definition (Not a Plan).
3. Generate the update for `project-state.md` populating Objectives, Scope, and the Execution Log.

Input Constraints:
- Do NOT create a detailed WBS or Schedule yet. Focus on alignment and definition.

Output Format:
Provide the content for the two files clearly separated.
```

Example execution (realistic)

**Output**
File: `project-charter.md` (excerpts)
> # Project Charter: Data Migration
> ## Problem
> Reporting is slow...
> ## Scope
> ...

File: `project-state.md` (updates)
> ## Objectives
> ...
> ## Execution Log
> - last_action: created project-charter.md
> - current_action: waiting for user approval of charter
```
