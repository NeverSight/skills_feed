---
name: stacked-prs
description: Create and manage stacked (dependent) pull requests for complex features
tags: [git, pull-requests, branching, workflow, collaboration]
related_agents: [version-control]
progressive_disclosure:
  entry_point:
    summary: "Create and manage stacked (dependent) pull requests for complex features"
    when_to_use: "When working with version control, branches, or pull requests."
    quick_start: "1. Review the core concepts below. 2. Apply patterns to your use case. 3. Follow best practices for implementation."
---
# Stacked Pull Requests

## Overview

Stacked PRs are dependent pull requests where each PR builds on the previous one. Use this pattern for complex features that need logical separation and parallel review.

## When to Use

### ✅ Use Stacked PRs When:
- User explicitly requests "stacked PRs" or "dependent PRs"
- Large feature needs to be split into logical phases
- Each phase has clear dependencies on previous phases
- User is comfortable with rebase workflows

### ❌ Use Main-Based PRs When (Default):
- Features are independent
- Simple bug fixes or enhancements
- Multiple agents working in parallel
- User doesn't specify preference

**DEFAULT: Always prefer main-based PRs unless user explicitly requests stacking.**

## Branch Naming Convention

Use sequential numbering to show dependencies:

```bash
feature/001-base-authentication       # PR-001 (base)
feature/002-user-profile              # PR-002 (depends on 001)
feature/003-admin-panel               # PR-003 (depends on 002)
```

Alternative patterns:
```bash
auth/01-foundation
auth/02-user-flow
auth/03-admin-features
```

## Creating Stacked PRs

### Step 1: Create Base PR (PR-001)

```bash
# Start from main
git checkout main
git pull origin main

# Create base branch
git checkout -b feature/001-base-auth

# Implement base functionality
# ... work ...

# Push and create PR
git push -u origin feature/001-base-auth

# Create PR in GitHub/GitLab
# Title: "[1/3] Base authentication foundation"
# Base: main
# Description: Include stack overview (see template below)
```

### Step 2: Create Dependent PR (PR-002)

**CRITICAL: Base on previous feature branch, NOT main**

```bash
# Start from PR-001's branch
git checkout feature/001-base-auth
git pull origin feature/001-base-auth

# Create dependent branch
git checkout -b feature/002-user-profile

# Implement dependent functionality
# ... work ...

# Push and create PR
git push -u origin feature/002-user-profile

# Create PR in GitHub/GitLab
# Title: "[2/3] User profile management"
# Base: feature/001-base-auth  ← NOT main!
# Description: "Depends on PR #123"
```

### Step 3: Create Final PR (PR-003)

```bash
# Start from PR-002's branch
git checkout feature/002-user-profile
git pull origin feature/002-user-profile

# Create final branch
git checkout -b feature/003-admin-panel

# Implement final functionality
# ... work ...

# Push and create PR
git push -u origin feature/003-admin-panel

# Create PR in GitHub/GitLab
# Title: "[3/3] Admin panel with full auth"
# Base: feature/002-user-profile  ← NOT main!
# Description: "Depends on PR #124"
```

## PR Description Template

Use this template for stacked PRs:

```markdown
## This PR
[Brief description of changes in THIS PR only]

## Depends On
- PR #123 (feature/001-base-auth) - Must merge first
- Builds on top of authentication foundation

## Stack Overview
1. PR #123: Base authentication (feature/001-base-auth) ← MERGE FIRST
2. PR #124: User profile (feature/002-user-profile) ← THIS PR
3. PR #125: Admin panel (feature/003-admin-panel) - Coming next

## Review Guidance
To see ONLY this PR's changes:
```bash
git diff feature/001-base-auth...feature/002-user-profile
```

Or on GitHub: Compare `feature/002-user-profile...feature/001-base-auth` (three dots)

## Testing
- Tested in combination with PR #123
- Includes tests for user profile functionality
- Integration tests pass with base auth layer
```

## Managing Rebase Chains

### When Base PR Changes (Review Feedback)

If PR-001 gets updated, rebase dependent PRs:

```bash
# Update PR-001 (base)
git checkout feature/001-base-auth
git pull origin feature/001-base-auth

# Rebase PR-002 on updated base
git checkout feature/002-user-profile
git rebase feature/001-base-auth
git push --force-with-lease origin feature/002-user-profile

# Rebase PR-003 on updated PR-002
git checkout feature/003-admin-panel
git rebase feature/002-user-profile
git push --force-with-lease origin feature/003-admin-panel
```

**IMPORTANT: Use `--force-with-lease` not `--force` for safety**

### Merge Strategy

**Option A: Sequential Merging (Recommended)**
1. Merge PR-001 to main
2. Change PR-002's base to main (GitHub: "Edit" button on PR)
3. Merge PR-002 to main
4. Change PR-003's base to main
5. Merge PR-003 to main

**Option B: Keep Stack Until End**
1. Merge PR-001 to main
2. Keep PR-002 based on feature/001 until PR-001 fully merged
3. Then rebase PR-002 onto main
4. Repeat for PR-003

## Common Pitfalls

### ❌ WRONG: All PRs from main
```bash
git checkout main
git checkout -b feature/001-base
# PR: feature/001-base → main

git checkout main  # ← WRONG
git checkout -b feature/002-next
# PR: feature/002-next → main  # ← WRONG (independent, not stacked)
```

### ✅ CORRECT: Each PR from previous
```bash
git checkout main
git checkout -b feature/001-base
# PR: feature/001-base → main

git checkout feature/001-base  # ← CORRECT
git checkout -b feature/002-next
# PR: feature/002-next → feature/001-base  # ← CORRECT (stacked)
```

## Agent Instructions

When delegating stacked PR creation to version-control agent:

```
Task: Create stacked PR branch structure

Stack Sequence:
1. PR-001: feature/001-base-auth → main (base layer)
2. PR-002: feature/002-user-profile → feature/001-base-auth (depends on 001)
3. PR-003: feature/003-admin-panel → feature/002-user-profile (depends on 002)

Requirements:
- Each branch MUST be based on previous feature branch
- Use sequential numbering (001, 002, 003)
- Include "depends on" notes in commit messages
- Create PR description with stack overview

CRITICAL: PR-002 bases on feature/001-base-auth, NOT on main
CRITICAL: PR-003 bases on feature/002-user-profile, NOT on main
```

## Verification Checklist

Before creating stacked PRs:

- [ ] User explicitly requested stacked PRs
- [ ] Feature has clear logical phases
- [ ] Each phase has dependency on previous
- [ ] User understands rebase workflow
- [ ] Branch names use sequential numbering
- [ ] Each branch created from correct base (previous feature branch)
- [ ] PR descriptions include dependency information
- [ ] Stack overview documented in each PR

## Related Skills

- `git-worktrees` - Work on multiple PRs simultaneously
- `git-workflow` - General git branching patterns
- `code-review` - Review strategies for stacked PRs
