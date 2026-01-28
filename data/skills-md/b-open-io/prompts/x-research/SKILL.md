---
name: x-research
version: 1.1.2
description: AI-powered X/Twitter research via xAI Grok. Returns AI SUMMARIES with analysis, not raw tweets. Use for "what's trending", "social sentiment", "summarize X discussion about", "analyze X conversation about", "research topic on X". For RAW tweet data, use x-user-timeline, x-tweet-search, x-tweet-fetch instead. Requires XAI_API_KEY.
allowed-tools: Bash(curl:*), Bash(jq:*), Bash(${CLAUDE_PLUGIN_ROOT}:*)
---

# X Research (xAI/Grok)

AI-powered research using xAI's Grok API. Returns **AI summaries with citations**, not raw tweet data.

> **Want raw tweets instead?** Use these skills:
> - `x-user-timeline` - Raw tweets from a user
> - `x-tweet-search` - Raw search results
> - `x-tweet-fetch` - Raw single tweet
> - `x-user-lookup` - User profile data
>
> These require `X_BEARER_TOKEN` instead of `XAI_API_KEY`.

## When to Use

**USE THIS SKILL FOR:**
- Summarized research with AI analysis
- Current events and breaking news
- Social sentiment ("What are developers saying about Y?")
- X/Twitter trending topics and viral posts
- Emerging tools/frameworks not in documentation yet
- Community opinions on best practices

**DON'T USE FOR:**
- Raw tweet data (use x-user-timeline, x-tweet-search)
- Specific user's posts verbatim (use x-user-timeline)
- Well-documented APIs (use WebFetch instead)

## Setup Requirements

Check if the API key is set:

```bash
if [ -z "$XAI_API_KEY" ]; then
  echo "ERROR: XAI_API_KEY is not set"
  echo "1. Get API key from https://x.ai/api"
  echo "2. Add to profile: export XAI_API_KEY=\"your-key\""
  echo "3. Restart terminal and Claude Code"
  exit 1
else
  echo "XAI_API_KEY is configured"
fi
```

If unavailable, inform the user that XAI_API_KEY must be configured before using this skill.

## API Overview

**Endpoint**: `https://api.x.ai/v1/responses`

**Recommended Model**: `grok-4-1-fast` (specifically trained for agentic search)

**Available Models**:
- `grok-4-1-fast` - Recommended for agentic search (auto-selects reasoning mode)
- `grok-4-1-fast-reasoning` - Explicit reasoning for complex research
- `grok-4-1-fast-non-reasoning` - Faster responses, simpler queries

**Available Search Tools**:
- `web_search` - Searches the internet and browses web pages
- `x_search` - Semantic and keyword search across X posts

## Basic Usage

### Simple Query with Search Tools

```bash
curl -s "https://api.x.ai/v1/responses" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $XAI_API_KEY" \
  -d '{
    "model": "grok-4-1-fast",
    "input": [{"role": "user", "content": "[YOUR QUERY]"}],
    "tools": [{"type": "web_search"}, {"type": "x_search"}]
  }' | jq -r '.output[-1].content[0].text'
```

### Query with Usage Tracking (Recommended)

```bash
RESPONSE=$(curl -s "https://api.x.ai/v1/responses" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $XAI_API_KEY" \
  -d '{
    "model": "grok-4-1-fast",
    "input": [{"role": "user", "content": "[YOUR QUERY]"}],
    "tools": [{"type": "web_search"}, {"type": "x_search"}]
  }')

# Extract usage stats
TOOL_CALLS=$(echo "$RESPONSE" | jq -r '.usage.num_server_side_tools_used // 0')
COST_TICKS=$(echo "$RESPONSE" | jq -r '.usage.cost_in_usd_ticks // 0')
COST_USD=$(echo "scale=4; $COST_TICKS / 1000000000" | bc)
echo "Tool calls: $TOOL_CALLS | Estimated cost: \$$COST_USD"
echo ""
echo "$RESPONSE" | jq -r '.output[-1].content[0].text'
```

## Search Tool Parameters

### Web Search Options

```json
"tools": [{
  "type": "web_search",
  "allowed_domains": ["github.com", "stackoverflow.com"],
  "excluded_domains": ["pinterest.com"],
  "enable_image_understanding": true
}]
```

- `allowed_domains` - Restrict to these domains only (max 5)
- `excluded_domains` - Exclude these domains (max 5)
- `enable_image_understanding` - Analyze images found during search

### X Search Options

