---
name: mapbox-geospatial-operations
description: Expert guidance on choosing the right geospatial tool based on problem type, accuracy requirements, and performance needs
---

# Mapbox Geospatial Operations Skill

Expert guidance for AI assistants on choosing the right geospatial tools from the Mapbox MCP Server. Focuses on selecting tools based on **what the problem requires** - geometric calculations vs routing, straight-line vs road network, and accuracy needs.

## Core Principle: Problem Type Determines Tool Choice

The Mapbox MCP Server provides two categories of geospatial tools:

1. **Offline Geometric Tools** - Use Turf.js for pure geometric/spatial calculations
2. **Routing & Navigation APIs** - Use Mapbox APIs when you need real-world routing, traffic, or travel times

**The key question: What does the problem actually require?**

### Decision Framework

| Problem Characteristic                                 | Tool Category     | Why                                      |
| ------------------------------------------------------ | ----------------- | ---------------------------------------- |
| **Straight-line distance** (as the crow flies)         | Offline geometric | Accurate for geometric distance          |
| **Road/path distance** (as the crow drives)            | Routing API       | Only routing APIs know road networks     |
| **Travel time**                                        | Routing API       | Requires routing with speed/traffic data |
| **Point containment** (is X inside Y?)                 | Offline geometric | Pure geometric operation                 |
| **Geographic shapes** (buffers, centroids, areas)      | Offline geometric | Mathematical/geometric operations        |
| **Traffic-aware routing**                              | Routing API       | Requires real-time traffic data          |
| **Route optimization** (best order to visit)           | Routing API       | Complex routing algorithm                |
| **High-frequency checks** (e.g., real-time geofencing) | Offline geometric | Instant response, no latency             |

## Decision Matrices by Use Case

### Distance Calculations

**User asks: "How far is X from Y?"**

| What They Actually Mean                            | Tool Choice                         | Why                                      |
| -------------------------------------------------- | ----------------------------------- | ---------------------------------------- |
| Straight-line distance (as the crow flies)         | `distance_tool`                     | Accurate for geometric distance, instant |
| Driving distance (as the crow drives)              | `directions_tool`                   | Only routing knows actual road distance  |
| Walking/cycling distance (as the crow walks/bikes) | `directions_tool`                   | Need specific path network               |
| Travel time                                        | `directions_tool` or `matrix_tool`  | Requires routing with speed data         |
| Distance with current traffic                      | `directions_tool` (driving-traffic) | Need real-time traffic consideration     |

**Example: "What's the distance between these 5 warehouses?"**

- As the crow flies → `distance_tool` (10 calculations, instant)
- As the crow drives → `matrix_tool` (5×5 matrix, one API call, returns actual route distances)

**Key insight:** Use the tool that matches what "distance" means in context. Always clarify: crow flies or crow drives?

### Proximity and Containment

**User asks: "Which points are near/inside this area?"**

| Query Type                   | Tool Choice                                           | Why                                                           |
| ---------------------------- | ----------------------------------------------------- | ------------------------------------------------------------- |
| "Within X meters radius"     | `distance_tool` + filter                              | Simple geometric radius                                       |
| "Within X minutes drive"     | `isochrone_tool` → `point_in_polygon_tool`            | Need routing for travel-time zone, then geometric containment |
| "Inside this polygon"        | `point_in_polygon_tool`                               | Pure geometric containment test                               |
| "Reachable by car in 30 min" | `isochrone_tool`                                      | Requires routing + traffic                                    |
| "Nearest to this point"      | `distance_tool` (geometric) or `matrix_tool` (routed) | Depends on definition of "nearest"                            |

**Example: "Are these 200 addresses in our 30-minute delivery zone?"**

1. Create zone → `isochrone_tool` (routing API - need travel time)
2. Check addresses → `point_in_polygon_tool` (geometric - 200 instant checks)

**Key insight:** Routing for creating travel-time zones, geometric for containment checks

### Routing and Navigation

**User asks: "What's the best route?"**

