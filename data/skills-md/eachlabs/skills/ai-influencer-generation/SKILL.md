---
name: AI Influencer Generation
description: Generate consistent AI influencer personas and social media content using each::sense API
metadata:
  category: image-generation
  api: sense
  endpoint: https://sense.eachlabs.run/chat
  features:
    - consistent-persona
    - social-media-content
    - brand-collaborations
    - virtual-models
---

# AI Influencer Generation

Generate consistent AI influencer personas for social media content, brand collaborations, and virtual modeling using the each::sense API.

## Overview

The AI Influencer Generation skill enables you to create and maintain consistent virtual personas for:

- **Consistent AI Personas**: Generate a virtual influencer with consistent appearance across all content
- **Social Media Content**: Create Instagram posts, Stories, Reels thumbnails, TikTok content, and more
- **Brand Ambassadors**: Virtual spokespeople for product promotions and collaborations
- **Virtual Models**: AI-generated models for fashion, lifestyle, and commercial content

## Quick Start

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a portrait of a young female AI influencer with long dark wavy hair, warm brown eyes, natural makeup, wearing a casual white linen shirt. Soft golden hour lighting, neutral background. Professional photography style, Instagram aesthetic.",
    "mode": "max"
  }'
```

## Content Types

| Content Type | Description | Recommended Mode |
|--------------|-------------|------------------|
| Instagram Posts | Feed photos, lifestyle shots, portraits | max |
| Instagram Stories | Casual, behind-the-scenes moments | eco |
| Reels Thumbnails | Eye-catching cover images for video content | max |
| TikTok Content | Trend-focused visuals and thumbnails | eco |
| YouTube Thumbnails | High-quality preview images | max |
| Brand Collaborations | Product placements, sponsored content | max |
| Fashion/OOTD | Outfit of the day, style showcases | max |
| Travel Content | Location-based lifestyle photography | max |

## Use Case Examples

### 1. Create AI Influencer Persona (Initial Character)

Establish your AI influencer's base appearance for consistency across all future content.

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a detailed portrait of an AI influencer persona: A 25-year-old woman with shoulder-length auburn hair with subtle waves, bright green eyes, light freckles across her nose and cheeks, warm peachy skin tone. She has a friendly, approachable smile. Wearing minimal natural makeup. Clean white background, soft studio lighting. Ultra-realistic photography, 4K quality.",
    "session_id": "influencer-maya-2024",
    "mode": "max"
  }'
```

### 2. Instagram Lifestyle Post

Generate casual lifestyle content for the Instagram feed.

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate an Instagram lifestyle photo: A young woman with shoulder-length auburn wavy hair, green eyes, and light freckles. She is sitting at a cozy coffee shop, holding a ceramic latte cup, wearing an oversized cream knit sweater. Warm ambient lighting, bokeh background with fairy lights. Candid pose, genuine smile. Instagram aesthetic, lifestyle photography.",
    "session_id": "influencer-maya-2024",
    "mode": "max",
    "image_urls": ["https://example.com/maya-reference.jpg"]
  }'
```

### 3. Instagram Stories Content

Create casual, engaging Stories content.

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an Instagram Stories photo: Close-up selfie of a young woman with auburn wavy hair and green eyes, light freckles. She is making a playful expression, holding up a peace sign. Morning light from a window, casual bedroom setting. Wearing a simple white t-shirt. Authentic, unfiltered look. Vertical 9:16 aspect ratio.",
    "session_id": "influencer-maya-2024",
    "mode": "eco",
    "image_urls": ["https://example.com/maya-reference.jpg"]
  }'
```

### 4. Brand Collaboration Post

Generate sponsored content for brand partnerships.

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a brand collaboration photo: A young woman with auburn wavy hair, green eyes, and freckles. She is elegantly holding a luxury skincare product bottle close to her face. Clean, minimalist white studio background. Wearing a silk robe in blush pink. Soft beauty lighting, dewy skin appearance. Professional product photography style, aspirational aesthetic.",
    "session_id": "influencer-maya-2024",
    "mode": "max",
    "image_urls": ["https://example.com/maya-reference.jpg"]
  }'
```

### 5. Travel Content

Create wanderlust-inspiring travel photography.

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate travel influencer content: A young woman with auburn wavy hair, green eyes, and light freckles. She is standing on a scenic cliff overlooking the Santorini coastline, white and blue buildings in the background. Wearing a flowing white maxi dress, wind gently blowing her hair. Golden sunset lighting. Travel photography, wanderlust aesthetic, editorial quality.",
    "session_id": "influencer-maya-2024",
    "mode": "max",
    "image_urls": ["https://example.com/maya-reference.jpg"]
  }'
```

### 6. Fashion/OOTD Post

Showcase outfit of the day content.

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an OOTD fashion post: Full-body shot of a young woman with auburn wavy hair, green eyes, and freckles. She is posing confidently on an urban street. Wearing a tailored beige blazer, white crop top, high-waisted dark denim jeans, and white sneakers. Carrying a designer handbag. Natural daylight, city backdrop with blurred pedestrians. Street style photography, fashion editorial aesthetic.",
    "session_id": "influencer-maya-2024",
    "mode": "max",
    "image_urls": ["https://example.com/maya-reference.jpg"]
  }'
