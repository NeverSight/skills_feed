---
name: creating-plugins
description: Guide for creating Claude Code plugins with commands, agents, skills, hooks, and MCP servers. Use when the user wants to create a new plugin, add plugin components (commands, agents, hooks), set up a plugin marketplace, or needs help with plugin.json configuration.
---

# Plugin Creator

Create Claude Code plugins to extend functionality with custom commands, agents, skills, hooks, and MCP servers.

## Plugin Creation Workflow

### 1. Gather Requirements

Ask the user:
- What functionality should the plugin provide?
- Which components are needed? (commands, agents, hooks, MCP servers, skills)
- Who is the target audience? (personal, team, public)

### 2. Create Plugin Structure

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json      # Required
├── commands/            # Optional: slash commands
├── agents/              # Optional: sub-agents
├── skills/              # Optional: agent skills
├── hooks/               # Optional: event handlers
└── .mcp.json           # Optional: MCP servers
```

### 3. Write plugin.json

Minimal example:
```json
{
  "name": "my-plugin",
  "description": "Brief description",
  "version": "1.0.0",
  "author": {"name": "Author Name"}
}
```

### 4. Add Components

Based on user requirements, add:
- **Commands**: See [commands.md](references/commands.md) for slash command format
- **Agents**: See [agents.md](references/agents.md) for agent definition format
- **Hooks**: See [hooks.md](references/hooks.md) for event handler configuration
- **MCP Servers**: See [mcp-servers.md](references/mcp-servers.md) for server configuration

### 5. Test Locally

Create a test marketplace:
```bash
mkdir test-marketplace/.claude-plugin
```

Create `test-marketplace/.claude-plugin/marketplace.json`:
```json
{
  "name": "test-marketplace",
  "owner": {"name": "Developer"},
  "plugins": [{"name": "my-plugin", "source": "./my-plugin"}]
}
```

Test commands:
```
/plugin marketplace add ./test-marketplace
/plugin install my-plugin@test-marketplace
```

## Quick Reference

### Command File (commands/hello.md)
```markdown
---
description: Greet the user
---
# Hello Command
Greet the user warmly.
```

### Agent File (agents/reviewer.md)
```markdown
---
description: Code review specialist
capabilities: ["review", "suggestions"]
---
# Reviewer
Review code for quality and best practices.
```

### Hooks (hooks/hooks.json)
```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Write|Edit",
      "hooks": [{"type": "command", "command": "prettier --write $CLAUDE_FILE_PATH"}]
    }]
  }
}
```

## References

### Plugin Development
- [Plugins Guide](references/plugins-guide.md) - Complete plugin creation guide
- [Plugins Reference](references/plugins-reference.md) - Technical schemas and configurations
- [Plugin Structure](references/plugin-structure.md) - Directory layout and plugin.json schema
- [Marketplace](references/marketplace.md) - Plugin distribution

### Plugin Components
- [Commands](references/commands.md) - Slash command format
- [Agents](references/agents.md) - Sub-agent definitions
- [Hooks](references/hooks.md) - Event handlers
- [MCP Servers](references/mcp-servers.md) - External tool integration

### Skills Development
- [Skills Overview](references/skills-overview.md) - What skills are and how they work
- [Skills Best Practices](references/skills-best-practices.md) - Writing effective skills
- [Skills Schema](references/skills-schema.md) - SKILL.md format and validation
