---
name: agent-skills
description: |
  Agent Skills - Open standard for packaging agent capabilities.
  Use when creating, integrating, or understanding agent skills format.
  Keywords: agent-skills, skill-structure, SKILL.md, progressive-disclosure, ai-agents, markdown-instructions.
compatibility: Any AI agent supporting the Agent Skills specification
metadata:
  source: https://agentskills.io/
  total_docs: 4
  generated: 2026-02-01
---

# Agent Skills

> Agent Skills are folders of instructions, scripts, and resources that agents can discover and use to do things more accurately and efficiently. An open standard for packaging agent capabilities.

## Quick Start

A skill is a folder with a `SKILL.md` file:

```
my-skill/
├── SKILL.md          # Required: instructions + metadata
├── scripts/          # Optional: executable code
├── references/       # Optional: documentation
└── assets/           # Optional: templates, resources
```

Minimal `SKILL.md`:

```markdown
---
name: my-skill
description: Does X when user needs Y.
---

# My Skill

## When to use
Use when the user needs to...

## Instructions
1. First step...
2. Second step...
```

## Documentation

Full documentation in `docs/`. See `docs/000-index.md` for navigation.

### By Topic

| Topic | Files | Description |
|-------|-------|-------------|
| Overview | 001 | What Agent Skills are and their purpose |
| Concepts | 002 | Skill structure and functionality |
| Integration | 003 | How to add skills support to agents |
| Specification | 004 | Complete technical format reference |

### By Keyword

| Keyword | File |
|---------|------|
| agent-skills | docs/001-home.md |
| skill-structure | docs/002-what-are-skills.md |
| progressive-disclosure | docs/002-what-are-skills.md |
| skills-integration | docs/003-integrate-skills.md |
| ai-agents | docs/003-integrate-skills.md |
| skill-format | docs/004-specification.md |
| directory-structure | docs/004-specification.md |
| yaml-frontmatter | docs/004-specification.md |
| validation | docs/004-specification.md |

### Learning Path

1. **Foundation**: Read `docs/001-home.md` for overview
2. **Concepts**: Read `docs/002-what-are-skills.md` for structure
3. **Integration**: Read `docs/003-integrate-skills.md` for implementation
4. **Reference**: Consult `docs/004-specification.md` for technical details

## Common Tasks

### Create a new skill
→ `docs/002-what-are-skills.md` (structure and SKILL.md format)
→ `docs/004-specification.md` (frontmatter fields, naming rules)

### Integrate skills into an agent
→ `docs/003-integrate-skills.md` (discovery, metadata, activation)

### Validate skill format
→ `docs/004-specification.md` (validation rules, skills-ref tool)

### Understand progressive disclosure
→ `docs/002-what-are-skills.md` (how skills manage context efficiently)