```json
"tools": [{
  "type": "x_search",
  "allowed_x_handles": ["elikimonimus", "anthropaboris"],
  "excluded_x_handles": ["spambot"],
  "from_date": "2025-01-01",
  "to_date": "2025-01-16",
  "enable_image_understanding": true,
  "enable_video_understanding": true
}]
```

- `allowed_x_handles` - Only include posts from these accounts (max 10)
- `excluded_x_handles` - Exclude posts from these accounts (max 10)
- `from_date` / `to_date` - ISO8601 date range (YYYY-MM-DD)
- `enable_image_understanding` - Analyze images in posts
- `enable_video_understanding` - Analyze videos in posts

## Examples

### X/Twitter Trending Topics

```bash
curl -s "https://api.x.ai/v1/responses" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $XAI_API_KEY" \
  -d '{
    "model": "grok-4-1-fast",
    "input": [{"role": "user", "content": "What is currently trending on X? Include viral posts and major discussions."}],
    "tools": [{"type": "x_search"}]
  }' | jq -r '.output[-1].content[0].text'
```

### Developer Sentiment on a Topic

```bash
curl -s "https://api.x.ai/v1/responses" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $XAI_API_KEY" \
  -d '{
    "model": "grok-4-1-fast",
    "input": [{"role": "user", "content": "What are developers saying about [TOPIC] on X? Include recent discussions and opinions."}],
    "tools": [{"type": "x_search"}, {"type": "web_search"}]
  }' | jq -r '.output[-1].content[0].text'
```

### News and Web Research

```bash
curl -s "https://api.x.ai/v1/responses" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $XAI_API_KEY" \
  -d '{
    "model": "grok-4-1-fast",
    "input": [{"role": "user", "content": "Latest news and developments about [TOPIC]"}],
    "tools": [{"type": "web_search"}]
  }' | jq -r '.output[-1].content[0].text'
```

### Research with Date Range

```bash
curl -s "https://api.x.ai/v1/responses" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $XAI_API_KEY" \
  -d '{
    "model": "grok-4-1-fast",
    "input": [{"role": "user", "content": "What happened with [TOPIC] last week?"}],
    "tools": [{
      "type": "x_search",
      "from_date": "2025-01-09",
      "to_date": "2025-01-16"
    }, {
      "type": "web_search"
    }]
  }' | jq -r '.output[-1].content[0].text'
```

## Response Structure

The response contains:

```json
{
  "output": [
    {"type": "web_search_call", "status": "completed", ...},
    {"type": "custom_tool_call", "name": "x_semantic_search", ...},
    {
      "type": "message",
      "content": [{
        "type": "output_text",
        "text": "The actual response with [[1]](url) inline citations",
        "annotations": [{"type": "url_citation", "url": "...", ...}]
      }]
    }
  ],
  "citations": ["url1", "url2", ...],
  "usage": {
    "input_tokens": 11408,
    "output_tokens": 2846,
    "num_server_side_tools_used": 8,
    "cost_in_usd_ticks": 429052500
  }
}
```

**Extracting content**: `jq -r '.output[-1].content[0].text'`

**Extracting citations**: `jq -r '.citations[]'`

## Pricing

**Search tools are currently FREE** (promotional pricing).

Standard pricing when active:
- Web Search, X Search: $5 per 1,000 tool invocations
- Token costs: Varies by model (~$3-15 per 1M input tokens)

Track costs via `response.usage.cost_in_usd_ticks` (divide by 1,000,000,000 for USD).

## Error Handling

If the API returns an error:
1. Check XAI_API_KEY is set and valid
2. Verify model name is correct (use `grok-4-1-fast`)
3. Check rate limits haven't been exceeded
4. Ensure `tools` array is properly formatted
5. Report the error to the user with the API response

Common errors:
- `"Internal error"` - Usually wrong model name or malformed request
- Timeout - Request took too long (rare with agentic API)

## Migration Notes

**DEPRECATED (January 12, 2026)**: The old Live Search API using `search_parameters` is being deprecated. This skill uses the new agentic tool calling API which is faster and more capable.

Old format (deprecated):
```json
{
  "model": "grok-4-latest",
  "messages": [...],
  "search_parameters": {"mode": "on"}
}
```

New format (use this):
```json
{
  "model": "grok-4-1-fast",
  "input": [...],
  "tools": [{"type": "web_search"}, {"type": "x_search"}]
}
```

## References

- **LLMs.txt (AI-optimized docs)**: https://docs.x.com/llms.txt
- [xAI API Documentation](https://docs.x.ai)
- [Search Tools Guide](https://docs.x.ai/docs/guides/tools/search-tools)
- [Models Reference](https://docs.x.ai/docs/models)
- [X.com API v2](https://developer.x.com/en/docs/x-api)
