---
name: linear-issue-workflow
description: Use when user provides a list of Linear issue IDs to fix sequentially; enforce status transitions (In Progress -> In Review), one issue at a time, and report build/test confirmation strategy.
---

# Linear Issue Workflow

Use this skill when user gives multiple Linear issue IDs and wants sequential fixes.

## Workflow

- Process issues strictly in order. One active issue at a time.
- Before coding each issue: fetch issue details, set status to `In Progress`.
- After implementing: set status to `In Review` (never Done unless explicitly asked).
- If blocked: stop and ask with short options.

## Build/Test Confirmation Strategy

- Default: run full gate via `just` (`just lint`, `just test`, `just build`) before handoff.
- If user asks to skip or system constraints prevent it: say so and ask for follow-up confirmation.

## Communication

- State which issue is active.
- Keep updates terse; list files changed.
- After each issue: brief verify steps or note skipped runs.
