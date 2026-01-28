---
name: perplexity
description: AI-powered search engine with real-time web grounding and citations
vm0_secrets:
  - PERPLEXITY_API_KEY
---

# Perplexity AI

AI search engine that provides real-time web-grounded answers with source citations. Unlike traditional search, Perplexity synthesizes information from multiple sources into coherent responses.

> Official docs: https://docs.perplexity.ai/

---

## When to Use

Use this skill when you need to:

- Get real-time information with source citations
- Research topics that require up-to-date web data
- Answer complex questions that need multi-source synthesis
- Perform academic or SEC filings research
- Get AI-generated summaries grounded in current web content

---

## Prerequisites

1. Create an account at https://perplexity.ai/
2. Navigate to API settings: https://perplexity.ai/account/api
3. Generate an API key

Set environment variable:

```bash
export PERPLEXITY_API_KEY="pplx-your-api-key"
```

---


> **Important:** When using `$VAR` in a command that pipes to another command, wrap the command containing `$VAR` in `bash -c '...'`. Due to a Claude Code bug, environment variables are silently cleared when pipes are used directly.
> ```bash
> bash -c 'curl -s "https://api.example.com" -H "Authorization: Bearer $API_KEY"' | jq .
> ```

## How to Use

### 1. Chat Completions (Recommended)

AI-powered Q&A with web search and citations. OpenAI SDK compatible.

**Basic query with sonar model:**

Write to `/tmp/perplexity_request.json`:

```json
{
  "model": "sonar",
  "messages": [
    {"role": "user", "content": "What is the current price of Bitcoin?"}
  ]
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.perplexity.ai/chat/completions" --header "Authorization: Bearer ${PERPLEXITY_API_KEY}" --header "Content-Type: application/json" -d @/tmp/perplexity_request.json'
```

**With system prompt:**

Write to `/tmp/perplexity_request.json`:

```json
{
  "model": "sonar",
  "messages": [
    {"role": "system", "content": "Be precise and concise. Answer in bullet points."},
    {"role": "user", "content": "What are the latest developments in AI?"}
  ]
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.perplexity.ai/chat/completions" --header "Authorization: Bearer ${PERPLEXITY_API_KEY}" --header "Content-Type: application/json" -d @/tmp/perplexity_request.json'
```

**Advanced query with sonar-pro:**

Write to `/tmp/perplexity_request.json`:

```json
{
  "model": "sonar-pro",
  "messages": [
    {"role": "user", "content": "Compare the latest iPhone and Samsung Galaxy flagship phones"}
  ],
  "temperature": 0.2,
  "web_search_options": {
    "search_context_size": "high"
  }
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.perplexity.ai/chat/completions" --header "Authorization: Bearer ${PERPLEXITY_API_KEY}" --header "Content-Type: application/json" -d @/tmp/perplexity_request.json'
```

### 2. Search with Domain Filter

Limit search to specific domains.

Write to `/tmp/perplexity_request.json`:

```json
{
  "model": "sonar",
  "messages": [
    {"role": "user", "content": "Latest research on transformer architectures"}
  ],
  "search_domain_filter": ["arxiv.org", "openai.com", "anthropic.com"]
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.perplexity.ai/chat/completions" --header "Authorization: Bearer ${PERPLEXITY_API_KEY}" --header "Content-Type: application/json" -d @/tmp/perplexity_request.json'
```

**Exclude domains (add `-` prefix):**

Write to `/tmp/perplexity_request.json`:

```json
{
  "model": "sonar",
  "messages": [
    {"role": "user", "content": "Best programming practices"}
  ],
  "search_domain_filter": ["-reddit.com", "-quora.com"]
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.perplexity.ai/chat/completions" --header "Authorization: Bearer ${PERPLEXITY_API_KEY}" --header "Content-Type: application/json" -d @/tmp/perplexity_request.json'
```

### 3. Search with Time Filter

Filter by recency.

Write to `/tmp/perplexity_request.json`:

```json
{
  "model": "sonar",
  "messages": [
    {"role": "user", "content": "Major tech news"}
  ],
  "search_recency_filter": "week"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.perplexity.ai/chat/completions" --header "Authorization: Bearer ${PERPLEXITY_API_KEY}" --header "Content-Type: application/json" -d @/tmp/perplexity_request.json'
```

**Filter by date range:**

Write to `/tmp/perplexity_request.json`:

