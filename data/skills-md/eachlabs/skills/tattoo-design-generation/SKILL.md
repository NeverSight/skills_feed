---
name: tattoo-design-generation
description: Generate custom tattoo designs using each::sense AI. Create traditional, Japanese, minimalist, geometric, watercolor, blackwork, realistic, floral, and script tattoo designs optimized for various styles and placements.
metadata:
  author: eachlabs
  version: "1.0"
---

# Tattoo Design Generation

Generate stunning custom tattoo designs using each::sense. This skill creates high-quality tattoo artwork across all major styles, from traditional Americana to intricate Japanese irezumi, minimalist line work to photorealistic portraits.

## Features

- **Traditional/Old School**: Bold lines, limited palette, classic flash designs
- **Japanese Irezumi**: Full-body capable, dragons, koi, waves, cherry blossoms
- **Minimalist Line Art**: Clean single-line designs, delicate and modern
- **Geometric/Mandala**: Sacred geometry, symmetrical patterns, dotwork
- **Watercolor**: Painterly effects, color splashes, artistic blending
- **Blackwork/Tribal**: Heavy black ink, patterns, negative space
- **Realistic Portraits**: Photorealistic faces, animals, detailed shading
- **Floral/Botanical**: Flowers, plants, nature-inspired designs
- **Script/Lettering**: Typography, calligraphy, custom fonts
- **Custom Concepts**: Transform any idea into tattoo-ready artwork

## Quick Start

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a minimalist line art tattoo of a wolf howling at the moon, suitable for forearm placement",
    "mode": "max"
  }'
```

## Tattoo Style Reference

| Style | Characteristics | Common Placements |
|-------|-----------------|-------------------|
| Traditional | Bold outlines, limited colors, iconic imagery | Arms, chest, legs |
| Japanese | Flowing designs, full backgrounds, mythical creatures | Back, sleeves, legs |
| Minimalist | Fine lines, simple shapes, negative space | Wrist, ankle, fingers |
| Geometric | Symmetry, patterns, sacred geometry | Forearm, back, chest |
| Watercolor | Color bleeds, painterly, no outlines | Shoulder, thigh, ribs |
| Blackwork | Solid black, patterns, high contrast | Anywhere, sleeves |
| Realistic | Photographic, detailed shading | Chest, back, arms |
| Floral | Natural elements, flowing, feminine | Shoulder, thigh, back |
| Script | Typography, quotes, names | Ribs, collarbone, wrist |

## Use Case Examples

### 1. Traditional/Old School Tattoo

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a traditional American old school tattoo design of an eagle with a banner. Bold black outlines, classic limited color palette (red, yellow, green, blue). Vintage sailor flash style. Suitable for upper arm placement.",
    "mode": "max"
  }'
```

### 2. Japanese Irezumi Style

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a Japanese irezumi style tattoo design featuring a koi fish swimming upstream through waves with cherry blossoms. Traditional Japanese tattoo aesthetic with flowing water, wind bars, and complementary background elements. Full sleeve design.",
    "mode": "max"
  }'
```

### 3. Minimalist Line Art Tattoo

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a minimalist single continuous line tattoo design of a woman's face in profile. Clean, elegant, modern aesthetic. Fine line work only, no shading. Small size suitable for wrist or ankle placement.",
    "mode": "max"
  }'
```

### 4. Geometric/Mandala Tattoo

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a geometric mandala tattoo design with sacred geometry elements. Incorporate dotwork shading, perfect symmetry, and intricate patterns. Include hexagonal shapes, flower of life elements, and fine line details. Suitable for chest or back center placement.",
    "mode": "max"
  }'
```

### 5. Watercolor Tattoo Style

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a watercolor style tattoo design of a hummingbird with splashes of vibrant color. Painterly effect with color bleeds in purple, blue, and teal. Soft edges blending into skin, artistic paint drips. No heavy outlines. Shoulder blade placement.",
    "mode": "max"
  }'
```

### 6. Blackwork/Tribal Tattoo

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a blackwork tattoo design combining geometric patterns with organic flow. Heavy solid black areas contrasted with negative space. Modern tribal-inspired but not cultural appropriation. Bold, graphic, high contrast. Half-sleeve design from shoulder to elbow.",
    "mode": "max"
  }'
```

### 7. Realistic Portrait Tattoo

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a photorealistic black and grey tattoo design of a lion portrait. Highly detailed fur texture, intense eyes, dramatic lighting with deep shadows. Hyper-realistic style suitable for chest or upper arm. Show fine detail work and smooth gradients.",
    "mode": "max"
  }'
```

