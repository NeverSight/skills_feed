---
name: firecrawl
description: Firecrawl web scraping API via curl. Use this skill to scrape webpages, crawl websites, discover URLs, search the web, or extract structured data.
vm0_secrets:
  - FIRECRAWL_API_KEY
---

# Firecrawl

Use the Firecrawl API via direct `curl` calls to **scrape websites and extract data for AI**.

> Official docs: `https://docs.firecrawl.dev/`

---

## When to Use

Use this skill when you need to:

- **Scrape a webpage** and convert to markdown/HTML
- **Crawl an entire website** and extract all pages
- **Discover all URLs** on a website
- **Search the web** and get full page content
- **Extract structured data** using AI

---

## Prerequisites

1. Sign up at https://www.firecrawl.dev/
2. Get your API key from the dashboard

```bash
export FIRECRAWL_API_KEY="fc-your-api-key"
```

---


> **Important:** When using `$VAR` in a command that pipes to another command, wrap the command containing `$VAR` in `bash -c '...'`. Due to a Claude Code bug, environment variables are silently cleared when pipes are used directly.
> ```bash
> bash -c 'curl -s "https://api.example.com" -H "Authorization: Bearer $API_KEY"'
> ```

## How to Use

All examples below assume you have `FIRECRAWL_API_KEY` set.

Base URL: `https://api.firecrawl.dev/v1`

---

## 1. Scrape - Single Page

Extract content from a single webpage.

### Basic Scrape

Write to `/tmp/firecrawl_request.json`:

```json
{
  "url": "https://example.com",
  "formats": ["markdown"]
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.firecrawl.dev/v1/scrape" -H "Authorization: Bearer ${FIRECRAWL_API_KEY}" -H "Content-Type: application/json" -d @/tmp/firecrawl_request.json'
```

### Scrape with Options

Write to `/tmp/firecrawl_request.json`:

```json
{
  "url": "https://docs.example.com/api",
  "formats": ["markdown"],
  "onlyMainContent": true,
  "timeout": 30000
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.firecrawl.dev/v1/scrape" -H "Authorization: Bearer ${FIRECRAWL_API_KEY}" -H "Content-Type: application/json" -d @/tmp/firecrawl_request.json' | jq '.data.markdown'
```

### Get HTML Instead

Write to `/tmp/firecrawl_request.json`:

```json
{
  "url": "https://example.com",
  "formats": ["html"]
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.firecrawl.dev/v1/scrape" -H "Authorization: Bearer ${FIRECRAWL_API_KEY}" -H "Content-Type: application/json" -d @/tmp/firecrawl_request.json' | jq '.data.html'
```

### Get Screenshot

Write to `/tmp/firecrawl_request.json`:

```json
{
  "url": "https://example.com",
  "formats": ["screenshot"]
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.firecrawl.dev/v1/scrape" -H "Authorization: Bearer ${FIRECRAWL_API_KEY}" -H "Content-Type: application/json" -d @/tmp/firecrawl_request.json' | jq '.data.screenshot'
```

**Scrape Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `url` | string | URL to scrape (required) |
| `formats` | array | `markdown`, `html`, `rawHtml`, `screenshot`, `links` |
| `onlyMainContent` | boolean | Skip headers/footers |
| `timeout` | number | Timeout in milliseconds |

---

## 2. Crawl - Entire Website

Crawl all pages of a website (async operation).

### Start a Crawl

Write to `/tmp/firecrawl_request.json`:

```json
{
  "url": "https://example.com",
  "limit": 50,
  "maxDepth": 2
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.firecrawl.dev/v1/crawl" -H "Authorization: Bearer ${FIRECRAWL_API_KEY}" -H "Content-Type: application/json" -d @/tmp/firecrawl_request.json'
```

**Response:**

```json
{
  "success": true,
  "id": "crawl-job-id-here"
}
```

### Check Crawl Status

Replace `<job-id>` with the actual job ID returned from the crawl request:

