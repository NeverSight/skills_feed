---
name: build-router
description: |
  Unified router for development, infrastructure, and documentation tasks.
  Absorbs development-router + infrastructure-router + documentation-router.
---

# Build Router (Unified)

**Tier**: unified
**Absorbs**: development-router + infrastructure-router + documentation-router
**Purpose**: All creation/building tasks (code, configs, docs)

## Triggers
```yaml
patterns:
  - build, implement, create, develop
  - frontend, backend, fullstack, API
  - mcp, server, hook, deploy
  - document, readme, explain, changelog
  - terminal, TUI, CLI interface
```

## Build Domains

### Frontend Development
```yaml
triggers: [UI, UX, component, styling, React, Vue, Svelte]
agent: frontend-engineer
skills:
  - frontend-ui-ux (active)
  - component patterns
  - accessibility (WCAG)
  - responsive design
```

### Backend Development
```yaml
triggers: [API, server, database, authentication]
patterns:
  - RESTful API design
  - GraphQL schemas
  - Database modeling
  - Authentication/authorization
```

### Infrastructure
```yaml
triggers: [MCP, hook, config, deploy, tooling]
skills:
  - mcp-builder (db/skill-db)
  - hook development
  - configuration management
workflows:
  - MCP server: Research → Implement → Review → Evaluate
```

### Documentation
```yaml
triggers: [document, readme, explain, changelog, API docs]
agent: document-writer
patterns:
  - README creation
  - API documentation
  - Code comments
  - Changelogs
```

## Workflow Integration
```yaml
standard_flow:
  1. Analyze requirements
  2. Plan implementation
  3. Build incrementally
  4. Test and validate
  5. Document

sc_commands:
  - sc:implement → Guided implementation
  - sc:build → Build workflow
  - sc:document → Documentation
```

## Build Tool Detection

```yaml
package_managers:
  package.json: pnpm | npm | yarn | bun
  pyproject.toml: uv | poetry | pip
  Cargo.toml: cargo
  go.mod: go

build_commands:
  typescript: "pnpm build" | "npm run build" | "bun build"
  python: "uv run python -m build" | "poetry build"
  rust: "cargo build --release"

test_runners:
  typescript: vitest | jest | playwright
  python: pytest
  rust: cargo test

linting:
  typescript: eslint | prettier | biome
  python: ruff | black | mypy
```

## Decision Tree

```
Build/Create Request
    │
    ├── Frontend?
    │   ├── TUI/terminal? → terminal skill
    │   ├── Component? → frontend-engineer agent
    │   └── Feature → sc:implement
    │
    ├── Backend?
    │   ├── API design? → sc:design
    │   └── Implementation → sc:build
    │
    ├── Infrastructure?
    │   ├── MCP server? → mcp-builder skill
    │   ├── Hooks? → hookify skill
    │   └── Config → component skill
    │
    └── Documentation?
        ├── README → document-writer agent
        ├── API docs → sc:document
        └── Changelog → create-release-note
```

## References
- Original development-router: ~/.claude/db/skills/routers/development-router/
- Original infrastructure-router: ~/.claude/db/skills/routers/infrastructure-router/
- Original documentation-router: ~/.claude/db/skills/routers/documentation-router/
