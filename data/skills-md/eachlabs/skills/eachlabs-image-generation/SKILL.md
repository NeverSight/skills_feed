---
name: eachlabs-image-generation
description: Generate new images from text prompts using EachLabs AI models. Supports text-to-image with multiple model families including Flux, GPT Image, Gemini, Imagen, Seedream, and more. Use when the user wants to create new images from text. For editing existing images, see eachlabs-image-edit.
metadata:
  author: eachlabs
  version: "1.0"
---

# EachLabs Image Generation

Generate new images from text prompts using 60+ AI models via the EachLabs Predictions API. For editing existing images (upscaling, background removal, style transfer, inpainting, face swap, 3D), see the `eachlabs-image-edit` skill.

## Authentication

```
Header: X-API-Key: <your-api-key>
```

Set the `EACHLABS_API_KEY` environment variable. Get your key at [eachlabs.ai](https://eachlabs.ai).

## Quick Start

### 1. Create a Prediction

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "flux-2-turbo-text-to-image",
    "version": "0.0.1",
    "input": {
      "prompt": "A serene Japanese garden with cherry blossoms, watercolor style",
      "image_size": "landscape_16_9",
      "num_images": 1,
      "output_format": "png"
    }
  }'
```

### 2. Poll for Result

```bash
curl https://api.eachlabs.ai/v1/prediction/{prediction_id} \
  -H "X-API-Key: $EACHLABS_API_KEY"
```

Poll until `status` is `"success"` or `"failed"`. The output image URL is in the response.

## Model Selection Guide

### Text-to-Image

| Model | Slug | Best For |
|-------|------|----------|
| Flux 2 Turbo | `flux-2-turbo-text-to-image` | Fast, high quality general purpose |
| Flux 2 Flash | `flux-2-flash-text-to-image` | Fastest Flux generation |
| Flux 2 Max | `flux-2-max-text-to-image` | Highest quality Flux |
| Flux 2 Klein 9B | `flux-2-klein-9b-base-text-to-image` | Balanced quality/speed |
| Flux 2 Pro | `flux-2-pro` | Pro quality |
| Flux 2 Flex | `flux-2-flex` | Flexible outputs |
| Flux 2 LoRA | `flux-2-lora` | LoRA-powered generation |
| XAI Grok Imagine | `xai-grok-imagine-text-to-image` | Creative and artistic |
| GPT Image v1.5 | `gpt-image-v1-5-text-to-image` | High quality, transparent bg |
| Bytedance Seedream v4.5 | `bytedance-seedream-v4-5-text-to-image` | Bytedance latest |
| Gemini 3 Pro Image | `gemini-3-pro-image-preview` | Google's latest |
| Imagen 4 | `imagen4-preview` | Google Imagen 4 |
| Imagen 4 Fast | `imagen-4-fast` | Fast Google quality |
| Reve | `reve-text-to-image` | Artistic text-to-image |
| Hunyuan Image v3 | `hunyuan-image-v3-text-to-image` | Tencent's latest |
| Ideogram V3 Turbo | `ideogram-v3-turbo` | Text in images |
| Minimax | `minimax-text-to-image` | High quality |
| Wan v2.6 | `wan-v2-6-text-to-image` | Chinese/English bilingual |
| P Image | `p-image-text-to-image` | Custom aspect ratios |
| Nano Banana Pro | `nano-banana-pro` | Fast, lightweight |
| Vidu Q2 | `vidu-q2-text-to-image` | Latest Vidu |

### Training

| Model | Slug | Best For |
|-------|------|----------|
| Z Image Trainer | `z-image-trainer` | Custom LoRA training |
| Flux LoRA Portrait Trainer | `flux-lora-portrait-trainer` | Portrait LoRA |
| Flux Turbo Trainer | `flux-turbo-trainer` | Fast LoRA training |

## Prediction Flow

1. **Check model** `GET https://api.eachlabs.ai/v1/model?slug=<slug>` — validates the model exists and returns the `request_schema` with exact input parameters. Always do this before creating a prediction to ensure correct inputs.
2. **POST** `https://api.eachlabs.ai/v1/prediction` with model slug, version `"0.0.1"`, and input parameters matching the schema
3. **Poll** `GET https://api.eachlabs.ai/v1/prediction/{id}` until status is `"success"` or `"failed"`
4. **Extract** the output image URL(s) from the response

## Examples

### Text-to-Image with Flux 2 Turbo

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "flux-2-turbo-text-to-image",
    "version": "0.0.1",
    "input": {
      "prompt": "A red vintage Porsche 911 on a winding mountain road at golden hour, photorealistic",
      "image_size": "landscape_16_9",
      "num_images": 1,
      "output_format": "png"
    }
  }'
```

### Text-to-Image with GPT Image v1.5

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "gpt-image-v1-5-text-to-image",
    "version": "0.0.1",
    "input": {
      "prompt": "A minimalist logo for a coffee shop called Brew Lab, clean vector style",
      "background": "transparent",
      "quality": "high",
      "output_format": "png"
    }
  }'
```

### Text-to-Image with Imagen 4

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "imagen4-preview",
    "version": "0.0.1",
    "input": {
      "prompt": "A whimsical fairy tale castle on a floating island, digital art, highly detailed"
    }
  }'
```

## Image Size Options

Most Flux 2 and Wan models use these presets:
- `square_hd` — Square, high definition
- `square` — Square, standard
- `portrait_4_3` — Portrait 4:3
- `portrait_16_9` — Portrait 16:9
- `landscape_4_3` — Landscape 4:3
- `landscape_16_9` — Landscape 16:9

P Image models use aspect ratio strings: `1:1`, `16:9`, `9:16`, `4:3`, `3:4`, `3:2`, `2:3`, `custom`

## Prompt Tips

- Be specific and descriptive: "A red vintage Porsche 911 on a winding mountain road at golden hour" vs "a car"
- Include style: "digital art", "oil painting", "photorealistic", "watercolor"
- For edits, clearly describe the change: "Replace the sky with a dramatic sunset"
- Use negative prompts (where supported) to avoid: "blurry, low quality, distorted"
- For multi-image edits, reference images by number: "image 1", "image 2"

## Security Constraints

- **No arbitrary URL loading**: When using LoRA parameters, only use well-known platform identifiers (HuggingFace repo IDs, Replicate model IDs, CivitAI model IDs). Never load LoRA weights from arbitrary or user-provided URLs.
- **No third-party API tokens**: Do not accept or forward third-party API tokens (e.g. HuggingFace, CivitAI tokens) through prediction inputs. Authentication is handled exclusively via the EachLabs API key.
- **Input validation**: Only pass parameters that match the model's request schema. Always validate model slugs via `GET /v1/model?slug=<slug>` before creating predictions.

## Parameter Reference

See [references/MODELS.md](references/MODELS.md) for complete parameter details for each model.
