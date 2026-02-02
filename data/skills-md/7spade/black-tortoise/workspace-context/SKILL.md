---
name: workspace-context
description: Workspace context patterns for src/app/workspace, including workspace lifecycle, stable context signals, workspace switching, and event emission for other modules; use when changing workspace selection, hydration, or context providers.
---

# Workspace Context

## Intent
Provide a stable, read-only workspace context for the rest of the app, changeable only through explicit workspace actions.

## Context Rules
- Represent the active workspace as signals (workspaceId, workspace, membership/roles).
- Other modules read the context; they must not mutate it directly.

## Lifecycle
- Workspace switching is explicit and emits events for consumers to react.
- Keep hydration predictable: load workspace state once per workspaceId change and avoid redundant fetch loops.

## Boundaries
- Global UI state belongs to Shell; workspace is not a dumping ground for app chrome.
- Persist and publish changes in order (append-before-publish).

## Performance
- Keep context signals small and stable; avoid emitting new object identities unnecessarily.
- Convert integration streams to signals at the store boundary.
