---
name: news-search
description: USE FOR news search. Returns news articles with title, URL, description, age, thumbnail. Supports freshness and date range filtering, SafeSearch filter and Goggles for custom ranking.
---

# News Search

> **Requires API Key**: Get one at https://api.search.brave.com
>
> **Plan**: Included in the **Search** plan. See https://api-dashboard.search.brave.com/app/subscriptions/subscribe

## Quick Start (cURL)

### Basic Search
```bash
curl -s "https://api.search.brave.com/res/v1/news/search?q=space+exploration" \
  -H "Accept: application/json" \
  -H "X-Subscription-Token: ${BRAVE_SEARCH_API_KEY}"
```

### Recent News (Past 24 Hours)
```bash
curl -s "https://api.search.brave.com/res/v1/news/search" \
  -H "Accept: application/json" \
  -H "X-Subscription-Token: ${BRAVE_SEARCH_API_KEY}" \
  -G \
  --data-urlencode "q=cybersecurity" \
  --data-urlencode "country=US" \
  --data-urlencode "freshness=pd" \
  --data-urlencode "count=20"
```

### Date Range Filter
```bash
curl -s "https://api.search.brave.com/res/v1/news/search" \
  -H "Accept: application/json" \
  -H "X-Subscription-Token: ${BRAVE_SEARCH_API_KEY}" \
  -G \
  --data-urlencode "q=climate summit" \
  --data-urlencode "freshness=2026-01-01to2026-01-31"
```

## Endpoint

```http
GET https://api.search.brave.com/res/v1/news/search
POST https://api.search.brave.com/res/v1/news/search
```

**Authentication**: `X-Subscription-Token: <API_KEY>` header

**Note**: Both GET and POST are supported. POST is useful for long queries or complex Goggles.

## Parameters

| Parameter | Type | Required | Default | Description |
|--|--|--|--|--|
| `q` | string | **Yes** | - | Search query (1-400 chars, max 50 words) |
| `country` | string | No | `US` | Search country (2-letter country code or `ALL`) |
| `search_lang` | string | No | `en` | Language preference (2+ char language code) |
| `ui_lang` | string | No | `en-US` | UI language (e.g., "en-US") |
| `count` | int | No | `20` | Number of results (1-50) |
| `offset` | int | No | `0` | Page offset (0-9) |
| `safesearch` | string | No | `strict` | Adult content filter (`off`/`moderate`/`strict`) |
| `freshness` | string | No | - | Time filter (`pd`/`pw`/`pm`/`py` or date range) |
| `spellcheck` | bool | No | `true` | Auto-correct query |
| `extra_snippets` | bool | No | - | Up to 5 additional excerpts per result |
| `goggles` | string or array | No | - | Custom ranking filter (URL or inline; repeat param for multiple) |
| `operators` | bool | No | `true` | Apply search operators |
| `include_fetch_metadata` | bool | No | `false` | Include fetch timestamps in results |

### Freshness Values

| Value | Description |
|--|--|
| `pd` | Past day (24 hours) - ideal for breaking news |
| `pw` | Past week (7 days) |
| `pm` | Past month (31 days) |
| `py` | Past year (365 days) |
| `YYYY-MM-DDtoYYYY-MM-DD` | Custom date range |

## Response Format

```json
{
  "type": "news",
  "query": {
    "original": "space exploration"
  },
  "results": [
    {
      "type": "news_result",
      "title": "New Developments in Space Exploration",
      "url": "https://news.example.com/space-exploration",
      "description": "Recent missions have advanced our understanding of...",
      "age": "2 hours ago",
      "page_age": "2026-01-15T14:30:00",
      "page_fetched": "2026-01-15T15:00:00Z",
      "meta_url": {
        "scheme": "https",
        "netloc": "news.example.com",
        "hostname": "news.example.com",
        "favicon": "https://imgs.search.brave.com/favicon/news.example.com",
        "path": "/space-exploration"
      },
      "thumbnail": {
        "src": "https://imgs.search.brave.com/..."
      }
    }
  ]
}
```

