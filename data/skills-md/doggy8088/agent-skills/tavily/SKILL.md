---
name: tavily
description: Use this skill for web search, extraction, mapping, crawling, and research via Tavily’s REST API when web searches are needed and no built-in tool is available, or when Tavily’s LLM-friendly format is beneficial.
---

# Tavily

## Purpose

Provide a curl-based interface to Tavily’s REST API for web search, extraction, mapping, crawling, and optional research. Return structured results suitable for LLM workflows and multi-step investigations.

## When to Use

- Use when a task needs live web information, site extraction, mapping, or crawling.
- Use when web searches are needed and no built-in tool is available, or when Tavily’s LLM-friendly output (summaries, chunks, sources, citations) is beneficial.
- Use when a task requires structured search results, extraction, or site discovery from Tavily.

## Required Environment

- Require `TAVILY_API_KEY` in the environment.
- If `TAVILY_API_KEY` is missing, prompt the user to provide the API key before proceeding.

## Base URL and Auth

- Base URL: `https://api.tavily.com`
- Authentication: `Authorization: Bearer $TAVILY_API_KEY`
- Content type: `Content-Type: application/json`
- Optional project tracking: add `X-Project-ID: <project-id>` if project attribution is needed.

## Tool Mapping (Tavily REST)

### 1) search → POST /search

Use for web search with optional answer and content extraction.

Recommended minimal request:

```bash
curl -sS -X POST "https://api.tavily.com/search" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TAVILY_API_KEY" \
  -d '{
    "query": "<query>",
    "search_depth": "basic",
    "max_results": 5,
    "include_answer": true,
    "include_raw_content": false,
    "include_images": false
  }'
```

Key parameters (all optional unless noted):
- `query` (required): search text
- `search_depth`: `basic` | `advanced` | `fast` | `ultra-fast`
- `chunks_per_source`: 1–3 (advanced only)
- `max_results`: 0–20
- `topic`: `general` | `news` | `finance`
- `time_range`: `day|week|month|year|d|w|m|y`
- `start_date`, `end_date`: `YYYY-MM-DD`
- `include_answer`: `false` | `true` | `basic` | `advanced`
- `include_raw_content`: `false` | `true` | `markdown` | `text`
- `include_images`: boolean
- `include_image_descriptions`: boolean
- `include_favicon`: boolean
- `include_domains`, `exclude_domains`: string arrays
- `country`: country name (general topic only)
- `auto_parameters`: boolean
- `include_usage`: boolean

Expected response fields:
- `answer` (if requested), `results[]` with `title`, `url`, `content`, `score`, `raw_content` (optional), `favicon` (optional)
- `response_time`, `usage`, `request_id`

### 2) extract → POST /extract

Use for extracting content from specific URLs.

```bash
curl -sS -X POST "https://api.tavily.com/extract" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TAVILY_API_KEY" \
  -d '{
    "urls": ["https://example.com/article"],
    "query": "<optional intent for reranking>",
    "chunks_per_source": 3,
    "extract_depth": "basic",
    "format": "markdown",
    "include_images": false,
    "include_favicon": false
  }'
```

Key parameters:
- `urls` (required): array of URLs
- `query`: rerank chunks by intent
- `chunks_per_source`: 1–5 (only when `query` provided)
- `extract_depth`: `basic` | `advanced`
- `format`: `markdown` | `text`
- `timeout`: 1–60 seconds
- `include_usage`: boolean

Expected response fields:
- `results[]` with `url`, `raw_content`, `images`, `favicon`
- `failed_results[]`, `response_time`, `usage`, `request_id`

### 3) map → POST /map

Use for generating a site map (URL discovery only).

```bash
curl -sS -X POST "https://api.tavily.com/map" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TAVILY_API_KEY" \
  -d '{
    "url": "https://docs.tavily.com",
    "max_depth": 1,
    "max_breadth": 20,
    "limit": 50,
    "allow_external": true
  }'
```

Key parameters:
- `url` (required)
- `instructions`: natural language guidance (raises cost)
- `max_depth`: 1–5
- `max_breadth`: 1+
- `limit`: 1+
- `select_paths`, `select_domains`, `exclude_paths`, `exclude_domains`: arrays of regex strings
- `allow_external`: boolean
- `timeout`: 10–150 seconds
- `include_usage`: boolean

Expected response fields:
- `base_url`, `results[]` (list of URLs), `response_time`, `usage`, `request_id`

### 4) crawl → POST /crawl

Use for site traversal with built-in extraction.

```bash
curl -sS -X POST "https://api.tavily.com/crawl" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TAVILY_API_KEY" \
  -d '{
    "url": "https://docs.tavily.com",
    "instructions": "Find all pages about the Python SDK",
    "max_depth": 1,
    "max_breadth": 20,
    "limit": 50,
    "extract_depth": "basic",
    "format": "markdown",
    "include_images": false
  }'
```

Key parameters:
- `url` (required)
- `instructions`: optional; raises cost and enables `chunks_per_source`
- `chunks_per_source`: 1–5 (only with `instructions`)
- `max_depth`, `max_breadth`, `limit`: same as map
- `extract_depth`: `basic` | `advanced`
- `format`: `markdown` | `text`
- `include_images`, `include_favicon`, `allow_external`
- `timeout`: 10–150 seconds
- `include_usage`: boolean

Expected response fields:
- `base_url`, `results[]` with `url`, `raw_content`, `favicon`
- `response_time`, `usage`, `request_id`

## Optional Research Workflow (Deep Investigation)

Use when a query needs multi-step analysis and citations.

### create research task → POST /research

```bash
curl -sS -X POST "https://api.tavily.com/research" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TAVILY_API_KEY" \
  -d '{
    "input": "<research question>",
    "model": "auto",
    "stream": false,
    "citation_format": "numbered"
  }'
```

Expected response fields:
- `request_id`, `created_at`, `status` (pending), `input`, `model`, `response_time`

### get research status → GET /research/{request_id}

```bash
curl -sS -X GET "https://api.tavily.com/research/<request_id>" \
  -H "Authorization: Bearer $TAVILY_API_KEY"
```

Expected response fields:
- `status`: `completed`
- `content`: report text or structured object
- `sources[]`: `{ title, url, favicon }`

### streaming research (SSE)

Set `"stream": true` in the POST body and use curl with `-N` to stream events:

```bash
curl -N -X POST "https://api.tavily.com/research" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TAVILY_API_KEY" \
  -d '{"input":"<question>","stream":true,"model":"pro"}'
```

Handle SSE events (tool calls, tool responses, content chunks, sources, done).

## Usage Notes

- Treat `search`, `extract`, `map`, and `crawl` as the primary endpoints for discovery and content retrieval.
- Return structured results with URLs, titles, and summaries for easy downstream use.
- Default to conservative parameters (`search_depth: basic`, `max_results: 5`) unless deeper recall is needed.
- Reuse consistent request bodies across calls to keep results predictable.

## Error Handling

- If any request returns 401/403, prompt for or re-check `TAVILY_API_KEY`.
- If timeouts occur, reduce `max_depth`/`limit` or use `search_depth: basic`.
- If responses are too large, lower `max_results` or `chunks_per_source`.
