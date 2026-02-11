---
name: langfuse-session-view
description: View Langfuse session details with all traces. Use when analyzing conversation flows, checking session costs, or debugging multi-turn interactions.
license: MIT
compatibility: Node.js 18+ (native fetch required)
metadata:
  author: neuradex
  category: observability
allowed-tools:
  - Bash(npx tsx *scripts/langfuse-session-view.ts*)
---

# Langfuse Session View

Display detailed information and all traces for a specific session.

## Setup

Set the following environment variables before use:

| Variable | Required | Description |
|----------|----------|-------------|
| `LANGFUSE_PUBLIC_KEY` | Yes | Langfuse public key |
| `LANGFUSE_SECRET_KEY` | Yes | Langfuse secret key |
| `LANGFUSE_HOST` or `LANGFUSE_BASE_URL` | No | Langfuse host URL (default: `https://us.cloud.langfuse.com`) |

## When to Use

- Checking specific session details
- Analyzing conversation flows
- "Show me all traces for this session"
- Investigating by session ID

## Commands

### 1. Get Session Details

```bash
npx tsx scripts/langfuse-session-view.ts <sessionId>
```

### 2. Specify Trace Count

```bash
npx tsx scripts/langfuse-session-view.ts <sessionId> --limit=100
```

### 3. JSON Output

```bash
npx tsx scripts/langfuse-session-view.ts <sessionId> --json
```

## Output Example

```
Langfuse Session Detail
=======================

Session ID: se:9ed69537-5952-40ee-9d98-5e1197fc5726
Created:    2025-01-15 10:30:45
Project:    project-123

Summary:
  Total Traces: 74
  Total Cost:   $0.1234
  Avg Latency:  856ms

Trace Types:
  chunk-extraction: 70
  chunking: 3
  source-parse: 1

Traces (50 of 74):
----------------------------------------------------------------------------------------------------
Timestamp           Name                                    Latency     Cost        ID
----------------------------------------------------------------------------------------------------
2025-01-15 10:30:45 chunk-extraction:abc123                 1234ms      $0.0150     abc123...
2025-01-15 10:30:46 chunk-extraction:def456                 856ms       $0.0080     def456...
```

## Fields

| Field | Description |
|-------|-------------|
| Session ID | Session identifier |
| Created | Creation timestamp |
| Project | Project ID |
| Total Traces | Total number of traces in the session |
| Total Cost | Estimated total cost for the session |
| Avg Latency | Average processing time |
| Trace Types | Trace count by name |
