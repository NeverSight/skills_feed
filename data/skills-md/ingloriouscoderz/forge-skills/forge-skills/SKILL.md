---
name: forge-skills
description: Ecosystem guide for building web apps and 2D games with Inglorious Forge packages. Use when selecting packages, combining @inglorious modules, or implementing architecture with @inglorious/store, @inglorious/web, @inglorious/engine, @inglorious/ssx, and related tooling.
---

# Forge Skills

Use this file as the routing entry point for the Inglorious Forge skill set. Load only the specific files in `skills/` that match the user request.

## Workflow

1. Identify the user goal (state management, web UI, realtime sync, game loop, scaffolding, charts, or tooling).
2. Select the minimum number of files from `skills/` needed to answer or implement the request.
3. Prefer package-specific guidance over generic assumptions.
4. For multi-package tasks, combine only the relevant skill files.

## Skills Map

### [@inglorious/utils](skills/utils.md)

Use for utility functions and algorithmic helpers.

- Math, vector operations, trigonometry, random helpers
- Physics helpers (velocity, acceleration, friction)
- Functional helpers (composition, piping)
- Data structures and algorithms

### [@inglorious/store](skills/store.md)

Use for entity-based state management.

- Event-driven handlers and deterministic event queues
- Middleware and testing utilities
- Redux-compatible API and DevTools integration
- Multiplayer-friendly patterns

### [@inglorious/server](skills/server.md)

Use for realtime server patterns.

- Store-backed server architecture
- Entity and event synchronization over WebSockets

### [@inglorious/react-store](skills/react-store.md)

Use for React integration with `@inglorious/store`.

- Provider setup and simplified hooks
- `useEntity` and `useNotify` patterns

### [@inglorious/web](skills/web.md)

Use for web UI architecture with `@inglorious/store` and `lit-html`.

- `render(entity, api)` patterns
- Whole-tree re-rendering with efficient DOM updates
- Built-in form, table, list, select, and router modules
- Testing patterns

### [@inglorious/charts](skills/charts.md)

Use for SVG chart construction.

- Declarative and composable chart primitives
- Configuration-driven chart behavior
- SSR-friendly chart rendering

### [@inglorious/ssx](skills/ssx.md)

Use for static site generation and hydration workflows.

- Development server with HMR
- Vite-based build and bundling
- Markdown, LaTeX math, and Mermaid support
- SEO support (sitemaps, manifests, metadata)
- Fast hydration with `@lit-labs/ssr`

### [@inglorious/engine](skills/engine.md)

Use for functional 2D game loop architecture.

- Frame-based `update(entity, dt)` handlers
- Entity pool middleware for high-frequency updates
- Optional IngloriousScript vector operators via Babel

## Tooling & Integration

- **[JSX Vite Plugin](skills/vite-plugin-jsx.md):** Use JSX syntax instead of `lit-html` templates.
- **[Vue Vite Plugin](skills/vite-plugin-vue.md):** Use Vue-like template syntax instead of `lit-html`.
- **[Create App](skills/create-app.md):** Scaffold Inglorious Web applications.
- **[Create Game](skills/create-game.md):** Scaffold Inglorious Engine games.
