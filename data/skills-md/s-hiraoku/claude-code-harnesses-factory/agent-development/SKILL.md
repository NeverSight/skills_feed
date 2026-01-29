---
name: agent-development
description: This skill guides creating autonomous agents for Claude Code plugins using markdown files with YAML frontmatter. Use when building new agents, designing agent system prompts, or configuring agent behavior.
---

# Agent Development

## Overview

Agents are autonomous AI specialists defined as markdown files with YAML frontmatter and system prompt body.

## Agent File Structure

```markdown
---
name: my-agent
description: Use this agent when... with 2-4 triggering examples
model: inherit
color: blue
tools: Tool1, Tool2
---

System prompt instructions here.
```

## Required Fields

| Field | Description |
|-------|-------------|
| `name` | Lowercase identifier (3-50 chars, hyphens only) |
| `description` | "Use this agent when..." with triggering conditions |

## Optional Fields

| Field | Description |
|-------|-------------|
| `model` | `inherit`, `sonnet`, `opus`, or `haiku` |
| `color` | Visual identifier: blue, cyan, green, yellow, magenta, red |
| `tools` | Array restricting tool access |

## System Prompt Design

Use second-person language in the markdown body:

```markdown
You are a [role] specialized in [domain].

## Process
1. First, analyze...
2. Then, evaluate...
3. Finally, provide...

## Output Format
Structure your response as...

## Quality Standards
Ensure all outputs...
```

### Prompt Guidelines

- Keep between 500-3,000 characters
- Define clear role and responsibilities
- Provide step-by-step analysis process
- Specify output format
- Include quality standards and edge cases

## Description Field (Critical)

The description teaches Claude when to activate the agent:

```yaml
description: |
  Use this agent when reviewing code changes for quality and security.
  Examples:
  - User asks "review my PR" → triggers because code review requested
  - User commits changes and wants feedback → triggers for post-commit review
  - User mentions security concerns in code → triggers for security-focused review
```

## Best Practices

1. **Principle of least privilege** - Restrict tools to minimum needed
2. **Consistent colors** - Use same color for similar agent types
3. **Test triggering** - Verify agent activates for intended scenarios
4. **Clear boundaries** - Define what agent does NOT do

## File Location

```
.claude/agents/my-agent.md      # Project scope
~/.claude/agents/my-agent.md    # User scope
plugin/agents/my-agent.md       # Plugin scope
```
