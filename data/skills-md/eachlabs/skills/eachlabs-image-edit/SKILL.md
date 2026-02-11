---
name: eachlabs-image-edit
description: Edit, transform, upscale, and enhance images using EachLabs AI models. Supports image editing, style transfer, background removal, upscaling, inpainting, face swap, virtual try-on, 3D generation, and image analysis. Use when the user wants to edit or transform existing images.
metadata:
  author: eachlabs
  version: "1.0"
---

# EachLabs Image Edit

Edit, transform, and enhance existing images using 130+ AI models via the EachLabs Predictions API.

## Authentication

```
Header: X-API-Key: <your-api-key>
```

Set the `EACHLABS_API_KEY` environment variable. Get your key at [eachlabs.ai](https://eachlabs.ai).

## Model Selection Guide

### General Image Editing

| Model | Slug | Best For |
|-------|------|----------|
| Flux 2 Turbo Edit | `flux-2-turbo-edit` | Fast high quality editing |
| Flux 2 Flash Edit | `flux-2-flash-edit` | Fastest editing |
| Flux 2 Max Edit | `flux-2-max-edit` | Highest quality editing |
| Flux 2 Pro Edit | `flux-2-pro-edit` | Pro quality editing |
| Flux 2 Flex Edit | `flux-2-flex-edit` | Flexible editing |
| Flux 2 Edit | `flux-2-edit` | Standard Flux editing |
| Flux 2 LoRA Edit | `flux-2-lora-edit` | LoRA-powered editing |
| XAI Grok Imagine Edit | `xai-grok-imagine-image-edit` | Creative edits |
| GPT Image v1.5 Edit | `gpt-image-v1-5-edit` | High quality (up to 10 images) |
| Bytedance Seedream v4.5 Edit | `bytedance-seedream-v4-5-edit` | Bytedance latest |
| Gemini 3 Pro Image Edit | `gemini-3-pro-image-preview-edit` | Google editing |
| Qwen Image Edit Plus | `qwen-image-edit-plus` | Advanced Qwen editing |
| Reve Fast Edit | `reve-fast-edit` | Fast artistic editing |
| Reve Edit | `reve-edit` | Artistic editing |
| Chrono Edit | `chrono-edit` | Temporal editing |
| Dream Omni 2 Edit | `dreamomni2-edit` | Dream editing |
| Kling O1 | `kling-o1` | Latest Kling editor |
| Seedream V4 Edit | `seedream-v4-edit` | Seedream editing |
| SeedEdit 3.0 | `seededit-3-0` | SeedEdit editing |
| Nano Banana Pro Edit | `nano-banana-pro-edit` | Lightweight editing |
| Nano Banana Edit | `nano-banana-edit` | Basic editing |

### Multi-Image Context Editing

| Model | Slug | Best For |
|-------|------|----------|
| Flux Kontext Max | `flux-kontext-max` | Best multi-image context |
| Flux Kontext Pro | `flux-kontext-pro` | Pro multi-image context |
| Flux Kontext Dev | `flux-kontext-dev` | Dev multi-image context |
| Multi Image Kontext Max | `multi-image-kontext-max` | Multi-image max |
| Multi Image Kontext Pro | `multi-image-kontext-pro` | Multi-image pro |
| Multi Image Kontext | `multi-image-kontext` | Multi-image base |
| Flux Kontext Dev LoRA | `flux-kontext-dev-lora` | LoRA context editing |
| P Image Edit | `p-image-edit` | Multi-image editing |
| Wan v2.6 I2I | `wan-v2-6-image-to-image` | Multi-image reference |

### Multi-Angle Views

| Model | Slug | Best For |
|-------|------|----------|
| Qwen Multi-Angle | `qwen-image-edit-2511-multiple-angles` | Camera angle views |
| Qwen Image Edit | `qwen-ai-image-edit` | Qwen editing |

### Upscaling & Enhancement

| Model | Slug | Best For |
|-------|------|----------|
| Topaz Image Upscale | `topaz-upscale-image` | Best quality upscale |
| Flux Vision Upscaler | `flux-vision-upscaler` | AI upscaling |
| Recraft Clarity Upscale | `recraft-clarity-upscale` | Clarity enhancement |
| CCSR Upscaler | `ccsr` | Detail restoration |
| Each Upscaler | `each-upscaler` | General upscaling |
| Eachlabs Pro Upscaler | `eachlabs-image-upscaler-pro-v1` | Pro upscaling |
| Real ESRGAN | `real-esrgan` | Face enhancement |
| Real ESRGAN A100 | `real-esrgan-a100` | Fast face enhancement |
| GFPGAN | `gfpgan` | Face restoration |
| Tencent Flux SRPO | `tencent-flux-srpo-image-to-image` | Super resolution |

### Background Removal & Inpainting

| Model | Slug | Best For |
|-------|------|----------|
| Rembg | `rembg` | Background removal |
| Rembg Enhance | `rembg-enhance` | Enhanced bg removal |
| Eachlabs BG Remover | `eachlabs-bg-remover-v1` | Background removal |
| Flux Fill Pro | `flux-fill-pro` | Inpainting |
| Stable Diffusion Inpainting | `stable-diffusion-inpainting` | Classic inpainting |
| Realistic Background | `realistic-background` | Background replacement |
| SDXL Ad Inpaint | `sdxl-ad-inpaint` | Ad background |
| Realistic Vision Inpainting | `realisitic-vision-v3-inpainting` | Realistic inpainting |

### Style Transfer & Effects

| Model | Slug | Best For |
|-------|------|----------|
| ByteDance Style Changer | `bytedance` | Style transfer |
| Nano Banana Pro Sketch | `nano-banana-pro-sketch` | Sketch conversion |
| Nano Banana Pro Comic | `nano-banana-pro-comic-art` | Comic art style |
| Nano Banana Pro Realism | `nano-banana-pro-realism` | Photo-realistic |
| Cartoonify | `cartoonify` | Cartoon style |
| Illusion Diffusion | `illusion-diffusion-hq` | Optical illusions |
| Fog Effect | `salih-girgin-fog-effect-image-to-image` | Fog effect |

### Post-Processing Effects

| Model | Slug | Best For |
|-------|------|----------|
| Post Processing Combine | `post-processing` | Combined effects |
| Vignette | `post-processing-vignette` | Vignette effect |
| Sharpen | `post-processing-sharpen` | Sharpening |
| Grain | `post-processing-grain` | Film grain |
| Color Correction | `post-processing-color-correction` | Color adjustment |
| Color Tint | `post-processing-color-tint` | Color tinting |
| Blur | `post-processing-blur` | Blur effect |
| Desaturate | `post-processing-desaturate` | Desaturation |
| Solarize | `post-processing-solarize` | Solarize effect |
| Dodge Burn | `post-processing-dodge-burn` | Dodge & burn |
| Chromatic Aberration | `post-processing-chromatic-aberration` | Chromatic aberration |
| Parabolize | `post-processing-parabolize` | Parabolize effect |

### Face & Portrait

| Model | Slug | Best For |
|-------|------|----------|
| AI Face Swap V1 | `aifaceswap-face-swap` | Face swap |
| Eachlabs Face Swap | `each-faceswap-v1` | Face swap |
| Face Swap | `face-swap-new` | Face swap |
| Face to Sticker | `face-to-sticker` | Sticker generation |
| Instant ID | `instant-id` | Avatar generation |
| Instant ID Anime | `instant-id-ip-adapter` | Anime avatar |
| Photomaker | `photomaker` | Photo composition |
| Photomaker Style | `photomaker-style` | Style composition |
| Omni Zero | `omni-zero` | Zero-shot identity |
| AI Face Aesthetics | `ai-face-aesthetics` | Face analysis |
| Baby Generator | `baby-generator` | Baby face generation |
| Hairstyle Changer | `change-haircut` | Change hairstyle |
| Couple Image Gen v2 | `couple-image-generation-v2` | Couple images |
| Become Image | `become-image` | Transform into style |
| Higgsfield AI Soul | `higgsfield-ai-soul` | Soul styling |

### Virtual Try-On & Fashion

| Model | Slug | Best For |
|-------|------|----------|
| Kolors Virtual Try-On | `kling-v1-5-kolors-virtual-try-on` | Best virtual try-on |
| IDM VTON | `idm-vton` | Virtual try-on |

### Image Reframing

| Model | Slug | Best For |
|-------|------|----------|
| Luma Photon Reframe | `luma-photon-reframe-image` | Image reframing |
| Luma Photon Flash Reframe | `luma-photon-flash-reframe-image` | Fast reframing |
| Luma Reframe Image | `reframe-image` | Dream Machine reframe |

### Reference-Based Generation

| Model | Slug | Best For |
|-------|------|----------|
| Vidu Q2 Reference | `vidu-q2-reference-to-image` | Reference-based |
| Minimax Subject Reference | `minimax-subject-reference` | Subject reference |
| Ideogram Character | `ideogram-character` | Character consistency |
| Flux Redux Dev | `flux-redux-dev` | Style reference |
| Flux Redux Schnell | `flux-redux-schnell` | Fast style reference |

### ControlNet & Depth

| Model | Slug | Best For |
|-------|------|----------|
| Flux Dev ControlNet | `flux-dev-controlnet` | Flux ControlNet |
| Flux Canny Pro | `flux-canny-pro` | Edge-guided |
| Flux Depth Pro | `flux-depth-pro` | Depth-guided |
| Flux Depth Dev | `flux-depth-dev` | Dev depth-guided |
| SDXL ControlNet | `sdxl-controlnet` | SDXL ControlNet |
| Z Image Turbo ControlNet | `z-image-turbo-controlnet` | Fast ControlNet |
| Z Image Turbo ControlNet LoRA | `z-image-turbo-controlnet-lora` | ControlNet + LoRA |
| Z Image Turbo I2I | `z-image-turbo-image-to-image` | Z Image transform |
| Z Image Turbo I2I LoRA | `z-image-turbo-image-to-image-lora` | Z Image + LoRA |

### 3D Generation

| Model | Slug | Best For |
|-------|------|----------|
| Hunyuan 3D V2.1 | `hunyuan-3d-v2-1` | Latest 3D generation |
| Hunyuan 3D V2 | `hunyuan-3d-v2` | 3D model generation |

### Image Analysis

| Model | Slug | Best For |
|-------|------|----------|
| Gemini 2.0 Flash Lite | `gemini-2-0-flash-lite` | Image understanding |
| NSFW Detection | `nsfw-image-detection` | Content moderation |
| Face Analyzer | `1019-face-analyzer` | Face analysis |
| BLIP-2 | `blip-2` | Image captioning |

### Product & E-Commerce

| Model | Slug | Best For |
|-------|------|----------|
| Bria Product Shot | `bria-product-shot` | Product photos |
| Product Shoot | `product-shoot` | Product shoot |
| Runway Gen4 Image | `runway-gen4-image` | Gen4 image editing |
| Eachlabs Image Generation | `eachlabs-image-generation` | Custom generation |
| Custom Image Gen v2 | `custom-image-generation-v2` | Custom generation |
| Action Figure Generator | `action-figure-generator` | Action figures |
| Reve Fast Remix | `reve-fast-remix` | Fast remix |
| Reve Remix | `reve-remix` | Remix editing |

## Prediction Flow

1. **Check model** `GET https://api.eachlabs.ai/v1/model?slug=<slug>` — validates the model exists and returns the `request_schema` with exact input parameters. Always do this before creating a prediction to ensure correct inputs.
2. **POST** `https://api.eachlabs.ai/v1/prediction` with model slug, version `"0.0.1"`, and input matching the schema
3. **Poll** `GET https://api.eachlabs.ai/v1/prediction/{id}` until status is `"success"` or `"failed"`
4. **Extract** the output image URL(s) from the response

## Examples

### Edit Image with Flux 2 Turbo

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "flux-2-turbo-edit",
    "version": "0.0.1",
    "input": {
      "prompt": "Change the background to a tropical beach at sunset",
      "image_urls": ["https://example.com/photo.jpg"],
      "image_size": "square_hd",
      "output_format": "png"
    }
  }'
