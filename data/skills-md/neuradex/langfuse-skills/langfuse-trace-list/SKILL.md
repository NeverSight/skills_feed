---
name: langfuse-trace-list
description: List Langfuse traces with filtering options. Use when checking recent LLM calls, debugging issues, or monitoring costs.
license: MIT
compatibility: Node.js 18+ (native fetch required)
metadata:
  author: neuradex
  category: observability
allowed-tools:
  - Bash(npx tsx *scripts/langfuse-trace-list.ts*)
---

# Langfuse Trace List

Display the latest traces with filtering options.

## Setup

Set the following environment variables before use:

| Variable | Required | Description |
|----------|----------|-------------|
| `LANGFUSE_PUBLIC_KEY` | Yes | Langfuse public key |
| `LANGFUSE_SECRET_KEY` | Yes | Langfuse secret key |
| `LANGFUSE_HOST` or `LANGFUSE_BASE_URL` | No | Langfuse host URL (default: `https://us.cloud.langfuse.com`) |

## When to Use

- Checking the trace list
- Debugging LLM calls
- "Show me recent traces"
- "Check traces for a specific user"

## Commands

### 1. Get Trace List

Get the latest 20 traces:
```bash
npx tsx scripts/langfuse-trace-list.ts
```

Specify the number of traces:
```bash
npx tsx scripts/langfuse-trace-list.ts --limit=50
```

### 2. Filter Options

```bash
# Filter by trace name
npx tsx scripts/langfuse-trace-list.ts --name=librarian/chat

# Filter by user ID
npx tsx scripts/langfuse-trace-list.ts --user=user-123

# Filter by session ID
npx tsx scripts/langfuse-trace-list.ts --session=session-abc

# Filter by environment
npx tsx scripts/langfuse-trace-list.ts --env=production

# Combine multiple filters
npx tsx scripts/langfuse-trace-list.ts --name=chat --env=production --limit=100
```

## Output Example

```
Langfuse Traces
===============

Timestamp           Name                               User                Session        Cost      ID
----------------------------------------------------------------------------------------------------------------------------------
2025-01-15 10:30:45 librarian/chat                     user-123            session-abc    $0.0150   abc123...
2025-01-15 10:28:12 knowledge-builder/extract          user-456            session-def    $0.0080   def456...
2025-01-15 10:25:33 chat/respond                       user-789            -              $0.0045   ghi789...

Showing 3 of 1234 traces
```

## Fields

| Field | Description |
|-------|-------------|
| Timestamp | Trace creation timestamp |
| Name | Trace name (feature/action format) |
| User | User ID |
| Session | Session ID |
| Cost | Estimated cost |
| ID | Trace ID (for viewing details) |
