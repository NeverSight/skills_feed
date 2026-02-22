---
name: photo-colorization
description: Colorize black and white photos using each::sense AI. Bring old family portraits, historical images, vintage photographs, and archival footage to life with intelligent, context-aware colorization.
metadata:
  author: eachlabs
  version: "1.0"
---

# Photo Colorization

Transform black and white photographs into vibrant, realistic color images using each::sense. This skill uses AI to intelligently analyze image content and apply historically accurate, contextually appropriate colors.

## Features

- **Automatic Colorization**: AI detects subjects and applies natural colors
- **Historical Accuracy**: Context-aware coloring for period-appropriate results
- **Portrait Enhancement**: Realistic skin tones for faces and portraits
- **Landscape Restoration**: Natural colors for outdoor and nature scenes
- **Vintage Photo Revival**: Bring old family photos back to life
- **Batch Processing**: Colorize multiple photos in sequence
- **Style Preservation**: Maintains original photo quality and details

## Quick Start

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Colorize this black and white photo with natural, realistic colors",
    "image_urls": ["https://example.com/bw-photo.jpg"],
    "mode": "max"
  }'
```

## Common Use Cases

| Use Case | Description | Best For |
|----------|-------------|----------|
| Family Archives | Colorize old family portraits and snapshots | Personal restoration |
| Historical Documentation | Period-accurate colorization for archives | Museums, historians |
| Portrait Enhancement | Realistic skin tones and facial features | Professional restoration |
| Landscape Revival | Natural outdoor and scenic colorization | Nature photography |
| Vintage Fashion | Accurate clothing and fabric colors | Fashion archives |
| Military/War Photos | Historical military photograph restoration | Memorial projects |
| Architecture | Building and interior colorization | Real estate, heritage |

## Use Case Examples

### 1. Automatic Colorization

Basic colorization with AI-detected colors.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Colorize this black and white photograph. Apply natural, realistic colors based on the image content. Maintain the original quality and details.",
    "image_urls": ["https://example.com/old-photo.jpg"],
    "mode": "max"
  }'
```

### 2. Historical Photo Colorization

Colorize with period-appropriate historical accuracy.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Colorize this historical photograph from the 1940s. Use period-accurate colors typical of that era - muted tones, authentic clothing colors, and historically appropriate details. This appears to be a street scene.",
    "image_urls": ["https://example.com/1940s-street.jpg"],
    "mode": "max"
  }'
```

### 3. Family Portrait Colorization

Bring old family photos to life with warm, natural tones.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Colorize this old family portrait photo. Apply natural skin tones, realistic hair colors, and period-appropriate clothing colors. The photo appears to be from the 1950s-1960s era. Make it look warm and inviting.",
    "image_urls": ["https://example.com/family-portrait-bw.jpg"],
    "mode": "max"
  }'
```

### 4. Landscape Colorization

Natural outdoor and scenic colorization.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Colorize this black and white landscape photograph. Apply natural colors - blue sky, green foliage, brown earth tones. Make it look like a vibrant summer day while preserving the original composition and atmosphere.",
    "image_urls": ["https://example.com/landscape-bw.jpg"],
    "mode": "max"
  }'
```

### 5. Portrait with Specific Skin Tones

Control skin tone colorization for accurate results.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Colorize this portrait photograph. The subject has a medium olive skin tone and dark brown hair. Apply natural, warm skin colors with subtle pink undertones. Eyes appear to be brown. Clothing looks like a dark formal suit.",
    "image_urls": ["https://example.com/portrait-bw.jpg"],
    "mode": "max"
  }'
```

### 6. Vintage Photo Colorization

Restore old photographs with era-specific styling.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Colorize this vintage photograph from the 1920s. Apply colors that match the Art Deco era - rich jewel tones for clothing, sepia-influenced skin tones, and period-appropriate interior colors. Maintain the vintage aesthetic while adding realistic color.",
    "image_urls": ["https://example.com/1920s-vintage.jpg"],
    "mode": "max"
  }'
