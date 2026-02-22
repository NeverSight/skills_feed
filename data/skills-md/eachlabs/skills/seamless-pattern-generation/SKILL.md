---
name: seamless-pattern-generation
description: Generate seamless, tileable patterns using each::sense AI. Create repeating patterns for textiles, wallpapers, gift wrap, digital backgrounds, and surface designs that tile perfectly without visible seams.
metadata:
  author: eachlabs
  version: "1.0"
---

# Seamless Pattern Generation

Generate professional-quality seamless, tileable patterns using each::sense. This skill creates repeating patterns that tile perfectly for textiles, wallpapers, packaging, digital backgrounds, and surface design applications.

## Features

- **Floral Patterns**: Botanical designs with flowers, leaves, and organic elements
- **Geometric Patterns**: Mathematical shapes, tessellations, and structured designs
- **Abstract Patterns**: Artistic, non-representational repeating designs
- **Textile/Fabric Patterns**: Fashion-ready prints for clothing and upholstery
- **Wallpaper Patterns**: Interior design patterns for walls and surfaces
- **Gift Wrap Patterns**: Festive and decorative wrapping paper designs
- **Camouflage Patterns**: Military, hunting, and fashion camo designs
- **Texture Patterns**: Marble, stone, wood, and material textures
- **Branded Patterns**: Custom patterns with brand elements and colors

## Quick Start

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a seamless floral pattern with pink roses and green leaves on a cream background, suitable for fabric printing",
    "mode": "max"
  }'
```

## Pattern Types & Use Cases

| Pattern Type | Common Uses | Key Characteristics |
|--------------|-------------|---------------------|
| Floral | Textiles, wallpaper, stationery | Organic, botanical, natural flow |
| Geometric | Modern interiors, tech branding | Precise, mathematical, structured |
| Abstract | Art prints, fashion, packaging | Artistic, unique, expressive |
| Textile | Fashion, upholstery, bedding | Production-ready, repeat-friendly |
| Wallpaper | Interior design, digital backgrounds | Large-scale, room-appropriate |
| Gift Wrap | Packaging, holidays, celebrations | Festive, colorful, decorative |
| Camouflage | Military, hunting, streetwear | Organic shapes, tactical colors |
| Texture | Surface design, 3D materials | Realistic, material-based |

## Use Case Examples

### 1. Floral Seamless Pattern

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a seamless tileable floral pattern featuring delicate watercolor roses, peonies, and eucalyptus leaves. Soft pink, blush, and sage green color palette on an off-white background. Romantic cottage core aesthetic, suitable for fabric printing and textile design.",
    "mode": "max"
  }'
```

### 2. Geometric Pattern

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a seamless geometric pattern with interlocking hexagons and triangles. Modern minimalist style with navy blue, gold, and white colors. Art deco influence, clean lines, perfect for luxury packaging or interior wallpaper. Must tile seamlessly.",
    "mode": "max"
  }'
```

### 3. Abstract Pattern

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a seamless abstract pattern with fluid organic shapes and bold brush strokes. Vibrant coral, teal, and mustard yellow on a dark charcoal background. Contemporary artistic style inspired by mid-century modern art. Tileable for fashion prints.",
    "mode": "max"
  }'
```

### 4. Fabric/Textile Pattern

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a seamless textile pattern for summer dress fabric. Tropical design with palm leaves, monstera, and hibiscus flowers. Fresh green, coral pink, and cream colors on white. Playful yet sophisticated, ready for fabric repeat printing.",
    "mode": "max"
  }'
```

### 5. Wallpaper Pattern

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a seamless wallpaper pattern with elegant chinoiserie style. Featuring birds, flowering branches, and butterflies. Soft blue and white porcelain color scheme with subtle gold accents. Classic, timeless interior design aesthetic. Must tile perfectly for wall application.",
    "mode": "max"
  }'
```

### 6. Gift Wrap Pattern

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a seamless gift wrap pattern for birthday celebrations. Colorful confetti, balloons, streamers, and party hats scattered playfully. Bright rainbow colors including pink, blue, yellow, and green on a light lavender background. Fun and festive, perfect for wrapping paper.",
    "mode": "max"
  }'
```

### 7. Camouflage Pattern

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a seamless woodland camouflage pattern with organic irregular shapes. Traditional military camo colors: olive green, brown, tan, and black. Realistic forest environment camouflage suitable for hunting gear or outdoor apparel. Must tile seamlessly.",
    "mode": "max"
  }'
```

