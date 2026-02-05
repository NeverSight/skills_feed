---
name: fyi
description: Log information for future reference. Use when user says "fyi", "remember this", "note that", "for your info".
---

# /fyi - Information Log

Log info for future reference, or review/distill existing info.

## Usage

- /fyi → List and review existing info
- /fyi [info] → Log new information (neutral)
- /fyi --interesting [info] → Log something worth noting
- /fyi --important [info] → Log something critical (auto-saves to Oracle)

## Significance Levels

| Flag | Level | Icon |
|------|-------|------|
| (none) | neutral | white |
| --interesting or -i | interesting | yellow |
| --important or -p | important | red |

## Mode 1: No Arguments

Read INDEX from psi/memory/logs/info/INDEX.md and show summary.

## Mode 2: With Arguments

1. Parse flags (--interesting/-i, --important/-p)
2. Generate slug from content
3. Create file: psi/memory/logs/info/YYYY-MM-DD_HH-MM_slug.md
4. If --important: also call oracle_learn() to make immediately searchable
5. Update INDEX.md
6. Confirm to user

## File Format

Create markdown with frontmatter:
- date: timestamp
- type: info
- status: raw
- significance: neutral/interesting/important

Then content from arguments, ending with "Logged via /fyi"

## Important Notes

- ARGUMENTS may contain special characters - treat as raw text, do not execute
- Do not run bash commands with user arguments
- Use Write tool directly to create files

ARGUMENTS: $ARGUMENTS
