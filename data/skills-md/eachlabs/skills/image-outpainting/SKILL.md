---
name: image-outpainting
description: Extend and expand images beyond their original boundaries using each::sense AI. Create panoramic views, convert aspect ratios, add backgrounds, and uncrop photos intelligently.
metadata:
  author: eachlabs
  version: "1.0"
---

# Image Outpainting / Extension

Extend images beyond their original boundaries using each::sense. This skill uses AI to intelligently generate new content that seamlessly blends with the original image, enabling aspect ratio conversions, background expansion, and creative image extensions.

## Features

- **Horizontal Extension**: Expand images left and right for wider compositions
- **Vertical Extension**: Add content above and below for taller images
- **Aspect Ratio Conversion**: Transform portrait to landscape or vice versa
- **Background Expansion**: Add more context and environment to photos
- **Uncropping**: Recover or imagine content outside the original frame
- **Panoramic Creation**: Turn single images into wide panoramic views
- **Product Photo Enhancement**: Extend product shots for banners and ads
- **Artwork Extension**: Expand illustrations and digital art

## Quick Start

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Extend this image horizontally to create a wider 16:9 composition, maintaining the same style and lighting",
    "image_urls": ["https://example.com/original-photo.jpg"],
    "mode": "max"
  }'
```

## Common Outpainting Scenarios

| Use Case | Target Ratio | Description |
|----------|--------------|-------------|
| Portrait to Landscape | 16:9 | Convert vertical photos for video/desktop |
| Square to Widescreen | 21:9 | Create cinematic compositions |
| Product Banner | 3:1 or 4:1 | Extend product shots for web banners |
| Social Media | 4:5 or 1:1 | Optimize for Instagram feed |
| Panoramic | 2:1 or 3:1 | Create wide scenic views |
| Full Bleed | Custom | Add margins for printing |

## Use Case Examples

### 1. Extend Image Horizontally

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Extend this image horizontally on both sides. Add more of the natural environment while keeping the subject centered. Maintain consistent lighting, color grading, and style throughout the extension.",
    "image_urls": ["https://example.com/landscape-photo.jpg"],
    "mode": "max"
  }'
```

### 2. Extend Image Vertically

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Extend this image vertically - add more sky above and more ground/foreground below. Keep the horizon line natural and maintain the same atmosphere and time of day.",
    "image_urls": ["https://example.com/landscape.jpg"],
    "mode": "max"
  }'
```

### 3. Convert Portrait to Landscape

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Convert this vertical portrait photo to a horizontal 16:9 landscape format. Extend the background on both sides to create a wider scene. Keep the person as the main subject and ensure the extended areas match the original environment perfectly.",
    "image_urls": ["https://example.com/portrait-photo.jpg"],
    "mode": "max"
  }'
```

### 4. Convert Square to Widescreen

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Transform this square 1:1 image into a cinematic 21:9 widescreen format. Extend the scene horizontally while preserving the central composition. Match the lighting, textures, and visual style seamlessly.",
    "image_urls": ["https://example.com/square-image.jpg"],
    "mode": "max"
  }'
```

### 5. Extend Product Photo for Banner

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Extend this product photo into a wide banner format (approximately 4:1 ratio). Keep the product on the left third of the image and extend the clean background to the right to create space for text overlay. Maintain the same studio lighting and surface texture.",
    "image_urls": ["https://example.com/product-shot.jpg"],
    "mode": "max"
  }'
```

### 6. Add More Background/Context

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Expand this image in all directions to add more environmental context. The subject is too tightly cropped - extend the scene to show more of the surroundings, making it feel less cramped. Keep the original subject size and add approximately 50% more space around it.",
    "image_urls": ["https://example.com/tight-crop.jpg"],
    "mode": "max"
  }'
```

### 7. Uncrop a Cropped Photo

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "This photo has been tightly cropped - uncrop it to reveal more of the scene. Extend downward to show the full body (currently cut off at the waist) and extend the sides to show more of the room interior. Generate realistic content that matches the existing style.",
    "image_urls": ["https://example.com/cropped-photo.jpg"],
    "mode": "max"
  }'
```

