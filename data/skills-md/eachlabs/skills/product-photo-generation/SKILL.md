---
name: Product Photo Generation
description: Generate professional product photography using each::sense API for e-commerce, marketing, and catalog imagery
metadata:
  category: image-generation
  api: each::sense
  modes: [max, eco]
  features: [product-shots, lifestyle-context, studio-lighting, white-background, multi-turn]
---

# Product Photo Generation

Generate professional product photography with the each::sense API. Create e-commerce ready images, lifestyle shots, and studio-quality product visuals for any item.

## Overview

The each::sense API enables generation of high-quality product photography suitable for:

- **E-commerce product shots** - Clean, professional images for online stores
- **Lifestyle context images** - Products shown in real-world settings
- **White background photography** - Standard catalog and marketplace images
- **Studio lighting setups** - Professional lighting for premium product presentation
- **Marketing visuals** - Eye-catching images for ads and promotions

You can also provide your own product images via `image_urls` to place your actual products into professionally styled scenes.

## Quick Start

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate a professional product photo of a minimalist ceramic coffee mug on a white background with soft studio lighting",
    "mode": "max"
  }'
```

## Product Photo Styles

| Style | Description | Best For |
|-------|-------------|----------|
| White Background | Clean, isolated product on pure white | E-commerce, marketplaces, catalogs |
| Lifestyle | Product in real-world context or environment | Social media, brand storytelling |
| Flat Lay | Top-down view with arranged props | Fashion, food, accessories |
| In-Context | Product being used or in its natural setting | Marketing campaigns, ads |
| Hero Shot | Dramatic lighting and angles for impact | Homepage banners, featured products |
| Detail Shot | Close-up focusing on texture and craftsmanship | Luxury goods, handmade items |

## Use Case Examples

### White Background Product Shot

Standard e-commerce product photography with clean white background.

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Professional product photo of a stainless steel water bottle on pure white background, centered composition, soft box lighting from above and sides, no shadows, e-commerce style, 4K quality",
    "mode": "max"
  }'
```

### Lifestyle Context Shot

Product shown in an aspirational real-world setting.

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Lifestyle product photography of premium wireless headphones on a modern wooden desk, morning light through window, MacBook and coffee cup in soft focus background, warm and inviting atmosphere",
    "mode": "max"
  }'
```

### Flat Lay Composition

Top-down arrangement with complementary props.

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Flat lay product photography of a leather wallet, arranged with sunglasses, car keys, and a fountain pen on marble surface, overhead shot, even lighting, editorial style composition",
    "mode": "max"
  }'
```

### Hero Shot with Dramatic Lighting

High-impact product image for marketing materials.

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Hero shot of a luxury perfume bottle, dramatic side lighting creating elegant shadows, dark moody background with subtle gradient, glass reflections and caustics, premium advertising quality",
    "mode": "max"
  }'
```

### Detail/Macro Shot

Close-up focusing on product texture and craftsmanship.

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Macro detail shot of handcrafted leather bag stitching, extreme close-up showing texture and quality of leather grain, shallow depth of field, warm directional lighting highlighting craftsmanship",
    "mode": "max"
  }'
```

### In-Use/Action Shot

Product being actively used or demonstrated.

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Action product shot of running shoes in motion, dynamic angle showing flexibility, slight motion blur on background, athletic track setting, energetic and sporty atmosphere",
    "mode": "max"
  }'
```

### Seasonal/Themed Shot

Product styled for specific season or holiday.

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Holiday themed product photo of a scented candle surrounded by pine branches, dried oranges, and cinnamon sticks, warm cozy lighting, festive winter atmosphere, gift-ready presentation",
    "mode": "max"
  }'
```

### Size Comparison Shot

Product shown with reference objects for scale.

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Product scale photo of a compact Bluetooth speaker next to a smartphone and coffee cup for size reference, clean white background, even lighting, showing portable dimensions clearly",
    "mode": "max"
  }'
```

### Packaging Shot

Product with its packaging for unboxing experience.

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Product and packaging photo of premium skincare bottle emerging from elegant black box, tissue paper visible, unboxing moment, luxury presentation, soft lighting on neutral background",
    "mode": "max"
  }'
```

## Using Your Own Product Images

