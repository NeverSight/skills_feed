---
name: gemini-image
description: Generate images using AI when user wants to create pictures, draw, paint, or generate artwork. Supports text-to-image and image-to-image generation.
---

# Gemini Image Generation

Use this skill when user expresses intent to generate images (e.g., "draw a...", "generate an image...", "create a picture...").

## Steps

### 1. Read Configuration
- Read `config/secrets.md` to get API Key

### 2. Construct Prompt

| Mode | Prompt Format | Example |
|------|---------------|---------|
| Text-to-Image | `description text` | `a cute orange cat` |
| Image-to-Image | `image_URL description` | `https://xxx.jpg draw similar style` |
| Multi-Image Reference | `URL1 URL2 description` | `https://a.jpg https://b.jpg merge these two` |

For image-to-image, upload local images first. See `tips/image-upload.md`.

### 3. Call API

```bash
curl -s -X POST "https://api.apicore.ai/v1/images/generations" \
  -H "Authorization: Bearer API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "model_name",
    "prompt": "prompt_text",
    "size": "aspect_ratio",
    "n": 1
  }'
```

### 4. Return Result

Extract `data[0].url` from response and return to user.

## Reference Docs

- `tips/image-upload.md` - Image upload methods
- `tips/chinese-text.md` - Chinese text handling tips
