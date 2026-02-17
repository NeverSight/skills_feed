---
name: plugin-development
description: Use when creating Claude Code plugins, writing skills, building commands, developing agents, or asking about "plugin development", "create skill", "write command", "build agent", "SKILL.md", "plugin structure", "progressive disclosure"
version: 1.0.0
---

# Claude Code Plugin Development

Guide for creating effective Claude Code plugins with skills, commands, and agents.

## Plugin Structure

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json         # Plugin metadata
├── skills/
│   └── skill-name/
│       ├── SKILL.md        # Required
│       ├── references/     # Detailed docs
│       ├── examples/       # Working code
│       └── scripts/        # Utilities
├── commands/
│   └── command-name.md
├── agents/
│   └── agent-name.md
└── hooks/
    └── hooks.json
```

## Skill Development

### SKILL.md Structure

```yaml
---
name: skill-name
description: This skill should be used when the user asks to "specific phrase 1", "specific phrase 2", or mentions "keyword". Be specific about triggers.
version: 1.0.0
---

# Skill Title

Core content here (1,500-2,000 words ideal).

## Additional Resources

- **`references/detailed.md`** - Detailed patterns
- **`examples/working.sh`** - Working example
```

### Progressive Disclosure

| Level | Content | When Loaded |
|-------|---------|-------------|
| **Metadata** | name + description | Always (~100 words) |
| **SKILL.md** | Core content | When triggered (<5k words) |
| **References** | Detailed docs | As needed (unlimited) |

### Description Best Practices

**Good:**

```yaml
description: This skill should be used when the user asks to "create a hook", "add PreToolUse hook", "validate tool use", or mentions hook events.
```

**Bad:**

```yaml
description: Provides hook guidance.  # Too vague
description: Use this skill for hooks.  # Not third person
```

### Writing Style

Use **imperative form**, not second person:

```markdown
# Good
Start by reading the configuration.
Validate the input before processing.

# Bad
You should start by reading...
You need to validate the input...
```

## Command Development

### Command Structure

```yaml
---
name: command-name
description: What the command does
argument-hint: "[optional args]"
---

# Command Title

Instructions for executing the command.
```

### Example Command

```yaml
---
name: review-pr
description: Review a GitHub PR with detailed code analysis
argument-hint: "[PR number or URL]"
---

# Review PR Command

1. Fetch PR details using `gh pr view`
2. Get changed files with `gh pr diff`
3. Analyze each file for issues
4. Provide summary with recommendations
```

## Agent Development

### Agent Structure

```yaml
---
agent: agent-name
description: |
  When to use this agent with examples:
  <example>
  Context: User situation
  user: "User request"
  assistant: "How assistant responds"
  <commentary>Why this agent is appropriate</commentary>
  </example>
model: sonnet
tools:
  - Read
  - Glob
  - Grep
  - Bash
color: cyan
---

# Agent Instructions

Detailed instructions for the agent's behavior.
```

### Agent Colors

Valid colors: `red`, `green`, `yellow`, `blue`, `magenta`, `cyan`, `white`

## Hooks Development

### hooks.json Structure

```json
{
  "hooks": [
    {
      "event": "PreToolUse",
      "matcher": "Write|Edit",
      "type": "prompt",
      "prompt": "Validate code before writing...",
      "timeout": 10000
    }
  ]
}
```

### Hook Events

| Event | When Fired |
|-------|-----------|
| `SessionStart` | Session begins |
| `PreToolUse` | Before tool execution |
| `PostToolUse` | After tool execution |
| `Stop` | Session ends |
| `Notification` | Background task complete |

## Validation Checklist

**Skills:**

- [ ] SKILL.md has valid YAML frontmatter
- [ ] Description uses third person with trigger phrases
- [ ] Body is 1,500-2,000 words (detailed content in references/)
- [ ] Uses imperative writing style
- [ ] Referenced files exist

**Commands:**

- [ ] Has name and description in frontmatter
- [ ] Clear instructions for execution
- [ ] argument-hint if accepts parameters

**Agents:**

- [ ] Has description with examples
- [ ] Specifies model and tools
- [ ] Valid color specified
- [ ] Detailed behavioral instructions

## Common Mistakes

1. **Weak skill descriptions** - Be specific with trigger phrases
2. **Too much in SKILL.md** - Use progressive disclosure
3. **Second person writing** - Use imperative form
4. **Missing resource references** - Point to references/examples
5. **Vague agent examples** - Include concrete user/assistant pairs
