---
name: local-search
description: |
  Search for places, businesses, and locations using Google Maps APIs via x402.

  USE FOR:
  - Finding businesses by name or type
  - Searching nearby places
  - Getting detailed place information (address, hours, reviews)
  - Finding restaurants, stores, services in an area
  - Getting business ratings and reviews

  TRIGGERS:
  - "find", "search for", "locate", "nearby"
  - "restaurants near", "hotels in", "stores around"
  - "business details", "opening hours", "reviews for"
  - "places in", "what's near", "directions to"

  Use mcp__x402__fetch for Google Maps endpoints. Choose partial ($0.02) vs full ($0.05-0.08) based on data needs.
---

# Local Search with Google Maps

Access Google Maps Places API through x402-protected endpoints.

## Setup

See [rules/getting-started.md](rules/getting-started.md) for installation and wallet setup.

## Quick Reference

| Task | Endpoint | Price | Data Included |
|------|----------|-------|---------------|
| Text search (basic) | `/api/google-maps/text-search/partial` | $0.02 | Name, address, rating |
| Text search (full) | `/api/google-maps/text-search/full` | $0.08 | + reviews, atmosphere |
| Nearby search (basic) | `/api/google-maps/nearby-search/partial` | $0.02 | Name, address, rating |
| Nearby search (full) | `/api/google-maps/nearby-search/full` | $0.08 | + reviews, atmosphere |
| Place details (basic) | `/api/google-maps/place-details/partial` | $0.02 | Core info |
| Place details (full) | `/api/google-maps/place-details/full` | $0.05 | All fields |

See [rules/partial-vs-full.md](rules/partial-vs-full.md) for tier selection guidance.

## Text Search

Search for places by text query:

```
mcp__x402__fetch(
  url="https://enrichx402.com/api/google-maps/text-search/partial",
  method="POST",
  body={
    "textQuery": "coffee shops in downtown Seattle"
  }
)
```

**Parameters:**
- `textQuery` - Search query (required)
- `locationBias` - Prefer results near a location
- `minRating` - Minimum rating filter (1-5)
- `openNow` - Only open places
- `maxResultCount` - Limit results (default: 20)

**Full tier** adds: reviews, atmosphere data, photos, price level.

## Nearby Search

Search for places near a location:

```
mcp__x402__fetch(
  url="https://enrichx402.com/api/google-maps/nearby-search/partial",
  method="POST",
  body={
    "locationRestriction": {
      "circle": {
        "center": {
          "latitude": 47.6062,
          "longitude": -122.3321
        },
        "radius": 1000
      }
    },
    "includedTypes": ["restaurant", "cafe"]
  }
)
```

**Parameters:**
- `locationRestriction` - Circle with center (lat/lng) and radius in meters
- `includedTypes` - Place types to include
- `excludedTypes` - Place types to exclude
- `minRating` - Minimum rating
- `openNow` - Only open places

## Place Details

Get detailed info for a specific place:

```
mcp__x402__fetch(
  url="https://enrichx402.com/api/google-maps/place-details/partial",
  method="POST",
  body={
    "placeId": "ChIJN1t_tDeuEmsRUsoyG83frY4"
  }
)
```

**Input:**
- `placeId` - Google Place ID (from search results)

**Partial returns:** Name, address, phone, website, hours, rating, types.

**Full returns:** + reviews, atmosphere (wheelchair access, pets allowed), photos, price level.

## Common Place Types

Use these with `includedTypes` / `excludedTypes`:

**Food & Drink:** restaurant, cafe, bar, bakery, coffee_shop

**Lodging:** hotel, motel, lodging, guest_house

**Shopping:** shopping_mall, store, supermarket, clothing_store

**Services:** bank, atm, gas_station, car_repair, car_wash

**Health:** hospital, pharmacy, doctor, dentist

**Entertainment:** movie_theater, museum, park, gym

## Workflows

### Find Businesses in Area

- [ ] (Optional) Check balance: `mcp__x402__get_wallet_info`
- [ ] Text search (partial) to find options
- [ ] Review results and select top picks
- [ ] Get full details for selected places

```
mcp__x402__fetch(
  url="https://enrichx402.com/api/google-maps/text-search/partial",
  method="POST",
  body={"textQuery": "Italian restaurants downtown Portland"}
)
```

```
mcp__x402__fetch(
  url="https://enrichx402.com/api/google-maps/place-details/full",
  method="POST",
  body={"placeId": "ChIJ..."}
)
```

### Nearby Search with Filters

- [ ] Get coordinates for the area
- [ ] Search with location restriction and filters
- [ ] Present sorted results

```
mcp__x402__fetch(
  url="https://enrichx402.com/api/google-maps/nearby-search/partial",
  method="POST",
  body={
    "locationRestriction": {
      "circle": {
        "center": {"latitude": 40.7128, "longitude": -74.0060},
        "radius": 500
      }
    },
    "includedTypes": ["restaurant"],
    "minRating": 4.0,
    "openNow": true
  }
)
```

### Compare Places with Reviews

- [ ] Search to get place IDs
- [ ] Fetch full details for each candidate
- [ ] Compare ratings, reviews, and amenities

```
mcp__x402__fetch(
  url="https://enrichx402.com/api/google-maps/place-details/full",
  method="POST",
  body={"placeId": "place_id_here"}
)
```

## Cost Optimization

### Use Partial Tier When:
- Just need name, address, basic info
- Browsing/discovering options
- Initial search before drilling down

### Use Full Tier When:
- Need reviews/ratings details
- Need atmosphere info (accessibility, etc.)
- Final decision-making

### Efficient Patterns

1. **Search partial, detail full:**
   - Text search (partial) to find places
   - Place details (full) for the one you care about

2. **Batch searches:**
   - Combine filters to reduce calls
   - Use `maxResultCount` to limit results

3. **Cache place IDs:**
   - Place IDs are stable
   - Re-fetch details only when needed

## Response Data

### Partial Tier Fields
- `name` - Place name
- `formattedAddress` - Full address
- `location` - Lat/lng coordinates
- `rating` - Average rating (1-5)
- `userRatingCount` - Number of ratings
- `types` - Place type categories
- `businessStatus` - OPERATIONAL, CLOSED, etc.
- `regularOpeningHours` - Hours of operation
- `nationalPhoneNumber` - Phone number
- `websiteUri` - Website URL

### Full Tier Additional Fields
- `reviews` - User reviews with text and ratings
- `priceLevel` - $ to $$$$
- `accessibilityOptions` - Wheelchair accessible, etc.
- `parkingOptions` - Parking availability
- `paymentOptions` - Accepted payment methods
- `photos` - Photo references
