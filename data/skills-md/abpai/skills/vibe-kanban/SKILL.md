---
name: vibe-kanban
description: >
  Manage work in Vibe Kanban (VK), the shared source of truth for agent tasks.
  Use when checking assigned work, creating/updating tasks, running heartbeat
  checks, scanning @mentions, or producing daily standup summaries. Triggers:
  "check the board", "what's on my plate", "create/update task", "heartbeat",
  "standup summary".
metadata:
  clawdbot:
    emoji: "\U0001F4CB"
    requires:
      bins: ["vk", "bun"]
---

# Vibe Kanban — Task Board Skill

Vibe Kanban (VK) is the shared task board for all agents and the single source
of truth for current work.

## When to Use

Use this skill when you need to:

- Check what you should work on next
- Claim, create, update, or complete tasks
- Run a heartbeat task check
- Scan for `@your-agent-id` mentions in task descriptions
- Generate a daily standup summary

## Access

### CLI (primary)

The `vk` binary is a standalone CLI generated from the VK MCP server schema.
It lives at `vibe-kanban/scripts/vk` and requires `bun` at runtime.

```bash
vk <command> [--flag value ...]
vk --help                         # list all commands
vk <command> --help               # help for a specific command
```

### MCP tools (alternative)

If the `vibe_kanban` MCP server is configured in your Claude Code session, you
can call tools directly (e.g. `list_projects`, `list_tasks`) without the CLI.

## Tool Reference

### Task management

```bash
vk list-projects
vk list-tasks --project-id <ID>
vk list-tasks --project-id <ID> --status todo
vk list-tasks --project-id <ID> --status inprogress --limit 10
vk create-task --project-id <ID> --title "[agent-id] Task description"
vk create-task --project-id <ID> --title "Title" --description "Details"
vk get-task --task-id <ID>
vk update-task --task-id <ID> --status inprogress
vk update-task --task-id <ID> --status done
vk delete-task --task-id <ID>
```

### Repository management

```bash
vk list-repos --project-id <ID>
vk get-repo --repo-id <ID>
vk update-setup-script --repo-id <ID> --script '#!/bin/bash\n...'
vk update-cleanup-script --repo-id <ID> --script '...'
vk update-dev-server-script --repo-id <ID> --script '...'
```

### Workspace sessions

```bash
vk start-workspace-session --task-id <ID> --executor CLAUDE_CODE --repos <repo-id1>,<repo-id2>
```

Supported executors: `CLAUDE_CODE`, `AMP`, `GEMINI`, `CODEX`, `OPENCODE`,
`CURSOR_AGENT`, `QWEN_CODE`, `COPILOT`, `DROID`.

## Task Statuses

| Status | Meaning |
|-------------|-------------------------------|
| `todo` | Not started |
| `inprogress`| Actively being worked on |
| `inreview` | Work done, awaiting review |
| `done` | Completed |
| `cancelled` | No longer needed |

## Task Assignment Convention

Assign tasks with a title prefix: `[agent-id]`.

Examples:

- `[main] Configure daily standup cron`
- `[andrej] Document all ~/Projects repos`
- `[fury] Research LLM fine-tuning approaches`

When checking assignments, filter by your own prefix first.

## Heartbeat Workflow

1. List todo tasks: `vk list-tasks --project-id <ID> --status todo`
2. Filter tasks with your `[agent-id]` prefix
3. Pick the highest-priority task (first valid match is acceptable)
4. Claim it: `vk update-task --task-id <ID> --status inprogress`
5. Execute the task work
6. Mark complete: `vk update-task --task-id <ID> --status done`
7. If no matching task exists, reply `HEARTBEAT_OK`
8. Scan descriptions for `@your-agent-id` mentions and respond as needed

## Standup Summary Workflow

1. List all tasks across all statuses
2. Group by status: **done** (last 24h), **inprogress**, **inreview**, **todo**
3. Format as:

```
📋 Daily Standup — YYYY-MM-DD

✅ Completed:
- [agent] Task description

🔍 In Review:
- [agent] Task description

🔄 In Progress:
- [agent] Task description

📌 To Do:
- [agent] Task description
```

## Tips

- Keep titles concise and descriptive
- Always include `[agent-id]` when creating tasks
- Update task status promptly so board state stays reliable
- Use descriptions for details, links, and handoff context
- Pass empty string to `--script` to clear a script
- Use `-o json` or `--output json` for machine-readable output (formats: text, markdown, json, raw)
