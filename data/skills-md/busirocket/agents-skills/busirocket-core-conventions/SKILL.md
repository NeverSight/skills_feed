---
name: busirocket-core-conventions
description:
  General engineering conventions optimized for AI agents. Use when creating or
  refactoring codebases and you need strict file discipline, clear module
  boundaries, naming/layout rules, and anti-pattern avoidance.
metadata:
  author: cristiandeluxe
  version: "1.0.0"
---

# Core Conventions

Reusable, project-agnostic conventions designed to keep codebases scalable and
easy for AI agents to navigate.

## When to Use

Use this skill when:

- Starting a new feature and deciding where code should live
- Refactoring to improve maintainability
- Enforcing “one-thing-per-file” discipline
- Establishing naming/layout conventions and boundary rules

## Non-Negotiables (MUST)

- Keep **many small, focused files** with explicit boundaries.
- **One exported symbol per file** for your own modules
  (component/hook/function/type).
- **No barrel/index files** (e.g. `index.ts`) that hide dependencies.
- **No inline types** outside `types/`.
- **No helper functions inside components or hooks**; extract to `utils/`.
- Avoid adding new dependencies for trivial helpers unless explicitly approved.

## Placement / Boundaries

- Route/pages: `app/**`
- Reusable UI: `components/<area>/...`
- Orchestration (state/effects): `hooks/<area>/useXxx.ts`
- Pure logic: `utils/<area>/xxx.ts`
- External boundaries (network/DB/auth/storage): `services/<area>/xxx.ts`
- Shared shapes: `types/<area>/Xxx.ts`

## Rules

### Core Principles

- `core-agent-defaults` - Agent behavior defaults (small changes, ask questions,
  avoid dependencies)
- `core-code-style` - Code style guidelines (English-only, pure functions, avoid
  nesting)
- `core-repo-hygiene` - Repository hygiene (no barrel files, one responsibility,
  thin handlers)

### Boundaries & Placement

- `core-boundaries-decision-tree` - Decision tree for where code belongs (app,
  components, hooks, utils, services, types)
- `core-boundaries-hard-rules` - Hard rules for boundaries (one export, no
  inline types, no helpers in components)

### Naming & Layout

- `core-naming-folder-layout` - Folder structure conventions
- `core-naming-file-naming` - File naming conventions (PascalCase, camelCase,
  kebab-case)
- `core-naming-exports` - Export conventions (default vs named, Next.js
  exceptions)
- `core-naming-imports` - Import conventions (no barrel files, relative vs
  aliases)

### Services vs Utils

- `core-services-vs-utils-contract` - When to use services/ vs utils/
- `core-services-vs-utils-api` - API guidance for services and utils
- `core-services-vs-utils-route-handlers` - Route handler requirements

### Anti-Patterns

- `core-anti-patterns-file-structure` - File structure anti-patterns (multiple
  exports, barrel files, misc modules)
- `core-anti-patterns-types` - Type anti-patterns (inline types, huge type
  files)
- `core-anti-patterns-react` - React anti-patterns (fetching in components,
  helpers in components)
- `core-anti-patterns-app-router` - App Router anti-patterns (fat handlers,
  unvalidated input)
- `core-anti-patterns-dependencies` - Dependency anti-patterns (trivial helpers)
- `core-anti-patterns-vite-browser` - Vite/Browser runtime anti-patterns
  (process.env, Node globals)

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/core-agent-defaults.md
rules/core-boundaries-decision-tree.md
rules/core-naming-folder-layout.md
```

Each rule file contains:

- Brief explanation of why it matters
- Code examples (correct and incorrect patterns)
- Additional context and best practices
