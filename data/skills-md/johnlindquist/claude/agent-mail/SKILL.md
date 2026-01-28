---
name: agent-mail
description: Inter-agent communication for multi-agent workflows. Use when multiple agents need to coordinate, share information, or reserve resources.
---

# Agent Mail System

Communication system for coordinating multiple agents.

## Overview

Agent mail enables:
- Message passing between agents
- File reservation to prevent conflicts
- Session tracking across agents
- Thread-based conversations

## Session Management

### Start Agent Session

Register agent and get inbox:

```bash
# Initialize session
curl -X POST http://localhost:3847/api/session/start \
  -H "Content-Type: application/json" \
  -d '{
    "project_path": "/path/to/project",
    "program": "claude-code",
    "model": "opus-4",
    "agent_name": "agent-1",
    "task_description": "Working on auth module"
  }'
```

### List Agents

```bash
curl http://localhost:3847/api/agents?project_path=/path/to/project
```

### Agent Info

```bash
curl http://localhost:3847/api/agents/agent-1?project_path=/path/to/project
```

## Messaging

### Send Message

```bash
curl -X POST http://localhost:3847/api/mail/send \
  -H "Content-Type: application/json" \
  -d '{
    "project_path": "/path/to/project",
    "sender_name": "agent-1",
    "to": ["agent-2"],
    "subject": "Auth module complete",
    "body_md": "## Summary\nAuth implementation is done.\n\n## Files changed\n- src/auth/*",
    "importance": "normal",
    "ack_required": false
  }'
```

### Check Inbox

```bash
curl "http://localhost:3847/api/mail/inbox?project_path=/path/to/project&agent_name=agent-1"
```

### Reply to Message

```bash
curl -X POST http://localhost:3847/api/mail/reply \
  -H "Content-Type: application/json" \
  -d '{
    "project_path": "/path/to/project",
    "message_id": 123,
    "sender_name": "agent-2",
    "body_md": "Thanks! I'\''ll start on the API integration."
  }'
```

### Acknowledge Message

```bash
curl -X POST http://localhost:3847/api/mail/ack \
  -H "Content-Type: application/json" \
  -d '{
    "project_path": "/path/to/project",
    "agent_name": "agent-2",
    "message_id": 123
  }'
```

### Search Messages

```bash
curl "http://localhost:3847/api/mail/search?project_path=/path/to/project&query=authentication"
```

## File Reservations

Prevent conflicts when multiple agents edit files.

### Reserve Files

```bash
curl -X POST http://localhost:3847/api/files/reserve \
  -H "Content-Type: application/json" \
  -d '{
    "project_path": "/path/to/project",
    "agent_name": "agent-1",
    "paths": ["src/auth/*.ts", "src/config.ts"],
    "exclusive": true,
    "reason": "Implementing authentication",
    "ttl_seconds": 3600
  }'
```

### Check Reservations

```bash
curl "http://localhost:3847/api/files/reservations?project_path=/path/to/project"
```

### Release Files

```bash
curl -X POST http://localhost:3847/api/files/release \
  -H "Content-Type: application/json" \
  -d '{
    "project_path": "/path/to/project",
    "agent_name": "agent-1",
    "paths": ["src/auth/*.ts"]
  }'
```

## Thread Management

### Get Thread Summary

```bash
curl "http://localhost:3847/api/mail/thread/THREAD_ID/summary?project_path=/path/to/project"
```

### Thread Operations

Threads are automatically created when replying to messages.

## Coordination Patterns

### Task Handoff

```markdown
Agent 1 completes task:
1. Reserve output files
2. Complete work
3. Send message to Agent 2 with handoff details
4. Release file reservations

Agent 2 receives:
1. Get inbox
2. Reserve input files
3. Continue work
4. Acknowledge receipt
```

### Parallel Work

```markdown
Coordinator:
1. Reserve coordination files
2. Send tasks to agents
3. Wait for completion messages
4. Merge results

Workers:
1. Reserve assigned files
2. Complete task
3. Send completion message
4. Release files
```

### Review Request

```markdown
Author:
1. Complete code
2. Send review request to reviewer agents
3. Wait for feedback

Reviewers:
1. Get inbox
2. Review code (read-only, no reservation needed)
3. Send feedback message
```

## Health Check

```bash
curl http://localhost:3847/api/health
```

## Message Importance Levels

| Level | Use Case |
|-------|----------|
| `low` | FYI, status updates |
| `normal` | Standard communication |
| `high` | Needs attention soon |
| `urgent` | Blocking, needs immediate response |

## Best Practices

1. **Reserve before editing** - Prevent conflicts
2. **Use meaningful subjects** - Easy inbox scanning
3. **Acknowledge important** - Confirm receipt when `ack_required`
4. **Release promptly** - Don't hold reservations unnecessarily
5. **Use threads** - Keep related messages together
6. **Check inbox regularly** - Don't miss messages
7. **Handoff cleanly** - Include all needed context
