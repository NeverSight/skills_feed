---
name: linkup
description: >
  Real-time web search and content retrieval via the Linkup API. Use when
  up-to-date information from the web, source-backed answers, or direct page
  content retrieval is required.
---

# Linkup

## Overview

The Linkup skill uses the Linkup API via `curl` to perform web searches and
fetch webpage content directly. Preferred over the Linkup MCP server for
real-time information and source-backed answers.

## Workflow

### Step 1: Run a Web Search

```bash
curl -s -X POST \
  -H "Authorization: Bearer $LINKUP_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "q": "QUERY",
    "depth": "standard",
    "outputType": "sourcedAnswer"
  }' \
  "https://api.linkup.so/v1/search"
```

**Parameters:**

- `q` (required): Natural language search query.
- `depth` (optional): Search depth (`standard` or `deep`).
- `outputType` (optional): Response format (e.g., `sourcedAnswer` for an answer +
  sources, or `searchResults` for raw results).
- `includeDomains` (optional): Array of domains/URLs to include.
- `excludeDomains` (optional): Array of domains/URLs to exclude.
- `includeImages` (optional): Include image results when set to `true`.
- `maxResults` (optional): Limit the number of returned results.

### Step 2: Fetch Page Content (Optional)

```bash
curl -s -X POST \
  -H "Authorization: Bearer $LINKUP_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com/article",
    "renderJs": false
  }' \
  "https://api.linkup.so/v1/fetch"
```

**Parameters:**

- `url` (required): The webpage to fetch and extract content from.
- `renderJs` (optional): Whether to render JavaScript content (default `false`).

## Examples

### Source-backed answer with citations

```bash
curl -s -X POST \
  -H "Authorization: Bearer $LINKUP_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "q": "What changed in the latest Node.js release?",
    "depth": "standard",
    "outputType": "sourcedAnswer",
    "maxResults": 5
  }' \
  "https://api.linkup.so/v1/search"
```

### Raw search results for deeper research

```bash
curl -s -X POST \
  -H "Authorization: Bearer $LINKUP_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "q": "EU AI Act compliance checklist",
    "depth": "deep",
    "outputType": "searchResults",
    "includeDomains": ["ec.europa.eu", "eur-lex.europa.eu"]
  }' \
  "https://api.linkup.so/v1/search"
```

### Fetch the content of a specific URL

```bash
curl -s -X POST \
  -H "Authorization: Bearer $LINKUP_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com/docs",
    "renderJs": true
  }' \
  "https://api.linkup.so/v1/fetch"
```

## Tips

- Use `outputType: sourcedAnswer` for concise answers with citations.
- Use `outputType: searchResults` for full result lists or manual synthesis.
- Prefer `depth: standard` for quick lookups and `depth: deep` for multi-source research.
- Use `includeDomains` / `excludeDomains` to control where sources come from.
