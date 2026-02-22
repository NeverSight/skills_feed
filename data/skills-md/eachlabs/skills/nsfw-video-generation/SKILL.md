---
name: NSFW Video Generation
description: Generate adult video content using each::sense API with safety checker disabled
metadata:
  category: video-generation
  subcategory: adult-content
  api_endpoint: https://sense.eachlabs.run/chat
  content_rating: adult
  requires_age_verification: true
tags:
  - nsfw
  - video-generation
  - adult-content
  - artistic
  - mature-themes
---

# NSFW Video Generation

Generate adult video content, artistic nude videos, and mature-themed animations using the each::sense API with safety restrictions disabled.

## Overview

The each::sense API enables creation of adult video content when the `enable_safety_checker` parameter is set to `false`. This unlocks generation capabilities for:

- **Artistic nude videos** - Fine art inspired videography
- **Glamour content** - Fashion and lingerie video production
- **Boudoir videos** - Intimate, tasteful bedroom aesthetics
- **Fantasy themes** - Mythological and fantasy adult content
- **Couples content** - Romantic and intimate pair scenarios

> **Important**: All requests must include `"enable_safety_checker": false` to generate NSFW content.

## Quick Start

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Create an artistic nude video of a woman in a classical renaissance painting style, soft natural lighting, elegant pose"
      }
    ],
    "mode": "video",
    "enable_safety_checker": false
  }'
```

## Video Types

| Type | Description | Best For |
|------|-------------|----------|
| Artistic | Fine art nude videography, classical aesthetics | Museum-quality artistic expression |
| Glamour | Fashion-forward, lingerie, elegant styling | Professional modeling portfolios |
| Boudoir | Intimate bedroom settings, soft lighting | Personal romantic content |
| Fantasy | Mythological, cosplay, themed scenarios | Creative storytelling |
| Couples | Romantic pairs, intimate moments | Relationship-focused content |
| Dance | Sensual movement, choreography | Performance and movement art |

## Use Case Examples

### 1. Artistic Video Content

Create fine art inspired nude videography with classical aesthetics.

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Generate an artistic nude video inspired by Botticelli, woman emerging from water, flowing hair, golden hour lighting, slow graceful movement, renaissance painting aesthetic"
      }
    ],
    "mode": "video",
    "enable_safety_checker": false
  }'
```

### 2. Glamour/Lingerie Video

Professional glamour and lingerie video production.

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Create a glamour video of a model in black lace lingerie, luxury bedroom setting, soft studio lighting, slow confident walk toward camera, high fashion editorial style"
      }
    ],
    "mode": "video",
    "enable_safety_checker": false
  }'
```

### 3. Boudoir Video

Intimate boudoir-style video with soft, romantic aesthetics.

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Generate a boudoir video, woman in silk robe by window, morning sunlight streaming through sheer curtains, gentle movement, intimate atmosphere, warm color palette"
      }
    ],
    "mode": "video",
    "enable_safety_checker": false
  }'
```

### 4. Dance/Movement Video

Sensual dance and movement-focused video content.

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Create a sensual contemporary dance video, woman in flowing sheer fabric, dramatic spotlight, fluid graceful movements, artistic choreography, black background"
      }
    ],
    "mode": "video",
    "enable_safety_checker": false
  }'
```

### 5. Fantasy Themed Video

Mythological and fantasy adult content with creative themes.

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Generate a fantasy video of a forest nymph, ethereal nude figure with flower crown, enchanted forest setting, magical glowing particles, mystical atmosphere, slow ethereal movement"
      }
    ],
    "mode": "video",
    "enable_safety_checker": false
  }'
```

### 6. Couples Content

Romantic and intimate couples video scenarios.

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Create a romantic couples video, intimate embrace on bed with white sheets, soft natural lighting, tender moment, tasteful artistic framing, warm romantic atmosphere"
      }
    ],
    "mode": "video",
    "enable_safety_checker": false
  }'
```

### 7. Image-to-Video Animation

Animate an existing image into NSFW video content by providing image URLs.

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Animate this artistic nude photo, add subtle breathing movement, gentle hair flowing, soft blinking, maintain the elegant pose and lighting"
      }
    ],
    "mode": "video",
    "image_urls": ["https://example.com/artistic-photo.jpg"],
    "enable_safety_checker": false
  }'
```

### 8. Consistent Character Video Series

