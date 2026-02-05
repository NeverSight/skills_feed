---
name: ratatouille
description: "Implement one prd.json task per iteration using tracer-bullet + compound mindset. Triggers on: ratatouille:."
---

# Ratatouille

Implement **one task** from `prd.json` per iteration using tracer-bullet methodology and a compounding engineering mindset. Maintain `progress.txt` across iterations.

## Trigger Formats

- `ratatouille: <short task hint>`
- `ratatouille: <file path>` (e.g., `ratatouille: prd.json`)

## Required Files

- `prd.json` (root)
- `progress.txt` (root)

## Workflow

### 0) Bootstrap (Always First)

1. Read `progress.txt` (if missing, create it).
2. Read `prd.json`. If missing, stop and ask user to run mise-en-place.
3. If this is the **first iteration**, ask what to do after each iteration and store in `progress.txt`.

Post-iteration action options:
- `qa` (run tests/checks)
- `simplify` (refactor for clarity)
- `deslop` (remove duplication, tighten docs)
- `review` (code-review + fix)
- `commit` (atomic commit)
- `none`

### 1) Pick the Next Task

- If the user provided a task hint, match it to a `tasks[].id` or `tasks[].title`.
- Otherwise, pick the first `status: "todo"` task.
- If multiple tasks are equally valid, ask the user to choose.

### 2) Tracer-Bullet Implementation

For the chosen task:
Use a tracer bullet to build the **thinnest end-to-end vertical slice** that touches every needed layer. This code is **not a throwaway prototype**—it becomes the foundation you expand after validating the path works. Aim for one happy path, minimal data, and fast feedback before adding depth.
1. Identify layers involved (UI, API, DB, config, tests).
2. Build the **thinnest end-to-end slice** that works.
3. Validate it (minimal integration test or manual check).
4. Expand only after the tracer bullet is working.

### 3) Compound Engineering Mindset

Apply compounding leverage:
- Prefer reusable abstractions only after the tracer works.
- Automate or document any non-obvious learnings.
- Make improvements that reduce future work (tests, scripts, patterns).

### 4) Update `progress.txt`

Append a new section:

```
Iteration: <N>
Task: <id + title>
Status: done|partial|blocked
Decisions:
- ...
Learnings:
- ...
Next:
- ...
Post-Iteration Actions:
- qa|simplify|deslop|review|commit|none
```

### 5) Update `prd.json`

- Set task `status` to `done` or `partial`.
- Add notes if blocked.
- Keep `updated` date fresh.

### 6) Run Post-Iteration Actions

Use the actions recorded in `progress.txt`:
- `qa`: run relevant tests/checks
- `simplify`: simplify or refactor touched code
- `deslop`: remove duplication, tighten docs
- `review`: run a code review and fix issues
- `commit`: create an atomic commit

### 7) Recursive Handoff

If tasks remain, re-trigger ratatouille:

- If the harness supports `/handoff` or `/new`, re-issue the same prompt with updated context.
- Otherwise, ask the user to re-run the same `ratatouille:` command.

## Notes

- Always start by reading `progress.txt`.
- Implement **one task per iteration**.
- Keep changes scoped and verified.