## Response Fields

| Field | Type | Description |
|--|--|--|
| `type` | string | Always `"news"` |
| `query.original` | string | The original search query |
| `query.altered` | string? | Spellcheck-corrected query (if changed) |
| `query.cleaned` | string? | Cleaned/normalized query from spellchecker |
| `query.spellcheck_off` | bool? | Whether spellcheck was disabled |
| `query.show_strict_warning` | bool? | True if strict safesearch blocked results |
| `query.search_operators` | object? | Applied search operators |
| `query.search_operators.applied` | bool | Whether operators were applied |
| `query.search_operators.cleaned_query` | string? | Query after operator processing |
| `query.search_operators.sites` | list[str]? | Domains from `site:` operators |
| `results[].type` | string | Always `"news_result"` |
| `results[].title` | string | Article title |
| `results[].url` | string | Source URL of the article |
| `results[].description` | string? | Article description/summary |
| `results[].age` | string? | Human-readable age (e.g. "2 hours ago") |
| `results[].page_age` | string? | Publication date from source (ISO datetime) |
| `results[].page_fetched` | string? | When page was last fetched (ISO datetime) |
| `results[].fetched_content_timestamp` | int? | Fetch timestamp (only with `include_fetch_metadata=true`) |
| `results[].meta_url.scheme` | string? | URL protocol scheme |
| `results[].meta_url.netloc` | string? | Network location |
| `results[].meta_url.hostname` | string? | Lowercased domain name |
| `results[].meta_url.favicon` | string? | Favicon URL |
| `results[].meta_url.path` | string? | URL path |
| `results[].thumbnail.src` | string | Served thumbnail URL |
| `results[].thumbnail.original` | string? | Original thumbnail URL |
| `results[].extra_snippets` | list[str]? | Up to 5 additional excerpts per result |

## Goggles (Custom Ranking) — Unique to Brave

Goggles let you **re-rank news results** — boost trusted outlets or suppress unwanted sources.

| Method | Example |
|--|--|
| **Hosted** | `--data-urlencode "goggles=https://raw.githubusercontent.com/brave/goggles-quickstart/main/goggles/hacker_news.goggle"` |
| **Inline** | `--data-urlencode 'goggles=$discard\n$site=example.com'` |

> **Hosted** goggles must be on GitHub/GitLab, include `! name:`, `! description:`, `! author:` headers, and be registered at https://search.brave.com/goggles/create. **Inline** rules need no registration.

**Syntax**: `$boost=N` / `$downrank=N` (1–10), `$discard`, `$site=example.com`. Combine with commas: `$site=example.com,boost=3`. Separate rules with `\n` (`%0A`).

**Allow list**: `$discard\n$site=docs.python.org\n$site=developer.mozilla.org` — **Block list**: `$discard,site=pinterest.com\n$discard,site=quora.com`

**Resources**: [Discover](https://search.brave.com/goggles/discover) · [Syntax](https://search.brave.com/help/goggles) · [Quickstart](https://github.com/brave/goggles-quickstart)

## Search Operators

Use search operators to refine results:
- `site:local-paper.com` - Limit to specific news site
- `"exact phrase"` - Match exact phrase
- `-exclude` - Exclude term

Set `operators=false` to disable operator parsing.

## Use Cases

- **Breaking news monitoring**: Use `freshness=pd` for the most recent articles on a topic.
- **Custom news feeds with Goggles**: Boost trusted sources and discard other sources — unique to Brave.
- **Historical news research**: Use `freshness=YYYY-MM-DDtoYYYY-MM-DD` to find articles from specific time periods.
- **Multilingual news**: Combine `country`, `search_lang`, and `ui_lang` for cross-locale results.
- **Data pipelines**: Set `include_fetch_metadata=true` for `fetched_content_timestamp` on each result.

## Notes

- **SafeSearch**: Defaults to `strict`
- **Pagination**: Use `offset` (0-9) with `count`
- **Extra snippets**: Up to 5 additional excerpts when `extra_snippets=true`
