---
name: ai-context-writer
description: Create and update ai-context.md files that document modules for AI assistants. Use when adding documentation for packages, apps, or external references that should be discoverable via /modules commands.
---

# AI Context Writer Skill

Use this skill when creating or updating `ai-context.md` files that document modules in the codebase. These files are indexed by the context-crawler and surfaced via `/modules`, `/module`, and `/module-search` commands.

## File Location

Context files must be named exactly `ai-context.md` and placed at the root of the module:

```
packages/my-package/ai-context.md    # Internal module
apps/my-app/ai-context.md            # Internal module
.context/external-lib/ai-context.md  # External reference (submodule)
```

## Required Structure

### Frontmatter (YAML)

```yaml
---
path: packages/my-package
summary: One-line description mentioning purpose and key technologies
tags: [effect, http-client, sdk-wrapper]
---
```

**Frontmatter Fields:**
- `path` - Module identifier (relative path from repo root)
- `summary` - Single sentence, concise description for module listings
- `tags` - Optional categorization for search (technologies, domains)

### Markdown Body Sections

```markdown
# Module Name

High-level overview paragraph explaining the module's purpose.

## Architecture

┌──────────────────┐
│    Component     │
└──────────────────┘
        │
        ▼
┌──────────────────┐
│     Service      │
└──────────────────┘

Brief explanation of the architecture diagram.

## Core Modules

| Module | Purpose |
|--------|---------|
| `Service.ts` | Main service implementation |
| `Client.ts` | HTTP client wrapper |

## Usage Patterns

### Basic Usage

```typescript
import * as MyModule from "@/packages/my-package"
import { Effect } from "effect"

const program = Effect.gen(function* () {
  const service = yield* MyModule.Service
  return yield* service.doThing()
})
```

## Key Patterns

### Pattern Name

Description of when and why to use this pattern.

```typescript
// Example code
```

## Design Decisions

**AD-1: Decision Title**
Explanation of the decision and trade-offs.

**AD-2: Another Decision**
Why this approach was chosen over alternatives.

## Dependencies

- `effect` - Core Effect library
- `@effect/platform` - Platform abstractions

## Spec Reference

- [specs/my-feature/DESIGN.md](../specs/my-feature/DESIGN.md)
```

## Section Guidelines

### Architecture Diagram

Use simple ASCII box-and-arrow diagrams:

```
┌──────────────┐     ┌──────────────┐
│   Service    │────▶│    Client    │
└──────────────┘     └──────────────┘
        │
        ▼
┌──────────────┐
│   Repository │
└──────────────┘
```

Characters: `┌ ┐ └ ┘ │ ─ ▼ ▲ ◀ ▶ ────▶`

### Core Modules Table

Quick reference for key files:

```markdown
| Module | Purpose |
|--------|---------|
| `ParallelClient.ts` | HTTP client with Effect integration |
| `ParallelRun.ts` | Async task execution |
| `Errors.ts` | Tagged error types |
```

### Usage Patterns

Always include:
- Full imports with namespace pattern (`import * as X`)
- Effect.gen for effectful code
- Layer construction if services are involved

```typescript
import * as MyService from "@/packages/my-service"
import { Effect, Layer } from "effect"

const program = Effect.gen(function* () {
  const svc = yield* MyService.Service
  return yield* svc.operation()
})

const live = program.pipe(
  Effect.provide(MyService.Live)
)
```

### Design Decisions

Use `AD-N` format for traceability:

```markdown
**AD-1: Use Effect.gen over flatMap chains**
Effect.gen provides cleaner syntax and better stack traces. The generator pattern
makes sequential operations readable without callback nesting.

**AD-2: Schema.TaggedStruct for all domain types**
Automatic discriminator and Data equality support. Enables pattern matching
with Match.typeTags.
```

### Dependencies

List external packages the module depends on:

```markdown
## Dependencies

- `effect` - Core Effect types and functions
- `@effect/platform` - FileSystem, HttpClient, Terminal
- `@effect/schema` - Runtime validation and serialization
```

## Summary Writing

The summary is critical - it appears in `/modules` listings.

**Good summaries:**
- "Effect wrapper for Parallel AI SDK - web search, content extraction, and async task runs"
- "React frontend with Effect-Atom state management and TanStack Router"
- "SQLite-backed workflow engine for durable execution patterns"

