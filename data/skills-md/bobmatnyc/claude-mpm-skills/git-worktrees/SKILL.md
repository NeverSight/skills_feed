---
name: git-worktrees
description: Use git worktrees for parallel development on multiple branches simultaneously
tags: [git, worktrees, parallel-development, productivity]
related_agents: [version-control, engineer]
progressive_disclosure:
  entry_point:
    summary: "Use git worktrees for parallel development on multiple branches simultaneously"
    when_to_use: "When working with version control, branches, or pull requests."
    quick_start: "1. Review the core concepts below. 2. Apply patterns to your use case. 3. Follow best practices for implementation."
---
# Git Worktrees

## Overview

Git worktrees allow you to have multiple working directories from the same repository, each with a different branch checked out. Work on multiple branches simultaneously without switching.

## When to Use Worktrees

### ✅ Perfect For:
- Stacked PR development (one worktree per PR)
- Urgent hotfix while working on feature
- Parallel development on multiple features
- Code review in isolation
- Testing cross-branch interactions
- Running multiple dev servers simultaneously

### ⚠️ Consider Alternatives When:
- Limited disk space (worktrees duplicate working directory)
- Simple branch switching is sufficient
- Only working on one branch at a time

## Basic Workflow

### Create Worktree

**New Branch:**
```bash
# Create worktree with new branch
git worktree add ../worktrees/feature-auth -b feature/authentication

# Navigate to worktree
cd ../worktrees/feature-auth
```

**Existing Branch:**
```bash
# Create worktree from existing remote branch
git worktree add ../worktrees/feature-profile feature/user-profile

# Or from origin
git worktree add ../worktrees/review origin/feature/pr-to-review
```

### List Worktrees

```bash
git worktree list

# Output:
# /Users/dev/project              abc123 [main]
# /Users/dev/worktrees/f-auth     def456 [feature/authentication]
# /Users/dev/worktrees/f-profile  ghi789 [feature/user-profile]
```

### Remove Worktree

```bash
# Remove worktree (deletes directory)
git worktree remove ../worktrees/feature-auth

# Or manually delete directory and prune
rm -rf ../worktrees/feature-auth
git worktree prune
```

## Directory Structure

Recommended layout:

```
/Users/dev/
├── my-project/              # Main repository
│   ├── .git/               # Git database
│   ├── src/
│   └── ...
└── my-project-worktrees/    # All worktrees here
    ├── feature-auth/       # feature/authentication branch
    ├── feature-profile/    # feature/user-profile branch
    ├── hotfix-urgent/      # hotfix/urgent-fix branch
    └── review-pr-123/      # Reviewing PR #123
```

## Use Case: Stacked PRs

Perfect for stacked PR workflow - one worktree per PR:

```bash
# Create worktree for each PR in stack
git worktree add ../stack/pr-001 -b feature/001-base-auth
git worktree add ../stack/pr-002 -b feature/002-user-profile
git worktree add ../stack/pr-003 -b feature/003-admin-panel

# Work in each independently
cd ../stack/pr-001
# Implement base auth
git commit -am "feat: base authentication"
git push -u origin feature/001-base-auth

cd ../stack/pr-002
# Already on feature/002-user-profile branch
# Implement user profile (depends on pr-001)
git commit -am "feat: user profile with auth"
git push -u origin feature/002-user-profile

cd ../stack/pr-003
# Implement admin panel (depends on pr-002)
git commit -am "feat: admin panel"
git push -u origin feature/003-admin-panel
```

## Use Case: Parallel Development

Run multiple dev servers simultaneously:

```bash
# Terminal 1: Main feature development
cd /project-worktrees/feature-new-ui
npm install
npm run dev  # Server on port 3000

# Terminal 2: Urgent hotfix (different branch)
cd /project-worktrees/hotfix-critical
npm install
npm run dev -- --port 3001  # Server on port 3001

# Both running simultaneously without branch switching
```

## Use Case: Code Review

Review PRs in isolation:

```bash
# Create worktree for PR review
git worktree add ../review/pr-456 origin/feature/user-auth

cd ../review/pr-456
npm install
npm test
npm run dev

# Review code, test functionality
# When done, remove worktree
cd /main-project
git worktree remove ../review/pr-456
```

