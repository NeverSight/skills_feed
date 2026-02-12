---
name: mapbox-search-patterns
description: Expert guidance on choosing the right Mapbox search tool and parameters for geocoding, POI search, and location discovery
---

# Mapbox Search Patterns Skill

Expert guidance for AI assistants on using Mapbox search tools effectively. Covers tool selection, parameter optimization, and best practices for geocoding, POI search, and location discovery.

## Available Search Tools

### 1. search_and_geocode_tool

**Best for:** Specific places, addresses, brands, named locations

**Use when query contains:**

- Specific names: "Starbucks on 5th Avenue", "Empire State Building"
- Brand names: "McDonald's", "Whole Foods"
- Addresses: "123 Main Street, Seattle", "1 Times Square"
- Chain stores: "Target"
- Cities/places: "San Francisco", "Portland"

**Don't use for:** Generic categories ("coffee shops", "museums")

### 2. category_search_tool

**Best for:** Generic place types, categories, plural queries

**Use when query contains:**

- Generic types: "coffee shops", "restaurants", "gas stations"
- Plural forms: "museums", "hotels", "parks"
- Is-a phrases: "any coffee shop", "all restaurants", "nearby pharmacies"
- Industry terms: "electric vehicle chargers", "ATMs"

**Don't use for:** Specific names or brands

### 3. reverse_geocode_tool

**Best for:** Converting coordinates to addresses, cities, towns, postcodes

**Use when:**

- Have GPS coordinates, need human-readable address
- Need to identify what's at a specific location
- Converting user location to address

## Tool Selection Decision Matrix

| User Query                      | Tool                    | Reasoning                |
| ------------------------------- | ----------------------- | ------------------------ |
| "Find Starbucks on Main Street" | search_and_geocode_tool | Specific brand name      |
| "Find coffee shops nearby"      | category_search_tool    | Generic category, plural |
| "What's at 37.7749, -122.4194?" | reverse_geocode_tool    | Coordinates to address   |
| "Empire State Building"         | search_and_geocode_tool | Specific named POI       |
| "hotels in downtown Seattle"    | category_search_tool    | Generic type + location  |
| "Target store locations"        | search_and_geocode_tool | Brand name (even plural) |
| "any restaurant near me"        | category_search_tool    | Generic + "any" phrase   |
| "123 Main St, Boston, MA"       | search_and_geocode_tool | Specific address         |
| "electric vehicle chargers"     | category_search_tool    | Industry category        |
| "McDonald's"                    | search_and_geocode_tool | Brand name               |

## Parameter Guidance

### Proximity vs Bbox vs Country

**Three ways to spatially constrain search results:**

#### 1. proximity (STRONGLY RECOMMENDED)

**What it does:** Biases results toward a location, but doesn't exclude distant matches

**Use when:**

- User says "near me", "nearby", "close to"
- Have a reference point but want some flexibility
- Want results sorted by relevance to a point

**Example:**

```json
{
  "q": "pizza",
  "proximity": {
    "longitude": -122.4194,
    "latitude": 37.7749
  }
}
```

**Why this works:** API returns SF pizza places first, but might include famous NYC pizzerias if highly relevant

**⚠️ Critical:** Always set proximity when you have a reference location! Without it, results are IP-based or global.

#### 2. bbox (Bounding Box)

**What it does:** Hard constraint - ONLY returns results within the box

**Use when:**

- User specifies an area: "in downtown", "within this neighborhood"
- Have a defined service area
- Need to guarantee results are within bounds

**Example:**

```json
{
  "q": "hotel",
  "bbox": [-122.51, 37.7, -122.35, 37.83] // [minLon, minLat, maxLon, maxLat]
}
```

**Why this works:** Guarantees all hotels are within SF's downtown area

**⚠️ Watch out:** Too small = no results; too large = irrelevant results

#### 3. country

**What it does:** Limits results to specific countries

**Use when:**

- User specifies country: "restaurants in France"
- Building country-specific features
- Need to respect regional boundaries
- Or it is otherwise clear they want results within a specific country

**Example:**

```json
{
  "q": "Paris",
  "country": ["FR"] // ISO 3166 alpha-2 codes
}
```

