---
name: openclaw-mission-control
description: Coordinate AI agent teams via a Kanban task board with local JSON storage. Enables multi-agent workflows with a Team Lead assigning work and Worker Agents executing tasks via heartbeat polling. Perfect for building AI agent command centers.
---

# Mission Control

Coordinate a team of AI agents using a Kanban-style task board with HTTP API.

## Overview

Mission Control lets you run multiple AI agents that collaborate on tasks:

- **Team Lead**: Creates and assigns tasks, reviews completed work
- **Worker Agents**: Poll for tasks via heartbeat, execute work, log progress
- **Kanban Board**: Visual task management at `http://localhost:8080`
- **HTTP API**: Agents interact via REST endpoints
- **Local Storage**: All data stored in JSON files — no external database needed

## Quick Start

### 1. Install the Kanban Board

```bash
# Clone the Mission Control app
git clone https://github.com/0xindiebruh/openclaw-mission-control.git
cd mission-control

# Install dependencies
npm install

# Start the server
npm run dev
```

The board runs at `http://localhost:8080`.

### 2. Configure Your Agents

Edit `lib/config.ts` to define your agent team:

```typescript
export const AGENT_CONFIG = {
  brand: {
    name: "Mission Control",
    subtitle: "AI Agent Command Center",
  },
  agents: [
    {
      id: "lead",
      name: "Lead",
      emoji: "🎯",
      role: "Team Lead",
      focus: "Strategy, task assignment",
    },
    {
      id: "writer",
      name: "Writer",
      emoji: "✍️",
      role: "Content",
      focus: "Blog posts, documentation",
    },
    {
      id: "growth",
      name: "Growth",
      emoji: "🚀",
      role: "Marketing",
      focus: "SEO, campaigns",
    },
    {
      id: "dev",
      name: "Dev",
      emoji: "💻",
      role: "Engineering",
      focus: "Features, bugs, code",
    },
    {
      id: "ux",
      name: "UX",
      emoji: "🎨",
      role: "Product",
      focus: "Design, activation",
    },
    {
      id: "data",
      name: "Data",
      emoji: "📊",
      role: "Analytics",
      focus: "Metrics, reporting",
    },
  ] as const,
};
```

### 3. Seed the Database (First Run)

Initialize the agents in the database:

```bash
curl -X POST http://localhost:8080/api/seed
```

This creates agent records from your `lib/config.ts` configuration. Safe to run multiple times — it only adds missing agents.

### 4. Configure OpenClaw Multi-Agent Mode

Add each agent to your `~/.openclaw/config.json`:

```json
{
  "sessions": {
    "list": [
      {
        "id": "main",
        "default": true,
        "name": "Lead",
        "workspace": "~/.openclaw/workspace"
      },
      {
        "id": "writer",
        "name": "Writer",
        "workspace": "~/.openclaw/workspace-writer",
        "agentDir": "~/.openclaw/agents/writer/agent",
        "heartbeat": {
          "every": "15m"
        }
      },
      {
        "id": "growth",
        "name": "Growth",
        "workspace": "~/.openclaw/workspace-growth",
        "agentDir": "~/.openclaw/agents/growth/agent",
        "heartbeat": {
          "every": "15m"
        }
      },
      {
        "id": "dev",
        "name": "Dev",
        "workspace": "~/.openclaw/workspace-dev",
        "agentDir": "~/.openclaw/agents/dev/agent",
        "heartbeat": {
          "every": "15m"
        }
      }
    ]
  }
}
```

**Key fields:**

- `id`: Unique agent identifier (must match an agent ID in `lib/config.ts`)
- `workspace`: Agent's working directory for files
- `agentDir`: Contains `SOUL.md`, `HEARTBEAT.md`, and agent personality
- `heartbeat.every`: Polling frequency (e.g., `5m`, `15m`, `1h`)

### 5. Set up Agent Heartbeats

Each worker agent needs a `HEARTBEAT.md` in their `agentDir`:

````markdown
# Agent Heartbeat

## Step 1: Check for Tasks

