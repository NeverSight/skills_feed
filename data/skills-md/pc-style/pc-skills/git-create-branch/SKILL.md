---
name: git-create-branch
description: Create a new Git branch with proper naming conventions. Use when the user asks to create a branch, start a new feature branch, or switch to a new branch. Handles branch creation from current HEAD or from a specific base branch, with conventional naming (feature/, fix/, hotfix/, etc.).
---

# Git Create Branch

Create a new Git branch with proper naming and checkout.

## When to Use

- Starting a new feature
- Creating a bug fix branch
- Starting work on a specific issue
- Any request to "create a branch" or "checkout new branch"

## Branch Naming Conventions

Use these prefixes for clarity:

- `feature/` - New features (e.g., `feature/add-login`)
- `fix/` - Bug fixes (e.g., `fix/login-error`)
- `hotfix/` - Urgent production fixes (e.g., `hotfix/critical-bug`)
- `refactor/` - Code refactoring (e.g., `refactor/auth-module`)
- `docs/` - Documentation changes (e.g., `docs/api-guide`)
- `test/` - Test additions/changes (e.g., `test/auth-tests`)
- `chore/` - Maintenance tasks (e.g., `chore/update-deps`)

## Workflow

### 1. Check Current State

```bash
git status
git branch --show-current
```

### 2. Create and Checkout Branch

**From current HEAD:**
```bash
git checkout -b <branch-name>
```

**From specific base branch:**
```bash
git checkout -b <branch-name> <base-branch>
```

### 3. Verify Creation

```bash
git branch --show-current
git log --oneline -3
```

## Examples

**Create feature branch from main:**
```bash
git checkout -b feature/user-profile main
```

**Create fix branch from current position:**
```bash
git checkout -b fix/validation-error
```

**Create branch for specific issue:**
```bash
git checkout -b feature/issue-123-add-search
```

## Best Practices

- Use descriptive names: `feature/add-dark-mode` not `feature/dark`
- Keep names concise but clear
- Use kebab-case (hyphens, not underscores)
- Include issue numbers when applicable: `fix/#456-memory-leak`
- Always verify you're on the new branch before making changes