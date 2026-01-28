---
name: using-git-worktrees
description: Use when starting new feature work to create isolated git worktrees with smart directory selection and safety verification. Keeps main branch clean while developing.
---

# Using Git Worktrees

## Core Principle

**Isolate feature work. Keep main clean.**

Git worktrees let you work on multiple branches simultaneously in separate directories.

## When to Use

- Starting a new feature
- Working on a bugfix while main development continues
- Need to context-switch without stashing
- Want clean separation between work streams

## Setup Process

### Step 1: Check for Existing Worktree Directory

```bash
# Check in priority order
ls -d .worktrees 2>/dev/null    # Preferred (hidden)
ls -d worktrees 2>/dev/null     # Alternative
```

If found: Use that directory.
If both exist: `.worktrees` wins.

### Step 2: Check CLAUDE.md for Preferences

```bash
grep -i "worktree.*director" CLAUDE.md 2>/dev/null
```

If preference specified: Use it without asking.

### Step 3: If No Directory Exists

Ask the user:
```
No worktree directory found. Where should I create worktrees?
1. .worktrees/ (project-local, hidden)
2. worktrees/ (project-local, visible)
3. ~/.config/superpowers/worktrees/<project-name>/ (global location)

Which would you prefer?
```

### Step 4: Verify .gitignore

```bash
# Check if directory pattern in .gitignore
grep -q "^\.worktrees/$" .gitignore || grep -q "^worktrees/$" .gitignore
```

If not present, add it:
```bash
echo ".worktrees/" >> .gitignore
# or
echo "worktrees/" >> .gitignore
```

## Creating a Worktree

### Standard Creation

```bash
# Determine branch name from feature
BRANCH_NAME="feature/descriptive-name"

# Create worktree with new branch
git worktree add ".worktrees/$BRANCH_NAME" -b "$BRANCH_NAME"

# Navigate to worktree
cd ".worktrees/$BRANCH_NAME"
```

### From Existing Branch

```bash
git worktree add ".worktrees/$BRANCH_NAME" "$BRANCH_NAME"
```

## Post-Creation Setup

### Install Dependencies

```bash
# Node.js
if [ -f package.json ]; then npm install; fi

# Rust
if [ -f Cargo.toml ]; then cargo build; fi

# Python
if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
if [ -f pyproject.toml ]; then poetry install; fi

# Go
if [ -f go.mod ]; then go mod download; fi
```

### Run Initial Tests

```bash
# Run test suite
npm test  # or appropriate command

# Report status
```

If tests fail: Report failures, ask whether to proceed or investigate.
If tests pass: Report ready.

## Worktree Management

### List Worktrees

```bash
git worktree list
```

### Remove Worktree

```bash
# After merging feature branch
git worktree remove ".worktrees/feature/branch-name"

# Force remove (if needed)
git worktree remove --force ".worktrees/feature/branch-name"
```

### Prune Stale Worktrees

```bash
git worktree prune
```

## Best Practices

### Naming Convention
- `feature/descriptive-name` for features
- `bugfix/issue-number-description` for bugs
- `hotfix/critical-issue` for urgent fixes

### Keep Worktrees Focused
- One feature per worktree
- Merge and remove when done
- Don't let worktrees accumulate

### Sync Regularly
```bash
# In worktree, get latest from main
git fetch origin
git rebase origin/main
```

## Completion Checklist

When feature is complete:
1. [ ] All tests pass
2. [ ] Code reviewed
3. [ ] Merged to main
4. [ ] Worktree removed
5. [ ] Branch deleted (if desired)

```bash
# Full cleanup
git checkout main
git pull
git worktree remove ".worktrees/feature/name"
git branch -d feature/name
```

## Announcement Template

At start of worktree creation:
```
"I'm using the using-git-worktrees skill to set up an isolated workspace for [feature name]."
```

On completion:
```
"Worktree ready at [full-path]
Tests passing ([N] tests, 0 failures)
Ready to implement [feature-name]"
```
