---
name: tavily-web
version: 1.0.2
author: BenedictKing
description: "Web research skill using Tavily API for search, extract, crawl, map, and structured research tasks. Use when you need latest information, extract content from URLs, or discover site structure. Triggers: tavily, web search, search web, latest info, extract, crawl, map, research, 搜索网页, 查资料, 最新"
allowed-tools:
  - Task
  - Bash
  - Read
  - Write
user-invocable: true
---

# Tavily Web Skill

## Trigger Conditions & Endpoint Selection

Choose Tavily endpoint based on user intent:

- **search**: Need to "search web / latest info / find sources / find links"
- **extract**: Given URL(s), need to extract/summarize content
- **crawl**: Need to traverse site following instructions and scrape page content
- **map**: Need to discover site page list/structure (without full content or metadata only)
- **research**: Need structured research output following given `output_schema`

## Recommended Architecture (Main Skill + Sub-skill)

This skill uses a two-phase architecture:

1. **Main skill (current context)**: Understand user question → Choose endpoint → Assemble JSON payload
2. **Sub-skill (fork context)**: Only responsible for HTTP call execution, avoiding conversation history token waste

## Execution Method

Use Task tool to invoke `tavily-fetcher` sub-skill, passing command and JSON (stdin):

```
Task parameters:
- subagent_type: Bash
- description: "Call Tavily API"
- prompt: cat <<'JSON' | node .claude/skills/tavily-web/tavily-api.js <search|extract|crawl|map|research>
  { ...payload... }
  JSON
```

## Payload Examples (Based on Provided curl)

### 1) Search the web

```bash
cat <<'JSON' | node .claude/skills/tavily-web/tavily-api.js search
{
  "query": "who is Leo Messi?",
  "auto_parameters": false,
  "topic": "general",
  "search_depth": "basic",
  "chunks_per_source": 3,
  "max_results": 1,
  "time_range": null,
  "start_date": "2025-02-09",
  "end_date": "2025-12-29",
  "include_answer": false,
  "include_raw_content": false,
  "include_images": false,
  "include_image_descriptions": false,
  "include_favicon": false,
  "include_domains": [],
  "exclude_domains": [],
  "country": null,
  "include_usage": false
}
JSON
```

### 2) Extract webpages

```bash
cat <<'JSON' | node .claude/skills/tavily-web/tavily-api.js extract
{
  "urls": "https://en.wikipedia.org/wiki/Artificial_intelligence",
  "query": "<string>",
  "chunks_per_source": 3,
  "extract_depth": "basic",
  "include_images": false,
  "include_favicon": false,
  "format": "markdown",
  "timeout": "None",
  "include_usage": false
}
JSON
```

### 3) Crawl webpages

```bash
cat <<'JSON' | node .claude/skills/tavily-web/tavily-api.js crawl
{
  "url": "docs.tavily.com",
  "instructions": "Find all pages about the Python SDK",
  "chunks_per_source": 3,
  "max_depth": 1,
  "max_breadth": 20,
  "limit": 50,
  "select_paths": null,
  "select_domains": null,
  "exclude_paths": null,
  "exclude_domains": null,
  "allow_external": true,
  "include_images": false,
  "extract_depth": "basic",
  "format": "markdown",
  "include_favicon": false,
  "timeout": 150,
  "include_usage": false
}
JSON
```

### 4) Map webpages

```bash
cat <<'JSON' | node .claude/skills/tavily-web/tavily-api.js map
{
  "url": "docs.tavily.com",
  "instructions": "Find all pages about the Python SDK",
  "max_depth": 1,
  "max_breadth": 20,
  "limit": 50,
  "select_paths": null,
  "select_domains": null,
  "exclude_paths": null,
  "exclude_domains": null,
  "allow_external": true,
  "timeout": 150,
  "include_usage": false
}
JSON
```

### 5) Create Research Task

```bash
cat <<'JSON' | node .claude/skills/tavily-web/tavily-api.js research
{
  "input": "What are the latest developments in AI?",
  "model": "auto",
  "stream": false,
  "output_schema": {
    "properties": {
      "company": {
        "type": "string",
        "description": "The name of the company"
      },
      "key_metrics": {
        "type": "array",
        "description": "List of key performance metrics",
        "items": {
          "type": "string"
        }
      },
      "financial_details": {
        "type": "object",
        "description": "Detailed financial breakdown",
        "properties": {
          "operating_income": {
            "type": "number",
            "description": "Operating income for the period"
          }
        }
      }
    },
    "required": [
      "company"
    ]
  },
  "citation_format": "numbered"
}
JSON
```

## Environment Variables & API Key

Two ways to configure API Key (priority: environment variable > `.env`):

1. Environment variable: `TAVILY_API_KEY`
2. `.env` file: Place in `.claude/skills/tavily-web/.env`, can copy from `.env.example`
