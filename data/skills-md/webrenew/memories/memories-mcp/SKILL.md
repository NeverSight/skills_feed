---
name: memories-mcp
description: "MCP server integration for memories.sh — the persistent memory layer for AI agents. Use when: (1) Configuring the memories.sh MCP server for any client (Claude Code, Cursor, Windsurf, VS Code, v0, Claude Desktop, OpenCode, Factory), (2) Using MCP tools to store, search, or retrieve memories programmatically, (3) Understanding get_context vs search_memories vs list_memories, (4) Working with streaming memory tools for SSE content, (5) Troubleshooting MCP connection issues, (6) Choosing between cloud MCP (HTTP) and local MCP (stdio) transports."
---

# memories-mcp

Connect AI agents to the memories.sh memory layer via MCP (Model Context Protocol).

> **The CLI is the primary interface for memories.sh** — use `memories generate` to create native config files for each tool. The MCP server is a **fallback** for real-time access when static configs aren't enough. It's also the **best choice for browser-based agents** (v0, bolt.new, Lovable) where the CLI can't run.

## Quick Start

```bash
# Local stdio transport (most reliable)
memories serve

# HTTP/SSE transport (for web clients like v0)
memories serve --sse --port 3030

# Cloud-hosted (no local install needed)
# Endpoint: https://memories.sh/api/mcp
# Header: Authorization: Bearer YOUR_KEY
```

## Primary Tool: `get_context`

Always start with `get_context` — it returns active rules + relevant memories in one call:

```
get_context({ query: "authentication flow" })
→ ## Active Rules
→ - Always use TypeScript strict mode
→ ## Relevant to: "authentication flow"
→ 💡 DECISION (P) abc123: Chose JWT for stateless auth
```

Leave `query` empty to get just rules. Use `limit` to control memory count (default: 10).

## Tool Selection Guide

| Goal | Tool | When |
|------|------|------|
| Start a task | `get_context` | Beginning of any task — gets rules + relevant context |
| Save knowledge | `add_memory` | After learning something worth persisting |
| Find specific info | `search_memories` | Full-text search with prefix matching |
| Browse recent | `list_memories` | Explore what's stored, filter by type/tags |
| Get coding standards | `get_rules` | When you only need rules, not memories |
| Update a memory | `edit_memory` | Fix content, change type, update tags |
| Remove a memory | `forget_memory` | Soft-delete (recoverable) |
| Bulk remove memories | `bulk_forget_memories` | Filtered mass soft-delete by type, tags, age, pattern |
| Reclaim storage | `vacuum_memories` | Permanently purge all soft-deleted records |

## Memory Types

When using `add_memory`, pick the right type:
- **rule** — Coding standards, preferences, constraints (always returned by `get_context`)
- **decision** — Architectural choices with rationale
- **fact** — Project-specific knowledge (API limits, env vars, etc.)
- **note** — General notes (default)
- **skill** — Reusable agent workflows (use with `category` and `metadata`)

## Scopes

- **project** (default) — Scoped to current git repo, detected automatically
- **global** — Applies everywhere, set `global: true` in `add_memory`
- **project override** — Set `project_id: "github.com/org/repo"` in `add_memory` (or `start_memory_stream`) to force project scope when the MCP process is running outside that repo

Do not send both `global: true` and `project_id` in the same call.

## Streaming Memory Tools

For collecting content from SSE sources (v0 artifacts, streaming responses):

1. `start_memory_stream({ type?, tags?, global?, project_id? })` → returns `stream_id`
2. `append_memory_chunk({ stream_id, chunk })` (repeat for each piece)
3. `finalize_memory_stream({ stream_id })` → creates memory + triggers embedding
4. `cancel_memory_stream({ stream_id })` → discard if aborted

## MCP Resources

For clients that support MCP resources:

| URI | Content |
|-----|---------|
| `memories://rules` | All active rules as markdown |
| `memories://recent` | 20 most recent memories |
| `memories://project/{id}` | Memories for a specific project |

## Transport Options

| Transport | Use Case | Command |
|-----------|----------|---------|
| **stdio** | Claude Code, Cursor, local tools | `memories serve` |
| **HTTP/SSE** | v0, web-based agents, remote | `memories serve --sse --port 3030` |
| **Cloud** | No local install, cross-device | `https://memories.sh/api/mcp` + `Authorization: Bearer KEY` |

## Reference Files

- **Client setup configs**: See [references/setup.md](references/setup.md) for copy-paste configs for every supported client
- **Full tool reference**: See [references/tools.md](references/tools.md) for all parameters, return formats, and examples
