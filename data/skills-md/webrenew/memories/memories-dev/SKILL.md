---
name: memories-dev
description: "Developer guide for contributing to and extending the memories.sh codebase. Use when: (1) Understanding the memories.sh architecture and how packages connect, (2) Adding new CLI commands or MCP tools, (3) Modifying the memory storage layer (SQLite/libSQL), (4) Working on the web dashboard (Next.js/Supabase), (5) Adding new generation targets for AI tools, (6) Extending cloud sync or embeddings functionality, (7) Debugging build, test, or deployment issues in the monorepo."
---

# memories-dev

Developer guide for contributing to the memories.sh monorepo.

## Project Structure

```
memories/
├── packages/
│   ├── cli/                  # @memories.sh/cli (npm package)
│   │   ├── src/
│   │   │   ├── commands/     # CLI commands (Commander.js)
│   │   │   ├── lib/          # Core: db, memory, auth, embeddings, git
│   │   │   └── mcp/          # MCP server (stdio + HTTP)
│   │   ├── tsup.config.ts    # Build config
│   │   └── package.json
│   └── web/                  # Next.js marketing + dashboard
│       ├── src/app/          # App Router pages + API routes
│       ├── src/components/   # UI components (shadcn/ui)
│       ├── src/lib/          # Auth, Stripe, Supabase, Turso
│       └── content/docs/     # Fumadocs documentation
├── supabase/                 # Database migrations
├── skills/                   # Distributable skills (this directory)
└── pnpm-workspace.yaml
```

## Architecture Overview

### Dependency Graph

```
db.ts (SQLite/libSQL, migrations, FTS5)
  ↓
memory.ts (CRUD, search, context, streaming)
  ↑          ↑
git.ts    embeddings.ts (Xenova/Transformers, cosine similarity)
  ↓
Commands ← auth.ts, turso.ts, config.ts, setup.ts
  ↓
MCP Server (stdio + StreamableHTTP transports)
```

### Key Lib Files

| File | Purpose |
|------|---------|
| `db.ts` | SQLite via libSQL. Schema migrations, FTS5 triggers, `getDb()` singleton |
| `memory.ts` | All memory operations: add, search, list, forget, update, getContext, getRules, streaming |
| `embeddings.ts` | Local embeddings via Xenova/Transformers. `generateEmbedding()`, cosine similarity |
| `git.ts` | `getProjectId()` — derives project ID from git remote URL |
| `auth.ts` | Cloud auth token storage, device code flow helpers |
| `turso.ts` | Turso embedded replica sync (cloud ↔ local) |
| `config.ts` | YAML config read/write (`~/.config/memories/`) |
| `setup.ts` | Tool detection (Cursor, Claude, Windsurf, VS Code), MCP config setup |
| `templates.ts` | Built-in memory templates (decision, error-fix, api-endpoint, etc.) |
| `ui.ts` | Terminal styling: chalk, figlet, gradient, boxen |

### Database Schema

SQLite with FTS5 full-text search:

- **memories** — Main table: id, content, type, tags, scope, project_id, created_at, updated_at, deleted_at
- **memories_fts** — FTS5 virtual table, synced via triggers
- **memory_embeddings** — Vector storage: memory_id, embedding (JSON float array), model
- **memory_links** — Bidirectional links: id1, id2, link_type
- **memory_history** — Version tracking: memory_id, version, content, tags, change_type

## Adding a New CLI Command

1. Create `packages/cli/src/commands/mycommand.ts`:

```typescript
import { Command } from "commander";

export const myCommand = new Command("mycommand")
  .description("What it does")
  .argument("<required>", "Description")
  .option("-f, --flag <value>", "Description", "default")
  .action(async (required, opts) => {
    // Use lib functions from ../lib/
    // Use ui.ts for styled output
  });
```

2. Register in `packages/cli/src/index.ts`:

```typescript
import { myCommand } from "./commands/mycommand.js";
program.addCommand(myCommand);
```

3. Add tests in `packages/cli/src/commands/mycommand.test.ts`.

## Adding a New MCP Tool

Edit `packages/cli/src/mcp/index.ts`:

```typescript
server.tool(
  "tool_name",
  "Description of what the tool does",
  {
    param: z.string().describe("Parameter description"),
  },
  async ({ param }) => {
    // Implementation
    return {
      content: [{ type: "text", text: "Result" }],
    };
  }
);
```

Parameters use Zod schemas. Return `{ isError: true }` for errors.

## Adding a New Generation Target

1. Add template to `packages/cli/src/lib/templates.ts`
2. Register in the generation targets map
3. Add detection in `packages/cli/src/lib/setup.ts`
4. Add docs page in `packages/web/content/docs/integrations/`

## Build & Test

```bash
pnpm build          # Build all packages
pnpm typecheck      # TypeScript checks
pnpm test           # Run all tests (vitest)

# CLI-specific
cd packages/cli
pnpm dev            # Watch mode (tsup)
pnpm test           # CLI tests only

# Web-specific
cd packages/web
pnpm dev            # Next.js dev server
pnpm build          # Production build
```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| CLI framework | Commander.js |
| Database | libSQL (SQLite-compatible) |
| Full-text search | FTS5 |
| Embeddings | Xenova/Transformers (local) |
| MCP SDK | @modelcontextprotocol/sdk |
| Build | tsup (CLI), Next.js (web) |
| Web framework | Next.js 15 (App Router) |
| Auth | Supabase Auth |
| Cloud sync | Turso embedded replicas |
| Payments | Stripe |
| Docs | Fumadocs |
| UI | shadcn/ui, Tailwind CSS v4 |
| Testing | Vitest |

## Reference Files

- **Architecture deep-dive**: See [references/architecture.md](references/architecture.md) for detailed module descriptions and data flow