### 8. Marble/Stone Texture Pattern

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a seamless marble texture pattern resembling Italian Calacatta marble. White base with elegant grey and gold veining. Luxurious, high-end aesthetic suitable for interior design, countertops visualization, or luxury packaging. Realistic stone texture that tiles without visible seams.",
    "mode": "max"
  }'
```

### 9. Digital Camo Pattern

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a seamless digital camouflage pattern with pixelated rectangular shapes. Urban style with grey, black, white, and dark blue colors. Modern tactical military aesthetic, similar to MARPAT or UCP patterns. Clean digital pixels, perfect for gaming, streetwear, or tech accessories.",
    "mode": "max"
  }'
```

### 10. Custom Branded Pattern

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a seamless branded pattern for a coffee shop. Feature small coffee cups, coffee beans, croissants, and steam swirls as repeating elements. Warm brown, cream, and copper color palette. Vintage artisanal cafe aesthetic, suitable for packaging, menus, and store decor. Tileable pattern.",
    "mode": "max"
  }'
```

## Best Practices

### Creating Seamless Patterns
- **Specify tileable/seamless**: Always mention that the pattern should tile seamlessly
- **Define scale**: Indicate if you need small repeat, medium, or large-scale patterns
- **Color palette**: Be specific about colors for brand consistency
- **Use case context**: Mention the intended application (fabric, wallpaper, digital)

### Pattern Design Tips
- **Balance**: Ensure even distribution of elements across the pattern
- **Contrast**: Include enough contrast for visual interest
- **Direction**: Specify if pattern should be directional or non-directional
- **Density**: Indicate how dense or sparse you want the pattern elements

### Technical Considerations
- **Resolution**: Higher resolution for print applications
- **Color mode**: Mention if CMYK-friendly colors are needed for print
- **Repeat type**: Specify if you need half-drop, brick, or straight repeat

## Prompt Tips for Pattern Generation

When creating seamless patterns, include these details in your prompt:

1. **Pattern Type**: Floral, geometric, abstract, etc.
2. **Design Elements**: Specific motifs and shapes to include
3. **Color Palette**: Exact colors or color mood
4. **Style/Aesthetic**: Modern, vintage, minimalist, maximalist
5. **Scale**: Small, medium, or large repeat
6. **Use Case**: What the pattern will be used for
7. **Seamless Requirement**: Always mention tileable/seamless

### Example Prompt Structure

```
"Create a seamless [pattern type] pattern featuring [design elements].
[Color palette] on a [background color] background.
[Style/aesthetic] style, suitable for [use case].
Must tile perfectly/seamlessly."
```

## Mode Selection

Ask your users before generating:

**"Do you want fast & cheap, or high quality?"**

| Mode | Best For | Speed | Quality |
|------|----------|-------|---------|
| `max` | Final production patterns, client deliverables | Slower | Highest |
| `eco` | Quick drafts, concept exploration, rapid iteration | Faster | Good |

## Multi-Turn Pattern Iteration

Use `session_id` to iterate on pattern designs:

```bash
# Initial pattern
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a seamless botanical pattern with ferns and monstera leaves, green tones on white",
    "session_id": "pattern-project-001"
  }'

# Iterate based on feedback
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Make the leaves larger and add some small berries in coral color",
    "session_id": "pattern-project-001"
  }'

# Request color variation
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a variation with a dark navy background instead of white",
    "session_id": "pattern-project-001"
  }'
```

## Pattern Collection Generation

Generate coordinating patterns for a collection:

```bash
# Main pattern
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a seamless floral pattern with large roses in dusty pink and sage green, vintage style",
    "session_id": "collection-vintage-florals",
    "mode": "max"
  }'

# Coordinating geometric
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a coordinating seamless stripe pattern using the same dusty pink and sage green colors, simple elegant stripes",
    "session_id": "collection-vintage-florals",
    "mode": "max"
  }'

# Coordinating small-scale
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a small-scale seamless polka dot pattern in the same color palette for a blender pattern",
    "session_id": "collection-vintage-florals",
    "mode": "max"
  }'
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | Insufficient balance | Top up at eachlabs.ai |
| Content policy violation | Prohibited content | Adjust prompt to comply with content policies |
| Timeout | Complex generation | Set client timeout to minimum 10 minutes |

## Related Skills

- `each-sense` - Core API documentation
- `product-photo-generation` - E-commerce product shots
- `texture-generation` - Material textures for 3D
