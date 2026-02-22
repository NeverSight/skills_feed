---
name: Real Estate Photo Generation
description: Generate professional real estate photography, virtual staging, interior design visuals, and architectural renders using each::sense API
metadata:
  category: real-estate
  api: each::sense
  endpoint: https://sense.eachlabs.run/chat
  method: POST
  features:
    - listing-photos
    - virtual-staging
    - interior-design
    - architectural-renders
    - renovation-previews
---

# Real Estate Photo Generation

Generate stunning real estate visuals using the each::sense API. Create professional listing photos, virtually stage empty rooms, design interior spaces, render architectural concepts, and preview renovations - all through natural language prompts.

## Overview

The each::sense API provides comprehensive real estate visualization capabilities:

- **Listing Photos**: Generate professional exterior and interior shots for property listings
- **Virtual Staging**: Transform empty rooms into furnished, styled spaces
- **Interior Design**: Create design concepts for kitchens, bathrooms, living rooms, and more
- **Architectural Renders**: Visualize new construction and renovations before they happen
- **Renovation Previews**: Show before/after transformations to help buyers envision potential

## Quick Start

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate a professional real estate photo of a modern 3-bedroom house exterior with manicured lawn, blue sky, warm afternoon lighting",
    "mode": "max"
  }'
```

## Real Estate Content Types

| Content Type | Description | Best Use Cases |
|--------------|-------------|----------------|
| Exterior Shots | Front facade, curb appeal photos | MLS listings, marketing materials |
| Interior Rooms | Living rooms, bedrooms, kitchens, bathrooms | Property tours, virtual walkthroughs |
| Virtual Staging | Digitally furnished empty spaces | Vacant property marketing |
| Twilight Shots | Dusk/evening exterior photography | Luxury listings, dramatic presentation |
| Aerial Views | Drone-style overhead perspectives | Large properties, lot visualization |
| Architectural Renders | 3D visualization of designs | New construction, pre-sale marketing |
| Renovation Previews | Before/after transformations | Fixer-upper potential, investor presentations |

## Use Case Examples

### 1. Exterior Property Shot

Generate a classic front-of-house listing photo:

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Professional real estate exterior photo of a two-story colonial house with white siding, black shutters, red front door, landscaped front yard with flowering bushes, paved driveway, bright sunny day with blue sky and white clouds, wide angle lens perspective, HDR photography style",
    "mode": "max"
  }'
```

### 2. Living Room Interior

Create an inviting living space photo:

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Bright and airy open concept living room, hardwood floors, large windows with natural light streaming in, modern gray sectional sofa, white walls, fireplace with stone surround, 10 foot ceilings, professional real estate interior photography, wide angle shot",
    "mode": "max"
  }'
```

### 3. Kitchen Photography

Showcase a stunning kitchen:

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Modern farmhouse kitchen with white shaker cabinets, quartz countertops, stainless steel appliances, large center island with pendant lighting, subway tile backsplash, breakfast nook with window, professional real estate photography, bright natural lighting, wide angle perspective highlighting the spacious layout",
    "mode": "max"
  }'
```

### 4. Virtual Staging (Empty Room to Furnished)

Transform an empty room using an existing photo:

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Virtually stage this empty living room with contemporary furniture: a modern beige sectional sofa, glass coffee table, area rug, floor lamp, wall art, potted plants. Keep the existing room architecture, flooring, and windows. Make it look professionally staged and inviting for real estate listing",
    "image_urls": ["https://example.com/empty-living-room.jpg"],
    "mode": "max"
  }'
```

### 5. Twilight/Dusk Exterior

Create dramatic evening curb appeal:

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Luxury home exterior at twilight, dusk photography, warm interior lights glowing through windows, dramatic purple and orange sky, landscape lighting illuminating walkway and architectural features, modern Mediterranean style villa, pool visible with underwater lighting, professional real estate twilight photography",
    "mode": "max"
  }'
```

### 6. Bathroom Renovation Preview

Visualize a bathroom remodel:

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Modern spa-like master bathroom renovation, freestanding soaking tub, walk-in shower with frameless glass and rainfall showerhead, double vanity with vessel sinks, large format marble tiles, LED mirror lighting, heated floors, neutral palette with brass fixtures, professional interior photography",
    "mode": "max"
  }'
```

### 7. Backyard/Outdoor Space

Showcase outdoor living areas:

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Expansive backyard with covered patio, outdoor kitchen with built-in grill and bar seating, rectangular swimming pool with spa, manicured lawn, mature landscaping, string lights overhead, outdoor fireplace, comfortable seating area, golden hour lighting, professional real estate photography showing entire outdoor space",
    "mode": "max"
  }'
```

### 8. Aerial/Drone View

Generate overhead property perspectives:

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Aerial drone photography of residential property on 2-acre lot, birds eye view showing ranch-style home, detached 3-car garage, swimming pool, tennis court, circular driveway, surrounded by trees, neighboring properties visible, clear sunny day, professional real estate aerial photography",
    "mode": "max"
  }'
```

### 9. Floor Plan to 3D Render

Visualize architectural plans:

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "3D architectural render of open floor plan home interior, view from above at 45 degree angle showing living room flowing into kitchen and dining area, furniture placed throughout, realistic materials and textures, afternoon sunlight through windows, architectural visualization style, professional quality",
    "mode": "max"
  }'
```

