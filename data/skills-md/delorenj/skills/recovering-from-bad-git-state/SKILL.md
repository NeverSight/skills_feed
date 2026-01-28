---
name: recovering-from-bad-git-state
description: Techniques for diagnosing and recovering from corrupted git state, orphaned worktrees, and inconsistent branch references.
---

# Git State Recovery Specialist

Use this skill when encountering corrupted git state, orphaned worktrees, or inconsistent branch references that prevent normal git operations.

## When to Use

Invoke proactively when you observe:

- `git worktree list` showing `00000000` commit hashes
- `git branch --show-current` contradicting actual HEAD state
- Worktree operations failing with "already used by worktree" errors
- HEAD pointing to non-existent branch refs
- Branch deletion failing due to phantom worktree claims
- `git status` showing "HEAD detached" unexpectedly

## Core Diagnostic Sequence

### 1. State Validation

```bash
# Check HEAD integrity
cat .git/HEAD
# Should show: ref: refs/heads/<branch-name>

# Verify worktree consistency
git worktree list
# Look for: invalid commit hashes (00000000), missing paths

# Cross-check branch state
git branch --show-current
git symbolic-ref HEAD
# These should agree
```

### 2. Identify Corruption Type

**Type A: Corrupted HEAD Reference**

- Symptoms: HEAD points to non-existent branch, operations fail with "unknown revision"
- Cause: Incomplete checkout or branch deletion while HEAD pointed to it
- Recovery: Force reset HEAD to known good branch

**Type B: Orphaned Worktree Metadata**

- Symptoms: `git worktree list` shows worktree but directory doesn't exist
- Cause: Manual directory deletion without `git worktree remove`
- Recovery: Prune stale worktree references

**Type C: Branch Lock Conflict**

- Symptoms: "branch is already used by worktree" but `git worktree list` shows different branch
- Cause: Worktree checked out branch, then had HEAD forcibly changed
- Recovery: Align HEAD with actual branch or force checkout

## Recovery Operations

### Fix Corrupted HEAD

```bash
# Identify correct branch from remote
git branch -r | grep main  # or master, develop, etc.

# Force reset HEAD (bypasses git safety checks)
echo "ref: refs/heads/main" > .git/HEAD

# Verify fix
git status
git branch --show-current
```

### Prune Orphaned Worktrees

```bash
# Standard prune (removes references to deleted directories)
git worktree prune -v

# If prune fails, manual cleanup
rm -rf .git/worktrees/<worktree-name>

# Verify cleanup
git worktree list
```

### Resolve Branch Lock Conflicts

```bash
# Option 1: Align HEAD with intended branch
git reset --hard origin/main

# Option 2: Force delete phantom worktree claim
# First ensure you're on a different branch
git checkout main
# Then force delete the locked branch
git branch -D <locked-branch>
git push origin --delete <locked-branch>  # if pushed
```

### Nuclear Option: Rebuild Branch Refs

```bash
# When refs are completely corrupted
git fetch --all --prune

# Recreate local branch from remote
git branch -D <branch-name>
git checkout -b <branch-name> origin/<branch-name>

# Verify state
git log --oneline -5
```

## Prevention Patterns

### Safe Worktree Operations

```bash
# Always use git worktree commands, never manual directory operations
git worktree add <path> <branch>    # Create
git worktree remove <path>          # Delete (not rm -rf)
git worktree prune                  # Clean stale refs
```

### Validate State Before Operations

```rust
// Example: iMi worktree manager
fn validate_repo_state(&self, repo: &Repository) -> Result<()> {
    let head = repo.head()?;

    // Ensure HEAD points to valid commit
    if head.target().is_none() {
        return Err(anyhow::anyhow!(
            "Repository HEAD is corrupted. Run git-state-recovery."
        ));
    }

    // Verify worktree list consistency
    let worktrees = repo.worktrees()?;
    for wt in worktrees.iter().flatten() {
        let wt_path = repo.workdir()
            .unwrap()
            .parent()
            .unwrap()
            .join(wt);
        if !wt_path.exists() {
            eprintln!("Warning: Orphaned worktree detected: {}", wt);
        }
    }

    Ok(())
}
```

## Integration with iMi

When building worktree management tools, add state validation hooks:

```rust
// Before any worktree operation
pub async fn create_worktree(&self, ...) -> Result<PathBuf> {
    // Validate repository state first
    self.validate_repo_state(&repo)?;

    // Proceed with operation
    self.git.create_worktree(...)?;

    // Verify post-operation state
    self.validate_worktree_created(&worktree_path)?;

    Ok(worktree_path)
}
```

## Common Edge Cases

### Case 1: Trunk Directory Checked Out to PR Branch

**Symptom:** `imi pr <num>` switches trunk to PR branch instead of creating separate worktree

**Root Cause:** `gh pr checkout` checks out in current directory as side effect

**Fix:** Fetch PR without checkout

```bash
# Get PR head ref
PR_REF=$(gh pr view <num> --json headRefName -q .headRefName)

# Fetch without checkout
git fetch origin $PR_REF:pr-<num>

# Create worktree from fetched ref
git worktree add ../pr-<num> pr-<num>
```

### Case 2: Multiple Repos with Same Worktree Name

**Symptom:** Creating `pr-123` in repo B fails because repo A has `pr-123`

**Root Cause:** Git worktree names are globally unique per repository

**Fix:** Use repo-prefixed worktree names

```rust
let worktree_name = format!("{}-pr-{}", repo_name, pr_number);
```

## Testing Recovery Procedures

Before deploying worktree automation:

```bash
# Create test scenario
git init test-repo && cd test-repo
git commit --allow-empty -m "init"
git worktree add ../test-wt

# Corrupt state
rm -rf ../test-wt
# Don't run git worktree prune yet

# Verify corruption detection
git worktree list  # Should show test-wt but invalid path

# Test recovery
git worktree prune -v
git worktree list  # Should be clean
```

## Escalation Path

If recovery procedures fail:

1. Backup corrupted repository: `tar -czf repo-backup.tar.gz .git/`
2. Clone fresh from remote: `git clone <url> repo-fresh`
3. Manually recreate worktrees from backup database/records
4. Document failure mode for future prevention

## Related Skills

- `ecosystem-patterns`: Composable git operations section
- `mise-task-managing`: Git workflow automation patterns
