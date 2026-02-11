---
name: '@gw-git-worktree-workflows'
description: Master Git worktrees and gw-tools workflows for parallel development. Use this skill when creating worktrees, managing multiple branches simultaneously, navigating between worktrees, troubleshooting worktree issues, or setting up feature branch workflows. Triggers on tasks involving git worktree commands, branch isolation, parallel development, or gw CLI usage.
license: MIT
metadata:
  author: mthines
  version: '1.0.0'
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

| Approach             | Pros                                               | Cons                                                  |
| -------------------- | -------------------------------------------------- | ----------------------------------------------------- |
| **Branch Switching** | Single directory, less disk space                  | Interrupts work, requires stashing, IDE reindexes     |
| **Worktrees**        | Parallel work, no interruption, shared Git history | Slightly more disk space for working files            |
| **Cloning**          | Complete isolation                                 | Huge disk space, separate Git history, harder to sync |

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

### Getting Started: Clone and Initialize

If you're setting up a new repository with gw, you can clone and initialize in one step:

```bash
# Clone a repository and automatically set up gw
$ gw init git@github.com:user/repo.git

Cloning repository from git@github.com:user/repo.git...
✓ Repository cloned to repo

Setting up gw_root branch...
✓ Created gw_root branch

Initializing gw configuration...
✓ Configuration created

Creating main worktree...
✓ Created main worktree

✓ Repository initialized successfully!
```

This automatically:

1. Clones the repository with `--no-checkout`
2. Creates a `gw_root` branch for the bare repository
3. Auto-detects the default branch (main, master, etc.)
4. Creates the gw configuration at `.gw/config.json`
5. Creates your first worktree for the default branch
6. Names the repository directory with `.git` suffix (bare repo convention)
7. Navigates you to the repository directory (with shell integration)

**Clone with configuration:**

```bash
# Clone with auto-copy files configured
$ gw init git@github.com:user/repo.git \
          --auto-copy-files .env,secrets/ \
          --post-add "pnpm install"

# Clone into a custom directory
$ gw init git@github.com:user/repo.git my-project

# Clone and configure interactively
$ gw init https://github.com/user/repo.git --interactive
```

**For existing repositories:**

If you already have a cloned repository, initialize gw from within it:

```bash
$ cd ~/projects/myapp
$ gw init

Auto-detected git root: /projects/myapp.git
✓ Configuration created successfully
```

### The `gw add` Command

The `gw add` command is an enhanced version of `git worktree add` with automatic file copying and navigation:

```bash
# Basic usage - create worktree for existing branch
# Automatically navigates to the new worktree
gw add feature-auth

# Create worktree without automatic navigation
gw add feature-auth --no-cd

# Create worktree with new branch
gw add feature-payments -b feature-payments

# Create from a different branch instead of defaultBranch
gw add feature-payment-v2 --from develop

# Create child feature branch from parent feature branch
gw add feature-auth-social --from feature-auth

# Create from specific start point
gw add hotfix-security -b hotfix-security main

# Force creation (even if branch already checked out elsewhere)
gw add feature-test --force
```

### Remote Fetch Behavior

When creating a new branch, `gw add` follows a **remote-first approach** to ensure your work starts from the latest code:

**What's happening under the hood:**

```bash
$ gw add feat/new-feature

Branch feat/new-feature doesn't exist, creating from main...
Fetching latest from remote to ensure fresh start point...
✓ Fetched successfully from remote
Creating from origin/main (latest from remote)

Creating worktree: feat/new-feature
```

The command:

1. Detects that `feat/new-feature` doesn't exist
2. Fetches the latest version of `main` from the remote (`origin/main`)
3. Creates your new branch from the fresh remote ref
4. Sets up tracking to `origin/feat/new-feature` for easy pushing

**Why this matters:**

- **Prevents conflicts**: Your branch starts from the latest remote code, not an outdated local branch
- **Ensures fresh code**: You're building on the most recent changes from your team
- **Reduces merge pain**: Fewer surprises when you eventually merge back to main

**Offline/fallback behavior:**

When remote fetch fails (network issues, offline work, no remote configured), behavior depends on the context:

