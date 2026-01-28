---
name: opencode-expert
description: This skill provides comprehensive guidance for using OpenCode, the open-source AI coding agent. Use this skill when working with OpenCode CLI commands, keyboard shortcuts, agents (build/plan), slash commands, tools, skills, MCP servers, or configuration. Automatically triggered when OpenCode-specific questions or tasks are detected.
---

# OpenCode Expert

Comprehensive guide for OpenCode - the open-source AI coding agent.

## Quick Reference

| Task | Command/Action |
|------|----------------|
| Start TUI | `opencode` |
| Continue session | `opencode -c` or `opencode --continue` |
| Run non-interactive | `opencode run "message"` |
| Start headless server | `opencode serve` |
| Web interface | `opencode web` |
| Switch agent | `Tab` key |
| File search | `@` then type filename |
| Undo changes | `/undo` |
| Redo changes | `/redo` |
| Share conversation | `/share` |
| Initialize project | `/init` |
| Configure API keys | `/connect` |

## Agents

OpenCode has two primary agents, switchable with `Tab`:

### Build Agent (Default)
- Full access to all tools
- Can edit files, run commands, make changes
- Use for active development work

### Plan Agent
- Read-only mode for analysis and exploration
- File edits and bash commands require approval (`ask` mode)
- Use for reviewing implementation strategy before changes

### Subagents

Invoke subagents with `@` mention:

- **@general** - Complex research and multi-step tasks with full tool access
- **@explore** - Fast read-only codebase searches and code questions

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Tab` | Switch between Build and Plan agents |
| `@` | Fuzzy file search |
| `Ctrl+C` | Cancel current operation |

## Slash Commands

| Command | Description |
|---------|-------------|
| `/connect` | Configure LLM provider API keys |
| `/init` | Initialize project and create `AGENTS.md` |
| `/undo` | Revert recent changes (stackable) |
| `/redo` | Restore undone changes |
| `/share` | Create shareable conversation link |

## CLI Commands

### Interactive Mode

```bash
# Start TUI in current directory
opencode

# Start in specific project
opencode /path/to/project

# Continue previous session
opencode --continue
opencode -c

# Use specific session
opencode --session <id>
opencode -s <id>

# Start with specific model
opencode --model <model>
opencode -m <model>

# Start with specific agent
opencode --agent build
opencode --agent plan
```

### Non-Interactive Mode

```bash
# Run single prompt
opencode run "Fix the bug in auth.py"

# Run with file attachment
opencode run "Review this" --file README.md
opencode run "Review this" -f README.md

# Run and share result
opencode run "Explain this code" --share

# Run specific command
opencode run --command "npm test"
```

### Server Mode

```bash
# Start headless API server
opencode serve

# With custom port
opencode serve --port 3000

# With mDNS discovery
opencode serve --mdns

# Web interface
opencode web
```

### Management Commands

```bash
# Authentication
opencode auth login
opencode auth list
opencode auth logout

# Models
opencode models              # List available models
opencode models --refresh    # Refresh model cache

# Agents
opencode agent create        # Create custom agent
opencode agent list          # List agents

# MCP servers
opencode mcp add <server>
opencode mcp list
opencode mcp auth
opencode mcp debug

# Sessions
opencode session list
opencode session list -n 10  # Last 10 sessions

# Statistics
opencode stats
opencode stats --days 7
opencode stats --tools
opencode stats --models

# Export/Import
opencode export <sessionID>
opencode import <file>

# Upgrade
opencode upgrade
opencode upgrade <version>
```

## Built-in Tools

OpenCode provides these tools to agents:

| Tool | Description |
|------|-------------|
| **read** | Read file contents with optional line ranges |
| **write** | Create new files or overwrite existing |
| **edit** | Modify files using exact string replacements |
| **patch** | Apply patch files |
| **grep** | Search file contents with regex |
| **glob** | Find files by pattern (`**/*.js`) |
| **list** | List files and directories |
| **bash** | Execute shell commands |
| **lsp** | Language Server Protocol integration (experimental) |
| **todowrite** | Create/update task lists |
| **todoread** | Read current todo state |
| **skill** | Load skill files into conversation |
| **webfetch** | Fetch and read web pages |
| **question** | Ask user clarifying questions |

## Skills

### File Locations

Skills are discovered from (in order):

1. `.opencode/skills/<name>/SKILL.md` (project)
2. `~/.config/opencode/skills/<name>/SKILL.md` (global)
3. `.claude/skills/<name>/SKILL.md` (Claude-compatible project)
4. `~/.claude/skills/<name>/SKILL.md` (Claude-compatible global)

### Skill Format

```markdown
---
name: my-skill
description: Description of what this skill does and when to use it.
---

# Skill Content

Instructions and documentation here...
```

### Name Rules

- Lowercase alphanumeric with single hyphens
- Cannot start/end with hyphens
- No consecutive hyphens (`--`)
- Must match directory name

## Configuration

### Config Locations

- Project: `.opencode/` or `opencode.json`
- Global: `~/.config/opencode/`

### Environment Variables

| Variable | Description |
|----------|-------------|
| `OPENCODE_CONFIG` | Custom config path |
| `OPENCODE_PERMISSION` | Permission mode |
| `OPENCODE_SERVER_PASSWORD` | Server auth password |
| `OPENCODE_DISABLE_AUTOUPDATE` | Disable auto-updates |
| `OPENCODE_EXPERIMENTAL` | Enable experimental features |
| `OPENCODE_ENABLE_EXA` | Enable Exa search |

### Custom Agents

Create agents via `opencode agent create` or define in:
- `opencode.json`
- `~/.config/opencode/agents/`
- `.opencode/agents/`

Agent config options: description, temperature, model, tool permissions, system prompts.

## Best Practices

### Use Plan Mode First
Switch to Plan agent (`Tab`) to review implementation strategy before making changes.

### File References
Use `@filename` to fuzzy search and reference files in prompts.

### Undo Stack
Use `/undo` liberally - changes are stackable and reversible with `/redo`.

### Session Management
Use `--continue` or `-c` to resume previous sessions and maintain context.

## References

For detailed documentation, see:
- `references/cli.md` - Complete CLI reference
- `references/tools.md` - Tool details and permissions
- `references/agents.md` - Agent configuration guide
