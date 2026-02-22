---
name: interior-design-visualization
description: Visualize interior design transformations using each::sense AI. Redesign rooms, change styles, update color schemes, and preview renovations from photos of your existing spaces.
metadata:
  author: eachlabs
  version: "1.0"
---

# Interior Design Visualization

Transform and visualize interior spaces using each::sense. This skill takes photos of existing rooms and generates redesigned versions with different styles, furniture, colors, and layouts.

## Features

- **Room Redesign**: Transform existing rooms into completely new designs
- **Style Transformation**: Apply modern, minimalist, bohemian, industrial, and other styles
- **Furniture Visualization**: See how new furniture would look in your space
- **Color Scheme Changes**: Preview walls, accents, and decor in different colors
- **Kitchen Remodels**: Visualize cabinet, countertop, and appliance updates
- **Bathroom Updates**: Preview tile, vanity, and fixture changes
- **Office Design**: Transform workspaces for productivity and aesthetics
- **Before/After Comparison**: Generate side-by-side visualizations

## Quick Start

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Redesign this living room in a modern minimalist style with neutral colors and clean lines",
    "image_urls": ["https://example.com/my-living-room.jpg"],
    "mode": "max"
  }'
```

## Interior Design Styles

| Style | Characteristics | Best For |
|-------|-----------------|----------|
| Modern | Clean lines, neutral colors, minimal decor | Living rooms, offices |
| Minimalist | Sparse furniture, white/light colors, open space | Any room |
| Scandinavian | Light wood, white walls, cozy textiles | Bedrooms, living rooms |
| Industrial | Exposed brick, metal accents, raw materials | Lofts, kitchens |
| Bohemian | Rich colors, patterns, eclectic decor | Bedrooms, living rooms |
| Mid-Century Modern | Retro furniture, warm woods, bold colors | Living rooms, offices |
| Farmhouse | Rustic wood, neutral colors, vintage accents | Kitchens, dining rooms |
| Contemporary | Current trends, mixed materials, sophisticated | Any room |
| Coastal | Light blues, whites, natural textures | Bedrooms, bathrooms |
| Traditional | Classic furniture, rich colors, ornate details | Formal spaces |

## Use Case Examples

### 1. Room Redesign from Photo

Transform an existing room with a complete redesign while maintaining the room's structure.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Completely redesign this room. Keep the same layout but update all furniture, decor, and colors. Make it feel more luxurious and sophisticated with a contemporary style. Include a statement light fixture and add some greenery.",
    "image_urls": ["https://example.com/current-room.jpg"],
    "mode": "max"
  }'
```

### 2. Style Transformation (Modern to Minimalist)

Convert a room from one design style to another.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Transform this cluttered traditional living room into a minimalist Japanese-inspired space. Remove excess furniture, use a neutral color palette with whites and light wood tones, add a low platform sofa, and incorporate zen elements like a simple indoor plant and natural light.",
    "image_urls": ["https://example.com/traditional-room.jpg"],
    "mode": "max"
  }'
```

### 3. Furniture Placement Visualization

See how specific furniture pieces would look in your space.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Add furniture to this empty living room: place a large L-shaped sectional sofa in gray fabric facing the window, a round marble coffee table in the center, two accent armchairs in terracotta velvet, a media console against the wall, and a large area rug underneath. Keep the existing flooring and wall color.",
    "image_urls": ["https://example.com/empty-living-room.jpg"],
    "mode": "max"
  }'
```

### 4. Color Scheme Change

Preview your room with different wall colors and accent colors.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Change the color scheme of this room. Paint the walls in a deep forest green, update the curtains to cream linen, add gold accent pieces, and change the throw pillows to mustard yellow and cream. Keep all existing furniture but change the soft furnishings.",
    "image_urls": ["https://example.com/beige-room.jpg"],
    "mode": "max"
  }'
```

### 5. Kitchen Remodel Visualization

Preview kitchen renovations including cabinets, countertops, and appliances.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Remodel this dated kitchen into a modern farmhouse style. Replace the cabinets with white shaker-style cabinets, add a large kitchen island with a butcher block top, install stainless steel appliances, add subway tile backsplash, change countertops to white quartz, and include open shelving on one wall. Add pendant lights over the island.",
    "image_urls": ["https://example.com/old-kitchen.jpg"],
    "mode": "max"
  }'
```

### 6. Bathroom Design Update

Transform bathroom aesthetics with new fixtures and finishes.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Transform this outdated bathroom into a spa-like retreat. Replace the vanity with a floating double vanity in walnut wood, add a frameless glass shower enclosure, install large format white marble-look tiles on the walls, add matte black fixtures and hardware, include a freestanding soaking tub if space allows, and add warm LED lighting behind the mirror.",
    "image_urls": ["https://example.com/bathroom-before.jpg"],
    "mode": "max"
  }'
