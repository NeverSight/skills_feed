---
name: using-git-worktrees
description: Use when starting feature work that needs isolation from current workspace or before executing implementation plans - creates isolated git worktrees with smart directory selection and safety verification
---

# Using Git Worktrees

## Core Principles

1. **Systematic selection** - Follow priority: existing dir > CLAUDE.md > ask user
2. **Safety first** - Always verify .gitignore for project-local worktrees
3. **Clean baseline** - Run tests before starting work

**Announce:** "I'm using the using-git-worktrees skill to set up an isolated workspace."

## Quick Reference

| Situation | Action |
|-----------|--------|
| `.worktrees/` exists | Use it (verify .gitignore) |
| `worktrees/` exists | Use it (verify .gitignore) |
| Both exist | Use `.worktrees/` |
| Neither exists | Check CLAUDE.md → Ask user |
| Not in .gitignore | Add immediately + commit |
| Tests fail | Report failures + ask before proceeding |

## Basic Workflow

```bash
# Check existing
ls -d .worktrees worktrees 2>/dev/null

# Verify gitignore (project-local only)
grep -q "^\.worktrees/$" .gitignore

# Create
git worktree add .worktrees/$BRANCH -b $BRANCH
cd .worktrees/$BRANCH

# Setup + verify
npm install  # or cargo build, pip install, etc.
npm test     # must pass before starting
```

## Anti-Patterns

- ❌ **Skipping .gitignore** - Worktree contents pollute git status
- ❌ **Assuming location** - Always follow priority order
- ❌ **Ignoring test failures** - Can't distinguish new vs pre-existing bugs
- ❌ **Hardcoding setup** - Auto-detect from package.json, Cargo.toml, etc.

## References

- [Creation Steps](references/creation-steps.md) - Full setup process with examples
- [Safety Verification](references/safety-verification.md) - .gitignore checks and directory selection

## Related

- **conductor** - Design approval triggers worktree creation
- **finishing-a-development-branch** - Cleanup after work complete
- **maestro-core** - Plugin coordination context
