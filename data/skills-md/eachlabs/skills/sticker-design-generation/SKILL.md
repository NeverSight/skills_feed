---
name: sticker-design-generation
description: Generate custom sticker designs using each::sense AI. Create die-cut stickers, vinyl decals, kawaii designs, brand logos, emoji packs, laptop stickers, bumper stickers, planner stickers, holographic effects, and complete sticker sheets.
metadata:
  author: eachlabs
  version: "1.0"
---

# Sticker Design Generation

Generate professional sticker designs using each::sense. This skill creates print-ready sticker artwork for various applications including die-cut stickers, vinyl decals, merchandise, branding, and digital sticker packs.

## Features

- **Die-Cut Stickers**: Custom shapes with clean edges for cutting
- **Vinyl Stickers**: Weather-resistant designs for outdoor use
- **Kawaii/Cute Stickers**: Japanese-inspired adorable characters and designs
- **Brand Logo Stickers**: Professional logo stickers for merchandise and marketing
- **Emoji-Style Packs**: Expressive character sets for messaging apps
- **Laptop Stickers**: Tech-aesthetic designs for device customization
- **Bumper Stickers**: Bold, readable designs for vehicles
- **Planner/Journal Stickers**: Decorative elements for planning and scrapbooking
- **Holographic Effects**: Iridescent and prismatic visual styles
- **Sticker Sheets**: Organized layouts with multiple designs

## Quick Start

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a die-cut sticker design of a cute cat astronaut floating in space with stars around it, white background for easy cutting",
    "mode": "max"
  }'
```

## Sticker Types & Specifications

| Sticker Type | Typical Size | Background | Use Case |
|--------------|--------------|------------|----------|
| Die-Cut | 2-4 inches | White/Transparent | Water bottles, laptops, notebooks |
| Vinyl | 3-5 inches | Solid colors | Outdoor, vehicles, windows |
| Kawaii | 1-3 inches | White/Pastel | Planners, journals, gifts |
| Logo | 2-4 inches | Brand colors | Marketing, merchandise |
| Emoji Pack | 1-2 inches | Transparent | Digital, messaging apps |
| Laptop | 3-6 inches | Various | Device customization |
| Bumper | 3x10 inches | Solid | Vehicles, outdoor |
| Planner | 0.5-2 inches | White/Clear | Bullet journals, calendars |
| Holographic | 2-4 inches | Iridescent effect | Premium merchandise |
| Sticker Sheet | 4x6 or 8.5x11 | White | Retail, bundles |

## Use Case Examples

### 1. Die-Cut Sticker Design

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a die-cut sticker design of a retro cassette tape with vibrant 80s colors (pink, cyan, purple). The design should have clean edges suitable for die-cutting, white background, vintage aesthetic with slight wear texture.",
    "mode": "max"
  }'
```

### 2. Vinyl Sticker Design

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Design a weatherproof vinyl sticker for outdoor use. Mountain landscape with a sunset, bold colors that stand out, simple shapes that read well from a distance. Include a small border for durability. Style: flat illustration, vector-like clean lines.",
    "mode": "max"
  }'
```

### 3. Kawaii/Cute Sticker

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a kawaii sticker design of a blushing strawberry with cute anime-style eyes, tiny hands, and sparkles around it. Pastel pink colors, white background, Japanese cute aesthetic. Add small hearts and stars as decorative elements.",
    "mode": "max"
  }'
```

### 4. Brand Logo Sticker

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Design a professional brand logo sticker for a coffee shop called 'Brew & Bean'. Circular badge design with a coffee cup icon, modern minimalist style, black and gold colors on white background. Include the brand name in a clean sans-serif font. Print-ready with bleed area.",
    "mode": "max"
  }'
```

### 5. Emoji-Style Sticker Pack

```bash
# First emoji in the pack
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create the first sticker in an emoji-style pack featuring a round yellow character. This one shows a happy laughing expression with closed eyes and open mouth. Bold black outlines, flat colors, transparent background. Style similar to popular messaging app stickers.",
    "session_id": "emoji-pack-001"
  }'

# Second emoji (same session for consistency)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create the second sticker in the pack with the same character, but showing a surprised/shocked expression with wide eyes and small O-shaped mouth. Maintain the same style and colors as the first one.",
    "session_id": "emoji-pack-001"
  }'

# Third emoji
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create the third sticker showing the character with heart eyes and a loving expression. Keep consistent with the previous designs.",
    "session_id": "emoji-pack-001"
  }'
```

### 6. Laptop Sticker Design

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Design a tech-themed laptop sticker featuring a cyberpunk-style geometric fox head with neon accents (electric blue and hot pink). Modern, edgy aesthetic suitable for developers and gamers. Clean die-cut shape, approximately 3 inches. Black background with glowing effects.",
    "mode": "max"
  }'
```