| Scenario                            | Tool Choice                         | Why                               |
| ----------------------------------- | ----------------------------------- | --------------------------------- |
| A to B directions                   | `directions_tool`                   | Turn-by-turn routing              |
| Optimal order for multiple stops    | `optimization_tool`                 | Solves traveling salesman problem |
| Clean GPS trace                     | `map_matching_tool`                 | Snaps to road network             |
| Just need bearing/compass direction | `bearing_tool`                      | Simple geometric calculation      |
| Route with traffic                  | `directions_tool` (driving-traffic) | Real-time traffic awareness       |
| Fixed-order waypoints               | `directions_tool` with waypoints    | Routing through specific points   |

**Example: "Navigate from hotel to airport"**

- Need turn-by-turn → `directions_tool`
- Just need to know "it's northeast" → `bearing_tool`

**Key insight:** Routing tools for actual navigation, geometric tools for directional info

### Area and Shape Operations

**User asks: "Create a zone around this location"**

| Requirement               | Tool Choice      | Why                      |
| ------------------------- | ---------------- | ------------------------ |
| Simple circular buffer    | `buffer_tool`    | Geometric circle/radius  |
| Travel-time zone          | `isochrone_tool` | Based on routing network |
| Calculate area size       | `area_tool`      | Geometric calculation    |
| Simplify complex boundary | `simplify_tool`  | Geometric simplification |
| Find center of shape      | `centroid_tool`  | Geometric centroid       |

**Example: "Show 5km coverage around each store"**

- 5km radius → `buffer_tool` (geometric circles)
- "What customers can reach in 15 min?" → `isochrone_tool` (routing-based)

**Key insight:** Geometric tools for distance-based zones, routing tools for time-based zones

## Performance and Scale Considerations

### When Volume Affects Tool Choice

**Small operations (< 100 calculations):**

- Geometric tools: Instant, iterate freely
- Routing APIs: Fast enough for most uses

**Medium operations (100-1,000 calculations):**

- Geometric tools: Still fast, no concerns
- Routing APIs: Consider batch operations (matrix_tool)

**Large operations (> 1,000 calculations):**

- Geometric tools: May need optimization but still fast
- Routing APIs: Definitely use batch tools (matrix_tool handles up to 25×25)

**Key insight:** Volume rarely affects geometric tool choice, but routing APIs have batch tools for efficiency

### Real-Time vs Batch

| Use Case                            | Approach             | Tool Choice                              |
| ----------------------------------- | -------------------- | ---------------------------------------- |
| Real-time geofencing (every second) | Geometric checks     | `point_in_polygon_tool` (instant)        |
| Route planning (one-time)           | Full routing         | `directions_tool` or `optimization_tool` |
| Periodic proximity checks           | Geometric distance   | `distance_tool`                          |
| Live traffic routing                | Routing with traffic | `directions_tool` (driving-traffic)      |

## Common Scenarios and Optimal Approaches

### Scenario 1: Store Locator

**User: "Find the closest store and show 5km coverage"**

**Optimal approach:**

1. Search stores → `category_search_tool` (returns distances automatically)
2. Create coverage zone → `buffer_tool` (5km geometric circle)
3. Visualize → `static_map_image_tool`

**Why:** Search already gives distances; geometric buffer for simple radius

### Scenario 2: Delivery Route Optimization

**User: "Optimize delivery to 8 addresses"**

**Optimal approach:**

1. Geocode addresses → `search_and_geocode_tool`
2. Optimize route → `optimization_tool` (TSP solver with routing)

**Why:** Need actual routing for turn-by-turn delivery, not geometric distances

### Scenario 3: Service Area Validation

**User: "Which of these 200 addresses can we deliver to in 30 minutes?"**

**Optimal approach:**

1. Create delivery zone → `isochrone_tool` (30-minute driving)
2. Check each address → `point_in_polygon_tool` (200 geometric checks)

**Why:** Routing for accurate travel-time zone, geometric for fast containment checks

