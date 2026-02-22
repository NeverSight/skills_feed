---
name: portrait-enhancement
description: Enhance portrait photos using each::sense AI. Professional-grade retouching including skin smoothing, teeth whitening, eye enhancement, blemish removal, lighting adjustment, and more.
metadata:
  author: eachlabs
  version: "1.0"
---

# Portrait Enhancement

Transform portrait photos with professional-grade AI retouching using each::sense. This skill provides comprehensive portrait enhancement capabilities for photographers, content creators, and anyone looking to polish their photos.

## Features

- **Skin Smoothing**: Natural texture-preserving skin retouching
- **Teeth Whitening**: Brighten smiles while maintaining realism
- **Eye Enhancement**: Brighten, sharpen, and enhance eye clarity
- **Blemish Removal**: Remove acne, scars, and skin imperfections
- **Lighting Adjustment**: Fix harsh shadows, add studio lighting effects
- **Background Blur (Bokeh)**: Create professional depth-of-field effects
- **Hair Enhancement**: Add volume, shine, and fix flyaways
- **Makeup Enhancement**: Enhance or add natural-looking makeup
- **Age Reduction**: Subtle age-defying retouching
- **Professional Polish**: Complete portrait finishing workflow

## Quick Start

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Enhance this portrait with natural skin smoothing and subtle teeth whitening",
    "mode": "max",
    "image_urls": ["https://example.com/portrait.jpg"]
  }'
```

## API Configuration

| Setting | Value |
|---------|-------|
| Endpoint | `POST https://sense.eachlabs.run/chat` |
| Content-Type | `application/json` |
| Accept | `text/event-stream` |
| Client Timeout | Minimum 10 minutes |

## Mode Selection

Ask your users before generating:

**"Do you want fast & cheap, or high quality?"**

| Mode | Best For | Speed | Quality |
|------|----------|-------|---------|
| `max` | Final deliverables, client work, print-ready | Slower | Highest |
| `eco` | Quick previews, bulk processing, drafts | Faster | Good |

## Use Case Examples

### 1. Skin Smoothing and Retouching

Natural skin smoothing that preserves texture and pores while reducing imperfections.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Apply natural skin smoothing to this portrait. Keep the skin texture realistic, reduce visible pores and fine lines, but avoid the plastic look. Maintain skin detail around eyes and lips.",
    "mode": "max",
    "image_urls": ["https://example.com/portrait.jpg"]
  }'
```

### 2. Teeth Whitening

Brighten teeth naturally without over-whitening.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Whiten the teeth in this portrait photo. Make them bright but natural looking - not Hollywood white. Remove any yellow or staining while keeping the natural tooth shape and texture.",
    "mode": "max",
    "image_urls": ["https://example.com/smile-portrait.jpg"]
  }'
```

### 3. Eye Enhancement

Brighten and sharpen eyes for a more captivating look.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Enhance the eyes in this portrait. Brighten the whites, add subtle catchlights, increase iris clarity and color vibrancy, and reduce any redness or dark circles under the eyes. Keep it natural.",
    "mode": "max",
    "image_urls": ["https://example.com/headshot.jpg"]
  }'
```

### 4. Blemish Removal

Remove acne, scars, and temporary skin imperfections.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Remove blemishes from this portrait including acne spots, small scars, and any temporary skin imperfections. Keep moles and natural beauty marks. Preserve the natural skin texture in treated areas.",
    "mode": "max",
    "image_urls": ["https://example.com/portrait-blemishes.jpg"]
  }'
```

### 5. Lighting Adjustment

Fix poor lighting or add studio-quality lighting effects.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Fix the lighting in this portrait. It was taken in harsh midday sun with unflattering shadows. Apply soft studio-style lighting with gentle shadows, reduce harsh highlights on the forehead, and add subtle rim lighting for depth.",
    "mode": "max",
    "image_urls": ["https://example.com/harsh-light-portrait.jpg"]
  }'
```

### 6. Background Blur (Bokeh)

Create professional depth-of-field effects to make subjects stand out.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Add a professional bokeh effect to this portrait. Blur the background with a smooth, creamy quality like an 85mm f/1.4 lens. Keep the subject perfectly sharp including hair edges. The blur should gradually increase with distance from the subject.",
    "mode": "max",
    "image_urls": ["https://example.com/portrait-busy-background.jpg"]
  }'
```

### 7. Hair Enhancement

Add volume, shine, and polish to hair.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Enhance the hair in this portrait. Add natural-looking shine and healthy luster, tame flyaway hairs, add subtle volume at the crown, and make the hair color more vibrant. Keep the overall hairstyle unchanged.",
    "mode": "max",
    "image_urls": ["https://example.com/portrait-hair.jpg"]
  }'
