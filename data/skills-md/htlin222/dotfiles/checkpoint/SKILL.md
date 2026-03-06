---
name: checkpoint
description: Git checkpoint management - create, list, restore checkpoints. Invoke when starting risky changes or needing safe recovery points.
allowed-tools: Bash, Read, Write, Glob
---

# Git checkpoint system

Manage git checkpoints (stashes) for safe code exploration and recovery.

## When to invoke

- Before making risky changes or refactoring
- When you want a quick save point without committing
- To restore previous state after experiments fail
- To maintain multiple work-in-progress states

## Usage

```
/checkpoint create [name]     # Create a named checkpoint
/checkpoint list              # List checkpoints
/checkpoint restore [name]    # Restore a specific checkpoint
/checkpoint pop               # Restore the most recent checkpoint
/checkpoint clear             # Remove checkpoints
```

## Instructions

### Create checkpoint

1. Check if in a git repository
2. Check for uncommitted changes
3. Create a git stash with the name: `claude-checkpoint_YYYYMMDD_HHMMSS: [name]`
4. Confirm the checkpoint creation

### List checkpoints

1. Run `git stash list`
2. Filter stashes that start with `claude-checkpoint`
3. Display in a formatted table:
   - Index (stash@{N})
   - Timestamp
   - Description
   - Number of files changed

### Restore checkpoint

1. Find the stash matching the given name or index
2. Apply the stash with `git stash apply stash@{N}`
3. Do NOT drop the stash (keep it for safety)
4. Report restoration details

### Pop checkpoint

1. Find the recent `claude-checkpoint` stash
2. Apply it with `git stash pop stash@{N}`
3. Report restoration details

### Clear checkpoints

1. List `claude-checkpoint` stashes
2. Ask for confirmation before proceeding
3. Drop each matching stash
4. Report removal count

## Examples

```bash
# Create checkpoint before risky changes
/checkpoint create "before refactoring auth module"

# List checkpoints
/checkpoint list

# Restore if something went wrong
/checkpoint restore "before refactoring auth module"

# Quick restore of the recent one
/checkpoint pop

# Clean up old checkpoints
/checkpoint clear
```

## Notes

- Checkpoints rely on git stash under the hood
- Include untracked files in checkpoints
- Checkpoints persist across sessions
- Apply descriptive names for identification