```bash
# Without --from (default branch): Warns but allows local fallback
$ gw add feat/offline

Branch feat/offline doesn't exist, creating from main...
Fetching latest from remote to ensure fresh start point...

⚠ WARNING Could not fetch from remote

Falling back to local branch. The start point may not be up-to-date with remote.
This is acceptable for offline development or when remote is unavailable.

Creating from main (local branch)

Creating worktree: feat/offline
```

```bash
# With --from: Requires successful fetch, exits on failure
$ gw add feat/explicit --from develop

Branch feat/explicit doesn't exist, creating from develop...
Fetching latest from remote to ensure fresh start point...

ERROR Could not fetch from remote

Cannot create branch from develop because the remote fetch failed.
This would use a potentially outdated local branch.

Possible causes:
  • Network connectivity issues
  • Branch develop doesn't exist on remote
  • Authentication issues

Options:
  1. Check your network connection and try again
  2. Verify the branch exists: git ls-remote origin develop
  3. Use a different source branch: gw add feat/explicit --from <branch>
  4. Create without --from to use default branch: gw add feat/explicit
```

**Key difference: `--from` requires freshness**

- **Without `--from`**: Uses default branch with fallback to local (offline support)
- **With `--from`**: Requires successful remote fetch (ensures explicit source is fresh)

### Navigating to Existing Worktrees

If you try to add a worktree that already exists, `gw add` will prompt you to navigate to it:

```bash
$ gw add feature-auth

ℹ Worktree feature-auth already exists at:
  /projects/myapp.git/feature-auth

Navigate to it? [Y/n]:
# Press Enter to navigate (default: Yes), or 'n' to cancel
```

This is convenient when you're not sure if you've already created a worktree for a branch. Requires shell integration to be installed (`gw install-shell`).

### Auto-Copying Files

When creating worktrees with `gw add`, files configured in `.gw/config.json` are automatically copied:

```json
{
  "root": "/Users/you/projects/myapp.git",
  "defaultBranch": "main",
  "autoCopyFiles": [".env", ".env.local", "secrets/", "components/ui/.vercel/"]
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
✓ Branch 'feature-new-dashboard' set up to track 'origin/feature-new-dashboard'
✓ Worktree created: /projects/myapp.git/feature-new-dashboard

Copying files from main...
✓ Copied: .env
✓ Copied: .env.local
✓ Copied: secrets/api-keys.json
✓ Copied: components/ui/.vercel/

Done! Navigate with: gw cd feature-new-dashboard
```

**Note:** The branch is configured to track its own remote branch (`origin/feature-new-dashboard`), not `origin/main`. This means `git push` will push to the correct branch without needing `-u origin <branch>`.

**Network Failure Handling:**

When creating worktrees, `gw add` has different behavior depending on whether you explicitly specify a source branch:

