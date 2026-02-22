---
name: virtual-staging
description: Transform empty rooms into beautifully furnished spaces using each::sense AI. Create photorealistic virtual staging for real estate listings, commercial properties, and interior design visualization.
metadata:
  author: eachlabs
  version: "1.0"
---

# Virtual Staging

Transform empty or outdated rooms into beautifully furnished spaces using each::sense. This skill creates photorealistic virtual staging for real estate listings, helping properties sell 73% faster with 72% more listing views.

## Features

- **Living Room Staging**: Transform empty spaces into inviting living areas
- **Bedroom Staging**: Create cozy, aspirational bedrooms
- **Kitchen Staging**: Showcase kitchen potential with modern appliances and decor
- **Home Office Staging**: Appeal to remote workers with functional workspaces
- **Outdoor/Patio Staging**: Visualize outdoor living spaces
- **Multiple Style Options**: Modern, traditional, minimalist, contemporary, and more
- **Commercial Staging**: Office spaces, retail, and commercial properties
- **Declutter & Stage**: Remove existing furniture and restage with better design

## Quick Start

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Stage this empty living room with modern furniture, neutral tones, and natural lighting. Add a sectional sofa, coffee table, area rug, and minimal decor.",
    "mode": "max",
    "image_urls": ["https://example.com/empty-living-room.jpg"]
  }'
```

## Why Virtual Staging?

| Metric | Impact |
|--------|--------|
| Faster Sales | 73% faster than non-staged listings |
| More Views | 72% increase in listing views |
| Cost Savings | 95% cheaper than physical staging |
| Turnaround | Minutes instead of days |

## Use Case Examples

### 1. Empty Room to Furnished Living Room

Transform a vacant living room into an inviting, furnished space.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Stage this empty living room with warm, inviting furniture. Add a large comfortable sofa, accent chairs, coffee table, area rug, floor lamp, and subtle wall art. Use neutral earth tones that appeal to broad buyers.",
    "mode": "max",
    "image_urls": ["https://example.com/empty-living-room.jpg"]
  }'
```

### 2. Bedroom Staging

Create a serene, restful bedroom that helps buyers visualize themselves in the space.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Stage this empty bedroom as a master suite. Add a king-size bed with plush bedding, nightstands with lamps, a bench at the foot of the bed, and soft curtains. Keep it elegant but not cluttered. Neutral color palette with subtle blue accents.",
    "mode": "max",
    "image_urls": ["https://example.com/empty-bedroom.jpg"]
  }'
```

### 3. Kitchen Staging

Showcase kitchen potential with thoughtful staging elements.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Stage this kitchen with lifestyle elements. Add bar stools at the island, pendant lighting, a fruit bowl on the counter, fresh flowers in a vase, and coordinated dish towels. Make it look lived-in but immaculate, ready for a real estate photo.",
    "mode": "max",
    "image_urls": ["https://example.com/empty-kitchen.jpg"]
  }'
```

### 4. Home Office Staging

Appeal to remote workers with a functional, stylish workspace.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Transform this empty room into a professional home office. Add a modern desk with ergonomic chair, bookshelf with books and decor, desk lamp, and a small plant. Include good task lighting and keep it organized and productive-looking.",
    "mode": "max",
    "image_urls": ["https://example.com/empty-room.jpg"]
  }'
```

### 5. Outdoor/Patio Staging

Visualize outdoor living potential.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Stage this empty patio/deck area as an outdoor living space. Add comfortable outdoor seating with cushions, a coffee table, potted plants, string lights, and outdoor rug. Make it feel like an extension of the home, perfect for entertaining.",
    "mode": "max",
    "image_urls": ["https://example.com/empty-patio.jpg"]
  }'
```

### 6. Different Furniture Styles

Generate the same room with different design aesthetics.

```bash
# Modern/Contemporary Style
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Stage this room in modern contemporary style. Clean lines, minimal furniture, neutral colors with bold accent pieces, geometric patterns, and sleek finishes. Include a low-profile sofa, glass coffee table, and abstract wall art.",
    "mode": "max",
    "image_urls": ["https://example.com/empty-room.jpg"],
    "session_id": "staging-styles-demo"
  }'

# Traditional Style (same session for comparison)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Now stage the same room in traditional style. Classic furniture with curved lines, rich wood tones, warm colors, elegant fabrics, and ornate details. Include a classic sofa, wooden coffee table, and traditional artwork.",
    "session_id": "staging-styles-demo"
  }'

# Minimalist Style (same session)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Now stage it minimalist style. Very few furniture pieces, lots of negative space, monochromatic color scheme, essential items only. Simple sofa, single plant, minimal decor. Less is more.",
    "session_id": "staging-styles-demo"
  }'
```

### 7. Commercial Space Staging

