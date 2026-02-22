---
name: object-removal
description: Remove unwanted objects, people, text, and imperfections from photos using each::sense AI. Clean up images with intelligent inpainting that seamlessly fills removed areas.
metadata:
  author: eachlabs
  version: "1.0"
---

# Object Removal & Inpainting

Remove unwanted elements from photos using each::sense. This skill intelligently removes objects, people, text, watermarks, and imperfections while seamlessly filling the removed areas with contextually appropriate content.

## Features

- **Object Removal**: Remove unwanted items from any photo
- **Person Removal**: Remove people from backgrounds cleanly
- **Text/Watermark Removal**: Clean up images with unwanted text overlays
- **Blemish Removal**: Remove skin imperfections and photo artifacts
- **Wire/Line Removal**: Clean up power lines, cables, and wires
- **Logo Removal**: Remove branding and logos from images
- **Shadow Removal**: Eliminate unwanted shadows
- **Background Cleanup**: Remove distracting background elements

## Quick Start

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Remove the person standing on the left side of this photo",
    "image_urls": ["https://example.com/beach-photo.jpg"],
    "mode": "max"
  }'
```

## Use Case Examples

### 1. Remove Person from Photo

Remove an unwanted person from a group photo or scenic shot.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Remove the person in the red shirt from this beach photo. Fill the area naturally with the ocean and sand background.",
    "image_urls": ["https://example.com/beach-group.jpg"],
    "mode": "max"
  }'
```

### 2. Remove Unwanted Object

Clean up photos by removing distracting objects.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Remove the trash can and bench from the right side of this park landscape photo. Make it look like a clean natural scene.",
    "image_urls": ["https://example.com/park-landscape.jpg"],
    "mode": "max"
  }'
```

### 3. Remove Text/Watermark

Clean up images with unwanted text overlays or watermarks.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Remove the watermark from the bottom right corner of this image. Restore the original background seamlessly.",
    "image_urls": ["https://example.com/watermarked-image.jpg"],
    "mode": "max"
  }'
```

### 4. Remove Blemish/Imperfection

Clean up skin imperfections or photo artifacts.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Remove the skin blemishes and acne marks from this portrait photo. Keep the skin looking natural and maintain the original skin texture.",
    "image_urls": ["https://example.com/portrait.jpg"],
    "mode": "max"
  }'
```

### 5. Remove Power Lines/Wires

Clean up landscape and architectural photos by removing distracting wires.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Remove all the power lines and electrical wires from this sunset cityscape photo. Make the sky look clean and unobstructed.",
    "image_urls": ["https://example.com/cityscape-wires.jpg"],
    "mode": "max"
  }'
```

### 6. Remove Tourists from Landmark Photo

Get that perfect empty landmark shot by removing crowds.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Remove all the tourists and people from this Eiffel Tower photo. I want it to look like an empty plaza with just the monument.",
    "image_urls": ["https://example.com/eiffel-tower-crowded.jpg"],
    "mode": "max"
  }'
```

### 7. Remove Ex from Photo

Salvage memories by removing someone from personal photos.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Remove the person on the right side of this vacation photo. Fill in with the background scenery naturally so it looks like a solo travel photo.",
    "image_urls": ["https://example.com/vacation-couple.jpg"],
    "mode": "max"
  }'
```

### 8. Remove Logo/Branding

Clean up product photos or images with unwanted branding.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Remove the brand logo from the t-shirt in this photo. Replace it with plain fabric that matches the shirt color and texture.",
    "image_urls": ["https://example.com/branded-shirt.jpg"],
    "mode": "max"
  }'
```

### 9. Clean Up Product Photo

Remove distracting elements from e-commerce product shots.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Clean up this product photo by removing the price tag, dust spots, and the reflection of the photographer in the surface. Make it look professional and ready for e-commerce.",
    "image_urls": ["https://example.com/product-raw.jpg"],
    "mode": "max"
  }'
```

### 10. Remove Shadow

Eliminate unwanted shadows from photos.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Remove the harsh shadow cast by the photographer on the ground in this outdoor portrait. Make the lighting look natural and even.",
    "image_urls": ["https://example.com/portrait-shadow.jpg"],
    "mode": "max"
  }'
```

## Multi-Turn Object Removal

Use `session_id` for iterative removal and refinement:

```bash
# First removal
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Remove the car parked on the left side of this street photo",
    "image_urls": ["https://example.com/street-scene.jpg"],
    "session_id": "cleanup-project-001"
  }'

# Second removal (same session)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Now also remove the garbage bins near the building entrance",
    "session_id": "cleanup-project-001"
  }'

# Refinement (same session)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "The area where the car was removed looks a bit blurry. Can you improve the texture to match the surrounding pavement better?",
    "session_id": "cleanup-project-001"
  }'
```

## Prompt Tips for Object Removal

When requesting object removal, include these details in your prompt:

1. **What to remove**: Be specific about the object(s) to remove
2. **Location**: Describe where the object is in the image (left, right, center, background)
3. **Fill guidance**: Describe what should replace the removed area
4. **Context preservation**: Mention if certain elements should be kept intact

### Example Prompt Structure

```
"Remove [object description] from [location in image].
Fill the area with [expected background/content].
Keep [elements to preserve] intact."
```

### Good Prompt Examples

- "Remove the person in the blue jacket standing near the fountain on the left side"
- "Remove all text and watermarks from the image, restore the original background"
- "Remove the car and fill with matching grass and pathway"

### Prompts to Avoid

- "Clean up this photo" (too vague)
- "Remove stuff" (not specific)
- "Make it better" (unclear objective)

## Mode Selection

| Mode | Best For | Speed | Quality |
|------|----------|-------|---------|
| `max` | Final deliverables, complex removals, professional work | Slower | Highest |
| `eco` | Quick previews, simple removals, bulk processing | Faster | Good |

**Recommendation**: Use `max` mode for complex removals (people, large objects) and `eco` for simple cleanups (small blemishes, dust spots).

## Best Practices

### For Best Results

- **High-resolution source**: Use the highest quality source image available
- **Clear descriptions**: Be specific about what to remove and where it is
- **Simple backgrounds**: Objects in front of simple, repetitive backgrounds are easier to remove cleanly
- **Multiple passes**: For complex scenes, use multi-turn removal to address one element at a time

### Challenging Scenarios

- **Complex backgrounds**: Objects in front of detailed, unique backgrounds may require manual refinement
- **Large objects**: Removing very large objects (more than 30% of image) may produce less realistic results
- **Reflections**: Objects with reflections may need separate removal requests for the object and its reflection
- **Shadows**: Remember to request shadow removal if the object casts a visible shadow

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | Insufficient balance | Top up at eachlabs.ai |
| Content policy violation | Prohibited content | Review content guidelines |
| Timeout | Complex generation | Set client timeout to minimum 10 minutes |
| Poor removal quality | Vague prompt | Be more specific about location and fill content |

## Client Timeout Configuration

Object removal operations can take time, especially for complex scenes. Configure your HTTP client with a minimum **10 minute timeout** to avoid premature disconnections.

```bash
# Example with extended timeout
curl --max-time 600 -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Remove all people from this crowded plaza photo",
    "image_urls": ["https://example.com/crowded-plaza.jpg"],
    "mode": "max"
  }'
```

## Related Skills

- `each-sense` - Core API documentation
- `image-edit` - General image editing capabilities
- `background-removal` - Remove and replace backgrounds