```

### Remove Background

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "rembg-enhance",
    "version": "0.0.1",
    "input": {
      "image_url": "https://example.com/photo.jpg"
    }
  }'
```

### Upscale Image

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "topaz-upscale-image",
    "version": "0.0.1",
    "input": {
      "image_url": "https://example.com/low-res.jpg"
    }
  }'
```

### Multi-Angle View

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "qwen-image-edit-2511-multiple-angles",
    "version": "0.0.1",
    "input": {
      "image_urls": ["https://example.com/product.jpg"],
      "horizontal_angle": 90,
      "vertical_angle": 15,
      "zoom": 5
    }
  }'
```

### Virtual Try-On

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "kling-v1-5-kolors-virtual-try-on",
    "version": "0.0.1",
    "input": {
      "human_image": "https://example.com/person.jpg",
      "garment_image": "https://example.com/clothing.jpg"
    }
  }'
```

### Generate 3D Model

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "hunyuan-3d-v2-1",
    "version": "0.0.1",
    "input": {
      "image_url": "https://example.com/object.jpg"
    }
  }'
```

## Security Constraints

- **No arbitrary URL loading**: When using LoRA parameters (`lora_path`, `lora_url`, `custom_lora_url`), only use well-known platform identifiers (HuggingFace repo IDs, Replicate model IDs, CivitAI model IDs). Never load weights from arbitrary or user-provided URLs.
- **Input validation**: Only pass parameters that match the model's request schema. Always validate model slugs via `GET /v1/model?slug=<slug>` before creating predictions.

## Parameter Reference

See [references/MODELS.md](references/MODELS.md) for complete parameter details for each model.
