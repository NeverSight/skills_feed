---
name: suggest
description: USE FOR query autocomplete/suggestions. Fast (<100ms). Returns suggested queries as user types. Supports rich suggestions with entity info. Typo-resilient.
---

# Suggest / Autocomplete

> **Requires API Key**: Get one at https://api.search.brave.com
>
> **Plan**: Included in the **Suggest** plan. See https://api-dashboard.search.brave.com/app/subscriptions/subscribe

## Quick Start (cURL)

### Basic Suggestions
```bash
curl -s "https://api.search.brave.com/res/v1/suggest/search?q=how+to+" \
  -H "Accept: application/json" \
  -H "X-Subscription-Token: ${BRAVE_SEARCH_API_KEY}"
```

### With All Parameters
```bash
curl -s "https://api.search.brave.com/res/v1/suggest/search" \
  -H "Accept: application/json" \
  -H "X-Subscription-Token: ${BRAVE_SEARCH_API_KEY}" \
  -G \
  --data-urlencode "q=albert" \
  --data-urlencode "country=US" \
  --data-urlencode "lang=en" \
  --data-urlencode "count=10" \
  --data-urlencode "rich=true"
```

## Endpoint

```http
GET https://api.search.brave.com/res/v1/suggest/search
```

**Authentication**: `X-Subscription-Token: <API_KEY>` header

**Optional Headers**:
- `Accept-Encoding: gzip` — Enable response compression

## Parameters

| Parameter | Type | Required | Default | Description |
|--|--|--|--|--|
| `q` | string | **Yes** | — | Suggest search query (1-400 chars, max 50 words) |
| `lang` | string | No | `en` | Language preference (2+ char language code, e.g. `fr`, `de`, `zh-hans`) |
| `country` | string | No | `US` | Search country (2-letter country code or `ALL`) |
| `count` | int | No | `5` | Number of suggestions (1-20). Actual results may be fewer |
| `rich` | bool | No | `false` | Enhance with entity info (title, description, image). Paid Search plan required |

## Response Fields

| Field | Type | Description |
|--|--|--|
| `type` | string | Always `"suggest"` |
| `query.original` | string | The original suggest search query |
| `results` | array | List of suggestions (may be empty) |
| `results[].query` | string | Suggested query completion |
| `results[].is_entity` | bool? | Whether the suggested enriched query is an entity (rich only) |
| `results[].title` | string? | The suggested query enriched title (rich only) |
| `results[].description` | string? | The suggested query enriched description (rich only) |
| `results[].img` | string? | The suggested query enriched image URL (rich only) |

Fields with `null` values are excluded from the response. Non-rich results contain only the `query` field.

### Rich Response Example (`rich=true`)
```json
{
  "type": "suggest",
  "query": { "original": "albert" },
  "results": [
    {
      "query": "albert einstein",
      "is_entity": true,
      "title": "Albert Einstein",
      "description": "German-born theoretical physicist",
      "img": "https://imgs.search.brave.com/..."
    },
    { "query": "albert einstein quotes", "is_entity": false }
  ]
}
```

## Use Cases

- **Search-as-you-type UI**: Real-time autocomplete dropdown. Debounce 150-300ms.
- **Query refinement for RAG**: Expand partial/ambiguous queries before calling `web-search` or `llm-context`.
- **Entity detection**: Use `rich=true` to detect entities with title, description, and image for preview cards.
- **Typo-tolerant input**: Get clean suggestions from misspelled input without separate spellcheck.

## Notes

- **Latency**: Designed for <100ms response times
- **Country/lang**: Hints for suggestion relevance, not strict filters
- **Typo handling**: Suggestions handle common typos without separate spellcheck
