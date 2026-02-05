---
name: git-worktree
description: Use when you need to work on multiple branches simultaneously, run parallel Claude Code sessions, handle emergency hotfixes during feature work, review PRs without switching branches, or test across branches without losing current work
license: MIT
metadata:
  author: antonin
  version: "2.0.0"
  argument-hint: <branch-name> [base-branch]
---

# Git Worktree - Parallel Development

## Overview

Git worktrees enable multiple working directories from a single repository. Each worktree has its own branch while sharing the same Git object database.

**Core principle:** Check worktree status, create worktree for parallel work, reference cleanup commands as needed.

## When to Use

**Use worktrees when:**
- Working on multiple branches simultaneously
- Emergency hotfix needed without disrupting current work
- Reviewing PRs in isolation
- Testing across branches without stashing

**Avoid when:**
- Quick branch switch (use `git switch` instead)
- Single feature, single branch workflow

## The Workflow

### Step 1: Check Worktree Status

Before creating a worktree, check what already exists:

```bash
# List all worktrees
git worktree list

# Verbose output with branch info
git worktree list --verbose
```

### Step 2: Create Worktree

**Basic creation:**

```bash
# Create worktree with new branch from HEAD
git worktree add ../project-feature-name -b feature-name

# Create from specific base branch
git worktree add ../project-hotfix -b hotfix-critical origin/main

# Create from existing remote branch
git worktree add ../project-review pr-123
```

**Safety check:**
Ensure worktrees are either outside the repo or in `.gitignore` to avoid tracking them.

```bash
# Check if path would be tracked
git check-ignore ../project-feature-name
```

**Recommended configuration (run once):**
```bash
git config worktree.guessRemote true
git config worktree.useRelativePaths true
```

### Step 3: Work in Worktree

Navigate to the worktree and work normally:

```bash
cd ../project-feature-name
# Install dependencies, run tests, start Claude, etc.
```

## Worktree Management Reference

These commands are available for managing worktrees. Surface these to the user when relevant:

**List worktrees:**
```bash
# List all worktrees
git worktree list

# Verbose output with branch and commit info
git worktree list --verbose
```

**Remove worktrees:**
```bash
# Remove a worktree (must have no uncommitted changes)
git worktree remove ../project-feature-name

# Force remove (discards uncommitted changes)
git worktree remove -f ../project-feature-name
```

**Prune stale worktrees:**
```bash
# Clean up metadata for manually deleted worktrees
git worktree prune

# Dry run to see what would be pruned
git worktree prune -n

# Repair a disconnected worktree
git worktree repair ../project-feature-name
```

## Troubleshooting

### "Another worktree already uses this branch"

**Cause:** Can't checkout same branch in multiple worktrees.

**Solution:**
```bash
# Check which worktree has it
git worktree list | grep branch-name

# Create new branch from same base instead
git worktree add ../new-path -b branch-copy origin/branch-name
```

### "Worktree contains modified or untracked files"

**Cause:** Can't remove worktree with uncommitted changes.

**Solution:**
```bash
# Commit or stash changes first
cd ../project-feature-name
git add . && git commit -m "Final changes"

# Or force remove (discards changes)
git worktree remove -f ../project-feature-name
```

### Stale Worktree References

**Cause:** Manually deleted worktree directory without `git worktree remove`.

**Solution:**
```bash
# List worktrees (shows "prunable" entries)
git worktree list --verbose

# Clean up stale metadata
git worktree prune
```
## Examples

### Example 1: Create worktree for new feature

<Good>
```bash
# Always check existing worktrees first
git worktree list

# Create worktree with descriptive branch name
git worktree add ../myproject-auth -b feature/auth
cd ../myproject-auth

# Install dependencies and verify setup
npm install
npm test
```

**Why this is good:** Checks existing worktrees, uses descriptive naming, verifies setup before work.
</Good>

<Bad>
```bash
# Create worktree without checking existing ones
git worktree add ../temp -b temp
cd ../temp
```

**Why this is bad:** No verification of existing worktrees, vague naming makes tracking difficult, no setup verification.
</Bad>

### Example 2: Emergency hotfix pattern

<Good>
```bash
# Create hotfix from main, not current branch
git worktree add ../myproject-hotfix -b hotfix/payment-bug origin/main
cd ../myproject-hotfix

# Fix bug, test, commit
npm test
git add .
git commit -m "Fix payment processor race condition"
git push -u origin hotfix/payment-bug

# Return to original work
cd ../myproject
git worktree remove ../myproject-hotfix
```

**Why this is good:** Branches from correct base (main), tests before committing, cleans up after.
</Good>

<Bad>
```bash
# Create hotfix from current feature branch
git worktree add ../fix -b fix
cd ../fix
# Make changes, forget to clean up
```

**Why this is bad:** Wrong base branch (includes feature work), vague naming, no cleanup.
</Bad>

### Example 3: Review PR without switching

<Good>
```bash
# Fetch PR and create read-only worktree
git fetch origin pull/123/head:pr-123
git worktree add ../myproject-pr-123 pr-123
cd ../myproject-pr-123

# Review and test
npm install
npm test
# Leave comments, then clean up
cd ../myproject
git worktree remove ../myproject-pr-123
```

**Why this is good:** Fetches PR properly, uses PR number in path, cleans up after review.
</Good>

<Bad>
```bash
# Try to checkout PR in main worktree
git checkout pr-123  # Loses current work
```

**Why this is bad:** Switches branch in main worktree, loses current state, forces stashing.
</Bad>

## Integration

**This skill enables:**
- Working on multiple branches simultaneously without context switching
- Running parallel Claude Code sessions (one per worktree)
- Emergency hotfixes without disrupting feature work
- Safe PR review in isolated environments

**Pairs with:**
- **track-session** - Create separate SESSION_PROGRESS.md in each worktree to track independent progress
- **commit workflows** - Each worktree has its own staging area and commits independently
- **Parallel Claude sessions** - Name each Claude session after its worktree branch for clarity

**Integration pattern with track-session:**
```bash
# Create worktree
git worktree add ../myproject-feature -b feature/new-api
cd ../myproject-feature

# Create independent progress tracking
echo "# Session Progress - New API Feature" > SESSION_PROGRESS.md

# Start Claude session named "myproject - New API Feature"
# Work proceeds with independent progress tracking
```

**Multi-worktree workflow:**
```bash
# Terminal 1: Feature work in main worktree
cd ~/myproject
# Claude session: "myproject - main"

# Terminal 2: Hotfix in separate worktree
cd ~/myproject-hotfix
# Claude session: "myproject - hotfix"

# Terminal 3: PR review in separate worktree
cd ~/myproject-pr-123
# Claude session: "myproject - PR review"
```

**Best practices:**
- Name Claude sessions to match worktree purpose
- Each worktree tracks progress independently
- Use `git worktree list` to see all active work
- Clean up worktrees when branches are merged
