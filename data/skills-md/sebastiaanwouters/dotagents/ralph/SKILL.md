---
name: ralph
description: "Autonomous feature development - setup and execution. Triggers on: ralph, set up ralph, run ralph, run the loop, implement tasks. Two phases: (1) Setup - chat through feature, create tasks with dependencies (2) Loop - pick ready tasks, implement, commit, repeat until done."
references:
  - references/setup.md
  - references/execution-loop.md
  - references/task-format.md
---

# Ralph - Autonomous Feature Development

Interactive feature planning and autonomous task execution.

## Two Phases

| Phase | Purpose | Trigger |
|-------|---------|---------|
| **Setup** | Plan feature, create tasks with dependencies | "set up ralph", "plan feature" |
| **Loop** | Execute tasks autonomously until done | "run ralph", "start the loop" |

## Quick Start

### Mode Selection

Ask the user:
```
Are you:
1. Starting a new feature (I'll help you plan and create tasks)
2. Using existing tasks (I'll set up Ralph to run them)
```

### Mode 1: New Feature
1. Chat through the feature - Ask clarifying questions
2. Break into small tasks - Each completable in one iteration
3. Create task_list tasks - Parent + subtasks with `dependsOn`
4. Set up ralph files - See [setup.md](references/setup.md)

### Mode 2: Existing Tasks
1. Find existing parent task
2. Verify subtasks have proper `dependsOn`
3. Set up ralph files
4. Show status (ready, completed, blocked)

## Core Principles

### Task Sizing

**Each task must be completable in ONE iteration (~one context window).**

**Right-sized:**
- Add a database column + migration
- Create a single UI component
- Implement one server action

**Too big (split these):**
- "Build the entire dashboard"
- "Add authentication"
- "Refactor the API"

**Rule of thumb:** If you can't describe the change in 2-3 sentences, it's too big.

### Dependency Order

```
Task 1: Schema (no dependencies)
Task 2: Server action (dependsOn: [task-1])
Task 3: UI component (dependsOn: [task-2])
Task 4: Tests (dependsOn: [task-3])
```

## Loop Workflow (Phase 2)

1. Read parent task ID from `scripts/ralph/parent-task-id.txt`
2. Query ready tasks (descendants of parent, `ready: true`, `status: "open"`)
3. Pick next task (prefer related to just-completed work)
4. Execute via handoff with quality checks
5. Update progress.txt, commit, mark complete
6. Re-invoke ralph to continue

**Stop condition:** All tasks completed → Archive progress, report success.

See [execution-loop.md](references/execution-loop.md) for full details.

## Quality Requirements

Before marking any task complete:
- Typecheck must pass (project's typecheck command)
- Tests must pass (project's test command)
- Changes must be committed
- Progress must be logged

## Key Files

| File | Purpose |
|------|---------|
| `scripts/ralph/parent-task-id.txt` | Current feature's parent task ID |
| `scripts/ralph/progress.txt` | Short-term memory for current feature |
| `scripts/ralph/archive/` | Archived progress from completed features |

## References

- [Setup Workflow](references/setup.md) - Detailed setup for both modes
- [Execution Loop](references/execution-loop.md) - Full loop implementation
- [Task Format](references/task-format.md) - How to write task descriptions
