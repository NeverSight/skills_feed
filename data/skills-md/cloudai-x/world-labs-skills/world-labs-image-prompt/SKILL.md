---
name: world-labs-image-prompt
description: Single image input for world generation - requirements, best practices, and examples
allowed-tools:
  - Bash
  - WebFetch
---

# World Labs Single Image Input

Generate 3D worlds from a single reference image. The model extrapolates the scene to create an immersive 360° environment.

## Quick Reference

| Requirement            | Specification                      |
| ---------------------- | ---------------------------------- |
| Recommended resolution | 1024px on long side                |
| Maximum file size      | 20 MB                              |
| Formats                | PNG (recommended), JPG, WebP       |
| Aspect ratio           | 16:9, 9:16, or anything in between |

### Credits

| Input Type     | Marble 0.1-plus | Marble 0.1-mini |
| -------------- | --------------- | --------------- |
| Standard image | 1,580           | 230             |
| Panorama image | 1,500           | 150             |

Panoramas skip the pano generation step, saving 80 credits.

## Best Practices

### DO

✅ **Clear spatial definition**: Images with obvious depth and perspective
✅ **Wide shots**: Show foreground, midground, and background
✅ **Visible ground/floor**: Helps establish world orientation
✅ **Consistent lighting**: Clear, well-lit scenes
✅ **Environmental scenes**: Landscapes, interiors, architectural spaces

### DON'T

❌ **Close-up shots**: Lack spatial context for 3D reconstruction
❌ **People or animals**: As main subjects (may cause artifacts)
❌ **Abstract images**: Non-representational art
❌ **Borders or frames**: Decorative edges, watermarks
❌ **Heavy text overlays**: Text doesn't render clearly
❌ **Flat graphics**: 2D illustrations without depth
❌ **Blurry or low-contrast images**: Reduces detail inference

## Ideal Image Types

### Excellent Results

1. **Landscape photography** - Wide vistas with clear horizon and natural depth
2. **Architectural interiors** - Rooms with visible floor/walls/ceiling
3. **Street scenes** - Urban environments with buildings receding into distance
4. **Natural environments** - Forests, caves, beaches with organic depth

### Challenging (Use with Caution)

- Indoor scenes with complex reflections
- Very dark or overexposed images
- Images with motion blur
- Heavily edited/filtered photos

## API Usage

### Option 1: From Uploaded Media Asset

First upload your image (see `world-labs-api` skill), then:

```json
{
  "model": "Marble 0.1-plus",
  "world_prompt": {
    "type": "image",
    "image_prompt": {
      "source": "media_asset",
      "media_asset_id": "550e8400-e29b-41d4-a716-446655440000"
    },
    "text_prompt": "Optional description to guide interpretation"
  }
}
```

### Option 2: From Public URL

```json
{
  "model": "Marble 0.1-plus",
  "world_prompt": {
    "type": "image",
    "image_prompt": {
      "source": "uri",
      "uri": "https://example.com/my-image.jpg"
    },
    "text_prompt": "A beautiful mountain landscape"
  }
}
```

### Panorama Images (use `is_pano` flag)

For 360° equirectangular panoramas (2:1 aspect ratio):

```json
{
  "model": "Marble 0.1-plus",
  "world_prompt": {
    "type": "image",
    "image_prompt": {
      "source": "media_asset",
      "media_asset_id": "550e8400-e29b-41d4-a716-446655440000",
      "is_pano": true
    }
  }
}
```

## Upload Workflow

### Step 1: Prepare Upload

```bash
curl -X POST "https://api.worldlabs.ai/marble/v1/media-assets:prepare_upload" \
  -H "WLT-Api-Key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "file_name": "landscape.jpg",
    "kind": "image",
    "extension": "jpg"
  }'
```

**Response:**

