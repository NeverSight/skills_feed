---
name: pr-stacking
description: PR stacking workflow for breaking large features into smaller, dependent PRs. Use when planning multi-step features, creating dependent branches, or rebasing stacked changes.
---

# PR Stacking

Break large features into logical, dependent PRs for better code quality and easier reviews.

## Prerequisites

```bash
# Install GitHub CLI (required for PR creation)
brew install gh        # macOS
# or: sudo apt install gh   # Ubuntu/Debian

# Authenticate
gh auth login
```

## When to Stack

Stack PRs when:
- Feature spans multiple logical steps (frontend + backend, model + UI)
- Change exceeds ~300 lines of diff
- Work can be merged incrementally

Skip stacking for:
- Single-purpose bug fixes
- Small, isolated changes
- Refactoring within one file

## Quick Start

```bash
# 1. Create first PR branch from main
git checkout main && git pull
git checkout -b feat/user-api

# 2. Make changes, commit, push
git add . && git commit -m "Add user API endpoint"
git push -u origin feat/user-api

# 3. Stack: create dependent branch FROM current branch
git checkout -b feat/user-ui  # branches from feat/user-api

# 4. Continue working on dependent changes
git add . && git commit -m "Add user profile component"
git push -u origin feat/user-ui
```

## Core Workflow

### Branch Naming

```
feat/<feature>-1-<step>   # First in stack
feat/<feature>-2-<step>   # Second in stack
feat/<feature>-3-<step>   # Third in stack
```

Example:
```
feat/dark-mode-1-theme-context
feat/dark-mode-2-toggle-component
feat/dark-mode-3-persist-preference
```

### PR Descriptions

Include stack context in PR body:

```markdown
## Stack Context
- **Depends on**: #123 (theme context)
- **Followed by**: #125 (persist preference)

## This PR
Adds toggle component for switching themes.
```

### Merge Order

Merge from bottom to top:
1. Merge base PR first (#123 theme context)
2. Rebase dependent PR onto updated main
3. Merge next PR (#124 toggle component)
4. Repeat until stack is fully merged

## Rebasing Stacked Branches

When base PR changes:

```bash
# Update base branch
git checkout feat/dark-mode-1-theme-context
git pull origin feat/dark-mode-1-theme-context

# Rebase dependent branch
git checkout feat/dark-mode-2-toggle-component
git rebase feat/dark-mode-1-theme-context

# Force push (branch only, never main)
git push --force-with-lease
```

## References

- [references/workflow-steps.md](references/workflow-steps.md) - Detailed step-by-step guide
- [references/rebase-guide.md](references/rebase-guide.md) - Handling conflicts and rebasing
