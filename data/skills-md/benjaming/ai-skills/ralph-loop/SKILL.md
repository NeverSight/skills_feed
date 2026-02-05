---
name: ralph-loop
description: Create autonomous iterative loops (Ralph Wiggum pattern) for multi-step tasks. Use when setting up automated workflows that iterate over a backlog of tasks with clear acceptance criteria. Triggers on requests like "create a ralph loop", "set up an iterative agent", "automate this migration", or "create an autonomous loop".
argument-hint: [output-directory]
disable-model-invocation: true
---

# Ralph Loop Creator

Create autonomous iterative loops that process a backlog of tasks with clear acceptance criteria. Named after the Ralph Wiggum pattern for spec-driven autonomous development.

## Overview

A Ralph loop consists of:
- **Task System** - Native Claude Code task management with dependency tracking
- **Prompt** (`prompt.md`) - Instructions for each iteration
- **Runner** (`ralph.sh`) - Bash script that loops until completion
- **Progress** (`progress.txt`) - Execution log
- **Knowledge** (`knowledge.md`) - Accumulated learnings

## Quick Start

To create a new Ralph loop, gather requirements then run the init script:

```bash
python ~/.claude/skills/ralph-loop/scripts/init_ralph.py <output-dir>
```

## Workflow

### Step 1: Gather Requirements

Before creating a loop, clarify these parameters with the user using AskUserQuestion:

**Loop Goal:**
- What is the global objective of this loop?
- What domain/codebase does it operate on?

**Task Structure:**
- What kind of tasks/items will be tracked?
- What dependencies exist between tasks?
- What metadata should each task have?

**Iteration Process:**
- What steps should each iteration perform?
- What tools/commands are needed?
- What files should be read/written?

**Acceptance Criteria:**
- How to validate a task is completed?
- What checks should pass before marking done?
- Should there be automated validation (tests, builds, typechecks)?

**Exit Conditions:**
- When should the loop terminate? (all tasks done, specific marker, max iterations)
- What completion marker to use? Default: `<promise>COMPLETE</promise>`

### Step 2: Select or Create Template

Available templates in `~/.claude/skills/ralph-loop/templates/`:

| Template | Use Case |
|----------|----------|
| `migration.md` | Migrating components, APIs, dependencies |
| `exploration.md` | Codebase analysis, documentation generation |
| `testing.md` | Test generation, coverage improvement |
| `refactoring.md` | Code cleanup, pattern enforcement |
| `custom.md` | Blank template for unique workflows |

### Step 3: Generate Loop Files

After gathering requirements, generate the loop structure:

```bash
python ~/.claude/skills/ralph-loop/scripts/init_ralph.py \
  --template migration \
  --output ./my-loop \
  --goal "Migrate React components from styled-components to Tailwind"
```

Or interactively:
```bash
python ~/.claude/skills/ralph-loop/scripts/init_ralph.py ./my-loop
```

### Step 4: Create Tasks Using Task System

After generating the loop, create tasks using the native Task tools:

```
TaskCreate:
  subject: "Migrate Button component"
  description: "Convert Button from styled-components to Tailwind CSS classes"
  activeForm: "Migrating Button component"
```

Set up dependencies between tasks:
```
TaskUpdate:
  taskId: "2"
  addBlockedBy: ["1"]  # Task 2 waits for Task 1
```

### Step 5: Run the Loop

```bash
cd <output-dir>
./ralph.sh [max-iterations]
```

Default max iterations: 50

## File Structure

```
<output-dir>/
├── ralph.sh          # Executable bash loop
├── prompt.md         # Iteration instructions (uses Task tools)
├── progress.txt      # Execution log
├── knowledge.md      # Accumulated learnings
└── logs/             # Per-run log files
```

## Task System Integration

The Ralph loop uses Claude Code's native Task management system:

**Tools:**
- `TaskCreate` - Create new tasks with subject, description, activeForm
- `TaskList` - View all tasks with status/owner/blockers
- `TaskGet` - Fetch full task details by ID
- `TaskUpdate` - Change status, set dependencies, mark complete

**Status values:** `pending`, `in_progress`, `completed`

**Dependencies:**
- `blocks` - Tasks that cannot start until this one completes
- `blockedBy` - Tasks that must complete before this one can start

**Benefits over JSON backlog:**
- Native dependency tracking
- Status validation (can't mark complete if tests fail)
- Parallel agent coordination via owner field
- Progress spinner shows activeForm text

## Prompt Template Structure

```markdown
# Ralph Agent: {Goal}

## Configuration
- List paths, files, tools

## Your Task (One Iteration)

### Step 1: Load Context
Use TaskList to get all tasks, read knowledge.md

### Step 2: Determine State
Check if all tasks are completed → output <promise>COMPLETE</promise>

### Step 3: Select Target
Use TaskList to find first task with:
- status: "pending"
- blockedBy: empty (no unresolved dependencies)
Use TaskUpdate to set status: "in_progress"

### Step 4-N: Execute
Task-specific steps using TaskGet for full details

### Final Step: Update
Use TaskUpdate to set status: "completed"
Update progress.txt and knowledge.md

## Completion
When all tasks completed: <promise>COMPLETE</promise>
```

## Creating Initial Tasks

After generating the loop, create tasks for the backlog. Example for a migration loop:

```
# Create first task
TaskCreate:
  subject: "Migrate Button component"
  description: "Convert Button.tsx from styled-components to Tailwind. Update imports, replace styled() calls with className props using Tailwind utilities."
  activeForm: "Migrating Button component"

# Create dependent task
TaskCreate:
  subject: "Migrate Modal component"
  description: "Convert Modal.tsx. Depends on Button migration since Modal uses Button internally."
  activeForm: "Migrating Modal component"

# Set dependency
TaskUpdate:
  taskId: "2"
  addBlockedBy: ["1"]
```

**Tip:** Use TaskUpdate with `addBlockedBy` to ensure tasks run in correct order.

## Best Practices

1. **One task per iteration** - Keep iterations focused
2. **Clear acceptance criteria** - Define what "done" means
3. **Use dependencies** - Set blockedBy for ordered tasks
4. **Incremental commits** - Commit after each successful task
5. **Knowledge accumulation** - Document learnings for future iterations
6. **Fail fast** - Stop on errors, don't silently continue
7. **Idempotent operations** - Safe to re-run if interrupted

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Loop never completes | Check completion marker in prompt.md matches ralph.sh |
| Tasks skipped | Verify status field updates in prompt.md |
| Context overflow | Reduce prompt.md size, move details to knowledge.md |
| Permission errors | Ensure ralph.sh has execute permissions |

## References

- [templates/](templates/) - Pre-built loop templates
- [references/patterns.md](references/patterns.md) - Common iteration patterns