```

### 7. Fitness Content

Generate health and wellness focused imagery.

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create fitness influencer content: A young athletic woman with auburn hair in a high ponytail, green eyes, light freckles. She is doing a yoga pose on a mat in a bright, modern home gym. Wearing a matching sage green sports bra and leggings set. Morning sunlight streaming through large windows. Healthy glow, natural sweat. Fitness photography, wellness aesthetic.",
    "session_id": "influencer-maya-2024",
    "mode": "max",
    "image_urls": ["https://example.com/maya-reference.jpg"]
  }'
```

### 8. Product Promotion

Create compelling product showcase content.

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate product promotion content: Close-up of a young woman with auburn wavy hair, green eyes, and freckles. She is applying lip gloss while looking at camera with a slight smile. The product is clearly visible in frame. Soft ring light reflection in eyes, beauty studio setting. Pink and rose gold color palette. Beauty influencer aesthetic, product-focused composition.",
    "session_id": "influencer-maya-2024",
    "mode": "max",
    "image_urls": ["https://example.com/maya-reference.jpg"]
  }'
```

### 9. Behind the Scenes Content

Generate authentic BTS moments.

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create behind-the-scenes content: A young woman with auburn wavy hair, green eyes, and freckles. She is sitting in a makeup chair, hair in rollers, laughing candidly while a makeup artist works. Studio environment visible with lighting equipment in background. Wearing a black cape over her clothes. Documentary style, authentic moment, slightly desaturated tones.",
    "session_id": "influencer-maya-2024",
    "mode": "eco",
    "image_urls": ["https://example.com/maya-reference.jpg"]
  }'
```

### 10. Seasonal/Holiday Content

Create themed content for special occasions.

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate holiday content: A young woman with auburn wavy hair, green eyes, and light freckles. She is decorating a Christmas tree, wearing a cozy red knit sweater. Warm interior with fireplace glow in background, string lights creating bokeh. Holding a gold ornament, looking at camera with a warm smile. Festive, cozy atmosphere, holiday photography aesthetic.",
    "session_id": "influencer-maya-2024",
    "mode": "max",
    "image_urls": ["https://example.com/maya-reference.jpg"]
  }'
```

## Maintaining Character Consistency

### Using Reference Images

Provide `image_urls` to maintain your AI influencer's appearance across all content:

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate new content maintaining the exact appearance of the reference image. Place her in a beach setting at sunset, wearing a casual summer dress.",
    "image_urls": ["https://your-storage.com/influencer-base-portrait.jpg"],
    "session_id": "influencer-maya-2024",
    "mode": "max"
  }'
```

### Multi-Turn Sessions

Use `session_id` to build consistent persona context across multiple generations:

```bash
# First request - establish persona
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "My AI influencer is named Sophia. She has long blonde hair, blue eyes, and a bright smile. She is 26 years old with a California beach vibe aesthetic.",
    "session_id": "sophia-influencer-session"
  }'

# Second request - generate content using established persona
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate an Instagram post of Sophia at a rooftop party in LA at night.",
    "session_id": "sophia-influencer-session",
    "mode": "max"
  }'
```

## Best Practices

### Persona Consistency

1. **Create a detailed character bible**: Document hair color, eye color, skin tone, distinctive features, and preferred aesthetic
2. **Use consistent descriptors**: Always include key identifying features in every prompt
3. **Maintain style continuity**: Keep lighting, color grading, and photography style consistent
4. **Save reference images**: Use generated images as references for future content

### Prompt Tips

- **Be specific about features**: "Auburn wavy hair, green eyes, light freckles" rather than "attractive woman"
- **Describe the aesthetic**: Include photography style, lighting, and mood
- **Specify clothing in detail**: Colors, fabrics, and styles for recognizable personal brand
- **Include environment context**: Settings that match your influencer's niche
- **Mention camera angle**: Close-up, full-body, candid shot, etc.

### Content Calendar Strategy

| Day | Content Type | Mode | Focus |
|-----|--------------|------|-------|
| Monday | Motivational quote overlay | eco | Inspiration |
| Tuesday | OOTD/Fashion | max | Style |
| Wednesday | Behind the scenes | eco | Authenticity |
| Thursday | Product/Brand content | max | Monetization |
| Friday | Lifestyle/Weekend preview | max | Engagement |
| Weekend | Travel/Adventure | max | Aspirational |

## Mode Selection

| Mode | Best For | Quality | Speed |
|------|----------|---------|-------|
| `max` | Hero images, brand collaborations, portfolio pieces | Highest | Standard |
| `eco` | Stories, casual content, high-volume posting | Good | Faster |

## Error Handling

```bash
# Check response for errors
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate AI influencer content...",
    "mode": "max"
  }' 2>&1 | while read line; do
    if echo "$line" | grep -q "error"; then
      echo "Error occurred: $line"
      exit 1
    fi
    echo "$line"
  done
```

## Related Skills

- [Image Generation](/skills/eachlabs-image-generation/SKILL.md) - General image generation capabilities
- [Product Visuals](/skills/eachlabs-product-visuals/SKILL.md) - Product photography for brand collaborations
- [Fashion AI](/skills/eachlabs-fashion-ai/SKILL.md) - Fashion and style content generation
