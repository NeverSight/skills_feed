---
name: langfuse-session-list
description: List Langfuse sessions. Use when checking user sessions, analyzing conversation flows, or monitoring session activity.
license: MIT
compatibility: Node.js 18+ (native fetch required)
metadata:
  author: neuradex
  category: observability
allowed-tools:
  - Bash(npx tsx *scripts/langfuse-session-list.ts*)
---

# Langfuse Session List

Display the latest sessions.

## Setup

Set the following environment variables before use:

| Variable | Required | Description |
|----------|----------|-------------|
| `LANGFUSE_PUBLIC_KEY` | Yes | Langfuse public key |
| `LANGFUSE_SECRET_KEY` | Yes | Langfuse secret key |
| `LANGFUSE_HOST` or `LANGFUSE_BASE_URL` | No | Langfuse host URL (default: `https://us.cloud.langfuse.com`) |

## When to Use

- Checking the session list
- Analyzing conversation flows
- "Show me the recent sessions"
- "Check session activity"

## Commands

### 1. Get Session List

Get the latest 20 sessions:
```bash
npx tsx scripts/langfuse-session-list.ts
```

Specify the number of sessions:
```bash
npx tsx scripts/langfuse-session-list.ts --limit=50
```

## Output Example

```
Langfuse Sessions
=================

Created At          Session ID                                         Trace Count
-------------------------------------------------------------------------------------
2025-01-15 10:30:45 session-abc-123-456-789                            15
2025-01-15 10:28:12 session-def-234-567-890                            8
2025-01-15 10:25:33 session-ghi-345-678-901                            3

Showing 3 of 456 sessions
```

## Fields

| Field | Description |
|-------|-------------|
| Created At | Session creation timestamp |
| Session ID | Session identifier |
| Trace Count | Number of traces in the session |

## What is a Session?

A session groups multiple traces together.
- 1 conversation thread = 1 session
- All traces within a session are associated
- You can filter traces by session ID
