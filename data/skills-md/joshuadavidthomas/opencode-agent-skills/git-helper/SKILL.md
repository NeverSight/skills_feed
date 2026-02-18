---
name: git-helper
description: Provides git workflow assistance, branch management, and commit message optimization
---

# Git Helper

A comprehensive skill for git workflow management and best practices.

## Quick Start

Use this skill when you need help with:
- Branch creation and management
- Commit message formatting
- Git workflow optimization
- Repository maintenance

## Common Workflows

### Creating a New Feature Branch
```bash
git checkout -b feature/your-feature-name
git push -u origin feature/your-feature-name
```

### Writing Good Commit Messages

Follow the conventional commit format:

```
type(scope): description

[optional body]

[optional footer]
```

Types: feat, fix, docs, style, refactor, test, chore

### Git Cleanup Commands

# Remove stale branches
```bash
git remote prune origin
```

# Clean up local branches
```bash
git branch -d branch-name
```

## Scripts

This skill includes helper scripts:

• `create-branch.sh` - Creates new feature branches with proper naming
• `commit-check.sh` - Validates commit message format
• `cleanup.sh` - Removes stale branches

## Best Practices

1. Always pull latest changes before creating branches
2. Use descriptive branch names with prefixes (feature/, bugfix/, hotfix/)
3. Write atomic commits (one logical change per commit)
4. Keep commit messages under 72 characters for the subject line
