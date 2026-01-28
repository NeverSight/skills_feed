---
name: infrastructure-router
description: Routes infrastructure, MCP, and tooling tasks. Triggers on mcp, server, deploy, orchestrate, pipeline, tools, docker, ci/cd, hook, config, setup.
---

# Infrastructure Router

Routes infrastructure, MCP development, and tooling tasks.

## Subcategories

### MCP Development
```yaml
triggers: [mcp, model-context-protocol, server, tool-registration]
skills:
  - mcp-builder: MCP server development guide
  - component: Claude Code components
```

### Tooling / CLI
```yaml
triggers: [cli, tool, script, automation, batch]
skills:
  - terminal: Terminal UI design
  - ccs: Claude Code Spawner delegation
  - ccs-delegation: Auto-delegation patterns
```

### Hooks / Configuration
```yaml
triggers: [hook, config, setup, settings, plugin]
skills:
  - hookify: Hook creation from behaviors
  - component: Component generation
```

### Orchestration
```yaml
triggers: [orchestrate, pipeline, workflow, multi-agent, coordinate]
skills:
  - agent: Agentic reasoning framework
  - mcp-skillset-workflows: Multi-skill orchestration
```

## Routing Decision Tree

```
infrastructure request
    │
    ├── MCP development?
    │   ├── Server creation? → mcp-builder
    │   └── Component? → component
    │
    ├── CLI/Tooling?
    │   ├── Terminal UI? → terminal
    │   └── Delegation? → ccs
    │
    ├── Hooks/Config?
    │   ├── Hook creation? → hookify
    │   └── Settings? → component
    │
    └── Orchestration?
        ├── Multi-agent? → agent
        └── Workflows → mcp-skillset-workflows
```

## Managed Skills

| Skill | Purpose | Trigger |
|-------|---------|---------|
| mcp-builder | MCP server guide | "MCP", "server" |
| component | CC components | "command", "agent" |
| terminal | TUI design | "terminal", "CLI" |
| ccs | Claude spawner | "delegate", "spawn" |
| hookify | Hook creation | "hook", "prevent" |
| agent | Agentic framework | "orchestrate", "agent" |
