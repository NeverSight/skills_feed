---
name: write-docs
description: Write AI-scannable technical documentation.
---

# Write Documentation

Documentation that is scannable, consistent, and actionable for AI agents.

## Structure

- Max 150 lines per file, one concept per file
- Start with `description:` in YAML frontmatter
- Add TL;DR section at top with most-needed info

## Content

- No duplicates (define once, link elsewhere)
- Use tables for structured data (parameters, config)
- Concrete examples for everything (copy-pasteable)
- Link to real code as templates

## Naming

| Pattern | Use For | Example |
|---------|---------|---------|
| `README.md` | Directory overview | `docs/README.md` |
| `{noun}.md` | Reference | `entities.md` |
| `{verb}-{noun}.md` | How-to | `add-entity.md` |

## Tips

- Use consistent terms (one term per concept)
- Group by task ("How to add X") not system ("X overview")
- Include troubleshooting for common errors
