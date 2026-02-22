---
name: TikTok Ad Creative Generation
description: Generate TikTok-native ad creatives using each::sense API - vertical videos, Spark Ads style, trending formats, and UGC aesthetics
metadata:
  category: video-generation
  platform: tiktok
  api: sense
  formats: [in-feed, topview, branded-effects, spark-ads]
---

# TikTok Ad Creative Generation

Generate scroll-stopping TikTok ad creatives using the each::sense API. Create native-feeling vertical video content optimized for TikTok's unique format and audience expectations.

## Overview

The each::sense API enables you to generate TikTok-optimized ad creatives that blend seamlessly with organic content:

- **TikTok-Native Vertical Video**: 9:16 aspect ratio optimized for full-screen mobile experience
- **Spark Ads Style**: Authentic, creator-driven aesthetics that feel native to the platform
- **Trending Formats**: UGC-style, challenge videos, duets, transitions, and viral hooks
- **Sound-On Design**: Visuals designed to complement trending audio and voiceovers
- **Fast Hooks**: First-frame impact to capture attention in under 1 second

## Quick Start

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a TikTok ad video for a skincare brand. UGC style, girl doing her morning routine, showing the product naturally. Vertical 9:16, trendy aesthetic, soft morning light.",
    "mode": "max"
  }'
```

## TikTok Ad Formats & Sizes

| Format | Aspect Ratio | Resolution | Duration | Description |
|--------|--------------|------------|----------|-------------|
| In-Feed Ads | 9:16 | 1080x1920 | 5-60s | Native video ads in For You feed |
| TopView | 9:16 | 1080x1920 | 5-60s | First ad users see when opening app |
| Spark Ads | 9:16 | 1080x1920 | 5-60s | Boosted organic-style content |
| Branded Effects | 9:16 | 1080x1920 | Variable | AR filters and effects |
| Collection Ads | 9:16 | 1080x1920 | 5-60s | Shoppable product galleries |
| Branded Hashtag | 9:16 | 1080x1920 | Variable | Challenge-based campaigns |

## Use Case Examples

### 1. UGC-Style Product Ad

Generate authentic user-generated content style ads that feel native to TikTok.

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a UGC-style TikTok ad. A young woman in her bedroom talking directly to camera about her favorite new lip gloss. Natural lighting, casual outfit, authentic vibe. She holds up the product excitedly. Vertical 9:16 format, iPhone selfie camera angle.",
    "mode": "max"
  }'
```

### 2. Product Showcase with Trending Transition

Create dynamic product reveals using popular TikTok transitions.

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "TikTok product showcase video for wireless earbuds. Start with hand covering camera, transition reveal to the earbuds floating with dynamic lighting. Trendy purple and blue gradient background, tech aesthetic. 9:16 vertical, punchy and fast-paced.",
    "mode": "max"
  }'
```

### 3. Trending Challenge Style

Capitalize on viral challenge formats for maximum engagement.

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a TikTok challenge-style video for a fitness app. Person doing the popular dance trend but incorporating workout moves. Energetic, fun, gym setting with ring light. Caption space at top. Vertical 9:16, high energy vibe.",
    "mode": "max"
  }'
```

### 4. Before/After Transformation

Showcase dramatic results with split-screen or transition reveals.

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Before and after TikTok ad for a hair styling tool. Left side: messy bedhead hair. Right side: sleek, styled hair. Same person, dramatic transformation. Clean white bathroom background, good lighting. 9:16 vertical split screen style.",
    "mode": "max"
  }'
```

### 5. Unboxing Experience

Create ASMR-friendly unboxing content that drives curiosity.

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "TikTok unboxing video for a luxury subscription box. Hands slowly opening a beautiful pink box, revealing tissue paper, then premium beauty products. ASMR aesthetic, close-up shots, soft overhead lighting. Vertical 9:16, satisfying and aesthetic.",
    "mode": "max"
  }'
```

### 6. Tutorial Style Ad

Educational content that provides value while showcasing products.

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Quick tutorial TikTok ad for a cooking gadget. Hands demonstrating how to use a vegetable spiralizer in 3 easy steps. Bright kitchen, overhead angle, ingredients visible. Text overlay space for step numbers. 9:16 vertical, fast and informative.",
    "mode": "max"
  }'
```

### 7. POV (Point of View) Format

Immersive first-person perspective that resonates with TikTok audiences.

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "POV TikTok ad: you just received your online order. First-person view of hands opening a package, pulling out trendy sneakers, trying them on. Bedroom floor setting, excited energy, millennial aesthetic. Vertical 9:16 format.",
    "mode": "max"
  }'
```

### 8. Reaction/Review Style

Authentic reaction content that builds trust and relatability.

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "TikTok reaction-style ad for a snack brand. Person trying the new flavor for the first time, genuine surprised expression, then excited approval. Casual home setting, ring light, talking to camera. Space for text overlays. 9:16 vertical.",
    "mode": "max"
  }'
```

### 9. Aesthetic Product Flat Lay

Visually pleasing arrangements perfect for beauty and lifestyle brands.

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Aesthetic flat lay TikTok video for a stationery brand. Hands arranging pastel notebooks, pens, and washi tape on a marble desk. Satisfying organization, soft shadows, minimal aesthetic. Stop motion feel. 9:16 vertical format.",
    "mode": "max"
  }'
```

### 10. Day-in-the-Life Integration

Seamlessly integrate products into lifestyle content.

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Day in the life TikTok ad for a coffee brand. Morning routine montage - alarm, stretching, making coffee with the product featured naturally, sipping while checking phone. Cozy apartment, golden hour light, lo-fi aesthetic. 9:16 vertical.",
    "mode": "max"
  }'