Create multiple videos with the same character using session_id for continuity.

```bash
# First video in series
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Create a glamour video introducing a character: tall brunette model, green eyes, elegant features, in a luxury penthouse, wearing silk robe, walking to window"
      }
    ],
    "mode": "video",
    "session_id": "glamour-series-001",
    "enable_safety_checker": false
  }'

# Second video continuing the series
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Continue with the same model, now she removes the robe to reveal lingerie, turns to face camera with confident expression"
      }
    ],
    "mode": "video",
    "session_id": "glamour-series-001",
    "enable_safety_checker": false
  }'
```

### 9. Poolside/Beach Scene

Outdoor sensual video content with natural settings.

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Generate a video of a woman in a revealing bikini at a luxury pool, sunset golden hour lighting, slow motion water droplets, cinematic quality, sensual atmosphere"
      }
    ],
    "mode": "video",
    "enable_safety_checker": false
  }'
```

### 10. Vintage/Retro Style

Classic pin-up and vintage aesthetic adult content.

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Create a 1950s pin-up style video, woman in vintage lingerie and stockings, classic boudoir setting, film grain effect, soft glamour lighting, playful poses"
      }
    ],
    "mode": "video",
    "enable_safety_checker": false
  }'
```

## Best Practices

### Cinematic Quality

- **Lighting**: Specify lighting conditions (golden hour, soft studio, natural window light)
- **Camera movement**: Describe camera behavior (slow pan, static shot, tracking)
- **Composition**: Include framing details (close-up, full body, artistic angles)
- **Color palette**: Define mood through colors (warm tones, moody shadows, high key)

### Tasteful Approach

- Focus on artistic merit and aesthetic quality
- Use evocative rather than explicit language
- Emphasize elegance, beauty, and artistry
- Consider classical art references for refined results

### Technical Specifications

- Videos generate at high resolution by default
- Typical duration is 4-8 seconds per generation
- For longer content, use session_id to create connected sequences

## Prompt Tips for NSFW Video

| Do | Avoid |
|----|----|
| Use artistic terminology | Crude or vulgar language |
| Describe lighting and mood | Overly explicit descriptions |
| Reference art styles | Unrealistic anatomical requests |
| Specify camera movement | Conflicting instructions |
| Include environment details | Vague or minimal prompts |

### Effective Prompt Structure

```
[Subject description] + [Setting/Environment] + [Lighting] + [Movement/Action] + [Style/Aesthetic]
```

Example:
> "Elegant woman with auburn hair, in a candlelit baroque bedroom, warm golden lighting, slowly turning toward camera, renaissance painting style"

## Mode Selection

| Mode | Use Case |
|------|----------|
| `video` | Generate new NSFW video content from text prompts |
| `video` + `image_urls` | Animate existing images into video |

## Multi-Turn Sessions

Use `session_id` to maintain character consistency across multiple video generations:

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Create the opening scene of an artistic video series: introduce a dancer in an empty studio"
      }
    ],
    "mode": "video",
    "session_id": "dancer-series-2024",
    "enable_safety_checker": false
  }'
```

Benefits of session continuity:
- Consistent character appearance across videos
- Build narrative sequences
- Create episodic content series
- Maintain style and aesthetic coherence

## Disclaimer

This API is intended for legal adult content creation only. Users must:

- Be of legal age in their jurisdiction
- Comply with all applicable laws and regulations
- Not generate content involving minors
- Not create non-consensual content
- Respect intellectual property rights
- Use generated content responsibly

The API provider reserves the right to monitor usage and terminate access for violations.

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `safety_filter_triggered` | Safety checker still enabled | Ensure `enable_safety_checker: false` is included |
| `invalid_mode` | Wrong mode specified | Use `mode: "video"` for video generation |
| `rate_limit_exceeded` | Too many requests | Implement exponential backoff |
| `invalid_session` | Session expired or invalid | Create new session_id |
| `content_policy_violation` | Request violates terms | Review content policy guidelines |

## Response Format

The API returns Server-Sent Events (SSE). See [SSE Events Reference](references/SSE-EVENTS.md) for detailed response handling.

## Related Skills

- [Video Generation](../eachlabs-video-generation/SKILL.md) - Standard video generation
- [Image Generation](../eachlabs-image-generation/SKILL.md) - Static image creation
- [Video Edit](../eachlabs-video-edit/SKILL.md) - Video editing and enhancement
