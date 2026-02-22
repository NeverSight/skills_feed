---
name: local-descriptions
description: USE FOR getting AI-generated POI text descriptions. Requires POI IDs obtained from web-search (with result_filter=locations). Returns markdown descriptions grounded in web search context. Max 20 IDs per request.
---

# Local Descriptions (Search API)

> **Requires API Key**: Get one at https://api.search.brave.com
>
> **Plan**: Included in the **Search** plan. See https://api-dashboard.search.brave.com/app/subscriptions/subscribe
>
> **Two-step flow**: This endpoint requires POI IDs from a prior web search.
>
> 1. Call `web-search` with `result_filter=locations` to get POI IDs from `locations.results[].id`
> 2. Pass those IDs to this endpoint to get AI-generated descriptions

## Quick Start (cURL)

### Get POI Description
```bash
curl -s "https://api.search.brave.com/res/v1/local/descriptions?ids=loc4CQWMJWLD4VBEBZ62XQLJTGK6YCJEEJDNAAAAAAA%3D" \
  -H "Accept: application/json" \
  -H "Accept-Encoding: gzip" \
  -H "X-Subscription-Token: ${BRAVE_SEARCH_API_KEY}"
```

### Multiple POIs
```bash
curl -s "https://api.search.brave.com/res/v1/local/descriptions" \
  -H "Accept: application/json" \
  -H "Accept-Encoding: gzip" \
  -H "X-Subscription-Token: ${BRAVE_SEARCH_API_KEY}" \
  -G \
  --data-urlencode "ids=loc4CQWMJWLD4VBEBZ62XQLJTGK6YCJEEJDNAAAAAAA=" \
  --data-urlencode "ids=loc4HTAVTJKP4RBEBZCEMBI3NG26YD4II4PATIHPDYI="
```

**Note**: POI IDs are opaque strings returned in web search `locations.results[].id`. They are valid for approximately 8 hours. The example IDs above are for illustration — fetch fresh IDs via `web-search` with `result_filter=locations`.

## Endpoint

```http
GET https://api.search.brave.com/res/v1/local/descriptions
```

**Authentication**: `X-Subscription-Token: <API_KEY>` header

## Parameters

| Parameter | Type | Required | Default | Description |
|--|--|--|--|--|
| `ids` | string[] | **Yes** | — | POI IDs from web search `locations.results[].id` (1-20, repeated: `?ids=a&ids=b`) |

## Response Format

### Response Fields

| Field | Type | Description |
|--|--|--|
| `type` | string | Always `"local_descriptions"` |
| `results` | array | List of description objects (entries may be `null`) |
| `results[].type` | string | Always `"local_description"` |
| `results[].id` | string | POI identifier matching the request |
| `results[].description` | string? | AI-generated markdown description, or `null` if unavailable |

### Example Response

```json
{
  "type": "local_descriptions",
  "results": [
    {
      "type": "local_description",
      "id": "loc4CQWMJWLD4VBEBZ62XQLJTGK6YCJEEJDNAAAAAAA=",
      "description": "### Overview\nA cozy neighborhood cafe known for its **artisanal coffee**..."
    }
  ]
}
```

## Getting POI IDs

POI IDs come from the **Web Search API** (`web-search`) with `result_filter=locations`:

```bash
# 1. Search for local businesses
curl -s "https://api.search.brave.com/res/v1/web/search?q=restaurants+san+francisco&result_filter=locations" \
  -H "Accept: application/json" \
  -H "X-Subscription-Token: ${BRAVE_SEARCH_API_KEY}"

# 2. Extract POI IDs from locations.results[].id
# 3. Use those IDs with local/pois and local/descriptions
```

## Use Cases

- **Local business overview**: Pair with `local-pois` to get both structured data (hours, ratings) and narrative descriptions
- **Travel/tourism enrichment**: Add descriptive context to POIs for travel planning or destination guides
- **Search results augmentation**: Supplement web search results with AI-generated summaries of local businesses

## Notes

- **Always markdown**: Descriptions use `###` headings, bullet lists, **bold**/*italics* — always formatted as markdown
- **Travel-guide tone**: Typically 200-400 words covering what makes the POI notable
- **AI-generated**: Descriptions are AI-generated based on web search context, not sourced from business profiles
- **Availability**: Not all POIs have descriptions — `description` may be `null`
- **Max IDs**: Up to 20 IDs per request
