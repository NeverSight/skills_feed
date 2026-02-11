---
name: eachlabs-fashion-ai
description: Generate fashion model imagery, virtual try-on, runway videos, and campaign visuals using EachLabs AI. Use when the user needs fashion content, model photography, or virtual try-on.
metadata:
  author: eachlabs
  version: "1.0"
---

# EachLabs Fashion AI

Generate AI fashion model imagery, virtual try-on experiences, runway content, and campaign visuals using EachLabs models.

## Authentication

```
Header: X-API-Key: <your-api-key>
```

Set the `EACHLABS_API_KEY` environment variable. Get your key at [eachlabs.ai](https://eachlabs.ai).

## Recommended Models

### Image Generation & Editing

| Task | Model | Slug |
|------|-------|------|
| Fashion model generation | GPT Image v1.5 | `gpt-image-v1-5-text-to-image` |
| Virtual try-on (best) | Kolors Virtual Try-On | `kling-v1-5-kolors-virtual-try-on` |
| Virtual try-on (alt) | IDM VTON | `idm-vton` |
| Garment on model | Wan v2.6 Image-to-Image | `wan-v2-6-image-to-image` |
| Model photoshoot | Product Photo to Modelshoot | `product-photo-to-modelshoot` |
| Photoshoot styling | Nano Banana Pro Photoshoot | `nano-banana-pro-photoshoot` |
| Face/look consistency | Omni Zero | `omni-zero` |
| Character consistency | Ideogram Character | `ideogram-character` |
| Photomaker | Photomaker | `photomaker` |
| Photomaker Style | Photomaker Style | `photomaker-style` |
| Avatar generation | Instant ID | `instant-id` |
| Soul styling | Higgsfield AI Soul | `higgsfield-ai-soul` |
| Become image | Become Image | `become-image` |

### Training

| Task | Model | Slug |
|------|-------|------|
| Brand style training | Z Image Trainer | `z-image-trainer` |
| Portrait LoRA | Flux LoRA Portrait Trainer | `flux-lora-portrait-trainer` |

### Video

| Task | Model | Slug |
|------|-------|------|
| Runway video | Pixverse v5.6 Image-to-Video | `pixverse-v5-6-image-to-video` |
| Catwalk animation | Bytedance Omnihuman v1.5 | `bytedance-omnihuman-v1-5` |
| Motion reference | Kling v2.6 Pro Motion | `kling-v2-6-pro-motion-control` |

## Prediction Flow

1. **Check model** `GET https://api.eachlabs.ai/v1/model?slug=<slug>` — validates the model exists and returns the `request_schema` with exact input parameters. Always do this before creating a prediction to ensure correct inputs.
2. **POST** `https://api.eachlabs.ai/v1/prediction` with model slug, version `"0.0.1"`, and input matching the schema
3. **Poll** `GET https://api.eachlabs.ai/v1/prediction/{id}` until status is `"success"` or `"failed"`
4. **Extract** output URL from response

## Workflows

### AI Fashion Model Generation

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "gpt-image-v1-5-text-to-image",
    "version": "0.0.1",
    "input": {
      "prompt": "Professional fashion model wearing a tailored navy blazer, editorial photography, studio lighting, full body shot, neutral background",
      "image_size": "1024x1536",
      "quality": "high"
    }
  }'
```

### Virtual Try-On

Combine a garment image with a model image:

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "wan-v2-6-image-to-image",
    "version": "0.0.1",
    "input": {
      "prompt": "The person in image 1 wearing the clothing from image 2, professional fashion photography, editorial style",
      "image_urls": ["https://example.com/model.jpg", "https://example.com/garment.jpg"],
      "image_size": "portrait_4_3"
    }
  }'
```

### Runway / Catwalk Video

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "pixverse-v5-6-image-to-video",
    "version": "0.0.1",
    "input": {
      "image_url": "https://example.com/fashion-model.jpg",
      "prompt": "Fashion model walking confidently on a runway, camera follows from front, professional fashion show lighting",
      "duration": "5",
      "resolution": "1080p"
    }
  }'
```

### Catwalk with Motion Reference

Use a real runway walk as motion reference:

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "kling-v2-6-pro-motion-control",
    "version": "0.0.1",
    "input": {
      "image_url": "https://example.com/fashion-model.jpg",
      "video_url": "https://example.com/runway-walk-reference.mp4",
      "character_orientation": "video"
    }
  }'
```

### Brand Style Training

Train a LoRA on your brand's visual style for consistent campaign imagery:

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "z-image-trainer",
    "version": "0.0.1",
    "input": {
      "image_data_url": "https://example.com/brand-photos.zip",
      "default_caption": "brand editorial fashion photography style",
      "training_type": "style",
      "steps": 1500
    }
  }'
```

## Prompt Tips for Fashion

- Specify pose: "full body shot", "half body", "close-up on garment details"
- Include lighting: "editorial studio lighting", "natural light", "dramatic side lighting"
- Mention style: "editorial", "street style", "haute couture", "casual lookbook"
- For diversity: specify body types, skin tones, and ages in prompts
- For consistency: use the same style keywords across a campaign series

## Parameter Reference

See the [eachlabs-image-generation](../eachlabs-image-generation/references/MODELS.md) and [eachlabs-video-generation](../eachlabs-video-generation/references/MODELS.md) references for complete model parameters.
