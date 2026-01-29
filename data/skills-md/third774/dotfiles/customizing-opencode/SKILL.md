---
name: customizing-opencode
description: Configure OpenCode via opencode.json, agents, commands, MCP servers, custom tools, plugins, themes, keybinds, and permissions. Use when setting up or modifying OpenCode configuration.
---

# Customizing OpenCode

Configure OpenCode behavior through config files, agents, commands, and extensions.

## Config File Locations

| Location | Path | Purpose |
|----------|------|---------|
| Global | `~/.config/opencode/opencode.json` | User-wide preferences |
| Project | `./opencode.json` | Project-specific settings |
| Custom | `$OPENCODE_CONFIG` env var | Override path |

**Precedence** (later overrides earlier): Remote `.well-known/opencode` < Global < Custom < Project

## Quick Reference

| Task | Where | Reference |
|------|-------|-----------|
| Set theme, model, autoupdate | `opencode.json` | [config-schema.md](references/config-schema.md) |
| Define specialized agents | `.opencode/agents/*.md` or config | [agents.md](references/agents.md) |
| Create slash commands | `.opencode/commands/*.md` or config | [commands.md](references/commands.md) |
| Add external tools via MCP | `opencode.json` `mcp` section | [mcp-servers.md](references/mcp-servers.md) |
| Write custom tool functions | `.opencode/tools/*.ts` | [custom-tools.md](references/custom-tools.md) |
| Extend with plugins/hooks | `.opencode/plugins/*.ts` or npm | [plugins.md](references/plugins.md) |
| Control tool access | `opencode.json` `permission` section | [permissions.md](references/permissions.md) |
| Customize keyboard shortcuts | `opencode.json` `keybinds` section | [keybinds.md](references/keybinds.md) |
| Change colors/appearance | `opencode.json` `theme` or custom JSON | [themes.md](references/themes.md) |

## Directory Structure

```
~/.config/opencode/           # Global config
├── opencode.json
├── AGENTS.md                 # Global rules
├── agents/                   # Global agents
├── commands/                 # Global commands
├── plugins/                  # Global plugins
├── skills/                   # Global skills
├── tools/                    # Global custom tools
└── themes/                   # Global custom themes

.opencode/                    # Project config (same structure)
├── agents/
├── commands/
├── plugins/
├── skills/
├── tools/
└── themes/
```

## When to Use What

| Need | Solution |
|------|----------|
| Change model/theme for all projects | Global `opencode.json` |
| Project-specific agent behavior | Project `.opencode/agents/` |
| Reusable prompt templates | Commands (`.opencode/commands/`) |
| External service integration | MCP servers |
| Custom logic the LLM can call | Custom tools |
| React to OpenCode events | Plugins |
| Restrict dangerous operations | Permissions |

## Variable Substitution

Use in any config value:

```jsonc
{
  "model": "{env:OPENCODE_MODEL}",           // Environment variable
  "instructions": ["{file:./rules.md}"]      // File contents
}
```

## Rules (AGENTS.md)

Project instructions loaded into LLM context:

| File | Scope |
|------|-------|
| `./AGENTS.md` | Project (traverses up to git root) |
| `~/.config/opencode/AGENTS.md` | Global |
| `instructions` array in config | Additional files/globs |

```jsonc
{
  "instructions": ["CONTRIBUTING.md", "docs/*.md"]
}
```

## Docs

Full documentation: https://opencode.ai/docs/config/
