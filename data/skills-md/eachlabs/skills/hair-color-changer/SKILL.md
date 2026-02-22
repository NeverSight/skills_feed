---
name: hair-color-changer
description: Change hair color in photos using each::sense AI. Transform hair to any color including natural shades, fantasy colors, ombre effects, highlights, and more.
metadata:
  author: eachlabs
  version: "1.0"
---

# Hair Color Changer

Transform hair color in photos using each::sense. This skill enables realistic hair color changes from subtle natural variations to bold fantasy colors, with support for complex effects like ombre, highlights, and multi-tone styling.

## Features

- **Natural Colors**: Blonde, brunette, black, red, auburn
- **Fantasy Colors**: Purple, blue, pink, green, and more
- **Ombre & Gradient**: Smooth color transitions from roots to tips
- **Highlights & Lowlights**: Multi-dimensional color effects
- **Gray & Silver**: Elegant silver, platinum, and gray tones
- **Color Correction**: Fix or enhance existing hair color
- **Multi-Turn Sessions**: Iterate on results and try different colors

## Quick Start

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Change the hair color to platinum blonde, keep it looking natural and shiny",
    "image_urls": ["https://example.com/portrait.jpg"],
    "mode": "max"
  }'
```

## Use Case Examples

### 1. Change Hair to Blonde

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Change the hair to a warm honey blonde color. Keep the hair texture and shine natural, maintain realistic highlights throughout.",
    "image_urls": ["https://example.com/original-photo.jpg"],
    "mode": "max"
  }'
```

### 2. Change Hair to Brunette

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Transform the hair to a rich chocolate brown color. Add subtle warm undertones and natural-looking dimension to the brunette shade.",
    "image_urls": ["https://example.com/portrait.jpg"],
    "mode": "max"
  }'
```

### 3. Change Hair to Red/Auburn

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Change the hair color to a vibrant auburn red. Make it look like natural ginger hair with copper highlights that catch the light.",
    "image_urls": ["https://example.com/model-photo.jpg"],
    "mode": "max"
  }'
```

### 4. Fantasy Colors (Purple, Blue, Pink)

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Transform the hair to a vivid galaxy purple color. Make it look like professionally dyed hair with deep violet tones and subtle blue undertones. Keep the hair healthy and shiny looking.",
    "image_urls": ["https://example.com/portrait.jpg"],
    "mode": "max"
  }'
```

```bash
# Electric blue hair
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Change the hair to electric blue color, like a bold fashion statement. Mix of deep blue and bright cyan tones throughout.",
    "image_urls": ["https://example.com/photo.jpg"],
    "mode": "max"
  }'
```

```bash
# Pastel pink hair
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Transform the hair to a soft pastel pink color. Think rose gold meets cotton candy - delicate, feminine, and Instagram-worthy.",
    "image_urls": ["https://example.com/headshot.jpg"],
    "mode": "max"
  }'
```

### 5. Ombre/Gradient Effect

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an ombre hair effect - dark brown roots transitioning smoothly to caramel blonde at the ends. Make the gradient look natural and well-blended like salon balayage.",
    "image_urls": ["https://example.com/full-portrait.jpg"],
    "mode": "max"
  }'
```

```bash
# Fantasy ombre
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a fantasy ombre effect with dark purple roots fading into bright pink, then to peachy coral at the tips. Smooth gradient transitions like a sunset.",
    "image_urls": ["https://example.com/model.jpg"],
    "mode": "max"
  }'
```

### 6. Highlights and Lowlights

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Add dimensional highlights and lowlights to the hair. Keep the base color but add face-framing blonde highlights and subtle caramel lowlights throughout for depth and dimension.",
    "image_urls": ["https://example.com/brunette-photo.jpg"],
    "mode": "max"
  }'
```

```bash
# Babylights effect
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Add subtle babylights throughout the hair - very fine, delicate highlights like sun-kissed natural lightening. Keep it soft and natural looking.",
    "image_urls": ["https://example.com/portrait.jpg"],
    "mode": "max"
  }'
```

### 7. Gray/Silver Hair

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Transform the hair to an elegant silver gray color. Make it look like intentional fashion-forward silver hair, not aging gray - metallic, shiny, and well-maintained.",
    "image_urls": ["https://example.com/fashion-photo.jpg"],
    "mode": "max"
  }'
```

