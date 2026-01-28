---
name: world-labs-multi-image
description: Multi-image input with direction control and auto layout for world generation
allowed-tools:
  - Bash
  - WebFetch
---

# World Labs Multi-Image Input

Generate 3D worlds from multiple reference images with precise directional control or automatic layout.

## Quick Reference

| Mode                  | Images  | Overlap                   | Best For                           |
| --------------------- | ------- | ------------------------- | ---------------------------------- |
| **Direction Control** | Up to 4 | Non-overlapping preferred | Creative connections between views |
| **Auto Layout**       | Up to 8 | Required                  | Reconstructing existing spaces     |

### Credits

| Model           | Credits |
| --------------- | ------- |
| Marble 0.1-plus | 1,600   |
| Marble 0.1-mini | 250     |

## Direction Control Mode

Use when you want explicit control over image placement. **Non-overlapping images** are preferred—the model creatively fills spaces between views.

### Azimuth Angles

| Azimuth | Direction | Description                         |
| ------- | --------- | ----------------------------------- |
| `0`     | Front     | Primary view, camera facing forward |
| `90`    | Right     | View from right side                |
| `180`   | Back      | Opposite of front view              |
| `270`   | Left      | View from left side                 |

Any value 0-360 is supported for non-cardinal directions.

### Visual Reference

```
              0° (Front)
                  ↑
                  |
    270° (Left) ←─┼─→ 90° (Right)
                  |
                  ↓
            180° (Back)
```

### API Usage (Direction Control)

```json
{
  "model": "Marble 0.1-plus",
  "world_prompt": {
    "type": "multi-image",
    "multi_image_prompt": [
      {
        "azimuth": 0,
        "content": {
          "source": "media_asset",
          "media_asset_id": "front_image_id"
        }
      },
      {
        "azimuth": 90,
        "content": {
          "source": "media_asset",
          "media_asset_id": "right_image_id"
        }
      },
      {
        "azimuth": 180,
        "content": {
          "source": "media_asset",
          "media_asset_id": "back_image_id"
        }
      },
      {
        "azimuth": 270,
        "content": {
          "source": "media_asset",
          "media_asset_id": "left_image_id"
        }
      }
    ],
    "text_prompt": "A grand Victorian mansion interior"
  }
}
```

### Using Public URLs

```json
{
  "model": "Marble 0.1-plus",
  "world_prompt": {
    "type": "multi-image",
    "multi_image_prompt": [
      {
        "azimuth": 0,
        "content": {
          "source": "uri",
          "uri": "https://example.com/front.jpg"
        }
      },
      {
        "azimuth": 180,
        "content": {
          "source": "uri",
          "uri": "https://example.com/back.jpg"
        }
      }
    ],
    "text_prompt": "A cozy living room"
  }
}
```

### Best Practices for Direction Control

✅ **Non-overlapping images**: Model creatively fills gaps between views
✅ **Consistent style**: All images should match aesthetically
✅ **Same lighting**: Consistent light direction across all images
✅ **Complementary angles**: Choose angles that tell a complete story

## Auto Layout Mode

Use when you have multiple overlapping images from the same space. The model automatically positions images.

### Requirements for Auto Layout

| Requirement  | Details                                         |
| ------------ | ----------------------------------------------- |
| Aspect ratio | **All images MUST have identical aspect ratio** |
| Resolution   | **All images MUST have identical resolution**   |
| Location     | All images from the same space                  |
| Overlap      | Visual overlap between images required          |
| Lighting     | Consistent lighting and color temperature       |

### API Usage (Auto Layout)

Auto Layout is primarily a UI feature. In API, omit azimuth values:

```json
{
  "model": "Marble 0.1-plus",
  "world_prompt": {
    "type": "multi-image",
    "multi_image_prompt": [
      {
        "content": {
          "source": "media_asset",
          "media_asset_id": "image_1_id"
        }
      },
      {
        "content": {
          "source": "media_asset",
          "media_asset_id": "image_2_id"
        }
      },
      {
        "content": {
          "source": "media_asset",
          "media_asset_id": "image_3_id"
        }
      }
    ],
    "text_prompt": "A mystical forest clearing"
  }
}
```

## Python Example