```

### 8. Makeup Enhancement

Enhance existing makeup or add subtle, natural-looking makeup.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Enhance the makeup in this portrait photo. Add subtle contouring to define cheekbones, slightly darken and define the eyebrows, add a soft natural lip color, and apply light mascara effect to the lashes. Keep everything looking natural and not overdone.",
    "mode": "max",
    "image_urls": ["https://example.com/natural-portrait.jpg"]
  }'
```

### 9. Age Reduction

Subtle, natural-looking age-defying retouching.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Apply subtle age reduction to this portrait. Soften fine lines and wrinkles, reduce sagging under the eyes, lift the corners of the mouth slightly, and add a healthy glow to the skin. The result should look natural - like a well-rested version, not like a different person.",
    "mode": "max",
    "image_urls": ["https://example.com/mature-portrait.jpg"]
  }'
```

### 10. Professional Portrait Polish

Complete professional retouching workflow combining multiple enhancements.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Give this portrait a complete professional polish suitable for a corporate headshot. Apply natural skin smoothing, subtle teeth whitening, eye enhancement with catchlights, blemish removal, soft studio lighting, gentle background blur, and hair touch-up. The final result should look polished but authentic - suitable for LinkedIn or company website.",
    "mode": "max",
    "image_urls": ["https://example.com/corporate-portrait.jpg"]
  }'
```

## Multi-Turn Enhancement Workflow

Use `session_id` to iteratively refine portrait enhancements:

```bash
# Initial enhancement
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Start with basic skin smoothing on this portrait",
    "session_id": "portrait-retouch-001",
    "image_urls": ["https://example.com/portrait.jpg"]
  }'

# Add teeth whitening
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Now add subtle teeth whitening to the result",
    "session_id": "portrait-retouch-001"
  }'

# Add eye enhancement
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Enhance the eyes - brighten and add catchlights",
    "session_id": "portrait-retouch-001"
  }'

# Final background blur
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Finally, add a gentle background blur for a professional look",
    "session_id": "portrait-retouch-001"
  }'
```

## Batch Processing Multiple Portraits

Process multiple portraits with consistent enhancement:

```bash
# Portrait 1
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Professional headshot retouch: natural skin smoothing, eye brightening, subtle background blur",
    "mode": "eco",
    "image_urls": ["https://example.com/team-member-1.jpg"]
  }'

# Portrait 2
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Professional headshot retouch: natural skin smoothing, eye brightening, subtle background blur",
    "mode": "eco",
    "image_urls": ["https://example.com/team-member-2.jpg"]
  }'

# Portrait 3
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Professional headshot retouch: natural skin smoothing, eye brightening, subtle background blur",
    "mode": "eco",
    "image_urls": ["https://example.com/team-member-3.jpg"]
  }'
```

## Prompt Tips for Portrait Enhancement

When requesting portrait enhancements, include these details:

1. **Specific Enhancement**: What exactly to enhance (skin, eyes, teeth, etc.)
2. **Intensity Level**: Subtle, moderate, or dramatic
3. **Natural Look**: Emphasize keeping results realistic
4. **Areas to Preserve**: Features that should remain unchanged
5. **Use Case**: Headshot, social media, print, etc.

### Example Prompt Structure

```
"Apply [enhancement type] to this portrait.
[Specific instructions for the enhancement].
Keep [what to preserve].
The result should look [desired outcome] for [use case]."
```

## Best Practices

### Maintaining Realism
- Always specify "natural looking" or "realistic" in prompts
- Request preservation of skin texture when smoothing
- Avoid over-whitening teeth or over-brightening eyes
- Keep enhancements subtle for professional contexts

### Preserving Identity
- Don't request changes that alter facial structure
- Preserve natural beauty marks and distinctive features
- Keep skin tone consistent across the image
- Maintain natural proportions

### Technical Considerations
- Provide high-resolution source images for best results
- Images with good initial lighting enhance better
- Front-facing portraits work best for most enhancements
- JPG and PNG formats are supported

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | Insufficient balance | Top up at eachlabs.ai |
| Content policy violation | Prohibited content | Ensure portrait is appropriate |
| Timeout | Complex enhancement | Set client timeout to minimum 10 minutes |
| No face detected | Face not visible | Provide clear portrait with visible face |

## Related Skills

- `each-sense` - Core API documentation
- `face-swap` - Face swapping capabilities
- `image-edit` - General image editing
- `image-generation` - Generate new portraits from scratch
