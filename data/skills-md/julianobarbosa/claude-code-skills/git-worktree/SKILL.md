---
name: git-worktree
description: Git worktree management with tmux and iTerm2 integration. Use when creating isolated dev environments, managing parallel feature branches, switching contexts without stashing, or running multiple Claude instances. Covers worktree creation, tmux window management, iTerm2 tabs, and cleanup workflows.
---

# Git Worktree Skill

Manage parallel development environments using git worktrees with seamless terminal integration.

## Overview

Git worktrees enable multiple working directories from a single repository:
- Isolated feature development without branch switching
- Run multiple Claude Code instances in parallel
- Context switching without stashing uncommitted changes
- Clean separation of experimental work

## Quick Commands

### wt - Worktree Manager

The `wt` command creates worktrees with automatic terminal integration:

```bash
# Create worktree with tmux window
wt add-new-feature

# This will:
# 1. Create git worktree named 'add-new-feature'
# 2. Create new tmux window in current session
# 3. Rename window to 'add-new-feature'
# 4. Change directory to the worktree
```

## tmux Integration

### Workflow: Create Worktree + tmux Window

```bash
# Function for ~/.zshrc or ~/.bashrc
wt() {
    local name="$1"
    local base_branch="${2:-main}"
    local repo_root=$(git rev-parse --show-toplevel 2>/dev/null)
    local worktree_path="$repo_root/.worktrees/$name"

    # Validate we're in a git repo
    if [[ -z "$repo_root" ]]; then
        echo "Error: Not in a git repository"
        return 1
    fi

    # Create worktree directory
    mkdir -p "$repo_root/.worktrees"

    # Create worktree with new branch
    if git worktree add -b "$name" "$worktree_path" "$base_branch" 2>/dev/null; then
        echo "Created worktree: $worktree_path"
    elif git worktree add "$worktree_path" "$name" 2>/dev/null; then
        echo "Attached to existing branch: $name"
    else
        echo "Error: Failed to create worktree"
        return 1
    fi

    # tmux integration
    if [[ -n "$TMUX" ]]; then
        # Create new window with worktree name
        tmux new-window -n "$name" -c "$worktree_path"
        echo "Created tmux window: $name"
    else
        # Not in tmux, just cd
        cd "$worktree_path"
        echo "Changed to: $worktree_path"
    fi
}

# Remove worktree and tmux window
wt-rm() {
    local name="$1"
    local repo_root=$(git rev-parse --show-toplevel 2>/dev/null)
    local worktree_path="$repo_root/.worktrees/$name"

    # Remove git worktree
    git worktree remove "$worktree_path" --force 2>/dev/null

    # Close tmux window if exists
    if [[ -n "$TMUX" ]]; then
        tmux kill-window -t "$name" 2>/dev/null
    fi

    # Optionally delete branch
    git branch -d "$name" 2>/dev/null

    echo "Removed worktree: $name"
}

# List all worktrees
wt-ls() {
    git worktree list
}
```

### tmux Session Management

```bash
# Create dedicated tmux session per project
wt-session() {
    local name="$1"
    local repo_root=$(git rev-parse --show-toplevel 2>/dev/null)
    local worktree_path="$repo_root/.worktrees/$name"

    # Create worktree first
    wt "$name"

    # Create new tmux session (or attach if exists)
    if tmux has-session -t "$name" 2>/dev/null; then
        tmux attach-session -t "$name"
    else
        tmux new-session -d -s "$name" -c "$worktree_path"
        tmux attach-session -t "$name"
    fi
}
```

## iTerm2 Integration

### AppleScript for iTerm2 Tabs

```bash
# Function for ~/.zshrc
wt-iterm() {
    local name="$1"
    local base_branch="${2:-main}"
    local repo_root=$(git rev-parse --show-toplevel 2>/dev/null)
    local worktree_path="$repo_root/.worktrees/$name"

    # Create worktree
    mkdir -p "$repo_root/.worktrees"
    git worktree add -b "$name" "$worktree_path" "$base_branch" 2>/dev/null || \
    git worktree add "$worktree_path" "$name" 2>/dev/null

    # Open in new iTerm2 tab
    osascript <<EOF
tell application "iTerm2"
    tell current window
        create tab with default profile
        tell current session
            write text "cd '$worktree_path' && clear"
        end tell
    end tell
end tell
EOF

    echo "Created worktree with iTerm2 tab: $name"
}

# Open worktree in new iTerm2 window
wt-iterm-window() {
    local name="$1"
    local base_branch="${2:-main}"
    local repo_root=$(git rev-parse --show-toplevel 2>/dev/null)
    local worktree_path="$repo_root/.worktrees/$name"

    # Create worktree
    mkdir -p "$repo_root/.worktrees"
    git worktree add -b "$name" "$worktree_path" "$base_branch" 2>/dev/null || \
    git worktree add "$worktree_path" "$name" 2>/dev/null

    # Open in new iTerm2 window
    osascript <<EOF
tell application "iTerm2"
    create window with default profile
    tell current session of current window
        write text "cd '$worktree_path' && clear"
    end tell
end tell
EOF

    echo "Created worktree with iTerm2 window: $name"
}
```

### iTerm2 Profile Integration

Create a dedicated iTerm2 profile for worktrees:

```json
{
  "Name": "Worktree",
  "Badge Text": "WT: \\(session.name)",
  "Working Directory": "$HOME/.worktrees",
  "Custom Directory": "Yes"
}
```

## Configuration

### Environment Variables

```bash
# Add to ~/.zshrc or ~/.bashrc

# Preferred terminal for worktree operations (auto-detected if not set)
export WORKTREE_TERMINAL="tmux"  # or "iterm2" or "auto"

# Auto-install dependencies after creating worktree
export WORKTREE_AUTO_INSTALL=true
```

