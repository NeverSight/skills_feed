---
name: git-version-control
description: Git workflows, branching strategies, collaboration, and code management
sasmp_version: "1.3.0"
bonded_agent: 03-devops-engineer
bond_type: SECONDARY_BOND
skill_version: "2.0.0"
last_updated: "2025-01"
complexity: foundational
estimated_mastery_hours: 40
prerequisites: []
unlocks: [cicd-pipelines, api-development]
---

# Git & Version Control

Production Git workflows, branching strategies, and collaborative development practices.

## Quick Start

```bash
# Initialize and configure
git init
git config user.name "Developer Name"
git config user.email "dev@company.com"

# Daily workflow
git checkout -b feature/add-data-pipeline
git add .
git commit -m "feat: add ETL pipeline for customer data"
git push -u origin feature/add-data-pipeline

# Create pull request (GitHub CLI)
gh pr create --title "Add ETL pipeline" --body "Implements customer data ETL"
```

## Core Concepts

### 1. Branching Strategies

```bash
# GitFlow
main           ──●──────────────────●──────────  # Production
                 │                  │
develop        ──●──●──●──────●──●──●──────────  # Integration
                    │   \    /
feature/x          ●────●──●                     # Features
                          │
release/1.0            ───●────                  # Release prep

# Trunk-Based Development (recommended for CI/CD)
main           ──●──●──●──●──●──●──●──●────────  # Always deployable
                 │  │     │     │
feature/*       ●  ●     ●     ●                 # Short-lived (1-2 days)

# Commands
git checkout -b feature/new-feature main
git push -u origin feature/new-feature
# After PR approval
git checkout main && git pull
git merge --squash feature/new-feature
git push origin main
git branch -d feature/new-feature
```

### 2. Commit Best Practices

```bash
# Conventional Commits format
# type(scope): description

git commit -m "feat(etl): add incremental load for orders table"
git commit -m "fix(api): handle null values in response"
git commit -m "docs(readme): update installation instructions"
git commit -m "refactor(pipeline): extract validation logic"
git commit -m "test(unit): add tests for data transformer"

# Types: feat, fix, docs, style, refactor, test, chore, perf

# Interactive rebase for clean history
git rebase -i HEAD~3
# pick -> squash commits, reword messages

# Amend last commit (before push)
git commit --amend -m "Updated message"
```

### 3. Resolving Conflicts

```bash
# Fetch and rebase (preferred over merge)
git fetch origin
git rebase origin/main

# If conflicts occur
# 1. Edit conflicted files
# 2. Mark as resolved
git add <resolved-files>
git rebase --continue

# Abort if needed
git rebase --abort

# Cherry-pick specific commits
git cherry-pick abc123

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1
```

### 4. Advanced Operations

```bash
# Stash changes
git stash save "WIP: refactoring"
git stash list
git stash pop  # Apply and remove
git stash apply stash@{0}  # Apply but keep

# Bisect to find bug
git bisect start
git bisect bad HEAD
git bisect good v1.0.0
# Git checks out commits, you test
git bisect good  # or bad
git bisect reset

# Find commits by content
git log -S "function_name" --oneline
git log --grep="fix" --oneline

# Blame to find author
git blame -L 10,20 src/pipeline.py

# Clean untracked files
git clean -fd  # Remove untracked files and directories
```

## Git Hooks

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Run linting
echo "Running linter..."
ruff check . || exit 1

# Run type checking
echo "Running type check..."
mypy src/ || exit 1

# Run tests
echo "Running tests..."
pytest tests/ -q || exit 1

echo "All checks passed!"
```

## Tools & Technologies

| Tool | Purpose | Version (2025) |
|------|---------|----------------|
| **Git** | Version control | 2.43+ |
| **GitHub CLI** | GitHub operations | 2.43+ |
| **pre-commit** | Git hooks framework | 3.6+ |
| **Conventional Commits** | Commit standard | - |
| **GitLens** | VS Code extension | Latest |

## Troubleshooting Guide

| Issue | Symptoms | Root Cause | Fix |
|-------|----------|------------|-----|
| **Merge Conflict** | Can't merge/rebase | Divergent changes | Resolve manually, `git add`, continue |
| **Detached HEAD** | Not on any branch | Checked out commit | `git checkout main` |
| **Lost Commits** | Commits missing | Reset/rebase | `git reflog`, `git cherry-pick` |
| **Large Repo** | Slow operations | Large files | Use Git LFS, clean history |

## Best Practices

```bash
# ✅ DO: Write meaningful commit messages
git commit -m "fix(etl): handle empty dataframes in transform step

Previously the pipeline would crash when receiving empty data.
Now it logs a warning and continues with the next batch."

# ✅ DO: Keep commits atomic and focused
# ✅ DO: Rebase feature branches before merging
# ✅ DO: Use .gitignore properly

# ❌ DON'T: Commit secrets or credentials
# ❌ DON'T: Force push to shared branches
# ❌ DON'T: Commit large binary files
```

## Resources

- [Pro Git Book](https://git-scm.com/book/en/v2)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Git Flight Rules](https://github.com/k88hudson/git-flight-rules)

---

**Skill Certification Checklist:**
- [ ] Can use branching and merging effectively
- [ ] Can write conventional commit messages
- [ ] Can resolve merge conflicts
- [ ] Can use interactive rebase
- [ ] Can set up pre-commit hooks
