---
name: worktree
description: Manage git worktrees for parallel development. Use to work on multiple branches simultaneously without stashing or switching contexts.
---

# Git Worktree Manager

Work on multiple branches simultaneously using git worktrees.

## Prerequisites

```bash
# Git 2.5+ (worktrees built-in)
git --version
```

## CLI Reference

### List Worktrees

```bash
# List all worktrees
git worktree list

# Porcelain format (machine-readable)
git worktree list --porcelain
```

### Create Worktree

```bash
# Create from existing branch
git worktree add ../feature-branch feature-branch

# Create new branch
git worktree add -b new-feature ../new-feature main

# Specific path
git worktree add /path/to/worktree branch-name

# Detached HEAD at commit
git worktree add --detach ../temp abc123
```

### Remove Worktree

```bash
# Remove worktree
git worktree remove ../feature-branch

# Force remove (uncommitted changes)
git worktree remove --force ../feature-branch

# Prune stale worktrees
git worktree prune
```

### Worktree Operations

```bash
# Move worktree
git worktree move ../old-path ../new-path

# Lock worktree (prevent pruning)
git worktree lock ../feature-branch
git worktree lock --reason "long-running task" ../feature-branch

# Unlock
git worktree unlock ../feature-branch
```

## Workflow Patterns

### Parallel Feature Development

```bash
# Main repo working on feature-a
cd ~/repos/myproject
git checkout feature-a

# Create worktree for feature-b
git worktree add ../myproject-feature-b feature-b

# Now you have two checkouts:
# ~/repos/myproject (feature-a)
# ~/repos/myproject-feature-b (feature-b)
```

### Quick Bug Fix

```bash
# Currently working on feature
cd ~/repos/myproject

# Create worktree for hotfix
git worktree add ../myproject-hotfix -b hotfix/urgent main

# Fix bug in worktree
cd ../myproject-hotfix
# make changes
git commit -am "fix: urgent bug"
git push origin hotfix/urgent

# Create PR
gh pr create --base main --title "Hotfix: urgent bug"

# Clean up
cd ../myproject
git worktree remove ../myproject-hotfix
```

### Review PR

```bash
# Create worktree for PR branch
git fetch origin pull/123/head:pr-123
git worktree add ../myproject-pr-123 pr-123

# Review and test
cd ../myproject-pr-123
npm install
npm test

# Clean up after review
cd ../myproject
git worktree remove ../myproject-pr-123
git branch -D pr-123
```

### Long-Running Comparison

```bash
# Worktree for baseline
git worktree add ../myproject-baseline main

# Run tests on both
cd ~/repos/myproject
npm test > /tmp/feature-tests.log

cd ../myproject-baseline
npm test > /tmp/baseline-tests.log

diff /tmp/baseline-tests.log /tmp/feature-tests.log
```

## Directory Structure

Recommended layout:

```
~/repos/
├── myproject/           # Main worktree (main branch)
├── myproject-feature-a/ # Feature worktree
├── myproject-feature-b/ # Another feature
└── myproject-hotfix/    # Hotfix worktree
```

Or nested:

```
~/repos/myproject/
├── main/      # Main worktree
├── features/
│   ├── auth/  # Feature worktree
│   └── ui/    # Feature worktree
└── hotfix/    # Hotfix worktree
```

## Beads with Worktrees

When using beads (task tracker) with worktrees, disable the daemon:

```bash
# In shell config
export BEADS_NO_DAEMON=1

# Or per-command
bd --no-daemon ready
bd --no-daemon create "task"
```

## Common Issues

### Branch Already Checked Out

```bash
# Error: 'branch' is already checked out at '/path'
# Solution: Use different branch or remove other worktree
git worktree remove /path/to/other
```

### Stale Worktree References

```bash
# Clean up deleted worktrees
git worktree prune

# Verbose output
git worktree prune --verbose
```

### Shared Resources

Each worktree shares:
- `.git` directory (refs, objects)
- Remote configurations
- Hooks

Each worktree has separate:
- Working directory
- Index (staging area)
- HEAD

## Scripts

### Create Feature Worktree
```bash
#!/bin/bash
FEATURE=$1
BASE=${2:-main}

git worktree add -b feature/$FEATURE ../${PWD##*/}-$FEATURE $BASE
cd ../${PWD##*/}-$FEATURE
npm install
echo "Worktree created at $(pwd)"
```

### Cleanup Old Worktrees
```bash
#!/bin/bash
# Remove worktrees for merged branches

for wt in $(git worktree list --porcelain | grep "^worktree" | cut -d' ' -f2); do
  branch=$(git -C "$wt" branch --show-current)
  if git branch --merged main | grep -q "$branch"; then
    echo "Removing merged worktree: $wt ($branch)"
    git worktree remove "$wt"
  fi
done
git worktree prune
```

## Best Practices

1. **Use descriptive paths** - Include branch name in directory
2. **Install dependencies** - Run npm/yarn install in each worktree
3. **Prune regularly** - Clean up stale references
4. **Don't nest worktrees** - Keep them sibling directories
5. **Lock long-running** - Prevent accidental pruning
6. **Separate IDE workspace** - Each worktree gets own IDE window
7. **Disable beads daemon** - Prevent database conflicts
