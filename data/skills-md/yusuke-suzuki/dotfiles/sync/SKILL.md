---
name: sync
description: Sync feature branch with main via rebase
---

# Sync

You are assisting with syncing a feature branch with the latest main branch. Follow these steps:

## 1. Initial Assessment

- Run `git status` to check for uncommitted changes (must be clean)
- Run `git fetch origin` to retrieve remote updates
- Display unpushed commits with `git log origin/main..HEAD --oneline`

## 2. Pre-Sync Validation

**Critical Check:**

- Ensure working directory is clean with no uncommitted changes
- If there are uncommitted changes, ask user to commit or stash them first
- Do NOT proceed with rebase if working directory is not clean

## 3. Synchronization Process

Execute the rebase:

```bash
git rebase origin/main
```

If conflicts occur:

1. Display the conflicting files
2. Guide user to resolve conflicts manually
3. After resolution, continue with `git rebase --continue`

## 4. Post-Sync Actions

After successful rebase:

1. Display the rebased commit history
2. Inform the user to run `/publish` to push the rebased changes

## Conflict Resolution Flow

If conflicts occur during rebase:

1. Show conflicting files with `git status`
2. User resolves conflicts in their editor
3. Stage resolved files with `git add <files>`
4. Continue rebase with `git rebase --continue`
5. Repeat until rebase completes

If rebase fails or conflicts are too complex, user can abort with `git rebase --abort`.
