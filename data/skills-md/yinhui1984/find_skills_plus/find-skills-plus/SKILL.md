---
name: find-skills-plus
description: Find agent skills by keyword and enrich results with descriptions. Use when a user asks to discover skills and wants more context than a raw list (e.g., descriptions or comparisons).
compatibility: Requires Node.js, npm (npx), and network access to skills.sh.
---

# Find Skills Plus

This skill searches the skills registry and enriches each result with a description.

## When to Use

Use this skill when the user asks to discover skills and wants more than just a list (e.g., asks for descriptions, comparisons, or short summaries).

## How It Works

1) Runs `npx skills find <query>` to get matching skills.
2) For each result, fetches the skills.sh page and extracts a description (first non-empty paragraph).
3) Prints results in an easy-to-scan format.

## Command

```bash
node scripts/enrich_find.js "<query>"
```

## Options

- `--max N` Limit number of results to enrich (default: 10)
- `--timeout SECONDS` Per-request timeout (default: 10)
- `--concurrency N` Concurrent fetches (default: 5)
- `--no-fetch` Show list only (skip description fetch)

## Output Format

```
owner/repo@skill
└ https://skills.sh/owner/repo/skill
[description]
```

## Notes

- Descriptions are pulled from the skills.sh page when available.
- If the skills.sh page is missing a description, the script falls back to agent-skills.md.
- If a description cannot be found, the output will say "[no description found]".
