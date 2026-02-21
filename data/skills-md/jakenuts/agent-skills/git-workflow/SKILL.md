---
name: git-workflow
description: Automated git workflow helpers for common development tasks like creating feature branches, cleaning up merged branches, and interactive rebasing. Use when the user mentions git branching, branch cleanup, feature workflow, or git automation. No prerequisites required - uses native git commands.
compatibility: Requires git installed (available in most development environments)
metadata:
  requires-setup: false
---

# Git Workflow Automation

Automated helpers for common git workflows and branch management tasks.

## No Setup Required

This skill uses native git commands and bash scripts - no additional tools or SDKs needed. Works immediately in any environment with git installed.

## Quick Start

### Create Feature Branch

Create a new feature branch following naming conventions:

```bash
# Interactive: prompts for feature name
cd /path/to/repo
bash ~/.claude/skills/git-workflow/scripts/create-feature-branch.sh

# Non-interactive: specify feature name
bash ~/.claude/skills/git-workflow/scripts/create-feature-branch.sh "add-user-auth"
# Creates: feature/add-user-auth
```

### Clean Up Merged Branches

Remove local branches that have been merged to main/master:

```bash
cd /path/to/repo

# Preview what would be deleted (dry run)
bash ~/.claude/skills/git-workflow/scripts/cleanup-merged-branches.sh --dry-run

# Actually delete merged branches
bash ~/.claude/skills/git-workflow/scripts/cleanup-merged-branches.sh

# Force cleanup (skip confirmations)
bash ~/.claude/skills/git-workflow/scripts/cleanup-merged-branches.sh --force
```

### Interactive Rebase Helper

Simplified interactive rebase with common options:

```bash
cd /path/to/repo

# Rebase last 3 commits
bash ~/.claude/skills/git-workflow/scripts/interactive-rebase.sh 3

# Rebase since a specific commit
bash ~/.claude/skills/git-workflow/scripts/interactive-rebase.sh abc123

# Rebase onto main
bash ~/.claude/skills/git-workflow/scripts/interactive-rebase.sh main
```

## Available Scripts

All scripts are located in the skill's `scripts/` directory and can be run with bash.

| Script | Purpose | Usage |
|--------|---------|-------|
| `create-feature-branch.sh` | Create feature branches with naming conventions | `bash script.sh [feature-name]` |
| `cleanup-merged-branches.sh` | Clean up merged branches | `bash script.sh [--dry-run\|--force]` |
| `interactive-rebase.sh` | Interactive rebase helper | `bash script.sh <commit-count\|ref>` |

## Workflow Examples

### Starting a New Feature

```bash
# 1. Ensure main is up to date
git checkout main
git pull origin main

# 2. Create feature branch
bash ~/.claude/skills/git-workflow/scripts/create-feature-branch.sh "user-authentication"

# 3. Work on feature...
# (make commits)

# 4. Push when ready
git push -u origin feature/user-authentication
```

### Cleaning Up After PR Merge

```bash
# 1. Update main branch
git checkout main
git pull origin main

# 2. Preview what will be deleted
bash ~/.claude/skills/git-workflow/scripts/cleanup-merged-branches.sh --dry-run

# 3. Clean up merged branches
bash ~/.claude/skills/git-workflow/scripts/cleanup-merged-branches.sh
```

### Squashing Commits Before PR

```bash
# Squash last 5 commits into one
bash ~/.claude/skills/git-workflow/scripts/interactive-rebase.sh 5

# In the editor that opens:
# - Change 'pick' to 'squash' (or 's') for commits 2-5
# - Keep first commit as 'pick'
# - Save and close

# Then edit the combined commit message
```

## Safety Features

All scripts include:
- **Dry run mode** - Preview changes before applying
- **Confirmation prompts** - Ask before destructive operations
- **Current branch protection** - Won't delete the branch you're on
- **Main/master protection** - Won't delete main branches
- **Uncommitted changes check** - Warns if working directory is dirty

## Prerequisites

- **git** - Installed and configured (available in most dev environments)
- **bash** - Standard shell (available on Linux, macOS, and Git Bash on Windows)

No additional tools, SDKs, or environment variables required.
