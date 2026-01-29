---
name: command-development
description: This skill guides creating slash commands for Claude Code—reusable Markdown-based prompts with YAML configuration. Use when building custom commands, designing command workflows, or extending Claude Code functionality.
---

# Command Development

## Overview

Commands are reusable prompts defined as Markdown files with optional YAML frontmatter.

**Critical**: Commands are instructions FOR Claude, not messages TO users.

## Command File Structure

```markdown
---
description: Brief help text shown in /help
allowed-tools: Bash(git:*), Read
model: sonnet
argument-hint: [file-path] [options]
---

Instructions for Claude here.

Analyze the file at $1 and provide...
```

## File Locations

| Location | Scope |
|----------|-------|
| `.claude/commands/` | Project (shared via git) |
| `~/.claude/commands/` | Personal (all projects) |
| `plugin/commands/` | Plugin distribution |

## Frontmatter Fields

| Field | Purpose |
|-------|---------|
| `description` | Help text for `/help` command |
| `allowed-tools` | Restrict tool access (e.g., `Bash(git:*)`) |
| `model` | Specify model: haiku, sonnet, opus |
| `argument-hint` | Document expected arguments |
| `disable-model-invocation` | Prevent programmatic calls |

## Dynamic Features

### Arguments

```markdown
# All arguments as single string
Process: $ARGUMENTS

# Positional arguments
File: $1
Options: $2
Mode: $3
```

### File References

```markdown
# Include file contents
Review this code: @src/main.ts

# Argument-based reference
Analyze: @$1
```

### Inline Bash Execution

```markdown
# Current context
Current branch: !`git branch --show-current`
Recent commits: !`git log --oneline -5`
```

## Naming Conventions

Use verb-noun format:
- `review-pr.md`
- `generate-tests.md`
- `fix-issue.md`

## Organization

```
.claude/commands/
├── review-pr.md           # Flat for <15 commands
├── git/                   # Namespaced for 15+
│   ├── commit.md          # Becomes /git-commit
│   └── push.md            # Becomes /git-push
└── testing/
    └── run-tests.md       # Becomes /testing-run-tests
```

## Best Practices

1. **Single responsibility** - One task per command
2. **Document arguments** - Always use `argument-hint`
3. **Validate inputs** - Check before processing
4. **Restrict tools** - Use `allowed-tools` appropriately
5. **Clear naming** - Verb-noun format
