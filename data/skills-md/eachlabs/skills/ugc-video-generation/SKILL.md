---
name: UGC Video Generation
description: Generate authentic user-generated content (UGC) style videos including testimonials, unboxings, reviews, and selfie-style content using each::sense API
metadata:
  category: video-generation
  tags:
    - ugc
    - testimonial
    - unboxing
    - review
    - user-content
    - social-media
  api: each::sense
  version: "1.0"
---

# UGC Video Generation

Generate authentic user-generated content (UGC) style videos using the each::sense API. Create testimonials, unboxing videos, product reviews, tutorials, and selfie-style content that feels natural and relatable.

## Overview

UGC videos are characterized by their authentic, casual feel - as if recorded by a real person on their phone. This skill enables you to generate:

- **Testimonial Videos**: Talking head style content with genuine-feeling endorsements
- **Unboxing Videos**: First impressions and product reveals
- **Product Reviews**: Honest-feeling assessments and demonstrations
- **Before/After Content**: Transformation reveals and comparisons
- **Tutorial Videos**: How-to and instructional content
- **Day-in-Life**: Lifestyle content featuring products naturally
- **Get Ready With Me (GRWM)**: Personal routine content
- **Reaction Videos**: Authentic responses and first impressions

## Quick Start

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a UGC testimonial video of a woman in her 30s talking about how this skincare product changed her skin. Casual iPhone footage look, natural lighting, filmed in her bathroom. She should be excited but genuine.",
    "mode": "max"
  }'
```

## UGC Video Formats

| Format | Description | Best For |
|--------|-------------|----------|
| Testimonial | Talking head, direct to camera | Product endorsements, service reviews |
| Unboxing | First-time product reveal | E-commerce, subscription boxes, tech |
| Tutorial | Step-by-step demonstration | Beauty, DIY, software, cooking |
| Review | In-depth product assessment | Electronics, apps, services |
| Before/After | Transformation reveal | Fitness, beauty, home improvement |
| Day-in-Life | Lifestyle integration | Wellness, productivity, fashion |
| GRWM | Personal routine showcase | Beauty, fashion, lifestyle |
| Reaction | First impression response | Entertainment, products, reveals |

## Use Case Examples

### 1. Testimonial Video (Talking Head)

Generate a genuine-feeling customer testimonial.

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a UGC testimonial video. A young professional man in his late 20s sits on his couch, talking directly to camera. He shares how the meal prep service saved him hours every week. iPhone selfie camera angle, living room setting with natural window light. Casual clothes, authentic delivery - not scripted feeling. He should occasionally look away thinking, then back at camera. 15-20 seconds.",
    "mode": "max"
  }'
```

### 2. Product Unboxing

Create an authentic unboxing experience video.

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate an unboxing video UGC style. A college-age woman opens a subscription beauty box on her bed. POV angle showing her hands and reactions. She pulls items out one by one, showing genuine excitement and surprise. Natural bedroom lighting, casual setting with some clutter visible. She comments on each product as she discovers it. iPhone footage aesthetic, 20-25 seconds.",
    "mode": "max"
  }'
```

### 3. Before/After Transformation

Show a transformation with authentic reveal moment.

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a before/after UGC video for a fitness app. Split format or transition style. Person films themselves in mirror - first clip shows them at the start of their journey (tired, unsure), then cut/transition to 3 months later (confident, energetic, visible progress). Bathroom or bedroom mirror, natural phone recording style. Include authentic facial expressions - nervous in before, proud in after. 15 seconds.",
    "mode": "max"
  }'
```

### 4. Tutorial/How-To

Generate step-by-step instructional content.

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a UGC tutorial video showing how to use a face serum. POV hands-on demonstration. Woman applies product step by step - cleanser first, then serum application technique, gentle patting motions. Bathroom counter setup, ring light visible in reflection for authenticity. She explains each step casually like talking to a friend. Some minor mistakes are okay - keeps it real. 25-30 seconds.",
    "mode": "max"
  }'
```

### 5. Review Style

Create an honest-feeling product review.

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate a UGC product review video. Man in his 40s reviews wireless earbuds from his home office. He shows the product, tests features, shares honest pros and cons. Webcam quality footage, casual home office background with some personalization visible. He demonstrates the fit, tests the sound, mentions battery life from his experience. Conversational tone, not overly polished. 30 seconds.",
    "mode": "max"
  }'
```

### 6. Day in the Life

Show natural product integration into daily routine.

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a day-in-the-life UGC video featuring a productivity app. Quick montage style - morning routine checking the app with coffee, using it during commute, referencing it during work, end of day review. Young professional woman, various locations throughout her day. iPhone footage, some clips handheld, some propped up. Natural lighting varies by scene. Lifestyle content feel, 20-25 seconds.",
    "mode": "max"
  }'
```

### 7. Get Ready With Me (GRWM)

Generate personal routine content.

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a GRWM (Get Ready With Me) UGC video. Woman does her morning skincare and makeup routine while casually chatting to camera. Bathroom vanity setup, phone propped against mirror. She applies each product naturally, mentioning what she uses and why. Soft morning light, slightly messy counter with various products. Relaxed, friendly vibe like catching up with a friend. 30-35 seconds.",
    "mode": "max"
  }'
```

### 8. Reaction Video

