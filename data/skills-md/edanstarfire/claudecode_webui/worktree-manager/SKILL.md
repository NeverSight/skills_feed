---
name: worktree-manager
description: Manage git worktrees for isolated issue work. Create, list, and remove worktrees safely.
---

# Worktree Manager

## Instructions

### When to Invoke This Skill
- Creating isolated worktree for issue work
- Listing all active worktrees
- Removing worktree after issue merged
- Checking worktree status
- Troubleshooting worktree issues

### Git Worktree Overview

Git worktrees allow multiple working directories from a single repository:
- Each worktree can be on a different branch
- Changes in one worktree don't affect others
- Perfect for parallel issue work
- Cleaner than stashing or multiple clones

### Standard Workflows

#### Creating a Worktree

**1. Ensure Worktrees Directory Exists**
```bash
mkdir -p worktrees
```

**2. Verify Worktree Doesn't Already Exist**
```bash
git worktree list | grep "worktrees/issue-$ISSUE_NUMBER"
```

If exists, inform user and ask if they want to remove and recreate.

**3. Create Worktree from Main**
```bash
# Ensure main is up to date
git fetch origin main

# Create worktree with new branch
git worktree add -b feature/issue-$ISSUE_NUMBER worktrees/issue-$ISSUE_NUMBER origin/main
```

**Branch Naming Convention:**
- `feature/issue-$N` - New features
- `fix/issue-$N` - Bug fixes
- `refactor/issue-$N` - Refactoring
- `docs/issue-$N` - Documentation

Determine prefix by analyzing issue labels/title.

**4. Verify Creation**
```bash
git worktree list
ls -la worktrees/issue-$ISSUE_NUMBER
```

**5. Report Success**
Inform user:
```
✅ Worktree created successfully
- Location: worktrees/issue-$ISSUE_NUMBER/
- Branch: feature/issue-$ISSUE_NUMBER
- Based on: origin/main
- Status: Ready for work
```

#### Listing Worktrees

**1. Get All Worktrees**
```bash
git worktree list
```

**2. Parse Output**
Format shows:
```
/path/to/repo              abc1234 [main]
/path/to/repo/worktrees/issue-123  def5678 [feature/issue-123]
/path/to/repo/worktrees/issue-456  ghi9012 [fix/issue-456]
```

**3. Enhanced Status**
For each worktree, check:
```bash
# Get branch status
cd worktrees/issue-$N && git status --short --branch

# Get last commit
cd worktrees/issue-$N && git log -1 --oneline
```

**4. Display Formatted List**
```
📁 Active Worktrees
===================

worktrees/issue-123/
  Branch: feature/issue-123
  Status: 2 files modified, 1 file added
  Last Commit: Add user authentication endpoint

worktrees/issue-456/
  Branch: fix/issue-456
  Status: Clean working directory
  Last Commit: Fix session timeout bug
```

#### Removing a Worktree

**CRITICAL**: Only remove worktrees after PR is merged and branch is deleted.

**1. Verify Worktree Exists**
```bash
git worktree list | grep "worktrees/issue-$ISSUE_NUMBER"
```

**2. Check for Uncommitted Changes**
```bash
cd worktrees/issue-$ISSUE_NUMBER && git status --short
```

If uncommitted changes exist:
- **STOP** - Warn user
- Ask if they want to:
  - Commit changes first
  - Discard changes
  - Abort removal

**3. Remove Worktree**
```bash
git worktree remove worktrees/issue-$ISSUE_NUMBER
```

**4. If Locked (Process Using It)**
```bash
# Force removal if locked and confirmed by user
git worktree remove --force worktrees/issue-$ISSUE_NUMBER
```

**5. Prune Stale References**
```bash
git worktree prune
```

**6. Verify Removal**
```bash
git worktree list
ls worktrees/
```

**7. Clean Up Empty Directory**
```bash
# If worktrees/ is now empty, optionally remove it
if [ -z "$(ls -A worktrees/)" ]; then
  rmdir worktrees/
fi
```

