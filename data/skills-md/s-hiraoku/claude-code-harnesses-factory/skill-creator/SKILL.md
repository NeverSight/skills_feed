---
name: skill-creator
description: This skill guides creating Claude skills—modular packages that extend capabilities with specialized knowledge and workflows. Use when creating new skills, packaging skills for distribution, or understanding skill architecture.
---

# Skill Creator

## Overview

Skills are modular packages that extend Claude's capabilities with specialized knowledge, workflows, and tool integrations.

## Skill Structure

```
my-skill/
├── SKILL.md          # Required - metadata and instructions
├── scripts/          # Optional - deterministic code
├── references/       # Optional - documentation loaded on-demand
└── assets/           # Optional - templates and boilerplate
```

## SKILL.md Format

```yaml
---
name: my-skill-name
description: Brief description and trigger conditions. "Use this skill when..."
allowed-tools: Tool1, Tool2  # Optional - restrict tool access
---

# Skill Name

## Instructions
Imperative instructions for Claude (not second person).

## Examples
Concrete usage examples.
```

## Six-Step Creation Process

1. **Understand** - Gather concrete use cases and validate understanding
2. **Plan** - Identify scripts, references, and assets needed
3. **Initialize** - Create directory structure with SKILL.md
4. **Develop** - Write instructions in imperative form (1,500-2,000 words max)
5. **Validate** - Test skill triggers correctly
6. **Iterate** - Refine based on real-world usage

## Progressive Disclosure Model

Skills use three-level loading:
1. **Metadata** (~100 words) - Always available
2. **SKILL.md body** - Loads when skill triggers
3. **Resources** - Load as needed

## Writing Requirements

- Use **imperative form**: "To accomplish X, do Y" (not "You should...")
- Description uses **third person**: "This skill should be used when..."
- Keep SKILL.md between 1,500-2,000 words
- Move detailed content to `references/` subdirectory

## Resource Types

| Type | Purpose |
|------|---------|
| **scripts/** | Deterministic code executed repeatedly |
| **references/** | Documentation loaded as needed |
| **assets/** | Templates and boilerplate code |

## Plugin Integration

Skills auto-discover in plugin `skills/` directories. No separate packaging needed—users receive skills when installing plugins.
