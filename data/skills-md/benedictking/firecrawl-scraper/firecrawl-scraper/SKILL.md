---
name: firecrawl-scraper
version: 1.0.0
author: BenedictKing
description: "Web scraping skill using Firecrawl API for deep content extraction, format conversion, and page interaction. Use when you need to scrape web pages, extract structured data, take screenshots, parse PDFs, or crawl entire websites. Triggers: firecrawl, scrape, extract content, screenshot, parse pdf, crawl website, 抓取网页, 提取内容, 网页截图"
allowed-tools:
  - Task
  - Bash
  - Read
  - Write
user-invocable: true
---

# Firecrawl Scraper Skill

## Trigger Conditions & Endpoint Selection

Choose Firecrawl endpoint based on user intent:

- **scrape**: Need to extract content from a single web page (markdown, html, json, screenshot, pdf)
- **crawl**: Need to crawl entire website with depth control and path filtering
- **map**: Need to quickly get a list of all URLs on a website
- **batch-scrape**: Need to scrape multiple URLs in parallel
- **crawl-status**: Given crawl job ID, check crawl progress/results (optional `--wait`)

## Recommended Architecture (Main Skill + Sub-skill)

This skill uses a two-phase architecture:

1. **Main skill (current context)**: Understand user question → Choose endpoint → Assemble JSON payload
2. **Sub-skill (fork context)**: Only responsible for HTTP call execution, avoiding conversation history token waste

## Execution Method

Use Task tool to invoke `firecrawl-fetcher` sub-skill, passing command and JSON (stdin):

```
Task parameters:
- subagent_type: Bash
- description: "Call Firecrawl API"
- prompt: cat <<'JSON' | node .claude/skills/firecrawl-scraper/firecrawl-api.js <scrape|crawl|map|batch-scrape|crawl-status> [--wait]
  { ...payload... }
  JSON
```

## Payload Examples

### 1) Scrape Single Page

```bash
cat <<'JSON' | node .claude/skills/firecrawl-scraper/firecrawl-api.js scrape
{
  "url": "https://example.com",
  "formats": ["markdown", "links"],
  "onlyMainContent": true,
  "includeTags": [],
  "excludeTags": ["nav", "footer"],
  "waitFor": 0,
  "timeout": 30000
}
JSON
```

**Available formats:**
- `"markdown"`, `"html"`, `"rawHtml"`, `"links"`, `"images"`, `"summary"`
- `{"type": "json", "prompt": "Extract product info", "schema": {...}}`
- `{"type": "screenshot", "fullPage": true, "quality": 85}`

### 2) Scrape with Actions (Page Interaction)

```bash
cat <<'JSON' | node .claude/skills/firecrawl-scraper/firecrawl-api.js scrape
{
  "url": "https://example.com",
  "formats": ["markdown"],
  "actions": [
    {"type": "wait", "milliseconds": 2000},
    {"type": "click", "selector": "#load-more"},
    {"type": "wait", "milliseconds": 1000},
    {"type": "scroll", "direction": "down", "amount": 500}
  ]
}
JSON
```

**Available actions:**
- `wait`, `click`, `write`, `press`, `scroll`, `screenshot`, `scrape`, `executeJavascript`

### 3) Parse PDF

```bash
cat <<'JSON' | node .claude/skills/firecrawl-scraper/firecrawl-api.js scrape
{
  "url": "https://example.com/document.pdf",
  "formats": ["markdown"],
  "parsers": ["pdf"]
}
JSON
```

### 4) Extract Structured JSON

```bash
cat <<'JSON' | node .claude/skills/firecrawl-scraper/firecrawl-api.js scrape
{
  "url": "https://example.com/product",
  "formats": [
    {
      "type": "json",
      "prompt": "Extract product information",
      "schema": {
        "type": "object",
        "properties": {
          "name": {"type": "string"},
          "price": {"type": "number"},
          "description": {"type": "string"}
        },
        "required": ["name", "price"]
      }
    }
  ]
}
JSON
```

### 5) Crawl Entire Website

```bash
cat <<'JSON' | node .claude/skills/firecrawl-scraper/firecrawl-api.js crawl
{
  "url": "https://docs.example.com",
  "formats": ["markdown"],
  "includePaths": ["^/docs/.*"],
  "excludePaths": ["^/blog/.*"],
  "maxDiscoveryDepth": 3,
  "limit": 100,
  "allowExternalLinks": false,
  "allowSubdomains": false
}
JSON
```

### 5.1) Crawl + Wait for Completion

```bash
cat <<'JSON' | node .claude/skills/firecrawl-scraper/firecrawl-api.js crawl --wait
{
  "url": "https://docs.example.com",
  "formats": ["markdown"],
  "limit": 100
}
JSON
```

### 6) Map Website URLs

```bash
cat <<'JSON' | node .claude/skills/firecrawl-scraper/firecrawl-api.js map
{
  "url": "https://example.com",
  "search": "documentation",
  "limit": 5000
}
JSON
```

### 7) Batch Scrape Multiple URLs

```bash
cat <<'JSON' | node .claude/skills/firecrawl-scraper/firecrawl-api.js batch-scrape
{
  "urls": [
    "https://example.com/page1",
    "https://example.com/page2",
    "https://example.com/page3"
  ],
  "formats": ["markdown"]
}
JSON
```

### 8) Check Crawl Status

```bash
node .claude/skills/firecrawl-scraper/firecrawl-api.js crawl-status <crawl-id>
```

Wait for completion:

```bash
node .claude/skills/firecrawl-scraper/firecrawl-api.js crawl-status <crawl-id> --wait
```

## Key Features

### Formats
- **markdown**: Clean markdown content
- **html**: Parsed HTML
- **rawHtml**: Original HTML
- **links**: All links on page
- **images**: All images on page
- **summary**: AI-generated summary
- **json**: Structured data extraction with schema
- **screenshot**: Page screenshot (PNG)

### Content Control
- `onlyMainContent`: Extract only main content (default: true)
- `includeTags`: CSS selectors to include
- `excludeTags`: CSS selectors to exclude
- `waitFor`: Wait time before scraping (ms)
- `maxAge`: Cache duration (default: 48 hours)

### Actions (Browser Automation)
- `wait`: Wait for specified time
- `click`: Click element by selector
- `write`: Input text into field
- `press`: Press keyboard key
- `scroll`: Scroll page
- `executeJavascript`: Run custom JS

### Crawl Options
- `includePaths`: Regex patterns to include
- `excludePaths`: Regex patterns to exclude
- `maxDiscoveryDepth`: Maximum crawl depth
- `limit`: Maximum pages to crawl
- `allowExternalLinks`: Follow external links
- `allowSubdomains`: Follow subdomains

## Environment Variables & API Key

Two ways to configure API Key (priority: environment variable > `.env`):

1. Environment variable: `FIRECRAWL_API_KEY`
2. `.env` file: Place in `.claude/skills/firecrawl-scraper/.env`, can copy from `.env.example`

## Response Format

All endpoints return JSON with:
- `success`: Boolean indicating success
- `data`: Extracted content (format depends on endpoint)
- For crawl: Returns job ID, use `crawl-status` (or GET /v2/crawl/{id}) to check status
