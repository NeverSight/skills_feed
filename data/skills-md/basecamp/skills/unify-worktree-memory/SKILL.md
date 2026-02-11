---
name: unify-worktree-memory
description: |
  Consolidate Claude Code memory across git worktrees so all branches of the
  same repo share a single memory directory. Use when memory is isolated per
  worktree, when switching branches loses context, or when setting up a new
  machine with worktree-based workflows.
triggers:
  # Direct invocations
  - unify-worktree-memory
  - /unify-worktree-memory
  # Problem descriptions
  - memory isolated per worktree
  - worktree memory not shared
  - losing memory when switching branches
  - each worktree has separate memory
  - memory not shared across worktrees
  - consolidate memory
  - share memory across worktrees
  - worktree memory consolidation
  # Setup / configuration
  - set up worktree memory sharing
  - configure shared memory
  - symlink memory across worktrees
  - worktree symlink
  # Claude Code + worktree
  - claude code worktree
  - claude memory worktree
  - claude worktree branch
  - project memory sharing
---

# unify-worktree-memory

Open `@references/guide.md` and follow it. Do not proceed without it.

Consolidate Claude Code's per-project memory across git worktrees so every branch of the same repo shares accumulated knowledge. The solution uses symlinks (Claude Code follows them transparently) and a SessionStart hook for automatic setup of future worktrees.

The guide contains:
- How Claude Code memory paths work and why worktrees fragment them
- One-time consolidation script for existing worktrees
- SessionStart hook for automatic future worktree handling
- Path encoding rules and prefix collision disambiguation
- Edge cases: orphaned worktrees, ambiguous repo name prefixes, content merging
