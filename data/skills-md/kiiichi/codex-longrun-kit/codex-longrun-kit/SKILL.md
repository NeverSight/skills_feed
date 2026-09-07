---
name: codex-longrun-kit
description: Initialize a repository for compact, reviewable long-running Codex work by creating a task contract, milestone plan, state snapshot, stop rules, validation gates, and lazy review workflow. Use when the user wants a multi-hour implementation, migration, refactor, or reviewable autonomous coding task; do not use for small one-shot edits.
---

# Codex Longrun Kit

## Goal

Prepare the current repo for long-running Codex work without creating document bloat.

Default output is compact:

- `docs/agent/LONGRUN.md` — task contract, milestones, stop rules, validation gates.
- `docs/agent/STATE.md` — current handoff snapshot. Keep short.

Create review files only when review is frozen. Create strict extra files only if the user asks for strict mode.

## Quick start

If scripts are available, run:

```bash
python scripts/init_longrun.py --target . --profile standard --task-brief "<task brief>"
```

Then inspect and complete `docs/agent/LONGRUN.md` and `docs/agent/STATE.md` from the user's task brief and the repo.

Stop at the plan review checkpoint unless the user explicitly asked to continue into implementation.

## Process

1. Explore briefly: read root `AGENTS.md`, `README`, package/build files, and existing docs.
2. Create compact scaffold: `LONGRUN.md` and `STATE.md`.
3. Draft milestones as vertical slices with acceptance criteria and validation commands.
4. Mark unknowns as `UNCONFIRMED`; never record guesses as facts.
5. Ask only blocking questions. Ask one question at a time.
6. Do not implement during initialization unless explicitly requested.

## Execution loop

When implementation begins:

1. Read `LONGRUN.md` and `STATE.md`.
2. Work one milestone at a time.
3. Keep the diff scoped to the current milestone.
4. Run the listed validation gate before moving on.
5. Update `STATE.md` only when status, validation, decisions, or next action changes.
6. Stop only when a stop rule triggers or the plan is complete.

## Review workflow

At review freeze:

1. Stop modifying product code.
2. Run `python scripts/freeze_review.py --target . --base <base-ref>` if available.
3. Create `docs/agent/REVIEW.md` and `docs/reviews/pending/`.
4. Each reviewer writes one independent JSON report.
5. Normalize reports into `docs/reviews/ReviewQueue.json` before fixing.

## Subagents

Default: no write-code subagents.

Allowed: read-only subagents for codebase exploration, test failure analysis, security/architecture/UX review, and feedback normalization.

Patch subagents are allowed only after review feedback has been normalized into independent tickets, preferably one ticket per worktree.

## Do not

- Do not create many blank docs during init.
- Do not start long-running dev servers in the foreground.
- Do not change sandbox, approval, secrets, production, or deployment settings.
- Do not treat `STATE.md` as more authoritative than code, git history, or validation output.
- Do not fix unrelated review tickets in the same patch.

## References

Read only when needed:

- `references/compact-runtime-docs.md`
- `references/longrun-runbook.md`
- `references/review-workflow.md`
- `references/subagents-and-worktrees.md`
- `references/approval-boundaries.md`
