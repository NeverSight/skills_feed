---
name: eachlabs-face-swap
description: Swap faces between images using EachLabs AI. Use when the user wants to replace or swap faces in photos.
metadata:
  author: eachlabs
  version: "1.0"
---

# EachLabs Face Swap

Swap faces between images and videos using the EachLabs Predictions API.

## Authentication

```
Header: X-API-Key: <your-api-key>
```

Set the `EACHLABS_API_KEY` environment variable. Get your key at [eachlabs.ai](https://eachlabs.ai).

## Available Models

| Model | Slug | Best For |
|-------|------|----------|
| AI Face Swap V1 | `aifaceswap-face-swap` | Image face swap |
| Eachlabs Face Swap | `each-faceswap-v1` | Image face swap |
| Face Swap (legacy) | `face-swap-new` | Image face swap |
| Faceswap Video | `faceswap-video` | Video face swap |

## Examples

### Image Face Swap with AI Face Swap V1

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "aifaceswap-face-swap",
    "version": "0.0.1",
    "input": {
      "target_image": "https://example.com/target-photo.jpg",
      "swap_image": "https://example.com/source-face.jpg"
    }
  }'
```

### Image Face Swap with Eachlabs

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "each-faceswap-v1",
    "version": "0.0.1",
    "input": {
      "target_image": "https://example.com/target-photo.jpg",
      "swap_image": "https://example.com/source-face.jpg"
    }
  }'
```

### Video Face Swap

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "faceswap-video",
    "version": "0.0.1",
    "input": {
      "target_video": "https://example.com/target-video.mp4",
      "swap_image": "https://example.com/source-face.jpg"
    }
  }'
```

### Alternative: Using GPT Image v1.5 Edit

For prompt-based face replacement:

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "gpt-image-v1-5-edit",
    "version": "0.0.1",
    "input": {
      "prompt": "Replace the face in image 1 with the face from image 2. Keep the same pose, lighting, and expression. Maintain natural skin tone and seamless blending.",
      "image_urls": [
        "https://example.com/target-photo.jpg",
        "https://example.com/source-face.jpg"
      ],
      "quality": "high"
    }
  }'
```

## Prediction Flow

1. **Check model** `GET https://api.eachlabs.ai/v1/model?slug=<slug>` — validates the model exists and returns the `request_schema` with exact input parameters. Always do this before creating a prediction to ensure correct inputs.
2. **POST** `https://api.eachlabs.ai/v1/prediction` with model slug, version `"0.0.1"`, and input matching the schema
3. **Poll** `GET https://api.eachlabs.ai/v1/prediction/{id}` until status is `"success"` or `"failed"`
4. **Extract** the output image URL from the response

## Tips for Best Results

- Use high-quality source images with clear, well-lit faces
- The source face image should be a clear frontal or near-frontal portrait
- Matching lighting conditions between source and target produces more natural results
- Specify "seamless blending" and "natural skin tone" in prompts
- For the target image, faces should be clearly visible and not heavily occluded
