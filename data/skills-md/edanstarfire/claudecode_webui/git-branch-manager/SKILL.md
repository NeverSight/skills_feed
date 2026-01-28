---
name: git-branch-manager
description: Create, switch, and manage git branches with proper handling of uncommitted changes. Use when creating feature branches, switching contexts, or cleaning up after merges.
---

# Git Branch Manager

## Instructions

### When to Invoke This Skill
- Creating a new feature/fix/chore branch
- Switching between branches
- Cleaning up merged branches
- Handling uncommitted changes before branch operations
- Validating current branch state

### Core Capabilities

1. **Branch Creation** - Create properly named branches from main
2. **Branch Switching** - Safe branch changes with uncommitted change handling
3. **Branch Cleanup** - Remove local branches after merge
4. **Branch Validation** - Verify branch state and history

### Standard Workflows

#### Creating a New Branch

1. **Check Repository State**
   **Invoke the `git-state-validator` skill** to verify:
   - Current branch status
   - Uncommitted changes
   - Working directory state

2. **Handle Uncommitted Changes**
   If changes exist, ask user:
   - **Stash**: `git stash push -m "WIP: switching to new branch"`
   - **Commit**: Guide through commit process first
   - **Abort**: Cancel branch creation

3. **Ensure Latest Main**
   ```bash
   git checkout main
   git fetch origin
   git pull origin main
   ```

4. **Determine Branch Prefix**
   Based on work type:
   - `feat/` - New features
   - `fix/` - Bug fixes
   - `chore/` - Maintenance, tooling
   - `docs/` - Documentation
   - `refactor/` - Code refactoring
   - `test/` - Test additions/fixes
   - `perf/` - Performance improvements

5. **Create Branch**
   ```bash
   git checkout -b <prefix>/<description>
   ```

   Branch name format:
   - Use kebab-case
   - Maximum 50 characters
   - Descriptive but concise
   - Example: `feat/add-user-authentication`

#### Switching Branches

1. **Check Repository State**
   **Invoke the `git-state-validator` skill** to verify:
   - Current branch name
   - Uncommitted changes
   - Working directory status

2. **Handle Changes** (if any)
   - Offer to stash, commit, or abort
   - If stash: `git stash push -m "WIP: switching from <current> to <target>"`

3. **Switch Branch**
   ```bash
   git checkout <branch-name>
   ```

4. **Restore Stash** (if applicable)
   After switching, if user stashed:
   ```bash
   git stash list
   git stash pop
   ```

#### Cleaning Up Branches

1. **Verify Branch is Merged**
   ```bash
   git branch --merged main
   ```

2. **Switch to Main** (if on the branch being deleted)
   ```bash
   git checkout main
   ```

3. **Check Branch Exists Before Deletion**
   ```bash
   git branch --list <branch-name>
   ```
   If no output, branch doesn't exist - skip deletion

4. **Delete Local Branch** (only if exists)
   ```bash
   git branch -d <branch-name>
   ```

   Use `-D` (force delete) only if user explicitly confirms:
   ```bash
   git branch -D <branch-name>
   ```

5. **Verify Deletion**
   ```bash
   git branch --list <branch-name>
   ```

### Safe Branch Deletion Helper

**CRITICAL**: Always check if branch exists before attempting deletion to avoid errors.

**Safe Deletion Pattern:**
```bash
# Check if branch exists
if git branch --list <branch-name> | grep -q <branch-name>; then
  git branch -d <branch-name>
  echo "Branch deleted"
else
  echo "Branch does not exist, skipping"
fi
```

**Why This Matters:**
- Prevents "branch not found" errors in automated workflows
- Handles cases where remote deletion already removed local tracking branch
- Makes cleanup scripts idempotent (safe to run multiple times)

### Branch Naming Conventions

**Good Examples:**
- `feat/user-profile-page`
- `fix/login-validation-error`
- `chore/update-dependencies`
- `docs/api-endpoint-guide`

**Bad Examples:**
- `my-branch` (no type prefix)
- `feat/ThisIsMyNewFeature` (not kebab-case)
- `feat/add-the-new-user-profile-page-with-authentication-and-settings` (too long)

### Error Handling

**Branch Already Exists:**
Ask user to:
- Switch to existing: `git checkout <branch-name>`
- Delete and recreate: `git branch -D <branch-name> && git checkout -b <branch-name>`
- Choose different name

**Uncommitted Changes Conflict:**
```
error: Your local changes to the following files would be overwritten by checkout
```
- Must stash or commit changes first
- Cannot proceed without handling changes

**Merge Conflicts When Pulling:**
```
error: Merge conflict in <file>
```
- Must resolve conflicts before creating branch
- Guide user through conflict resolution

**Cannot Delete Current Branch:**
```
error: Cannot delete branch '<name>' checked out at '<path>'
```
- Must switch to different branch first
- Run: `git checkout main` then retry delete

## Examples

### Example 1: Create feature branch for issue
```
Context: Working on issue #42 to add dark mode
Action:
1. Check uncommitted changes (none found)
2. Switch to main: git checkout main
3. Update main: git pull origin main
4. Create branch: git checkout -b feat/add-dark-mode-toggle
Output: "Created and switched to feat/add-dark-mode-toggle"
```

### Example 2: Switch branches with uncommitted work
```
Context: User has uncommitted changes, wants to switch branches
Action:
1. Detect uncommitted changes
2. Ask user: "You have uncommitted changes. Stash, commit, or abort?"
3. User chooses stash
4. Run: git stash push -m "WIP: switching branches"
5. Switch: git checkout other-branch
6. Offer to pop stash if returning later
```

### Example 3: Clean up after merge
```
Context: PR merged, need to clean up local branch
Action:
1. Verify branch is merged: git branch --merged main
2. Switch to main: git checkout main
3. Check if branch exists: git branch --list feat/old-feature
4. Delete branch (if exists): git branch -d feat/old-feature
5. Update main: git pull origin main
Output: "Branch cleaned up, main is up to date"
```

### Example 4: Handle branch naming
```
Context: User wants to fix a bug in login validation
Action:
1. Determine type: "fix" (bug fix)
2. Extract description: "login validation"
3. Format: fix/login-validation-error
4. Create: git checkout -b fix/login-validation-error
```
