---
name: skill-builder
description: Guide for creating effective Claude Code skills. Use when users want to create a new skill, update an existing skill, package a skill for distribution, or need guidance on skill structure and best practices. Triggers include "create skill", "build skill", "new skill", "make skill", "skill template", "package skill", or working with SKILL.md files.
---

# Skill Builder

Create Claude Code skills that extend capabilities with specialized knowledge, workflows, and tools.

## Quick Commands

| Task | Command |
|------|---------|
| New skill | `python scripts/init_skill.py <name> --path <dir>` |
| Validate | `python scripts/quick_validate.py <skill-dir>` |
| Package | `python scripts/package_skill.py <skill-dir> [output-dir]` |

## Core Principles

1. **Concise is key** - Claude is smart; only add what it doesn't know
2. **Progressive disclosure** - Metadata always loaded, SKILL.md on trigger, references on-demand
3. **Appropriate freedom** - High for flexible tasks, low for fragile operations

## Skill Creation Process

### Step 1: Clarify Requirements

Ask the user:
- What task should the skill automate?
- What triggers should invoke it? (keywords, file types, scenarios)
- What outputs are expected?
- Can you show example use cases?

### Step 2: Plan Resources

Analyze each use case to identify:
- **scripts/** - Repetitive code that should be deterministic
- **references/** - Documentation too long for SKILL.md
- **assets/** - Templates, images, boilerplate for output

### Step 3: Initialize

```bash
python scripts/init_skill.py my-skill --path ~/.claude/skills
```

### Step 4: Edit SKILL.md

#### Frontmatter (Critical)

```yaml
---
name: my-skill
description: What this skill does and WHEN to use it. Include triggers, file types, scenarios. This is the primary trigger mechanism. Max 1024 chars.
---
```

**Description rules:**
- Include BOTH what the skill does AND when to use it
- List specific triggers (file types, keywords, scenarios)
- No `<` or `>` characters
- Max 1024 characters

#### Body Patterns

**Pattern 1: Workflow-Based** (sequential processes)
```markdown
## Workflow
1. Analyze input -> Run `scripts/analyze.py`
2. Transform -> Apply rules
3. Output -> Save result
```

**Pattern 2: Task-Based** (tool collections)
```markdown
## Tasks
### Create New
[instructions]
### Edit Existing
[instructions]
```

**Pattern 3: Reference-Based** (standards/guidelines)
```markdown
## Guidelines
### Colors
### Typography
```

### Step 5: Add Resources

#### Scripts (`scripts/`)
For deterministic, repetitive operations.
- Test scripts before packaging
- Make executable: `chmod +x script.py`

#### References (`references/`)
Documentation loaded on-demand.
- For content >100 lines, add table of contents
- Split by domain/variant when >500 lines
- Avoid duplication with SKILL.md

#### Assets (`assets/`)
Files used in output (not loaded into context).
- Templates, images, fonts
- Boilerplate code

### Step 6: Validate & Package

```bash
python scripts/quick_validate.py my-skill/
python scripts/package_skill.py my-skill/ ./dist
```

## Frontmatter Rules

| Field | Required | Limit | Notes |
|-------|----------|-------|-------|
| name | Yes | 64 chars | hyphen-case only (`a-z`, `0-9`, `-`) |
| description | Yes | 1024 chars | No `<` or `>` characters |
| allowed-tools | No | - | Restrict tool access |

## Progressive Disclosure Patterns

**Keep SKILL.md under 500 lines.** Split to references/ when needed.

**High-level guide with references:**
```markdown
## Quick Start
[Essential workflow]

## Advanced
- **Forms**: See `references/forms.md`
- **API**: See `references/api.md`
```

**Domain-specific organization:**
```
skill/
├── SKILL.md (overview + navigation)
└── references/
    ├── aws.md
    ├── gcp.md
    └── azure.md
```

## What NOT to Include

- README.md (redundant with SKILL.md)
- CHANGELOG.md
- INSTALLATION_GUIDE.md
- User-facing documentation

Skills are for AI agents, not humans.

## References

- `references/skill-creation-guide.md` - Complete skill creation guide
- `references/output-patterns.md` - Template and example patterns
- `references/workflows.md` - Sequential and conditional workflow patterns
