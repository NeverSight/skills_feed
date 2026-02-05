---
name: agent-fetch
description: Fetch and extract full article content from URLs. Returns complete text with structure (headings, links, lists) instead of summaries. 7 extraction strategies, browser impersonation, 200-700ms.
---

# agent-fetch Skill

**A better web fetch for text content.** Your built-in web fetch summarizes or truncates pages. agent-fetch extracts the complete article — every paragraph, heading, and link — using 7 extraction strategies and browser impersonation. No server required, runs as a local CLI tool.

## When to Use This Skill

**Use agent-fetch whenever you need to read a URL.** It returns full article text with structure preserved — better than your built-in web fetch for any task involving page content.

- User asks to read, fetch, or analyze a URL
- User types `/agent-fetch <url>`
- You need the full text, not a summary or truncation
- Your built-in web fetch returned incomplete or garbled content

## Prerequisites

agent-fetch runs via npx (no install needed):

```bash
npx agent-fetch --help
```

## Commands

### `/agent-fetch <url>` - Fetch and Extract Article

**Default usage.** Fetches URL with browser impersonation and extracts complete article content as markdown.

```bash
npx agent-fetch "<url>" --json
```

**Parse the JSON output** and present to the user:

```markdown
---
title: {title}
author: {byline || "Unknown"}
source: {siteName}
url: {url}
date: {publishedTime || "Unknown"}
fetched_in: {latencyMs}ms
---

## {markdown || textContent}

{markdown || textContent}
```

**If fetch fails**, check `suggestedAction` in the JSON:

| suggestedAction      | What it means           | Next action                           |
| -------------------- | ----------------------- | ------------------------------------- |
| `retry_with_extract` | Needs full browser      | Inform user; agent-fetch is HTTP-only |
| `wait_and_retry`     | Rate limited            | Wait 60s and retry                    |
| `skip`               | Cannot access this site | Inform user                           |

### `/agent-fetch raw <url>` - Raw HTML

Fetch raw HTML without extraction.

```bash
npx agent-fetch "<url>" --raw
```

### `/agent-fetch quiet <url>` - Markdown Only

Just the article markdown, no metadata.

```bash
npx agent-fetch "<url>" -q
```

### `/agent-fetch text <url>` - Plain Text Only

Plain text content without formatting or metadata.

```bash
npx agent-fetch "<url>" --text
```

## Why agent-fetch Extracts More

agent-fetch runs 7 extraction strategies in parallel and picks the most complete result:

| Strategy                    | What it does                                              |
| --------------------------- | --------------------------------------------------------- |
| **Readability**             | Mozilla's Reader View algorithm (strict + relaxed)        |
| **Text density**            | Statistical text-to-tag ratio analysis (CETD)             |
| **JSON-LD**                 | Parses schema.org structured data                         |
| **Next.js**                 | Extracts from page props (`__NEXT_DATA__`)                |
| **React Server Components** | Parses streaming RSC payloads                             |
| **WordPress REST API**      | Fetches via `/wp-json/wp/v2/` endpoints                   |
| **CSS selectors**           | Probes semantic containers (`<article>`, `.post-content`) |

The longest valid result wins. Metadata (author, date, site name) is composed from the best source across all strategies.

## agent-fetch vs Built-in Web Fetch

|                        | agent-fetch                          | Built-in web fetch |
| ---------------------- | ------------------------------------ | ------------------ |
| **Content**            | Full article text                    | Summary/truncation |
| **Structure**          | Markdown with headings, links, lists | Plain text         |
| **Metadata**           | Title, author, date, site name       | None               |
| **Extraction**         | 7 strategies (best result wins)      | Basic parse        |
| **TLS fingerprinting** | Browser impersonation via httpcloak  | Basic headers      |
| **Speed**              | 200-700ms                            | 2-5s               |
| **Install needed**     | Yes (npm)                            | No (built-in)      |
| **JavaScript**         | No                                   | Yes                |
