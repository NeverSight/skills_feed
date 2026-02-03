---
name: ats
description: Connect to ATS backend for task orchestration. Use when creating, listing, claiming, or completing tasks, watching real-time events, or coordinating work between agents and humans.
---

# ATS Backend Skill

Connect to and interact with the Agent Task Service (ATS) backend for task orchestration between AI agents and humans.

## Overview

The Agent Task Service is a PostgreSQL-backed task orchestration platform that enables intelligent handoffs between agents and humans. Use this skill when you need to:

- Create, list, claim, or complete tasks
- Subscribe to real-time task events
- Send messages on task threads
- Coordinate work between agents and humans

## Prerequisites

**FIRST: Verify ATS CLI Installation**

```bash
ats --version  # Requires v1.x+
```

If not installed:

```bash
npm install -g @difflabai/ats-cli
```

**Default Server:** `https://ats.difflab.ai`

**Environment Variables:**
- `ATS_URL` - Override server URL
- `ATS_ORG` - Default organization
- `ATS_PROJECT` - Default project
- `ATS_ACTOR_TYPE` - Default actor type (human, agent, system)
- `ATS_ACTOR_ID` - Default actor ID
- `ATS_ACTOR_NAME` - Default actor display name

---

## Configuration

ATS CLI stores defaults in `~/.ats/config`:

```json
{
  "organization": "default",
  "project": "main",
  "url": "https://ats.difflab.ai",
  "actor": {
    "type": "agent",
    "id": "claude-code",
    "name": "Claude Code"
  }
}
```

**Priority:** CLI flags > environment variables > config file > defaults

---

## Organization Commands

```bash
# List organizations you belong to
ats org list

# Get organization details
ats org get <slug>

# Set default organization
ats org switch <slug>

# Show current organization
ats org current

# Create a new organization
ats org create <slug> --name "Organization Name"
```

---

## Project Commands

```bash
# List projects in current org (with task counts)
ats project list

# Get project details
ats project get <slug>

# Set default project
ats project switch <slug>

# Show current project
ats project current

# Create a new project
ats project create <slug> --name "Project Name" --description "..."
```

---

## Task Operations

### List Tasks

```bash
# List pending tasks (default - what needs attention)
ats list

# List all tasks
ats list --all

# Filter by status, channel, type
ats list --status in_progress
ats list --channel reviews
ats list --type approval

# Combine filters
ats list --status pending --channel support --limit 10

# JSON output for scripting
ats list -f json | jq '.[] | .title'
```

### Create a Task

```bash
# Simple task
ats create "Review the pull request"

# With options
ats create "Deploy to production" \
  --type deployment \
  --channel ops \
  --priority 8 \
  --description "Deploy v2.1.0 to production cluster"

# With JSON payload
ats create "Process data import" \
  --payload '{"source": "s3://bucket/data.csv", "rows": 50000}'
```

**Priority levels:** 1-10, higher is more urgent (default: 5)

### Get Task Details

```bash
# Human-readable output
ats get 123

# JSON for scripting
ats get 123 -f json | jq '.status'
```

### Update a Task

```bash
ats update 123 --priority 9
ats update 123 --title "Updated title" --description "New description"
```

### Claim a Task (Start Working)

Claiming moves the task to `in_progress` and starts a lease timer:

```bash
ats claim 123

# Custom lease duration (ms)
ats claim 123 --lease 120000
```

**Important:** The lease expires after 60 seconds by default. If the worker crashes, the task returns to `pending` automatically.

### Complete a Task

```bash
# Simple completion
ats complete 123

# With output data
ats complete 123 --outputs '{"result": "Approved", "notes": "LGTM"}'
```

### Cancel a Task

```bash
ats cancel 123
```

### Fail a Task

```bash
ats fail 123 --reason "Unable to connect to external service"
```

### Reject a Task

```bash
ats reject 123 --reason "This task is outside my capabilities"
```

### Delete a Task

```bash
ats delete 123
```

---

## Message Operations

### Add a Message to a Task

```bash
# Simple text message
ats message add 123 "I've started working on this"

# With content type
ats message add 123 '{"status": "analyzing", "progress": 50}' --type data
```

### List Messages for a Task

```bash
ats message list 123

# JSON output
ats message list 123 -f json
```

---

## Real-Time Events

### Watch for Events

```bash
# Watch all events
ats watch

# Filter by channel
ats watch --channel support

# Filter by task type
ats watch --type approval

# Filter by specific events
ats watch --events task.created,task.completed
```

