---
name: eye-color-changer
description: Change eye colors in photos using each::sense AI. Transform natural eye colors, create fantasy effects, heterochromia, glowing eyes, and more with realistic blending and natural-looking results.
metadata:
  author: eachlabs
  version: "1.0"
---

# Eye Color Changer

Transform eye colors in photos using each::sense. This skill enables realistic eye color changes, fantasy effects, and creative eye modifications while maintaining natural appearance and proper iris detail.

## Features

- **Natural Color Changes**: Blue, green, brown, hazel, gray, amber
- **Fantasy Colors**: Purple, red, golden, silver, white
- **Heterochromia**: Different colors for each eye
- **Special Effects**: Cat/slit pupils, glowing eyes, hypnotic patterns
- **Color Enhancement**: Intensify natural eye colors
- **Batch Processing**: Multiple color options from a single photo
- **Realistic Blending**: Maintains natural iris texture and reflections

## Quick Start

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Change the eye color to bright blue in this photo",
    "image_urls": ["https://example.com/portrait.jpg"],
    "mode": "max"
  }'
```

## Supported Eye Color Options

| Category | Colors | Best For |
|----------|--------|----------|
| Natural | Blue, green, brown, hazel, gray, amber | Realistic transformations |
| Fantasy | Purple, violet, red, golden, silver | Creative/artistic portraits |
| Special | Glowing, cat-eye, heterochromia | Fantasy characters, cosplay |
| Enhanced | Vivid versions of natural colors | Making eyes pop in photos |

## Use Case Examples

### 1. Change to Blue Eyes

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Change the eye color to a natural bright blue. Keep the iris texture and reflections realistic. The blue should look like natural blue eyes, not contact lenses.",
    "image_urls": ["https://example.com/portrait.jpg"],
    "mode": "max"
  }'
```

### 2. Change to Green Eyes

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Transform the eye color to emerald green. Maintain natural iris patterns and make sure the color blends realistically with the skin tone around the eyes.",
    "image_urls": ["https://example.com/portrait.jpg"],
    "mode": "max"
  }'
```

### 3. Change to Brown Eyes

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Change the eyes to warm brown color. Make it look like natural dark brown eyes with subtle golden flecks in the iris for realism.",
    "image_urls": ["https://example.com/portrait.jpg"],
    "mode": "max"
  }'
```

### 4. Change to Hazel Eyes

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Transform the eye color to hazel - a natural blend of green and brown with golden undertones. The color should transition from darker near the pupil to lighter at the edges of the iris.",
    "image_urls": ["https://example.com/portrait.jpg"],
    "mode": "max"
  }'
```

### 5. Fantasy Colors (Purple, Red, Golden)

```bash
# Purple/Violet Eyes
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Change the eye color to a deep violet purple. Make it look otherworldly but still maintain realistic iris texture. Perfect for a fantasy or cosplay character look.",
    "image_urls": ["https://example.com/portrait.jpg"],
    "mode": "max"
  }'

# Red Eyes
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Transform the eyes to a striking crimson red color. Keep the iris detail and make it look like supernatural red eyes - vampire or demon aesthetic.",
    "image_urls": ["https://example.com/portrait.jpg"],
    "mode": "max"
  }'

# Golden Eyes
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Change the eye color to golden yellow, like a wolf or supernatural being. Maintain realistic iris patterns but with a luminous golden color.",
    "image_urls": ["https://example.com/portrait.jpg"],
    "mode": "max"
  }'
```

### 6. Heterochromia (Different Colored Eyes)

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create heterochromia - make the left eye bright blue and the right eye emerald green. Both eyes should look natural and realistic, just different colors from each other.",
    "image_urls": ["https://example.com/portrait.jpg"],
    "mode": "max"
  }'
```

### 7. Cat/Slit Pupil Effect

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Transform the eyes to have cat-like vertical slit pupils with golden yellow iris color. Make it look like feline or reptilian eyes while keeping the overall eye shape natural to the face.",
    "image_urls": ["https://example.com/portrait.jpg"],
    "mode": "max"
  }'
```

### 8. Glowing Eyes Effect

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Make the eyes glow with an ethereal blue light. Add a subtle luminous effect that makes the eyes appear to emit light, with a soft glow around the iris. Perfect for a supernatural or magical character effect.",
    "image_urls": ["https://example.com/portrait.jpg"],
    "mode": "max"
  }'
```

### 9. Natural Color Enhancement

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Enhance the natural eye color to make it more vivid and striking. Intensify the existing color, add more depth and clarity to the iris, and make the eyes really pop without changing the base color.",
    "image_urls": ["https://example.com/portrait.jpg"],
    "mode": "max"
  }'
```

### 10. Multiple Color Options from Same Photo

```bash
# Use session_id to generate multiple variations
# First variation - Blue
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Change the eye color to bright blue. Keep it natural looking.",
    "image_urls": ["https://example.com/portrait.jpg"],
    "session_id": "eye-color-variations-001",
    "mode": "eco"
  }'

# Second variation - Green (same session)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Now create another version with emerald green eyes instead.",
    "session_id": "eye-color-variations-001",
    "mode": "eco"
  }'

# Third variation - Hazel (same session)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create one more version with hazel eyes.",
    "session_id": "eye-color-variations-001",
    "mode": "eco"
  }'
```

## Best Practices

### For Realistic Results
- **High-quality source images**: Use well-lit photos where eyes are clearly visible
- **Front-facing portraits**: Best results with eyes looking toward the camera
- **Describe iris details**: Mention if you want specific patterns, flecks, or gradients
- **Natural lighting reference**: Mention the lighting style for consistent reflections

### For Fantasy Effects
- **Specify the aesthetic**: Vampire, alien, anime, supernatural, etc.
- **Describe intensity**: Subtle glow vs. bright luminescence
- **Include character context**: Helps AI match the overall style

### Prompt Tips
1. **Be specific about shade**: "Ice blue" vs. "ocean blue" vs. "navy blue"
2. **Mention blending**: Ask for natural transitions at iris edges
3. **Request iris texture**: Preserve or modify the natural patterns
4. **Consider lighting**: Specify if you want reflections maintained

## Mode Selection

| Mode | Best For | Speed | Quality |
|------|----------|-------|---------|
| `max` | Final photos, professional use, detailed effects | Slower | Highest |
| `eco` | Quick previews, batch variations, testing colors | Faster | Good |

## Multi-Turn Creative Iteration

Use `session_id` to refine eye color changes:

```bash
# Initial change
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Change the eye color to blue",
    "image_urls": ["https://example.com/portrait.jpg"],
    "session_id": "eye-edit-project"
  }'

# Refine the result
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Make the blue more intense and add a slight ring of darker blue around the edge of the iris",
    "session_id": "eye-edit-project"
  }'

# Add special effect
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Now add a subtle glow effect to make the eyes look magical",
    "session_id": "eye-edit-project"
  }'
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | Insufficient balance | Top up at eachlabs.ai |
| No eyes detected | Face not visible or eyes closed | Use a photo with clearly visible open eyes |
| Unnatural blending | Poor source image quality | Use higher resolution, well-lit photos |
| Timeout | Complex generation | Set client timeout to minimum 10 minutes |

## Related Skills

- `each-sense` - Core API documentation
- `face-swap` - Face swapping capabilities
- `image-edit` - General image editing
- `portrait-generation` - AI portrait creation