```python
import requests

def generate_world_multi_image(
    api_key: str,
    images: list[dict],  # [{"path": "...", "azimuth": 0}, ...] or [{"path": "..."}]
    prompt: str = None
):
    base_url = "https://api.worldlabs.ai/marble/v1"
    headers = {"WLT-Api-Key": api_key, "Content-Type": "application/json"}

    multi_image_prompt = []

    for img in images:
        # Get extension
        ext = img["path"].lower().split('.')[-1]
        if ext == "jpeg":
            ext = "jpg"

        # Prepare upload
        prep = requests.post(
            f"{base_url}/media-assets:prepare_upload",
            headers=headers,
            json={"file_name": img["path"].split('/')[-1], "kind": "image", "extension": ext}
        ).json()

        media_asset_id = prep["media_asset"]["media_asset_id"]
        upload_url = prep["upload_info"]["upload_url"]

        # Upload file
        content_types = {"jpg": "image/jpeg", "png": "image/png", "webp": "image/webp"}
        with open(img["path"], 'rb') as f:
            requests.put(upload_url, headers={"Content-Type": content_types.get(ext, "image/jpeg")}, data=f.read())

        # Build image reference
        image_entry = {
            "content": {
                "source": "media_asset",
                "media_asset_id": media_asset_id
            }
        }
        if "azimuth" in img:
            image_entry["azimuth"] = img["azimuth"]

        multi_image_prompt.append(image_entry)

    # Build world_prompt
    world_prompt = {
        "type": "multi-image",
        "multi_image_prompt": multi_image_prompt
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

# Usage with direction control
operation_id = generate_world_multi_image(
    "your_api_key",
    [
        {"path": "front_view.jpg", "azimuth": 0},
        {"path": "right_view.jpg", "azimuth": 90},
        {"path": "back_view.jpg", "azimuth": 180},
        {"path": "left_view.jpg", "azimuth": 270},
    ],
    prompt="A cozy cabin interior"
)

# Usage with auto layout (no azimuth)
operation_id = generate_world_multi_image(
    "your_api_key",
    [{"path": f"ref_{i}.jpg"} for i in range(6)],
    prompt="An enchanted garden"
)
```

## Common Use Cases

### Interior Room (4 corners)

```json
{
  "world_prompt": {
    "type": "multi-image",
    "multi_image_prompt": [
      {
        "azimuth": 45,
        "content": { "source": "media_asset", "media_asset_id": "corner_1" }
      },
      {
        "azimuth": 135,
        "content": { "source": "media_asset", "media_asset_id": "corner_2" }
      },
      {
        "azimuth": 225,
        "content": { "source": "media_asset", "media_asset_id": "corner_3" }
      },
      {
        "azimuth": 315,
        "content": { "source": "media_asset", "media_asset_id": "corner_4" }
      }
    ]
  }
}
```

### Street Scene (looking both ways)

```json
{
  "world_prompt": {
    "type": "multi-image",
    "multi_image_prompt": [
      {
        "azimuth": 0,
        "content": { "source": "media_asset", "media_asset_id": "street_north" }
      },
      {
        "azimuth": 180,
        "content": { "source": "media_asset", "media_asset_id": "street_south" }
      }
    ]
  }
}
```

## Comparison: Direction Control vs Auto Layout

| Aspect       | Direction Control         | Auto Layout          |
| ------------ | ------------------------- | -------------------- |
| Max images   | 4                         | 8                    |
| Overlap      | Non-overlapping preferred | Required             |
| Aspect ratio | Can vary                  | Must be identical    |
| Resolution   | Can vary                  | Must be identical    |
| Same space   | Recommended               | Required             |
| Use case     | Creative connections      | Space reconstruction |

## Troubleshooting

| Issue               | Cause                   | Solution                                    |
| ------------------- | ----------------------- | ------------------------------------------- |
| Seams between views | Inconsistent lighting   | Match exposure and white balance            |
| Floating objects    | Conflicting depth info  | Use more consistent reference images        |
| Distorted geometry  | Images too different    | Use more similar reference images           |
| Auto layout fails   | Different aspect ratios | Ensure all images have identical dimensions |

## Related Skills

- `world-labs-api` - API integration details
- `world-labs-image-prompt` - Single image input
- `world-labs-pano-video` - Panorama and video input (most control)