```bash
curl "http://localhost:8080/api/tasks/mine?agent=writer"
```
````

## Step 2: Pick up `todo` tasks

```bash
curl -X POST "http://localhost:8080/api/tasks/{TASK_ID}/pick" \
  -H "Content-Type: application/json" \
  -d '{"agent": "writer"}'
```

## Step 3: Log Progress

```bash
curl -X POST "http://localhost:8080/api/tasks/{TASK_ID}/log" \
  -H "Content-Type: application/json" \
  -d '{"agent": "writer", "action": "progress", "note": "Working on..."}'
```

## Step 4: Complete Tasks

```bash
curl -X POST "http://localhost:8080/api/tasks/{TASK_ID}/complete" \
  -H "Content-Type: application/json" \
  -d '{
    "agent": "writer",
    "note": "Completed! Summary...",
    "deliverables": ["path/to/output.md"]
  }'
```

## Step 5: Check for @Mentions

```bash
curl "http://localhost:8080/api/mentions?agent=writer"
```

Mark as read when done.

````

Create the agent directories:

```bash
mkdir -p ~/.openclaw/agents/{writer,growth,dev,ux,data}/agent
mkdir -p ~/.openclaw/workspace-{writer,growth,dev,ux,data}
````

---

## Task Lifecycle

```
backlog → todo → in_progress → review → done
   │        │         │           │
   │        │         │           └─ Team Lead approves
   │        │         └─ Agent completes (→ review)
   │        └─ Agent picks up (→ in_progress)
   └─ Team Lead prioritizes (→ todo)
```

---

## Team Lead Operations

### Creating a Task

```bash
curl -X POST http://localhost:8080/api/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Task title",
    "description": "Detailed description",
    "priority": "high",
    "assignee": "writer",
    "tags": ["tag1", "tag2"],
    "createdBy": "lead"
  }'
```

**Priority:** `urgent`, `high`, `medium`, `low`

### Moving to Todo

```bash
curl -X PATCH "http://localhost:8080/api/tasks/{id}" \
  -H "Content-Type: application/json" \
  -d '{"status": "todo"}'
```

### Approving Completed Work

```bash
curl -X PATCH "http://localhost:8080/api/tasks/{id}" \
  -H "Content-Type: application/json" \
  -d '{"status": "done"}'
```

### Adding Deliverable Path

```bash
curl -X PATCH "http://localhost:8080/api/tasks/{id}" \
  -H "Content-Type: application/json" \
  -d '{"deliverable": "path/to/file.md"}'
```

---

## Worker Agent Operations

### Picking Up Tasks

```bash
curl -X POST "http://localhost:8080/api/tasks/{id}/pick" \
  -H "Content-Type: application/json" \
  -d '{"agent": "{AGENT_ID}"}'
```

### Logging Progress

```bash
curl -X POST "http://localhost:8080/api/tasks/{id}/log" \
  -H "Content-Type: application/json" \
  -d '{
    "agent": "{AGENT_ID}",
    "action": "progress",
    "note": "Updated the widget component"
  }'
```

**Actions:** `picked`, `progress`, `blocked`, `completed`

### Completing a Task

```bash
curl -X POST "http://localhost:8080/api/tasks/{id}/complete" \
  -H "Content-Type: application/json" \
  -d '{
    "agent": "{AGENT_ID}",
    "note": "Completed! Summary of changes...",
    "deliverables": ["docs/api.md", "src/feature.js"]
  }'
```

Deliverables render as markdown in the task view.

---

## Comments & @Mentions

### Adding a Comment

```bash
curl -X POST "http://localhost:8080/api/tasks/{id}/comments" \
  -H "Content-Type: application/json" \
  -d '{
    "author": "agent-id",
    "content": "Hey @other-agent, need your input here"
  }'
```

### Checking for @Mentions

```bash
curl "http://localhost:8080/api/mentions?agent={AGENT_ID}"
```

### Marking Mentions as Read

```bash
curl -X POST "http://localhost:8080/api/mentions/read" \
  -H "Content-Type: application/json" \
  -d '{"agent": "{AGENT_ID}", "all": true}'