```json
{
  "media_asset": {
    "media_asset_id": "550e8400-e29b-41d4-a716-446655440000"
  },
  "upload_info": {
    "upload_url": "https://storage.googleapis.com/...",
    "upload_method": "PUT",
    "required_headers": {
      "x-goog-content-length-range": "0,1048576000"
    }
  }
}
```

### Step 2: Upload Image

```bash
curl -X PUT "UPLOAD_URL" \
  -H "Content-Type: image/jpeg" \
  -H "x-goog-content-length-range: 0,1048576000" \
  --data-binary @landscape.jpg
```

### Step 3: Generate World

```bash
curl -X POST "https://api.worldlabs.ai/marble/v1/worlds:generate" \
  -H "WLT-Api-Key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "Marble 0.1-plus",
    "world_prompt": {
      "type": "image",
      "image_prompt": {
        "source": "media_asset",
        "media_asset_id": "550e8400-e29b-41d4-a716-446655440000"
      },
      "text_prompt": "A dramatic mountain landscape at sunset"
    }
  }'
```

## Python Example

```python
import requests

def upload_image_and_generate(image_path: str, api_key: str, prompt: str = None, is_pano: bool = False):
    base_url = "https://api.worldlabs.ai/marble/v1"
    headers = {"WLT-Api-Key": api_key, "Content-Type": "application/json"}

    # Get extension
    ext = image_path.lower().split('.')[-1]
    if ext == "jpeg":
        ext = "jpg"

    # Step 1: Prepare upload
    prep_response = requests.post(
        f"{base_url}/media-assets:prepare_upload",
        headers=headers,
        json={"file_name": image_path.split('/')[-1], "kind": "image", "extension": ext}
    )
    prep_data = prep_response.json()
    media_asset_id = prep_data["media_asset"]["media_asset_id"]
    upload_url = prep_data["upload_info"]["upload_url"]

    # Step 2: Upload image
    content_types = {"jpg": "image/jpeg", "png": "image/png", "webp": "image/webp"}
    with open(image_path, 'rb') as f:
        requests.put(
            upload_url,
            headers={"Content-Type": content_types.get(ext, "image/jpeg")},
            data=f.read()
        )

    # Step 3: Generate world
    image_prompt = {"source": "media_asset", "media_asset_id": media_asset_id}
    if is_pano:
        image_prompt["is_pano"] = True

    world_prompt = {"type": "image", "image_prompt": image_prompt}
    if prompt:
        world_prompt["text_prompt"] = prompt

    gen_response = requests.post(
        f"{base_url}/worlds:generate",
        headers=headers,
        json={"model": "Marble 0.1-plus", "world_prompt": world_prompt}
    )

    return gen_response.json()["operation_id"]

# Usage
operation_id = upload_image_and_generate(
    "mountain_vista.jpg",
    "your_api_key",
    "Add dramatic storm clouds and golden sunset light"
)
```

## Combining Text with Images

Text prompts guide interpretation and can transform the scene:

| Text Prompt               | Effect                                      |
| ------------------------- | ------------------------------------------- |
| None (omitted)            | Auto-caption generated, faithful recreation |
| "At sunset"               | Changes lighting/atmosphere                 |
| "In winter with snow"     | Adds seasonal elements                      |
| "Abandoned and overgrown" | Adds decay/nature reclaim                   |
| "Futuristic version"      | Sci-fi transformation                       |

When text is omitted, the model auto-generates a caption from the image.

## Troubleshooting

| Issue              | Solution                                                    |
| ------------------ | ----------------------------------------------------------- |
| Distorted geometry | Use image with clearer depth cues                           |
| Missing areas      | Provide image with more context/edges                       |
| Wrong scale        | Include recognizable objects for reference                  |
| Artifacts on faces | Avoid images with people as main subject                    |
| Billboard warping  | Objects far from center may warp; center important elements |

## Related Skills

- `world-labs-api` - API integration details
- `world-labs-text-prompt` - Text prompting best practices
- `world-labs-multi-image` - Using multiple images with direction control
- `world-labs-pano-video` - Panorama and video input