**Event Types:**
- `task.created` - New task created
- `task.claimed` - Task claimed by worker
- `task.updated` - Task fields modified
- `task.completed` - Task finished successfully
- `task.cancelled` - Task cancelled
- `task.failed` - Task failed with error
- `task.rejected` - Task rejected by worker
- `task.message` - New message added
- `task.lease_expired` - Worker lease expired, task returned to pending

---

## Task Status Flow

```
pending ──claim──→ in_progress ──complete──→ completed
   │                    │
   │                    ├──cancel───→ cancelled
   │                    │
   │                    ├──fail─────→ failed
   │                    │
   │                    └─(lease expires)─→ pending
   │
   └──reject──→ rejected
```

**Terminal states:** `completed`, `cancelled`, `failed`, `rejected`

---

## Common Patterns

### Pattern 1: Create Task and Wait for Human Response

```bash
# Create task for human review
TASK_ID=$(ats create "Approve deployment" --type approval --channel ops -f json | jq -r '.id')
echo "Created task: $TASK_ID"

# Poll for completion
while true; do
  STATUS=$(ats get $TASK_ID -f json | jq -r '.status')
  if [ "$STATUS" = "completed" ] || [ "$STATUS" = "rejected" ]; then
    echo "Task finished with status: $STATUS"
    break
  fi
  sleep 5
done
```

### Pattern 2: Claim and Process Tasks

```bash
# Get first pending task of a specific type
TASK_ID=$(ats list --type code-review -f json | jq -r '.[0].id')

# Claim it
ats claim $TASK_ID

# Do the work...

# Complete with results
ats complete $TASK_ID --outputs '{"review": "LGTM, approved"}'
```

### Pattern 3: Escalate to Human

When Claude Code encounters something requiring human decision:

```bash
ats create "Human decision required: Delete production database?" \
  --type escalation \
  --channel urgent \
  --priority 10 \
  --description "The user requested to delete the production database. This requires human approval." \
  --payload '{
    "context": "User command: DROP DATABASE production",
    "risk_level": "critical",
    "suggested_action": "confirm_with_user"
  }'
```

### Pattern 4: Pipeline with jq

```bash
# Get high-priority pending tasks
ats list -f json | jq '.[] | select(.priority >= 8)'

# Count tasks by status
ats list --all -f json | jq 'group_by(.status) | map({status: .[0].status, count: length})'

# Get task IDs for a channel
ats list --channel support -f json | jq -r '.[].id'
```

---

## Actor Identity

Configure how you appear in ATS:

```bash
# As an agent (default for Claude Code)
ats list --actor-type agent --actor-id claude-code --actor-name "Claude Code Agent"

# As a human
ats list --actor-type human --actor-id user-123 --actor-name "John Doe"

# Or set via environment
export ATS_ACTOR_TYPE=agent
export ATS_ACTOR_ID=claude-code
export ATS_ACTOR_NAME="Claude Code Agent"
```

---

## Health Check

```bash
ats health
```

---

## Global Options

| Option | Short | Description |
|--------|-------|-------------|
| `--url` | `-u` | Service URL (default: https://ats.difflab.ai) |
| `--org` | | Override default organization |
| `--project` | | Override default project |
| `--format` | `-f` | Output format: table, json |
| `--actor-type` | | Actor type: human, agent, system |
| `--actor-id` | | Actor identifier |
| `--actor-name` | | Actor display name |
| `--verbose` | `-v` | Verbose output (shows HTTP requests) |
| `--help` | `-h` | Show help |

---

## Quick Reference

| Operation | Command |
|-----------|---------|
| **Organizations** | |
| List orgs | `ats org list` |
| Switch org | `ats org switch <slug>` |
| Current org | `ats org current` |
| **Projects** | |
| List projects | `ats project list` |
| Switch project | `ats project switch <slug>` |
| Current project | `ats project current` |
| **Tasks** | |
| List pending | `ats list` |
| List all | `ats list --all` |
| Create task | `ats create "title"` |
| Get task | `ats get ID` |
| Update task | `ats update ID --priority 8` |
| Claim task | `ats claim ID` |
| Complete task | `ats complete ID` |
| Cancel task | `ats cancel ID` |
| Fail task | `ats fail ID --reason "..."` |
| Reject task | `ats reject ID --reason "..."` |
| Add message | `ats message add ID "text"` |
| List messages | `ats message list ID` |
| Watch events | `ats watch` |
| Health check | `ats health` |