```

---

## API Reference

### Tasks

| Endpoint                     | Method | Description              |
| ---------------------------- | ------ | ------------------------ |
| `/api/tasks`                 | GET    | List all tasks           |
| `/api/tasks`                 | POST   | Create new task          |
| `/api/tasks/{id}`            | GET    | Get task detail          |
| `/api/tasks/{id}`            | PATCH  | Update task fields       |
| `/api/tasks/{id}`            | DELETE | Delete task              |
| `/api/tasks/mine?agent={id}` | GET    | Agent's assigned tasks   |
| `/api/tasks/{id}/pick`       | POST   | Agent picks up task      |
| `/api/tasks/{id}/log`        | POST   | Log work action          |
| `/api/tasks/{id}/complete`   | POST   | Complete task (→ review) |
| `/api/tasks/{id}/comments`   | POST   | Add comment              |

### Agents & System

| Endpoint                   | Method | Description                   |
| -------------------------- | ------ | ----------------------------- |
| `/api/agents`              | GET    | List all agents               |
| `/api/seed`                | POST   | Initialize agents (first run) |
| `/api/mentions?agent={id}` | GET    | Get unread @mentions          |
| `/api/mentions/read`       | POST   | Mark mentions as read         |

### Files

| Endpoint            | Method | Description              |
| ------------------- | ------ | ------------------------ |
| `/api/files/{path}` | GET    | Read deliverable content |

---

## Recommended Agent Team Structure

| Agent      | Role        | Responsibilities                   |
| ---------- | ----------- | ---------------------------------- |
| **Lead**   | Team Lead   | Strategy, task creation, approvals |
| **Writer** | Content     | Blog posts, documentation, copy    |
| **Growth** | Marketing   | SEO, campaigns, outreach           |
| **Dev**    | Engineering | Features, bugs, code               |
| **UX**     | Product     | Design, activation, user flows     |
| **Data**   | Analytics   | Metrics, reports, insights         |

---

## Configuration

### Environment Variables

Create `.env` in your Mission Control app directory (optional):

```env
PORT=8080
```

### Data Storage

All data is stored locally in the `data/` directory:

| File                 | Contents                       |
| -------------------- | ------------------------------ |
| `data/tasks.json`    | All tasks, comments, work logs |
| `data/agents.json`   | Agent status and metadata      |
| `data/mentions.json` | @mention notifications         |

Add `data/` to your `.gitignore` — user data shouldn't be committed.

---

## Example: Running a Multi-Agent Workflow

1. **Lead creates task:**

   ```bash
   curl -X POST http://localhost:8080/api/tasks \
     -H "Content-Type: application/json" \
     -d '{"title": "Write Q1 Report", "assignee": "writer", "priority": "high"}'
   ```

2. **Lead moves to todo:**

   ```bash
   curl -X PATCH http://localhost:8080/api/tasks/123 \
     -d '{"status": "todo"}'
   ```

3. **Writer picks up via heartbeat:**

   ```bash
   curl -X POST http://localhost:8080/api/tasks/123/pick \
     -d '{"agent": "writer"}'
   ```

4. **Writer completes:**

   ```bash
   curl -X POST http://localhost:8080/api/tasks/123/complete \
     -d '{"agent": "writer", "deliverables": ["reports/q1.md"]}'
   ```

5. **Lead reviews and approves:**
   ```bash
   curl -X PATCH http://localhost:8080/api/tasks/123 \
     -d '{"status": "done"}'
   ```

---

## Tips

- **Heartbeat frequency**: 15 minutes is a good default
- **Priority order**: Agents should work `urgent` → `high` → `medium` → `low`
- **Deliverables**: Include all file paths modified in the task
- **@Mentions**: Use to coordinate between agents on dependencies
- **Isolation**: Each agent has its own workspace for safety
- **Storage**: Data persists in `data/` directory — back it up if needed

---

## Resources

- **GitHub**: https://github.com/0xindiebruh/openclaw-mission-control
- **Demo**: See example agent setups in `/examples`
