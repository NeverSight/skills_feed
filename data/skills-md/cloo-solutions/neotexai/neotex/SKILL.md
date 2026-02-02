---
name: neotex
description: Use when working in projects with .neotex/ directory to retrieve organizational knowledge, search for patterns/guidelines/decisions, store learnings, or manage reference assets like images and files.
---

# Neotex Knowledge Integration

## Overview

Neotex is an agent-first knowledge system for storing and retrieving organizational knowledge and assets. This skill integrates Claude Code with neotex via CLI commands.

## Conversation Start: Auto-Check

At conversation start, check if neotex is initialized:

```bash
ls .neotex/index.json 2>/dev/null
```

- **If exists**: Note available knowledge (scan summaries, don't fetch all)
- **If missing but .neotex/ exists**: Suggest `neotex pull`
- **If no .neotex/**: Skip neotex workflow unless user wants to initialize

## When to Search

Search neotex when user asks about:
- Organizational conventions, standards, guidelines
- "How we do X here" or past decisions
- Patterns or templates for common tasks
- Reference images, mockups, or design files

```bash
neotex search "<query>" --limit 5
neotex search "type:guideline status:active path:backend <query>" --mode hybrid
neotex search "<query>" --source asset --mode lexical
neotex search "<query>" --exact
neotex get <id> --search-id <search_id>   # fetch if score > 0.7
neotex asset get <asset_id> --search-id <search_id>
```

- Use `--mode lexical` for exact terms, filenames, or code identifiers
- Use `--exact` to disable query expansion
- Pass `--search-id` to help the system learn which results were selected

## Precise Content Retrieval (VFS)

For large documents or when you need specific sections:

```bash
# Open with line range (like head/tail)
neotex context open <id> --lines 0:100 --max-chars 4000

# Open specific chunk from search result
neotex context open <id> --chunk <chunk_id>

# List items matching filters (like ls)
neotex context list --path /docs --type guideline --source knowledge
```

- Search results include `chunk_id` for precise retrieval
- Use `--max-chars` to limit response size (default 4000)
- Prefer chunk retrieval over full document when search provides chunk_id

## When to Store Knowledge

After completing significant work, evaluate:
- Non-obvious solution others would benefit from?
- Decision with tradeoffs worth documenting?
- Reusable pattern or template?

If yes, ask user before storing:
> "This involved [description]. Save to neotex as [type]: [title]?"

```bash
echo '{"type":"learning","title":"...","body_md":"# Title\n\n## Context\n..."}' | neotex add
```

## When to Store Assets

**IMPORTANT**: When users upload reference files, proactively offer to save them to neotex.

Save assets when user provides:
- Reference images (mockups, screenshots, diagrams)
- Design files (logos, icons, UI specs)
- Documentation PDFs
- Configuration files for reference
- Any file they want the team/AI to access later

**Prompt user:**
> "You uploaded [filename]. Save to neotex for future reference? I can add keywords and description for searchability."

```bash
# Upload an asset
neotex asset add <filepath> --description "..." --keywords "ui,mockup,login"

# Retrieve an asset
neotex asset get <asset_id> -o <output_path>
```

## Asset Best Practices

1. **Always ask before saving** - User may not want file persisted
2. **Add descriptive keywords** - Makes assets searchable (e.g., "login, mockup, mobile, v2")
3. **Include context in description** - Why this file matters, what it shows
4. **Link to knowledge when relevant** - Associate asset with related documentation
5. **Retrieve before recreating** - Search for existing assets before generating new ones

## Knowledge Types

| Type | Use For |
|------|---------|
| guideline | Rules to follow |
| learning | Insights from experience |
| decision | Architectural choices |
| template | Reusable structures |
| checklist | Verification steps |
| snippet | Reusable code |

## Common Mistakes

- **Fetching everything upfront**: Search on-demand, not at start
- **Storing trivial changes**: Only lasting organizational value
- **Duplicating**: Search before creating
- **Storing secrets**: Never include credentials or sensitive files
- **Ignoring uploaded files**: Always offer to save reference materials
- **Missing keywords**: Assets without keywords are hard to find later
