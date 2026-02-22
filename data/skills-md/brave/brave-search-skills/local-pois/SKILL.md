---
name: local-pois
description: USE FOR getting local business/POI details. Requires POI IDs obtained from web-search (with result_filter=locations). Returns full business information including ratings, hours, contact info. Max 20 IDs.
---

# Local POIs (Search API)

> **Requires API Key**: Get one at https://api.search.brave.com
>
> **Plan**: Included in the **Search** plan. See https://api-dashboard.search.brave.com/app/subscriptions/subscribe
>
> **Two-step flow**: This endpoint requires POI IDs from a prior web search.
>
> 1. Call `web-search` with `result_filter=locations` to get POI IDs from `locations.results[].id`
> 2. Pass those IDs to this endpoint to get full business details

## Quick Start (cURL)

### Get POI Details
```bash
curl -s "https://api.search.brave.com/res/v1/local/pois" \
  -H "Accept: application/json" \
  -H "Accept-Encoding: gzip" \
  -H "X-Subscription-Token: ${BRAVE_SEARCH_API_KEY}" \
  -G \
  --data-urlencode "ids=loc4CQWMJWLD4VBEBZ62XQLJTGK6YCJEEJDNAAAAAAA="
```

### Multiple POIs with Location Headers
```bash
curl -s "https://api.search.brave.com/res/v1/local/pois" \
  -H "Accept: application/json" \
  -H "Accept-Encoding: gzip" \
  -H "X-Subscription-Token: ${BRAVE_SEARCH_API_KEY}" \
  -H "X-Loc-Lat: 37.7749" \
  -H "X-Loc-Long: -122.4194" \
  -G \
  --data-urlencode "ids=loc4CQWMJWLD4VBEBZ62XQLJTGK6YCJEEJDNAAAAAAA=" \
  --data-urlencode "ids=loc4HTAVTJKP4RBEBZCEMBI3NG26YD4II4PATIHPDYI=" \
  --data-urlencode "units=imperial"
```

**Note**: POI IDs are opaque strings returned in web search `locations.results[].id`. IDs are ephemeral and expire after ~8 hours. The example IDs above are for illustration — fetch fresh IDs via `web-search` with `result_filter=locations`. Use `--data-urlencode` since IDs may contain `=`.

## Endpoint

```http
GET https://api.search.brave.com/res/v1/local/pois
```

**Authentication**: `X-Subscription-Token: <API_KEY>` header

## Parameters

| Parameter | Type | Required | Default | Description |
|--|--|--|--|--|
| `ids` | string[] | **Yes** | — | POI IDs from web search results (1-20) |
| `search_lang` | string | No | `en` | Language preference (2+ char language code) |
| `ui_lang` | string | No | `en-US` | UI language (locale code, e.g., "en-US") |
| `units` | string | No | null | `metric` (km) or `imperial` (miles) |

### Location Headers (Optional)

For distance calculation from user location:

| Header | Type | Range | Description |
|--|--|--|--|
| `X-Loc-Lat` | float | -90.0 to 90.0 | User latitude |
| `X-Loc-Long` | float | -180.0 to 180.0 | User longitude |

## Response Fields

The response has `type: "local_pois"` and a `results` array of `LocationResult` objects:

