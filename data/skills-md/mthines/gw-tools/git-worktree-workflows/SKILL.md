---
name: "@gw-git-worktree-workflows"
description: Master Git worktrees and gw-tools workflows for parallel development. Use this skill when creating worktrees, managing multiple branches simultaneously, navigating between worktrees, troubleshooting worktree issues, or setting up feature branch workflows. Triggers on tasks involving git worktree commands, branch isolation, parallel development, or gw CLI usage.
license: MIT
metadata:
  author: mthines
  version: "1.0.0"
---

# Git Worktree Workflows - Comprehensive Guide

This guide teaches you how to master Git worktrees using the `gw` CLI tool for optimized development workflows.

## Table of Contents

1. [Git Worktree Fundamentals](#1-git-worktree-fundamentals)
2. [Creating and Managing Worktrees with gw](#2-creating-and-managing-worktrees-with-gw)
3. [Navigating Between Worktrees](#3-navigating-between-worktrees)
4. [Listing and Inspecting Worktrees](#4-listing-and-inspecting-worktrees)
5. [Common Workflow Patterns](#5-common-workflow-patterns)
6. [Cleanup and Maintenance](#6-cleanup-and-maintenance)
7. [Troubleshooting Common Issues](#7-troubleshooting-common-issues)

---

## 1. Git Worktree Fundamentals

### What are Git Worktrees?

Git worktrees allow you to have multiple working directories attached to a single repository. Instead of switching branches in your current directory, you can check out different branches in separate directories simultaneously.

**Traditional branch switching:**
```bash
# Your current work is interrupted
git checkout feature-a     # Work on feature A
git checkout feature-b     # Switch context, lose focus
git checkout main          # Switch again for hotfix
```

**With worktrees:**
```bash
# Each branch has its own directory
/repo.git/main/           # Main branch always ready
/repo.git/feature-a/      # Feature A development
/repo.git/feature-b/      # Feature B development in parallel
/repo.git/hotfix-123/     # Hotfix without interrupting features
```

### Worktree vs Branch Switching vs Cloning

| Approach | Pros | Cons |
|----------|------|------|
| **Branch Switching** | Single directory, less disk space | Interrupts work, requires stashing, IDE reindexes |
| **Worktrees** | Parallel work, no interruption, shared Git history | Slightly more disk space for working files |
| **Cloning** | Complete isolation | Huge disk space, separate Git history, harder to sync |

### When Worktrees Shine

Worktrees are ideal for:

- **Parallel feature development** - Work on multiple features without context switching
- **Hotfix workflows** - Handle urgent bugs while continuing feature work
- **Code reviews** - Check out PR branches without disrupting your current work
- **Testing** - Test multiple versions or configurations simultaneously
- **Long-running experiments** - Keep experimental branches separate from main work
- **Build artifacts** - Separate build processes without conflicts

### Worktree Limitations and Gotchas

**What worktrees share:**
- ✅ Git repository (.git directory)
- ✅ Commit history and objects
- ✅ Branches and tags
- ✅ Stashes
- ✅ Hooks and config

**What worktrees DON'T share:**
- ❌ Working directory files
- ❌ Untracked files
- ❌ node_modules (unless symlinked)
- ❌ Build artifacts
- ❌ .env files (unless copied)

**Important limitations:**
- You cannot check out the same branch in multiple worktrees simultaneously
- Each worktree needs its own dependencies installed (node_modules, vendor/, etc.)
- IDE workspace settings may need adjustment for each worktree
- Some Git UI tools have limited worktree support

---

## 2. Creating and Managing Worktrees with gw

### The `gw add` Command

The `gw add` command is an enhanced version of `git worktree add` with automatic file copying:

```bash
# Basic usage - create worktree for existing branch
gw add feature-auth

# Create worktree with new branch
gw add feature-payments -b feature-payments

# Create from specific start point
gw add hotfix-security -b hotfix-security main

# Force creation (even if branch already checked out elsewhere)
gw add feature-test --force
```

### Auto-Copying Files

When creating worktrees with `gw add`, files configured in `.gw/config.json` are automatically copied:

```json
{
  "root": "/Users/you/projects/myapp.git",
  "defaultBranch": "main",
  "autoCopyFiles": [
    ".env",
    ".env.local",
    "secrets/",
    "components/ui/.vercel/"
  ]
}
```

**What gets copied:**
- Environment files (.env, .env.local)
- Secrets and credentials
- Local configuration
- Cache directories (if needed)

**What should NOT be auto-copied:**
- node_modules (install fresh or symlink)
- Build artifacts (build fresh)
- Large binary files
- IDE settings (.vscode/, .idea/)

Example creating a worktree with auto-copy:

```bash
$ gw add feature-new-dashboard

Creating worktree feature-new-dashboard...
✓ Branch 'feature-new-dashboard' set up to track 'origin/main'
✓ Worktree created: /projects/myapp.git/feature-new-dashboard

Copying files from main...
✓ Copied: .env
✓ Copied: .env.local
✓ Copied: secrets/api-keys.json
✓ Copied: components/ui/.vercel/

Done! Navigate with: gw cd feature-new-dashboard
```

### Manual File Copying with `gw sync`

If you need to copy files later or from a different source:

```bash
# Copy all autoCopyFiles from config (if configured)
gw sync feature-auth

# Copy specific files from main to current worktree
gw sync feature-auth .env components/agents/.env

# Copy from a different worktree
gw sync --from staging feature-auth .env
```

### Tracking vs Detached HEAD States

**Tracking branches** (recommended):
```bash
# Creates branch that tracks remote
gw add feature-x -b feature-x origin/main

# Shows branch relationship
$ git status
On branch feature-x
Your branch is up to date with 'origin/main'.
```

**Detached HEAD** (for temporary work):
```bash
# Check out specific commit
gw add temp-test --detach v1.2.3

# No branch, just a commit
$ git status
HEAD detached at v1.2.3
```

Use tracking branches for features you'll push. Use detached HEAD for temporary testing or inspecting old commits.

### Branch Creation Strategies

**Feature branches:**
```bash
# Branch from main
gw add feature-name -b feature-name main

# Branch from develop
gw add feature-name -b feature-name develop
```

**Hotfix branches:**
```bash
# Branch from production tag
gw add hotfix-security -b hotfix-security v1.2.3

# Branch from main for immediate fix
gw add hotfix-critical -b hotfix-critical main
```

**Release branches:**
```bash
# Create release candidate from develop
gw add release-v2.0 -b release-v2.0 develop
```

---

## 3. Navigating Between Worktrees

### Using `gw cd` for Quick Navigation

The `gw cd` command provides smart navigation to worktrees:

```bash
# Full worktree name
gw cd feature-authentication

# Partial match (first match wins)
gw cd feat    # Matches feature-authentication if it's first

# Smart matching by branch name
gw cd auth    # Finds worktree with 'auth' in name
```

### Shell Integration

After installing `gw` via npm, a shell function is automatically installed:

```bash
# This is actually a shell function, not the binary
gw cd feature-auth

# The shell function:
# 1. Calls the actual gw binary
# 2. Gets the worktree path
# 3. Changes directory in your current shell
```

**Checking if shell integration is installed:**

```bash
# Test it
gw cd main
pwd  # Should show path to main worktree

# If not working, reinstall shell integration
gw install-shell
```

### IDE Workspace Management

**VS Code:**

Open each worktree as a separate window:

```bash
gw cd feature-a
code .
```

Or use multi-root workspaces:

```json
// myapp.code-workspace
{
  "folders": [
    {" "name": "Main",
      "path": "/projects/myapp.git/main"
    },
    {
      "name": "Feature A",
      "path": "/projects/myapp.git/feature-a"
    },
    {
      "name": "Feature B",
      "path": "/projects/myapp.git/feature-b"
    }
  ]
}
```

**JetBrains IDEs (WebStorm, IntelliJ, etc.):**

Each worktree can be its own project:

```bash
gw cd feature-a
idea .
```

Or attach multiple source roots to a single project.

---

## 4. Listing and Inspecting Worktrees

### The `gw list` Command

List all worktrees in your repository:

```bash
$ gw list

/projects/myapp.git/main          abc123f [main]
/projects/myapp.git/feature-auth  def456a [feature-auth]
/projects/myapp.git/hotfix-bug    ghi789b [hotfix-bug] (detached)
/projects/myapp.git/old-feature   jkl012c [feature-old] (locked)
```

### Understanding Worktree States

**Normal worktree:**
```
/projects/myapp.git/feature-auth  def456a [feature-auth]
```
- Path, commit hash, branch name

**Detached HEAD:**
```
/projects/myapp.git/temp  xyz789d (detached)
```
- No branch, pointing to specific commit

**Locked worktree:**
```
/projects/myapp.git/protected  abc123f [protected] (locked)
```
- Cannot be removed with `gw remove` unless unlocked first

**Prunable worktree:**
```
/old/path/feature  abc123f [feature] (prunable)
```
- Directory was moved or deleted, reference still exists

### Finding Worktrees by Branch Name

```bash
# List all worktrees
gw list

# Filter with grep
gw list | grep feature

# Find specific branch
gw list | grep "\[main\]"
```

### Identifying the Main Worktree

The first worktree listed is the main worktree (the original repository):

```bash
$ gw list
/projects/myapp.git/main  abc123f [main]  ← Main worktree
/projects/myapp.git/feature  def456a [feature]
```

The main worktree:
- Contains the actual `.git` directory
- Cannot be removed
- Is the parent of all other worktrees

---

## 5. Common Workflow Patterns

### Feature Branch Development

**Scenario:** Starting a new feature without interrupting current work

```bash
# Currently working in main
pwd  # /projects/myapp.git/main

# Create feature worktree
gw add feature-user-profiles -b feature-user-profiles

# Navigate to new worktree
gw cd feature-user-profiles

# Work on feature
npm install
npm run dev

# Meanwhile, main worktree is untouched
```

**Benefit:** Your main branch stays clean and ready for hotfixes or other work.

### Keeping Feature Branches Up to Date

**Scenario:** Updating your feature branch with latest changes from main

```bash
# Working in feature worktree
gw cd feature-user-profiles

# Merge latest changes from main into your feature branch
gw pull

# Or merge from a different branch
gw pull --from develop

# Preview what would be merged
gw pull --dry-run
```

**Why use `gw pull` instead of `git pull`?**

When working in a worktree, you cannot simply checkout main to pull the latest changes because main is typically checked out in another worktree. The `gw pull` command solves this by:

1. Fetching the latest version of main (or specified branch) from remote
2. Merging it into your current branch without needing to switch worktrees
3. Handling conflicts and providing clear guidance

**Safety features:**
- Blocks if you have uncommitted changes (use `--force` to override)
- Blocks if you're in a detached HEAD state
- Provides clear guidance when merge conflicts occur

**Example workflow:**

```bash
# Start working on feature
gw cd feature-dashboard

# Work for a few days...
git add .
git commit -m "feat: add dashboard widgets"

# Meanwhile, main has new changes
# Update your feature branch with latest main
gw pull

# If there's a conflict, you'll get clear guidance:
# Resolve conflicts manually:
#   1. Edit conflicted files
#   2. git add <resolved-files>
#   3. git commit

# Continue working
git add .
git commit -m "feat: integrate new API endpoints from main"
```

**Benefit:** Keep your feature branch up to date without switching worktrees or manually managing fetch/merge operations.

### Hotfix Workflows While Continuing Feature Work

**Scenario:** Critical bug in production while working on a feature

```bash
# Currently working on feature-dashboard
gw cd feature-dashboard
# In the middle of uncommitted changes...

# Create hotfix worktree (doesn't interrupt feature work)
gw add hotfix-login-bug -b hotfix-login-bug main

# Navigate to hotfix
gw cd hotfix-login-bug

# Fix the bug
vim src/auth/login.js
git add .
git commit -m "fix: resolve login timeout issue"
git push origin hotfix-login-bug

# Go back to feature work
gw cd feature-dashboard
# All your uncommitted changes are still there!
```

**Benefit:** No need to stash, commit WIP, or lose context.

### Code Review Workflows

**Scenario:** Reviewing a teammate's PR without disrupting your work

```bash
# Create reviewer worktree
gw add review-pr-123 -b pr-123 origin/pr-123

# Navigate and review
gw cd review-pr-123
npm install
npm test
npm run dev  # Test the changes

# Run code reviews, add comments
git checkout -b pr-123-suggestions
# Make suggestions...

# Return to your work
gw cd feature-dashboard

# Clean up when done
gw remove review-pr-123
```

**Benefit:** Review code in a real environment without affecting your workspace.

### Testing Multiple Versions Simultaneously

**Scenario:** Testing a feature across Node.js 18 and Node.js 20

```bash
# Create worktrees for each test environment
gw add test-node18 -b feature-api
gw add test-node20 -b feature-api --force

# Set up Node 18 environment
gw cd test-node18
nvm use 18
npm install
npm test

# Set up Node 20 environment (in another terminal)
gw cd test-node20
nvm use 20
npm install
npm test

# Compare results
```

**Benefit:** Run tests in parallel, catch version-specific issues early.

### Long-Running Experiment Branches

**Scenario:** Trying a risky refactor without committing to it

```bash
# Create experiment worktree
gw add experiment-new-architecture -b experiment/new-arch

# Work on experiment over days/weeks
gw cd experiment-new-architecture
# Radical changes...

# Keep working on main features in other worktrees
gw cd feature-payments
# Normal work continues...

# Later: merge experiment if successful, or delete if not
gw cd experiment-new-architecture
git push origin experiment/new-arch  # Share with team

# Or abandon
gw remove experiment-new-architecture
```

**Benefit:** Experiment freely without risking main development.

---

## 6. Cleanup and Maintenance

### Removing Worktrees

**Safe removal:**

```bash
# Remove worktree (commits must be pushed or merged)
gw remove feature-completed

# Force removal (even with unpushed commits)
gw remove feature-abandoned --force
```

**What happens:**
- Working directory is deleted
- Worktree reference removed from Git
- Branch remains in repository (can still be checked out elsewhere)

### Cleaning Up Stale Worktrees

**Automatically remove old worktrees:**

```bash
# Preview what would be removed (safe to run)
gw clean --dry-run

# Remove stale worktrees older than configured threshold
gw clean

# Force removal (skips safety checks - dangerous!)
gw clean --force
```

**How it works:**
- Checks for worktrees older than the configured threshold (default: 7 days)
- By default, only removes worktrees with:
  - NO uncommitted changes
  - NO unpushed commits
- Always prompts for confirmation before deletion
- Never removes bare/main repository worktrees

**Configure the threshold:**

```bash
# Set to 14 days during initialization
gw init --clean-threshold 14

# Or manually edit .gw/config.json
{
  "cleanThreshold": 14
}
```

**Example workflow:**

```bash
# Check what would be cleaned
$ gw clean --dry-run
INFO: Checking for worktrees older than 7 days...

Worktrees to remove:
  ✗ old-feature-1 (14 days old)
  ✗ old-feature-2 (10 days old)

Skipped worktrees:
  ⚠ recent-feature - has uncommitted changes

# Review and clean
$ gw clean
Remove 2 worktree(s)?
Type 'yes' to confirm: yes

Removing old-feature-1...
  ✓ Removed

Removing old-feature-2...
  ✓ Removed

SUCCESS: Removed 2 worktree(s)
```

### Pruning Stale Worktree References

**Scenario:** You manually deleted a worktree directory

```bash
# This shows stale references
$ gw list
/projects/myapp.git/main      abc123f [main]
/projects/myapp.git/deleted   def456a [feature] (prunable)

# Clean up stale references
gw prune

# Confirm
$ gw list
/projects/myapp.git/main  abc123f [main]
```

### Locking/Unlocking Worktrees

**Protect a worktree from accidental removal:**

```bash
# Lock production deployment worktree
gw lock production-deploy

# Try to remove (fails)
$ gw remove production-deploy
fatal: 'production-deploy' is locked; use 'git worktree unlock' to remove

# Unlock when ready
gw unlock production-deploy
gw remove production-deploy
```

### Disk Space Management Strategies

**Check worktree sizes:**

```bash
du -sh /projects/myapp.git/*
# 150M main
# 145M feature-auth
# 892M feature-payments  # Lots of node_modules!
```

**Optimization strategies:**

1. **Share node_modules with symlinks** (advanced, use with caution):
```bash
# In feature worktree
rm -rf node_modules
ln -s ../main/node_modules node_modules
```

2. **Use pnpm** (shares packages automatically):
```bash
pnpm install  # Shares packages across worktrees
```

3. **Remove old worktrees regularly**:
```bash
# List and remove old feature worktrees
gw list | grep feature-old
gw remove feature-old-1 feature-old-2
```

4. **Archive instead of keeping:**
```bash
# Push branch, remove worktree
git push origin feature-complete
gw remove feature-complete
# Can recreate later if needed
```

---

## 7. Troubleshooting Common Issues

### "Worktree already exists" Errors

**Problem:**

```bash
$ gw add feature-auth
fatal: 'feature-auth' already exists
```

**Solution:**

```bash
# List existing worktrees
gw list

# Remove old worktree first
gw remove feature-auth

# Or use a different name
gw add feature-auth-v2
```

### Locked Worktree Recovery

**Problem:**

```bash
$ gw remove feature-x
fatal: 'feature-x' is locked
```

**Solution:**

```bash
# Unlock the worktree
gw unlock feature-x

# Now remove
gw remove feature-x
```

### Corrupted Worktree State

**Problem:**

```bash
$ gw cd feature-x
fatal: 'feature-x' does not appear to be a git repository
```

**Solution:**

```bash
# Repair worktree administrative files
gw repair

# If that doesn't work, remove and recreate
gw remove feature-x --force
gw add feature-x -b feature-x origin/feature-x
```

### Permission Issues

**Problem:**

```bash
$ gw add feature-y
fatal: could not create work tree dir 'feature-y': Permission denied
```

**Solution:**

```bash
# Check parent directory permissions
ls -la /projects/myapp.git/

# Fix permissions
chmod 755 /projects/myapp.git/

# Or use sudo (not recommended)
sudo gw add feature-y
```

### Git Administrative File Repair

**Problem:**

```bash
$ git status
error: bad signature 0x00000000
fatal: index file corrupt
```

**Solution:**

```bash
# In affected worktree
rm .git/index
git reset

# Or use repair command
gw repair

# Rebuild index
git add .
```

### Branch Checkout Conflicts

**Problem:**

```bash
$ gw add feature-x
fatal: 'feature-x' is already checked out at '/projects/myapp.git/other-worktree'
```

**Solution:**

```bash
# Option 1: Use the existing worktree
gw cd feature-x  # Goes to /projects/myapp.git/other-worktree

# Option 2: Create new branch
gw add feature-x-new -b feature-x-new feature-x

# Option 3: Force checkout (only if you know what you're doing)
gw add feature-x-copy -b feature-x-copy --force
```

### Cleaning Up After Errors

**Problem:** Failed worktree creation left partial state

**Solution:**

```bash
# Remove partial worktree
rm -rf /projects/myapp.git/failed-worktree

# Clean up Git references
gw prune

# Verify clean state
gw list
```

---

## Summary

You now understand:

- ✅ Git worktree fundamentals and when to use them
- ✅ Creating and managing worktrees with `gw add`
- ✅ Quick navigation with `gw cd`
- ✅ Common workflow patterns for features, hotfixes, and reviews
- ✅ Maintenance and cleanup strategies
- ✅ Troubleshooting common issues

### Next Steps

1. Try creating your first worktree with `gw add`
2. Set up auto-copy configuration (see [config-management skill](../config-management/))
3. Explore advanced parallel workflows (see [multi-worktree-dev skill](../multi-worktree-dev/))

### Additional Resources

- [Getting Started Example](./examples/getting-started.md)
- [Parallel Development Example](./examples/parallel-development.md)
- [Troubleshooting Guide](./examples/troubleshooting-worktrees.md)
- [gw CLI Documentation](../../packages/gw-tool/README.md)

---

*Part of the [gw-tools skills collection](../README.md)*