Provide actual product photos via `image_urls` to place your products into professionally styled scenes.

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Place this product in a modern kitchen setting, morning light, marble countertop, lifestyle photography style",
    "image_urls": ["https://example.com/my-product.jpg"],
    "mode": "max"
  }'
```

### Product with Custom Background

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Put this product on a pure white background with professional studio lighting, remove existing background, e-commerce ready",
    "image_urls": ["https://example.com/raw-product-photo.jpg"],
    "mode": "max"
  }'
```

## Best Practices for Product Photography

### Lighting Guidelines

- **Soft box lighting** - Even illumination for e-commerce shots
- **Rim lighting** - Creates separation from background
- **Natural window light** - Warm, authentic lifestyle feel
- **Dramatic side lighting** - Adds depth and premium look
- **Diffused overhead** - Minimizes harsh shadows

### Composition Tips

- Center important products for e-commerce
- Use rule of thirds for lifestyle shots
- Leave negative space for text overlay
- Consider the platform aspect ratio requirements
- Include context elements that tell a story

### Background Selection

- Pure white (#FFFFFF) for marketplace requirements
- Gradient backgrounds for premium products
- Contextual environments for lifestyle appeal
- Complementary colors that enhance product
- Textured surfaces for artisanal products

## Prompt Tips

Effective prompts for product photography include:

**Lighting descriptors:**
- "soft box lighting", "natural window light", "dramatic side lighting"
- "rim light", "backlit", "diffused overhead lighting"
- "golden hour warmth", "cool studio lighting"

**Angle specifications:**
- "eye-level shot", "45-degree angle", "overhead flat lay"
- "low angle hero shot", "three-quarter view", "straight-on"

**Background details:**
- "pure white background", "gradient gray backdrop"
- "marble surface", "wooden table", "concrete texture"

**Style references:**
- "e-commerce style", "editorial quality", "magazine advertisement"
- "catalog photography", "Instagram aesthetic", "premium brand look"

**Props and context:**
- "minimalist props", "lifestyle elements", "seasonal decorations"
- "complementary accessories", "natural elements"

## Mode Selection

| Mode | Best For | Output Quality |
|------|----------|----------------|
| `max` | Hero shots, marketing materials, premium products | Highest quality, detailed rendering |
| `eco` | Quick iterations, bulk catalog photos, testing concepts | Fast generation, good quality |

Use `max` mode for final marketing assets and hero images. Use `eco` mode for rapid prototyping and generating multiple variations quickly.

## Multi-Turn Sessions for Product Series

Use `session_id` to maintain consistency across a product line or catalog series.

### Start a product series session

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate a product photo of a blue ceramic coffee mug on white background with soft natural lighting, minimalist style",
    "session_id": "product-catalog-2024",
    "mode": "max"
  }'
```

### Continue with consistent style

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Now generate the matching red ceramic mug in the same style and lighting setup",
    "session_id": "product-catalog-2024",
    "mode": "max"
  }'
```

### Add variations

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a lifestyle version showing both mugs on a breakfast table with croissants",
    "session_id": "product-catalog-2024",
    "mode": "max"
  }'
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid or missing API key | Verify `X-API-Key` header is set correctly |
| 400 Bad Request | Malformed request body | Check JSON syntax and required fields |
| 429 Rate Limited | Too many requests | Implement exponential backoff |
| 500 Server Error | Service temporarily unavailable | Retry after a brief delay |

### Retry with exponential backoff

```bash
for i in 1 2 3; do
  response=$(curl -s -w "%{http_code}" -X POST "https://sense.eachlabs.run/chat" \
    -H "Content-Type: application/json" \
    -H "X-API-Key: $EACHLABS_API_KEY" \
    -H "Accept: text/event-stream" \
    -d '{
      "message": "Professional product photo of wireless earbuds on white background",
      "mode": "max"
    }')

  http_code="${response: -3}"
  if [ "$http_code" -eq 200 ]; then
    echo "${response%???}"
    break
  fi
  sleep $((2**i))
done
```

## Related Skills

- [Image Generation](/skills/image-generation) - General purpose image creation
- [Image Edit](/skills/image-edit) - Modify and enhance existing images
- [Fashion AI](/skills/fashion-ai) - Fashion-specific product photography