```bash
bash -c 'curl -s "https://api.firecrawl.dev/v1/crawl/<job-id>" -H "Authorization: Bearer ${FIRECRAWL_API_KEY}"' | jq '{status, completed, total}'
```

### Get Crawl Results

Replace `<job-id>` with the actual job ID:

```bash
bash -c 'curl -s "https://api.firecrawl.dev/v1/crawl/<job-id>" -H "Authorization: Bearer ${FIRECRAWL_API_KEY}"' | jq '.data[] | {url: .metadata.url, title: .metadata.title}'
```

### Crawl with Path Filters

Write to `/tmp/firecrawl_request.json`:

```json
{
  "url": "https://blog.example.com",
  "limit": 20,
  "maxDepth": 3,
  "includePaths": ["/posts/*"],
  "excludePaths": ["/admin/*", "/login"]
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.firecrawl.dev/v1/crawl" -H "Authorization: Bearer ${FIRECRAWL_API_KEY}" -H "Content-Type: application/json" -d @/tmp/firecrawl_request.json'
```

**Crawl Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `url` | string | Starting URL (required) |
| `limit` | number | Max pages to crawl (default: 100) |
| `maxDepth` | number | Max crawl depth (default: 3) |
| `includePaths` | array | Paths to include (e.g., `/blog/*`) |
| `excludePaths` | array | Paths to exclude |

---

## 3. Map - URL Discovery

Get all URLs from a website quickly.

### Basic Map

Write to `/tmp/firecrawl_request.json`:

```json
{
  "url": "https://example.com"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.firecrawl.dev/v1/map" -H "Authorization: Bearer ${FIRECRAWL_API_KEY}" -H "Content-Type: application/json" -d @/tmp/firecrawl_request.json' | jq '.links[:10]'
```

### Map with Search Filter

Write to `/tmp/firecrawl_request.json`:

```json
{
  "url": "https://shop.example.com",
  "search": "product",
  "limit": 500
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.firecrawl.dev/v1/map" -H "Authorization: Bearer ${FIRECRAWL_API_KEY}" -H "Content-Type: application/json" -d @/tmp/firecrawl_request.json' | jq '.links'
```

**Map Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `url` | string | Website URL (required) |
| `search` | string | Filter URLs containing keyword |
| `limit` | number | Max URLs to return (default: 1000) |

---

## 4. Search - Web Search

Search the web and get full page content.

### Basic Search

Write to `/tmp/firecrawl_request.json`:

```json
{
  "query": "AI news 2024",
  "limit": 5
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.firecrawl.dev/v1/search" -H "Authorization: Bearer ${FIRECRAWL_API_KEY}" -H "Content-Type: application/json" -d @/tmp/firecrawl_request.json' | jq '.data[] | {title: .metadata.title, url: .url}'
```

### Search with Full Content

Write to `/tmp/firecrawl_request.json`:

```json
{
  "query": "machine learning tutorials",
  "limit": 3,
  "scrapeOptions": {
    "formats": ["markdown"]
  }
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.firecrawl.dev/v1/search" -H "Authorization: Bearer ${FIRECRAWL_API_KEY}" -H "Content-Type: application/json" -d @/tmp/firecrawl_request.json' | jq '.data[] | {title: .metadata.title, content: .markdown[:500]}'
```

**Search Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `query` | string | Search query (required) |
| `limit` | number | Number of results (default: 10) |
| `scrapeOptions` | object | Options for scraping results |

---

## 5. Extract - AI Data Extraction

Extract structured data from pages using AI.

### Basic Extract

Write to `/tmp/firecrawl_request.json`:

```json
{
  "urls": ["https://example.com/product/123"],
  "prompt": "Extract the product name, price, and description"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.firecrawl.dev/v1/extract" -H "Authorization: Bearer ${FIRECRAWL_API_KEY}" -H "Content-Type: application/json" -d @/tmp/firecrawl_request.json' | jq '.data'
```

### Extract with Schema

Write to `/tmp/firecrawl_request.json`:

