---
name: image-upscaling
description: Upscale images using each::sense AI. Enhance resolution for web, print, large format displays, with options for face enhancement, noise reduction, and AI art optimization.
metadata:
  author: eachlabs
  version: "1.0"
---

# Image Upscaling

Upscale and enhance images using each::sense. This skill provides AI-powered image upscaling from 2x to 16x resolution with intelligent enhancement options for faces, noise reduction, and detail preservation.

## Features

- **2x Upscaling**: Quick enhancement for web images and social media
- **4x Upscaling**: High-quality output for print materials
- **8x/16x Upscaling**: Large format displays, billboards, posters
- **Face Enhancement**: Intelligent facial detail restoration during upscale
- **Noise Reduction**: Clean up grainy or compressed images while upscaling
- **Old Photo Restoration**: Revive vintage and damaged photographs
- **AI Art Enhancement**: Preserve and enhance AI-generated artwork details
- **Product Image Enhancement**: E-commerce ready high-resolution product shots

## Quick Start

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Upscale this image 4x for print quality",
    "image_urls": ["https://example.com/my-image.jpg"],
    "mode": "max"
  }'
```

## Upscaling Scale Factors

| Scale | Output Size (from 1024px) | Best Use Case |
|-------|---------------------------|---------------|
| 2x | 2048px | Web images, social media, thumbnails |
| 4x | 4096px | Print materials, high-res displays |
| 8x | 8192px | Large format prints, posters |
| 16x | 16384px | Billboards, exhibition displays |

## Use Case Examples

### 1. 2x Upscaling for Web Images

Perfect for improving image quality for websites, social media posts, and digital marketing.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Upscale this web image 2x. Optimize for fast loading while improving sharpness and clarity. The image will be used on a website hero section.",
    "image_urls": ["https://example.com/website-hero.jpg"],
    "mode": "eco"
  }'
```

### 2. 4x Upscaling for Print

High-quality upscaling for brochures, flyers, magazines, and other print materials requiring 300 DPI.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Upscale this image 4x for print production. I need 300 DPI quality for a magazine spread. Preserve all fine details and ensure crisp edges.",
    "image_urls": ["https://example.com/magazine-photo.jpg"],
    "mode": "max"
  }'
```

### 3. 8x/16x Upscaling for Large Format

Extreme upscaling for billboards, trade show displays, and wall-sized prints.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Upscale this image 8x for a large format banner print. The final output will be displayed on a 10 foot wide trade show backdrop. Maximize detail enhancement and ensure no artifacts.",
    "image_urls": ["https://example.com/tradeshow-banner.jpg"],
    "mode": "max"
  }'
```

### 4. Face Enhancement During Upscale

Intelligent facial restoration that enhances eyes, skin texture, and facial features while upscaling portraits.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Upscale this portrait 4x with face enhancement enabled. Restore facial details, enhance eyes, improve skin texture while keeping it natural. This is a headshot photo.",
    "image_urls": ["https://example.com/portrait-headshot.jpg"],
    "mode": "max"
  }'
```

### 5. Noise Reduction + Upscale

Clean up grainy, compressed, or low-quality images while increasing resolution.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Upscale this noisy low-light photo 4x. Apply aggressive noise reduction while preserving important details. The image was taken in low light conditions and has visible grain and compression artifacts.",
    "image_urls": ["https://example.com/low-light-photo.jpg"],
    "mode": "max"
  }'
```

### 6. Old Photo Upscaling

Restore and upscale vintage photographs, old family photos, and historical images.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Upscale and restore this old family photograph from the 1970s. The image is faded, slightly damaged, and low resolution. Enhance to 4x while restoring colors, fixing damage, and improving clarity. Preserve the vintage aesthetic.",
    "image_urls": ["https://example.com/old-family-photo.jpg"],
    "mode": "max"
  }'
```

### 7. AI Art Upscaling

Enhance AI-generated artwork while preserving artistic style and avoiding artifacts.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Upscale this AI-generated artwork 4x for print. Preserve the artistic style and enhance fine details. This is digital art created by an AI image generator - avoid adding unwanted textures or changing the artistic style.",
    "image_urls": ["https://example.com/ai-artwork.png"],
    "mode": "max"
  }'
```

