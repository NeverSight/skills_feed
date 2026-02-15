---
name: tavily-search
description: |
  Tavily AI search API - Optimized search for AI agents. Use when searching the web for current information, news, facts, or any task requiring real-time data.
---

# Tavily Search

Web search optimized for AI agents using Tavily API.

## Usage

```bash
./scripts/search "your search query"
```

## Scripts

| Script | Usage |
|--------|-------|
| `scripts/search <query>` | Search the web |
| `scripts/search "latest AI news" --format json` | JSON output |

## Environment

```bash
export TAVILY_API_KEY="your-api-key"
```

Get API key: https://tavily.com/

## Example

```bash
./scripts/search "Claude AI latest features"
# Returns: Search results optimized for AI context
```
