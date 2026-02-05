---
name: unknown-patterns
description: Learn unfamiliar implementation patterns and fill in missing pieces when building features in a specific environment (e.g., data fetching in a particular runtime). Use when you need to discover or confirm patterns for an unimplemented area; implementation uses erudita and osgrep.
---

# Erudita Patterns

## Workflow

- Install docs into the project: `erudita install <package...>`
- Install from config: `erudita install --mode copy` (uses `erudita.json` and prunes stale entries)

## Search

- Semantic search across installed docs:
  - `osgrep search "keywords" .erudita`

## Tips

- Use `erudita fetch --deps <dev|prod|all>` to cache docs for project dependencies.
- Use `erudita install --mode <link|copy>` to control `.erudita/` install mode.