### 8. Product Image Upscaling

E-commerce optimized upscaling for product photography with detail enhancement.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Upscale this product photo 4x for e-commerce use. Enhance product details, improve sharpness on edges and textures. The image is of a leather handbag and needs to show material texture clearly for zoom functionality.",
    "image_urls": ["https://example.com/product-handbag.jpg"],
    "mode": "max"
  }'
```

### 9. Video Frame Upscaling

Enhance individual video frames or thumbnails extracted from video content.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Upscale this video frame 4x. This is a still frame extracted from 1080p video footage. Enhance it to 4K quality while reducing compression artifacts and maintaining natural motion blur where present.",
    "image_urls": ["https://example.com/video-frame.jpg"],
    "mode": "max"
  }'
```

### 10. Batch Upscaling Workflow

Process multiple images with consistent settings using session persistence.

```bash
# First image in batch
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Upscale this product image 4x with face enhancement and noise reduction. This is the first of a series of product photos I need processed.",
    "image_urls": ["https://example.com/product-001.jpg"],
    "session_id": "batch-upscale-products",
    "mode": "max"
  }'

# Second image (same session maintains settings)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Upscale this next product image using the same settings as before.",
    "image_urls": ["https://example.com/product-002.jpg"],
    "session_id": "batch-upscale-products"
  }'

# Third image
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Continue with the same upscaling settings for this product image.",
    "image_urls": ["https://example.com/product-003.jpg"],
    "session_id": "batch-upscale-products"
  }'
```

## Best Practices

### Choosing Scale Factor
- **2x**: Sufficient for most web and social media use cases
- **4x**: Standard for print quality (300 DPI equivalent)
- **8x+**: Only for large format where viewing distance is greater

### Quality Tips
- **Source Quality Matters**: Higher quality input produces better upscaled output
- **File Format**: Use PNG or high-quality JPEG (90%+) as input when possible
- **Face Enhancement**: Enable only for images with human faces
- **Noise Reduction**: Use aggressively for low-light or heavily compressed images

### Output Considerations
- **File Size**: Higher scale factors produce significantly larger files
- **Processing Time**: 8x and 16x upscaling takes longer - be patient
- **Viewing Distance**: Large format prints are viewed from distance; extreme detail isn't always necessary

## Prompt Tips for Image Upscaling

When requesting upscaling, include these details in your prompt:

1. **Scale Factor**: Specify 2x, 4x, 8x, or 16x
2. **Use Case**: Web, print, large format display
3. **Image Type**: Photo, AI art, product shot, portrait
4. **Special Requirements**: Face enhancement, noise reduction, artifact removal
5. **Output Intent**: Final use case helps optimize processing

### Example Prompt Structure

```
"Upscale this [image type] [scale factor] for [use case].
[Special requirements like face enhancement or noise reduction].
[Additional context about the source image quality or intended output]."
```

## Mode Selection

Ask your users before processing:

**"Do you want fast & cheap, or high quality?"**

| Mode | Best For | Speed | Quality |
|------|----------|-------|---------|
| `max` | Final production images, print materials, important projects | Slower | Highest |
| `eco` | Quick previews, batch testing, web thumbnails | Faster | Good |

## Multi-Turn Upscaling Workflow

Use `session_id` to iterate on upscaling results:

```bash
# Initial upscale
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Upscale this photo 4x for print",
    "image_urls": ["https://example.com/photo.jpg"],
    "session_id": "upscale-project-001"
  }'

# Request adjustments
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "The result looks good but can you also apply face enhancement and reduce noise?",
    "session_id": "upscale-project-001"
  }'

# Request different scale
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Actually I need 8x for a larger print. Can you upscale it further?",
    "session_id": "upscale-project-001"
  }'
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | Insufficient balance | Top up at eachlabs.ai |
| Image too large | Source image exceeds maximum dimensions | Resize source image before upscaling |
| Timeout | Large scale factors take longer | Set client timeout to minimum 10 minutes |
| Unsupported format | Invalid image format | Use JPEG, PNG, or WebP input |

## Related Skills

- `each-sense` - Core API documentation
- `image-generation` - Generate images from text prompts
- `image-editing` - Edit and modify existing images
- `old-photo-restoration` - Specialized restoration for vintage photos
