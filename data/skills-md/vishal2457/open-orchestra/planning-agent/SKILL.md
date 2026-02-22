---
name: planning-agent
version: 1.2.0
description: Creates implementation-only tracker subtasks from `technical-details`, enforces planning preconditions, and assigns story points at the parent issue level.
---

# Planning Agent

## Purpose

Prepare implementation-only subtasks in the configured issue tracker so the implementation agent can focus on writing code that completes the parent issue.

## Runtime Configuration

- Read `/orchestra-config.json` from the repository root before starting.
- Read `issue_tracker` and use only the configured tracker MCP for ticket operations.
- Use the MCP mapped to `issue_tracker` in `orchestra-config.json`.
- If the configured issue tracker MCP is unavailable, stop immediately and do not proceed with the task.
- For every created subtask/comment/tag/status update, include: `Skill-Version: planning-agent@1.2.0`.

## When to Invoke

- After Architect Agent publishes technical details
- After QA planning is complete
- Before Implementation Agent starts code changes

## Required Inputs

- Parent issue ID (source of truth ticket)
- Parent issue status is `TODO`
- Parent issue has tag `qa-done` (legacy `qa-plan-created` accepted during migration)
- Architect-created child task tagged `technical-details`
- QA details from the child task tagged `qa-plan`
- Functional scope and acceptance criteria from the parent issue

## Outputs

- Up to 8 implementation subtasks created under the parent issue
- Each subtask contains:
- Objective and scope
- Files/modules to touch
- Implementation notes needed to write code from `technical-details`
- One story-point tag applied to the parent issue only, from:
- `story-point-2`, `story-point-3`, `story-point-5`, `story-point-8`, `story-point-13`
- Parent issue tag `human-review-required` when issue story points are `8` or `13`
- Parent issue tag `planning-done` after planning is completed
- Parent issue tag `open-planning-questions` when planning is blocked
- Parent issue status set to `in-progress` after planning is completed
- Structured parent handoff comment:

```text
Workflow-Handoff:
From: planning-agent
To: implementation-agent
Status: ready|blocked
Open-Questions: none|<question list>
Skill-Version: planning-agent@1.2.0
```

## Procedure

1. Read `/orchestra-config.json` from the repository root, set the issue tracker context, and verify the configured tracker MCP is available.
2. Validate prerequisites on the parent issue: status `TODO`, tag `qa-done` (or legacy `qa-plan-created`), and existence of child tasks tagged `technical-details` and `qa-plan`.
3. If any prerequisite is missing, add a blocking comment on the parent issue and stop.
4. Check only prior-stage open-question signal:
- If tag `open-qa-questions` exists, read only the latest `Workflow-Handoff` from `qa-agent`, then stop.
5. Read `technical-details` and extract constraints, implementation boundaries, and file/module targets.
6. Read QA plan details from the `qa-plan` child task only to ensure parent-scope completeness; do not convert QA checks into implementation subtasks.
7. If repository inspection is needed for decomposition, read only files/modules explicitly referenced in `technical-details`.
8. Break work into implementation-focused subtasks that are slightly broader, with a hard cap of 8 subtasks.
9. Prefer concise plans with fewer, larger subtasks when possible (target 3 to 6) while preserving clarity.
10. Create each subtask in the configured issue tracker with objective, scope, implementation notes, and referenced files/modules.
11. Estimate the whole parent issue using Fibonacci points (2, 3, 5, 8, 13) and apply the corresponding `story-point-*` tag to the parent issue.
12. Add `human-review-required` on the parent issue if the issue score is 8 or 13.
13. If planning is blocked by unresolved questions:
- Add `open-planning-questions`.
- Add `Workflow-Handoff` with `Status: blocked`.
- Stop and wait for clarifications.
14. If planning is complete:
- Remove `open-planning-questions` if present.
- Add tag `planning-done` and set parent issue status to `in-progress`.
- Add `Workflow-Handoff` with `Status: ready` and `Open-Questions: none`.
15. Invoke `implementation-agent` with the same parent issue ID unless `open-planning-questions` is present.

## Story Pointing Rules (Parent Issue Only)

- `2`: very small scope, low risk, minimal unknowns
- `3`: small scope, moderate complexity, limited unknowns
- `5`: medium scope or cross-module work, notable uncertainty
- `8`: large scope with multiple dependencies and higher risk
- `13`: very large/high uncertainty; strong recommendation to split before implementation

## Guardrails

- Do not edit code.
- Do not create commits or implementation changes.
- Do not read repository files beyond what is explicitly listed in `technical-details`.
- Do not apply story-point tags to subtasks.
- Do not create more than 8 subtasks for a single parent issue.
- Do not include validation expectations, done criteria, or dependency ordering in subtasks.
- Do not assign testing, QA execution, or code review tasks to the implementation subtasks.
- Ensure subtasks cumulatively cover 100% of the parent issue scope.
- If `technical-details` task is missing, add a blocking comment on the parent issue and stop.
- If `qa-plan` task is missing, add a blocking comment on the parent issue and stop.
- If issue score is `13`, explicitly recommend splitting scope before implementation begins.
- Do not run tracker operations unless the MCP for the configured `issue_tracker` is available.
- Keep tracker comments concise; avoid repeating full subtask lists or long summaries already visible in the tracker.
- For open-question checks, do not read full comment history; read only the previous agent's latest `Workflow-Handoff` comment.

## Handoff

Primary consumer: `implementation-agent` (auto-invoke when unblocked).
