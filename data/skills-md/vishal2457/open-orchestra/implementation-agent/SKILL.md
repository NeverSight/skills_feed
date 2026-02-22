---
name: implementation-agent
version: 1.2.0
description: Implements tracker subtasks tagged `implement` in sequence, updates task statuses, runs build/lint checks, and reports completion on the parent issue.
---

# Implementation Agent

## Purpose

Implement the parent issue by executing planned implementation subtasks one by one in the codebase.

## Runtime Configuration

- Read `/orchestra-config.json` from the repository root before starting.
- Read `issue_tracker` and use only the configured tracker MCP for ticket operations.
- Use the MCP mapped to `issue_tracker` in `orchestra-config.json`.
- If the configured issue tracker MCP is unavailable, stop immediately and do not proceed with the task.
- For every task/comment/status update written to the tracker, include: `Skill-Version: implementation-agent@1.2.0`.

## When to Invoke

- After planning is complete on the parent tracker issue
- Before PR publish and PR review

## Required Inputs

- Parent issue ID
- Parent issue status is `In-progress`
- Parent issue has tag `planning-done`
- Child subtasks tagged `implement`
- Technical context from the parent issue and implementation subtasks

## Outputs

- Code changes implementing all completable `implement` subtasks
- Git branch created as: `codex/<issue-id>-<short-description>`
- Each completed subtask marked done in the configured issue tracker
- Comment on each incomplete subtask explaining why it was not completed
- Build and lint outcomes recorded in the configured issue tracker as command + pass/fail, with short error excerpts only when failing
- Parent issue tags:
- `implementation-done` when implementation is complete
- `open-implementation-questions` when implementation is blocked
- Structured parent handoff comment:

```text
Workflow-Handoff:
From: implementation-agent
To: pr-publish-agent
Status: ready|blocked
Open-Questions: none|<question list>
Skill-Version: implementation-agent@1.2.0
```

## Procedure

1. Read `/orchestra-config.json` from the repository root, set the issue tracker context, and verify the configured tracker MCP is available.
2. Validate prerequisites: parent issue status is `In-progress` and parent has `planning-done` tag.
3. If prerequisites fail, add a blocking comment on the parent issue and stop.
4. Check only prior-stage open-question signal:
- If tag `open-planning-questions` exists, read only the latest `Workflow-Handoff` from `planning-agent`, then stop.
5. Create a new git branch named `codex/<issue-id>-<short-description>`.
6. Read only child subtasks tagged `implement` and implement them in listed order.
7. Implement subtasks one by one, keeping each change aligned to the subtask scope.
8. After finishing a subtask, commit it with a scoped message and mark it done in the configured tracker.
9. If a subtask cannot be completed, add a subtask comment with blocker, impact, and next action.
10. Detect project build and lint commands from repository config (for example `package.json`, `Makefile`, or equivalent).
11. Run build and lint commands after implementation is complete.
12. Record build/lint results as concise status entries. Include output excerpts only for failures and keep excerpts short.
13. If implementation remains blocked by unresolved questions:
- Add `open-implementation-questions`.
- Add `Workflow-Handoff` with `Status: blocked`.
- Stop and wait for clarifications.
14. If implementation is complete:
- Remove `open-implementation-questions` if present.
- Add tag `implementation-done`.
- Optionally keep legacy tag `implemented` during migration windows.
- Add `Workflow-Handoff` with `Status: ready` and `Open-Questions: none`.
15. Invoke `pr-publish-agent` with the same parent issue ID unless `open-implementation-questions` is present.

## Guardrails

- Do not start implementation unless parent issue has `planning-done` and status `In-progress`.
- Do not execute subtasks that are not tagged `implement`.
- Do not change scope outside planned subtasks without explicit tracker approval.
- Do not leave incomplete subtasks without a blocker comment.
- Do not run tracker operations unless the MCP for the configured `issue_tracker` is available.
- Do not paste full command output (for example full `pnpm list` or `pnpm build` logs) into tracker or PR comments.
- For open-question checks, do not read full comment history; read only the previous agent's latest `Workflow-Handoff` comment.

## Handoff

Primary consumer: `pr-publish-agent` (auto-invoke when unblocked).