```json
{
  "urls": ["https://example.com/product/123"],
  "prompt": "Extract product information",
  "schema": {
    "type": "object",
    "properties": {
      "name": {"type": "string"},
      "price": {"type": "number"},
      "currency": {"type": "string"},
      "inStock": {"type": "boolean"}
    }
  }
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.firecrawl.dev/v1/extract" -H "Authorization: Bearer ${FIRECRAWL_API_KEY}" -H "Content-Type: application/json" -d @/tmp/firecrawl_request.json' | jq '.data'
```

### Extract from Multiple URLs

Write to `/tmp/firecrawl_request.json`:

```json
{
  "urls": [
    "https://example.com/product/1",
    "https://example.com/product/2"
  ],
  "prompt": "Extract product name and price"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.firecrawl.dev/v1/extract" -H "Authorization: Bearer ${FIRECRAWL_API_KEY}" -H "Content-Type: application/json" -d @/tmp/firecrawl_request.json' | jq '.data'
```

**Extract Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `urls` | array | URLs to extract from (required) |
| `prompt` | string | Description of data to extract (required) |
| `schema` | object | JSON schema for structured output |

---

## Practical Examples

### Scrape Documentation

Write to `/tmp/firecrawl_request.json`:

```json
{
  "url": "https://docs.python.org/3/tutorial/",
  "formats": ["markdown"],
  "onlyMainContent": true
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.firecrawl.dev/v1/scrape" -H "Authorization: Bearer ${FIRECRAWL_API_KEY}" -H "Content-Type: application/json" -d @/tmp/firecrawl_request.json' | jq -r '.data.markdown' > python-tutorial.md
```

### Find All Blog Posts

Write to `/tmp/firecrawl_request.json`:

```json
{
  "url": "https://blog.example.com",
  "search": "post"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.firecrawl.dev/v1/map" -H "Authorization: Bearer ${FIRECRAWL_API_KEY}" -H "Content-Type: application/json" -d @/tmp/firecrawl_request.json' | jq -r '.links[]'
```

### Research a Topic

Write to `/tmp/firecrawl_request.json`:

```json
{
  "query": "best practices REST API design 2024",
  "limit": 5,
  "scrapeOptions": {"formats": ["markdown"]}
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.firecrawl.dev/v1/search" -H "Authorization: Bearer ${FIRECRAWL_API_KEY}" -H "Content-Type: application/json" -d @/tmp/firecrawl_request.json' | jq '.data[] | {title: .metadata.title, url: .url}'
```

### Extract Pricing Data

Write to `/tmp/firecrawl_request.json`:

```json
{
  "urls": ["https://example.com/pricing"],
  "prompt": "Extract all pricing tiers with name, price, and features"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.firecrawl.dev/v1/extract" -H "Authorization: Bearer ${FIRECRAWL_API_KEY}" -H "Content-Type: application/json" -d @/tmp/firecrawl_request.json' | jq '.data'
```

### Poll Crawl Until Complete

Replace `<job-id>` with the actual job ID:

```bash
while true; do
  STATUS="$(bash -c 'curl -s "https://api.firecrawl.dev/v1/crawl/<job-id>" -H "Authorization: Bearer ${FIRECRAWL_API_KEY}"' | jq -r '.status')"
  echo "Status: $STATUS"
  [ "$STATUS" = "completed" ] && break
  sleep 5
done
```

---

## Response Format

### Scrape Response

```json
{
  "success": true,
  "data": {
  "markdown": "# Page Title\n\nContent...",
  "metadata": {
  "title": "Page Title",
  "description": "...",
  "url": "https://..."
  }
  }
}
```

### Crawl Status Response

```json
{
  "success": true,
  "status": "completed",
  "completed": 50,
  "total": 50,
  "data": [...]
}
```

---

## Guidelines

1. **Rate limits**: Add delays between requests to avoid 429 errors
2. **Crawl limits**: Set reasonable `limit` values to control API usage
3. **Main content**: Use `onlyMainContent: true` for cleaner output
4. **Async crawls**: Large crawls are async; poll `/crawl/{id}` for status
5. **Extract prompts**: Be specific for better AI extraction results
6. **Check success**: Always check `success` field in responses
