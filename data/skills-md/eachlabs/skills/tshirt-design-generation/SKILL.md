---
name: tshirt-design-generation
description: Generate print-ready t-shirt and apparel designs using each::sense AI. Create graphic tees, typography designs, vintage styles, illustrations, and more for custom apparel printing.
metadata:
  author: eachlabs
  version: "1.0"
---

# T-Shirt Design Generation

Generate professional, print-ready t-shirt and apparel designs using each::sense. This skill creates high-quality graphics optimized for screen printing, DTG (direct-to-garment), sublimation, and heat transfer printing methods.

## Features

- **Graphic Designs**: Bold illustrations and artwork for statement tees
- **Typography**: Text-based designs with creative lettering and fonts
- **Vintage/Retro**: Distressed, worn-look designs with classic aesthetics
- **Minimalist**: Clean, simple designs with maximum impact
- **Illustrations**: Hand-drawn style artwork and characters
- **Band/Music**: Concert merch style designs
- **Sports Team**: Athletic apparel graphics and logos
- **Humor/Meme**: Funny designs and pop culture references
- **Abstract Art**: Artistic patterns and contemporary designs
- **Print-Ready**: Transparent background exports for production

## Quick Start

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a graphic t-shirt design featuring a roaring tiger with geometric patterns, bold colors, suitable for screen printing",
    "mode": "max"
  }'
```

## Design Specifications

| Print Method | Recommended Format | Colors | Notes |
|--------------|-------------------|--------|-------|
| Screen Print | PNG with transparency | Limited (1-6 colors) | Spot colors, high contrast |
| DTG | PNG with transparency | Unlimited | Full color, photorealistic ok |
| Sublimation | PNG/JPG | Unlimited | All-over prints, vibrant colors |
| Heat Transfer | PNG with transparency | Unlimited | Works on dark/light garments |
| Vinyl Cut | Vector-style PNG | 1-3 colors | Simple shapes, no gradients |

## Use Case Examples

### 1. Graphic T-Shirt Design

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a graphic t-shirt design of a wolf howling at the moon. Use a bold, illustrative style with deep blues and purples. The design should be centered and work well on both black and white shirts. Include some geometric elements and stars around the wolf.",
    "mode": "max"
  }'
```

### 2. Typography/Text-Based Design

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a typography t-shirt design with the phrase \"Stay Wild\" in a bold, hand-lettered style. Add decorative flourishes and small nature elements like mountains and pine trees integrated into the lettering. Black ink style, suitable for light colored shirts.",
    "mode": "max"
  }'
```

### 3. Vintage/Retro Style Design

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a vintage retro t-shirt design for a fictional surf shop called \"Pacific Wave Co. Est. 1975\". Use faded colors, distressed textures, and 70s typography. Include a sunset, palm trees, and surfboard. Circular badge design with worn, screen-printed look.",
    "mode": "max"
  }'
```

### 4. Minimalist Design

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a minimalist t-shirt design featuring a simple line art mountain range with a small sun. Single continuous line style, black only. Clean, modern, Scandinavian aesthetic. Small chest placement size, very simple and elegant.",
    "mode": "max"
  }'
```

### 5. Illustration-Based Design

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an illustrated t-shirt design of a Japanese koi fish swimming through waves. Traditional Japanese art style with modern twist. Use orange, red, white, and blue colors. Include cherry blossom petals and water splashes. Vertical composition for front of shirt.",
    "mode": "max"
  }'
```

### 6. Band/Music T-Shirt Design

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a rock band t-shirt design for a fictional band called \"Electric Storm\". Heavy metal aesthetic with lightning bolts, skulls, and electric guitar. Gothic typography for the band name. Black and white with red accents. Tour dates style layout on the back.",
    "mode": "max"
  }'
```

### 7. Sports Team Design

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a sports team t-shirt design for \"Thunder Hawks Basketball\". Athletic style with an aggressive hawk mascot holding a basketball. Team colors navy blue and gold. Include \"2024 Champions\" text. Bold, dynamic composition with motion lines.",
    "mode": "max"
  }'
```

### 8. Funny/Meme T-Shirt Design

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a funny t-shirt design featuring a lazy sloth hanging from a branch with text \"Running Late Is My Cardio\". Cute cartoon style, pastel colors. The sloth should have a sleepy, unbothered expression. Light-hearted and humorous vibe.",
    "mode": "max"
  }'
