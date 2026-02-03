---
name: hzl
description: This skill should be used when working with HZL for task tracking, when the user asks to "break down work into tasks", "track tasks with HZL", "claim a task", "checkpoint progress", "complete a task", or when working on a project that uses HZL. Provides guidance on effective task management patterns for AI agents.
---

# HZL Task Management

HZL is a lightweight task tracking system for AI agents. It is a dumb ledger—it tracks work state but does not orchestrate, prioritize, or decide what to do next. Orchestration logic belongs in agents, not in HZL.

This skill teaches how to use HZL effectively for tracking work across projects.

## When to Use HZL

HZL is designed for persistent, structured task tracking across sessions and agents.

**HZL excels at (strongly consider using it for):**
- Complex plans with **nesting** (parent tasks + subtasks)
- Tasks with **dependencies** (task B waits for task A)
- Need **visibility** into progress (web dashboard at `hzl serve`)
- **Long-running work** where checkpoints help track progress
- Work spanning **multiple sessions** or days
- **Multi-agent** coordination

**Your native tools (TodoWrite, update_plan) may be fine for:**
- Simple flat checklists
- Quick ephemeral notes within a short session
- Trivial tasks that don't need persistence

**Key differences:**
- HZL persists across sessions; native tools are session-local
- HZL supports nesting and dependencies; native tools are flat
- HZL has a web dashboard; native tools are context-only

Use your judgment. For anything non-trivial, HZL is usually the better choice.

## Core Concepts

**Projects** group related work. Use stable identifiers:
- Working in a repo → use the repository name (e.g., `myapp`)
- Long-lived agent → use agent identity (e.g., `openclaw`)

Projects are long-lived. Do not create per-feature projects.

**Tasks** are units of work within projects. Tasks can have:
- Priority (higher number = higher priority)
- Tags for categorization
- Dependencies on other tasks
- A parent task (creating a subtask relationship, max 1 level deep)

**Parent tasks** are organizational containers. They are never returned by `hzl task next`—only leaf tasks (tasks without children) are claimable work.

**Checkpoints** preserve progress. Use them liberally to enable recovery.

## Anti-pattern: Project Sprawl

Projects are stable containers—one per repo. Features, initiatives, and requests are **tasks**, not projects.

**Wrong (creates sprawl):**
```bash
hzl project create "query-perf"
hzl task add "Fix search N+1" -P query-perf
hzl task add "Cache statements" -P query-perf
hzl task add "Batch temp table" -P query-perf
```

**Correct (uses parent + subtasks):**
```bash
# Use existing repo project
hzl task add "Query performance fixes" -P myrepo
# → Created task abc123

hzl task add "Fix search N+1" --parent abc123
hzl task add "Cache statements" --parent abc123
hzl task add "Batch temp table" --parent abc123
```

Why this matters:
- Projects accumulate forever; you'll have dozens of abandoned one-off projects
- `hzl task next --project X` requires knowing which project to query
- Parent tasks group related work AND provide dashboard visibility (subtask progress rolls up)

## Sizing Parent Tasks

HZL supports one level of nesting (parent → subtasks). Scope parent tasks to completable outcomes.

**The completability test:** "I finished [parent task]" should describe a real outcome.
- ✓ "Finished the user authentication feature"
- ✗ "Finished the backend work" (frontend still pending)
- ✗ "Finished home automation" (open-ended, never done)

**Scope by problem, not technical layer.** A full-stack feature (frontend + backend + tests) is usually one parent if it ships together.

**Split into multiple parents when:**
- Parts deliver independent value (can ship separately)
- You're solving distinct problems that happen to be related

**Adding context:** Use `--links` to attach specs or design docs when the description isn't enough:
```bash
hzl task add "User authentication" -P myrepo \
  --links docs/auth-spec.md \
  --links "https://example.com/design-doc"
```

## ⚠️ DESTRUCTIVE COMMANDS - READ CAREFULLY

The following commands **PERMANENTLY DELETE HZL DATA** and cannot be undone:

| Command | Effect |
|---------|--------|
| `hzl init --force` | **DELETES ALL DATA.** Prompts for confirmation. |
| `hzl init --force --yes` | **DELETES ALL DATA WITHOUT CONFIRMATION.** Extremely dangerous. |
| `hzl task prune ... --yes` | **PERMANENTLY DELETES** old done/archived tasks and their event history. |

**AI agents: NEVER run these commands unless the user EXPLICITLY asks you to delete data.**

