---
name: git-workflow
description: Handle squashing multiple commits and rebasing feature branches safely. Use when consolidating commits into a single commit, or rebasing feature branches onto updated development branches. Falls back from jj when not available.
---

# Git Workflow

Safe, non-interactive approaches for squashing commits and rebasing feature branches.

> **Tip**: If jj is available (`jj root` succeeds), prefer jj-workflow—it's simpler and has automatic safety via oplog.

## Squash N Commits

```bash
git reset --soft HEAD~3
git commit -m "Your consolidated message"
```

That's it. The `--soft` flag keeps your changes staged and ready to commit.

## Rebase Feature Branch

Update dev first, then rebase:

```bash
git fetch origin dev && git checkout dev && git pull
git checkout my-feature
git rebase --committer-date-is-author-date dev
git push -f origin my-feature
```

The `--committer-date-is-author-date` flag puts your feature commits on top chronologically.

## Key Safety Rules

- **Never rebase shared branches** — only rebase local feature branches
- **Check `git status` first** — ensure no uncommitted changes
- **Create a backup branch**: `git branch backup-$(date +%s)`
- **Review changes** before committing: `git diff --cached`

## Pre-Commit Hook Changes

If hooks modify files during commit, stage and amend:

```bash
git add .
git commit --amend --no-edit
```

## When Things Go Wrong

```bash
git rebase --abort              # Stop rebase, go back
git reflog                      # See recent commits
git reset --hard <commit-hash>  # Recovery
```

See REFERENCE.md for detailed workflows and troubleshooting.
