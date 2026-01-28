---
name: tavily
description: Tavily AI search API integration via curl. Use this skill to perform live web search and RAG-style retrieval.
vm0_secrets:
  - TAVILY_API_KEY
---

# Tavily Search API

Use Tavily's search API via direct `curl` calls to perform **live web search**, ideal for powering retrieval-augmented generation (RAG) for LLMs and agents.

> Official documentation: `https://docs.tavily.com/`

---

## When to Use

Use this skill when you need:

- **Fresh, up-to-date information** (news, trends, ongoing events)
- **Search results with sources/links** to ground LLM or agent answers
- **Research / desk research** inside automation workflows
- A **reliable retrieval layer** for RAG, combined with skills like Notion or Firecrawl

---

## Prerequisites

1. Sign up for Tavily and create an API key
2. Store your Tavily API key in the environment variable `TAVILY_API_KEY`

Set it in your local shell or runtime environment, for example:

```bash
export TAVILY_API_KEY="tvly-xxxxxxxxxxxxxxxx"
```

---


> **Important:** When using `$VAR` in a command that pipes to another command, wrap the command containing `$VAR` in `bash -c '...'`. Due to a Claude Code bug, environment variables are silently cleared when pipes are used directly.
> ```bash
> bash -c 'curl -s "https://api.example.com" -H "Authorization: Bearer $API_KEY"' | jq '.results[] | {title, url}'
> ```

## How to Use

All examples below assume you have `TAVILY_API_KEY` set in your environment.
The base endpoint for the Tavily search API is a `POST` request to:

- `https://api.tavily.com/search`

with a JSON body.

---

### 1. Basic Search

Write to `/tmp/tavily_request.json`:

```json
{
  "query": "2025 AI Trending",
  "search_depth": "basic",
  "max_results": 5
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.tavily.com/search" --header "Content-Type: application/json" --header "Authorization: Bearer ${TAVILY_API_KEY}" -d @/tmp/tavily_request.json'
```

**Key parameters:**

- `query`: Search query or natural language question
- `search_depth`:
  - `"basic"` – faster, good for most use cases
  - `"advanced"` – deeper search and higher recall
- `max_results`: Maximum number of results to return (e.g. 3 / 5 / 10)

---

### 2. Advanced Search

Write to `/tmp/tavily_request.json`:

```json
{
  "query": "serverless SaaS pricing best practices",
  "search_depth": "advanced",
  "max_results": 8,
  "include_answer": true,
  "include_domains": ["docs.aws.amazon.com", "cloud.google.com"],
  "exclude_domains": ["reddit.com", "twitter.com"],
  "include_raw_content": false
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.tavily.com/search" --header "Content-Type: application/json" --header "Authorization: Bearer ${TAVILY_API_KEY}" -d @/tmp/tavily_request.json'
```

**Common advanced parameters:**

- `include_answer`: When `true`, Tavily returns a summarized `answer` field
- `include_domains`: Whitelist of domains to include
- `exclude_domains`: Blacklist of domains to exclude
- `include_raw_content`: Whether to include raw page content (HTML / raw text). Default is `false`.

---

### 3. Typical Response Structure (Example)

Tavily returns a JSON object similar to:

```json
{
  "answer": "Brief summary...",
  "results": [
  {
  "title": "Article title",
  "url": "https://example.com/article",
  "content": "Snippet or extracted content...",
  "score": 0.89
  }
  ]
}
```

In agents or automation flows you typically:

- Use `answer` as a concise, ready-to-use summary
- Iterate over `results` to extract `title` + `url` as references / citations

---

### 4. Using Tavily in n8n (HTTP Request Node)

To integrate Tavily in n8n with the HTTP Request node:

- **Method**: `POST`
- **URL**: `https://api.tavily.com/search`
- **Headers**:
  - `Content-Type`: `application/json`
  - `Authorization`: `Bearer {{ $env.TAVILY_API_KEY }}`
- **Body**: JSON, for example:

```json
{
  "query": "n8n self-hosted best practices",
  "search_depth": "basic",
  "max_results": 5
}
```

This lets you pipe Tavily search results into downstream nodes such as LLMs, Notion, Slack notifications, etc.

---

## Guidelines

1. **Use `advanced` only when necessary**: it consumes more resources and is best for deep research / high-value questions.
2. **Mind quotas and cost**: Tavily typically offers free tiers plus paid usage; in automation flows, add guards (filters, rate limits).
3. **Post-process results with an LLM**: use Tavily for retrieval, then let your LLM summarize, extract tables, or generate reports.
4. **Handle sensitive data carefully**: avoid sending raw secrets or PII directly in `query`; anonymize or mask when possible.
