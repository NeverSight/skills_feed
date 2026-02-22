---
name: langfuse-prompt-list
description: List all Langfuse prompts with their labels and versions. Use when checking available prompts, verifying label assignments, or getting an overview of prompt status.
license: MIT
compatibility: Node.js 18+ (native fetch required)
metadata:
  author: neuradex
  category: observability
allowed-tools:
  - Bash(npx tsx *scripts/langfuse-prompt-list.ts*)
---

# Langfuse Prompt List

List all registered prompts and their label status.

## Setup

Set the following environment variables before use:

| Variable | Required | Description |
|----------|----------|-------------|
| `LANGFUSE_PUBLIC_KEY` | Yes | Langfuse public key |
| `LANGFUSE_SECRET_KEY` | Yes | Langfuse secret key |
| `LANGFUSE_HOST` or `LANGFUSE_BASE_URL` | No | Langfuse host URL (default: `https://us.cloud.langfuse.com`) |

## When to Use

- Checking the prompt list
- Verifying label assignments
- "What prompts are available?"

## Commands

### Get Prompt List

```bash
npx tsx scripts/langfuse-prompt-list.ts
```

## Output Example

```
Langfuse Prompts
================

Name                                         Labels                             Version
-------------------------------------------------------------------------------------------------------------
answer-evaluation                            development                        v1
chat-system                                  development, production            v2
librarian-system                             development                        v1
thread-title                                 (none)                             v1

Total: 16 prompts
```

## Label Status

| Status | Description |
|--------|-------------|
| `development` only | In development, not released to production |
| `development, production` | Released to production |
| No labels | Initial state, needs label assignment |
