---
name: using-git-worktrees
description: Creates isolated git worktrees for parallel development. Use when starting feature work needing isolation or working on multiple branches simultaneously. Not for simple branch switching or basic git operations.
allowed-tools:
  - Read
  - Bash
  - Grep
  - Glob
---

# Git Worktrees

Git worktrees create isolated workspaces sharing the same repository, allowing work on multiple branches simultaneously.

**Announce at start:** "I'm using the using-git-worktrees skill to set up an isolated workspace."

## Quick Start

```bash
# Create worktree with new branch
git worktree add .worktrees/feature-auth -b feature/auth

# Create worktree from existing branch
git worktree add .worktrees/bugfix bugfix/issue-123

# List worktrees
git worktree list

# Remove worktree
git worktree remove .worktrees/feature-auth
```

## Directory Selection

1. Check existing: `.worktrees/` or `worktrees/`
2. Check CLAUDE.md for preference
3. Ask user if neither exists

## Safety Requirements

**Before creating project-local worktree:**

```bash
# Verify directory is in .gitignore
grep -q "^\.worktrees/$" .gitignore || grep -q "^worktrees/$" .gitignore
```

If NOT in .gitignore: Add it immediately and commit.

## References

- [WORKFLOW.md](WORKFLOW.md) - Detailed workflow steps
- [scripts/](scripts/) - Helper scripts