- `hzl init --force` deletes the entire event database: all projects, tasks, checkpoints, and history
- `hzl task prune` deletes only tasks in terminal states (done/archived) older than the specified age
- There is NO undo. There is NO recovery without a backup.

## Scenario: Setting Up

When starting work on a project that uses HZL:

```bash
# Check if HZL is initialized
hzl project list --json

# If no projects exist, initialize (safe, won't overwrite existing data)
hzl init

# Create or verify project exists
hzl project create <project-name>
```

Use the repository name as the project name for consistency.

## Scenario: Breaking Down Work

When facing a complex task or feature, use subtasks for organization and dependencies for sequencing.

### Using subtasks for organization

Subtasks group related work under a parent:

```bash
# Create the parent task (organizational container)
hzl task add "Implement user authentication" -P myapp --priority 2
# → Created task abc123

# Create subtasks (project inherited automatically)
hzl task add "Set up database schema" --parent abc123
hzl task add "Create auth endpoints" --parent abc123
hzl task add "Write auth tests" --parent abc123

# View the breakdown
hzl task show abc123
```

**Key behavior:** Parent tasks are organizational containers. When you call `hzl task next`, only leaf tasks (tasks without children) are returned. The parent is never "available work"—it represents the umbrella.

```bash
# Get next available subtask
hzl task next --project myapp
# → Returns a subtask, never the parent

# Scope to specific parent's subtasks
hzl task next --parent abc123
# → Returns next available subtask of abc123
```

When all subtasks are done, manually complete the parent:
```bash
hzl task complete abc123
```

### Using dependencies for sequencing

Dependencies express "must complete before" relationships:

```bash
# Create tasks with sequencing
hzl task add "Set up database schema" -P myapp --priority 2
hzl task add "Create auth endpoints" -P myapp --depends-on <schema-task-id>
hzl task add "Write auth tests" -P myapp --depends-on <endpoints-task-id>

# Validate no circular dependencies
hzl validate
```

### Combining subtasks and dependencies

Subtasks can have dependencies on other subtasks:

```bash
hzl task add "Auth feature" -P myapp --priority 2
# → parent123

hzl task add "Database schema" --parent parent123
# → schema456

hzl task add "Auth endpoints" --parent parent123 --depends-on schema456
hzl task add "Auth tests" --parent parent123 --depends-on <endpoints-id>
```

**Work breakdown principles:**
- Use subtasks to group related work under a logical parent
- Use dependencies to express sequencing requirements
- Break work into tasks that can be completed in a single session
- Parent tasks are never claimable—work happens on leaf tasks

## Scenario: Working on Tasks

The core workflow: list available → claim → work → checkpoint → complete.

### Find available work

```bash
# List tasks ready to be claimed (no unmet dependencies)
hzl task list --project myapp --available --json

# See what's next by priority
hzl task next --project myapp --json
```

Always use `--json` for structured output that can be parsed programmatically.

### Claim a task

```bash
# Claim by ID
hzl task claim <task-id> --author <agent-name>

# Or claim the next available task
hzl task next --project myapp --claim --author <agent-name>
```

Use `--author` to identify which agent owns the task. This enables tracking who is working on what.

For long-running work, use leases:

```bash
hzl task claim <task-id> --author <agent-name> --lease 30
```

The lease (in minutes) indicates how long before the task is considered stuck.

### Checkpoint progress

Checkpoint frequently to preserve progress:

```bash
# Simple checkpoint
hzl task checkpoint <task-id> "Completed database schema migration"

# Checkpoint with progress percentage (0-100)
hzl task checkpoint <task-id> "Halfway done with auth" --progress 50

# Checkpoint with structured data
hzl task checkpoint <task-id> "step-3-complete" --data '{"files":["auth.ts","user.ts"]}'
```

You can also set progress without a checkpoint:
```bash
hzl task progress <task-id> 75
```

Checkpoints serve two purposes:
1. Progress visibility for humans monitoring work
2. Recovery context if another agent needs to take over

### Check for steering comments

Before completing a task, check for human guidance:

```bash
hzl task show <task-id> --json
```

Review the task history for any comments added by humans. Incorporate steering feedback before marking complete.

### Complete the task

```bash
hzl task complete <task-id>
```

Only mark complete when the work is fully done and verified.

## Scenario: Handling Blocked Work

When a task cannot proceed due to external factors, mark it as blocked:

```bash
# Mark task as blocked with a reason
hzl task block <task-id> --reason "Waiting for API credentials from DevOps"

# Check task status
hzl task show <task-id> --json
```

