---
name: photo-restoration
description: Restore and enhance old, damaged, or degraded photos using each::sense AI. Fix scratches, tears, fading, water damage, colorize black and white photos, and restore faces in historical images.
metadata:
  author: eachlabs
  version: "1.0"
---

# Photo Restoration

Restore and enhance old, damaged, or degraded photos using each::sense. This skill leverages AI-powered restoration models to repair scratches, colorize black and white images, fix fading, remove film grain, and bring damaged photos back to life.

## Features

- **Damage Repair**: Fix scratches, tears, creases, and physical damage
- **Colorization**: Add natural colors to black and white photos
- **Fading Recovery**: Restore vibrancy to faded and washed-out images
- **Water Damage Repair**: Recover photos affected by water or moisture damage
- **Face Restoration**: Enhance and restore faces in old or low-quality photos
- **Film Grain Removal**: Clean up grain and noise from old film photographs
- **Historical Photo Enhancement**: Improve quality of archival and vintage images
- **Torn Photo Reconstruction**: Digitally repair torn and ripped photographs

## Quick Start

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Restore this old damaged family photo - fix the scratches and improve the overall quality",
    "mode": "max",
    "image_urls": ["https://example.com/old-family-photo.jpg"]
  }'
```

## Use Case Examples

### 1. Old Damaged Photo Restoration

Restore a photo with multiple types of damage including scratches, stains, and degradation.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Restore this old damaged photo from the 1950s. It has scratches, some staining, and general degradation. Please repair the damage while preserving the authentic vintage feel.",
    "mode": "max",
    "image_urls": ["https://example.com/damaged-1950s-photo.jpg"]
  }'
```

### 2. Black and White Photo Colorization

Add realistic colors to a black and white photograph.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Colorize this black and white photo from the 1940s. It shows a family portrait - add natural, realistic colors to skin tones, clothing, and the background.",
    "mode": "max",
    "image_urls": ["https://example.com/bw-family-portrait.jpg"]
  }'
```

### 3. Scratched Photo Repair

Remove scratches and surface damage from a photograph.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Remove the scratches from this photo. There are multiple deep scratches across the surface and some light surface marks. Keep the image sharp and clear after repair.",
    "mode": "max",
    "image_urls": ["https://example.com/scratched-photo.jpg"]
  }'
```

### 4. Faded Photo Enhancement

Restore color and contrast to faded photographs.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Enhance this faded photo - the colors have washed out over time and the image looks dull. Restore the vibrancy and contrast while keeping it looking natural, not over-processed.",
    "mode": "max",
    "image_urls": ["https://example.com/faded-vintage-photo.jpg"]
  }'
```

### 5. Water Damaged Photo Recovery

Repair photos that have suffered water or moisture damage.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Restore this water damaged photo. It has staining, warping effects, and some areas where the image has deteriorated due to moisture. Recover as much detail as possible.",
    "mode": "max",
    "image_urls": ["https://example.com/water-damaged-photo.jpg"]
  }'
```

### 6. Face Restoration in Old Photos

Enhance and restore faces that are blurry or degraded in old photographs.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Restore the faces in this old family photo. The faces are blurry and lack detail. Enhance facial features to make them clear and recognizable while maintaining the authentic look of the era.",
    "mode": "max",
    "image_urls": ["https://example.com/old-blurry-faces.jpg"]
  }'
```

### 7. Historical Photo Restoration

Restore archival photographs with professional-grade enhancement.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Restore this historical photograph from the early 1900s. It is a street scene that has significant age-related degradation. Improve clarity, fix damage, and optionally colorize it while preserving historical accuracy.",
    "mode": "max",
    "image_urls": ["https://example.com/historical-1900s-street.jpg"]
  }'
```

### 8. Family Photo Restoration

Restore precious family memories with comprehensive repair.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Restore this precious family photo from my grandparents wedding in 1960. It has yellowing, some creases, and the edges are damaged. Make it look fresh while preserving the nostalgic quality.",
    "mode": "max",
    "image_urls": ["https://example.com/grandparents-wedding.jpg"]
  }'
```

### 9. Torn Photo Repair

Digitally reconstruct photos that have been physically torn.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Repair this torn photo - there is a visible tear line running through the middle of the image. Reconstruct the damaged areas seamlessly and restore the photo to its original state.",
    "mode": "max",
    "image_urls": ["https://example.com/torn-photo.jpg"]
  }'
```

### 10. Film Grain Removal

Clean up excessive grain and noise from old film photographs.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Remove the heavy film grain from this old photograph. The grain is very visible and distracting. Clean it up while preserving the sharpness and detail of the image. Keep some subtle texture so it does not look overly processed.",
    "mode": "max",
    "image_urls": ["https://example.com/grainy-film-photo.jpg"]
  }'
```

## Multi-Turn Restoration Sessions

Use `session_id` for iterative restoration and refinement:

```bash
# Initial restoration
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Restore this old damaged black and white photo - fix the scratches and damage first",
    "session_id": "family-photo-restoration",
    "image_urls": ["https://example.com/old-bw-damaged.jpg"]
  }'

# Follow up with colorization
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Now colorize the restored photo with natural colors appropriate for the 1930s era",
    "session_id": "family-photo-restoration"
  }'

# Further refinement
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Enhance the faces to make them clearer and more detailed",
    "session_id": "family-photo-restoration"
  }'
```

## Batch Restoration

Process multiple photos with consistent settings:

```bash
# Photo 1
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Restore and colorize this old family photo",
    "mode": "eco",
    "image_urls": ["https://example.com/family-photo-1.jpg"]
  }'

# Photo 2
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Restore and colorize this old family photo",
    "mode": "eco",
    "image_urls": ["https://example.com/family-photo-2.jpg"]
  }'

# Photo 3
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Restore and colorize this old family photo",
    "mode": "eco",
    "image_urls": ["https://example.com/family-photo-3.jpg"]
  }'
```

## Mode Selection

Ask your users before processing:

**"Do you want fast & affordable, or highest quality?"**

| Mode | Best For | Speed | Quality |
|------|----------|-------|---------|
| `max` | Final restorations, precious family photos, professional archival work | Slower | Highest |
| `eco` | Quick previews, batch processing, initial assessments | Faster | Good |

## Best Practices

### For Optimal Results

- **Provide context**: Mention the era, type of damage, and what aspects are most important to preserve
- **Start with damage repair**: Fix scratches and tears before colorization
- **Use multi-turn sessions**: Build up restoration in stages for complex projects
- **Specify faces**: If faces are important, explicitly mention face restoration
- **Preserve authenticity**: Request preservation of vintage qualities if desired

### Prompt Tips

1. **Describe the damage**: Scratches, tears, fading, water stains, yellowing
2. **Mention the era**: This helps with appropriate colorization
3. **State priorities**: What matters most - faces, overall clarity, color accuracy
4. **Set expectations**: Natural look vs maximum enhancement

### Example Prompt Structure

```
"Restore this [era] photo. The damage includes [list damage types].
Focus on [priority areas]. [Additional preferences like colorization,
authenticity preservation, etc.]"
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | Insufficient balance | Top up at eachlabs.ai |
| Content policy violation | Prohibited content | Ensure photo complies with content policies |
| Timeout | Complex restoration | Set client timeout to minimum 10 minutes |
| Low quality result | Insufficient input resolution | Use highest available scan/photo resolution |

## Related Skills

- `each-sense` - Core API documentation
- `image-enhancement` - General image quality improvement
- `face-restoration` - Specialized face enhancement
- `image-upscaling` - Increase image resolution
