---
name: opencode
description: Expert guide for working with opencode.ai - TUI commands, CLI operations, custom commands, agents, tools, skills system, and AGENTS.md configuration
license: MIT
compatibility: opencode
metadata:
  version: 1.0.0
  author: opencode
  primary_use: agent_assistant
---

## When to Use This Skill

Load this skill when the user:
- Asks about OpenCode installation, setup, or configuration
- Mentions opencode.ai commands like /init, /connect, /undo
- Needs help with AGENTS.md or custom commands
- Asks about TUI features, mode switching, or tools
- Wants to create agents, skills, or custom commands
- References opencode configuration (opencode.json)
- Is working on a project with .opencode directory

This skill provides specialized knowledge for OpenCode workflows.

# OpenCode Agent Guide

## Quick Start

### Installation
```bash
# Recommended: Install script
curl -fsSL https://opencode.ai/install | bash

# Or use npm
npm install -g opencode-ai

# Or use Homebrew (macOS/Linux)
brew install anomalyco/tap/opencode
```
[Source: https://opencode.ai/docs]

### Setup
```bash
# Navigate to your project
cd /path/to/project

# Start OpenCode
opencode

# Configure your AI provider
/connect

# Initialize project (creates AGENTS.md)
/init
```
[Source: https://opencode.ai/docs]

**Essential commands**: /init, /help, /exit, /new, /sessions [Source: https://opencode.ai/docs/tui]

**File references**: `@path/to/file` - fuzzy file search and content injection [Source: https://opencode.ai/docs]

**Bash commands**: `!npm install` - execute shell commands directly [Source: https://opencode.ai/docs]

**Undo/redo**: /undo (Git-based), /redo restore changes [Source: https://opencode.ai/docs/tui]

## Core Usage Patterns

### File References
```
@filename                    # Fuzzy search single file
@src/components/*.tsx       # Pattern matching
@path/to/file.ts:42         # Line-specific reference
```
Use @ for fuzzy file matching. Agent reads file content automatically [Source: https://opencode.ai/docs]

### Bash Commands
```
!npm install                # Run npm commands
!git status && git diff     # Chain commands
!`git log --oneline -5`     # Output injection in custom commands
```
Execute shell commands. Use workdir parameter instead of cd patterns [Source: https://opencode.ai/docs/tools]

### Agent Switching
- Tab key: Switch between Build mode (default) and Plan mode [Source: https://opencode.ai/docs/agents]
- @subagent: Invoke subagents (General, Explore) via @mention [Source: https://opencode.ai/docs/agents]
- Ctrl+x: Default leader key for shortcuts [Source: https://opencode.ai/docs/tui]

## TUI Commands

**Session**: /sessions, /new, /exit, /share, /unshare [Source: https://opencode.ai/docs/tui]

**Configuration**: /connect, /models, /editor, /themes [Source: https://opencode.ai/docs/tui]

**View**: /compact, /details, /thinking [Source: https://opencode.ai/docs/tui]

**Git**: /undo, /redo, /export, /import [Source: https://opencode.ai/docs/tui]

**Help**: /help, /init (creates AGENTS.md) [Source: https://opencode.ai/docs/tui]

## CLI Usage

Default: `opencode` starts TUI. Non-interactive: `opencode run <prompt>` [Source: https://opencode.ai/docs/cli]

**Commands**: agent, attach, auth, github, mcp, models, run, serve, session, stats, export, import, web [Source: https://opencode.ai/docs/cli]

**Global flags**: --help, --version, --print-logs, --log-level [Source: https://opencode.ai/docs/cli]

**Environment**: OPENCODE_AUTO_SHARE, OPENCODE_CONFIG, OPENCODE_DISABLE_CLAUDE_CODE [Source: https://opencode.ai/docs/cli]

## Configuration

**Files**: `.opencode/opencode.json` (project), `~/.config/opencode/config.json` (global) [Source: https://opencode.ai/docs]

**Basic opencode.json structure**:
```json
{
  "agents": {
    "default": {
      "model": "provider/model",
      "temperature": 0.7
    }
  },
  "tools": {
    "bash": {
      "permissions": "allow"
    }
  }
}
```
[Source: https://opencode.ai/docs/agents]

**Initial setup**: /connect command configures connection [Source: https://opencode.ai/docs]

**Agent config**: tools, permissions, model, temperature [Source: https://opencode.ai/docs/agents]

**Claude compatibility**: Reads CLAUDE.md when AGENTS.md not present [Source: https://opencode.ai/docs/rules]

For advanced configuration (remote config, plugins, formatters), see [CONFIGURATION.md](CONFIGURATION.md)

## Custom Commands

**Location**: `.opencode/commands/` or `~/.config/opencode/commands/` [Source: https://opencode.ai/docs/commands]

**Format**: Markdown with YAML frontmatter [Source: https://opencode.ai/docs/commands]

```markdown
---
description: Run tests with coverage
agent: Build
template: |
  !npm run test -- --coverage && !npm run lint
  $ARGUMENTS
---
# Test Runner

Run tests and lint. Arguments passed directly.
```

**Arguments**: $ARGUMENTS (all), $1, $2, $3 (positional) [Source: https://opencode.ai/docs/commands]

**Shell injection**: `!`command`` - injects output into command template [Source: https://opencode.ai/docs/commands]

**File references**: @filename in commands [Source: https://opencode.ai/docs/commands]

**Config options**: template, description, agent, subtask, model [Source: https://opencode.ai/docs/commands]

## Agents

**Modes**: Build (default), Plan - switch with Tab key [Source: https://opencode.ai/docs/agents]

**Subagents**: General, Explore - invoke via @mention [Source: https://opencode.ai/docs/agents]

**Configuration**: JSON or Markdown files in `.opencode/agents/` [Source: https://opencode.ai/docs/agents]

**Options**: description, temperature, max_steps, disable, prompt, model, tools, permissions, mode, hidden, task_permissions, color, top_p [Source: https://opencode.ai/docs/agents]

**Creation**: `opencode agent create <name>` [Source: https://opencode.ai/docs/agents]

**Switching**: Tab key cycles between Build mode and Plan mode; @subagent invokes subagents [Source: https://opencode.ai/docs/agents]

## Tools

**Built-in tools**:
- `bash` - Execute shell commands
- `edit` - Edit files in place
- `write` - Write new files
- `read` - Read file contents
- `grep` - Search file contents
- `glob` - Find files by pattern
- `list` - List directory contents
- `lsp` - Language Server Protocol (experimental)
- `patch` - Apply patches
- `skill` - Load agent skills
- `todowrite/todoread` - Task management
- `webfetch` - Fetch web content
- `question` - Interactive prompts
[Source: https://opencode.ai/docs/tools]

**Permissions**: allow, deny, ask per tool [Source: https://opencode.ai/docs/tools]

**Custom tools**: Configure in opencode.json [Source: https://opencode.ai/docs/tools]

**MCP servers**: External tool integrations [Source: https://opencode.ai/docs/tools]

**Ignore patterns**: .ignore file in project root [Source: https://opencode.ai/docs/tools]

**Best practices**: Use workdir param instead of cd patterns. Batch independent tool calls. Prefer grep over bash grep [Source: https://opencode.ai/docs/tools]

## Skills System

**Format**: SKILL.md with YAML frontmatter [Source: https://opencode.ai/docs/skills]

**Locations**: `.opencode/skills/<name>/`, `~/.config/opencode/skills/<name>/`, `.claude/skills/<name>/`, `~/.claude/skills/<name>/` [Source: https://opencode.ai/docs/skills]

**Frontmatter**: name (req), description (req), license (opt), compatibility (opt), metadata (opt) [Source: https://opencode.ai/docs/skills]

**Name validation**: 1-64 chars, lowercase alphanumeric with hyphens, regex: `^[a-z0-9]+(-[a-z0-9]+)*$` [Source: https://opencode.ai/docs/skills]

**Description**: 1-1024 characters [Source: https://opencode.ai/docs/skills]

**Discovery**: Walks up from CWD to git worktree, loads from global configs [Source: https://opencode.ai/docs/skills]

**Loading**: skill tool loads by name [Source: https://opencode.ai/docs/skills]

**Permissions**: pattern-based allow/deny/ask [Source: https://opencode.ai/docs/skills]

## Rules and AGENTS.md

**AGENTS.md**: Project root file created by /init command [Source: https://opencode.ai/docs/rules]

**Types**: Project (local), Global (~/.config/opencode/AGENTS.md), Claude Code Compatible [Source: https://opencode.ai/docs/rules]

**Custom instructions**: instructions field in opencode.json [Source: https://opencode.ai/docs/rules]

**External refs**: Reference external files from AGENTS.md [Source: https://opencode.ai/docs/rules]

**Precedence**: local AGENTS.md > global AGENTS.md > Claude CLAUDE.md [Source: https://opencode.ai/docs/rules]

## Common Workflows

### Add a New Feature
```
1. Switch to Plan mode (Tab key)
2. Plan: "Add user authentication to /settings route. Check @src/notes.ts for reference"
3. Review and iterate on the plan
4. Switch to Build mode (Tab key)
5. Build: "Go ahead and implement"
6. Test: !npm test
7. Commit: !git add . && git commit -m "feat: add authentication"
```

### Debug an Issue
```
1. Identify error location: @src/api/error.ts:42
2. Check related files: @src/components/*
3. Run with debug output: !npm run dev -- --verbose
4. Add breakpoints based on error
5. Test fix: !npm run test -- --watch
6. If issue persists: /undo to revert, refine prompt
```

### Git Workflow
```
!git status
@path/to/changed/file.ts
!git add . && git commit -m "message"
```
Use /undo to revert changes via Git, /redo to restore [Source: https://opencode.ai/docs/tui]

### Multi-Mode Task
```
@plan-agent: Create implementation plan
Tab to Build mode, execute plan
```

### Custom Command Workflow
```
Create command in .opencode/commands/
Use @file references for context
Use $ARGUMENTS for user input
Test with /help command
```