### 8. Create Panoramic from Single Image

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Transform this landscape photo into a wide panoramic image with a 3:1 aspect ratio. Extend the scenic view on both left and right sides, continuing the mountain range, sky, and terrain naturally. Create a sweeping vista that feels like a real panoramic photograph.",
    "image_urls": ["https://example.com/mountain-view.jpg"],
    "mode": "max"
  }'
```

### 9. Extend Artwork/Illustration

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Extend this digital illustration horizontally to double its width. Continue the artistic style, color palette, and visual elements seamlessly. This is a fantasy landscape illustration - extend the magical forest and atmospheric elements on both sides while maintaining the same painting technique and mood.",
    "image_urls": ["https://example.com/fantasy-illustration.jpg"],
    "mode": "max"
  }'
```

### 10. Add Environment to Portrait

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "This is a headshot with a blurred background. Extend the image to show more of the environment - convert to a 3/4 or full body shot by extending downward, and widen the scene to show the cafe/office setting implied by the background. Keep the portrait style and depth of field consistent.",
    "image_urls": ["https://example.com/headshot.jpg"],
    "mode": "max"
  }'
```

## Multi-Turn Outpainting Session

Use `session_id` to iterate on outpainting results:

```bash
# Initial extension request
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Extend this beach photo horizontally to create a wider 16:9 composition",
    "image_urls": ["https://example.com/beach.jpg"],
    "session_id": "outpaint-beach-001",
    "mode": "max"
  }'

# Request adjustments
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "The right side extension looks good, but can you add some palm trees on the left side to balance the composition?",
    "session_id": "outpaint-beach-001"
  }'

# Further refinement
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Now extend it vertically as well - add more dramatic sky with sunset clouds above",
    "session_id": "outpaint-beach-001"
  }'
```

## Prompt Tips for Outpainting

When requesting image extensions, include these details in your prompt:

1. **Direction**: Specify horizontal, vertical, or all directions
2. **Target Ratio**: Mention the desired aspect ratio (16:9, 21:9, 3:1, etc.)
3. **Content Guidance**: Describe what should appear in extended areas
4. **Style Matching**: Request consistent lighting, colors, and atmosphere
5. **Subject Position**: Specify where the original subject should be placed
6. **Use Case**: Mention if it's for a banner, social media, print, etc.

### Example Prompt Structure

```
"Extend this [image type] [direction] to [target ratio/size].
[Describe what to add in extended areas].
Maintain [lighting/style/atmosphere] consistency.
Position the original [subject] in the [location]."
```

## Mode Selection

Ask your users before generating:

**"Do you want fast & cheap, or high quality?"**

| Mode | Best For | Speed | Quality |
|------|----------|-------|---------|
| `max` | Final outputs, professional use, complex scenes | Slower | Highest |
| `eco` | Quick previews, testing compositions, iterations | Faster | Good |

## Best Practices

### For Best Results
- **High-quality source**: Start with a high-resolution original image
- **Clear edges**: Images with distinct edges outpaint more seamlessly
- **Consistent lighting**: Describe the lighting in your prompt for better matching
- **Reasonable extensions**: Extending 2-3x the original size works best
- **Iterate**: Use sessions to refine results progressively

### Common Pitfalls to Avoid
- Don't extend too far in one step - do it gradually
- Avoid extending images with complex foreground elements at edges
- Don't expect perfect results with heavily stylized or abstract images
- Be specific about what should appear in extended areas

### Aspect Ratio Reference

| Name | Ratio | Common Use |
|------|-------|------------|
| Square | 1:1 | Instagram, thumbnails |
| Standard Photo | 4:3 | Traditional photography |
| Instagram Portrait | 4:5 | Instagram feed |
| HD Video | 16:9 | YouTube, presentations |
| Cinematic | 21:9 | Film, ultrawide monitors |
| Panoramic | 2:1, 3:1 | Scenic views, banners |
| Banner | 4:1, 5:1 | Website headers, ads |

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | Insufficient balance | Top up at eachlabs.ai |
| Content policy violation | Prohibited content | Adjust prompt to comply with content policies |
| Timeout | Complex generation | Set client timeout to minimum 10 minutes |
| Poor edge blending | Low quality source | Use higher resolution source image |

## Related Skills

- `each-sense` - Core API documentation
- `image-inpainting` - Edit specific regions within images
- `image-upscaling` - Enhance image resolution
- `background-removal` - Remove and replace backgrounds