- **With `--from <branch>`**: Requires a successful fetch from the remote. If the fetch fails (network issues, branch doesn't exist on remote, authentication problems), the command exits with detailed error messages and suggestions. This ensures you're working with the latest code when you explicitly specify a source.
- **Without `--from` (default branch)**: Warns about fetch failures but allows creation using the local branch. This provides a fallback for offline work or when no remote is configured.

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
# Creates branch from origin/main, tracking its own remote branch
gw add feature-x

# Shows branch relationship
$ git status
On branch feature-x
Your branch is up to date with 'origin/feature-x'.

# Push works without specifying remote/branch
git push  # Pushes to origin/feature-x
```

**Note:** When `gw add` creates a new branch, it automatically configures upstream tracking to `origin/<branch-name>`, not to the branch it was created from. This ensures `git push` works correctly.

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

### Using `gw checkout` (or `gw co`) for Smart Branch Checkout

The `gw checkout` command is a smart wrapper around `git checkout` that understands worktrees:

```bash
# Checkout a branch - navigates if already checked out elsewhere
gw checkout main
# or use the alias
gw co main

# If branch is checked out in another worktree:
# Output: Branch main is checked out in another worktree:
#   /projects/myapp.git/main
# Navigating there...

# If branch exists on remote but not locally, prompts to create worktree:
gw checkout feature-new
# Output: Branch feature-new exists on remote but not locally.
# Create a new worktree for it? [Y/n]:
```

**When to use `gw checkout` vs `gw cd`:**

- Use `gw checkout <branch>` when you think of branches (like `git checkout`)
- Use `gw cd <worktree>` when you think of directory names
- Both support partial matching and navigate to existing worktrees
- `gw checkout` additionally handles remote branches and provides worktree-aware error messages

**Why not just use `git checkout`?**

With worktrees, `git checkout main` will fail if main is checked out in another worktree:

```bash
$ git checkout main
fatal: 'main' is already checked out at '/projects/myapp.git/main'
```

With `gw checkout`, this just takes you there instead of showing an error. It reduces friction when transitioning from traditional Git workflows to worktree-based workflows.

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

**Shell integration features:**

- **Real-time streaming output** - Commands like `gw add` now stream output as it's generated (no buffering)
- **Auto-navigation** - Automatically navigate to new worktrees after `gw add` completes
- **Smart cleanup** - Auto-navigate to repo root when removing the current worktree with `gw remove`

**For development aliases:**

If you're developing gw-tools locally, you can install shell integration for a development command:

```bash
# Install for development (replace with your actual path)
gw install-shell --name gw-dev \
  --command "deno run --allow-all ~/path/to/gw-tools/packages/gw-tool/src/main.ts"

# Then use it with full integration
gw-dev add feat-branch  # Output streams in real-time!
gw-dev cd feat-branch   # Navigation works!
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

# Update with latest changes from main (uses configured strategy)
gw update

# Or update from a different branch
gw update --from develop

# Force merge strategy (overrides config)
gw update --merge

# Force rebase strategy (overrides config)
gw update --rebase

# Preview what would happen
gw update --dry-run
```

**Why use `gw update` instead of `git pull`?**

When working in a worktree, you cannot simply checkout main to pull the latest changes because main is typically checked out in another worktree. The `gw update` command solves this by:

1. Fetching the latest version of main (or specified branch) from remote
2. Updating your current branch using either merge or rebase strategy
3. Handling conflicts and providing clear guidance

**Update strategies:**

- **Merge** (default): Creates merge commits, preserves complete history
- **Rebase**: Replays commits for linear history, cleaner but rewrites history

Configure default strategy in `.gw/config.json` or override per-command with `--merge`/`--rebase` flags.

**Safety features:**

- Blocks if you have uncommitted changes (use `--force` to override)
- Blocks if you're in a detached HEAD state
- Provides clear guidance when merge/rebase conflicts occur

**Network Failure Handling:**

Similar to `gw add`, the `gw update` command has different behavior for network failures:

- **With `--from <branch>`**: Requires a successful fetch from the remote. If the fetch fails, the command exits with detailed error messages and troubleshooting steps. This prevents updating from a potentially outdated local branch when you've explicitly specified a source.
- **Without `--from` (default branch)**: Warns about fetch failures but allows the update using the local branch. This provides a fallback for offline work.

**Example workflow:**

```bash
# Start working on feature
gw cd feature-dashboard

# Work for a few days...
git add .
git commit -m "feat: add dashboard widgets"

# Meanwhile, main has new changes
# Update your feature branch with latest main
gw update

# If there's a conflict, you'll get clear guidance:
# For merge conflicts:
#   1. Edit conflicted files
#   2. git add <resolved-files>
#   3. git commit
# For rebase conflicts:
#   1. Edit conflicted files
#   2. git add <resolved-files>
#   3. git rebase --continue

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

### Hierarchical Feature Development

**Scenario:** Building related features where one depends on another

Sometimes you need to create a child feature branch that builds on top of a parent feature branch that hasn't been merged yet. The `--from` option makes this workflow seamless:

```bash
# Create parent feature from main
gw add feature-auth

# Work on authentication foundation
gw cd feature-auth
# ... implement basic auth ...
git add .
git commit -m "feat: add basic authentication"

# Create child feature from the auth branch (not main)
gw add feature-auth-social --from feature-auth

# Navigate to child feature
gw cd feature-auth-social

# This branch now has all the auth foundation from feature-auth
# Build social login on top of basic auth
# ... implement OAuth integration ...
git add .
git commit -m "feat: add social login with OAuth"
```

**Benefits:**

- Child feature automatically includes all parent feature commits
- Can develop related features in parallel without waiting for merges
- Tracks `origin/feature-auth-social` for push (not `origin/feature-auth`)
- Clear dependency relationship between features
- Ensures latest code from the source branch by requiring successful remote fetch

**Common patterns:**

```bash
# Experimental variations of a feature
gw add feature-dashboard-v2 --from feature-dashboard

# Staged rollouts with different implementations
gw add feature-api-graphql --from feature-api
gw add feature-api-rest --from feature-api

# Environment-specific feature branches
gw add feature-payment-staging --from develop
gw add feature-payment-prod --from main
```

**When to merge:**

1. Merge parent feature first: `feature-auth` → `main`
2. Rebase or merge child onto updated main
3. Merge child feature: `feature-auth-social` → `main`

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

**Protected branches** (cannot be removed):

- Default branch (typically `main`, configured in `.gw/config.json`)
- `gw_root` branch (bare repository root)
- Bare repository worktree

**What happens:**

- Working directory is deleted
- Worktree reference removed from Git
- Branch remains in repository (can still be checked out elsewhere)

### Cleaning Up Stale Worktrees

**Remove safe worktrees:**

```bash
# Preview all safe worktrees (default behavior)
gw clean --dry-run

# Remove all safe worktrees regardless of age
gw clean

# Only remove worktrees older than configured threshold
gw clean --use-autoclean-threshold

# Preview old worktrees with threshold check
gw clean --use-autoclean-threshold --dry-run

# Force removal (skips safety checks - dangerous!)
gw clean --force
```

**How it works:**

- **Default mode:** Finds ALL safe worktrees (no age check)
- **With `--use-autoclean-threshold`:** Only finds worktrees older than configured threshold (default: 7 days)
- By default, only removes worktrees with:
  - NO uncommitted changes
  - NO unpushed commits
- Always prompts for confirmation before deletion
- **Protected worktrees** (never removed):
  - Bare repository worktree
  - Default branch (configured in `.gw/config.json`, typically `main`)
  - `gw_root` branch (bare repository root)

**Cleanup strategies:**

| Command                              | When to Use                                       |
| ------------------------------------ | ------------------------------------------------- |
| `gw clean`                           | Clean up all finished work regardless of age      |
| `gw clean --use-autoclean-threshold` | Regular maintenance (only old worktrees)          |
| `gw prune --clean`                   | Aggressive cleanup with default branch protection |

**Configure the threshold:**

```bash
# Set to 14 days during initialization
gw init --clean-threshold 14

# Or manually edit .gw/config.json
{
  "cleanThreshold": 14
}
```

**Example workflow (default mode):**

```bash
# Check what would be cleaned (all safe worktrees)
$ gw clean --dry-run
INFO: Checking for safe worktrees to clean...

Worktrees to remove:
  ✗ completed-feature-1 (2 days old)
  ✗ completed-feature-2 (14 days old)

Skipped worktrees:
  ⚠ active-feature - has uncommitted changes

# Review and clean
$ gw clean
Remove 2 worktree(s)?
Type 'yes' to confirm: yes

Removing completed-feature-1...
  ✓ Removed

Removing completed-feature-2...
  ✓ Removed

SUCCESS: Removed 2 worktree(s)
```

**Example workflow (threshold mode):**

```bash
# Check what would be cleaned (only old worktrees)
$ gw clean --use-autoclean-threshold --dry-run
INFO: Checking for worktrees older than 7 days...

Worktrees to remove:
  ✗ old-feature-1 (14 days old)
  ✗ old-feature-2 (10 days old)

Skipped worktrees:
  ⚠ recent-feature - has uncommitted changes

# Review and clean
$ gw clean --use-autoclean-threshold
Remove 2 worktree(s)?
Type 'yes' to confirm: yes

SUCCESS: Removed 2 worktree(s)
```

### Cleanup Strategies: `gw clean` vs `gw prune --clean`

The gw tool provides two complementary cleanup commands for different scenarios:

**Age-based Cleanup: `gw clean`**

- Removes worktrees **older than configured threshold** (default: 7 days)
- Good for regular maintenance
- Respects safety checks (no uncommitted changes, no unpushed commits)
- Configurable via `.gw/config.json`

```bash
# Regular maintenance (weekly)
gw clean --dry-run  # Preview
gw clean            # Remove old worktrees
```

**Complete Cleanup: `gw prune --clean`**

- Removes **ALL clean worktrees** (regardless of age)
- First runs `git worktree prune` to clean up administrative data
- Protects default branch and current worktree
- Good for aggressive cleanup before archiving or when disk space is critical

```bash
# Aggressive cleanup (before vacation, archiving)
gw prune --clean --dry-run  # Preview
gw prune --clean            # Remove all clean worktrees
```

**Comparison:**
| Feature | `gw clean` | `gw prune --clean` |
|---------|-----------|-------------------|
| Age-based | Yes (configurable) | No (removes all clean) |
| Safety checks | Yes | Yes |
| Protects default branch | No | Yes |
| Runs `git worktree prune` | No | Yes |
| Use case | Regular maintenance | Aggressive cleanup |

**When to use which:**

Use `gw clean`:

- Weekly/monthly maintenance to remove stale worktrees
- When you want to keep recent worktrees but clean up old ones
- As part of automated cleanup routines

Use `gw prune --clean`:

- Before archiving a project or taking a break
- When you need to free up disk space quickly
- To reset to a minimal worktree setup (just main branch + current work)
- After completing a major milestone or release

**Example workflow:**

```bash
# Regular maintenance (weekly)
gw clean --dry-run  # Preview old worktrees
gw clean            # Remove if ok

# Major cleanup (quarterly or before breaks)
gw prune --clean --dry-run  # Preview all clean worktrees
gw prune --clean            # Remove all clean worktrees
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

### Git Ref Conflicts (Branch Name Hierarchy)

**Problem:**

```bash
$ gw add test
Cannot create branch test because it conflicts with existing branch test/foo

Git doesn't allow both refs/heads/test and refs/heads/test/foo
```

Git prevents creating branches with hierarchical naming conflicts (e.g., both `test` and `test/foo`) because they would require the same path to be both a file and a directory in `.git/refs/heads/`.

**Solution:**

```bash
# Option 1: Use a different name
gw add test-new -b test-new

# Option 2: Delete the conflicting branch
git branch -d test/foo
gw add test

# Option 3: Use the existing conflicting branch
gw add test/foo
```

**Prevention:** Use consistent naming conventions. Good: `feature/auth`, `feature/checkout`. Bad: mixing `feature` and `feature/new`.

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

### Shell Integration Issues

**Problem:** `gw cd` doesn't navigate or shows parse errors

```bash
# Zsh example error:
/Users/name/.gw/shell/integration-gw-dev.zsh:2: defining function based on alias `gw-dev'
/Users/name/.gw/shell/integration-gw-dev.zsh:2: parse error near `()'
```

**Solution:**

```bash
# For regular gw installation
gw install-shell

# For development aliases, remove any existing alias first
# Then install with --command flag
gw install-shell --name gw-dev \
  --command "deno run --allow-all ~/path/to/gw-tools/packages/gw-tool/src/main.ts"

# Reload your shell
source ~/.zshrc  # or ~/.bashrc
```

**Common causes:**

- Conflicting alias and function with same name (remove alias from .zshrc)
- Old integration script format (reinstall fixes this)
- Shell not supported (only zsh, bash, fish)

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
3. Explore autonomous workflows (see [autonomous-workflow skill](../autonomous-workflow/))

### Additional Resources

- [Getting Started Example](./examples/getting-started.md)
- [Parallel Development Example](./examples/parallel-development.md)
- [Troubleshooting Guide](./examples/troubleshooting-worktrees.md)
- [gw CLI Documentation](../../packages/gw-tool/README.md)

---

_Part of the [gw-tools skills collection](../README.md)_
