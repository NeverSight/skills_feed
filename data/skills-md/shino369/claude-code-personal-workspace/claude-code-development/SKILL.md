---
name: claude-code-development
description: Expert knowledge in creating and configuring Claude Code components (subagents, skills, slash commands, hooks, MCP integrations). Use when the user asks to create, modify, or extend .claude/ directory components. Follows official best practices and documentation standards.
---

# Claude Code Development

## Overview

This skill provides comprehensive guidance for creating and configuring Claude Code components following official best practices. Use this when working with `.claude/` directory structure including agents, skills, commands, hooks, and MCP integrations.

## Official Documentation

All official documentation references are maintained in `docs/claude/README.md`. Always consult these references for the latest standards and best practices:

- [Claude Code Settings](https://code.claude.com/docs/en/settings.md)
- [Claude Code Memory Management](https://code.claude.com/docs/en/memory.md)
- [Claude Code Sub-agents Documentation](https://code.claude.com/docs/en/sub-agents.md)
- [Claude Code Skills Documentation](https://code.claude.com/docs/en/skills.md)
- [Claude Code Slash Commands Documentation](https://code.claude.com/docs/en/slash-commands.md)
- [Claude Code Hooks Documentation](https://code.claude.com/docs/en/hooks.md)
- [Claude Code MCP Support](https://code.claude.com/docs/en/mcp.md)
- [Agent Skills Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices.md)

When creating new components, fetch and review the relevant documentation using the WebFetch tool.

## Quick Start

### When to Use Which Component?

**Use a Subagent** when you need:

- Task isolation in a separate context
- Specialized model or tool restrictions
- Repeated complex workflows

**Use a Skill** when you need:

- Reusable knowledge that Claude lacks
- Domain-specific terminology or patterns
- Expert knowledge loaded into context

**Use a Command** when you need:

- User-invocable workflows
- Shortcuts for common tasks
- Structured argument handling

**Use a Hook** when you need:

- Automated actions on tool events
- Validation before operations
- Cleanup after operations

### Quick Examples

**Agent** (specialized AI for focused tasks):

```yaml
name: code-reviewer
description: Reviews code for quality and best practices
tools: Read, Grep, Glob
```

**Skill** (reusable knowledge package):

```yaml
name: api-design-patterns
description: REST API design. Use when designing or reviewing APIs.
```

**Command** (user-invocable workflow):

```yaml
description: Review code changes
allowed-tools: Task(code-reviewer)
```

See detailed guides: [Agents](agents-guide.md) | [Skills](skills-guide.md) | [Commands](commands-guide.md)

## Component Types Overview

### Subagents (.claude/agents/)

Specialized AI assistants that handle specific types of tasks in isolated contexts.

- **File Format**: Markdown with YAML frontmatter
- **Location**: `.claude/agents/[agent-name].md`
- **Key Fields**: name, description, tools, model, skills, permissionMode

See [Agent Creation Guide](agents-guide.md) for complete details.

### Skills (.claude/skills/)

Reusable knowledge packages that can be loaded into conversations or subagents.

- **File Format**: Markdown with YAML frontmatter
- **Location**: `.claude/skills/[skill-name]/SKILL.md`
- **Key Fields**: name, description, allowed-tools, context

See [Skills Creation Guide](skills-guide.md) for complete details.

### Slash Commands (.claude/commands/)

User-invocable prompts that provide reusable workflows.

- **File Format**: Markdown with YAML frontmatter
- **Location**: `.claude/commands/[command-name].md`
- **Key Fields**: description, argument-hint, allowed-tools

See [Commands Creation Guide](commands-guide.md) for complete details.

### Hooks (.claude/hooks/)

Scripts that run automatically on tool events.

- **Configuration**: In `.claude/settings.json` or component frontmatter
- **Hook Events**: PreToolUse, PostToolUse, SubagentStart, SubagentStop, Stop
- **Hook Types**: command (shell), prompt (text injection)

See [Hooks Reference Guide](hooks-guide.md) for complete details.

## Directory Structure

Standard layout for a well-organized `.claude/` directory:

```
.claude/
├── settings.json              # Project-level configuration
├── agents/
│   ├── agent-name-1.md
│   └── agent-name-2.md
├── skills/
│   ├── skill-name-1/
│   │   ├── SKILL.md
│   │   ├── reference.md       # Progressive disclosure
│   │   └── scripts/
│   │       └── helper.py
│   └── skill-name-2/
│       └── SKILL.md
├── commands/
│   ├── command-1.md
│   └── command-2.md
└── hooks/
    ├── README.md              # Hook documentation
    └── scripts/
        ├── validate.sh
        └── lint.sh
```

## Naming Conventions

**Agents**: `lowercase-with-hyphens`

- Good: `code-reviewer`, `test-runner`, `db-analyzer`
- Avoid: `CodeReviewer`, `test_runner`, `DBAnalyzer`

**Skills**: `lowercase-with-hyphens` (gerund form preferred)

- Good: `processing-pdfs`, `analyzing-data`, `reviewing-code`
- Acceptable: `pdf-processing`, `data-analysis`, `code-review`
- Avoid: `helper`, `utils`, `tools` (too vague)

**Commands**: `lowercase-with-hyphens`

- Good: `translate`, `deploy-staging`, `run-tests`
- Avoid: `doTranslate`, `Deploy_Staging`

**Files**: Always use `.md` extension for agents, skills, and commands

## Quality Checklist

**All Components**: Valid YAML, clear description with trigger terms, follows naming conventions

**Agents**: Focused purpose, minimal tools, clear workflow, tested
**Skills**: Concise (<500 lines), concrete examples, one-level references
**Commands**: User-facing, clear arguments, examples included
**Hooks**: Fast execution, proper error handling, appropriate scope

For detailed checklists, see component-specific guides.

## Best Practices Summary

1. **Follow official documentation**: Always consult official guides
2. **Be concise**: Assume Claude is smart, avoid over-explaining
3. **Use progressive disclosure**: Split large content into multiple files
4. **Test thoroughly**: Verify components work as expected
5. **Iterate based on behavior**: Watch how Claude uses components and refine
6. **Keep components focused**: Each component should do one thing well
7. **Document clearly**: Good descriptions and examples are essential
8. **Use appropriate tools**: Restrict tool access to minimum needed
9. **Maintain consistency**: Follow naming conventions and patterns
10. **Version control**: Check components into git for team collaboration

## References

For detailed guidance, see these companion guides:

- **[Agent Creation Guide](agents-guide.md)** - Comprehensive subagent development
- **[Skills Creation Guide](skills-guide.md)** - Detailed skill creation with progressive disclosure
- **[Commands Creation Guide](commands-guide.md)** - Slash command development patterns
- **[Hooks Reference Guide](hooks-guide.md)** - Complete hooks documentation
- **[Common Patterns & Examples](patterns-examples.md)** - Practical patterns and examples

Always refer to the official documentation (see top of this file) when:

- Creating new component types
- Using advanced features
- Troubleshooting issues
- Following best practices
- Understanding permission models

The official documentation is the source of truth. This skill provides a practical guide, but defer to official docs for authoritative information.