### 8. Floral/Botanical Tattoo

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a botanical tattoo design featuring peonies and roses with leaves and delicate stems. Fine line work with subtle dotwork shading. Elegant, feminine, flowing composition. Black and grey with option for soft color accents. Thigh or shoulder placement.",
    "mode": "max"
  }'
```

### 9. Script/Lettering Tattoo

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a script tattoo design with elegant flowing calligraphy lettering. Gothic blackletter style mixed with modern flourishes. Design should flow naturally with the body, suitable for ribcage or collarbone placement. Include decorative elements that complement the text without overwhelming it.",
    "mode": "max"
  }'
```

### 10. Custom Tattoo from Concept

```bash
# Initial concept request
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a custom tattoo design that combines a compass with mountain scenery and forest elements. The compass should be the central focus with mountains and pine trees integrated into the design. Add small geometric accents. Adventure/travel theme. Forearm placement, vertical orientation.",
    "session_id": "custom-tattoo-001",
    "mode": "max"
  }'

# Iterate on the design
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "I like it but can you make the mountains more prominent and add a crescent moon at the top? Keep the compass but make it slightly smaller.",
    "session_id": "custom-tattoo-001"
  }'

# Request variations
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create 2 variations - one with more fine line detail and one with bolder blackwork elements",
    "session_id": "custom-tattoo-001"
  }'
```

## Best Practices

### Design Guidelines
- **Line Weight**: Specify if you want bold, medium, or fine lines
- **Shading Style**: Dotwork, smooth gradient, stippling, or no shading
- **Color vs B&G**: Black and grey ages better; color needs touch-ups
- **Placement**: Always specify body placement for proper proportions
- **Size**: Mention approximate size (small/palm-sized, medium/hand-sized, large/back piece)

### Style-Specific Tips
- **Traditional**: Request "bold black outlines" and "limited palette"
- **Japanese**: Mention "background elements" like wind bars, waves, clouds
- **Minimalist**: Specify "single line" or "continuous line" if desired
- **Geometric**: Request "perfect symmetry" and "clean edges"
- **Watercolor**: Ask for "no outlines" and "color bleeds"
- **Realistic**: Specify "photorealistic" and mention lighting direction

### Prompt Tips for Tattoo Designs

When creating tattoo designs, include these details in your prompt:

1. **Style**: Clearly specify the tattoo style
2. **Subject**: What is the main element or imagery
3. **Composition**: How elements should be arranged
4. **Line Work**: Bold, fine, or mixed line weights
5. **Shading**: Type of shading technique desired
6. **Color**: Full color, limited palette, or black and grey
7. **Placement**: Body location for proper sizing/orientation
8. **Size**: Approximate size of the final tattoo

### Example Prompt Structure

```
"Create a [style] tattoo design of [subject].
[Composition details] with [line work] lines.
[Shading style] shading, [color preference].
Suitable for [placement] placement, [size] size.
[Additional style elements or references]"
```

## Mode Selection

Ask your users before generating:

**"Do you want fast drafts or highest quality?"**

| Mode | Best For | Speed | Quality |
|------|----------|-------|---------|
| `max` | Final designs, client presentations, detailed work | Slower | Highest |
| `eco` | Quick concepts, style exploration, rough drafts | Faster | Good |

## Multi-Turn Design Iteration

Use `session_id` to iterate on tattoo designs:

```bash
# Initial design
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a neo-traditional snake and dagger tattoo design",
    "session_id": "snake-dagger-design"
  }'

# Add elements
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Add roses around the dagger and make the snake more menacing with detailed scales",
    "session_id": "snake-dagger-design"
  }'

# Style adjustment
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Convert this to black and grey only, with heavy contrast",
    "session_id": "snake-dagger-design"
  }'
```

## Placement-Specific Designs

Generate designs optimized for specific body placements:

```bash
# Sleeve design (wrapping)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a full sleeve tattoo design with Japanese waves and koi fish. Design should flow around the arm and connect seamlessly. Include filler elements for gaps.",
    "mode": "max"
  }'

# Small wrist design
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a tiny minimalist tattoo design of a paper airplane with a dotted flight path. Very small scale suitable for inner wrist. Fine lines that will hold up at small size.",
    "mode": "max"
  }'
```

## Reference Image Input

Use reference images for inspiration or style matching:

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a tattoo design in a similar style to this reference but featuring a phoenix instead. Match the line weight and shading technique.",
    "mode": "max",
    "image_urls": ["https://example.com/tattoo-reference.jpg"]
  }'
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | Insufficient balance | Top up at eachlabs.ai |
| Content policy violation | Prohibited content | Adjust prompt - avoid offensive imagery |
| Timeout | Complex generation | Set client timeout to minimum 10 minutes |

## Related Skills

- `each-sense` - Core API documentation
- `image-generation` - General image creation
- `image-edit` - Edit and refine generated designs
