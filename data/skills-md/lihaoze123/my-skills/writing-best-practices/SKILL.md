---
name: writing-best-practices
description: Use when creating structured best practices guides, organizing technical documentation, or establishing reference materials for teams or agents
license: MIT
metadata:
  author: chumeng
  version: "2.0.0"
  lastUpdated: "2026-01-24"
---

# Writing Best Practices

Create structured, maintainable best practices documentation that scales from quick reference to detailed guides.

## Core Principle

**Separate quick reference from comprehensive documentation.**

## When to Use

- Creating technical best practices guides
- Organizing reference documentation for teams or agents
- Building structured knowledge bases
- Documenting proven patterns and approaches

**Don't use for:**
- One-time documentation (use simple README)
- Project-specific notes (use CLAUDE.md)
- Narrative blog posts or tutorials

## Quick Reference

| Topic | Rule File |
|-------|-----------|
| Core structure and organization | [structure](rules/structure.md) |
| Frontmatter format | [frontmatter](rules/frontmatter.md) |
| Impact levels | [impact-levels](rules/impact-levels.md) |
| Validation and verification | [validation](rules/validation.md) |
| Writing individual rules | [writing-rules](rules/writing-rules.md) |
| Code examples and patterns | [code-examples](rules/code-examples.md) |
| Quick reference tables | [quick-reference](rules/quick-reference.md) |
| Maintenance and updates | [maintenance](rules/maintenance.md) |
| Common anti-patterns | [anti-patterns](rules/anti-patterns.md) |

## Essential Structure

```
best-practice-name/
├── SKILL.md          # Quick reference (human scan)
├── AGENTS.md         # Full content (agent read)
└── rules/            # Modular rule files
    ├── rule-1.md
    ├── rule-2.md
    └── ...
```

**SKILL.md** (2-3 pages):
- Overview and core principle
- When to use/not use
- Quick reference table
- Essential pattern code
- Red flags
- Link to full doc

**AGENTS.md** (complete compilation):
- All content in single document
- Generated or compiled from rules/
- Comprehensive with all details

**rules/** (modular sections):
- One file per focused topic
- Mix of concept + examples
- Easy to update independently

## Common Patterns

| Need | Pattern |
|------|---------|
| Quick lookup | Table with rule file links |
| Deep understanding | AGENTS.md with all details |
| Specific topic | Individual rule file |
| Code variations | Tables instead of multiple examples |

## Red Flags - STOP

| Anti-pattern | Fix |
|--------------|-----|
| "Put everything in one file" | Use modular structure |
| "No need for quick reference" | Humans scan, agents read |
| "Five language examples" | One excellent example is enough |
| "Narrative style rules" | Use problem/solution format |

## How to Use

Each rule file contains:
- Why the pattern matters
- ❌ Incorrect vs ✅ Correct examples
- Additional context and references

For the complete guide: `AGENTS.md`