```

## Using Reference Images

Provide product images or brand references to guide the generation.

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a TikTok ad featuring this product. UGC style, young creator showing it off in their room. Trendy, authentic, vertical 9:16 format.",
    "image_urls": ["https://example.com/product-image.jpg"],
    "mode": "max"
  }'
```

## Best Practices for TikTok Ads

### Hook in the First Second

TikTok users scroll fast. Your opening frame must grab attention immediately.

- Start with movement or action
- Use bold visuals or unexpected elements
- Avoid slow intros or logo reveals
- Lead with the most compelling moment

### Native Feel Over Polished Production

TikTok audiences respond better to authentic content than traditional ads.

- Use natural lighting when possible
- Embrace imperfection and rawness
- Mimic creator content, not TV commercials
- Keep the energy casual and relatable

### Sound-On Design

TikTok is a sound-on platform - design visuals that complement audio.

- Leave space for trending sounds
- Consider lip-sync moments
- Use visual cues that match beat drops
- Design for both sound-on and sound-off viewing

### Follow Trends (But Stay Relevant)

Leverage trending formats while maintaining brand relevance.

- Reference current TikTok trends in prompts
- Adapt viral formats to your product
- Keep content timely and fresh
- Avoid outdated or overused trends

### Mobile-First Composition

Design for vertical, full-screen mobile viewing.

- Keep important elements in the center
- Leave space for captions and UI elements
- Use close-ups for product details
- Ensure text is readable on small screens

## Prompt Tips for TikTok Aesthetic

### Include These Elements

- **Format**: Always specify "9:16 vertical" or "TikTok format"
- **Style**: UGC, authentic, native, creator-style, casual
- **Lighting**: Natural, ring light, golden hour, soft
- **Setting**: Bedroom, bathroom, kitchen, everyday spaces
- **Energy**: Fast-paced, punchy, dynamic, engaging
- **Camera angle**: Selfie, handheld, POV, overhead

### Effective Prompt Structure

```
[Content type] + [Subject/Action] + [Setting] + [Aesthetic] + [Format] + [Special elements]
```

Example:
```
"UGC-style TikTok ad + girl applying skincare + bathroom mirror + clean girl aesthetic + 9:16 vertical + morning light, text overlay space"
```

### Style Keywords That Work

| Category | Keywords |
|----------|----------|
| Aesthetic | Clean girl, that girl, dark academia, cottagecore, Y2K, minimal |
| Energy | Chaotic, chill, energetic, cozy, satisfying, dramatic |
| Camera | Selfie angle, overhead, close-up, wide, tracking, shaky |
| Lighting | Golden hour, ring light, natural, moody, soft, harsh |
| Edit style | Jump cuts, transitions, slow-mo, speed ramp, split screen |

## Mode Selection

### Max Mode

Use for high-quality ad creatives requiring detailed visuals.

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Premium TikTok TopView ad for a luxury perfume. Cinematic close-up of the bottle, light refracting through glass, elegant hands reaching for it. High-end aesthetic, 9:16 vertical.",
    "mode": "max"
  }'
```

### Eco Mode

Use for rapid iteration and concept exploration.

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Quick TikTok ad concept for a snack brand. Person snacking while scrolling phone. Casual, relatable. 9:16.",
    "mode": "eco"
  }'
```

## Multi-Turn Iteration with Session ID

Refine your TikTok ad creatives through conversation.

### Initial Generation

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a TikTok ad for a new energy drink. Young person at the gym, taking a sip, then crushing their workout. High energy, motivational. 9:16 vertical.",
    "session_id": "tiktok-ad-energy-001",
    "mode": "max"
  }'
```

### Iterate on Style

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Make it more UGC style, less polished. Like someone filming themselves with their phone propped up.",
    "session_id": "tiktok-ad-energy-001",
    "mode": "max"
  }'
```

### Adjust for Brand Guidelines

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Add more neon green accents to match our brand colors. Keep the can prominently visible.",
    "session_id": "tiktok-ad-energy-001",
    "mode": "max"
  }'
```

## Error Handling

### Rate Limiting

```bash
# Implement retry with exponential backoff
for i in 1 2 3; do
  response=$(curl -s -w "\n%{http_code}" -X POST "https://sense.eachlabs.run/chat" \
    -H "Content-Type: application/json" \
    -H "X-API-Key: $EACHLABS_API_KEY" \
    -H "Accept: text/event-stream" \
    -d '{
      "message": "TikTok ad for a fashion brand, trendy outfit reveal. 9:16 vertical.",
      "mode": "max"
    }')

  http_code=$(echo "$response" | tail -n1)

  if [ "$http_code" -eq 200 ]; then
    echo "$response" | head -n -1
    break
  elif [ "$http_code" -eq 429 ]; then
    echo "Rate limited, retrying in $((i * 5)) seconds..."
    sleep $((i * 5))
  else
    echo "Error: HTTP $http_code"
    break
  fi
done
```

### Validation

```bash
# Validate required parameters before sending
if [ -z "$EACHLABS_API_KEY" ]; then
  echo "Error: EACHLABS_API_KEY environment variable is not set"
  exit 1
fi

curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "TikTok in-feed ad for headphones. 9:16 vertical format.",
    "mode": "max"
  }'
```

## Related Skills

- [Video Generation](/skills/eachlabs-video-generation) - General video creation capabilities
- [Video Edit](/skills/eachlabs-video-edit) - Post-generation video editing
- [Image Generation](/skills/eachlabs-image-generation) - Static ad thumbnails and stills
- [Product Visuals](/skills/eachlabs-product-visuals) - E-commerce product imagery
