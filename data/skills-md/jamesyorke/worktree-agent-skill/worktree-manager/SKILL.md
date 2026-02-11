---
name: worktree-manager
description: "Git worktree management with safe defaults and flexible placement strategies. Use when users ask to: (1) create a new worktree or work on multiple branches in parallel, (2) list existing worktrees, (3) remove or clean up worktrees, (4) manage worktree placement (subfolder vs sibling directory), or any other git worktree operations."
---
# Worktree Manager

Fast, interactive management of git worktrees with consistent conventions and automatic housekeeping.

## Agent behavior contract

1. Always use `--force` when removing worktrees — repos with submodules will fail without it.
2. Always run `git worktree prune` after removing a worktree to clean up stale references.
3. When creating subfolder worktrees, ensure `.worktrees/` is in `.gitignore` before creating.
4. Never hardcode worktree paths in remove operations — always read from `git worktree list`.
5. Default to subfolder placement unless the user explicitly chooses parent folder.
6. Default the worktree folder name to the last segment of the branch name.

## Triage (detect action)

If the user provided an argument (create, list, or remove), use that action.
If no argument was provided, ask the user which action they want:
- **create** — Create a new worktree with a new branch
- **list** — List all current worktrees
- **remove** — Remove an existing worktree

Then read the appropriate reference:

## Routing map

- **Creating a worktree** → `references/creating.md`
- **Listing worktrees** → `references/listing.md`
- **Removing a worktree** → `references/removing.md`
- **Placement strategies & conventions** → `references/placement.md`
- **Common issues & troubleshooting** → `references/troubleshooting.md`

## Common errors → next best move

- **"working trees containing submodules cannot be moved or removed"** → use `--force` flag (see `references/removing.md`)
- **Stale worktree references after manual deletion** → run `git worktree prune` (see `references/removing.md`)
- **Branch already checked out in another worktree** → list worktrees to find which one, remove or use a different branch
- **`.worktrees/` showing up in git status** → add to `.gitignore` (see `references/placement.md`)
