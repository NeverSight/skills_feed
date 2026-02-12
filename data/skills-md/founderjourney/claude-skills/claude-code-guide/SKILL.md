---
name: claude-code-guide
description: Comprehensive guide and skill for Claude Code CLI. Installation, configuration, commands, keyboard shortcuts, MCP integration, sub-agents, and best practices.
original_source: https://github.com/zebbern/claude-code-guide
author: zebbern
license: MIT
---

# Claude Code Guide

Comprehensive reference for Claude Code, Anthropic's official CLI tool for AI-assisted development.

## When to Use This Skill

- Learning Claude Code features
- Configuring Claude Code settings
- Understanding keyboard shortcuts
- Setting up MCP servers
- Creating custom sub-agents
- Troubleshooting issues
- Optimizing workflows

## Installation

### macOS/Linux
```bash
npm install -g @anthropic-ai/claude-code
```

### Windows
```powershell
npm install -g @anthropic-ai/claude-code
```

### Verify Installation
```bash
claude --version
```

## Authentication

### API Key Setup
```bash
# Set API key
export ANTHROPIC_API_KEY="your-key"

# Or via CLI
claude auth login
```

### Check Auth Status
```bash
claude auth status
```

## Basic Commands

| Command | Description |
|---------|-------------|
| `claude` | Start interactive session |
| `claude "prompt"` | One-shot query |
| `claude -c` | Continue last conversation |
| `claude --help` | Show help |

## Keyboard Shortcuts

### Navigation
| Shortcut | Action |
|----------|--------|
| `Ctrl+C` | Cancel current operation |
| `Ctrl+D` | Exit Claude Code |
| `Ctrl+L` | Clear screen |
| `↑/↓` | Navigate history |

### Editing
| Shortcut | Action |
|----------|--------|
| `Ctrl+A` | Move to line start |
| `Ctrl+E` | Move to line end |
| `Ctrl+W` | Delete word backward |
| `Ctrl+U` | Delete to line start |

### Special
| Shortcut | Action |
|----------|--------|
| `Tab` | Autocomplete |
| `Shift+Enter` | Multi-line input |
| `Escape` | Cancel current input |

## Slash Commands

| Command | Description |
|---------|-------------|
| `/help` | Show help |
| `/clear` | Clear conversation |
| `/compact` | Toggle compact mode |
| `/model` | Change model |
| `/cost` | Show token usage |
| `/bug` | Report a bug |

## Configuration

### Config File Location
```
~/.claude/settings.json
```

### Settings Options
```json
{
  "model": "claude-sonnet-4-20250514",
  "theme": "dark",
  "editor": "vscode",
  "autoSave": true,
  "permissions": {
    "allowFileWrite": true,
    "allowBash": true,
    "allowNetwork": true
  }
}
```

### Project Settings
Create `.claude/settings.json` in project root:
```json
{
  "systemPrompt": "You are helping with a Node.js project...",
  "allowedPaths": ["src/", "tests/"],
  "blockedPaths": ["node_modules/", ".env"]
}
```

## MCP (Model Context Protocol)

### What is MCP?
MCP allows Claude to interact with external tools and services through standardized servers.

### MCP Configuration
```json
// ~/.claude/mcp.json
{
  "servers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-server-filesystem"],
      "env": {
        "ALLOWED_PATHS": "/home/user/projects"
      }
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

### Available MCP Servers
- `@anthropic-ai/mcp-server-filesystem` - File operations
- `@anthropic-ai/mcp-server-github` - GitHub integration
- `@anthropic-ai/mcp-server-postgres` - Database queries
- `@anthropic-ai/mcp-server-puppeteer` - Browser automation

## Sub-Agents

### Creating Custom Agents
Create in `~/.claude/agents/`:

```markdown
---
name: code-reviewer
description: Reviews code for best practices
model: claude-sonnet-4-20250514
---

# Code Review Agent

You are a senior code reviewer. When reviewing code:

1. Check for security issues
2. Verify error handling
3. Assess readability
4. Suggest improvements

Be constructive and educational in feedback.
```

### Using Agents
```bash
# List agents
claude agents list

# Use specific agent
claude --agent code-reviewer
```

## Skills

### Installing Skills
```bash
# From marketplace
claude skills install skill-name

# From GitHub
claude skills install github:user/repo
```

### Skill Location
```
~/.claude/skills/skill-name/SKILL.md
```

### Creating Skills
See [skill-creator](../skill-creator/) skill.

## Hooks

### Pre/Post Hooks
```json
// .claude/hooks.json
{
  "preCommand": ["echo 'Starting...'"],
  "postCommand": ["echo 'Done!'"],
  "preFileWrite": ["backup.sh"],
  "postFileWrite": ["format.sh"]
}
```

## Permissions

### Permission Levels
- `ask` - Prompt for each action
- `allow` - Allow without prompting
- `deny` - Block action

### Configure Permissions
```json
{
  "permissions": {
    "file:write": "ask",
    "bash:execute": "ask",
    "network:fetch": "allow"
  }
}
```

## Performance Tips

1. **Use `.claudeignore`**: Exclude large directories
2. **Project Context**: Set in `.claude/` folder
3. **Compact Mode**: For faster responses
4. **Specific Prompts**: Be precise in requests
5. **File References**: Use `@filename` syntax

## Troubleshooting

### Common Issues

**"Command not found"**
```bash
# Reinstall
npm install -g @anthropic-ai/claude-code
# Check PATH
echo $PATH
```

**"Authentication failed"**
```bash
# Re-authenticate
claude auth logout
claude auth login
```

**"Rate limited"**
- Wait and retry
- Check API usage dashboard
- Consider upgrading plan

### Debug Mode
```bash
claude --debug
```

### Logs Location
```
~/.claude/logs/
```

## Best Practices

1. **Clear Context**: Start fresh for unrelated tasks
2. **Incremental Requests**: Break large tasks
3. **Review Changes**: Always review file modifications
4. **Use Git**: Commit before major operations
5. **Custom Instructions**: Set project-specific prompts

## Resources

- [Official Docs](https://docs.anthropic.com/claude-code)
- [GitHub Issues](https://github.com/anthropics/claude-code/issues)
- [Community Discord](https://discord.gg/anthropic)

## Credits

Guide created by [zebbern](https://github.com/zebbern/claude-code-guide). Licensed under MIT.
