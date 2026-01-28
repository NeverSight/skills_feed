---
name: autonomous-skill
description: 'Use when user wants to execute long-running tasks that require multiple sessions to complete. This skill manages task decomposition, progress tracking, and autonomous execution using Claude Code headless mode with auto-continuation. Trigger phrases: "autonomous", "long-running task", "multi-session", "自主执行", "长时任务", "autonomous skill".'
allowed-tools: Read, Write, Edit, Glob, Grep, Task, Bash(cat:*), Bash(ls:*), Bash(tree:*), Bash(mkdir:*), Bash(touch:*), Bash(pwd:*), Bash(cd:*), Bash(grep:*), Bash(find:*), Bash(head:*), Bash(tail:*), Bash(claude:*)
---

# Autonomous Skill - Long-Running Task Execution

Execute complex, long-running tasks across multiple sessions using a dual-agent pattern (Initializer + Executor) with automatic session continuation.

## Directory Structure

All task data is stored in `.autonomous/<task-name>/` under the project root:

```
project-root/
└── .autonomous/
    ├── build-rest-api/
    │   ├── task_list.md
    │   └── progress.md
    ├── refactor-auth/
    │   ├── task_list.md
    │   └── progress.md
    └── ...
```

This allows multiple autonomous tasks to run in parallel without conflicts.

## Workflow Overview

```
User Request → Generate Task Name → Create .autonomous/<task-name>/ → Execute Sessions
```

## Step 1: Initialize Task Directory

Generate a task name from user's description and create the directory:

```bash
# Generate task name (lowercase, hyphens, max 30 chars)
# Example: "Build a REST API for todo app" → "build-rest-api-todo"
TASK_NAME=$(echo "$USER_TASK" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/--*/-/g' | cut -c1-30 | sed 's/-$//')

# Create task directory
TASK_DIR=".autonomous/$TASK_NAME"
mkdir -p "$TASK_DIR"

echo "Task directory: $TASK_DIR"
```

## Step 2: Analyze Current State

Check if this is a new task or continuation:

```bash
TASK_DIR=".autonomous/$TASK_NAME"

# Look for existing task list
if [ -f "$TASK_DIR/task_list.md" ]; then
  echo "=== CONTINUATION MODE ==="
  echo "Found existing task at: $TASK_DIR"

  # Show progress summary
  TOTAL=$(grep -c '^\- \[' "$TASK_DIR/task_list.md" 2>/dev/null || echo "0")
  DONE=$(grep -c '^\- \[x\]' "$TASK_DIR/task_list.md" 2>/dev/null || echo "0")
  echo "Progress: $DONE/$TOTAL tasks completed"

  # Show recent progress notes
  echo ""
  echo "=== Recent Progress ==="
  head -50 "$TASK_DIR/task_list.md"
else
  echo "=== NEW TASK MODE ==="
  echo "Creating new task at: $TASK_DIR"
  mkdir -p "$TASK_DIR"
fi
```

## Step 3: Choose Agent Mode

### For NEW Tasks (Initializer Mode)

If `task_list.md` does NOT exist in the task directory:

```bash
SKILL_DIR="${CLAUDE_PLUGIN_ROOT}/skills/autonomous-skill"
TASK_DIR=".autonomous/$TASK_NAME"

# Read the initializer prompt template
INITIALIZER_PROMPT=$(cat "$SKILL_DIR/templates/initializer-prompt.md")

# Execute initializer session
claude -p "Task: $USER_TASK_DESCRIPTION
Task Directory: $TASK_DIR

$INITIALIZER_PROMPT" \
  --output-format stream-json \
  --max-turns 50 \
  --append-system-prompt "You are the Initializer Agent. Create task_list.md and progress.md in $TASK_DIR directory."
```

### For CONTINUATION (Executor Mode)

If `task_list.md` EXISTS in the task directory:

