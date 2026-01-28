---
name: development-router
description: Routes development tasks to frontend, backend, or fullstack skills. Triggers on build, implement, code, create, feature, component, UI, API, server, database, docker, deploy.
---

# Development Router

Routes development-related tasks to appropriate specialized skills.

## Subcategories

### Frontend Development
```yaml
triggers: [UI, component, React, Vue, Svelte, CSS, Tailwind, design-system, terminal-ui, responsive]
skills:
  - terminal: TUI/CLI interfaces with high design quality
  - component: Claude Code configuration components
  - sc:implement: Feature implementation with persona activation
```

### Backend Development
```yaml
triggers: [api, server, database, auth, REST, GraphQL, microservice, endpoint]
skills:
  - sc:build: Build and compile projects
  - sc:design: System architecture and API design
  - mcp-builder: MCP server development
```

### Fullstack / Infrastructure
```yaml
triggers: [fullstack, monorepo, deployment, docker, ci/cd, pipeline]
skills:
  - sc:workflow: Implementation workflows from PRDs
  - sc:task: Complex task execution with persistence
```

## Routing Decision Tree

```
development request
    │
    ├── UI/component keywords?
    │   ├── TUI/terminal? → @skills/terminal
    │   ├── Claude component? → @skills/component
    │   └── general UI → sc:implement
    │
    ├── API/server keywords?
    │   ├── MCP server? → @skills/mcp-builder
    │   ├── architecture? → sc:design
    │   └── implementation → sc:build
    │
    └── deployment/infra?
        └── sc:workflow
```

## Managed Skills

| Skill | Purpose | Trigger |
|-------|---------|---------|
| terminal | Production-grade TUI | "terminal UI", "CLI tool" |
| component | CC config components | "command", "subagent", "skill" |
| sc:implement | Feature implementation | "implement", "build feature" |
| sc:build | Build/compile | "build", "compile", "package" |
| sc:design | Architecture | "design", "architecture" |
| mcp-builder | MCP servers | "MCP", "model context protocol" |
| sc:workflow | PRD workflows | "workflow", "PRD" |