| Field | Type | Description |
|--|--|--|
| `title` | string | Business/POI name |
| `url` | string | Canonical URL for the location |
| `provider_url` | string | Provider page URL |
| `type` | string | Always `"location_result"` |
| `id` | string | POI identifier (opaque string, valid ~8 hours) |
| `description` | string? | Short description |
| `postal_address.type` | string | Always `"PostalAddress"` |
| `postal_address.displayAddress` | string | Formatted display address |
| `postal_address.streetAddress` | string? | Street address |
| `postal_address.addressLocality` | string? | City |
| `postal_address.addressRegion` | string? | State/region |
| `postal_address.postalCode` | string? | Postal/ZIP code |
| `postal_address.country` | string? | Country code |
| `contact.telephone` | string? | Phone number |
| `contact.email` | string? | Email address |
| `rating.ratingValue` | float? | Average rating (≥0) |
| `rating.bestRating` | float? | Max possible rating |
| `rating.reviewCount` | int? | Number of reviews |
| `rating.profile.name` | string? | Rating provider name |
| `rating.profile.url` | string? | Rating provider URL |
| `opening_hours.current_day` | object[]? | Today's hours (`abbr_name`, `full_name`, `opens`, `closes`) |
| `opening_hours.days` | object[][]? | Hours for each day of the week (same structure) |
| `coordinates` | [float, float]? | `[latitude, longitude]` tuple |
| `distance.value` | float? | Distance from user location |
| `distance.units` | string? | Distance unit (`km` or `miles`) |
| `categories` | string[] | Business categories (default `[]`) |
| `price_range` | string? | Price indicator (`$`, `$$`, `$$$`, `$$$$`) |
| `serves_cuisine` | string[]? | Cuisine types (restaurants) |
| `thumbnail.src` | string? | Thumbnail image URL |
| `thumbnail.original` | string? | Original image URL |
| `profiles` | object[]? | External profiles (`name`, `url`, `long_name`, `img`) |
| `reviews.reviews_in_foreign_language` | bool | Whether reviews in a foreign language are available |
| `pictures.results` | object[]? | Photo thumbnails |
| `action` | object? | Action to take — has `type` (string) and `url` (string) |
| `results` | object[]? | Related web results (`LocationWebResult` with `meta_url`) |
| `timezone` | string? | IANA timezone (e.g., `America/Los_Angeles`) |
| `timezone_offset` | int? | UTC timezone offset |

### Example Response

```json
{
  "type": "local_pois",
  "results": [
    {
      "type": "location_result",
      "title": "Park Mediterranean Grill",
      "url": "https://yelp.com/biz/park-mediterranean-grill-sf",
      "provider_url": "https://yelp.com/biz/park-mediterranean-grill-sf",
      "id": "loc4CQWMJWLD4VBEBZ62XQLJTGK6YCJEEJDNAAAAAAA=",
      "postal_address": {
        "type": "PostalAddress",
        "displayAddress": "123 Main St, San Francisco, CA 94102",
        "streetAddress": "123 Main St",
        "addressLocality": "San Francisco",
        "addressRegion": "CA",
        "postalCode": "94102",
        "country": "US"
      },
      "contact": { "telephone": "+1 415-555-0123" },
      "thumbnail": {
        "src": "https://example.com/thumb.jpg",
        "original": "https://example.com/original.jpg"
      },
      "rating": {
        "ratingValue": 4.5,
        "bestRating": 5.0,
        "reviewCount": 234,
      },
      "opening_hours": {
        "current_day": [
          { "abbr_name": "Mon", "full_name": "Monday", "opens": "07:00", "closes": "21:00" }
        ]
      },
      "coordinates": [37.7749, -122.4194],
      "distance": { "value": 0.3, "units": "miles" },
      "categories": ["Mediterranean", "Greek"],
      "price_range": "$$",
      "serves_cuisine": ["Mediterranean", "Greek"],
      "timezone": "America/Los_Angeles"
    }
  ]
}
```

## Getting POI IDs

POI IDs come from the **Web Search API** (`web-search`) with `result_filter=locations`:

```bash
# 1. Search for local businesses
curl -s "https://api.search.brave.com/res/v1/web/search?q=coffee+shops+near+me&result_filter=locations" \
  -H "Accept: application/json" \
  -H "X-Subscription-Token: ${BRAVE_SEARCH_API_KEY}" \
  -H "X-Loc-Lat: 37.7749" \
  -H "X-Loc-Long: -122.4194"

# 2. Extract POI IDs from locations.results[].id
# 3. Use those IDs with this endpoint
```

## Use Cases

- **Local business lookup**: Retrieve full details (hours, contact, address) for POIs surfaced in web search
- **Restaurant discovery pipeline**: Search for restaurants, fetch POI details, filter by cuisine/rating/price_range
- **Business hours checker**: Get opening_hours for a business to determine if currently open
- **Location-aware application**: Combine with location headers to get distance calculations for nearby POIs

## Notes

- **ID format**: Opaque strings (use `--data-urlencode` for cURL)
- **Units**: `metric` or `imperial` for distance measurement preference
- **Max IDs**: Up to 20 IDs per request