```

### 7. Office Space Design

Create productive and stylish home office or commercial workspace designs.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Design this spare bedroom as a professional home office. Add a large L-shaped desk in walnut, an ergonomic mesh office chair, built-in bookshelves on one wall, proper task lighting with a desk lamp and overhead light, some indoor plants for freshness, and a comfortable reading nook by the window. Keep it professional but warm.",
    "image_urls": ["https://example.com/spare-bedroom.jpg"],
    "mode": "max"
  }'
```

### 8. Bedroom Makeover

Transform bedrooms with new furniture, textiles, and ambiance.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Give this master bedroom a luxury hotel makeover. Add an upholstered king bed with a tall tufted headboard in gray velvet, matching nightstands with elegant table lamps, a bench at the foot of the bed, floor-to-ceiling curtains in a soft white, layered bedding in white and taupe, and a plush area rug. Create a serene and sophisticated atmosphere.",
    "image_urls": ["https://example.com/bedroom-current.jpg"],
    "mode": "max"
  }'
```

### 9. Living Room Style Options (Multi-Turn)

Generate multiple style options for the same room using session continuity.

```bash
# First option - Modern style
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Redesign this living room in a modern contemporary style with clean lines, neutral colors, and sophisticated furniture. Include a sectional sofa, modern coffee table, and contemporary art.",
    "image_urls": ["https://example.com/living-room.jpg"],
    "session_id": "living-room-options-001",
    "mode": "max"
  }'

# Second option - Bohemian style (same session)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Now redesign the same living room in a bohemian style. Use rich colors, layered textiles, eclectic furniture, lots of plants, and global-inspired decor. Make it feel cozy and collected.",
    "session_id": "living-room-options-001",
    "mode": "max"
  }'

# Third option - Scandinavian style (same session)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a third option with Scandinavian style. Light wood floors, white walls, minimal furniture in light colors, cozy textiles like sheepskin throws, and plenty of natural light. Keep it simple and hygge.",
    "session_id": "living-room-options-001",
    "mode": "max"
  }'
```

### 10. Before/After Comparison

Generate a side-by-side visualization showing the transformation.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a dramatic before and after comparison. Take this dated 1990s living room and transform it into a modern 2024 design. Show both versions side by side - the original on the left and the redesigned version on the right. The new design should feature contemporary furniture, updated lighting, modern color palette, and current design trends.",
    "image_urls": ["https://example.com/dated-room.jpg"],
    "mode": "max"
  }'
```

## Best Practices

### Photo Requirements
- **Good lighting**: Use well-lit photos for best results
- **Clear angles**: Wide-angle shots showing the full room work best
- **Minimal obstructions**: Remove temporary items like laundry or personal effects
- **Multiple angles**: For complex projects, provide multiple views

### Prompt Tips
- **Be specific**: Mention exact styles, colors, and materials
- **Reference the space**: Describe what to keep vs. change
- **Include details**: Mention lighting, textures, and accessories
- **Set the mood**: Describe the atmosphere you want (cozy, luxurious, bright)

### Example Prompt Structure

```
"Transform this [room type] into a [style] design.
[Specific changes for major elements like walls, floors, furniture]
[Color palette preferences]
[Lighting requirements]
[Accessories and decor]
[Overall mood/atmosphere]"
```

## Mode Selection

Ask your users before generating:

**"Do you want fast & cheap, or high quality?"**

| Mode | Best For | Speed | Quality |
|------|----------|-------|---------|
| `max` | Final design presentations, client proposals | Slower | Highest |
| `eco` | Quick concept exploration, initial brainstorming | Faster | Good |

## Multi-Turn Design Refinement

Use `session_id` to iterate on designs:

```bash
# Initial design
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Redesign this bedroom in a modern style with neutral colors",
    "image_urls": ["https://example.com/bedroom.jpg"],
    "session_id": "bedroom-project-001",
    "mode": "max"
  }'

# Refine based on feedback
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "I like it but make the headboard larger and add more warm wood tones. Also add some plants.",
    "session_id": "bedroom-project-001",
    "mode": "max"
  }'

# Final adjustments
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Perfect! Now add some artwork above the bed and change the throw pillows to a dusty rose color.",
    "session_id": "bedroom-project-001",
    "mode": "max"
  }'
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | Insufficient balance | Top up at eachlabs.ai |
| Content policy violation | Prohibited content | Adjust prompt to comply with content policies |
| Timeout | Complex generation | Set client timeout to minimum 10 minutes |
| Image not accessible | Invalid or private URL | Use publicly accessible image URLs |

## Related Skills

- `each-sense` - Core API documentation
- `product-photo-generation` - E-commerce product shots
- `meta-ad-creative-generation` - Social media ad creatives
