---
name: using-git-worktrees
description: Use when starting feature work that needs isolation from current workspace or before executing implementation plans - creates isolated git worktrees with smart directory selection and safety verification
---

# Using Git Worktrees

## Overview

Git worktrees create isolated workspaces sharing the same repository, allowing work on multiple branches simultaneously without switching.

**Core principle:** Systematic directory selection + safety verification = reliable isolation.

**Announce at start:** "I'm using the using-git-worktrees skill to set up an isolated workspace."

## Worktree Creation

Use `scripts/worktree-setup <branch-name>` to handle directory selection, safety verification, dependency installation, and baseline testing in one step.

The script auto-detects the worktree directory (`.worktrees/` > `worktrees/` > CLAUDE.md preference), verifies gitignore, installs deps, and runs baseline tests. If no directory is auto-detected, it exits with a suggestion — the skill then asks the user and re-runs with `--dir <path>`.

**Options:** `--dir <path>` (override directory), `--no-install`, `--no-test`
**Exit codes:** 0 = ready + tests pass, 1 = fatal, 2 = created but tests fail/not found

## Quick Reference

| Situation | Action |
|-----------|--------|
| `.worktrees/` exists | Use it (verify ignored) |
| `worktrees/` exists | Use it (verify ignored) |
| Both exist | Use `.worktrees/` |
| Neither exists | Check CLAUDE.md -> Ask user |
| Directory not ignored | Add to .gitignore + commit |
| Tests fail during baseline | Report failures + ask |

## Red Flags

**Never:** Create worktree without verifying ignored (project-local), skip baseline test verification, proceed with failing tests without asking, assume directory location.

**Always:** Follow directory priority (existing > CLAUDE.md > ask), verify ignored, auto-detect and run project setup, verify clean test baseline.

## Integration

**Called by:** brainstorming (Phase 4), plan-execution
**Pairs with:** finishing-a-development-branch (cleanup after work complete)

For detailed creation steps, setup commands, and example workflow, see [references/creation-steps.md](references/creation-steps.md).
