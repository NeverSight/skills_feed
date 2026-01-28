---
name: git-state-validator
description: Check git repository status, detect conflicts, and validate branch state before operations. Use when verifying working directory cleanliness, checking for conflicts, or validating branch state.
---

# Git State Validator

## Instructions

### When to Invoke This Skill
- Before creating new branches
- Before switching branches
- Before merging or pulling
- After conflicts occur
- When verifying clean working directory
- Before committing changes

### Core Validations

1. **Working Directory Status** - Check for uncommitted changes
2. **Branch Validation** - Verify current branch and relationship to main
3. **Conflict Detection** - Identify merge conflicts
4. **Remote Sync Status** - Check if local is ahead/behind remote
5. **Repository Health** - Verify git repository integrity

### Standard Workflows

#### Check Working Directory Status

1. **Get Status**
   ```bash
   git status
   ```

2. **Parse Output**
   - **Clean**: "nothing to commit, working tree clean"
   - **Unstaged changes**: Modified files not added
   - **Staged changes**: Files added but not committed
   - **Untracked files**: New files not added to git

3. **Get Machine-Readable Status**
   ```bash
   git status --porcelain
   ```
   Prefixes:
   - `M` - Modified
   - `A` - Added
   - `D` - Deleted
   - `??` - Untracked
   - `UU` - Merge conflict

#### Validate Branch State

1. **Get Current Branch**
   ```bash
   git branch --show-current
   ```

2. **Check if on Main**
   ```bash
   git branch --show-current | grep -E "^(main|master)$"
   ```

3. **Get Branch List**
   ```bash
   git branch -a
   ```
   - Local branches (no prefix)
   - Remote branches (remotes/origin/...)

4. **Check Branch Relationship**
   ```bash
   git merge-base --is-ancestor main HEAD
   ```
   Exit code 0: Current branch is based on main

#### Detect Conflicts

1. **Check for Conflict Markers**
   ```bash
   git diff --check
   ```

2. **List Conflicted Files**
   ```bash
   git diff --name-only --diff-filter=U
   ```

3. **View Conflict Details**
   ```bash
   git status
   ```
   Look for "both modified" or "both added"

4. **Analyze Conflict Markers**
   Search files for:
   ```
   <<<<<<< HEAD
   <current changes>
   =======
   <incoming changes>
   >>>>>>> branch-name
   ```

#### Check Remote Sync Status

1. **Fetch Remote State** (without merging)
   ```bash
   git fetch origin
   ```

2. **Compare with Remote**
   ```bash
   git status -sb
   ```
   Output patterns:
   - `[ahead 3]` - Local has 3 commits not pushed
   - `[behind 2]` - Remote has 2 commits not pulled
   - `[ahead 1, behind 2]` - Both have unpushed/unpulled commits

3. **View Unpushed Commits**
   ```bash
   git log origin/main..HEAD --oneline
   ```

4. **View Unpulled Commits**
   ```bash
   git log HEAD..origin/main --oneline
   ```

#### Validate Repository Health

1. **Check Repository Integrity**
   ```bash
   git fsck --full
   ```

2. **Verify Object Database**
   ```bash
   git count-objects -v
   ```

3. **Check for Corrupted Objects**
   ```bash
   git fsck --lost-found
   ```

### Common Status Interpretations

#### Clean Working Directory
```
$ git status
On branch feat/new-feature
nothing to commit, working tree clean
```
**Interpretation**: Safe to switch branches, merge, or create new branch

#### Uncommitted Changes
```
$ git status
On branch feat/new-feature
Changes not staged for commit:
  modified:   src/main.py
  modified:   src/utils.py
```
**Interpretation**: Need to commit or stash before branch operations

#### Merge Conflict
```
$ git status
On branch feat/new-feature
You have unmerged paths.

Unmerged paths:
  both modified:   src/config.py
```
**Interpretation**: Must resolve conflicts before proceeding

#### Ahead of Remote
```
$ git status -sb
## feat/new-feature...origin/feat/new-feature [ahead 3]
```
**Interpretation**: Local has 3 commits not pushed to remote

#### Behind Remote
```
$ git status -sb
## main...origin/main [behind 5]
```
**Interpretation**: Remote has 5 commits not pulled locally

### Error Scenarios

**Not a Git Repository:**
```
fatal: not a git repository (or any of the parent directories): .git
```
**Action**: Navigate to git repository or run `git init`

**Detached HEAD State:**
```
HEAD detached at <commit>
```
**Action**: Create branch or checkout existing branch

**Corrupted Repository:**
```
error: object file .git/objects/... is empty
```
**Action**: Try `git fsck`, may need to restore from backup

## Examples

### Example 1: Pre-branch creation validation
```
Context: About to create new feature branch
Action:
1. Check status: git status
2. Verify on main: git branch --show-current
3. Check for uncommitted changes: git status --porcelain
4. Verify remote sync: git status -sb
Output: "Working directory clean, on main, synced with remote - safe to create branch"
```

### Example 2: Detect merge conflicts
```
Context: Pull resulted in conflicts
Action:
1. Run git status
2. Identify "both modified" files
3. List conflicted files: git diff --name-only --diff-filter=U
4. For each file, read and identify conflict markers
Output: "3 files have conflicts: src/main.py, src/utils.py, src/config.py"
```

### Example 3: Validate before commit
```
Context: Ready to commit changes
Action:
1. Check branch: git branch --show-current
2. Verify not on main: Ensure branch name != main/master
3. Review changes: git status
4. View diff: git diff
Output: "On feature branch with 5 modified files - safe to commit"
```

### Example 4: Sync status check
```
Context: Before pushing changes
Action:
1. Fetch remote: git fetch origin
2. Check status: git status -sb
3. If behind: Suggest pull first
4. If ahead: Confirm ready to push
Output: "Local is ahead by 2 commits - ready to push"
```
