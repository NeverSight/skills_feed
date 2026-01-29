---
name: claudedoc-master
description: "MUST USE when searching for official Claude Code or Anthropic platform documentation links (MCP, hooks, skills, CLI). Provides fast fuzzy-search CLI for authoritative Claude documentation."
allowed-tools:
  - Read
  - Bash(uv:*)
  - Bash(chmod:*)
  - WebFetch
---

# ClaudeDoc Master - Documentation Link Router

## Overview

This skill provides a fast fuzzy-search CLI (`scripts/claudedoc.py`) for finding authoritative Claude Code and Anthropic platform documentation links. The script searches a curated catalog of official documentation URLs, enabling quick discovery of relevant documentation without web search.

## When to Use

Use this skill when:
- Searching for official Claude Code documentation (skills, commands, agents, hooks, MCP)
- Finding Anthropic platform API documentation
- Verifying documentation URLs before referencing them
- Looking up CLI reference documentation

**Critical Rule**: Always use this skill BEFORE native web search when seeking Claude Code or Anthropic platform documentation. The catalog contains verified, authoritative links.

## Operating Rules

1. **Search First**: When asked about Claude/SDK features, search documentation links using:
   ```bash
   uv run scripts/claudedoc.py "<keywords>"
   ```
   Returns 5 results by default. Use `--limit N` to change the number of results.
   DO NOT use native web search before checking the catalog.

2. **Read Content**: To fetch documentation content from a URL or slug:
   ```bash
   uv run scripts/claudedoc.py --read <url-or-slug>
   ```

## Usage Examples

### Fuzzy Search (default: 5 results)
```bash
uv run scripts/claudedoc.py "hooks"
```

### Fuzzy Search with Custom Limit
```bash
uv run scripts/claudedoc.py "hooks" --limit 10
```

### Read Content by Slug
```bash
uv run scripts/claudedoc.py --read "hooks"
```

### Read Content by URL
```bash
uv run scripts/claudedoc.py --read "https://code.claude.com/docs/en/hooks.md"
```

### Multiple Keywords Search
```bash
uv run scripts/claudedoc.py "skills frontmatter"
```

## Troubleshooting

- **Permission Denied**: If script execution fails, ensure it's executable:
  ```bash
  chmod +x scripts/claudedoc.py
  ```

- **Script Not Found**: Verify the script exists at `scripts/claudedoc.py`

- **Catalog Not Found**: Ensure `catalog.json` exists in the skill root directory