Stage office buildings, retail spaces, and commercial properties.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Stage this empty commercial office space. Add modern workstations, ergonomic chairs, a reception area with seating, plants, and professional decor. Make it look like a productive, appealing workplace that companies would want to lease.",
    "mode": "max",
    "image_urls": ["https://example.com/empty-office-space.jpg"]
  }'
```

### 8. Before/After Comparison - Multiple Views

Create staged versions of multiple rooms for a complete listing.

```bash
# Living room
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Stage this living room photo for a real estate listing. Modern farmhouse style with comfortable furniture, cozy textiles, and warm lighting. Keep architectural features visible.",
    "mode": "max",
    "image_urls": ["https://example.com/listing-living-room.jpg"],
    "session_id": "full-home-staging"
  }'

# Master bedroom (same listing, same session)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Now stage the master bedroom in the same modern farmhouse style. Maintain consistency with the living room staging. King bed with white linens, wooden nightstands, soft lighting.",
    "image_urls": ["https://example.com/listing-master-bedroom.jpg"],
    "session_id": "full-home-staging"
  }'
```

### 9. Multiple Style Options for Same Room

Generate several staging options for client selection.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Stage this empty living room in 3 different styles: 1) Coastal - light blues, whites, natural textures, beachy vibe 2) Mid-century modern - iconic furniture shapes, warm wood tones, retro accents 3) Scandinavian - light woods, white and gray palette, cozy hygge feel. Generate all three versions.",
    "mode": "max",
    "image_urls": ["https://example.com/empty-living-room.jpg"]
  }'
```

### 10. Declutter and Restage Existing Room

Remove outdated or cluttered furniture and restage with better design.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "This room has old, dated furniture. Remove all existing furniture and restage with modern, neutral furniture that will appeal to more buyers. Keep the room layout logical but update everything - sofa, chairs, tables, decor. Make it look like a model home.",
    "mode": "max",
    "image_urls": ["https://example.com/dated-living-room.jpg"]
  }'
```

## Staging Styles Reference

| Style | Key Elements | Best For |
|-------|--------------|----------|
| Modern | Clean lines, neutral colors, minimal decor | Urban condos, new construction |
| Traditional | Classic furniture, warm woods, elegant fabrics | Established neighborhoods, colonial homes |
| Minimalist | Essential pieces only, lots of space | Small apartments, modern homes |
| Farmhouse | Rustic wood, cozy textiles, vintage accents | Suburban homes, country properties |
| Coastal | Light blues, whites, natural textures | Beach properties, warm climates |
| Mid-Century | Iconic shapes, warm tones, retro accents | 1950s-60s homes, trendy urban areas |
| Scandinavian | Light woods, white palette, hygge comfort | Modern apartments, young buyers |
| Industrial | Exposed elements, metal accents, urban edge | Lofts, converted spaces |

## Mode Selection

| Mode | Best For | Speed | Quality |
|------|----------|-------|---------|
| `max` | Final listing photos, client deliverables | Slower | Highest |
| `eco` | Quick previews, style exploration, bulk processing | Faster | Good |

## Multi-Turn Creative Iteration

Use `session_id` to refine staging results:

```bash
# Initial staging
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Stage this empty living room with modern furniture",
    "image_urls": ["https://example.com/empty-room.jpg"],
    "session_id": "living-room-project"
  }'

# Request adjustments
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "The sofa looks good, but can you add more warmth? Add some throw pillows, a cozy blanket, and warmer lighting",
    "session_id": "living-room-project"
  }'

# Try a different arrangement
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Actually, lets try a different furniture arrangement with the sofa facing the window instead",
    "session_id": "living-room-project"
  }'
```

## Best Practices

### For Real Estate Listings
- **Neutral Appeal**: Use colors and styles that appeal to the broadest audience
- **Show Scale**: Include furniture that helps buyers understand room dimensions
- **Preserve Features**: Ensure architectural details (fireplaces, windows, moldings) remain visible
- **Consistency**: Maintain the same style throughout a property listing

### For Maximum Realism
- **Match Lighting**: Request furniture that matches the existing room lighting
- **Appropriate Scale**: Ensure furniture fits naturally in the space
- **Shadows & Reflections**: High-quality staging includes realistic shadows

### Pro Tips
- Always provide high-resolution source images
- Specify the style upfront to avoid iterations
- Use session_id to generate consistent styling across multiple rooms
- For vacant homes, stage the key selling rooms: living room, master bedroom, kitchen

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | Insufficient balance | Top up at eachlabs.ai |
| Content policy violation | Prohibited content | Adjust prompt |
| Timeout | Complex generation | Set client timeout to minimum 10 minutes |

## Related Skills

- `each-sense` - Core API documentation
- `product-photo-generation` - E-commerce product shots
- `image-edit` - General image editing capabilities
