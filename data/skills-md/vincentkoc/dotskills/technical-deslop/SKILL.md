---
name: technical-deslop
description: Remove AI-style noise from staged and branch diffs while preserving behavior and repository style.
license: AGPL-3.0-only
metadata:
  source: "https://github.com/vincentkoc/dotskills"
---

# Technical Deslop

## Purpose

Clean branch/staged diffs by removing AI-style slop and restoring repo-consistent style without changing behavior.

## When to use

- A diff feels over-explained, overly defensive, or inconsistent with surrounding code.
- You need a final cleanup pass before review/PR.
- You want to normalize style after automated generation.

## Workflow

1. Capture scope with `git diff --cached` and `git diff $(git merge-base origin/main HEAD)..HEAD`.
2. Focus only on changed hunks (or user-scoped files).
3. Apply the cleanup sequence in `references/playbook.md`.
4. Remove slop patterns: redundant comments, unnecessary defensive branches, non-idiomatic casts, and style drift.
5. Re-check behavior boundaries: no logic changes unless the user explicitly requested them.
6. Report a short 1-3 sentence summary of cleanup performed.

Read `references/slop-patterns.md` for detection rules and `references/playbook.md` for execution order.

## Inputs

- Optional file scope (`FILES`) or explicit user file targets.
- Current branch diff and staged diff.
- Repository conventions from local instructions/config.

## Outputs

- Behavior-preserving cleanup in touched files.
- Minimal summary of what was normalized and where.