Blocked tasks:
- Stay visible in the dashboard (Blocked column)
- Keep their assignee
- Don't appear in `--available` lists

When the blocker is resolved:

```bash
# Unblock the task (returns to in_progress)
hzl task unblock <task-id>

# Add a checkpoint and continue working
hzl task checkpoint <task-id> "Got API credentials, resuming work"
```

**Note:** `blocked` status is for external blockers (waiting for credentials, human decisions, etc.). Dependency blocking (task A depends on task B) is handled automatically—tasks with unmet dependencies won't appear in `--available` lists but remain in `ready` status.

## Scenario: Multi-Agent Coordination

When multiple agents work on the same project:

### Claiming prevents conflicts

HZL uses atomic claiming. Two agents calling `task next --claim` simultaneously will get different tasks. This prevents duplicate work.

### Authorship tracking

HZL tracks authorship at two levels:

| Concept | What it tracks | Set by |
|---------|----------------|--------|
| **Assignee** | Who owns the task | `--author` on `claim` |
| **Event author** | Who performed an action | `--author` on any command |

The `--author` flag appears on many commands (checkpoint, comment, block, etc.) to record who performed each action. This is separate from task ownership:

```bash
# Alice owns the task
hzl task claim <id> --author alice

# Bob adds a checkpoint (doesn't change ownership)
hzl task checkpoint <id> "Reviewed the code" --author bob

# Task is still assigned to Alice, but checkpoint was recorded by Bob
```

For AI agents that need session tracking, use `--agent-id` on claim:
```bash
hzl task claim <id> --author "Claude Code" --agent-id "session-abc123"
```

### Recover stuck tasks

If an agent dies or becomes unresponsive:

```bash
# Find tasks with expired leases
hzl task stuck --json

# Take over an expired task
hzl task steal <task-id> --if-expired --author agent-2
```

Before stealing, review checkpoints to understand where the previous agent left off:

```bash
hzl task show <task-id> --json
```

For advanced lease and recovery options, see `hzl task claim --help` and `hzl task steal --help`.

## Scenario: Human Oversight

Humans can monitor and steer agent work through HZL:

### Monitoring progress

```bash
hzl project list
hzl task list --project myapp --status in_progress
hzl task show <task-id>
```

### Providing guidance

```bash
hzl task comment <task-id> "Please also handle the edge case where user is already logged in"
```

Agents should check for comments before completing tasks (see "Check for steering comments" above).

## Command Quick Reference

| Action | Command |
|--------|---------|
| List projects | `hzl project list` |
| Create project | `hzl project create <name>` |
| Add task | `hzl task add "<title>" -P <project>` |
| Create subtask | `hzl task add "<title>" --parent <id>` |
| List available | `hzl task list --project <p> --available --json` |
| List subtasks | `hzl task list --parent <id>` |
| List root tasks | `hzl task list --root` |
| Claim task | `hzl task claim <id> --author <name>` |
| Checkpoint | `hzl task checkpoint <id> "<message>" [--progress 50]` |
| Set progress | `hzl task progress <id> <0-100>` |
| Block task | `hzl task block <id> --reason "<why>"` |
| Unblock task | `hzl task unblock <id>` |
| Show task | `hzl task show <id> --json` |
| Complete | `hzl task complete <id>` |
| Next subtask | `hzl task next --parent <id>` |
| Add dependency | `hzl task add-dep <task> <depends-on>` |
| Archive cascade | `hzl task archive <id> --cascade` |
| Validate | `hzl validate` |

For complete command options, use `hzl <command> --help`.

## Best Practices

1. **Always use `--json`** for programmatic output
2. **Checkpoint frequently** to enable recovery
3. **Check for comments** before completing tasks
4. **Use stable project names** derived from repo or agent identity
5. **Break down work** into single-session tasks
6. **Use dependencies** to express sequencing, not priority
7. **Use leases** for long-running work to enable stuck detection
8. **Review checkpoints** before stealing stuck tasks

## What HZL Does Not Do

HZL is deliberately limited:

- **No orchestration** - Does not spawn agents or assign work
- **No task decomposition** - Does not break down tasks automatically
- **No smart scheduling** - Uses simple priority + FIFO ordering

These are features for your orchestration layer, not for the task tracker.

**What HZL does provide** (but isn't covered in this skill):

- Cloud sync via Turso for backup and multi-device access (`hzl init --sync-url ...`)
- Web dashboard for human monitoring (`hzl serve`)
