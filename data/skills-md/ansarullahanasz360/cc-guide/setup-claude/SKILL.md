---
name: setup-claude
description: Interactive Claude Code repository setup and optimization. Configures the complete ecosystem - skills, commands, subagents, hooks, rules, MCPs, and plugins. Invoke with /setup-claude init or /setup-claude audit.
user-invocable: true
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
  - Edit
  - Bash
  - AskUserQuestion
  - TodoWrite
---

# Claude Repository Setup System

You are an expert at configuring repositories for optimal Claude Code usage. You help users set up new projects from scratch or audit existing projects for improvements.

## Core Philosophy

1. **CLI-First**: Always prefer CLI tools over MCP (more token-efficient)
2. **Context Window is Precious**: Keep under 10 MCPs enabled, under 80 tools active
3. **Modular Configuration**: Rules in .claude/rules/, not one mega CLAUDE.md
4. **Subagent Delegation**: Scope subagents with limited tools for focused execution
5. **Progressive Automation**: Hooks for formatting, linting, reminders

## Mode Detection

When invoked, determine which mode to use:

1. **Explicit mode**: If the user specifies `init` or `audit`, use that mode
2. **Auto-detect mode**: Otherwise, analyze the current directory:
   - If `.claude/` directory exists OR `CLAUDE.md` exists → **audit mode**
   - If directory is empty or has minimal files (< 5 files) → **init mode**
   - If directory has code but no Claude config → **audit mode** (treat as existing project needing setup)

## Mode Routing

### Init Mode (New Repositories)
For setting up new or nearly-empty repositories from scratch.

Follow the workflow in: `workflows/init-new-repo.md`

**13 Phases:**
1. Environment & Global Tools Check
2. Project Scaffolding
3. Tech Stack Interview
4. CLI Discovery & Authentication ⭐
5. MCP Configuration (Context Window Aware) ⭐
6. Plugin Setup
7. Skills Installation
8. Subagent Configuration
9. Rules Configuration
10. Hooks Configuration
11. CLAUDE.md Generation
12. Ralph TUI Setup
13. Verification & Summary

### Audit Mode (Existing Repositories)
For analyzing and improving existing repositories.

Follow the workflow in: `workflows/audit-existing-repo.md`

**8 Phases:**
1. Environment Analysis
2. CLI Audit ⭐
3. Context Window Analysis ⭐
4. Gap Analysis
5. Recommendations Report
6. Interactive Fixes
7. Context Window Optimization
8. Summary & Verification

## Complete Ecosystem

The skill configures all of these:

```
~/.claude/                    # Global config (personal)
├── skills/                   # Broader workflow definitions
├── commands/                 # Quick executable prompts
├── agents/                   # Subagent definitions
├── rules/                    # Modular best practice .md files
├── settings.json             # Global hooks & permissions
└── CLAUDE.md                 # Global context

.claude/                      # Project-level config
├── skills/                   # Project-specific skills
├── commands/                 # Project-specific commands
├── agents/                   # Project subagents
├── rules/                    # Project rules
└── settings.json             # Project hooks

CLAUDE.md                     # Project context file (10 sections)
.mcp.json                     # MCP configuration
.ralph-tui/                   # Ralph TUI config
```

## Component Reference

When executing workflows, reference these components for detailed guidance:

| Component | Purpose |
|-----------|---------|
| `components/cli-discovery.md` | CLI-first service integration |
| `components/mcp-management.md` | MCP setup + context window management |
| `components/plugin-setup.md` | Essential plugins configuration |
| `components/subagent-setup.md` | Subagent templates and scoping |
| `components/rules-configuration.md` | Modular rules setup |
| `components/documentation-setup.md` | Context7 + web research guidance |
| `components/tools-installation.md` | Global tools setup |
| `components/skills-discovery.md` | Skill recommendation and installation |
| `components/hooks-configuration.md` | Hook patterns for automation |
| `components/claudemd-writing.md` | CLAUDE.md with all 10 sections |
| `components/folder-structure.md` | Project scaffolding templates |

## Reference Data

| Reference | Contents |
|-----------|----------|
| `reference/tech-stack-clis.md` | CLI tools by technology |
| `reference/mcp-servers.md` | MCP server configurations |
| `reference/essential-plugins.md` | Plugin recommendations |
| `reference/subagent-templates.md` | Common subagent patterns |
| `reference/hook-patterns.md` | Enhanced hook patterns |
| `reference/mandatory-skills.md` | Skills always installed (PRD, Agent Browser) |
| `reference/tech-stack-skills.md` | Skills mapped to frameworks |
| `reference/hook-templates.md` | Pre-built hook JSON configurations |

## Templates

| Template | Purpose |
|----------|---------|
| `templates/ralph-tui/config.toml` | Ralph TUI configuration |
| `templates/ralph-tui/prompt.hbs` | Ralph prompt template |
| `templates/subagents/*.md` | Subagent definitions |
| `templates/rules/*.md` | Rule templates |
| `templates/claude-md/complete-template.md` | Full CLAUDE.md template |

## Quick Start Examples

**New project:**
```
User: /setup-claude init
Claude: [Runs 13-phase init workflow]
```

**Existing project:**
```
User: /setup-claude audit
Claude: [Runs 8-phase audit workflow]
```

**Auto-detect:**
```
User: /setup-claude
Claude: [Detects mode based on directory contents]
```

## Important Notes

- Always use TodoWrite to track progress through phases
- Use Bash for tool installation and verification commands
- Use AskUserQuestion for all user choices (never assume)
- Create backup before modifying existing files
- Summarize changes at the end of each workflow
- **CLI-First**: Check for CLI before enabling MCP
- **Context Window**: Warn when MCPs exceed recommended limits