### 7. Bumper Sticker Design

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a bumper sticker design, rectangular format (approximately 3x10 inch ratio). Bold text saying 'ADVENTURE AWAITS' with a mountain and sun icon. High contrast colors (navy blue background, white and yellow graphics) for visibility. Simple, readable from a distance, weather-resistant design considerations.",
    "mode": "max"
  }'
```

### 8. Planner/Journal Stickers

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Design a set of planner stickers for productivity and journaling. Include: a 'To Do' header banner, small checkmark icons, coffee cup doodle, stack of books, tiny plant illustration, and motivational quote bubble saying 'You got this!'. Cohesive pastel color palette (mint, peach, lavender), hand-drawn illustration style, white background.",
    "mode": "max"
  }'
```

### 9. Holographic Effect Sticker

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a holographic-style sticker design of a crystal cluster. Iridescent rainbow effect with prismatic light reflections, shifting colors from pink to blue to green. Add sparkle elements and light flares. The design should simulate the look of a holographic/foil sticker material. White background for die-cutting.",
    "mode": "max"
  }'
```

### 10. Sticker Sheet Layout

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Design a complete sticker sheet (4x6 inch format) with a cohesive 'Ocean Life' theme. Include: 2 large stickers (jellyfish and sea turtle), 4 medium stickers (seashells, starfish, coral, seahorse), and 6 small decorative elements (bubbles, waves, anchors). Watercolor illustration style, soft blue and coral color palette. Arrange neatly on white background with proper spacing for cutting.",
    "mode": "max"
  }'
```

## Best Practices

### Design Guidelines
- **Clean Edges**: Ensure designs have clear boundaries for die-cutting
- **White/Transparent Background**: Makes production easier and cleaner
- **Bold Colors**: Use vibrant, saturated colors that print well
- **Simple Shapes**: Complex details may be lost at small sizes
- **Bleed Area**: Include extra margin for cutting tolerance

### Print Considerations
- **Resolution**: Request high-resolution output for print quality
- **Color Mode**: Consider CMYK-friendly colors for printing
- **Size Specification**: Mention target size in your prompt
- **Material Type**: Specify if designing for matte, glossy, or holographic materials

### Style Tips
- **Consistency**: Use session_id when creating sticker packs for visual consistency
- **Contrast**: Ensure good contrast for readability
- **Scalability**: Designs should look good at various sizes
- **Theme Cohesion**: Maintain consistent style across related stickers

## Prompt Tips for Sticker Designs

When creating sticker designs, include these details in your prompt:

1. **Sticker Type**: Die-cut, vinyl, holographic, etc.
2. **Subject/Theme**: What the sticker depicts
3. **Style**: Kawaii, minimalist, retro, hand-drawn, vector, etc.
4. **Colors**: Specific palette or color scheme
5. **Size/Format**: Target dimensions or aspect ratio
6. **Background**: White, transparent, colored, or gradient
7. **Special Effects**: Holographic, metallic, glow, etc.
8. **Use Case**: Where the sticker will be applied

### Example Prompt Structure

```
"Create a [sticker type] sticker design of [subject].
Style: [artistic style].
Colors: [color palette].
Size: [dimensions/format].
Background: [background type].
Additional details: [special effects, text, decorative elements]."
```

## Mode Selection

Ask your users before generating:

**"Do you want fast & cheap, or high quality?"**

| Mode | Best For | Speed | Quality |
|------|----------|-------|---------|
| `max` | Final print-ready designs, client deliverables | Slower | Highest |
| `eco` | Quick concepts, draft iterations, bulk exploration | Faster | Good |

## Multi-Turn Creative Iteration

Use `session_id` to iterate on sticker designs:

```bash
# Initial design concept
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a die-cut sticker of a happy cactus in a pot, kawaii style",
    "session_id": "cactus-sticker-project"
  }'

# Refine based on feedback
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Make the cactus blush more, add small flower on top, and include tiny sparkles around it",
    "session_id": "cactus-sticker-project"
  }'

# Create variations
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create 3 more variations with different expressions: sleepy, excited, and winking",
    "session_id": "cactus-sticker-project"
  }'
```

## Batch Generation for Sticker Packs

Generate multiple themed stickers efficiently:

```bash
# Sticker 1 - Main character
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a cute raccoon character sticker, sitting pose, holding a cookie, kawaii style with pastel colors",
    "mode": "eco",
    "session_id": "raccoon-pack"
  }'

# Sticker 2 - Different pose
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Same raccoon character but sleeping curled up, with a tiny snot bubble",
    "mode": "eco",
    "session_id": "raccoon-pack"
  }'

# Sticker 3 - Action pose
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Same raccoon character waving hello with sparkles, cheerful expression",
    "mode": "eco",
    "session_id": "raccoon-pack"
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
- `product-photo-generation` - Product photography for merchandise
- `brand-logo-generation` - Logo design for sticker branding
- `character-design` - Character creation for sticker packs
