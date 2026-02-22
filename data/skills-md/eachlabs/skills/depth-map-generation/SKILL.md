---
name: depth-map-generation
description: Generate depth maps from images using each::sense AI. Create depth estimation for 3D effects, parallax animations, VR/AR applications, focus effects, and stereo image generation.
metadata:
  author: eachlabs
  version: "1.0"
---

# Depth Map Generation

Generate accurate depth maps from any image using each::sense. This skill extracts depth information from 2D images for 3D effects, parallax animations, VR/AR applications, computational photography, and more.

## Features

- **Monocular Depth Estimation**: Extract depth from single images
- **Portrait Depth Maps**: Precise depth for portrait photography effects
- **Landscape Depth**: Scene depth for panoramic and landscape images
- **Product Depth**: 3D-ready depth maps for e-commerce
- **Architectural Depth**: Building and interior depth analysis
- **3D Parallax Effects**: Depth data for Ken Burns-style animations
- **VR/AR Depth**: Real-time depth estimation for immersive experiences
- **Stereo Image Generation**: Convert 2D to stereoscopic 3D
- **Focus Stacking**: Depth-based focus plane selection
- **Background Blur**: Depth-aware bokeh and blur effects

## Quick Start

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate a depth map from this photo",
    "image_urls": ["https://example.com/photo.jpg"],
    "mode": "max"
  }'
```

## Depth Map Output Formats

| Format | Description | Use Case |
|--------|-------------|----------|
| Grayscale | 8-bit depth (white=near, black=far) | General purpose, visualization |
| Inverse Grayscale | 8-bit depth (black=near, white=far) | Some 3D software compatibility |
| Normalized | 0-1 range depth values | Machine learning pipelines |
| Metric | Real-world distance estimation | AR/VR, robotics |

## Use Case Examples

### 1. Generate Depth Map from Photo

Basic depth extraction from any image.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate a depth map from this image. Output as grayscale where white represents closer objects and black represents distant objects.",
    "image_urls": ["https://example.com/scene.jpg"],
    "mode": "max"
  }'
```

### 2. Portrait Depth Map

Extract precise depth from portrait photos for bokeh effects and 3D portraits.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a high-precision depth map from this portrait photo. Focus on accurate edge detection around the subject, especially hair and facial features. I need this for applying realistic depth-of-field effects.",
    "image_urls": ["https://example.com/portrait.jpg"],
    "mode": "max"
  }'
```

### 3. Landscape Depth Map

Generate depth from landscape and outdoor scenes with extended depth range.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate a depth map from this landscape photo. The scene has foreground elements, mid-ground terrain, and distant mountains. Capture the full depth range from near to far with good separation between depth layers.",
    "image_urls": ["https://example.com/landscape.jpg"],
    "mode": "max"
  }'
```

### 4. Product Depth for 3D Effect

Create depth maps for product images to enable 3D viewing experiences.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Extract a depth map from this product photo. I need accurate depth information to create a 3D interactive view for an e-commerce website. Focus on capturing the product shape and surface details.",
    "image_urls": ["https://example.com/product-sneaker.jpg"],
    "mode": "max"
  }'
```

### 5. Architectural Depth Map

Generate depth from architectural and interior photos for visualization.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a depth map from this interior architecture photo. Capture the spatial relationships between walls, furniture, and architectural elements. I need this for a virtual tour with depth-based transitions.",
    "image_urls": ["https://example.com/interior.jpg"],
    "mode": "max"
  }'
```

### 6. 3D Parallax Effect Creation

Generate depth maps optimized for creating parallax animations and Ken Burns effects.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate a depth map from this photo that I will use for a 3D parallax animation. I need clear depth separation between foreground, midground, and background elements. The depth should be smooth with distinct layers for a compelling parallax effect.",
    "image_urls": ["https://example.com/scene-for-parallax.jpg"],
    "mode": "max"
  }'
```

### 7. VR/AR Depth Estimation

Create depth maps suitable for virtual and augmented reality applications.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate a depth map from this room photo for AR/VR use. I need metric depth estimation that accurately represents real-world distances. This will be used for placing virtual objects in an augmented reality application.",
    "image_urls": ["https://example.com/room.jpg"],
    "mode": "max"
  }'
```

### 8. Stereo Image Generation

