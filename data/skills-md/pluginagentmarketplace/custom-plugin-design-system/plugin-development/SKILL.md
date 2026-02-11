---
name: plugin-development
description: Master writing plugins including agent implementation, skill creation, command development, and hook scripting. Learn best practices for plugin coding.
sasmp_version: "1.3.0"
bonded_agent: 02-plugin-developer
bond_type: PRIMARY_BOND
---

# Plugin Development

## Quick Start

Create a complete agent:

```markdown
---
description: Expert in X domain, helping with Y and Z
capabilities:
  - "Build X systems"
  - "Optimize performance"
  - "Debug issues"
---

# Agent Name

## Overview
Expert specializing in X domain with 5+ years experience.

## Expert Areas

### Area 1: Core Concepts
Explanation and best practices...

## When to Use
Use this agent when building X or optimizing Y.

## Integration
Works with: agent-2, agent-3, skill-common
```

## Agent Implementation

### YAML Frontmatter

```yaml
---
description: "What agent does. When to use. Max 1024 chars."
capabilities:
  - "Specific capability 1"
  - "Specific capability 2"
  - "Specific capability 3"
  - "Specific capability 4"
---
```

### Content Structure

```markdown
# Agent Name

## Overview
[1-2 sentences about agent expertise]

## Expert Areas

### Area 1
[Detailed explanation with examples]

### Area 2
[More specific guidance]

### Area 3
[Best practices]

## When to Use
Use this agent when:
- Task 1
- Task 2
- Task 3

## Integration
Works with:
- Agent name (for X)
- Agent name (for Y)
- Skill name (for Z)

---
**Status**: ✅ Production Ready | **Updated**: [Date]
```

## Skill Implementation

### SKILL.md Template

```markdown
---
name: skill-id
description: "What it teaches and when to use (max 1024 chars)"
---

# Skill Name

## Quick Start

[Working code - immediately useful]

```python
# Real example
result = do_something()
print(result)
```

## Core Concepts

### Concept 1
[Explanation with code]

### Concept 2
[Practical patterns]

### Concept 3
[Advanced usage]

## Advanced Topics

[Expert-level material]

## Real-World Projects

[1-3 practical applications]

---

**Use this skill when:**
- Learning X
- Implementing Y
- Solving Z problem
```

## Command Implementation

### Command Files

```markdown
# /command-name - One-Line Description

## What This Does

[Clear explanation of what command does]

## Usage

```
/command-name
/command-name --option value
/command-name --flag1 v1 --flag2 v2
```

## Options

| Option | Type | Description |
|--------|------|-------------|
| `--option` | string | What it does |
| `--flag` | boolean | Enables X |

## Example

```
$ /command-name my-plugin
Creating plugin...
✅ Done!

Next: /command-2
```

## Tips

- Tip 1
- Tip 2

## Related Commands

- `/other-command`
```

## Hook Implementation

### Hook JSON

```json
{
  "hooks": [
    {
      "id": "unique-id",
      "name": "Hook Display Name",
      "description": "What it does",
      "event": "event-type",
      "condition": "condition-logic",
      "action": "action-handler",
      "enabled": true
    }
  ],
  "notifications": {
    "enabled": true,
    "channels": ["in-app", "console"]
  }
}
```

### Hook Event Types

- `command-executed` - When command runs
- `agent-invoked` - When agent used
- `skill-loaded` - When skill accessed
- `scheduled` - Periodic events

## Code Quality Standards

### Agent Quality

```
✅ Clear description (100-200 chars)
✅ 5-10 specific capabilities
✅ 3-5 expert areas
✅ "When to Use" section
✅ Integration points documented
✅ 250-400 lines total
```

### Skill Quality

```
✅ Name: lowercase-hyphens
✅ Description: actionable, clear
✅ Quick Start: working code
✅ 3+ core concepts
✅ Advanced section
✅ 2+ real projects
✅ 200-300 lines total
```

### Command Quality

```
✅ Clear description
✅ Usage examples
✅ Options documented
✅ Example output shown
✅ Next steps suggested
✅ 100-150 lines total
```

## Common Implementation Patterns

### Knowledge Pattern
```
Agent → Explains concept
Skill → Provides examples
Command → Enable practice
```

### Workflow Pattern
```
Command → Starts workflow
Agent → Guides decisions
Hook → Automate steps
```

### Integration Pattern
```
Agent A → Recommends B
Agent B → Links to skill X
Skill X → Suggests command Y
```

## Testing Your Implementation

### Agent Testing

```markdown
✅ Description under 1024 chars
✅ Capabilities are specific
✅ Content is 250-400 lines
✅ Integration documented
✅ Status included
```

### Skill Testing

```markdown
✅ Name lowercase-hyphenated
✅ Quick Start runs without error
✅ 3+ concepts explained
✅ Real projects included
✅ Proper formatting
```

### Command Testing

```markdown
✅ Command executes
✅ Options work as documented
✅ Output matches description
✅ Next steps provided
✅ No errors
```

## Documentation Requirements

### For Agents

```
✅ What agent does
✅ When to use
✅ Capabilities (5-10)
✅ Expert areas (3-5)
✅ Integration points
✅ Status & date
```

### For Skills

```
✅ Clear description
✅ Quick Start code
✅ Core concepts (3+)
✅ Advanced topics
✅ Real projects (2+)
✅ Usage guidelines
```

### For Commands

```
✅ What it does
✅ Usage syntax
✅ Options table
✅ Example output
✅ Next steps
✅ Related commands
```

## Version Control Practices

### Commit Messages

```
feat: Add new skill for X
fix: Correct Y in agent
docs: Update Z documentation
refactor: Improve performance
test: Add validation tests
```

### File Changes

```
New agent?
  → Ensure manifest updated
  → Add to appropriate section
  → Document relationships

New skill?
  → Create folder with SKILL.md
  → Reference in manifest
  → Add to agent capabilities

New command?
  → Create markdown file
  → Add to manifest
  → Document options
```

---

**Use this skill when:**
- Writing agent content
- Creating new skills
- Implementing commands
- Setting up hooks
- Testing implementation

---

**Status**: ✅ Production Ready | **SASMP**: v1.3.0 | **Bonded Agent**: 02-plugin-developer
