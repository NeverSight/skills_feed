---
name: langfuse-trace-view
description: View Langfuse trace details. Use when checking specific trace input/output, debugging LLM calls, or analyzing costs.
license: MIT
compatibility: Node.js 18+ (native fetch required)
metadata:
  author: neuradex
  category: observability
allowed-tools:
  - Bash(npx tsx *scripts/langfuse-trace-view.ts*)
---

# Langfuse Trace View

Display detailed information for a specific trace.

## Setup

Set the following environment variables before use:

| Variable | Required | Description |
|----------|----------|-------------|
| `LANGFUSE_PUBLIC_KEY` | Yes | Langfuse public key |
| `LANGFUSE_SECRET_KEY` | Yes | Langfuse secret key |
| `LANGFUSE_HOST` or `LANGFUSE_BASE_URL` | No | Langfuse host URL (default: `https://us.cloud.langfuse.com`) |

## When to Use

- Checking specific trace details
- Viewing LLM input/output
- "Show me the details of this trace"
- Investigating by trace ID

## Commands

### 1. Get Trace Details

```bash
npx tsx scripts/langfuse-trace-view.ts <traceId>
```

### 2. JSON Output

```bash
npx tsx scripts/langfuse-trace-view.ts <traceId> --json
```

## Output Example

```
Langfuse Trace Detail
=====================

ID:        abc123-def456-ghi789
Name:      librarian/chat
Timestamp: 2025-01-15 10:30:45
User ID:   user-123
Session:   lb:session-456
Latency:   1234ms
Cost:      $0.0150
Tags:      env:production

Metadata:
{
  "projectId": "project-123",
  "organizationId": "org-456"
}

Input:
{
  "userMessage": "Search the knowledge base"
}

Output:
{
  "response": "Here are the search results..."
}

Observations (3):
--------------------------------------------------------------------------------

[GENERATION] llm-call
  Time: 10:30:46  Model: gpt-4o  Cost: $0.0120  Tokens: in:150 out:200
  Input: {"role": "user", ...}
  Output: Here are the search results...

[SPAN] tool-execution
  Time: 10:30:47  Model: -  Cost: -  Tokens: -
```

## Fields

| Field | Description |
|-------|-------------|
| ID | Trace ID |
| Name | Trace name |
| Timestamp | Creation timestamp |
| User ID | User ID |
| Session | Session ID |
| Latency | Processing time (ms) |
| Cost | Estimated cost |
| Tags | Tag list |
| Metadata | Metadata |
| Input | Trace input |
| Output | Trace output |
| Observations | Child spans (Generation, Span, etc.) |
