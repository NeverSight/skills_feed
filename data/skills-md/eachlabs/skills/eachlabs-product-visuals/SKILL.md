---
name: eachlabs-product-visuals
description: Generate professional e-commerce product photography and videos using EachLabs AI models. Product shots, background replacement, lifestyle scenes, and 360-degree views. Use when the user needs product images for e-commerce or marketing.
metadata:
  author: eachlabs
  version: "1.0"
---

# EachLabs Product Visuals

Generate professional product photography, e-commerce visuals, and product videos using EachLabs AI models.

## Authentication

```
Header: X-API-Key: <your-api-key>
```

Set the `EACHLABS_API_KEY` environment variable. Get your key at [eachlabs.ai](https://eachlabs.ai).

## Recommended Models

### E-Commerce Specific

| Task | Model | Slug |
|------|-------|------|
| Product photoshoot | Product to Photoshoot | `product-to-photoshoot` |
| Product on model | Product Photo to Modelshoot | `product-photo-to-modelshoot` |
| Color variations | Product Colors | `product-colors` |
| Food photography | Food Photos | `food-photos` |
| Background removal | Product Background Remover | `product-backround-remover` |
| Image upscaling | Product Photo Upscaler | `product-photo-upscaler` |
| Home scene placement | Product Home View | `product-home-view` |
| Product shot | Bria Product Shot | `bria-product-shot` |
| Product shoot | Product Shoot | `product-shoot` |
| Product arc shot | Eachlabs Product Arc Shot | `eachlabs-product-arc-shot-v1` |
| Product zoom in | Eachlabs Product Zoom In | `eachlabs-product-zoom-in-v1` |

### General Purpose

| Task | Model | Slug |
|------|-------|------|
| Product photography | GPT Image v1.5 | `gpt-image-v1-5-text-to-image` |
| Background replacement | GPT Image v1.5 Edit | `gpt-image-v1-5-edit` |
| Product editing | Flux 2 Turbo Edit | `flux-2-turbo-edit` |
| Multi-angle views | Qwen Image Edit | `qwen-image-edit-2511-multiple-angles` |
| Background removal | Rembg Enhance | `rembg-enhance` |
| Background removal | Eachlabs BG Remover | `eachlabs-bg-remover-v1` |
| Image upscaling | Eachlabs Upscaler Pro | `eachlabs-image-upscaler-pro-v1` |
| Ad inpainting | SDXL Ad Inpaint | `sdxl-ad-inpaint` |
| Custom product style | Z Image Trainer | `z-image-trainer` |
| Product video | Pixverse v5.6 Image-to-Video | `pixverse-v5-6-image-to-video` |

## Prediction Flow

1. **Check model** `GET https://api.eachlabs.ai/v1/model?slug=<slug>` — validates the model exists and returns the `request_schema` with exact input parameters. Always do this before creating a prediction to ensure correct inputs.
2. **POST** `https://api.eachlabs.ai/v1/prediction` with model slug, version `"0.0.1"`, and input matching the schema
3. **Poll** `GET https://api.eachlabs.ai/v1/prediction/{id}` until status is `"success"` or `"failed"`
4. **Extract** output URL from response

## Workflows

### Product on White Background

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "gpt-image-v1-5-edit",
    "version": "0.0.1",
    "input": {
      "prompt": "Place this product on a clean white background with soft studio lighting and subtle shadows",
      "image_urls": ["https://example.com/product.jpg"],
      "background": "opaque",
      "quality": "high"
    }
  }'
```

### Lifestyle Scene Generation

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "gpt-image-v1-5-edit",
    "version": "0.0.1",
    "input": {
      "prompt": "Place this coffee mug on a cozy wooden desk in a modern home office with warm morning light, lifestyle photography",
      "image_urls": ["https://example.com/mug.jpg"],
      "quality": "high"
    }
  }'
```

### Multi-Angle Product Views

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "qwen-image-edit-2511-multiple-angles",
    "version": "0.0.1",
    "input": {
      "image_urls": ["https://example.com/product.jpg"],
      "horizontal_angle": 45,
      "vertical_angle": 15,
      "zoom": 5
    }
  }'
```

Generate multiple angles by running separate predictions with different `horizontal_angle` values (0, 45, 90, 135, 180, 225, 270, 315 for a full 360).

### Product with Transparent Background

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "gpt-image-v1-5-edit",
    "version": "0.0.1",
    "input": {
      "prompt": "Remove the background from this product image",
      "image_urls": ["https://example.com/product.jpg"],
      "background": "transparent",
      "output_format": "png"
    }
  }'
```

### Product Video from Image

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "pixverse-v5-6-image-to-video",
    "version": "0.0.1",
    "input": {
      "image_url": "https://example.com/product-studio.jpg",
      "prompt": "Slow cinematic camera rotation around the product with dramatic studio lighting",
      "duration": "5",
      "resolution": "1080p"
    }
  }'
```

## Prompt Tips for Products

- Specify lighting: "soft studio lighting", "dramatic side lighting", "natural window light"
- Mention surface: "marble surface", "wooden table", "clean white background"
- Include shadows: "soft shadows", "reflection on surface"
- Add context: "lifestyle setting", "in-use shot", "flat lay arrangement"
- For batch catalog shots, maintain consistency with similar prompts

## Batch Processing

For catalog-scale processing, create multiple predictions in parallel by sending separate POST requests for each product. Poll each prediction independently.

## Parameter Reference

See the [eachlabs-image-generation](../eachlabs-image-generation/references/MODELS.md) and [eachlabs-video-generation](../eachlabs-video-generation/references/MODELS.md) references for complete model parameters.