Convert 2D images to stereoscopic 3D using depth estimation.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate a depth map from this photo and use it to create a stereoscopic 3D image pair (left and right eye views). The stereo effect should be subtle enough for comfortable viewing but noticeable enough to create depth perception.",
    "image_urls": ["https://example.com/photo-for-stereo.jpg"],
    "mode": "max"
  }'
```

### 9. Focus Stacking Depth

Generate depth maps for computational focus stacking and all-in-focus composites.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a depth map from this macro/close-up photo. I need precise depth information to identify focus planes for computational focus stacking. Each depth layer should be clearly defined so I can select which areas should be in focus.",
    "image_urls": ["https://example.com/macro-photo.jpg"],
    "mode": "max"
  }'
```

### 10. Depth-Aware Background Blur

Generate depth for applying realistic bokeh and background blur effects.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate a depth map from this photo for applying depth-aware background blur. The subject in the foreground should be clearly separated from the background. I need accurate edge detection so the blur transition looks natural, similar to a portrait mode effect.",
    "image_urls": ["https://example.com/photo-for-blur.jpg"],
    "mode": "max"
  }'
```

## Multi-Turn Depth Processing

Use `session_id` to refine depth maps or process multiple related images:

```bash
# Initial depth estimation
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate a depth map from this photo",
    "image_urls": ["https://example.com/scene.jpg"],
    "session_id": "depth-project-001"
  }'

# Refine the depth map
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "The depth map looks good but can you enhance the edge detection around the main subject? The boundaries are a bit fuzzy.",
    "session_id": "depth-project-001"
  }'

# Apply the depth map for an effect
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Now use this depth map to create a 3D parallax video animation with subtle camera movement",
    "session_id": "depth-project-001"
  }'
```

## Batch Depth Processing

Process multiple images for consistent depth estimation:

```bash
# Process first image
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate a depth map from this product photo. I will be sending more product images that need consistent depth estimation.",
    "image_urls": ["https://example.com/product1.jpg"],
    "session_id": "product-depth-batch",
    "mode": "eco"
  }'

# Process second image with same settings
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate depth map for this product using the same approach as before",
    "image_urls": ["https://example.com/product2.jpg"],
    "session_id": "product-depth-batch",
    "mode": "eco"
  }'
```

## Mode Selection

| Mode | Best For | Speed | Quality |
|------|----------|-------|---------|
| `max` | Final production depth maps, VR/AR applications, professional compositing | Slower | Highest precision |
| `eco` | Quick previews, batch processing, prototyping | Faster | Good quality |

**Recommendation:** Use `max` mode when depth accuracy is critical (VR/AR, 3D conversion, professional compositing). Use `eco` mode for rapid iteration and batch processing.

## Best Practices

### Input Image Quality
- **Resolution**: Higher resolution inputs produce more detailed depth maps
- **Lighting**: Even lighting helps with accurate depth estimation
- **Contrast**: Clear contrast between objects improves depth separation
- **Focus**: Sharp images yield better edge detection in depth maps

### Depth Map Applications
- **Parallax Effects**: Use 3-5 distinct depth layers for best results
- **Bokeh/Blur**: Ensure clean subject edges for natural blur falloff
- **3D Conversion**: Provide context about scene scale for metric depth
- **VR/AR**: Request metric depth for real-world distance accuracy

### Prompt Tips
1. **Specify output format**: Grayscale, normalized, or metric depth
2. **Describe the scene**: Help the model understand spatial relationships
3. **State your use case**: Different applications benefit from different depth characteristics
4. **Request edge quality**: Specify if you need sharp or smooth depth transitions

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | Insufficient balance | Top up at eachlabs.ai |
| Image loading failed | Invalid or inaccessible image URL | Verify image URL is publicly accessible |
| Timeout | Complex or high-resolution image | Set client timeout to minimum 10 minutes |
| Low quality depth output | Poor input image quality | Use higher resolution, better lit source image |

## Technical Notes

- **Client Timeout**: Set your HTTP client timeout to minimum 10 minutes for complex depth estimation
- **Image Formats**: Supports JPEG, PNG, WebP input images
- **Output Format**: Depth maps are typically output as grayscale PNG images
- **Depth Range**: Relative depth (0-1) by default; metric depth available on request

## Related Skills

- `each-sense` - Core API documentation
- `image-to-3d` - Full 3D model generation from images
- `image-editing` - Apply depth-based effects to images
- `video-generation` - Create parallax videos from depth maps
