---
name: commit-conventions
description: Create conventional commit messages and plan commits. Use when a user asks to commit changes, write commit messages, or organize commits. Enforce repo-specific git/commit rules from AGENTS.md and split multiple logical changes into separate, digestible commits.
---

# Commit Conventions

## Overview

Plan and execute commits that follow Conventional Commits plus any repository rules in AGENTS.md. Default to multiple commits when changes span more than one logical unit.

## Workflow

1. Read AGENTS.md (repo root or nearest) and apply any git/commit rules.
2. Inspect the working tree: `git status -sb`, `git diff --stat`, and focused `git diff` as needed.
3. Group changes by logical unit (feature, fix, refactor, docs, build/CI, etc.).
4. If more than one logical unit exists, create multiple commits. Propose a brief commit plan before committing.
5. Stage per group (`git add -p` or specific paths), then commit with a Conventional Commit message.
6. If the user asks for a single commit but changes are multiple logical units, warn and ask for confirmation before combining.

## Conventional Commit Format

- Format: `<type>(<scope>): <subject>`
- Scope is optional unless AGENTS.md requires it. Use short, stable areas (e.g., `dsp_core`, `plugin`, `ci`, `fastlane`).
- Subject is imperative, lowercase, and has no trailing period.

## Type Selection

- Prefer repo-specific types/scopes from AGENTS.md.
- Otherwise use standard types: `feat`, `fix`, `refactor`, `perf`, `docs`, `test`, `build`, `ci`, `chore`, `revert`.

## File Hygiene

- Exclude unrelated changes or generated artifacts unless explicitly required.
- If untracked files appear, confirm they are intended before staging.
- Avoid mixing unrelated existing changes into the same commit.

## Examples

- `fix(ci): use macos match certificates for signing`
- `build: split plugin signing into notarized release artifacts`
