---
name: web-search
description: >-
  Web search and content extraction using ddgs (multi-engine metasearch). No API keys required.
  Use when: searching documentation, facts, current information, news, fetching web content.
  Triggers: search the web, look up, find information, web search, news search, fetch page.
---

# Web Search

Web search and content extraction using [ddgs](https://github.com/deedy5/ddgs) — a multi-engine metasearch CLI.
No API keys, no signup, no browser required.

## Setup

Install ddgs (run once):

```bash
uv tool install ddgs
```

Install Node.js dependencies for content extraction (run once):

```bash
cd {baseDir}
npm install
```

## Search

```bash
{baseDir}/search.js "query"                         # Basic search (5 results)
{baseDir}/search.js "query" -n 10                   # More results
{baseDir}/search.js "query" --content               # Include page content as markdown
{baseDir}/search.js "query" -t w                    # Results from last week
{baseDir}/search.js "query" -t m                    # Results from last month
{baseDir}/search.js "query" -r es-es                # Results in Spanish
{baseDir}/search.js "query" -b google               # Use Google backend
{baseDir}/search.js "query" -n 3 --content          # Combined options
```

### Options

- `-n <num>` — Number of results (default: 5)
- `--content` — Fetch and include page content as markdown
- `-r <region>` — Region code: `us-en`, `es-es`, `de-de`, `fr-fr`, etc. (default: none)
- `-t <timelimit>` — Filter by time: `d` (day), `w` (week), `m` (month), `y` (year)
- `-b <backend>` — Search backend: `auto`, `all`, `bing`, `brave`, `duckduckgo`, `google`, `mojeek`, `yandex`, `yahoo`, `wikipedia` (default: auto)

## News Search

```bash
{baseDir}/search.js --news "query"                  # News search
{baseDir}/search.js --news "query" -n 10 -t w       # News from last week
{baseDir}/search.js --news "query" --content         # News with full article content
```

News backends: `auto`, `all`, `bing`, `duckduckgo`, `yahoo`

## Extract Page Content

```bash
{baseDir}/content.js https://example.com/article
```

Fetches a URL and extracts readable content as markdown.

## Output Format

### Text search

```text
--- Result 1 ---
Title: Page Title
Link: https://example.com/page
Snippet: Description from search results
Content: (if --content flag used)
  Markdown content extracted from the page...

--- Result 2 ---
...
```

### News search

```text
--- Result 1 ---
Title: Article Title
Link: https://news.example.com/article
Date: 2026-02-08T10:18:00+00:00
Source: Reuters
Snippet: Article summary...
Content: (if --content flag used)
  Full article as markdown...

--- Result 2 ---
...
```

## When to Use

- Searching for documentation or API references
- Looking up facts or current information
- News search for recent events
- Fetching content from specific URLs
- Any task requiring web search without interactive browsing
- When no API key is available (unlike Brave Search)
