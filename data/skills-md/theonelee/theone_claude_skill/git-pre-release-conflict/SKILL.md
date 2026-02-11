---
name: git-pre-release-conflict
description: Use when asked to publish or sync a feature branch to pre in this repo, or to resolve complex git conflicts that occur in that release flow.
---

# Git Pre Release + Conflict Resolution

## When to use
- Requests like "publish to pre", "sync branch to pre", or "rebuild pre".
- Any complex Git conflict resolution in this repo, especially during release merges.

## Quick start
1. Confirm `<main_branch>` and `<feature_branch>` with the user.
2. For the release/sync workflow, follow `references/flow.md`.
3. If conflicts occur, follow `references/conflict_playbook.md`.

## Safety gates
- Do not delete or force-push branches without explicit user confirmation.
- If network access is blocked, request approval before any `git fetch`/`git push`.
- Preserve unrelated changes; avoid `git add .` unless explicitly told.

## Output expectations
- Report branch names, stash actions, and conflict file list.
- Summarize conflict decisions (ours/theirs/manual merge).
- Provide final `git status` summary and next steps.
