---
name: plugin-architecture
description: Master plugin folder structure, manifest design, and architectural patterns. Learn to organize plugins for scalability and maintainability.
sasmp_version: "1.3.0"
bonded_agent: 01-plugin-architect
bond_type: PRIMARY_BOND
---

# Plugin Architecture

## Quick Start

A well-structured plugin follows this minimal layout:

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json              # Required manifest
├── agents/
│   └── agent.md                 # Agent definition
├── skills/
│   └── skill-name/SKILL.md      # Skill definition
├── commands/
│   └── command.md               # Command definition
├── hooks/
│   └── hooks.json               # Automation hooks
└── README.md
```

## Plugin Manifest (plugin.json)

The manifest defines what your plugin does and what it contains.

```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "What my plugin does",
  "author": "Your Name",
  "license": "MIT",
  "repository": "https://github.com/user/repo",
  "agents": [
    {
      "name": "agent-id",
      "description": "What it does",
      "file": "agents/agent.md"
    }
  ],
  "commands": [
    {
      "name": "command",
      "file": "commands/command.md",
      "description": "What it does"
    }
  ],
  "skills": [
    {
      "name": "skill-id",
      "file": "skills/skill-id/SKILL.md"
    }
  ],
  "hooks": {
    "file": "hooks/hooks.json"
  }
}
```

### Manifest Rules

- **name**: lowercase-hyphens, 10-50 chars
- **version**: semantic (MAJOR.MINOR.PATCH)
- **description**: 50-256 characters
- **agents**: array of agent definitions
- **commands**: array of command definitions
- **skills**: array of skill definitions
- **hooks**: optional, points to hooks.json

## Agent Structure

Each agent is a markdown file with YAML frontmatter:

```markdown
---
description: What this agent does (max 1024 chars)
capabilities:
  - "Capability 1"
  - "Capability 2"
  - "Capability 3"
---

# Agent Name

[Detailed content about what agent does]

## When to Use

Use this agent when:
- Need 1
- Need 2
- Need 3
```

### Naming Convention

```
01-primary-agent.md
02-secondary-agent.md
03-tertiary-agent.md
```

## Skill Structure

Skills provide reusable knowledge and examples.

```
skills/
├── skill-one/
│   ├── SKILL.md              # Always named SKILL.md
│   └── resources/            # Optional: additional files
│       ├── example.py
│       └── reference.md
└── skill-two/
    └── SKILL.md
```

### SKILL.md Format

```markdown
---
name: skill-unique-id
description: "What skill teaches (max 1024 chars)"
---

# Skill Name

## Quick Start

[Working code - copy-paste ready]

## Core Concepts

### Concept 1
[Explanation with code]

### Concept 2
[More examples]

## Advanced Topics

[Expert-level content]

## Real-World Projects

[Practical applications]
```

## Command Structure

Commands are entry points for users:

```
commands/
├── create.md
├── design.md
├── test.md
└── deploy.md
```

### Command Format

```markdown
# /command-name - Brief Description

## What This Does

[Clear explanation]

## Usage

```
/command-name [options]
```

## Options

| Option | Description |
|--------|-------------|
| `--flag` | What it does |

## Example

[Sample output]

## Next Steps

[What to do next]
```

## Hook Configuration

Hooks automate plugin behavior:

```json
{
  "hooks": [
    {
      "id": "hook-id",
      "name": "Hook Name",
      "event": "event-type",
      "condition": "condition",
      "action": "action-name",
      "enabled": true
    }
  ]
}
```

## Architectural Patterns

### Single Responsibility

```
Agent 1: Domain A only
Agent 2: Domain B only
Agent 3: Domain C only
```

### Layered Architecture

```
Commands (User interface)
    ↓
Agents (Logic & guidance)
    ↓
Skills (Knowledge & examples)
    ↓
Hooks (Automation)
```

### Agent Collaboration

```
Agent A → asks → Agent B
  ↓
Links to shared skills
  ↓
Agent C for final review
```

## File Organization Best Practices

```
✅ Logical grouping
├─ All agents together
├─ All skills organized
├─ All commands grouped
└─ Config centralized

✅ Clear naming
├─ agents/01-primary.md
├─ agents/02-secondary.md
├─ skills/skill-one/SKILL.md
└─ commands/action.md

✅ Scalable structure
├─ Easy to add agents
├─ Simple to extend skills
├─ Clear command naming
└─ Organized hooks
```

## Scaling Your Plugin

### From Simple to Complex

**Stage 1**: 1 agent, 2 skills, 1 command
```
Minimal viable plugin
```

**Stage 2**: 3 agents, 5 skills, 3 commands
```
Feature-rich plugin
```

**Stage 3**: 5-7 agents, 10+ skills, 5+ commands
```
Enterprise plugin
```

## Common Mistakes

❌ **Unclear structure** → Use recommended layout
❌ **Mixed concerns** → One agent = one domain
❌ **Missing manifest** → Always include plugin.json
❌ **Bad naming** → Use lowercase-hyphens
❌ **No documentation** → Document everything

---

**Use this skill when:**
- Designing plugin structure
- Creating plugin.json
- Organizing agents and skills
- Planning plugin growth

---

**Status**: ✅ Production Ready | **SASMP**: v1.3.0 | **Bonded Agent**: 01-plugin-architect
