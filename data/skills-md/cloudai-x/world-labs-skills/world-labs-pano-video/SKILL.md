---
name: world-labs-pano-video
description: Panorama and video input for world generation - maximum layout control
allowed-tools:
  - Bash
  - WebFetch
---

# World Labs Panorama & Video Input

Panoramas and videos provide the most control over world layout by capturing complete scene coverage.

## Quick Reference

### Credits

| Input Type | Marble 0.1-plus | Marble 0.1-mini |
| ---------- | --------------- | --------------- |
| Panorama   | 1,500           | 150             |
| Video      | 1,600           | 250             |

Panoramas skip the pano generation step, saving 80 credits compared to regular images.

## Panorama Input

### Requirements

| Requirement  | Specification                   |
| ------------ | ------------------------------- |
| Format       | 360° equirectangular projection |
| Aspect ratio | 2:1 (width:height) exactly      |
| Recommended  | 2560 pixels wide                |
| File size    | Max 20 MB                       |
| Formats      | PNG (recommended), JPG, WebP    |

### Equirectangular Format

```
┌─────────────────────────────────────────────┐
│                                             │
│  ← 360° horizontal field of view →          │
│                                             │
│  ← Left        Center        Right →        │
│                                             │
│  ↑ 180° vertical (zenith to nadir)          │
│                                             │
└─────────────────────────────────────────────┘
         Aspect ratio: 2:1
```

### Creating Panoramas

**From Phone:**

- iPhone: Panorama mode (stitch 360° or use apps like Street View)
- Android: Photo Sphere, Google Camera

**From Camera:**

- Shoot overlapping photos, stitch with PTGui, Hugin, or Lightroom

**From 360° Camera:**

- Insta360, GoPro Max, Ricoh Theta

### API Usage (Panorama)

Panoramas use the image type with the `is_pano` flag:

```json
{
  "model": "Marble 0.1-plus",
  "world_prompt": {
    "type": "image",
    "image_prompt": {
      "source": "media_asset",
      "media_asset_id": "550e8400-e29b-41d4-a716-446655440000"
    },
    "is_pano": true,
    "text_prompt": "Add dramatic sunset lighting"
  }
}
```

### Using Public URL (Panorama)

```json
{
  "model": "Marble 0.1-plus",
  "world_prompt": {
    "type": "image",
    "image_prompt": {
      "source": "uri",
      "uri": "https://example.com/360-panorama.jpg"
    },
    "is_pano": true,
    "text_prompt": "Transform into a mystical forest"
  }
}
```

### Best Practices for Panoramas

✅ **Level horizon**: Keep camera level during capture
✅ **Consistent exposure**: Use manual settings or HDR
✅ **No moving objects**: Static scenes work best
✅ **Clean nadir**: Bottom of image should be clean
✅ **Full 360°**: Complete coverage essential
✅ **Exact 2:1 aspect ratio**: Required for recognition

❌ **Tripod visible**: Remove or patch the tripod
❌ **People in frame**: Causes artifacts
❌ **Heavy stitching seams**: Fix edges before uploading
❌ **Phone panoramas**: Often lack full 180° vertical coverage

## Video Input

### Requirements

| Requirement  | Specification                    |
| ------------ | -------------------------------- |
| File size    | Max 100 MB                       |
| Duration     | Max 30 seconds                   |
| Rotation     | Camera should cover 180-360°     |
| Focal length | Fixed (no zoom during recording) |
| Exposure     | Fixed (manual mode)              |
| Movement     | Slow, smooth rotation            |
| Formats      | mp4, mov, webm                   |

### Recording Guidelines

**Camera Movement:**

```
         Start
           ↓
    ┌──────○──────┐
    │      │      │
    │   Rotate    │
    │   180-360°  │
    │      │      │
    └──────○──────┘
           ↓
          End
```

**DO:**

- Rotate camera smoothly in one direction
- Keep camera height constant
- Use gimbal or tripod for stability
- Maintain consistent speed
- Cover at least 180° of the space

**DON'T:**

- Pan back and forth
- Change height during recording
- Zoom in/out
- Record moving objects
- Exceed 30 seconds

### API Usage (Video)

```json
{
  "model": "Marble 0.1-plus",
  "world_prompt": {
    "type": "video",
    "video_prompt": {
      "source": "media_asset",
      "media_asset_id": "550e8400-e29b-41d4-a716-446655440000"
    },
    "text_prompt": "Transform into a mystical nighttime scene"
  }
}
```

