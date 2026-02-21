---
name: meta-ad-creative-generation
description: Generate Meta (Facebook & Instagram) ad creatives using each::sense AI. Create feed ads, stories, reels, carousel images, and video ads optimized for Meta's ad formats and best practices.
metadata:
  author: eachlabs
  version: "1.0"
---

# Meta Ad Creative Generation

Generate high-converting Meta (Facebook & Instagram) ad creatives using each::sense. This skill creates images and videos optimized for Meta's ad placements, formats, and best practices.

## Features

- **Feed Ads**: Static images and videos for Facebook/Instagram feed
- **Stories & Reels**: Vertical 9:16 content for immersive placements
- **Carousel Ads**: Multiple images for product showcases
- **Video Ads**: Short-form video content for engagement
- **Product Ads**: E-commerce focused creatives with lifestyle context
- **Brand Awareness**: Eye-catching visuals for reach campaigns
- **Lead Generation**: Compelling visuals with clear CTAs

## Quick Start

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a Facebook feed ad for a fitness app showing someone working out with energetic vibes, include space for headline text",
    "mode": "max"
  }'
```

## Meta Ad Formats & Sizes

| Placement | Aspect Ratio | Recommended Size | Use Case |
|-----------|--------------|------------------|----------|
| Feed (Image) | 1:1 | 1080x1080 | Product ads, brand awareness |
| Feed (Image) | 4:5 | 1080x1350 | More vertical space, higher engagement |
| Feed (Video) | 1:1 or 4:5 | 1080x1080 or 1080x1350 | Product demos, testimonials |
| Stories/Reels | 9:16 | 1080x1920 | Full-screen immersive ads |
| Carousel | 1:1 | 1080x1080 | Product catalogs, features |
| Right Column | 1.91:1 | 1200x628 | Desktop sidebar ads |

## Use Case Examples

### 1. Product Ad (E-commerce)

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1:1 Facebook product ad for wireless earbuds. Show the earbuds on a clean minimal background with lifestyle context - someone at a gym or running. Modern, premium feel. Leave space at top for headline.",
    "mode": "max"
  }'
```

### 2. Instagram Stories Ad

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 9:16 Instagram Stories ad for a skincare brand. Show a woman with glowing skin, soft natural lighting, minimalist aesthetic. Leave safe zones at top and bottom for UI elements.",
    "mode": "max"
  }'
```

### 3. Facebook Video Ad

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 5 second 1:1 video ad for a coffee subscription service. Show steaming coffee being poured, cozy morning vibes, warm color grading. Eye-catching for autoplay without sound.",
    "mode": "max"
  }'
```

### 4. Carousel Ad (Multiple Products)

```bash
# First image
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1:1 carousel ad image 1 of 4 for a furniture store. Show a modern sofa in a stylish living room. Clean, aspirational lifestyle photography style.",
    "session_id": "carousel-furniture-001"
  }'

# Second image (same session for consistency)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create carousel image 2 of 4. Show a dining table set in the same style as the previous image. Maintain consistent lighting and aesthetic.",
    "session_id": "carousel-furniture-001"
  }'
```

### 5. Reels Ad (Vertical Video)

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 9:16 vertical video ad for Instagram Reels. Fashion brand summer collection - show a model walking on a beach in a flowing dress, cinematic slow motion, golden hour lighting. 5 seconds.",
    "mode": "max"
  }'
```

### 6. App Install Ad

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 4:5 Facebook ad for a meditation app. Show a peaceful person meditating in nature, soft morning light, calming colors (blues and greens). Include visual space for app store badges and CTA button.",
    "mode": "max"
  }'
```

### 7. Restaurant/Food Ad

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1:1 Facebook ad for an Italian restaurant. Show a delicious pasta dish with steam rising, rustic table setting, warm inviting atmosphere. Food photography style, make it look appetizing.",
    "mode": "max"
  }'
```

### 8. Lead Generation Ad (B2B)

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1:1 Facebook lead gen ad for a B2B SaaS product. Show a professional working on a laptop with data visualizations, modern office environment, confident and productive mood. Corporate but not boring.",
    "mode": "max"
  }'
```

