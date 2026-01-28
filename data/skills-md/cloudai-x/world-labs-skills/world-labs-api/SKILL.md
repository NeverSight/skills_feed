---
name: world-labs-api
description: World Labs Marble API integration - authentication, endpoints, models, and media uploads
allowed-tools:
  - Bash
  - WebFetch
---

# World Labs Marble API Integration

## Authentication

All API requests require the `WLT-Api-Key` header:

```bash
curl -X POST "https://api.worldlabs.ai/marble/v1/worlds:generate" \
  -H "WLT-Api-Key: YOUR_API_KEY" \
  -H "Content-Type: application/json"
```

Get your API key from: <https://platform.worldlabs.ai>

**Note**: API credits purchased at platform.worldlabs.ai are separate from Marble app (marble.worldlabs.ai) credits.

## Base URL

```
https://api.worldlabs.ai/marble/v1
```

## Models

| Model           | ID                | Best For                            |
| --------------- | ----------------- | ----------------------------------- |
| Marble 0.1-plus | `Marble 0.1-plus` | High-quality production (~5 min)    |
| Marble 0.1-mini | `Marble 0.1-mini` | Quick drafts/iteration (~30-45 sec) |

### Credits by Input Type

| Input Type       | Marble 0.1-plus | Marble 0.1-mini |
| ---------------- | --------------- | --------------- |
| Panorama image   | 1,500           | 150             |
| Text             | 1,580           | 230             |
| Image (non-pano) | 1,580           | 230             |
| Multi-image      | 1,600           | 250             |
| Video            | 1,600           | 250             |

**Pricing**: $1 = 1,250 credits (minimum purchase: $5 / 6,250 credits)

## Core Endpoints

### Generate World

```http
POST /marble/v1/worlds:generate
```

**Request Body (Text Prompt):**

```json
{
  "display_name": "My World",
  "model": "Marble 0.1-plus",
  "world_prompt": {
    "type": "text",
    "text_prompt": "A cozy cabin in snowy mountains at sunset",
    "disable_recaption": false
  },
  "seed": 42,
  "tags": ["landscape", "winter"],
  "permission": {
    "public": false
  }
}
```

**Response:**

```json
{
  "done": false,
  "operation_id": "op_abc123",
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-01T12:00:00Z",
  "metadata": {}
}
```

### Poll Operation Status

```http
GET /marble/v1/operations/{operation_id}
```

**Response (in progress):**

```json
{
  "done": false,
  "operation_id": "op_abc123",
  "metadata": {
    "world_id": "world_xyz789"
  }
}
```

**Response (complete):**

```json
{
  "done": true,
  "operation_id": "op_abc123",
  "response": {
    "world_id": "world_xyz789",
    "display_name": "My World",
    "world_marble_url": "https://marble.worldlabs.ai/world/...",
    "assets": {
      "thumbnail_url": "...",
      "imagery": { "pano_url": "..." },
      "mesh": { "collider_mesh_url": "..." },
      "splats": { "spz_urls": {} }
    }
  }
}
```

### Get World

```http
GET /marble/v1/worlds/{world_id}
```

Returns full world object with assets.

### List Worlds

```http
POST /marble/v1/worlds:list
```

```json
{
  "page_size": 20,
  "status": "SUCCEEDED",
  "model": "Marble 0.1-plus",
  "sort_by": "created_at"
}
```

## Media Asset Upload Workflow

### Step 1: Prepare Upload

```http
POST /marble/v1/media-assets:prepare_upload
```

```json
{
  "file_name": "landscape.jpg",
  "kind": "image",
  "extension": "jpg"
}
```

**Response:**

```json
{
  "media_asset": {
    "media_asset_id": "550e8400-e29b-41d4-a716-446655440000",
    "file_name": "landscape.jpg",
    "kind": "image",
    "extension": "jpg"
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

### Step 2: Upload File

```bash
curl -X PUT "UPLOAD_URL" \
  -H "Content-Type: image/jpeg" \
  -H "x-goog-content-length-range: 0,1048576000" \
  --data-binary @landscape.jpg
```

### Step 3: Use in Generation

**Single Image:**

```json
{
  "model": "Marble 0.1-plus",
  "world_prompt": {
    "type": "image",
    "image_prompt": {
      "source": "media_asset",
      "media_asset_id": "550e8400-e29b-41d4-a716-446655440000"
    },
    "text_prompt": "Enhance with dramatic lighting"
  }
}
```

**Panorama Image (use `is_pano` flag):**

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

**Multi-Image with Azimuth:**

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
        "azimuth": 180,
        "content": {
          "source": "media_asset",
          "media_asset_id": "back_image_id"
        }
      }
    ],
    "text_prompt": "A cozy living room"
  }
}
```

**Video:**

```json
{
  "model": "Marble 0.1-plus",
  "world_prompt": {
    "type": "video",
    "video_prompt": {
      "source": "media_asset",
      "media_asset_id": "video_asset_id"
    },
    "text_prompt": "A scenic mountain landscape"
  }
}
```

## File Requirements

| Type     | Formats              | Max Size | Notes                               |
| -------- | -------------------- | -------- | ----------------------------------- |
| Image    | png, jpg, jpeg, webp | 20 MB    | 1024px on long side recommended     |
| Panorama | png, jpg, jpeg, webp | 20 MB    | 2:1 aspect, 2560px wide recommended |
| Video    | mp4, mov, webm       | 100 MB   | Max 30 seconds                      |

## Python Example

```python
import requests
import time

API_KEY = "your_api_key"
BASE_URL = "https://api.worldlabs.ai/marble/v1"

def generate_world(prompt: str, model: str = "Marble 0.1-plus") -> dict:
    """Generate a world and return the world data."""
    headers = {"WLT-Api-Key": API_KEY, "Content-Type": "application/json"}

    # Start generation
    response = requests.post(
        f"{BASE_URL}/worlds:generate",
        headers=headers,
        json={
            "model": model,
            "world_prompt": {
                "type": "text",
                "text_prompt": prompt
            }
        }
    )
    response.raise_for_status()
    operation_id = response.json()["operation_id"]

    # Poll until complete
    while True:
        status_response = requests.get(
            f"{BASE_URL}/operations/{operation_id}",
            headers={"WLT-Api-Key": API_KEY}
        )
        status_response.raise_for_status()
        result = status_response.json()

        if result.get("done"):
            if "error" in result and result["error"]:
                raise Exception(f"Generation failed: {result['error']}")
            return result["response"]

        time.sleep(5)

# Usage
world = generate_world("A mystical forest with glowing mushrooms")
print(f"World created: {world['world_id']}")
print(f"View at: {world['world_marble_url']}")
```

## Error Handling

| Status Code | Meaning                    |
| ----------- | -------------------------- |
| 400         | Invalid request parameters |
| 401         | Invalid or missing API key |
| 402         | Insufficient credits       |
| 429         | Rate limit exceeded        |
| 500         | Server error               |

## Rate Limits

- ~6 world generation requests per minute (rolling window)
- 429 error returned when exceeded; retry after limit resets

## Related Skills

- `world-labs-text-prompt` - Text prompting best practices
- `world-labs-image-prompt` - Single image input
- `world-labs-multi-image` - Multi-image direction control
- `world-labs-pano-video` - Panorama and video input
- `world-labs-export` - Export formats and integrations
