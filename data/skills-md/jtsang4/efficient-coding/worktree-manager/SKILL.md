---
name: worktree-manager
description: Manage Git worktrees. Use when asked to create/switch/list/merge/remove worktrees, to keep multiple branches in parallel directories, or to clean up worktrees safely during development.
---

# Worktree Manager

## Overview

Use Worktrunk (`wt`) as the single interface for Git worktree management: create/switch worktrees, list global status, merge back to the default branch, and remove worktrees safely. Prefer safe operations; never use destructive flags unless the user explicitly requests them.

## Workflow Decision Tree

### Recovery: If a `wt` command fails because `wt` is missing

Do not preflight-check `wt` on every invocation. Instead, attempt the requested `wt` command. If it fails with an error like "command not found: wt" (or equivalent), then:

1. Ask the user: "I can't run `wt` because it isn't installed. Should I install Worktrunk now (recommended)?"
2. If the user says yes:
   - Run the installer script:
     `scripts/install_worktrunk.sh`
     - Example: `bash <SKILL_DIR>/scripts/install_worktrunk.sh`
   - Verify: `wt --version`
   - Re-run the original `wt ...` command.
3. Do not install shell integration without confirmation (it edits shell rc files):
   - Ask before running: `wt config shell install`

### Step 1: Always run guardrails before merge/remove

Before `wt merge` / `wt remove` / anything with `--force` / `-D`:

1. Confirm repo context:
   - `git rev-parse --show-toplevel`
   - `pwd`
2. Confirm working tree cleanliness (if dirty, ask what to do; do not proceed):
   - `git status --porcelain`
3. Confirm the current worktree and branch:
   - `git branch --show-current`
   - `wt list` (use as the global source of truth for other worktrees)

### Step 2: Handle the user request via the matching workflow

#### A) Create or switch worktrees (most common)

Goal: "Put branch X into its own directory and switch into it."

1. If the user gave a branch/worktree name:
   - `wt switch <name>`
2. If the user asked to create a new branch/worktree:
   - Default (this repo): create the worktree by **copying the current working state** from the current worktree, so experiments are isolated but start "warm" (deps + uncommitted changes).
   - Implement with Worktrunk by creating from the current worktree as the base (use `--base=@` unless the user explicitly wants a clean base).
   - Run: `wt switch --create <name> --base=@`
3. If the user gave no name:
   - Show options with `wt list` and ask which one to switch to.

Notes:
- Do not invent naming conventions; follow the repo's existing pattern (or ask).
- If `wt switch` does not change directories in the current shell, suggest enabling shell integration (with confirmation) via `wt config shell install`.
- This repo has Worktrunk hooks in `.config/wt.toml` (notably `post-create`) that may copy the base worktree's working directory into a new worktree.
- If the user explicitly wants a completely clean worktree (skip all hooks/copy behavior), pass `--no-verify` (e.g. `wt switch --create <name> --base=@ --no-verify`).

#### B) List and diagnose global worktree state

Goal: "What worktrees exist and which ones are dirty/out-of-date?"

1. `wt list`
2. If the user needs machine-readable output, use the JSON option supported by Worktrunk (if available in their version) and paste only the relevant fields.

#### C) Merge the current worktree branch back and clean up

Goal: "Finish this branch and get back to the default branch cleanly."

1. Run guardrails (Step 1).
2. Confirm intent (quickly): target branch is the default branch; merge strategy is Worktrunk defaults unless the user asked otherwise.
3. If any flag/target behavior is unclear, check: `wt merge --help`
4. Run: `wt merge`
5. If the user wants to keep the worktree, use the appropriate Worktrunk flag (only if requested) to prevent removal.

Rules:
- Do not run `wt merge` if the tree is dirty unless the user explicitly tells you to proceed and how to handle changes.

#### D) Remove worktrees safely

Goal: "Delete a worktree directory safely without losing uncommitted work."

1. Run guardrails (Step 1).
2. Prefer safe removal:
   - `wt remove <name>`
3. Only use destructive options if the user explicitly asks:
   - `--force` (can discard untracked files depending on tool behavior)
   - `-D` (force-delete an unmerged branch/worktree)
4. If flags/behavior are unclear, check: `wt remove --help`

## Installation Notes (read only when needed)

See `references/install.md` for platform-specific notes. Use `scripts/install_worktrunk.sh` to install after the user confirms.
