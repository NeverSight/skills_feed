---
name: commit-helper
description: Generate conventional commit from staged changes
---

# Commit Helper

Generate a conventional commit message from staged changes.

## Changes to commit
!`git diff --staged --stat`

## Detailed diff
!`git diff --staged`

## Recent commit style
!`git log --oneline -5`

---

Generate a conventional commit message following these rules:
- Follow Conventional Commits 1.0.0 format
- 50 characters maximum for title, 70 characters for body lines
- Use past tense
- State **what** and **why** only, not how
- Use British spelling
- Cohesive paragraph unless multiple distinct points require bullet points
- Present the commit message for user approval before executing

Example format:
```
feat: added worktree deletion confirmation

Implemented confirmation dialogue before deleting worktrees to prevent
accidental data loss. The confirmation shows the worktree path and any
uncommitted changes that would be lost.
```