### Worktree Location

Worktrees are stored **inside the project directory**:

```
~/Repos/github/my-project/
├── .worktrees/
│   ├── feature-auth/      # worktree for feature-auth branch
│   ├── bugfix-login/      # worktree for bugfix-login branch
│   └── add-new-skill/     # worktree for add-new-skill branch
├── src/
├── package.json
└── ...
```

### Shell Configuration

Functions are defined in `~/.zsh/functions.zsh` (already loaded by your zshrc):

```zsh
# Functions location: ~/.zsh/functions.zsh

# Aliases
alias wt='wt'
alias wtl='wt-ls'
alias wtr='wt-rm'
alias wts='wt-session'

# Completion for wt commands
_wt_completion() {
    local branches=$(git branch --format='%(refname:short)' 2>/dev/null)
    local worktrees=$(git worktree list --porcelain 2>/dev/null | grep '^worktree' | cut -d' ' -f2 | xargs -I{} basename {})
    _alternative \
        "branches:branch:($branches)" \
        "worktrees:worktree:($worktrees)"
}
compdef _wt_completion wt wt-rm
```

## Git Worktree Commands Reference

### Creating Worktrees

```bash
# Create worktree with new branch from current HEAD
git worktree add ../feature-x -b feature-x

# Create worktree from specific branch
git worktree add ../hotfix hotfix-branch

# Create worktree from remote branch
git worktree add ../upstream upstream/main

# Create worktree at specific commit
git worktree add ../review abc123
```

### Managing Worktrees

```bash
# List all worktrees
git worktree list

# Show worktree details (porcelain format)
git worktree list --porcelain

# Lock worktree (prevent pruning)
git worktree lock ../feature-x --reason "WIP"

# Unlock worktree
git worktree unlock ../feature-x

# Remove worktree
git worktree remove ../feature-x

# Force remove (discards changes)
git worktree remove ../feature-x --force

# Prune stale worktrees
git worktree prune
```

### Advanced Operations

```bash
# Move worktree to new location
git worktree move ../old-path ../new-path

# Repair worktree after manual move
git worktree repair ../moved-worktree
```

## Parallel Claude Development

### Running Multiple Instances

```bash
# Create worktrees for parallel development
wt feature-auth
wt feature-api
wt bugfix-login

# Each worktree gets its own:
# - tmux window / iTerm2 tab
# - Git index and working directory
# - Port allocation (if configured)
# - Claude Code instance
```

### Port Management

```bash
# Configure port pools per worktree
export WORKTREE_PORT_BASE=8100
export WORKTREE_PORTS_PER_TREE=2

# Calculate ports for worktree
get_worktree_ports() {
    local index=$(git worktree list | grep -n "$PWD" | cut -d: -f1)
    local base=$((WORKTREE_PORT_BASE + (index - 1) * WORKTREE_PORTS_PER_TREE))
    echo "Dev server: $base, API: $((base + 1))"
}
```

## Cleanup Workflows

### Merge and Cleanup

```bash
# After PR merge, clean up worktree
wt-cleanup() {
    local name="$1"
    local repo_root=$(git rev-parse --show-toplevel 2>/dev/null)
    local worktree_path="$repo_root/.worktrees/$name"

    # Switch to main worktree
    cd "$repo_root"

    # Update main
    git fetch origin
    git pull origin main

    # Remove worktree
    git worktree remove "$worktree_path" --force

    # Delete branch if merged
    if git branch --merged | grep -q "$name"; then
        git branch -d "$name"
        echo "Branch $name was merged and deleted"
    else
        echo "Branch $name not yet merged, kept locally"
    fi

    # Close tmux window
    [[ -n "$TMUX" ]] && tmux kill-window -t "$name" 2>/dev/null
}
```

### Bulk Cleanup

```bash
# Remove all worktrees with merged branches
wt-cleanup-merged() {
    local main_dir=$(git worktree list | head -1 | awk '{print $1}')

    git worktree list | tail -n +2 | while read -r line; do
        local wt_path=$(echo "$line" | awk '{print $1}')
        local wt_branch=$(echo "$line" | awk '{print $3}' | tr -d '[]')

        if git branch --merged main | grep -q "$wt_branch"; then
            echo "Removing merged worktree: $wt_branch"
            git worktree remove "$wt_path" --force
            git branch -d "$wt_branch"
        fi
    done
}
```

## Troubleshooting

### Common Issues

**Worktree already exists:**
```bash
# List existing worktrees
git worktree list

# Remove stale entry
git worktree prune
```

**Branch already checked out:**
```bash
# Error: 'branch' is already checked out at '/path'
# Solution: Use a different branch name or remove existing worktree
git worktree remove /path/to/existing
```

**tmux window naming conflicts:**
```bash
# Rename existing window first
tmux rename-window -t old-name new-name

# Or kill conflicting window
tmux kill-window -t conflicting-name
```

**iTerm2 AppleScript errors:**
```bash
# Ensure iTerm2 is running
open -a iTerm

# Grant automation permissions
# System Preferences > Security & Privacy > Privacy > Automation
```

## References

- [references/tmux-config.md](references/tmux-config.md) - tmux configuration for worktrees
- [references/iterm2-config.md](references/iterm2-config.md) - iTerm2 profile setup
- Shell functions: `~/.zsh/functions.zsh`

## External Links

- Git Worktree Documentation: https://git-scm.com/docs/git-worktree
- tmux Manual: https://man.openbsd.org/tmux
- iTerm2 Documentation: https://iterm2.com/documentation.html