```

### 9. Abstract Art Design

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an abstract art t-shirt design with fluid shapes, bold brushstrokes, and vibrant colors. Contemporary art gallery style. Mix of geometric and organic forms. Colors: electric blue, hot pink, orange, and black. Large front print composition.",
    "mode": "max"
  }'
```

### 10. Print-Ready Design with Transparent Background

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a print-ready t-shirt design with transparent background. Design a detailed skull with flowers growing from it (memento mori style). High contrast, clean edges suitable for screen printing. Output as PNG with transparency. Colors: limited to 4 spot colors - black, red, green, cream.",
    "mode": "max"
  }'
```

## Best Practices

### Design Guidelines
- **Placement**: Consider standard print areas (front center, left chest, back)
- **Resolution**: Request high resolution for print quality (300 DPI equivalent)
- **Color Count**: Specify limited colors for screen printing cost efficiency
- **Contrast**: Ensure design works on intended shirt colors
- **Edges**: Clean, defined edges for easier separation

### Print Considerations
- **Bleed Area**: Leave margin around design edges
- **Underbase**: For dark shirts, mention if white underbase is needed
- **Halftones**: Specify if gradients should use halftone patterns
- **Registration**: Simple designs with fewer colors = easier registration

### File Output Tips
- Request transparent PNG for versatility
- Specify if you need vector-style output
- Mention target print size (e.g., "12 inches wide for standard front print")

## Mode Selection

**"Do you want fast drafts or production-quality designs?"**

| Mode | Best For | Speed | Quality |
|------|----------|-------|---------|
| `max` | Final print-ready designs, client presentations | Slower | Highest |
| `eco` | Quick concepts, design exploration, mockup iterations | Faster | Good |

## Multi-Turn Design Iteration

Use `session_id` to refine designs through conversation:

```bash
# Initial concept
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a vintage motorcycle t-shirt design with a classic chopper",
    "session_id": "moto-design-001"
  }'

# Refine the design
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Add flames coming from the exhaust and put \"Born to Ride\" text in a banner below",
    "session_id": "moto-design-001"
  }'

# Request color variation
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a version with only black and gold colors for a premium look",
    "session_id": "moto-design-001"
  }'
```

## Design Collections (Batch Generation)

Generate multiple designs for a collection:

```bash
# Design 1 - Mountain theme
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an outdoor adventure t-shirt design with mountains and \"Explore More\" text. Earth tones, vintage camping aesthetic.",
    "session_id": "outdoor-collection",
    "mode": "eco"
  }'

# Design 2 - Forest theme (same session for style consistency)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a matching design for the collection with forest and pine trees theme. Same style as the mountain design. Text: \"Get Lost\"",
    "session_id": "outdoor-collection",
    "mode": "eco"
  }'

# Design 3 - Campfire theme
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Third design in the collection - campfire scene with stars. Same vintage outdoor style. Text: \"Under the Stars\"",
    "session_id": "outdoor-collection",
    "mode": "eco"
  }'
```

## Prompt Tips for T-Shirt Designs

Include these details for best results:

1. **Style**: Illustrative, minimalist, vintage, cartoon, realistic, etc.
2. **Subject**: What the main visual element is
3. **Colors**: Specific colors or color scheme
4. **Target Garment**: Black tee, white tee, or both
5. **Print Method**: Screen print, DTG, etc.
6. **Placement**: Front, back, left chest, all-over
7. **Text**: Any typography to include
8. **Mood**: Edgy, fun, professional, artistic, etc.

### Example Prompt Structure

```
"Create a [style] t-shirt design featuring [subject].
Use [colors] color scheme. Design should work on [garment color] shirts.
Include text: \"[text]\". [Additional requirements].
Output as [format] for [print method]."
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | Insufficient balance | Top up at eachlabs.ai |
| Content policy violation | Prohibited content | Adjust prompt to comply with content policies |
| Timeout | Complex generation | Set client timeout to minimum 10 minutes |

## Related Skills

- `each-sense` - Core API documentation
- `product-photo-generation` - Product mockups and photos
- `image-generation` - General image generation
