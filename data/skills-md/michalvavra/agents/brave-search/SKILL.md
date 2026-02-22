---
name: brave-search
description: Web search via the Brave Search API. Use to retrieve search results from Brave when web lookups are needed.
compatibility: Requires env. variable BRAVE_SEARCH_API_KEY and uv with Python 3.12+.
---

# Brave Search

## Usage

```bash
uv run --script {thisSkillDir}/scripts/brave-search.py "QUERY" [OPTIONS] --json
```

## Options

- `--count <N>`: Maximum results to return (default: 5)
- `--offset <N>`: Offset into the result set (default: 0)
- `--country <CODE>`: Two letter country code
- `--search-lang <CODE>`: Search language code
- `--safesearch <off|moderate|strict>`: Safe search mode
- `--freshness <day|week|month>`: Filter by recency
- `--json`: Output normalized JSON
- `--raw`: Output raw API response
- `--help`: Show help

## Examples

```bash
uv run --script {thisSkillDir}/scripts/brave-search.py "observability tools" --count 3 --json
```
