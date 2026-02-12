---
name: persistent-memory
description: ALWAYS USE THIS SKILL when handling persistent memory in this workspace, including task-start memory recall, explicit "remember" instructions, storing durable preferences/facts, and retrieving prior context. This skill owns the local memory workflow and CLI for init/sync/search/add/recent/stats.
---

# Persistent Memory

Use this skill as the single memory system for this repository.

## Commands

Use either command style:
- `python3 .agents/skills/persistent-memory/scripts/memory.py <command>`
- `.agents/skills/persistent-memory/scripts/pmem <command>`

Supported commands:
- `init`
- `sync` (database-only health check)
- `cleanup-legacy`
- `backfill-embeddings --batch 500`
- `prune --source "<label>" [--older-than <days>]`
- `search "<query>" --limit 8`
- `add "<memory text>" --tags "<comma,tags>" --source "assistant"`
- `recent --limit 10`
- `stats`

## Required Workflow

1. Initialize memory in a fresh workspace:
- `pmem init`

2. At the start of substantial tasks:
- `pmem sync` (database-only health check)
- `pmem search "<topic keywords>" --limit 8`

3. When user explicitly says `remember` or when a durable preference/fact is learned:
- `pmem add "<memory text>" --tags "<tags>" --source "assistant"`

4. Before finalizing memory-sensitive work, verify recall state:
- `pmem stats`

## One-Time Migration (If Upgrading From Older Setup)

1. Remove legacy imported rows:
- `pmem cleanup-legacy`

2. Generate vectors for existing notes:
- `pmem backfill-embeddings`

## Storage Rules

- Store durable preferences, long-lived facts, stable workflows, and repeated constraints.
- Do not store noisy one-off transient details unless requested.
- Keep entries concise and specific.
- Prefer tags that improve retrieval quality (`preferences`, `calendar`, `comms`, `product`).

## Retrieval Rules

- Use targeted search queries instead of broad terms.
- Keep default `--limit` low unless deeper recall is needed.
- `search` automatically reinforces recalled entries by updating `hits` and `last_seen_at`.
- `hits` are analytics-oriented and not used as a direct ranking boost.
- Search uses hybrid retrieval: lexical + semantic.
- Semantic search tries `sqlite-vec` first and auto-falls back to Python cosine if needed.

## Bootstrapping and Recovery

- If `.memory/` is missing, run `pmem init`.
- `pmem sync` is a lightweight database-only check (no markdown import/export).
- If semantic mode degrades, run `pmem stats` to inspect `semantic_backend` and `embedding_coverage`.
- For command examples and quick troubleshooting, read `references/usage.md`.
