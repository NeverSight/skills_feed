---
name: git-sync
description: Synchronize local main branch with remote, ensuring up-to-date base for worktrees.
---

# Git Sync

## Instructions

### When to Invoke This Skill
- Before creating new worktrees (ensure latest main)
- Periodically to stay up to date with team changes
- After multiple PRs have been merged
- When starting a new batch of issue work

### Purpose

Keeps the local main branch synchronized with the remote repository, ensuring all new worktrees are based on the latest code.

### Standard Workflow

#### Synchronizing Main Branch

**1. Verify Current Branch**
```bash
git branch --show-current
```

If not on main, switch:
```bash
git checkout main
```

**2. Check for Uncommitted Changes**
```bash
git status --short
```

If uncommitted changes exist on main:
- **WARN USER** - main should typically be clean
- Options:
  - Stash: `git stash push -m "Temp stash before sync"`
  - Commit to feature branch
  - Abort sync

**3. Fetch Latest from Remote**
```bash
git fetch origin
```

This updates remote-tracking branches without modifying working directory.

**4. Check If Behind Remote**
```bash
git rev-list --count HEAD..origin/main
```

If count > 0, local is behind remote.

**5. Pull Changes**
```bash
git pull origin main --ff-only
```

Using `--ff-only` ensures:
- No merge commits created
- Only fast-forward updates allowed
- Fails if local has diverged (needs manual resolution)

**6. Verify Sync Success**
```bash
# Should show "Your branch is up to date with 'origin/main'"
git status

# Verify latest commit matches remote
git log -1 --oneline
git log origin/main -1 --oneline
```

**7. Report Status**
```
✅ Main branch synchronized
- Fetched latest changes from origin
- Fast-forwarded to origin/main
- Current commit: abc1234 Fix session bug
- Branch is up to date
```

### Error Handling

#### Diverged Branches (Local Commits on Main)

If `git pull --ff-only` fails:

```bash
# Check divergence
git log HEAD..origin/main --oneline  # Remote commits
git log origin/main..HEAD --oneline  # Local commits
```

**Resolution Options:**

1. **No Local Commits (should be normal):**
   ```bash
   git reset --hard origin/main
   ```

2. **Local Commits Exist (unexpected):**
   - **STOP and WARN USER**
   - Main branch should not have local commits
   - Ask user:
     - Move commits to feature branch?
     - Discard local commits?
     - Manual resolution needed?

#### Merge Conflicts

Should not happen on main (main should be clean), but if it does:
- **STOP and ALERT USER**
- Main branch has been modified locally
- Needs manual intervention

#### Network Issues

```bash
git fetch origin
# If fails, check network
git remote -v
```

Report to user: "Unable to fetch from remote. Check network connection."

### Pre-Sync Validation

Before syncing, verify:

**1. No Active Worktrees on Main**
```bash
git worktree list | grep "\[main\]"
```

If main is checked out in multiple places, this could cause issues.

**2. Clean Working Directory**
```bash
git status --short
```

Main should typically be clean.

**3. Remote Is Reachable**
```bash
git ls-remote origin main
```

Verifies remote connectivity.

### Post-Sync Actions

After successful sync:

**1. Verify Worktrees Still Valid**

Existing worktrees are based on old main commits, which is fine. They'll be rebased or merged when creating PRs.

**2. Report Summary**
```bash
# Show what changed
git log --oneline --graph --decorate -10

# Count new commits
git rev-list --count @{1}..HEAD
```

**3. Inform User**
```
✅ Sync complete - 5 new commits pulled
- Latest: Fix authentication timeout
- Ready to create new worktrees based on current main
```

### Best Practices

**When to Sync:**
- Beginning of work session
- Before spawning workers for new issues
- After being notified of merged PRs
- When explicitly requested

**When NOT to Sync:**
- While workers are running (doesn't affect them)
- During active development on main (shouldn't happen)
- When network is unavailable

**Frequency:**
- At least once per work session
- Before each new batch of issues
- After multiple PRs merged to main

## Examples

### Example 1: Simple sync (no changes)
```
Context: Local main is up to date

Actions:
1. git checkout main
2. git fetch origin
3. git pull origin main --ff-only
4. git status

Result: "Already up to date"
```

### Example 2: Sync with new commits
```
Context: 3 PRs were merged since last sync

Actions:
1. git checkout main
2. git fetch origin
3. git rev-list --count HEAD..origin/main
   → Output: 3
4. git pull origin main --ff-only
5. git log --oneline -3

Result:
✅ Main branch synchronized
- Pulled 3 new commits
- Latest: Fix session timeout (abc1234)
- Ready for new issue work
```

### Example 3: Sync from feature branch
```
Context: Currently on feature branch

Actions:
1. git branch --show-current
   → Output: feature/issue-123
2. git checkout main
3. git fetch origin
4. git pull origin main --ff-only
5. git checkout feature/issue-123

Result: Main updated, returned to feature branch
```

### Example 4: Uncommitted changes on main (unexpected)
```
Context: Main has uncommitted changes (shouldn't happen)

Actions:
1. git checkout main
2. git status --short
   → Output: M src/config.py
3. WARN USER: "Uncommitted changes on main branch detected"
4. Ask user: "Options:
   - Stash changes: git stash
   - Discard changes: git restore .
   - Abort sync"
5. Based on choice, proceed or abort

Result: User handles unexpected state
```

### Example 5: Diverged main (local commits)
```
Context: Main has local commits (shouldn't happen)

Actions:
1. git checkout main
2. git fetch origin
3. git pull origin main --ff-only
   → Error: "fatal: Not possible to fast-forward"
4. git log origin/main..HEAD --oneline
   → Output: 2 local commits
5. ALERT USER: "Main branch has local commits"
6. Ask: "Options:
   - Reset to origin/main (discard local)
   - Move commits to feature branch
   - Manual resolution"
7. Based on choice:
   - Reset: git reset --hard origin/main
   - Feature branch: git checkout -b recover/main-commits && git checkout main && git reset --hard origin/main
   - Manual: Stop and let user handle

Result: Main synchronized, local commits preserved if requested
```

### Example 6: Sync before spawning workers
```
Context: About to spawn workers for issues #123, #456, #789

Actions:
1. git checkout main
2. git fetch origin
3. git pull origin main --ff-only
4. git log -1 --oneline
   → Latest commit shown
5. Report: "Main synchronized - ready to spawn 3 workers"

Result: All workers will be based on latest main
```