```bash
# Platinum silver
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Change hair to platinum silver with icy undertones. Think high fashion editorial silver - cool-toned, luminous, and striking.",
    "image_urls": ["https://example.com/model-headshot.jpg"],
    "mode": "max"
  }'
```

### 8. Natural Color Variations

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Adjust the hair color to be 2 shades darker, turning it from medium brown to a deep espresso brown. Keep all the natural texture and shine.",
    "image_urls": ["https://example.com/natural-photo.jpg"],
    "mode": "max"
  }'
```

```bash
# Warm up cool tones
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Add warm golden undertones to the existing hair color. Keep the same overall shade but remove any ashy tones and make it warmer and more vibrant.",
    "image_urls": ["https://example.com/portrait.jpg"],
    "mode": "eco"
  }'
```

### 9. Multiple Color Options from Same Photo

Use `session_id` to try different colors on the same photo:

```bash
# First option - Blonde
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Change my hair to platinum blonde. I want to see how I would look with this color.",
    "image_urls": ["https://example.com/my-photo.jpg"],
    "session_id": "hair-color-tryout-001",
    "mode": "eco"
  }'

# Second option - Red (same session)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Now show me the same photo but with fiery red hair instead.",
    "session_id": "hair-color-tryout-001",
    "mode": "eco"
  }'

# Third option - Black (same session)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "And one more variation with jet black hair please.",
    "session_id": "hair-color-tryout-001",
    "mode": "eco"
  }'
```

### 10. Before/After Comparison

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Change the hair to rose gold color, then create a side-by-side before and after comparison showing the original on the left and the new color on the right.",
    "image_urls": ["https://example.com/original-portrait.jpg"],
    "mode": "max"
  }'
```

```bash
# Iterative refinement for comparison
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Transform the hair to strawberry blonde.",
    "image_urls": ["https://example.com/client-photo.jpg"],
    "session_id": "client-consultation-001",
    "mode": "max"
  }'

# Follow-up to adjust
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Make the strawberry blonde a bit more pink and less orange. Also make it slightly lighter overall.",
    "session_id": "client-consultation-001",
    "mode": "max"
  }'
```

## Best Practices

### Getting Realistic Results

- **Good Lighting**: Use photos with clear, even lighting on the hair
- **Hair Visibility**: Ensure the hair is clearly visible and not obscured
- **Face Forward**: Front-facing or 3/4 angle photos work best
- **High Resolution**: Higher quality source images yield better results

### Prompt Tips

1. **Be Specific**: Describe the exact shade you want (e.g., "warm honey blonde" vs just "blonde")
2. **Reference Tones**: Mention undertones (warm, cool, neutral, ashy, golden)
3. **Texture Preservation**: Request to maintain natural texture and shine
4. **Realistic Expectations**: Fantasy colors may look more vibrant on lighter base colors

### Example Prompt Structure

```
"Change the hair to [specific color with undertones].
[Additional details about dimension, highlights, or effects].
Keep the hair looking [natural/healthy/shiny/textured]."
```

## Mode Selection

**"Do you want fast results or highest quality?"**

| Mode | Best For | Speed | Quality |
|------|----------|-------|---------|
| `max` | Final results, client presentations, portfolio work | Slower | Highest |
| `eco` | Quick previews, trying multiple colors, concept exploration | Faster | Good |

## Multi-Turn Color Exploration

Use `session_id` to iterate and explore colors:

```bash
# Start with a base change
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Change my hair to copper red",
    "image_urls": ["https://example.com/selfie.jpg"],
    "session_id": "hair-exploration"
  }'

# Request adjustment
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Make it more auburn and less orange, add some brown lowlights",
    "session_id": "hair-exploration"
  }'

# Try a completely different direction
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Actually, let me see the original photo with silver gray hair instead",
    "session_id": "hair-exploration"
  }'
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | Insufficient balance | Top up at eachlabs.ai |
| No hair detected | Hair not visible in image | Use a clearer photo with visible hair |
| Unnatural results | Low quality source image | Use higher resolution photo with good lighting |
| Timeout | Complex generation | Set client timeout to minimum 10 minutes |

## Related Skills

- `each-sense` - Core API documentation
- `face-swap` - Face swapping capabilities
- `image-edit` - General image editing
- `product-photo-generation` - E-commerce product shots
