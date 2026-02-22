---
name: style-transfer
description: Transform photos into stunning artistic styles using each::sense AI. Apply Van Gogh, Picasso, anime, watercolor, oil painting, and more to any image.
metadata:
  author: eachlabs
  version: "1.0"
---

# Image Style Transfer

Transform any photo into stunning artistic styles using each::sense. This skill applies artistic techniques from famous painters, illustration styles, and digital art to your images while preserving the original composition and subject.

## Features

- **Classic Art Styles**: Van Gogh, Monet, Picasso, Rembrandt
- **Traditional Media**: Watercolor, oil painting, pencil sketch, charcoal
- **Digital Art**: Anime/manga, pixel art, pop art, comic book
- **Custom Reference**: Use any reference image as a style source
- **Preservation Options**: Maintain facial features, composition, and key details
- **Multiple Outputs**: Generate variations with different intensity levels

## Quick Start

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Transform this photo into Van Gogh Starry Night style with swirling brushstrokes and vibrant blues",
    "image_urls": ["https://example.com/my-portrait.jpg"],
    "mode": "max"
  }'
```

## Style Categories

| Category | Styles | Best For |
|----------|--------|----------|
| Impressionist | Monet, Renoir, Degas | Landscapes, gardens, soft scenes |
| Post-Impressionist | Van Gogh, Cezanne | Portraits, expressive scenes |
| Cubist | Picasso, Braque | Portraits, abstract interpretations |
| Traditional | Watercolor, oil, pencil | Any subject, classic feel |
| Digital | Anime, pixel art, pop art | Modern, stylized looks |
| Custom | Any reference image | Matching specific aesthetics |

## Use Case Examples

### 1. Van Gogh Starry Night Style

Transform photos with Van Gogh's iconic swirling brushstrokes and expressive color palette.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Apply Van Gogh Starry Night style to this cityscape photo. Use swirling, dynamic brushstrokes, deep blues and bright yellows, expressive post-impressionist technique. Make the sky dramatic with spiral patterns.",
    "image_urls": ["https://example.com/cityscape.jpg"],
    "mode": "max"
  }'
```

### 2. Picasso Cubism Style

Deconstruct and reimagine photos in Picasso's revolutionary cubist style.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Transform this portrait into Picasso cubist style. Fragment the face into geometric shapes, show multiple perspectives simultaneously, use muted earth tones with bold accents. Analytical cubism approach.",
    "image_urls": ["https://example.com/portrait.jpg"],
    "mode": "max"
  }'
```

### 3. Monet Impressionist Style

Apply Monet's soft, light-filled impressionist technique to landscapes and scenes.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Apply Claude Monet impressionist style to this garden photo. Soft dappled light, loose brushstrokes, focus on atmosphere and light rather than details. Like his Water Lilies series - dreamy and ethereal.",
    "image_urls": ["https://example.com/garden.jpg"],
    "mode": "max"
  }'
```

### 4. Anime/Manga Style Transfer

Convert photos into Japanese anime or manga illustration style.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Transform this photo into anime style. Large expressive eyes, clean line art, cel-shaded coloring, vibrant colors. Studio Ghibli inspired aesthetic with soft backgrounds and detailed character rendering.",
    "image_urls": ["https://example.com/person-photo.jpg"],
    "mode": "max"
  }'
```

### 5. Watercolor Painting Style

Transform photos into delicate watercolor paintings with flowing colors and soft edges.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Convert this landscape photo into a watercolor painting. Soft washes of color, visible paper texture, gentle color bleeds, transparent layers. Traditional watercolor technique with wet-on-wet effects.",
    "image_urls": ["https://example.com/landscape.jpg"],
    "mode": "max"
  }'
```

### 6. Oil Painting Style

Apply rich, textured oil painting techniques to create museum-quality artistic renditions.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Transform this portrait into a classical oil painting. Rich impasto brushstrokes, dramatic chiaroscuro lighting, deep saturated colors. Renaissance master style with visible paint texture and depth.",
    "image_urls": ["https://example.com/portrait.jpg"],
    "mode": "max"
  }'
```

### 7. Pencil Sketch Style

Convert photos into detailed pencil drawings with crosshatching and shading.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Convert this photo into a detailed pencil sketch. Fine crosshatching for shading, clean outlines, graphite texture on paper. Photorealistic pencil drawing style with subtle gradients and precise details.",
    "image_urls": ["https://example.com/subject.jpg"],
    "mode": "max"
  }'
```