### 10. Before/After Renovation

Show transformation potential:

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Transform this dated kitchen into a modern renovation: replace oak cabinets with white shaker style, add quartz countertops, install stainless steel appliances, update to pendant lighting over island, add subway tile backsplash, keep the same window and layout, photorealistic renovation preview",
    "image_urls": ["https://example.com/dated-kitchen.jpg"],
    "mode": "max"
  }'
```

## Using image_urls for Virtual Staging

The `image_urls` parameter enables powerful virtual staging and renovation visualization by providing existing property photos as reference:

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Virtually stage this empty bedroom as a luxurious master suite: king size bed with upholstered headboard, matching nightstands with lamps, bench at foot of bed, area rug, curtains on windows, tasteful artwork. Maintain the room dimensions, flooring, and natural light from the windows",
    "image_urls": ["https://your-domain.com/empty-bedroom-photo.jpg"],
    "mode": "max"
  }'
```

**Virtual Staging Tips:**
- Provide high-quality, well-lit photos of empty rooms
- Reference the existing architectural features you want preserved
- Specify furniture style that matches the property's character
- Request realistic proportions and natural-looking placement

## Best Practices for Real Estate Photography

### Composition and Perspective
- Use wide angle language ("wide angle view", "expansive shot") to capture full rooms
- Specify corner angles for interior shots to show depth
- Include ceiling and floor references to convey room height
- Mention "straight vertical lines" to avoid distortion

### Lighting Descriptions
- "Bright natural light streaming through windows"
- "Warm afternoon golden hour lighting"
- "HDR balanced exposure" for interiors with window views
- "Soft diffused daylight" for even, flattering illumination

### Staging and Styling
- Keep staging neutral and widely appealing
- Specify "decluttered" and "clean" for professional look
- Include lifestyle elements: fresh flowers, books, throw blankets
- Match staging style to property price point

### Technical Quality
- Request "professional real estate photography" in prompts
- Add "high resolution" or "detailed" for sharp results
- Mention "color corrected" for accurate representation
- Include "publication quality" for listing-ready images

## Prompt Tips

**Effective prompt elements for real estate visuals:**

| Element | Example Phrases |
|---------|-----------------|
| Wide Angle | "wide angle lens", "expansive view", "full room visible" |
| Bright & Airy | "natural light flooding in", "bright and welcoming", "light-filled space" |
| Feature Highlights | "showcasing the fireplace", "highlighting the chef's kitchen", "featuring the pool" |
| Professional Quality | "MLS-ready photo", "publication quality", "professional real estate photography" |
| Time of Day | "morning light", "golden hour", "twilight", "midday sun" |
| Architecture Style | "modern farmhouse", "contemporary", "traditional", "mid-century modern" |

## Mode Selection

Choose the appropriate mode based on your quality and speed requirements:

| Mode | Best For | Characteristics |
|------|----------|-----------------|
| `max` | Final listing photos, marketing materials, client presentations | Highest quality, maximum detail, best for publication |
| `eco` | Quick previews, concept exploration, draft iterations | Faster generation, suitable for review stages |

```bash
# High-quality listing photo
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Luxury master bedroom with king bed, tray ceiling, sitting area by bay window",
    "mode": "max"
  }'

# Quick concept preview
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Modern kitchen concept with waterfall island",
    "mode": "eco"
  }'
```

## Multi-Turn Sessions for Property Series

Use `session_id` to maintain consistency when generating multiple images for the same property listing:

```bash
# Generate exterior shot
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Modern craftsman style home exterior, gray siding with white trim, covered front porch, landscaped yard, sunny day",
    "session_id": "property-123-listing",
    "mode": "max"
  }'

# Generate matching interior - maintains style consistency
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Living room interior of this craftsman home, matching the exterior style, built-in bookshelves, hardwood floors, neutral palette",
    "session_id": "property-123-listing",
    "mode": "max"
  }'

# Generate kitchen with same style language
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Kitchen of this craftsman home, shaker cabinets, apron sink, butcher block island, consistent with the home style",
    "session_id": "property-123-listing",
    "mode": "max"
  }'
```

**Benefits of session-based property series:**
- Consistent architectural style across all images
- Cohesive color palette and finishes
- Unified quality and lighting approach
- Professional listing package feel

## Error Handling

Handle API responses appropriately in your integration:

```bash
# Request with error handling
response=$(curl -s -w "\n%{http_code}" -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Modern house exterior photo",
    "mode": "max"
  }')

http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | sed '$d')

if [ "$http_code" -eq 200 ]; then
  echo "Success: $body"
elif [ "$http_code" -eq 401 ]; then
  echo "Error: Invalid API key"
elif [ "$http_code" -eq 429 ]; then
  echo "Error: Rate limit exceeded, retry after delay"
else
  echo "Error $http_code: $body"
fi
```

**Common issues and solutions:**

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid or missing API key | Verify EACHLABS_API_KEY is set correctly |
| 429 Too Many Requests | Rate limit exceeded | Implement exponential backoff retry |
| 400 Bad Request | Malformed request body | Validate JSON structure and required fields |
| Timeout | Complex generation taking too long | Consider using `eco` mode for faster results |

## Related Skills

- **Image Generation** - General purpose image creation for marketing materials
- **Image Edit** - Modify and enhance existing property photos
- **Product Visuals** - Showcase home products and furnishings