### Using Public URL (Video)

```json
{
  "model": "Marble 0.1-plus",
  "world_prompt": {
    "type": "video",
    "video_prompt": {
      "source": "uri",
      "uri": "https://example.com/room-rotation.mp4"
    },
    "text_prompt": "A scenic mountain landscape"
  }
}
```

## Python Example

```python
import requests

def generate_from_pano_or_video(
    api_key: str,
    file_path: str,
    input_type: str,  # "panorama" or "video"
    prompt: str = None
):
    base_url = "https://api.worldlabs.ai/marble/v1"
    headers = {"WLT-Api-Key": api_key, "Content-Type": "application/json"}

    # Determine kind and extension
    ext = file_path.lower().split('.')[-1]
    if ext == "jpeg":
        ext = "jpg"

    # Set kind based on input type
    kind = "video" if input_type == "video" else "image"

    # Prepare upload
    prep = requests.post(
        f"{base_url}/media-assets:prepare_upload",
        headers=headers,
        json={"file_name": file_path.split('/')[-1], "kind": kind, "extension": ext}
    ).json()

    media_asset_id = prep["media_asset"]["media_asset_id"]
    upload_url = prep["upload_info"]["upload_url"]

    # Determine content type for upload
    content_types = {
        "jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png", "webp": "image/webp",
        "mp4": "video/mp4", "mov": "video/quicktime", "webm": "video/webm"
    }
    content_type = content_types.get(ext, "application/octet-stream")

    # Upload file
    with open(file_path, 'rb') as f:
        requests.put(upload_url, headers={"Content-Type": content_type}, data=f.read())

    # Build world_prompt based on type
    if input_type == "video":
        world_prompt = {
            "type": "video",
            "video_prompt": {
                "source": "media_asset",
                "media_asset_id": media_asset_id
            }
        }
    else:  # panorama
        world_prompt = {
            "type": "image",
            "image_prompt": {
                "source": "media_asset",
                "media_asset_id": media_asset_id
            },
            "is_pano": True
        }

    if prompt:
        world_prompt["text_prompt"] = prompt

    # Generate
    response = requests.post(
        f"{base_url}/worlds:generate",
        headers=headers,
        json={"model": "Marble 0.1-plus", "world_prompt": world_prompt}
    )

    return response.json()["operation_id"]

# Panorama example
pano_op = generate_from_pano_or_video(
    "your_api_key",
    "360_office.jpg",
    "panorama",
    "Add warm afternoon sunlight"
)

# Video example
video_op = generate_from_pano_or_video(
    "your_api_key",
    "room_rotation.mp4",
    "video",
    "Make it look abandoned and overgrown"
)
```

## Comparison: Panorama vs Video vs Images

| Feature          | Panorama                 | Video        | Multi-Image     |
| ---------------- | ------------------------ | ------------ | --------------- |
| Layout control   | ★★★★★                    | ★★★★☆        | ★★★☆☆           |
| Ease of capture  | ★★★☆☆                    | ★★★★☆        | ★★★★★           |
| Coverage         | Full 360°                | 180-360°     | Selected angles |
| Equipment needed | 360° camera or stitching | Phone/camera | Any camera      |
| Best for         | Complete environments    | Room capture | Specific views  |
| Credits (plus)   | 1,500                    | 1,600        | 1,600           |
| Credits (mini)   | 150                      | 250          | 250             |

## Troubleshooting

### Panorama Issues

| Problem                    | Solution                               |
| -------------------------- | -------------------------------------- |
| Not recognized as panorama | Verify exactly 2:1 aspect ratio        |
| Warped horizon             | Re-level panorama in editing software  |
| Stitching seams            | Use better overlap or manual alignment |
| Tripod in nadir            | Clone-stamp or use nadir patch         |
| Overexposed sky            | Use HDR or graduated filters           |

### Video Issues

| Problem               | Solution                         |
| --------------------- | -------------------------------- |
| Shaky footage         | Use gimbal or stabilize in post  |
| Inconsistent exposure | Lock exposure in manual mode     |
| Too fast rotation     | Slow down, stay under 30 seconds |
| Insufficient coverage | Ensure at least 180° rotation    |

## Related Skills

- `world-labs-api` - API integration details
- `world-labs-image-prompt` - Single image input
- `world-labs-multi-image` - Multi-image with direction control
- `world-labs-studio` - Compose and animate generated worlds
