---
name: images-search
description: USE FOR image search. Returns images with title, source URL, thumbnail. Supports SafeSearch filter. Up to 200 results.
---

# Images Search

> **Requires API Key**: Get one at https://api.search.brave.com
>
> **Plan**: Included in the **Search** plan. See https://api-dashboard.search.brave.com/app/subscriptions/subscribe

## Quick Start (cURL)

### Basic Search
```bash
curl -s "https://api.search.brave.com/res/v1/images/search?q=mountain+landscape" \
  -H "Accept: application/json" \
  -H "X-Subscription-Token: ${BRAVE_SEARCH_API_KEY}"
```

### With Parameters
```bash
curl -s "https://api.search.brave.com/res/v1/images/search" \
  -H "Accept: application/json" \
  -H "X-Subscription-Token: ${BRAVE_SEARCH_API_KEY}" \
  -G \
  --data-urlencode "q=northern lights photography" \
  --data-urlencode "country=US" \
  --data-urlencode "search_lang=en" \
  --data-urlencode "count=20" \
  --data-urlencode "safesearch=strict"
```

## Endpoint

```http
GET https://api.search.brave.com/res/v1/images/search
```

**Authentication**: `X-Subscription-Token: <API_KEY>` header

## Parameters

| Parameter | Type | Required | Default | Description |
|--|--|--|--|--|
| `q` | string | **Yes** | - | Search query (1-400 chars, max 50 words) |
| `country` | string | No | `US` | Search country (2-letter country code or `ALL`) |
| `search_lang` | string | No | `en` | 2+ char language code |
| `count` | int | No | 50 | Results to return (1-200) |
| `safesearch` | string | No | `strict` | `off` or `strict` (no `moderate` for images) |
| `spellcheck` | bool | No | true | Auto-correct query; corrected query in `query.altered` |

## Response Format

```json
{
  "type": "images",
  "query": {
    "original": "mountain landscape",
    "altered": null,
    "spellcheck_off": false,
    "show_strict_warning": false
  },
  "results": [
    {
      "type": "image_result",
      "title": "Beautiful Mountain Landscape",
      "url": "https://example.com/mountain-photo",
      "source": "example.com",
      "page_fetched": "2025-09-15T10:30:00Z",
      "thumbnail": {
        "src": "https://imgs.search.brave.com/...",
        "width": 200,
        "height": 150
      },
      "properties": {
        "url": "https://example.com/images/mountain.jpg",
        "placeholder": "https://imgs.search.brave.com/placeholder/...",
        "width": 1920,
        "height": 1080
      },
      "meta_url": {
        "scheme": "https",
        "netloc": "example.com",
        "hostname": "example.com",
        "favicon": "https://imgs.search.brave.com/favicon/...",
        "path": "/mountain-photo"
      },
      "confidence": "high"
    }
  ],
  "extra": {
    "might_be_offensive": false
  }
}
```

## Response Fields

| Field | Type | Description |
|--|--|--|
| `type` | string | Always `"images"` |
| `query.original` | string | Original query |
| `query.altered` | string? | Spellchecked query (null if no correction) |
| `query.spellcheck_off` | bool? | Whether spellcheck was disabled |
| `query.show_strict_warning` | bool? | True if strict safesearch hid relevant results |
| `results[]` | array | List of image results |
| `results[].type` | string | Always `"image_result"` |
| `results[].title` | string? | Image title |
| `results[].url` | string? | Page URL where image was found |
| `results[].source` | string? | Source domain |
| `results[].page_fetched` | string? | ISO datetime of last page crawl |
| `results[].thumbnail.src` | string? | Brave-proxied thumbnail URL (~500px width) |
| `results[].thumbnail.width` | int? | Thumbnail width |
| `results[].thumbnail.height` | int? | Thumbnail height |
| `results[].properties.url` | string? | Original full-size image URL |
| `results[].properties.placeholder` | string? | Low-res placeholder URL (Brave-proxied) |
| `results[].properties.width` | int? | Original image width (may be null) |
| `results[].properties.height` | int? | Original image height (may be null) |
| `results[].meta_url.scheme` | string? | URL protocol scheme |
| `results[].meta_url.netloc` | string? | Network location |
| `results[].meta_url.hostname` | string? | Lowercased domain |
| `results[].meta_url.favicon` | string? | Favicon URL |
| `results[].meta_url.path` | string? | URL path |
| `results[].confidence` | string? | Relevance: `low`, `medium`, or `high` |
| `extra.might_be_offensive` | bool | Whether results may contain offensive content |

## Use Cases

- **Visual content discovery**: Build image galleries, mood boards, or visual research tools. Use `count=200` for comprehensive coverage. Prefer over `web-search` when you need image-specific metadata (dimensions, thumbnails).
- **Content enrichment**: Add relevant images to articles or generated content. Use `country` and `search_lang` to target your audience's locale.
- **Safe image retrieval**: Default `safesearch=strict` ensures family-friendly results out of the box. Only two modes (off/strict) — no moderate option, unlike web/video/news search.
- **High-volume batch retrieval**: Up to 200 images per request (vs 20 for web, 50 for videos/news). Ideal for bulk image sourcing or visual analysis pipelines.

## Notes

- **SafeSearch**: Defaults to `strict` for images (stricter than web search)
- **High volume**: Can return up to 200 results per request
- **Thumbnails**: Brave-proxied for user privacy (500px width). Use `properties.url` for original full-resolution image.
- **Dimensions**: `properties.width/height` may be missing for some images
- **Placeholder**: `properties.placeholder` is a low-res URL (not inline base64) useful for progressive loading UX