## Updating Stacked PRs with Worktrees

When base PR changes, update chain across worktrees:

```bash
# PR-001 got feedback
cd /stack/pr-001
git pull origin feature/001-base-auth
# Make changes, push

# Update PR-002 (in separate worktree)
cd /stack/pr-002
git rebase feature/001-base-auth
git push --force-with-lease origin feature/002-user-profile

# Update PR-003 (in separate worktree)
cd /stack/pr-003
git rebase feature/002-user-profile
git push --force-with-lease origin feature/003-admin-panel
```

## Managing Dependencies

### Shared node_modules (Save Disk Space)

**Option 1: Symlink**
```bash
cd /worktrees/feature-auth
ln -s /main-project/node_modules node_modules
```

**Option 2: Separate Install**
```bash
cd /worktrees/feature-auth
npm install  # Independent node_modules
```

Trade-off:
- Symlink: Less disk space, may have version conflicts
- Separate: More disk space, guaranteed isolation

## Best Practices

### 1. Naming Convention
```bash
# Use descriptive, consistent names
git worktree add ../worktrees/feature-authentication feature/authentication
git worktree add ../worktrees/hotfix-security hotfix/security-patch
```

### 2. Location Strategy
```bash
# Keep worktrees outside main repo
/Users/dev/project/              # Main repo (never delete)
/Users/dev/project-worktrees/    # All worktrees here (safe to delete)
```

### 3. Cleanup Discipline
```bash
# When PR merged, remove worktree immediately
git worktree remove path/to/worktree

# Periodically check for stale worktrees
git worktree prune

# Delete merged branches
git branch -d feature/old-branch
git push origin --delete feature/old-branch
```

### 4. One Branch Per Worktree
```
❌ WRONG: Switching branches in worktree defeats the purpose
✅ CORRECT: Each worktree permanently on one branch
```

## Common Commands

```bash
# Create worktree with new branch
git worktree add <path> -b <branch>

# Create worktree from existing branch
git worktree add <path> <branch>

# List all worktrees
git worktree list

# Remove worktree
git worktree remove <path>

# Clean up stale references
git worktree prune

# Move worktree to different location
git worktree move <old-path> <new-path>
```

## Troubleshooting

### Issue: "fatal: '<branch>' is already checked out"

**Cause:** Branch is checked out in another worktree

**Solution:**
```bash
# List worktrees to find where branch is checked out
git worktree list

# Either work in existing worktree or remove it first
git worktree remove <path-to-old-worktree>
```

### Issue: Disk space concerns

**Solution:**
- Use symlinks for node_modules
- Remove worktrees when PRs merged
- Run `git worktree prune` regularly
- Consider using sparse-checkout for large repos

### Issue: IDE confusion with multiple worktrees

**Solution:**
- Open each worktree as separate workspace
- Use IDE's multi-window/split-workspace features
- Name worktrees descriptively for easy identification

## Agent Instructions

When delegating worktree setup to version-control agent:

```
Task: Create worktrees for stacked PR development

Requirements:
- Create 3 worktrees in /project-worktrees/
- Worktree 1: pr-001 with branch feature/001-base-auth
- Worktree 2: pr-002 with branch feature/002-user-profile
- Worktree 3: pr-003 with branch feature/003-admin-panel

Commands:
git worktree add ../project-worktrees/pr-001 -b feature/001-base-auth
git worktree add ../project-worktrees/pr-002 -b feature/002-user-profile
git worktree add ../project-worktrees/pr-003 -b feature/003-admin-panel

Verification: git worktree list should show all 3 worktrees
```

## Benefits

✅ **No Branch Switching:** Work on multiple branches without `git checkout`
✅ **Parallel Servers:** Run multiple dev environments simultaneously
✅ **Preserve State:** Build artifacts and node_modules stay per-branch
✅ **Safer Reviews:** Test PRs without affecting main working directory
✅ **Faster Context Switch:** Jump between worktrees instead of rebasing

## Related Skills

- `stacked-prs` - Combine worktrees with stacked PR workflow
- `git-workflow` - General git branching patterns
- `code-review` - Review code in isolated worktrees