```bash
SKILL_DIR="${CLAUDE_PLUGIN_ROOT}/skills/autonomous-skill"
TASK_DIR=".autonomous/$TASK_NAME"

# Read the executor prompt template
EXECUTOR_PROMPT=$(cat "$SKILL_DIR/templates/executor-prompt.md")

# Read current state
TASK_LIST=$(cat "$TASK_DIR/task_list.md")
PROGRESS=$(cat "$TASK_DIR/progress.md" 2>/dev/null || echo "No previous progress notes")

# Execute executor session
claude -p "Continue working on the task.
Task Directory: $TASK_DIR

Current task_list.md:
$TASK_LIST

Previous progress notes:
$PROGRESS

$EXECUTOR_PROMPT" \
  --output-format stream-json \
  --max-turns 100 \
  --append-system-prompt "You are the Executor Agent. Complete tasks and update files in $TASK_DIR directory."
```

## Step 4: Auto-Continue Loop

After each session completes, check remaining tasks and auto-continue:

```bash
#!/bin/bash
TASK_DIR=".autonomous/$TASK_NAME"
AUTO_CONTINUE_DELAY=3
SESSION_NUM=1

while true; do
  echo ""
  echo "=========================================="
  echo "  SESSION $SESSION_NUM - Task: $TASK_NAME"
  echo "=========================================="

  # Run the appropriate agent
  # ... execute session ...

  # Check completion
  if [ -f "$TASK_DIR/task_list.md" ]; then
    TOTAL=$(grep -c '^\- \[' "$TASK_DIR/task_list.md" 2>/dev/null || echo "0")
    DONE=$(grep -c '^\- \[x\]' "$TASK_DIR/task_list.md" 2>/dev/null || echo "0")

    echo ""
    echo "=== Progress: $DONE/$TOTAL tasks completed ==="

    if [ "$DONE" -eq "$TOTAL" ] && [ "$TOTAL" -gt 0 ]; then
      echo ""
      echo "All tasks completed! Exiting."
      break
    fi
  fi

  # Auto-continue with delay
  echo ""
  echo "Continuing in $AUTO_CONTINUE_DELAY seconds... (Press Ctrl+C to pause)"
  sleep $AUTO_CONTINUE_DELAY

  SESSION_NUM=$((SESSION_NUM + 1))
done
```

## Step 5: Report Progress

After execution, display a clear progress report:

```
==========================================
  SESSION COMPLETE - Task: build-rest-api
==========================================

Task Directory: .autonomous/build-rest-api/

Tasks completed this session:
- [x] Task 5: Implement user authentication
- [x] Task 6: Add login form validation

Overall Progress: 18/50 tasks (36%)

Next tasks:
- [ ] Task 7: Create password reset flow
- [ ] Task 8: Add session management

Continuing in 3 seconds... (Press Ctrl+C to pause)
```

## Usage Examples

### Example 1: Start New Task

```
User: Please use autonomous skill to build a REST API for a todo app

Response:
1. Generated task name: "build-rest-api-todo"
2. Created directory: .autonomous/build-rest-api-todo/
3. Running Initializer Agent...
4. Created task_list.md with 25 tasks
5. Progress: 3/25 completed
6. Auto-continuing in 3 seconds...
```

### Example 2: Continue Existing Task

```
User: Continue the autonomous task "build-rest-api-todo"

Response:
1. Found task: .autonomous/build-rest-api-todo/
2. Current progress: 15/25 tasks
3. Running Executor Agent...
4. Completed tasks 16-17
5. Progress: 17/25 completed
6. Auto-continuing in 3 seconds...
```

### Example 3: List All Tasks

```bash
# List all autonomous tasks
ls -la .autonomous/

# Show progress for specific task
cat .autonomous/build-rest-api-todo/task_list.md
```

## Key Files

For each task in `.autonomous/<task-name>/`:

| File | Purpose |
|------|---------|
| `task_list.md` | Master task list with checkbox progress |
| `progress.md` | Session-by-session progress notes |

## Important Notes

1. **Task Isolation**: Each task has its own directory, no conflicts
2. **Task Naming**: Auto-generated from description (lowercase, hyphens)
3. **Task List is Sacred**: Never delete or modify descriptions, only mark `[x]`
4. **One Task at a Time per Session**: Focus on completing tasks thoroughly
5. **Auto-Continue**: Sessions auto-continue with 3s delay; Ctrl+C to pause

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Task not found | Check `.autonomous/` for existing tasks |
| Multiple tasks | Specify task name explicitly |
| Session stuck | Check `progress.md` in task directory |
| Need to restart | Delete task directory and start fresh |
