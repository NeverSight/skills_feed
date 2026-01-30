---
name: openspec-change-proposal
description: Creates lightweight proposals for L0-1 work.
allowed-tools: ["Read", "Write", "Grep", "Bash"]
metadata:
  auto-invoke: true
  triggers:
    patterns:
      - "fix bug"
      - "small change"
      - "quick feature"
      - "simple fix"
      - "minor update"
    keywords:
      - bug
      - fix
      - small
      - quick
      - simple
      - minor
      - lightweight
  capabilities:
    - proposal-creation
    - change-scoping
    - task-definition
    - lightweight-planning
  prerequisites: []
  outputs:
    - proposal
    - tasks
    - spec-delta
---

# OpenSpec Propose Skill

## When to Invoke

**Automatically activate when user:**
- Says "Fix this bug", "Small change", "Quick feature"
- Asks "Simple fix for [issue]", "Minor update to [component]"
- Mentions "bug fix", "small improvement", "quick change"
- Has a Level 0-1 scoped change (small, low risk, no major unknowns)
- Uses words like: bug, fix, small, quick, simple, minor, lightweight

**Specific trigger phrases:**
- "Fix this bug: [description]"
- "Small change to [component]"
- "Quick feature: [simple feature]"
- "Simple fix for [issue]"
- "Minor update: [description]"
- "Lightweight change proposal"

**Prerequisites:**
- Change is Level 0-1 (small, well-defined)
- No major unknowns or architectural changes
- Existing codebase (not greenfield project)

**Do NOT invoke when:**
- Complex feature requiring PRD (use BMAD instead)
- Architectural changes needed (use bmad-architecture-design)
- Multiple teams coordination (use BMAD)
- Level 2+ complexity (escalate to BMAD)
- Greenfield project (use BMAD workflow)

**Auto-escalate to BMAD when:**
- Scope grows beyond Level 1
- Major unknowns emerge
- Requires cross-team coordination

## Mission
Capture small change requests or bug fixes and translate them into concise proposals and task outlines without invoking the full BMAD workflow.

## Inputs Required
- change_request: description of the existing behavior and desired adjustment
- impact_surface: files, services, or user flows likely affected
- constraints: timeline, risk, or approvals that bound the solution

## Outputs
- `proposal.md` summarizing problem, desired behavior, and acceptance signals (template: `assets/proposal-template.md.template`)
- `tasks.md` listing actionable steps sized for rapid implementation (template: `assets/tasks-template.md.template`)
- `specs/spec-delta.md` capturing ADDED/MODIFIED/REMOVED requirements (template: `assets/spec-delta-template.md.template`)
- Optional `design.md` scaffolded when deeper technical notes are required

`scripts/scaffold_change.py` creates this structure in `openspec/changes/<change-id>/` using the templates above.

## Process
1. Validate Level 0-1 scope using `CHECKLIST.md`.
2. Run `scripts/scaffold_change.py <change-id>` to create the workspace under `openspec/changes/`.
3. Clarify current vs. target behavior and record feasibility notes in `proposal.md`.
4. Draft `tasks.md` and populate `specs/spec-delta.md` using the templates in `assets/`.
5. Highlight dependencies, approvals, and risks, then hand off for review or implementation scheduling.

## Quality Gates
Ensure checklist items pass before finalizing. Escalate to BMAD if scope exceeds Level 1 or introduces major unknowns.

## Error Handling
- If information is insufficient, ask for missing context (screenshots, logs, reproduction steps).
- When risks are high or ambiguity remains, recommend migrating to BMAD discovery-analysis.
