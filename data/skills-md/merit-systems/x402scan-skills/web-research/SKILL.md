---
name: web-research
description: |
  Neural web search and content extraction using x402-protected APIs. Better than WebSearch for deep research and WebFetch for blocked sites.

  USE FOR:
  - Deep web research and investigation
  - Finding similar pages to a reference URL
  - Extracting clean text from web pages
  - Scraping sites that block standard fetchers
  - Getting direct answers to factual questions
  - Research requiring multiple sources

  TRIGGERS:
  - "research", "investigate", "deep dive", "find sources"
  - "similar to", "pages like", "more like this"
  - "scrape", "extract content from", "get the text from"
  - "blocked site", "can't access", "paywall"
  - "what is", "explain", "answer this"

  Use mcp__x402__fetch for these endpoints. Prefer Exa for semantic/neural search, Firecrawl for direct scraping.
---

# Web Research with x402 APIs

Access Exa (neural search) and Firecrawl (web scraping) through x402-protected endpoints.

## Setup

See [rules/getting-started.md](rules/getting-started.md) for installation and wallet setup.

## Quick Reference

| Task | Endpoint | Price | Best For |
|------|----------|-------|----------|
| Neural search | `/api/exa/search` | $0.01 | Semantic web search |
| Find similar | `/api/exa/find-similar` | $0.01 | Pages similar to a URL |
| Extract text | `/api/exa/contents` | $0.002 | Clean text from URLs |
| Direct answers | `/api/exa/answer` | $0.01 | Factual Q&A |
| Scrape page | `/api/firecrawl/scrape` | $0.0126 | Single page to markdown |
| Web search | `/api/firecrawl/search` | $0.0252 | Search with scraping |

## When to Use What

| Scenario | Tool |
|----------|------|
| General web search | WebSearch (free) or Exa ($0.01) |
| Semantic/conceptual search | Exa search |
| Find pages like X | Exa find-similar |
| Get clean text from URL | Exa contents |
| Scrape blocked/JS-heavy site | Firecrawl scrape |
| Search + scrape results | Firecrawl search |
| Quick fact lookup | Exa answer |

See [rules/when-to-use.md](rules/when-to-use.md) for detailed guidance.

## Exa Neural Search

Semantic search that understands meaning, not just keywords:

```
mcp__x402__fetch(
  url="https://enrichx402.com/api/exa/search",
  method="POST",
  body={
    "query": "startups building AI agents for customer support",
    "numResults": 10,
    "type": "neural"
  }
)
```

**Options:**
- `query` - Search query (required)
- `numResults` - Number of results (default: 10, max: 25)
- `type` - "neural" (semantic) or "keyword" (traditional)
- `includeDomains` - Only search these domains
- `excludeDomains` - Skip these domains
- `startPublishedDate` / `endPublishedDate` - Date range filter

**Returns**: List of URLs with titles, snippets, and relevance scores.

## Find Similar Pages

Find pages semantically similar to a reference URL:

```
mcp__x402__fetch(
  url="https://enrichx402.com/api/exa/find-similar",
  method="POST",
  body={
    "url": "https://example.com/article-i-like",
    "numResults": 10
  }
)
```

Great for:
- Finding competitor products
- Discovering related content
- Expanding research sources

## Extract Text Content

Get clean, structured text from URLs:

```
mcp__x402__fetch(
  url="https://enrichx402.com/api/exa/contents",
  method="POST",
  body={
    "urls": [
      "https://example.com/article1",
      "https://example.com/article2"
    ]
  }
)
```

**Options:**
- `urls` - Array of URLs to extract
- `text` - Include full text (default: true)
- `highlights` - Include key highlights

Cheapest option ($0.002) when you already have URLs and just need the content.

## Direct Answers

Get factual answers to questions:

```
mcp__x402__fetch(
  url="https://enrichx402.com/api/exa/answer",
  method="POST",
  body={
    "query": "What is the population of Tokyo?"
  }
)
```

Returns a direct answer with source citations. Best for:
- Factual questions
- Quick lookups
- Verification of claims

## Firecrawl Scrape

Scrape a single page to clean markdown:

```
mcp__x402__fetch(
  url="https://enrichx402.com/api/firecrawl/scrape",
  method="POST",
  body={
    "url": "https://example.com/page-to-scrape"
  }
)
```

**Options:**
- `url` - Page to scrape (required)
- `formats` - Output formats: ["markdown", "html", "links"]
- `onlyMainContent` - Skip nav/footer/ads (default: true)
- `waitFor` - Wait ms for JS to render

**Advantages over WebFetch:**
- Handles JavaScript-rendered content
- Bypasses common blocking
- Extracts main content only
- LLM-optimized markdown output

## Firecrawl Search

Web search with automatic scraping of results:

```
mcp__x402__fetch(
  url="https://enrichx402.com/api/firecrawl/search",
  method="POST",
  body={
    "query": "best practices for react server components",
    "limit": 5
  }
)
```

**Options:**
- `query` - Search query (required)
- `limit` - Number of results (default: 5)
- `scrapeOptions` - Options passed to scraper

Returns search results with full scraped content for each.

## Workflows

### Deep Research

- [ ] (Optional) Check balance: `mcp__x402__get_wallet_info`
- [ ] Search broadly with Exa
- [ ] Find related sources with find-similar
- [ ] Extract content from top sources
- [ ] Synthesize findings

```
mcp__x402__fetch(
  url="https://enrichx402.com/api/exa/search",
  method="POST",
  body={"query": "AI agents in healthcare 2024", "numResults": 15}
)
```

```
mcp__x402__fetch(
  url="https://enrichx402.com/api/exa/find-similar",
  method="POST",
  body={"url": "https://best-article-found.com"}
)
```

```
mcp__x402__fetch(
  url="https://enrichx402.com/api/exa/contents",
  method="POST",
  body={"urls": ["url1", "url2", "url3"]}
)
```

### Blocked Site Scraping

- [ ] Try WebFetch first (free)
- [ ] If blocked/empty, use Firecrawl with `waitFor` for JS-heavy sites

```
mcp__x402__fetch(
  url="https://enrichx402.com/api/firecrawl/scrape",
  method="POST",
  body={"url": "https://blocked-site.com/article", "waitFor": 3000}
)
```

## Cost Optimization

- **Use Exa contents** ($0.002) when you already have URLs
- **Use WebSearch/WebFetch first** (free) and fall back to x402 endpoints
- **Batch URL extraction** - pass multiple URLs to Exa contents
- **Limit results** - request only as many as needed

## Parallel Calls

Independent searches can run in parallel:

```
# These don't depend on each other
mcp__x402__fetch(url=".../exa/search", body={"query": "topic A"})
mcp__x402__fetch(url=".../exa/search", body={"query": "topic B"})
```