**8. Report Success**
```
✅ Worktree removed successfully
- Removed: worktrees/issue-$ISSUE_NUMBER/
- Branch reference pruned
- Ready for new worktrees
```

#### Troubleshooting Worktrees

**Locked Worktree**
```bash
# Check lock reason
cat worktrees/issue-$N/.git | head -1

# Remove lock if safe
rm -f .git/worktrees/issue-$N/lock
```

**Orphaned Worktree (directory exists but not in git)**
```bash
# Prune git references
git worktree prune

# Manually remove directory
rm -rf worktrees/issue-$N/
```

**Corrupted Worktree**
```bash
# Remove and recreate
git worktree remove --force worktrees/issue-$N
git worktree prune
git worktree add -b feature/issue-$N worktrees/issue-$N origin/main
```

### Best Practices

**Before Creating:**
- Always base on latest origin/main
- Use consistent naming: `worktrees/issue-$N/`
- Use semantic branch names: `feature/issue-$N`

**During Use:**
- Each worktree is independent
- Don't move or rename worktree directories manually
- Commit regularly within worktree

**Before Removing:**
- Verify PR is merged
- Verify remote branch is deleted
- Check for uncommitted changes
- Consider archiving important local changes

**Directory Structure:**
```
repository/
├── .git/
├── src/                    # Main repo files
├── worktrees/             # All worktrees
│   ├── issue-123/         # Worktree for issue 123
│   │   ├── src/
│   │   └── .git           # Worktree git link
│   └── issue-456/         # Worktree for issue 456
│       ├── src/
│       └── .git
```

### Safety Checks

**Always verify before creating:**
1. Main branch is up to date
2. Worktree path doesn't already exist
3. Branch name is unique

**Always verify before removing:**
1. PR is merged (ask user to confirm)
2. No uncommitted changes or user approves discarding
3. No processes using the worktree

**Never:**
- Create worktree with existing branch name
- Remove worktree while process is running in it
- Manually delete worktree directory (use git worktree remove)
- Share worktrees between different repositories

## Examples

### Example 1: Create worktree for new feature
```
Context: Issue #123 is a new user profile feature

Actions:
1. mkdir -p worktrees
2. git fetch origin main
3. git worktree add -b feature/issue-123 worktrees/issue-123 origin/main
4. Verify with git worktree list

Result: Clean worktree ready for development
```

### Example 2: Create worktree for bug fix
```
Context: Issue #456 is a bug in session management

Actions:
1. mkdir -p worktrees
2. git fetch origin main
3. git worktree add -b fix/issue-456 worktrees/issue-456 origin/main
4. Verify creation

Result: Isolated environment for bug fix
```

### Example 3: Remove worktree after merge
```
Context: Issue #123 PR was merged and branch deleted

Actions:
1. cd worktrees/issue-123 && git status --short
2. Verify no uncommitted changes
3. cd ../..
4. git worktree remove worktrees/issue-123
5. git worktree prune
6. Verify removal

Result: Worktree cleanly removed
```

### Example 4: Handle uncommitted changes before removal
```
Context: Worktree has uncommitted changes, PR is merged

Actions:
1. cd worktrees/issue-456 && git status
2. Detect uncommitted changes
3. Ask user: "Uncommitted changes found. Options:
   - Commit them to a local branch for reference
   - Discard changes
   - Abort removal"
4. Based on user choice:
   - Commit: git checkout -b archive/issue-456 && git commit
   - Discard: git worktree remove --force
   - Abort: Stop and return

Result: User decides fate of uncommitted work
```

### Example 5: List all active worktrees with status
```
Context: User wants to see all active issue work

Actions:
1. git worktree list
2. For each worktree:
   - cd into it
   - git status --short --branch
   - git log -1 --oneline
3. Format output

Result:
📁 Active Worktrees
===================

worktrees/issue-123/
  Branch: feature/issue-123 (ahead 3)
  Status: M src/auth.py, A src/profile.py
  Last Commit: Add profile endpoint

worktrees/issue-456/
  Branch: fix/issue-456 (ahead 1)
  Status: Clean
  Last Commit: Fix session timeout
```
