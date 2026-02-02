---
name: gemini-image
description: Generate images from text prompts using fal.ai Gemini 3 Pro. Use when the user asks to create, generate, or make an image from a text description. Supports multiple aspect ratios and resolutions up to 4K.
allowed-tools: Bash, Read, Write
---

# Gemini Image Generation

Generate high-quality images from text prompts using Google's Gemini 3 Pro model via fal.ai.

## Prerequisites

- `FAL_KEY` environment variable must be set (typically in `~/.zshrc`)

## API Endpoint

`POST https://fal.run/fal-ai/gemini-3-pro-image-preview`

## Parameters

### Required
- `prompt` (string): The text description of the image to generate

### Optional
| Parameter | Type | Default | Options |
|-----------|------|---------|---------|
| `num_images` | integer | 1 | 1-4 |
| `aspect_ratio` | string | "1:1" | "21:9", "16:9", "3:2", "4:3", "5:4", "1:1", "4:5", "3:4", "2:3", "9:16" |
| `output_format` | string | "png" | "jpeg", "png", "webp" |
| `resolution` | string | "1K" | "1K", "2K", "4K" |
| `sync_mode` | boolean | false | Returns data URI when true |
| `enable_web_search` | boolean | false | Uses current web data for generation |
| `limit_generations` | boolean | false | Restricts to 1 image per prompt round |

## Usage

### cURL
```bash
curl --request POST \
  --url https://fal.run/fal-ai/gemini-3-pro-image-preview \
  --header "Authorization: Key $FAL_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "prompt": "A serene mountain landscape at sunset with golden light",
    "num_images": 1,
    "aspect_ratio": "16:9",
    "resolution": "2K",
    "output_format": "png"
  }'
```

### Python
```python
import fal_client

result = fal_client.subscribe(
    "fal-ai/gemini-3-pro-image-preview",
    arguments={
        "prompt": "A serene mountain landscape at sunset with golden light",
        "num_images": 1,
        "aspect_ratio": "16:9",
        "resolution": "2K"
    }
)

# Access the generated image URL
image_url = result["images"][0]["url"]
print(f"Generated image: {image_url}")
```

### JavaScript
```javascript
import { fal } from "@fal-ai/client";

const result = await fal.subscribe("fal-ai/gemini-3-pro-image-preview", {
  input: {
    prompt: "A serene mountain landscape at sunset with golden light",
    num_images: 1,
    aspect_ratio: "16:9",
    resolution: "2K"
  }
});

console.log("Generated image:", result.images[0].url);
```

## Response Format

```json
{
  "images": [
    {
      "file_name": "generated_image.png",
      "content_type": "image/png",
      "url": "https://storage.googleapis.com/..."
    }
  ],
  "description": "A description of the generated image"
}
```

## Examples

1. **Simple image generation**:
   - Prompt: "Generate an image of a futuristic city at night"

2. **Specific aspect ratio**:
   - Prompt: "Create a portrait-oriented image of a forest path" with `aspect_ratio: "9:16"`

3. **High resolution**:
   - Prompt: "Generate a detailed 4K image of a coral reef" with `resolution: "4K"`

## Tips

- Be specific in your prompts for better results
- Include lighting, mood, and style descriptors
- Use appropriate aspect ratios for your use case (16:9 for landscapes, 9:16 for portraits)
- Higher resolution takes longer to generate

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `401 Unauthorized` | Invalid FAL_KEY | Verify key at fal.ai dashboard |
| `429 Too Many Requests` | Rate limit exceeded | Wait 60 seconds, retry |
| `400 Bad Request` | Invalid parameters | Check aspect_ratio, resolution values |
| `500 Server Error` | API temporary issue | Retry after 30 seconds |
| `Timeout` | Generation taking too long | Reduce resolution or simplify prompt |