**Why this works:** Finds Paris, France (not Paris, Texas)

**Can combine:** `proximity` + `country` + `bbox` or any combination of the three

### Decision Matrix: Spatial Filters

| Scenario                           | Use                                 | Why                               |
| ---------------------------------- | ----------------------------------- | --------------------------------- |
| "Find coffee near me"              | proximity                           | Bias toward user location         |
| "Coffee shops in downtown Seattle" | proximity + bbox                    | Center on downtown, limit to area |
| "Hotels in France"                 | country                             | Hard country boundary             |
| "Best pizza in San Francisco"      | proximity + country ["US"]          | Bias to SF, limit to US           |
| "Gas stations along this route"    | bbox around route                   | Hard constraint to route corridor |
| "Restaurants within 5 miles"       | proximity (then filter by distance) | Bias nearby, filter results       |

### Setting limit Parameter

**category_search_tool only** (1-25, default 10)

| Use Case              | Limit | Reasoning               |
| --------------------- | ----- | ----------------------- |
| Quick suggestions     | 5     | Fast, focused results   |
| Standard list         | 10    | Default, good balance   |
| Comprehensive search  | 25    | Maximum allowed         |
| Map visualization     | 25    | Show all nearby options |
| Dropdown/autocomplete | 5     | Don't overwhelm UI      |

**Performance tip:** Lower limits = faster responses

### types Parameter (search_and_geocode_tool)

**Filter by feature type:**

| Type       | What It Includes                           | Use When                          |
| ---------- | ------------------------------------------ | --------------------------------- |
| `poi`      | Points of interest (businesses, landmarks) | Looking for POIs, not addresses   |
| `address`  | Street addresses                           | Need specific address             |
| `place`    | Cities, neighborhoods, regions             | Looking for area/region           |
| `street`   | Street names without numbers               | Need street, not specific address |
| `postcode` | Postal codes                               | Searching by ZIP/postal code      |
| `district` | Districts, neighborhoods                   | Area-based search                 |
| `locality` | Towns, villages                            | Municipality search               |
| `country`  | Country names                              | Country-level search              |

**Example combinations:**

```json
// Only POIs and addresses, no cities
{"q": "Paris", "types": ["poi", "address"]}
// Returns Paris Hotel, Paris Street, not Paris, France

// Only places (cities/regions)
{"q": "Paris", "types": ["place"]}
// Returns Paris, France; Paris, Texas; etc.
```

**Default behavior:** All types included (usually what you want)

### poi_category Parameter

**search_and_geocode_tool:** Narrow generic searches

```json
{
  "q": "lunch",
  "poi_category": ["restaurant", "cafe"],
  "proximity": { "longitude": -122.4194, "latitude": 37.7749 }
}
```

**When to use:**

- Generic query that could match multiple categories
- Want to focus search within category
- User specifies type implicitly

**category_search_tool:** Use `poi_category_exclusions` instead

```json
{
  "category": "food_and_drink",
  "poi_category_exclusions": ["bar", "nightclub"]
}
```

**When to use:**

- Broad category but want to exclude subcategories
- "Restaurants but not fast food"

### auto_complete Parameter (search_and_geocode_tool)

**What it does:** Enables partial/fuzzy matching

| Setting           | Behavior                     | Use When                      |
| ----------------- | ---------------------------- | ----------------------------- |
| `true`            | Matches partial words, typos | User typing in real-time      |
| `false` (default) | Exact matching               | Final query, not autocomplete |

**Example:**

<!-- cspell:disable -->

```json
// User types "starb"
{ "q": "starb", "auto_complete": true }
// Returns: Starbucks, Starboard Tavern, etc.
```

**Use for:**

