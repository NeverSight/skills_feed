---
name: firecrawl
description: Web scraping, search, and data extraction using Firecrawl API. Use when users need to fetch web content, discover URLs on sites, search the web, or extract structured data from pages.
---

# Firecrawl

## Overview

Firecrawl is a powerful web scraping and search API. This skill provides a token-efficient interface for Claude Code through the MCP server integration.

## When to Use This Skill

- **Scraping**: Fetch content from a single URL as markdown
- **Crawling**: Crawl entire websites following links
- **Mapping**: Discover all URLs on a website
- **Searching**: Search the web and optionally scrape results
- **Extracting**: Pull structured data from pages using LLM

## MCP Server Tools

When the Firecrawl MCP server is configured, you have access to these tools:

### firecrawl_scrape
Scrape a single URL and get clean markdown content.

```
Use: mcp__firecrawl__firecrawl_scrape
Parameters:
  - url: The URL to scrape
  - formats: ["markdown"] (optional)
```

### firecrawl_crawl
Crawl a website starting from a URL, following links.

```
Use: mcp__firecrawl__firecrawl_crawl
Parameters:
  - url: Starting URL
  - maxDepth: How deep to crawl (default: 2)
  - limit: Max pages to crawl
```

### firecrawl_map
Discover all URLs on a website without scraping content.

```
Use: mcp__firecrawl__firecrawl_map
Parameters:
  - url: The website URL
  - limit: Max URLs to return (default: 100)
```

### firecrawl_search
Search the web and get results with content.

```
Use: mcp__firecrawl__firecrawl_search
Parameters:
  - query: Search query
  - limit: Max results (default: 5)
```

Supports search operators:
- `"exact phrase"` - Exact match
- `-term` - Exclude term
- `site:example.com` - Limit to domain
- `intitle:word` - Word in title

### firecrawl_extract
Extract structured data from pages using LLM.

```
Use: mcp__firecrawl__firecrawl_extract
Parameters:
  - urls: Array of URLs to extract from
  - prompt: What to extract
  - schema: JSON Schema for structured output (optional)
```

## Quick Reference

| Task | MCP Tool |
|------|----------|
| Scrape a page | `firecrawl_scrape` |
| Crawl a site | `firecrawl_crawl` |
| Map site URLs | `firecrawl_map` |
| Search the web | `firecrawl_search` |
| Extract data | `firecrawl_extract` |

## Example Workflows

### Research a Topic
1. Use `firecrawl_search` to find relevant pages
2. Use `firecrawl_scrape` on the best results for full content

### Analyze a Documentation Site
1. Use `firecrawl_map` to discover all pages
2. Use `firecrawl_scrape` on specific sections

### Extract Product Information
1. Use `firecrawl_extract` with a prompt describing what to extract
2. Optionally provide a JSON schema for structured output

## Environment Setup

The MCP server requires `FIRECRAWL_API_KEY` environment variable.

Get your API key from: https://firecrawl.dev

## Token Efficiency

The MCP tools are designed for minimal token consumption:

- **Scrape**: Returns clean markdown
- **Map**: Returns URL list only
- **Search**: Returns summaries with optional full content
- **Extract**: Returns only requested data

## Error Handling

Common errors:
- `API key required` - Set FIRECRAWL_API_KEY in MCP config
- `Invalid URL` - Check URL format
- `Rate limited` - Wait and retry (auto-handled)
- `Site blocked` - Some sites block scraping

## Pricing Note

Firecrawl charges per operation:
- Scrape: 1 credit per page
- Map: 1 credit per call
- Search: 1 credit per result
- Extract: Varies by complexity

Check https://firecrawl.dev/pricing for current rates.

## Self-Hosted Option

If you have Firecrawl self-hosted on your server, configure the MCP server with:
- `FIRECRAWL_API_URL`: Your self-hosted instance URL (e.g., `http://localhost:3002`)
- No API key needed for self-hosted
