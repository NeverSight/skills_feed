---
name: claude-code-guide
description: |
  Use this agent when the user asks questions ("Can Claude...", "Does Claude...", "How do I...") about: (1) Claude Code (the CLI tool) - features, hooks, slash commands, MCP servers, settings, IDE integrations, keyboard shortcuts; (2) Claude Agent SDK - building custom agents; (3) Claude API (formerly Anthropic API) - API usage, tool use, Anthropic SDK usage. **IMPORTANT:** Before spawning a new agent, check if there is already a running or recently completed claude-code-guide agent that you can resume using the "resume" parameter.
allowed-tools:
  - Glob
  - Grep
  - Read
  - WebFetch
  - WebSearch
---

# Claude Code Guide

This skill provides comprehensive guidance for Claude Code - the agentic coding tool from Anthropic.

## What is Claude Code?

Claude Code is an **agentic coding assistant** that operates directly in your terminal. Unlike chat-based AI tools, Claude Code:

- **Sees your codebase**: Reads files, understands project structure, follows imports
- **Takes action**: Edits files, runs commands, creates commits, manages git workflows
- **Verifies results**: Runs tests, checks build output, validates changes
- **Learns context**: Remembers project conventions via CLAUDE.md files

## The Agentic Loop

Claude Code operates in a continuous **gather → act → verify** loop:

```
┌─────────────────────────────────────────────────────┐
│                   AGENTIC LOOP                       │
├─────────────────────────────────────────────────────┤
│  1. GATHER CONTEXT                                   │
│     • Read files, search code, explore structure     │
│     • Understand current state and requirements      │
│                                                      │
│  2. TAKE ACTION                                      │
│     • Edit files, run commands, create content       │
│     • May require permission for sensitive ops       │
│                                                      │
│  3. VERIFY RESULTS                                   │
│     • Check command output, run tests                │
│     • Validate changes meet requirements             │
│                                                      │
│  4. REPEAT or COMPLETE                               │
│     • Continue if more work needed                   │
│     • Report results when done                       │
└─────────────────────────────────────────────────────┘
```

**Read more**: `references/core/agentic-loop.md`

## Key Features Quick Reference

| Feature | Description | Learn More |
|---------|-------------|------------|
| **Tools** | File ops, search, bash, web access | `references/core/tools.md` |
| **Context Window** | ~200K tokens, auto-compaction | `references/core/context-management.md` |
| **CLAUDE.md** | Project-specific instructions | `references/configuration/memory.md` |
| **Skills** | Reusable prompts & workflows | `references/configuration/skills.md` |
| **Hooks** | Shell commands on events | `references/configuration/hooks.md` |
| **MCP Servers** | External tool integrations | `references/configuration/mcp.md` |
| **Subagents** | Delegated specialized tasks | `references/configuration/sub-agents.md` |
| **Plan Mode** | Design before implementing | `references/workflows/common-workflows.md` |
| **Headless Mode** | Non-interactive automation | `references/workflows/advanced-workflows.md` |

## Extension Points Comparison

Choose the right extension mechanism for your needs:

| Mechanism | Best For | Scope | Complexity |
|-----------|----------|-------|------------|
| **CLAUDE.md** | Project conventions, coding standards, context | Project | Low |
| **Skills** | Reusable prompts, workflows, templates | User/Project | Low-Medium |
| **Hooks** | Automation, validation, logging, side effects | User/Project | Medium |
| **MCP Servers** | External APIs, databases, custom tools | User/Project | Medium-High |
| **Subagents** | Specialized tasks, parallel work, isolation | User/Project | Medium |

### When to Use What

**Use CLAUDE.md when:**
- Defining coding standards ("use tabs, not spaces")
- Documenting project architecture
- Specifying test commands
- Setting up file organization rules

**Use Skills when:**
- Creating reusable workflows (/commit, /review)
- Building prompt templates with arguments
- Packaging documentation for reference
- Defining specialized behaviors

**Use Hooks when:**
- Running commands before/after actions
- Validating or blocking tool usage
- Logging activity
- Auto-formatting code on save

**Use MCP Servers when:**
- Connecting to external APIs (GitHub, Jira, databases)
- Adding custom tool capabilities
- Integrating with existing services
- Providing resources from external sources

**Use Subagents when:**
- Delegating specialized investigations
- Running parallel analysis tasks
- Isolating context for focused work
- Creating custom agent personas

## Navigation Guide

### Understanding How Claude Code Works
- **How does the agentic loop work?** → `references/core/agentic-loop.md`
- **What tools does Claude have?** → `references/core/tools.md`
- **How does context management work?** → `references/core/context-management.md`

### Configuration & Setup
- **How do I set up CLAUDE.md?** → `references/configuration/memory.md`
- **How do I create skills?** → `references/configuration/skills.md`
- **How do I configure hooks?** → `references/configuration/hooks.md`
- **How do I add MCP servers?** → `references/configuration/mcp.md`
- **How do I create subagents?** → `references/configuration/sub-agents.md`

### Workflows & Best Practices
- **Common tasks (exploration, debugging, PRs)** → `references/workflows/common-workflows.md`
- **Advanced patterns (parallel, CI/CD, headless)** → `references/workflows/advanced-workflows.md`
- **Best practices & tips** → `references/best-practices.md`

### CLI Reference
- **Commands, flags, and options** → `references/cli-reference.md`

## Quick Tips

### Effective Prompting
```
# Be specific about verification
"Add input validation to the signup form. Run the tests to verify."

# Provide context
"The auth system uses JWT tokens stored in httpOnly cookies.
Add a logout endpoint that clears the cookie."

# Request exploration first
"Explore how error handling works in this codebase, then
suggest improvements to the API error responses."
```

### Keyboard Shortcuts
| Key | Action |
|-----|--------|
| `Enter` | Send message (configurable) |
| `Esc` | Cancel current generation |
| `Ctrl+C` | Interrupt / Exit |
| `Tab` | Accept autocomplete |
| `Up/Down` | Navigate history |

### Essential Commands
| Command | Purpose |
|---------|---------|
| `/help` | Show all commands |
| `/compact` | Reduce context usage |
| `/clear` | Start fresh conversation |
| `/rewind` | Undo to checkpoint |
| `/status` | Show current state |
| `/config` | Open settings |
| `/review` | Review code changes |
| `/pr-comments` | Address PR feedback |

## Common Questions

**Q: How much context does Claude Code have?**
A: ~200K tokens. Use `/compact` if running low. See `references/core/context-management.md`.

**Q: Can Claude Code run commands without asking?**
A: Depends on permission mode. Safe commands auto-approve; destructive ones ask. See `references/core/agentic-loop.md`.

**Q: How do I share context across sessions?**
A: Use CLAUDE.md files for persistent context. See `references/configuration/memory.md`.

**Q: Can I use Claude Code in CI/CD?**
A: Yes, with headless mode (`claude -p`). See `references/workflows/advanced-workflows.md`.

**Q: How do I add custom tools?**
A: Via MCP servers. See `references/configuration/mcp.md`.

## IDE Integration

Claude Code integrates with VS Code and JetBrains IDEs:

**VS Code**: Install "Claude Code" extension
- `Cmd+Esc` (Mac) / `Ctrl+Esc` (Windows/Linux) to open
- Automatic file sync with editor
- Inline diff viewing

**JetBrains**: Install "Claude Code" plugin
- Same keyboard shortcut
- Project context awareness
- Integrated terminal

## Getting Help

- **In Claude Code**: Type `/help` for commands
- **Documentation**: https://docs.anthropic.com/claude-code
- **Issues**: https://github.com/anthropics/claude-code/issues