```json
{
  "model": "sonar",
  "messages": [
    {"role": "user", "content": "AI announcements"}
  ],
  "search_after_date_filter": "12/01/2024",
  "search_before_date_filter": "12/31/2024"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.perplexity.ai/chat/completions" --header "Authorization: Bearer ${PERPLEXITY_API_KEY}" --header "Content-Type: application/json" -d @/tmp/perplexity_request.json'
```

### 4. Academic Search

Search academic sources.

Write to `/tmp/perplexity_request.json`:

```json
{
  "model": "sonar",
  "messages": [
    {"role": "user", "content": "Recent papers on large language model alignment"}
  ],
  "search_mode": "academic"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.perplexity.ai/chat/completions" --header "Authorization: Bearer ${PERPLEXITY_API_KEY}" --header "Content-Type: application/json" -d @/tmp/perplexity_request.json'
```

### 5. Raw Search API

Get raw search results without AI synthesis.

Write to `/tmp/perplexity_request.json`:

```json
{
  "query": "Claude AI Anthropic",
  "max_results": 5
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.perplexity.ai/search" --header "Authorization: Bearer ${PERPLEXITY_API_KEY}" --header "Content-Type: application/json" -d @/tmp/perplexity_request.json'
```

**With domain and time filters:**

Write to `/tmp/perplexity_request.json`:

```json
{
  "query": "machine learning tutorials",
  "max_results": 10,
  "search_domain_filter": ["github.com", "medium.com"],
  "search_recency_filter": "month",
  "country": "US"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.perplexity.ai/search" --header "Authorization: Bearer ${PERPLEXITY_API_KEY}" --header "Content-Type: application/json" -d @/tmp/perplexity_request.json'
```

### 6. Deep Research (Long-form)

For comprehensive research reports.

Write to `/tmp/perplexity_request.json`:

```json
{
  "model": "sonar-deep-research",
  "messages": [
    {"role": "user", "content": "Write a comprehensive analysis of the electric vehicle market in 2024"}
  ],
  "reasoning_effort": "high"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.perplexity.ai/chat/completions" --header "Authorization: Bearer ${PERPLEXITY_API_KEY}" --header "Content-Type: application/json" -d @/tmp/perplexity_request.json'
```

### 7. Reasoning Model

For complex problem-solving.

Write to `/tmp/perplexity_request.json`:

```json
{
  "model": "sonar-reasoning-pro",
  "messages": [
    {"role": "user", "content": "Analyze the pros and cons of microservices vs monolithic architecture for a startup"}
  ]
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.perplexity.ai/chat/completions" --header "Authorization: Bearer ${PERPLEXITY_API_KEY}" --header "Content-Type: application/json" -d @/tmp/perplexity_request.json'
```

---

## Models

| Model | Description | Best For |
|-------|-------------|----------|
| `sonar` | Lightweight, cost-effective | Quick facts, news, simple Q&A |
| `sonar-pro` | Advanced search, deeper understanding | Complex queries, detailed research |
| `sonar-reasoning-pro` | Multi-step reasoning with search | Problem-solving, analysis |
| `sonar-deep-research` | Exhaustive research, reports | Academic research, market analysis |

---

## Response Format

Chat completions return:

```json
{
  "id": "uuid",
  "model": "sonar",
  "choices": [
  {
  "message": {
  "role": "assistant",
  "content": "The answer with [1] citations..."
  }
  }
  ],
  "citations": ["https://source1.com", "https://source2.com"],
  "search_results": [
  {
  "title": "Source Title",
  "url": "https://source.com",
  "snippet": "Relevant excerpt..."
  }
  ],
  "usage": {
  "prompt_tokens": 10,
  "completion_tokens": 150,
  "total_tokens": 160
  }
}
```

---

## Guidelines

1. **Model Selection**: Use `sonar` for simple queries, `sonar-pro` for complex ones
2. **Cost Optimization**: Lower `search_context_size` reduces costs (low/medium/high)
3. **Domain Filters**: Limit to 20 domains max; use `-` prefix to exclude
4. **Recency Filters**: Options are `day`, `week`, `month`, `year`
5. **Temperature**: Lower (0.1-0.3) for factual queries, higher for creative
6. **Rate Limits**: Vary by tier; check https://docs.perplexity.ai/guides/rate-limits-usage-tiers
7. **Citations**: Response includes numbered citations `[1]` that map to `citations` array