- Search-as-you-type interfaces
- Handling typos ("mcdonalds" → McDonald's)
<!-- cspell:enable -->
- Incomplete queries

**Don't use for:**

- Final/submitted queries (less precise)
- When you need exact matches

### ETA Parameters (search_and_geocode_tool)

**Request estimated time of arrival to results**

**Parameters:**

- `eta_type`: Set to `"navigation"`
- `navigation_profile`: `"driving"` | `"walking"` | `"cycling"`
- `origin`: Starting coordinates

**Use when:**

- User asks "how long to get there?"
- Sorting by travel time, not distance
- Need route time, not straight-line distance

**Example:**

```json
{
  "q": "grocery stores",
  "proximity": { "longitude": -122.4194, "latitude": 37.7749 },
  "eta_type": "navigation",
  "navigation_profile": "driving",
  "origin": { "longitude": -122.4194, "latitude": 37.7749 }
}
```

**Returns:** Results with `eta` (travel time in seconds)

**⚠️ Cost:** Requires routing calculation per result (counts toward API quota)

**When NOT to use:**

- Just need straight-line distance (use distance_tool offline after search)
- Budget-conscious (adds API cost)

### format Parameter (category_search_tool)

**Choose output format:**

| Format                     | Returns                | Use When                      |
| -------------------------- | ---------------------- | ----------------------------- |
| `formatted_text` (default) | Human-readable text    | Displaying to user directly   |
| `json_string`              | GeoJSON as JSON string | Need to parse/process results |

**Example:**

**formatted_text:**

```
1. Blue Bottle Coffee
   Address: 66 Mint St, San Francisco, CA
   Coordinates: 37.7825, -122.4052
   Type: poi
```

**json_string:**

```json
{
  "type": "FeatureCollection",
  "features": [{
    "type": "Feature",
    "geometry": {"type": "Point", "coordinates": [-122.4052, 37.7825]},
    "properties": {"name": "Blue Bottle Coffee", ...}
  }]
}
```

**Decision:**

- Showing list to user → `formatted_text`
- Plotting on map → `json_string` (parse and use coordinates)
- Further processing → `json_string`

### language Parameter

**ISO language codes** (e.g., "en", "es", "fr", "de", "ja", "zh")

**Use when:**

- Building multilingual app
- User's language preference known
- Need localized names

**Example:**

```json
{
  "q": "東京タワー",
  "language": "ja"
}
// Returns results in Japanese
```

**Default:** English (if not specified)

**Tip:** Match user's locale for best experience

## Common Patterns and Workflows

### Pattern 1: "Near Me" Search

**User:** "Find coffee shops near me"

**Optimal approach:**

```
1. Get user's location (from app/browser)
2. Use category_search_tool:
   - category: "coffee_shop"
   - proximity: user's coordinates
   - limit: 10
```

**Why:** Category tool for generic "coffee shops", proximity for "near me"

### Pattern 2: Branded Chain Lookup

**User:** "Find all Starbucks in Seattle"

**Optimal approach:**

```
1. Use search_and_geocode_tool:
   - q: "Starbucks"
   - proximity: Seattle coordinates
   - country: ["US"]
2. Or if need strict boundary:
   - bbox: Seattle city bounds
```

**Why:** Brand name = search_and_geocode_tool; proximity biases to Seattle

### Pattern 3: Address Geocoding

**User:** "What are the coordinates of 1600 Pennsylvania Ave?"

**Optimal approach:**

```
Use search_and_geocode_tool:
- q: "1600 Pennsylvania Ave, Washington DC"
- types: ["address"]  // Focus on addresses
- country: ["US"]     // Narrow to US
```

**Why:** Specific address with country context for disambiguation

### Pattern 4: Category Search with Area Restriction

**User:** "Show me all hotels in downtown Portland"

**Optimal approach:**

```
1. Geocode "downtown Portland" → get center point
2. Define downtown bbox (or use 1-2 mile radius)
3. Use category_search_tool:
   - category: "hotel"
   - bbox: downtown bounds (or proximity + filter by distance)
   - limit: 25  // Get comprehensive list
```

**Why:** Category for "hotels", bbox for "in downtown" hard boundary

### Pattern 5: Reverse Geocoding

**User:** "What's at these GPS coordinates?"

**Optimal approach:**

```
Use reverse_geocode_tool:
- longitude: -122.4194
- latitude: 37.7749
- types: ["address"]  // Get address (can also use place, locality, postcode, etc.)
```

**Why:** Coordinates → address is exactly what reverse geocoding does

### Pattern 6: Route-Based Search

**User:** "Find gas stations along my route"

**Optimal approach:**

```
1. Get route geometry from directions_tool
2. Create bbox around route (use bounding_box_tool)
3. Use category_search_tool:
   - category: "gas_station"
   - bbox: route bounding box
4. Filter results to those within X meters of route (use distance_tool)
```

**Why:** Bbox for rough filter, then distance calculation for precision

### Pattern 7: Multilingual POI Search

**User:** "Find ramen shops" (user locale: ja)

**Optimal approach:**

```
Use category_search_tool:
- category: "ramen_restaurant" (or "restaurant")
- language: "ja"
- proximity: user location
```

**Why:** Returns Japanese names/addresses for better UX

## Anti-Patterns to Avoid

### ❌ Don't: Use category_search for brands

```javascript
// BAD
category_search_tool({ category: 'starbucks' });
// "starbucks" is not a category, returns error

// GOOD
search_and_geocode_tool({ q: 'Starbucks' });
```

### ❌ Don't: Use search_and_geocode for generic categories

```javascript
// BAD
search_and_geocode_tool({ q: 'coffee shops' });
// Less precise, may return unrelated results

// GOOD
category_search_tool({ category: 'coffee_shop' });
```

### ❌ Don't: Forget proximity for local searches

```javascript
// BAD - Results may be anywhere globally
category_search_tool({ category: 'restaurant' });

// GOOD - Biased to user location
category_search_tool({
  category: 'restaurant',
  proximity: { longitude: -122.4194, latitude: 37.7749 }
});
```

### ❌ Don't: Use bbox when you mean proximity

```javascript
// BAD - Hard boundary may exclude good nearby results
search_and_geocode_tool({
  q: 'pizza',
  bbox: [-122.42, 37.77, -122.41, 37.78] // Tiny box
});

// GOOD - Bias toward point, but flexible
search_and_geocode_tool({
  q: 'pizza',
  proximity: { longitude: -122.4194, latitude: 37.7749 }
});
```

### ❌ Don't: Request ETA unnecessarily

```javascript
// BAD - Costs API quota for routing calculations
search_and_geocode_tool({
  q: 'museums',
  eta_type: 'navigation',
  navigation_profile: 'driving'
});
// User didn't ask for travel time!

// GOOD - Only add ETA when needed
search_and_geocode_tool({ q: 'museums' });
// If user asks "how long to get there?", then add ETA
```

### ❌ Don't: Set limit too high for UI display

```javascript
// BAD - Overwhelming for simple dropdown
category_search_tool({
  category: 'restaurant',
  limit: 25
});
// Returns 25 restaurants for a 5-item dropdown

// GOOD - Match UI needs
category_search_tool({
  category: 'restaurant',
  limit: 5
});
```

## Performance Optimization

### Minimize API Calls

**Pattern: Geocode once, reuse coordinates**

```
// GOOD
1. User enters "Seattle"
2. Geocode "Seattle" → (lng, lat)
3. Use those coordinates for multiple category searches
4. Cache coordinates for session

// BAD
1. Geocode "Seattle" for coffee search
2. Geocode "Seattle" again for restaurant search
3. Geocode "Seattle" again for hotel search
```

### Set Appropriate Limits

| UI Context            | Recommended Limit |
| --------------------- | ----------------- |
| Autocomplete dropdown | 5                 |
| List view             | 10                |
| Map view              | 25                |
| Export/download       | 25 (or paginate)  |

### Use Offline Tools When Possible

**After getting search results:**

```
1. category_search_tool → Get POIs
2. distance_tool (offline) → Calculate distances
3. bearing_tool (offline) → Get directions
```

**Why:** Search once (API), then use offline tools for calculations (free, fast)

## Combining Search with Other Tools

### Search → Distance Calculation

```
1. category_search_tool({category: "hospital", proximity: user_location})
   → Returns 10 hospitals with coordinates
2. distance_tool(user_location, each_hospital)
   → Calculate exact distances offline
3. Sort by distance
```

### Search → Directions

```
1. search_and_geocode_tool({q: "Space Needle"})
   → Get destination coordinates
2. directions_tool({from: user_location, to: space_needle_coords})
   → Get turn-by-turn directions
```

### Search → Isochrone → Containment Check

```
1. search_and_geocode_tool({q: "warehouse"})
   → Get warehouse coordinates
2. isochrone_tool({coordinates: warehouse, time: 30, profile: "driving"})
   → Get 30-minute delivery zone polygon
3. point_in_polygon_tool(customer_address, delivery_zone)
   → Check if customer is in delivery zone
```

### Search → Static Map Visualization

```
1. category_search_tool({category: "restaurant", limit: 10})
   → Get restaurant coordinates
2. static_map_image_tool({
     markers: restaurant_coordinates,
     auto_fit: true
   })
   → Create map image showing all restaurants
```

## Handling No Results

### If category_search returns no results:

**Possible reasons:**

1. Invalid category → Use `resource_reader_tool` with `mapbox://categories` to see valid categories
2. Too restrictive bbox → Expand area or use proximity instead
3. No POIs in area → Try broader category or remove spatial filters
4. Wrong country filter → Check country codes

**Example recovery:**

```
1. category_search_tool({category: "taco"}) → No results
2. Check: Is "taco" a valid category?
   → Use category_list_tool → See "mexican_restaurant" is valid
3. Retry: category_search_tool({category: "mexican_restaurant"}) → Success
```

### If search_and_geocode returns no results:

**Possible reasons:**

1. Typo in query → Retry with `auto_complete: true`
2. Too specific → Broaden search (remove address numbers, try nearby city)
3. Wrong types filter → Remove or expand types
4. Not a recognized place → Check spelling, try alternative names

## Category List Resource

**Get valid categories:** Use `resource_reader_tool` or `category_list_tool`

```
resource_reader_tool({uri: "mapbox://categories"})
```

**Returns:** All valid category IDs (e.g., "restaurant", "hotel", "gas_station")

**When to use:**

- User enters free-text category
- Need to map user terms to Mapbox categories
- Validating category before search

**Example mapping:**

- User: "places to eat" → Category: "restaurant"
- User: "gas" → Category: "gas_station"
- User: "lodging" → Category: "hotel"

## Quick Reference

### Tool Selection Flowchart

```
User query contains...

→ Specific name/brand (Starbucks, Empire State Building)
  → search_and_geocode_tool

→ Generic category/plural (coffee shops, museums, any restaurant)
  → category_search_tool

→ Coordinates → Address
  → reverse_geocode_tool

→ Address → Coordinates
  → search_and_geocode_tool with types: ["address"]
```

### Essential Parameters Checklist

**For local searches, ALWAYS set:**

- ✅ `proximity` (or bbox if strict boundary needed)

**For category searches, consider:**

- ✅ `limit` (match UI needs)
- ✅ `format` (json_string if plotting on map)

**For disambiguation, use:**

- ✅ `country` (when geographic context matters)
- ✅ `types` (when feature type matters)

**For travel-time ranking:**

- ✅ `eta_type`, `navigation_profile`, `origin` (costs API quota)

## Common Mistakes

1. **Forgetting proximity** → Results are global/IP-based
2. **Using wrong tool** → category_search for "Starbucks" (use search_and_geocode)
3. **Invalid category** → Check category_list first
4. **Bbox too small** → No results; use proximity instead
5. **Requesting ETA unnecessarily** → Adds API cost
6. **Limit too high for UI** → Overwhelming user
7. **Not filtering types** → Get cities when you want POIs

## Integration with Other Skills

**Works with:**

- **mapbox-geospatial-operations**: After search, use offline distance/bearing calculations
- **mapbox-web-integration-patterns**: Display search results on map in web app
- **mapbox-token-security**: Ensure search requests use properly scoped tokens

## Resources

- [Mapbox Search Box API Docs](https://docs.mapbox.com/api/search/search-box/)
- [Category Search API](https://docs.mapbox.com/api/search/search-box/#category-search)
- [Geocoding API](https://docs.mapbox.com/api/search/geocoding/)
- [Category List Resource](https://docs.mapbox.com/api/search/search-box/#category-list)
