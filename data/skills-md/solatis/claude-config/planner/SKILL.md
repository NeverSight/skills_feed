---
name: planner
description: Interactive planning and execution for complex tasks. Use when user asks to use or invoke planner skill.
---

# Planner Skill

Two workflows: **planning** (13-step plan creation + review) and **execution**
(implement plans).

## Activation

When this skill activates, IMMEDIATELY invoke the corresponding script. The
script IS the workflow.

| Mode      | Intent                             | Command                                                                                                             |
| --------- | ---------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| planning  | "plan", "design", "architect"      | `<invoke working-dir=".claude/skills/scripts" cmd="python3 -m skills.planner.planner --step 1 --total-steps 13" />` |
| execution | "execute", "implement", "run plan" | `<invoke working-dir=".claude/skills/scripts" cmd="python3 -m skills.planner.executor --step 1 --total-steps 9" />` |

## When to Use

Use when task has:

- Multiple milestones with dependencies
- Architectural decisions requiring documentation
- Complexity benefiting from forced reflection pauses

Skip when task is:

- Single-step with obvious implementation
- Quick fix or minor change
- Already well-specified by user

## Resources

| Resource                             | Contents                   | Read When                                       |
| ------------------------------------ | -------------------------- | ----------------------------------------------- |
| `.claude/conventions/diff-format.md` | Unified diff specification | Writing code changes in milestones              |
| `resources/plan-format.md`           | Plan template structure    | Completing planning phase (injected by script)  |
| `.claude/conventions/temporal.md`    | Comment hygiene heuristics | Writing comments in code snippets               |
| `.claude/conventions/structural.md`  | Structural conventions     | Making decisions without explicit user guidance |

## Planning Workflow (13 steps)

**Steps 1-5: Planning**

1. Context Discovery - explore, gather requirements
2. Testing Strategy Discovery - identify test patterns
3. Approach Generation - generate options with tradeoffs
4. Assumption Surfacing - user confirmation of choices
5. Approach Selection & Milestones - decide, write milestones + Code Intent

**Steps 6-13: Review**

6. QR-Completeness - validate plan structure
7. Gate - route based on QR result
8. Developer Fills Diffs - convert Code Intent to diffs
9. QR-Code - validate diffs and code quality
10. Gate - route based on QR result
11. TW Documentation Scrub - clean comments, inject WHY
12. QR-Docs - validate comment hygiene
13. Gate - PLAN APPROVED

## Execution Workflow (9 steps)

1. Execution planning - wave analysis
2. Reconciliation (conditional) - validate existing code
3. Implementation - wave-aware parallel dispatch to developers
4. Code QR - verify code quality (RULE 0/1/2)
5. Code QR Gate - route to step 3 on fail
6. Documentation - create CLAUDE.md/README.md
7. Doc QR - verify documentation quality
8. Doc QR Gate - route to step 6 on fail
9. Retrospective - summary presentation

Scripts inject step-specific guidance. Invoke and follow output.
