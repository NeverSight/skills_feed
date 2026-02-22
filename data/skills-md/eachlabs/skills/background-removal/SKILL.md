---
name: background-removal
description: Remove backgrounds from images using each::sense AI. Create transparent PNGs, replace backgrounds with solid colors or scenes, and handle complex edges like hair with precision.
metadata:
  author: eachlabs
  version: "1.0"
---

# Background Removal

Remove backgrounds from images using each::sense. This skill creates professional cutouts with transparent backgrounds, replaces backgrounds with solid colors or scenes, and handles complex edges including hair and fur with precision.

## Features

- **Transparent PNG Export**: Clean cutouts with alpha channel transparency
- **Solid Color Replacement**: Replace backgrounds with any solid color
- **Scene Replacement**: Place subjects in new environments
- **Hair Detail Preservation**: Advanced edge detection for fine details
- **Complex Edge Handling**: Accurate cutouts for difficult subjects
- **Batch Processing**: Remove backgrounds from multiple images
- **E-commerce Ready**: Product cutouts optimized for online stores
- **Portrait Optimization**: Professional headshots and profile photos

## Quick Start

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Remove the background from this image and export as transparent PNG",
    "image_urls": ["https://example.com/my-photo.jpg"],
    "mode": "max"
  }'
```

## Use Case Examples

### 1. Product Background Removal

Clean cutouts for e-commerce product listings.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Remove the background from this product photo. Create a clean cutout with transparent background, preserving all product details and shadows. Output as PNG.",
    "image_urls": ["https://example.com/product-shoe.jpg"],
    "mode": "max"
  }'
```

### 2. Portrait Background Removal

Professional headshot cutouts for business or personal use.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Remove the background from this portrait photo. Preserve all hair details and create clean edges around the person. Export as transparent PNG for professional use.",
    "image_urls": ["https://example.com/headshot.jpg"],
    "mode": "max"
  }'
```

### 3. Transparent PNG Export

Export with alpha channel for use in design software.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Remove the background from this image and export as a high-quality transparent PNG. Ensure clean alpha channel edges suitable for compositing in Photoshop or Figma.",
    "image_urls": ["https://example.com/object.jpg"],
    "mode": "max"
  }'
```

### 4. Background Replacement with Solid Color

Replace background with a specific solid color.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Remove the background from this product image and replace it with a pure white background (#FFFFFF). Keep the product shadows for a natural look.",
    "image_urls": ["https://example.com/product.jpg"],
    "mode": "max"
  }'
```

### 5. Background Replacement with Scene

Place subject in a completely new environment.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Remove the background from this person photo and place them in a modern office environment with soft natural lighting from large windows. Make it look natural and professional.",
    "image_urls": ["https://example.com/person.jpg"],
    "mode": "max"
  }'
```

### 6. Hair Detail Preservation

Handle complex hair edges with precision.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Remove the background from this portrait. Pay special attention to preserving fine hair details, flyaway strands, and wispy edges. The subject has curly hair that needs careful edge handling. Export as transparent PNG.",
    "image_urls": ["https://example.com/curly-hair-portrait.jpg"],
    "mode": "max"
  }'
```

### 7. Complex Edge Handling

Handle difficult subjects like fur, feathers, or translucent objects.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Remove the background from this image of a fluffy cat. Preserve all the fur details including the soft edges and individual hair strands. The cat has white fur which is challenging - maintain clean edges without halos.",
    "image_urls": ["https://example.com/fluffy-cat.jpg"],
    "mode": "max"
  }'
```

### 8. Batch Background Removal

Process multiple product images with consistent results.

```bash
# First image in batch
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Remove the background from this product image. Export as transparent PNG with consistent edge quality.",
    "image_urls": ["https://example.com/product-1.jpg"],
    "session_id": "batch-background-removal-001",
    "mode": "eco"
  }'

# Second image (same session for consistency)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Remove the background from this product image with the same settings as before.",
    "image_urls": ["https://example.com/product-2.jpg"],
    "session_id": "batch-background-removal-001",
    "mode": "eco"
  }'

# Third image
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Remove the background from this product image, same approach.",
    "image_urls": ["https://example.com/product-3.jpg"],
    "session_id": "batch-background-removal-001",
    "mode": "eco"
  }'
```

### 9. E-commerce Product Cutouts

Amazon/Shopify-ready product images with white backgrounds.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an e-commerce ready product cutout from this image. Remove the background and replace with pure white. The product should be centered with clean edges. This is for Amazon/Shopify listing - must meet marketplace image requirements.",
    "image_urls": ["https://example.com/product-handbag.jpg"],
    "mode": "max"
  }'
```

### 10. Social Media Profile Photos

Create professional profile pictures with clean backgrounds.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Remove the background from this selfie and replace with a professional gradient background (dark blue to light blue). Preserve all hair details. This is for a LinkedIn profile photo - make it look polished and professional.",
    "image_urls": ["https://example.com/selfie.jpg"],
    "mode": "max"
  }'
```

## Multi-Turn Creative Iteration

Use `session_id` to refine background removal results:

```bash
# Initial removal
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Remove the background from this portrait photo",
    "image_urls": ["https://example.com/portrait.jpg"],
    "session_id": "portrait-project-001"
  }'

# Refine the result
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "The hair edges look a bit rough. Can you refine them to be smoother and more natural?",
    "session_id": "portrait-project-001"
  }'

# Change background
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Now place this cutout on a beach sunset background",
    "session_id": "portrait-project-001"
  }'
```

## Mode Selection

Ask your users before generating:

**"Do you want fast & cheap, or high quality?"**

| Mode | Best For | Speed | Quality |
|------|----------|-------|---------|
| `max` | Final production images, complex edges, hair details | Slower | Highest |
| `eco` | Quick previews, batch processing, simple objects | Faster | Good |

## Best Practices

### For Products
- **Lighting**: Original image should have even lighting for best results
- **Contrast**: High contrast between product and background helps accuracy
- **Shadows**: Request shadow preservation for natural-looking results
- **Resolution**: Higher resolution input yields better edge quality

### For Portraits
- **Hair**: Mention hair type in prompt for better edge detection
- **Clothing**: Describe clothing edges if they blend with background
- **Accessories**: Note glasses, jewelry, or items that need preservation

### For Complex Subjects
- **Transparency**: Mention glass, smoke, or translucent elements
- **Fine Details**: Specify fur, feathers, or intricate patterns
- **Multiple Subjects**: Describe what should be kept vs removed

## Prompt Tips

When requesting background removal, include:

1. **Subject Type**: Product, person, animal, object
2. **Edge Complexity**: Simple edges vs hair/fur/fine details
3. **Output Format**: Transparent PNG or replacement background
4. **Background Color**: Specific hex code if replacing with solid color
5. **Use Case**: E-commerce, social media, compositing, etc.

### Example Prompt Structure

```
"Remove the background from this [subject type].
[Specific edge requirements like hair or fur details].
Output as [transparent PNG / white background / specific scene].
This is for [use case] - [any specific requirements]."
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | Insufficient balance | Top up at eachlabs.ai |
| Poor edge quality | Low resolution input | Use higher resolution source image |
| Halos around edges | Complex background colors | Use `max` mode for better edge detection |
| Timeout | Large image or complex processing | Set client timeout to minimum 10 minutes |

## Related Skills

- `each-sense` - Core API documentation
- `product-photo-generation` - Generate product images from scratch
- `image-edit` - General image editing capabilities
