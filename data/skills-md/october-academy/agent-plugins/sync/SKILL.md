---
name: sync
description: Quick remote sync shortcut. Use when user says "/sync", "동기화", "pull", "git pull", or wants to pull latest changes from remote. Defaults to pulling from origin main.
user-invocable: true
---

# Sync Skill

Quick git synchronization with remote repository.

## Usage

### Commands

```bash
/sync              # Pull from origin main
/sync develop      # Pull from origin develop
/sync upstream     # Pull from upstream main (forks)
```

### Korean Triggers

- "동기화"
- "원격에서 가져와"
- "풀 받아"

## Workflow

### 1. Pre-sync Check

```bash
git status
```

If working directory has uncommitted changes:

**Options:**
1. **Stash**: `git stash` → sync → `git stash pop`
2. **Commit first**: Suggest using `/cp`
3. **Discard**: Only if user confirms with `git checkout .`

### 2. Fetch and Pull

Default (origin main):

```bash
git pull origin main
```

With rebase (cleaner history):

```bash
git pull --rebase origin main
```

### 3. Report Results

After successful sync:

```
Synced with origin/main
- 3 commits pulled
- Files changed: 5
- No conflicts
```

## Handling Conflicts

If merge conflicts occur:

1. List conflicting files
2. Offer to help resolve
3. After resolution: `git add <files>` → `git commit`

## Common Scenarios

### Fork Workflow

```bash
# Add upstream if not exists
git remote add upstream <original-repo-url>

# Sync with upstream
git fetch upstream
git merge upstream/main
```

### Diverged Branches

If local and remote have diverged:

```bash
# Option 1: Merge (default)
git pull origin main

# Option 2: Rebase (cleaner)
git pull --rebase origin main

# Option 3: Reset (destructive, ask user)
git fetch origin
git reset --hard origin/main
```

## Error Handling

| Error | Solution |
|-------|----------|
| "Uncommitted changes" | Stash or commit first |
| "Merge conflict" | Help resolve conflicts |
| "Remote not found" | Check `git remote -v` |
