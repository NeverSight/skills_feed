---
name: ralph-tools
description: Use when managing runtime tasks or memories during Ralph orchestration runs
---

# Ralph Tools

Quick reference for `ralph tools task` and `ralph tools memory` commands used during orchestration.

## Two Task Systems

| System | Command | Purpose | Storage |
|--------|---------|---------|---------|
| **Runtime tasks** | `ralph tools task` | Track work items during runs | `.agent/tasks.jsonl` |
| **Code tasks** | `ralph task` | Implementation planning | `tasks/*.code-task.md` |

This skill covers **runtime tasks**. For code tasks, see `/code-task-generator`.

## Task Commands

```bash
ralph tools task add "Title" -p 2 -d "description" --blocked-by id1,id2
ralph tools task list [--status open|in_progress|closed] [--format table|json|quiet]
ralph tools task ready                    # Show unblocked tasks
ralph tools task close <task-id>
ralph tools task show <task-id>
```

**Task ID format:** `task-{timestamp}-{4hex}` (e.g., `task-1737372000-a1b2`)

**Priority:** 1-5 (1 = highest, default 3)

## Memory Commands

```bash
ralph tools memory add "content" -t pattern --tags tag1,tag2
ralph tools memory list [-t type] [--tags tags]
ralph tools memory search "query" [-t type] [--tags tags]
ralph tools memory prime --budget 2000    # Output for context injection
ralph tools memory show <mem-id>
ralph tools memory delete <mem-id>
```

**Memory types:**
- `pattern` (default) - How this codebase does things
- `decision` - Why something was chosen
- `fix` - Solution to a recurring problem
- `context` - Project-specific knowledge

**Memory ID format:** `mem-{timestamp}-{4hex}` (e.g., `mem-1737372000-a1b2`)

**NEVER use echo/cat to write tasks or memories** — always use CLI tools.

## Output Formats

All commands support `--format`:
- `table` (default) - Human-readable
- `json` - Machine-parseable
- `quiet` - IDs only (for scripting)
- `markdown` - Memory prime only

## Common Workflows

### Track dependent work
```bash
ralph tools task add "Setup auth" -p 1
# Returns: task-1737372000-a1b2

ralph tools task add "Add user routes" --blocked-by task-1737372000-a1b2
ralph tools task ready  # Only shows unblocked tasks
```

### Store a discovery
```bash
ralph tools memory add "Parser requires snake_case keys" -t pattern --tags config,yaml
```

### Find relevant memories
```bash
ralph tools memory search "config" --tags yaml
ralph tools memory prime --budget 1000 -t pattern  # For injection
```