**Bad summaries:**
- "A module for doing stuff" (too vague)
- "This is the main package that handles various functionality" (no specifics)

**Summary formula:**
`[Primary purpose] - [key feature 1], [key feature 2], and [key feature 3]`

## Discovery and Indexing

Context files are indexed by `context-crawler.ts`:

1. Recursively finds all `ai-context.md` files
2. Extracts frontmatter (path, summary, tags)
3. Falls back to first paragraph if no summary
4. Excludes `node_modules`, `.git`, `dist`, `build`, `.turbo`

### Module Classification

- **Internal**: Local `ai-context.md` files in packages/apps
- **External**: Submodules from `.gitmodules` (may lack ai-context.md)

External modules without context files show: `(grep for implementation details)`

## Commands for Discovery

```bash
# List all modules with summaries
/modules

# Get full content of specific module
/module packages/parallel

# Search modules by pattern
/module-search http
```

## Complete Example

```markdown
---
path: packages/parallel
summary: Effect wrapper for Parallel AI SDK - web search, content extraction, and async task runs
tags: [effect, sdk-wrapper, parallel-ai, http-client]
---

# Parallel SDK Effect Wrapper

Effect-native wrapper for the Parallel AI SDK. Injects Effect's HttpClient as the
fetch implementation, providing typed errors, deferred computation patterns, and
composable layer construction.

## Architecture

┌─────────────────────────────────────────────────────────────────┐
│                         User Code                                │
│                    (Effect programs)                             │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      ParallelClient                              │
│    ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐    │
│    │   search()   │  │  extract()   │  │   createRun()    │    │
│    └──────────────┘  └──────────────┘  └──────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Effect HttpClient                             │
│              (injected via Layer.provide)                        │
└─────────────────────────────────────────────────────────────────┘

## Core Modules

| Module | Purpose |
|--------|---------|
| `ParallelClient.ts` | Service interface with Effect operations |
| `ParallelClientLive.ts` | Live implementation using HttpClient |
| `ParallelRun.ts` | Async run execution with polling |
| `Errors.ts` | Tagged error types for failure handling |

## Usage Patterns

### Basic Search

```typescript
import * as Parallel from "@/packages/parallel"
import { Effect } from "effect"

const program = Effect.gen(function* () {
  const client = yield* Parallel.ParallelClient
  const results = yield* client.search({ query: "Effect TypeScript" })
  return results
})

const runnable = program.pipe(
  Effect.provide(Parallel.Live)
)
```

### Error Handling

```typescript
import * as Parallel from "@/packages/parallel"
import { Effect } from "effect"

const safe = program.pipe(
  Effect.catchTag("ParallelApiError", (e) =>
    Effect.succeed({ error: e.message })
  ),
  Effect.catchTag("ParallelNetworkError", () =>
    Effect.succeed({ error: "Network unavailable" })
  )
)
```

## Design Decisions

**AD-1: Inject HttpClient via Layer**
Enables testing with mock HTTP responses. Production uses FetchHttpClient,
tests use a custom client that returns canned responses.

**AD-2: Tagged errors for all failure modes**
ParallelApiError, ParallelNetworkError, ParallelTimeoutError. Enables
precise error handling with catchTag.

## Dependencies

- `effect` - Core runtime
- `@effect/platform` - HttpClient abstraction
- `parallel-sdk` - Underlying SDK (via .context/parallel-sdk-typescript)

## Spec Reference

- [specs/parallel/DESIGN.md](../../specs/parallel/DESIGN.md)
```

## When to Use This Skill

- Adding a new package or app that should be discoverable
- Documenting an existing module for AI assistants
- Creating context for external libraries added as submodules
- Updating documentation after significant refactoring
- Ensuring modules appear in `/modules` listings

## Key Principles

1. **Frontmatter is required** - path and summary enable indexing
2. **Summary is critical** - appears in all module listings
3. **Architecture diagrams** - visual overview aids understanding
4. **Usage patterns with imports** - show how to actually use the module
5. **Design decisions** - explain why, not just what
6. **Code examples compile** - include all necessary imports
7. **Namespace imports** - always `import * as X from`