### Scenario 4: GPS Trace Analysis

**User: "How long was this bike ride?"**

**Optimal approach:**

1. Clean GPS trace → `map_matching_tool` (snap to bike paths)
2. Get distance → Use API response or calculate with `distance_tool`

**Why:** Need road/path matching; distance calculation either way works

### Scenario 5: Coverage Analysis

**User: "What's our total service area?"**

**Optimal approach:**

1. Create buffers around each location → `buffer_tool`
2. Calculate total area → `area_tool`
3. Or, if time-based → `isochrone_tool` for each location

**Why:** Geometric for distance-based coverage, routing for time-based

## Anti-Patterns: Using the Wrong Tool Type

### ❌ Don't: Use geometric tools for routing questions

```javascript
// WRONG: User asks "how long to drive there?"
distance_tool({ from: A, to: B });
// Returns 10km as the crow flies, but actual drive is 15km

// CORRECT: Need routing for driving distance
directions_tool({
  coordinates: [
    { longitude: A[0], latitude: A[1] },
    { longitude: B[0], latitude: B[1] }
  ],
  routing_profile: 'mapbox/driving'
});
// Returns actual road distance and drive time as the crow drives
```

**Why wrong:** As the crow flies ≠ as the crow drives

### ❌ Don't: Use routing APIs for geometric operations

```javascript
// WRONG: Check if point is in polygon
// (Can't do this with routing APIs)

// CORRECT: Pure geometric operation
point_in_polygon_tool({ point: location, polygon: boundary });
```

**Why wrong:** Routing APIs don't do geometric containment

### ❌ Don't: Confuse "near" with "reachable"

```javascript
// User asks: "What's reachable in 20 minutes?"

// WRONG: 20-minute distance at average speed
distance_tool + calculate 20min * avg_speed

// CORRECT: Actual routing with road network
isochrone_tool({
  coordinates: {longitude: startLng, latitude: startLat},
  contours_minutes: [20],
  profile: "mapbox/driving"
})
```

**Why wrong:** Roads aren't straight lines; traffic varies

### ❌ Don't: Use routing when bearing is sufficient

```javascript
// User asks: "Which direction is the airport?"

// OVERCOMPLICATED: Full routing
directions_tool({
  coordinates: [
    { longitude: hotel[0], latitude: hotel[1] },
    { longitude: airport[0], latitude: airport[1] }
  ]
});

// BETTER: Just need bearing
bearing_tool({ from: hotel, to: airport });
// Returns: "Northeast (45°)"
```

**Why better:** Simpler, instant, answers the actual question

## Hybrid Approaches: Combining Tool Types

Some problems benefit from using both geometric and routing tools:

### Pattern 1: Routing + Geometric Filter

```
1. directions_tool → Get route geometry
2. buffer_tool → Create corridor around route
3. category_search_tool → Find POIs in corridor
4. point_in_polygon_tool → Filter to those actually along route
```

**Use case:** "Find gas stations along my route"

### Pattern 2: Routing + Distance Calculation

```
1. category_search_tool → Find 10 nearby locations
2. distance_tool → Calculate straight-line distances (geometric)
3. For top 3, use directions_tool → Get actual driving time
```

**Use case:** Quickly narrow down, then get precise routing for finalists

### Pattern 3: Isochrone + Containment

```
1. isochrone_tool → Create travel-time zone (routing)
2. point_in_polygon_tool → Check hundreds of addresses (geometric)
```

**Use case:** "Which customers are in our delivery zone?"

## Decision Algorithm

When user asks a geospatial question:

```
1. Does it require routing, roads, or travel times?
   YES → Use routing API (directions, matrix, isochrone, optimization)
   NO → Continue

2. Does it require traffic awareness?
   YES → Use directions_tool or isochrone_tool with traffic profile
   NO → Continue

3. Is it a geometric/spatial operation?
   - Distance between points (straight-line) → distance_tool
   - Point containment → point_in_polygon_tool
   - Area calculation → area_tool
   - Buffer/zone → buffer_tool
   - Direction/bearing → bearing_tool
   - Geometric center → centroid_tool
   - Bounding box → bounding_box_tool
   - Simplification → simplify_tool

4. Is it a search/discovery operation?
   YES → Use search tools (search_and_geocode, category_search)
```