```

### 7. War/Military Photo Colorization

Historical military photograph restoration with accuracy.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Colorize this World War II military photograph. Apply historically accurate colors - olive drab for US Army uniforms, appropriate skin tones for the soldiers, realistic equipment colors. Maintain the somber, documentary feel of the original while adding authentic military colors.",
    "image_urls": ["https://example.com/wwii-soldiers.jpg"],
    "mode": "max"
  }'
```

### 8. Architecture Colorization

Building and interior photograph colorization.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Colorize this black and white photograph of a Victorian-era building. Apply appropriate architectural colors - red or brown brick, white trim, dark roof tiles, green copper patina if visible. Include natural sky colors and surrounding landscape elements.",
    "image_urls": ["https://example.com/victorian-building.jpg"],
    "mode": "max"
  }'
```

### 9. Fashion/Clothing Colorization

Accurate fabric and fashion colorization.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Colorize this 1960s fashion photograph. Apply era-appropriate colors - bold mod colors like orange, turquoise, and pink were popular. The model appears to be wearing a structured dress. Apply realistic fabric textures and vibrant 60s palette.",
    "image_urls": ["https://example.com/1960s-fashion.jpg"],
    "mode": "max"
  }'
```

### 10. Batch Colorize Multiple Photos

Process multiple photos with consistent styling using session continuity.

```bash
# First photo in batch
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Colorize this black and white family photo from the 1950s. Apply warm, natural colors with period-appropriate tones. This is photo 1 of a series from the same family album.",
    "image_urls": ["https://example.com/family-album-001.jpg"],
    "session_id": "family-album-colorization",
    "mode": "max"
  }'

# Second photo (same session for consistency)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Colorize this second photo from the same family album. Maintain consistent skin tones and color style as the previous colorization.",
    "image_urls": ["https://example.com/family-album-002.jpg"],
    "session_id": "family-album-colorization",
    "mode": "max"
  }'

# Third photo (continuing series)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Colorize the third photo. Same family, same era. Keep the color palette consistent with previous images.",
    "image_urls": ["https://example.com/family-album-003.jpg"],
    "session_id": "family-album-colorization",
    "mode": "max"
  }'
```

## Best Practices

### Image Quality
- **Resolution**: Higher resolution photos yield better colorization results
- **Contrast**: Good contrast in the original helps AI identify details
- **Clarity**: Sharp, clear photos colorize better than blurry ones
- **Condition**: Digital restoration before colorization can improve results

### Prompt Tips
- **Provide context**: Mention the era, location, or subject matter
- **Specify skin tones**: If known, describe the subject's complexion
- **Note clothing colors**: If you know original colors, include them
- **Describe the scene**: Outdoor/indoor, season, time of day

### Historical Accuracy
- Research the time period for authentic color palettes
- Consider regional variations in fashion and architecture
- Military uniforms and equipment have specific documented colors
- Vintage car and vehicle colors are often well-documented

## Mode Selection

| Mode | Best For | Speed | Quality |
|------|----------|-------|---------|
| `max` | Final restorations, archival work, gifts | Slower | Highest |
| `eco` | Quick previews, batch testing, drafts | Faster | Good |

**Recommendation**: Use `eco` mode for initial tests, then `max` for final output.

## Multi-Turn Refinement

Use `session_id` to iterate and refine colorization:

```bash
# Initial colorization
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Colorize this old portrait photograph with natural colors",
    "image_urls": ["https://example.com/portrait.jpg"],
    "session_id": "portrait-restoration"
  }'

# Refine the result
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "The skin tones look a bit too warm. Can you redo the colorization with cooler, more natural skin tones?",
    "session_id": "portrait-restoration"
  }'

# Further adjustment
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "The dress should be blue, not green. Please adjust the clothing color.",
    "session_id": "portrait-restoration"
  }'
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | Insufficient balance | Top up at eachlabs.ai |
| `Invalid image URL` | URL not accessible | Ensure image URL is publicly accessible |
| Timeout | Large image or complex scene | Set client timeout to minimum 10 minutes |
| Poor colorization | Low quality source | Use higher resolution, clearer source image |

## Related Skills

- `each-sense` - Core API documentation
- `image-restoration` - General image restoration
- `image-enhancement` - Enhance and upscale images
- `face-restoration` - Specialized face enhancement