### 8. Pop Art Style

Transform photos into bold, colorful pop art inspired by Warhol and Lichtenstein.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Apply pop art style to this portrait. Bold flat colors, Ben-Day dots, high contrast, Andy Warhol inspired. Bright neon palette with black outlines, comic book aesthetic meets fine art.",
    "image_urls": ["https://example.com/portrait.jpg"],
    "mode": "max"
  }'
```

### 9. Pixel Art Style

Convert photos into retro pixel art with limited color palettes.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Transform this photo into pixel art style. 16-bit retro gaming aesthetic, limited color palette, visible pixels, clean edges. Like classic SNES or arcade game sprites but detailed.",
    "image_urls": ["https://example.com/character.jpg"],
    "mode": "max"
  }'
```

### 10. Custom Reference Image Style

Use any artwork as a style reference to transfer its aesthetic to your photo.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Apply the artistic style from the first image (the reference artwork) to the second image (the photo). Match the color palette, brushwork, texture, and overall aesthetic of the reference while preserving the composition of the photo.",
    "image_urls": [
      "https://example.com/reference-artwork.jpg",
      "https://example.com/my-photo.jpg"
    ],
    "mode": "max"
  }'
```

## Best Practices

### Style Transfer Tips
- **Be Specific**: Describe the exact style elements you want (brushstrokes, colors, technique)
- **Reference Artists**: Mention specific artists or artworks for more accurate results
- **Preserve Features**: For portraits, mention if you want to preserve facial features
- **Intensity Control**: Use terms like "subtle," "moderate," or "dramatic" to control effect strength

### Image Guidelines
- **High Resolution**: Start with high-quality source images for best results
- **Clear Subjects**: Well-lit photos with clear subjects transfer better
- **Composition Matters**: Simple compositions often yield cleaner stylized results

### Prompt Tips for Style Transfer

Include these details in your prompts:

1. **Style Name**: Specific artist or technique (Van Gogh, watercolor, anime)
2. **Key Elements**: Brushstrokes, colors, textures you want
3. **Mood**: Dramatic, soft, vibrant, muted
4. **Preservation**: What to keep from the original (face, composition)
5. **Intensity**: How strongly to apply the style

### Example Prompt Structure

```
"Apply [style name] style to this [subject type].
[Describe key style elements: brushstrokes, colors, technique].
[Mood and atmosphere].
[What to preserve from original]."
```

## Mode Selection

Ask your users before generating:

**"Do you want fast & cheap, or high quality?"**

| Mode | Best For | Speed | Quality |
|------|----------|-------|---------|
| `max` | Final artwork, prints, professional use | Slower | Highest |
| `eco` | Quick previews, style exploration, drafts | Faster | Good |

## Multi-Turn Style Iteration

Use `session_id` to iterate on style transfers:

```bash
# Initial style transfer
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Apply Van Gogh style to this portrait",
    "image_urls": ["https://example.com/portrait.jpg"],
    "session_id": "style-project-001"
  }'

# Refine the style
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Make the brushstrokes more pronounced and add more yellow tones like in Starry Night",
    "session_id": "style-project-001"
  }'

# Try a variation
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Now create a version with cooler blue tones instead",
    "session_id": "style-project-001"
  }'
```

## Batch Style Exploration

Generate multiple style variations for comparison:

```bash
# Van Gogh variation
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Apply Van Gogh style to this photo",
    "image_urls": ["https://example.com/photo.jpg"],
    "mode": "eco"
  }'

# Monet variation
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Apply Monet impressionist style to this photo",
    "image_urls": ["https://example.com/photo.jpg"],
    "mode": "eco"
  }'

# Anime variation
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Transform this photo into anime style",
    "image_urls": ["https://example.com/photo.jpg"],
    "mode": "eco"
  }'
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | Insufficient balance | Top up at eachlabs.ai |
| Content policy violation | Prohibited content | Ensure source image complies with content policies |
| Timeout | Complex generation | Set client timeout to minimum 10 minutes |
| Style not recognized | Vague style description | Be more specific about the artistic style wanted |

## Related Skills

- `each-sense` - Core API documentation
- `image-generation` - Generate images from text
- `image-editing` - Edit and enhance images
- `product-photo-generation` - E-commerce product shots