Capture authentic first impression responses.

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate a reaction video UGC style. Teen reacts to trying a new snack for the first time. Selfie angle, bedroom background with posters visible. Initial skepticism, first bite, genuine surprise at the taste, enthusiastic recommendation. Raw, unfiltered reactions - could be positive or comically disgusted. Natural facial expressions, authentic Gen-Z energy. 15 seconds.",
    "mode": "max"
  }'
```

### 9. Consistent Character with Image Reference

Use image_urls to maintain consistent presenter across videos.

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a UGC testimonial video using the person in the reference image. They should be in their kitchen, talking about their experience with a cooking app. Natural morning light, casual pajamas, coffee in hand. Genuine enthusiasm about how the app helped them learn to cook. iPhone front camera angle, 20 seconds.",
    "image_urls": ["https://example.com/your-presenter-reference.jpg"],
    "mode": "max"
  }'
```

### 10. Product-Focused UGC with Visual Reference

Include product images for consistent product appearance.

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an unboxing and first impressions UGC video featuring this product. Young woman opens the package at her desk, examines the product from the reference image, tests it out, shares initial thoughts. Home office setting, afternoon light from window, laptop visible in background. Authentic excitement, genuine reactions. 25 seconds.",
    "image_urls": ["https://example.com/your-product-image.jpg"],
    "mode": "max"
  }'
```

## Best Practices for Authentic UGC Feel

### Visual Authenticity
- Request "iPhone footage" or "phone camera quality" in prompts
- Include natural lighting variations (window light, bathroom lighting)
- Allow for slight camera shake or imperfect framing
- Show real environments with some clutter or personalization

### Performance Authenticity
- Ask for "genuine" or "authentic" reactions
- Include natural pauses, thinking moments, looking away
- Request conversational, not scripted-sounding delivery
- Allow for minor imperfections - they add credibility

### Setting Authenticity
- Use real-life locations: bedrooms, bathrooms, kitchens, offices
- Include background elements that feel lived-in
- Match lighting to location (ring light for beauty, natural for lifestyle)
- Show products in natural use contexts

## Prompt Tips

### For iPhone Footage Look
Include phrases like:
- "iPhone selfie camera angle"
- "Front-facing camera perspective"
- "Phone propped up on surface"
- "Handheld phone footage"
- "Vertical video format"

### For Natural Lighting
Specify:
- "Natural window light"
- "Morning bathroom lighting"
- "Soft afternoon light"
- "Ring light visible in background" (for beauty content)

### For Casual Settings
Describe:
- "Bedroom with unmade bed visible"
- "Bathroom counter with products scattered"
- "Living room couch, relaxed setting"
- "Kitchen counter, morning routine"

### For Authentic Delivery
Request:
- "Conversational tone, like talking to a friend"
- "Genuine reactions, not over-performed"
- "Natural pauses and thinking moments"
- "Casual speech with some filler words"

## Mode Selection

| Mode | Best For | Quality |
|------|----------|---------|
| `max` | Final content, campaign assets | Highest quality, longer processing |
| `eco` | Drafts, testing concepts, iterations | Faster, lower cost |

```bash
# High quality for final assets
"mode": "max"

# Quick draft for concept testing
"mode": "eco"
```

## Multi-Turn Iteration with Session ID

Use session_id to maintain context and create consistent content across a series.

### Initial Video

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a UGC testimonial. Young woman talks about discovering a new vitamin brand. Casual, in her kitchen, morning light. She explains why she decided to try it.",
    "session_id": "ugc-campaign-001",
    "mode": "max"
  }'
```

### Follow-Up Video (Same Presenter)

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a follow-up video with the same presenter. Now she has been using the vitamins for 2 weeks. Same kitchen setting but different outfit. She shares her experience so far - more energy, better sleep. Still casual and genuine.",
    "session_id": "ugc-campaign-001",
    "mode": "max"
  }'
```

### Series Conclusion

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Final video in the series with our presenter. One month update. She gives her honest final review, would she recommend it? Kitchen setting, but this time shes making her morning smoothie while talking. Natural integration of the product into her routine.",
    "session_id": "ugc-campaign-001",
    "mode": "max"
  }'
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid or missing API key | Verify `EACHLABS_API_KEY` is set correctly |
| 400 Bad Request | Malformed request body | Check JSON syntax and required parameters |
| 413 Payload Too Large | Image files too large | Compress images or use smaller files |
| 429 Rate Limited | Too many requests | Implement backoff, reduce request frequency |
| 500 Server Error | Processing failure | Retry with exponential backoff |

### Retry Example

```bash
# Simple retry with delay
for i in 1 2 3; do
  response=$(curl -s -w "%{http_code}" -X POST "https://sense.eachlabs.run/chat" \
    -H "Content-Type: application/json" \
    -H "X-API-Key: $EACHLABS_API_KEY" \
    -H "Accept: text/event-stream" \
    -d '{
      "message": "Create a quick UGC testimonial video, casual selfie style, 10 seconds.",
      "mode": "eco"
    }')

  http_code="${response: -3}"
  if [ "$http_code" = "200" ]; then
    echo "Success"
    break
  fi

  echo "Attempt $i failed with code $http_code, retrying..."
  sleep $((i * 2))
done
```

## Related Skills

- **Video Generation**: General video creation capabilities
- **Image Generation**: Create reference images for consistent characters
- **Voice Audio**: Generate voiceovers for UGC content
- **Video Edit**: Post-process and edit generated UGC videos
