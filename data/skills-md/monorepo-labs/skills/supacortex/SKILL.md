---
name: supacortex
description: Personal memory layer — save bookmarks and conversation summaries using the Supacortex CLI. Use when the user says "save to cortex", "save to supacortex", "save this session", or asks to recall past conversations.
allowed-tools: Bash(scx bookmarks *) Bash(scx conversation *)
compatibility: Requires the scx CLI to be installed and authenticated (scx login)
metadata:
  author: monorepo-labs
  version: "1.1"
---

# Supacortex — CLI Skill

Supacortex is a personal memory layer. Two CLI commands: bookmarks and conversations.

## Setup

```bash
npm i -g @supacortex/cli
scx login
```

## 1. Bookmarks (`scx bookmarks`)

Save and search bookmarks (links, YouTube videos).

### Commands

#### List bookmarks

```bash
scx bookmarks list [--search "<query>"] [--type <tweet|link|youtube>] [--limit <n>] [--offset <n>] [--pretty]
```

#### Add a bookmark

```bash
scx bookmarks add <url> [--pretty]
```

#### Get a bookmark by ID

```bash
scx bookmarks get <id> [--pretty]
```

#### Delete a bookmark

```bash
scx bookmarks delete <id> [--pretty]
```

### When to use bookmarks

- User asks to save a link or YouTube video
- User wants to search their saved content
- When you need to reference previously saved URLs

## 2. Conversations (`scx conversation`)

Save summaries of AI chat sessions. Every conversation has a **tier** that determines its depth.

### Tiers

| Tier | When to use | Content format |
|------|-------------|----------------|
| `brief` | Throwaway queries, quick lookups | Single sentence: "Asked about JSON parsing in Bun" |
| `summary` | Most working sessions | Markdown — 3-8 bullet points covering what was discussed, decided, and found |
| `detailed` | Deep sessions with architectural decisions, research findings | Markdown — full structured document with headings, reasoning, code snippets, follow-ups |

### Commands

#### Save a conversation

```bash
scx conversation add "<content>" --tier <brief|summary|detailed> [--title "<title>"] [--metadata '<json>'] [--pretty]
```

The `--tier` flag is required. It maps to memory types: `conversation_brief`, `conversation_summary`, `conversation_detailed`.

**Examples:**

```bash
# Brief — one sentence
scx conversation add "Helped debug CORS issue in Hono API" --tier brief

# Summary — bullet points
scx conversation add "- Set up memory table with tsvector search
- Added triggers for auto search vector generation
- Created API routes for CRUD
- Decided on hybrid schema approach" \
  --tier summary \
  --title "Memory system setup" \
  --metadata '{"source": "claude-code"}'

# Detailed — full document
scx conversation add "## Memory Architecture Decision..." --tier detailed --title "Memory layer brainstorm"
```

#### List conversations

```bash
scx conversation list [--search "<query>"] [--tier <brief|summary|detailed>] [--limit <n>] [--offset <n>] [--pretty]
```

#### Get a conversation by ID

```bash
scx conversation get <id> [--pretty]
```

#### Update a conversation

```bash
scx conversation update <id> [--title "<title>"] [--content "<content>"] [--tier <tier>] [--metadata '<json>'] [--pretty]
```

#### Delete a conversation

```bash
scx conversation delete <id> [--pretty]
```

### When to save conversations

Save when the user says:
- "save to cortex" / "save to supacortex"
- "save this session" / "remember this"
- "log this conversation"

### When to recall conversations

Pull past conversations when the user says:
- "check my conversation about X"
- "pull the X conversation"
- "get the summary for X"
- "what did we work on last time?"

## Metadata

Metadata is freeform JSON passed via `--metadata`. The AI decides what to store. Common fields:

- `source` — where this was captured ("claude-code", "chatgpt", "opencode")
- `tags` — array of topic tags
- `project` — which project the conversation was about (e.g. "supacortex", "supalytics")
- `category` — topic area: "project", "life", "general", "learning", "work"

## Consistent verbs across all commands

Both commands (`bookmarks`, `conversation`) support: `list`, `add`, `get`, `delete`.

`conversation` also supports: `update`.

All commands output JSON by default (optimized for AI agents). Use `--pretty` for human-readable output.