### 9. UGC-Style Ad

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a UGC-style 9:16 video ad for a teeth whitening product. Show a young woman doing a selfie-style testimonial, authentic iPhone footage look, bathroom mirror setting, before/after reveal moment. 10 seconds.",
    "mode": "max"
  }'
```

### 10. Retargeting Ad (with Product Image)

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1:1 retargeting ad for sneakers. Show white sneakers prominently with a lifestyle background (urban street scene). Add visual urgency - style that says limited time offer. Clean product focus.",
    "mode": "max",
    "image_urls": ["https://example.com/product-sneakers.jpg"]
  }'
```

## Best Practices

### Image Ads
- **Text Overlay**: Keep text minimal - Meta recommends less than 20% text coverage
- **Safe Zones**: Leave 14% margin at top/bottom for Stories/Reels UI elements
- **Focal Point**: Place key visual elements in the center
- **Contrast**: Use contrasting colors to stand out in feed
- **Brand Colors**: Maintain consistent brand identity across ads

### Video Ads
- **Hook in 3 seconds**: Capture attention immediately
- **Design for sound-off**: Use captions, visual storytelling
- **Loop-friendly**: Create seamless loops for short videos
- **Mobile-first**: Design for vertical/square on mobile

### Carousel Ads
- **Visual consistency**: Maintain same style across all cards
- **Story arc**: Create a narrative flow between images
- **First image hook**: Make the first card most compelling

## Prompt Tips for Meta Ads

When creating Meta ad creatives, include these details in your prompt:

1. **Format**: Specify aspect ratio (1:1, 4:5, 9:16)
2. **Placement**: Mention if it's for feed, stories, or reels
3. **Product/Service**: Clearly describe what you're advertising
4. **Target Audience**: Who is this ad for?
5. **Mood/Style**: Energetic, calm, luxurious, playful, etc.
6. **Text Space**: Request space for headlines/CTAs if needed
7. **Brand Guidelines**: Mention colors, style preferences

### Example Prompt Structure

```
"Create a [aspect ratio] [placement] ad for [product/service].
Show [visual description] with [mood/style].
Target audience: [demographic].
[Additional requirements like text space, brand colors, etc.]"
```

## Mode Selection

Ask your users before generating:

**"Do you want fast & cheap, or high quality?"**

| Mode | Best For | Speed | Quality |
|------|----------|-------|---------|
| `max` | Final ad creatives, A/B testing winners | Slower | Highest |
| `eco` | Quick drafts, concept exploration, bulk testing | Faster | Good |

## Multi-Turn Creative Iteration

Use `session_id` to iterate on ad creatives:

```bash
# Initial creative
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1:1 Facebook ad for a watch brand, luxury feel",
    "session_id": "watch-ad-project"
  }'

# Iterate based on feedback
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Make it more dramatic with darker background, add some bokeh lights",
    "session_id": "watch-ad-project"
  }'

# Request variation
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create 2 more variations of this ad with different angles",
    "session_id": "watch-ad-project"
  }'
```

## A/B Testing Batch Generation

Generate multiple variations for testing:

```bash
# Variation A - Lifestyle focus
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1:1 ad for protein powder - lifestyle shot with athlete in gym",
    "mode": "eco"
  }'

# Variation B - Product focus
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1:1 ad for protein powder - clean product shot with ingredients",
    "mode": "eco"
  }'

# Variation C - Benefit focus
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1:1 ad for protein powder - before/after transformation style",
    "mode": "eco"
  }'
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | Insufficient balance | Top up at eachlabs.ai |
| Content policy violation | Prohibited content | Adjust prompt to comply with Meta ad policies |
| Timeout | Complex generation | Set client timeout to minimum 10 minutes |

## Related Skills

- `each-sense` - Core API documentation
- `google-ad-creative-generation` - Google Ads creatives
- `tiktok-ad-creative-generation` - TikTok ad creatives
- `product-photo-generation` - E-commerce product shots
