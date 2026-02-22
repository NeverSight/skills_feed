---
name: videos-search
description: USE FOR video search. Returns videos with title, URL, thumbnail, duration, view count, creator. Supports freshness filters, SafeSearch, pagination.
---

# Videos Search

> **Requires API Key**: Get one at https://api.search.brave.com
>
> **Plan**: Included in the **Search** plan. See https://api-dashboard.search.brave.com/app/subscriptions/subscribe

## Quick Start (cURL)

### Basic Search
```bash
curl -s "https://api.search.brave.com/res/v1/videos/search?q=python+tutorial" \
  -H "Accept: application/json" \
  -H "X-Subscription-Token: ${BRAVE_SEARCH_API_KEY}"
```

### With Parameters
```bash
curl -s "https://api.search.brave.com/res/v1/videos/search" \
  -H "Accept: application/json" \
  -H "X-Subscription-Token: ${BRAVE_SEARCH_API_KEY}" \
  -G \
  --data-urlencode "q=machine learning explained" \
  --data-urlencode "country=US" \
  --data-urlencode "search_lang=en" \
  --data-urlencode "count=20" \
  --data-urlencode "freshness=pm"
```

## Endpoint

```http
GET https://api.search.brave.com/res/v1/videos/search
POST https://api.search.brave.com/res/v1/videos/search
```

**Authentication**: `X-Subscription-Token: <API_KEY>` header

**Note**: Both GET and POST methods are supported. POST is useful for long queries.

## Parameters

| Parameter | Type | Required | Default | Description |
|--|--|--|--|--|
| `q` | string | **Yes** | - | Search query (1-400 chars, max 50 words) |
| `country` | string | No | `US` | Search country (2-letter country code or `ALL`) |
| `search_lang` | string | No | `en` | Language preference (2+ char language code) |
| `ui_lang` | string | No | `en-US` | UI language (e.g., "en-US") |
| `count` | int | No | `20` | Number of results (1-50) |
| `offset` | int | No | `0` | Page offset (0-9) |
| `safesearch` | string | No | `moderate` | Adult content filter (`off`/`moderate`/`strict`) |
| `freshness` | string | No | - | Time filter (`pd`/`pw`/`pm`/`py` or date range) |
| `spellcheck` | bool | No | `true` | Auto-correct query |
| `operators` | bool | No | `true` | Apply search operators |
| `include_fetch_metadata` | bool | No | `false` | Include `fetched_content_timestamp` in results |

### Freshness Values

| Value | Description |
|--|--|
| `pd` | Past day (24 hours) |
| `pw` | Past week (7 days) |
| `pm` | Past month (31 days) |
| `py` | Past year (365 days) |
| `YYYY-MM-DDtoYYYY-MM-DD` | Custom date range |

## Response Format

```json
{
  "type": "videos",
  "query": {
    "original": "python tutorial",
    "spellcheck_off": false
  },
  "extra": {
    "might_be_offensive": false
  },
  "results": [
    {
      "type": "video_result",
      "title": "Python Tutorial for Beginners",
      "url": "https://www.youtube.com/watch?v=rfscVS0vtbw",
      "description": "Learn Python programming from scratch...",
      "age": "February 12, 2025",
      "page_age": "2025-02-12T00:00:00",
      "page_fetched": "2025-02-12T15:00:00Z",
      "thumbnail": {
        "src": "https://imgs.search.brave.com/...",
        "original": "https://i.ytimg.com/vi/rfscVS0vtbw/hqdefault.jpg"
      },
      "video": {
        "duration": "03:45:00",
        "views": 1523000,
        "creator": "freeCodeCamp",
        "publisher": "YouTube",
        "requires_subscription": false,
        "tags": ["python", "programming"],
        "author": {
          "name": "freeCodeCamp.org",
          "url": "https://www.youtube.com/@freecodecamp"
        }
      },
      "meta_url": {
        "scheme": "https",
        "netloc": "youtube.com",
        "hostname": "www.youtube.com",
        "favicon": "https://imgs.search.brave.com/...",
        "path": "\u203a watch"
      }
    }
  ]
}
```

## Response Fields

| Field | Type | Description |
|--|--|--|
| `type` | string | Always `"videos"` |
| `query.original` | string | The original search query |
| `query.altered` | string? | Spellcheck-corrected query (if changed) |
| `query.cleaned` | string? | Cleaned/normalized query |
| `query.spellcheck_off` | bool? | Whether spellcheck was disabled |
| `query.show_strict_warning` | bool? | True if strict safesearch blocked adult results |
| `query.search_operators` | object? | Applied search operators (`applied`, `cleaned_query`, `sites`) |
| `extra.might_be_offensive` | bool | Whether results may contain offensive content |
| `results[].type` | string | Always `"video_result"` |
| `results[].url` | string | Source URL of the video |
| `results[].title` | string | Video title |
| `results[].description` | string? | Video description |
| `results[].age` | string? | Human-readable age (e.g. "6 months ago") or absolute date (e.g. "February 12, 2025") |
| `results[].page_age` | string? | Page age from source (ISO datetime) |
| `results[].page_fetched` | string? | ISO datetime when page was last fetched (e.g. `2025-02-12T15:00:00Z`) |
| `results[].fetched_content_timestamp` | int? | Fetch timestamp (only with `include_fetch_metadata=true`) |
| `results[].video.duration` | string? | Time string (variable format) |
| `results[].video.views` | int? | View count as integer |
| `results[].video.creator` | string? | Channel/creator name |
| `results[].video.publisher` | string? | Platform (YouTube, Vimeo, etc.) |
| `results[].video.requires_subscription` | bool? | Whether video requires a subscription |
| `results[].video.tags` | list[str]? | Tags relevant to the video |
| `results[].video.author` | object? | Author profile |
| `results[].video.author.name` | string | Author name |
| `results[].video.author.url` | string | Author profile URL |
| `results[].video.author.long_name` | string? | Extended author name |
| `results[].video.author.img` | string? | Author profile image URL |
| `results[].thumbnail.src` | string | Served thumbnail URL |
| `results[].thumbnail.original` | string? | Original thumbnail URL |
| `results[].meta_url.scheme` | string? | URL protocol scheme |
| `results[].meta_url.netloc` | string? | Network location |
| `results[].meta_url.hostname` | string? | Lowercased domain name |
| `results[].meta_url.favicon` | string? | Favicon URL |
| `results[].meta_url.path` | string? | URL path |

## Search Operators

Use search operators to refine results:
- `site:youtube.com` - Limit to specific site
- `"exact phrase"` - Match exact phrase
- `-exclude` - Exclude term

Set `operators=false` to disable operator parsing.

## Use Cases

- **Video content research**: Find tutorials, explainers, and reviews by topic. Use the `video.duration`, `video.views`, and `video.creator` metadata to filter and rank results programmatically. Prefer videos-search over web-search when you need a dedicated video index with richer metadata (duration, views, creator, tags) and up to 50 results per request.
- **Fresh video monitoring**: Use `freshness=pd` or `freshness=pw` to track newly published video content on trending topics or specific subjects.
- **Platform-specific search**: Use `site:youtube.com` or `site:vimeo.com` operators to target specific video platforms.
- **Video metadata extraction**: Get view counts, durations, creator info, and tags for analytics, content curation, or recommendation systems.

## Notes

- **Pagination**: Use `offset` (0-9) with `count` for more results
- **Max results**: Up to 50 results per request
