---
name: beads
description: Manage plan tasks using the beads distributed, git-backed graph issue tracker. Supports creating, updating, closing tasks, managing dependencies, and syncing with git.
---

# Beads Task Management

This skill enables AI-powered task management using the beads (`bd`) distributed issue tracker. Beads provides persistent, structured memory for coding agents with dependency-aware task graphs.

## When to Use This Skill

Use this skill when you need to:
- Create or manage tasks for a development plan
- Track work items with priorities and dependencies
- View ready tasks (tasks with no open blockers)
- Update task status during implementation
- Close completed tasks
- Create epics with sub-tasks
- Sync task state with git

## Prerequisites

- beads CLI (`bd`) must be installed globally
- Project must be initialized with `bd init`
- Git repository (beads uses git as its database backend)

## Core Commands

### Viewing Tasks

```bash
# List tasks ready to work on (no open blockers)
bd ready --json

# List all open tasks
bd list --json

# Show task details
bd show <id> --json

# Search tasks by text
bd search "keyword" --json

# View database status and statistics
bd status --json
```

### Creating Tasks

```bash
# Create a P0 (highest priority) task
bd create "Task title" -p 0 --json

# Create with priority and type
bd create "Bug fix" -p 1 -t bug --json

# Create with detailed description
bd create "Feature name" -p 2 -t feature --json

# Quick capture (returns only ID)
bd q "Quick task" -p 1
```

### Updating Tasks

**IMPORTANT: DO NOT use `bd edit` - it opens an interactive editor which AI agents cannot use.**

```bash
# Update task description
bd update <id> --description "new description"

# Update task title
bd update <id> --title "new title"

# Update design notes
bd update <id> --design "design notes"

# Add notes
bd update <id> --notes "additional notes"

# Set acceptance criteria
bd update <id> --acceptance "acceptance criteria"

# Set status to in progress
bd update <id> --status in_progress
```

### Managing Dependencies

```bash
# Add dependency (child is blocked by parent)
bd dep add <child> <parent>

# Remove dependency
bd dep rm <child> <parent>

# List dependencies for a task
bd dep list <id> --json
```

### Closing Tasks

```bash
# Close a single task
bd close <id> --reason "Completed" --json

# Close multiple tasks
bd close <id1> <id2> --reason "Completed" --json

# Reopen a closed task
bd reopen <id>
```

### Hierarchical Tasks (Epics)

Beads supports hierarchical IDs for epics:
- `bd-a3f8` (Epic)
- `bd-a3f8.1` (Task)
- `bd-a3f8.1.1` (Sub-task)

```bash
# List children of a parent task
bd children <parent-id> --json

# Create epic structure
bd create "Epic: Major feature" -p 1 -t epic --json
```

### Syncing with Git

```bash
# Force immediate sync (export, commit, pull, push)
bd sync

# Check for issues with bd doctor
bd doctor --json
```

## Task Workflow

### Starting a Work Session

1. Check ready tasks:
   ```bash
   bd ready --json
   ```

2. Pick a task and mark in progress:
   ```bash
   bd update <id> --status in_progress
   ```

3. View task details:
   ```bash
   bd show <id> --json
   ```

### During Implementation

1. Create sub-tasks if needed:
   ```bash
   bd create "Sub-task description" -p 1 --json
   bd dep add <child> <parent>
   ```

2. Update notes as you go:
   ```bash
   bd update <id> --notes "Implementation notes..."
   ```

### Completing Work

1. Close finished tasks:
   ```bash
   bd close <id> --reason "Completed implementation" --json
   ```

2. Sync to git:
   ```bash
   bd sync
   ```

### Landing the Plane

When ending a work session, complete ALL steps:

1. **File beads issues for remaining work**:
   ```bash
   bd create "Follow-up task" -p 2 --json
   ```

2. **Close finished work**:
   ```bash
   bd close <finished-ids> --reason "Completed" --json
   ```

3. **Sync and push**:
   ```bash
   bd sync
   git push
   ```

4. **Choose next work**:
   ```bash
   bd ready --json
   ```

## Priority Levels

- **P0**: Critical - must be done immediately
- **P1**: High - should be done soon
- **P2**: Medium - normal priority
- **P3**: Low - nice to have
- **P4**: Backlog - future consideration

## Task Types

Common types: `task`, `bug`, `feature`, `epic`, `chore`, `documentation`

## Best Practices

1. **Use JSON output** - Always use `--json` flag for machine-readable output
2. **Sync frequently** - Run `bd sync` after making changes
3. **Include context** - Add descriptions and notes for future reference
4. **Track dependencies** - Use `bd dep add` to show what blocks what
5. **Close with reasons** - Include why tasks were closed
6. **Commit message convention** - Include issue ID: `git commit -m "Fix bug (bd-abc)"`

## Commit Message Convention

When committing work for an issue, include the issue ID in parentheses:

```bash
git commit -m "Add retry logic for database locks (bd-xyz)"
```

This enables `bd doctor` to detect orphaned issues.

## Common Patterns

### Pattern: Create and Track a Bug Fix
```bash
# Create bug task
bd create "Fix login validation error" -p 1 -t bug --json

# Mark in progress
bd update bd-xxx --status in_progress

# ... do the work ...

# Close when done
bd close bd-xxx --reason "Fixed validation logic" --json
bd sync
```

### Pattern: Create Epic with Sub-tasks
```bash
# Create epic
bd create "Epic: User profile redesign" -p 2 -t epic --json

# Create sub-tasks
bd create "Design new profile layout" -p 2 -t task --json
bd create "Implement profile header" -p 2 -t task --json

# Link dependencies
bd dep add <subtask1> <epic>
bd dep add <subtask2> <epic>
```

### Pattern: Check What's Ready
```bash
# See tasks ready to work on
bd ready --json

# Get count of open issues
bd count --json
```

## Limitations

- `bd edit` opens an interactive editor - use `bd update` with flags instead
- Beads requires git for persistence
- Task IDs are hash-based (e.g., `bd-a1b2`)