## Key Decision Questions

Before choosing a tool, ask:

1. **Does "distance" mean as the crow flies or as the crow drives?**
   - As the crow flies (straight-line) → geometric tools
   - As the crow drives (road distance) → routing APIs

2. **Does the user need travel time?**
   - Yes → routing APIs (only they know speeds/traffic)
   - No → geometric tools may suffice

3. **Is this about roads/paths or pure spatial relationships?**
   - Roads/paths → routing APIs
   - Spatial relationships → geometric tools

4. **Does this need to happen in real-time with low latency?**
   - Yes + geometric problem → offline tools (instant)
   - Yes + routing problem → use routing APIs (still fast)

5. **Is accuracy critical, or is approximation OK?**
   - Critical + routing → routing APIs
   - Approximation OK → geometric tools may work

## Terminology Guide

Understanding what users mean:

| User Says             | Usually Means                                      | Tool Type   |
| --------------------- | -------------------------------------------------- | ----------- |
| "Distance"            | Context-dependent! Ask: crow flies or crow drives? | Varies      |
| "How far"             | Often as the crow drives (road distance)           | Routing API |
| "Nearby"              | Usually as the crow flies (straight-line radius)   | Geometric   |
| "Close"               | Could be either - clarify!                         | Ask         |
| "Reachable"           | Travel-time based (crow drives with traffic)       | Routing API |
| "Inside/contains"     | Geometric containment                              | Geometric   |
| "Navigate/directions" | Turn-by-turn routing                               | Routing API |
| "Bearing/direction"   | Compass direction (crow flies)                     | Geometric   |

## Quick Reference

### Geometric Operations (Offline Tools)

- `distance_tool` - Straight-line distance between two points
- `bearing_tool` - Compass direction from A to B
- `midpoint_tool` - Midpoint between two points
- `point_in_polygon_tool` - Is point inside polygon?
- `area_tool` - Calculate polygon area
- `buffer_tool` - Create circular buffer/zone
- `centroid_tool` - Geometric center of polygon
- `bbox_tool` - Min/max coordinates of geometry
- `simplify_tool` - Reduce geometry complexity

### Routing & Navigation (APIs)

- `directions_tool` - Turn-by-turn routing
- `matrix_tool` - Many-to-many travel times
- `optimization_tool` - Route optimization (TSP)
- `isochrone_tool` - Travel-time zones
- `map_matching_tool` - Snap GPS to roads

### When to Use Each Category

**Use Geometric Tools When:**

- Problem is spatial/mathematical (containment, area, bearing)
- Straight-line distance is appropriate
- Need instant results for real-time checks
- Pure geometry (no roads/traffic involved)

**Use Routing APIs When:**

- Need actual driving/walking/cycling distances
- Need travel times
- Need to consider road networks
- Need traffic awareness
- Need route optimization
- Need turn-by-turn directions

## Integration with Other Skills

**Works with:**

- **mapbox-search-patterns**: Search for locations, then use geospatial operations
- **mapbox-web-performance-patterns**: Optimize rendering of geometric calculations
- **mapbox-token-security**: Ensure requests use properly scoped tokens

## Resources

- [Mapbox MCP Server](https://github.com/mapbox/mcp-server)
- [Turf.js Documentation](https://turfjs.org/) (Powers geometric tools)
- [Mapbox Directions API](https://docs.mapbox.com/api/navigation/directions/)
- [Mapbox Isochrone API](https://docs.mapbox.com/api/navigation/isochrone/)
- [Mapbox Matrix API](https://docs.mapbox.com/api/navigation/matrix/)
- [Mapbox Optimization API](https://docs.mapbox.com/api/navigation/optimization/)
