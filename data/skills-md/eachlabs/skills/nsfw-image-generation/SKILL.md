---
name: NSFW Image Generation
description: Generate adult images, artistic nudes, glamour photography, and fantasy art using the each::sense API with safety checker disabled
metadata:
  category: image-generation
  subcategory: nsfw
  api_endpoint: https://sense.eachlabs.run/chat
  content_rating: adult
  requires_age_verification: true
tags:
  - nsfw
  - adult-content
  - artistic-nude
  - glamour
  - boudoir
  - fantasy-art
  - fine-art
---

# NSFW Image Generation

Generate adult images, artistic nude photography, glamour shots, boudoir photography, and fantasy art using the each::sense API.

## Overview

The each::sense API enables NSFW image generation when the `enable_safety_checker` parameter is set to `false`. This unlocks the ability to create:

- **Artistic Nude Photography**: Fine art nudes with emphasis on form, lighting, and composition
- **Glamour Photography**: Professional glamour and lingerie photography
- **Boudoir Photography**: Intimate, sensual imagery with elegant aesthetics
- **Pin-Up Style**: Retro-inspired pin-up art and photography
- **Fantasy Art**: Adult fantasy illustrations and character art
- **Fine Art Nude**: Classical artistic representations of the human form

## Quick Start

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $EACH_API_KEY" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Create an artistic nude photograph, elegant female form, dramatic chiaroscuro lighting, black and white, fine art style"
      }
    ],
    "mode": "max",
    "enable_safety_checker": false
  }'
```

## Image Styles

| Style | Description | Best For |
|-------|-------------|----------|
| Artistic Nude | Fine art focus on human form, lighting, composition | Gallery-quality art, photography portfolios |
| Glamour | Professional glamour photography, lingerie, fashion | Fashion, modeling portfolios |
| Boudoir | Intimate, sensual, elegant bedroom aesthetics | Personal projects, romantic imagery |
| Pin-Up | Retro-inspired, playful, vintage aesthetics | Illustration, nostalgic themes |
| Fantasy | Adult fantasy art, mythical characters, illustrations | Character design, fantasy projects |
| Fine Art | Classical artistic style, museum-quality aesthetics | Art collections, exhibitions |

## Use Case Examples

### 1. Artistic Nude Photography

Classic fine art nude with emphasis on form and lighting.

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $EACH_API_KEY" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Artistic nude photograph, elegant female figure silhouette against window light, soft morning glow, minimalist composition, black and white, fine art photography style, emphasis on curves and shadows"
      }
    ],
    "mode": "max",
    "enable_safety_checker": false
  }'
```

### 2. Glamour and Lingerie Photography

Professional glamour photography with fashion aesthetics.

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $EACH_API_KEY" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Glamour photography, stunning model in black lace lingerie, luxurious bedroom setting, soft golden hour lighting through sheer curtains, professional fashion photography, high-end editorial style"
      }
    ],
    "mode": "max",
    "enable_safety_checker": false
  }'
```

### 3. Boudoir Style Photography

Intimate and sensual boudoir imagery.

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $EACH_API_KEY" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Boudoir photography, woman lounging on vintage chaise lounge, silk robe partially draped, soft romantic lighting with candles, intimate atmosphere, warm color palette, elegant and tasteful"
      }
    ],
    "mode": "max",
    "enable_safety_checker": false
  }'
```

### 4. Pin-Up Style Art

Retro-inspired pin-up illustrations and photography.

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $EACH_API_KEY" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Classic 1950s pin-up style illustration, playful pose, vintage swimsuit, retro color palette, Gil Elvgren inspired, cheerful expression, vibrant background, nostalgic Americana aesthetic"
      }
    ],
    "mode": "max",
    "enable_safety_checker": false
  }'
```

### 5. Fantasy Art

Adult fantasy illustrations with mythical themes.

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $EACH_API_KEY" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Fantasy art, beautiful elven warrior goddess, flowing silver hair, ethereal glowing skin, mystical forest setting, moonlit atmosphere, ornate minimal armor, magical aura, detailed digital painting style"
      }
    ],
    "mode": "max",
    "enable_safety_checker": false
  }'
```

### 6. Fine Art Nude

Classical fine art representation of the human form.

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $EACH_API_KEY" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Fine art nude in classical Renaissance style, reclining figure on draped fabric, Titian-inspired color palette, oil painting texture, museum quality, emphasis on human beauty and classical proportions"
      }
    ],
    "mode": "max",
    "enable_safety_checker": false
  }'
```

### 7. Couples Content

Romantic and intimate couples imagery.

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $EACH_API_KEY" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Romantic couples photography, intimate embrace, soft natural lighting, bedroom setting with white linens, artistic and tasteful, focus on connection and emotion, warm skin tones, professional boudoir style"
      }
    ],
    "mode": "max",
    "enable_safety_checker": false
  }'
```

### 8. Character-Based with Consistent Persona

Generate consistent character imagery using reference images.

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $EACH_API_KEY" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Create a glamour portrait of this model in elegant lingerie, professional studio lighting, high fashion aesthetic"
      }
    ],
    "image_urls": ["https://example.com/reference-model.jpg"],
    "mode": "max",
    "enable_safety_checker": false
  }'
```

### 9. Artistic Body Study

Detailed body study for artistic purposes.

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $EACH_API_KEY" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Artistic body study, athletic male figure, dramatic Rembrandt lighting, emphasis on musculature and form, studio photography, high contrast black and white, fine art aesthetic"
      }
    ],
    "mode": "max",
    "enable_safety_checker": false
  }'
```

### 10. Vintage Erotica Style

Classic vintage erotica aesthetics.

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $EACH_API_KEY" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Vintage 1920s erotica style photograph, art deco setting, sepia tones, elegant flapper aesthetic, pearl accessories, soft focus, classic Hollywood glamour, tasteful and artistic"
      }
    ],
    "mode": "max",
    "enable_safety_checker": false
  }'
```

## Best Practices

### Artistic Quality

- **Lighting**: Specify lighting style (chiaroscuro, Rembrandt, soft, natural, studio)
- **Composition**: Include composition guidance (rule of thirds, centered, negative space)
- **Style Reference**: Reference known photographers or art styles for consistency
- **Color Palette**: Define warm, cool, monochrome, or specific color schemes

### Prompt Structure

For best results, structure your prompts with:

1. **Subject**: Describe the subject and pose
2. **Setting**: Environment, background, props
3. **Lighting**: Type and direction of light
4. **Style**: Photography or art style reference
5. **Mood**: Atmosphere and emotional tone
6. **Technical**: Camera angle, depth of field, format

### Example Structured Prompt

```
Subject: Elegant female figure in graceful pose
Setting: Minimalist white studio with draped silk fabric
Lighting: Soft wraparound lighting with subtle shadows
Style: High-fashion editorial photography
Mood: Sophisticated and sensual
Technical: Medium format, shallow depth of field
```

## Prompt Tips for NSFW Imagery

### Do Include

- Artistic style references (fine art, glamour, boudoir)
- Lighting descriptions (soft, dramatic, natural)
- Mood and atmosphere (intimate, sensual, elegant)
- Composition guidance (silhouette, profile, three-quarter)
- Quality indicators (professional, high-end, editorial)

### Avoid

- Overly explicit or crude language (reduces quality)
- Vague descriptions (leads to inconsistent results)
- Conflicting style directions
- Unrealistic anatomical requests

## Mode Selection

| Mode | Use Case | Quality | Speed |
|------|----------|---------|-------|
| `max` | Final images, portfolio work, high detail | Highest | Slower |
| `eco` | Drafts, concept exploration, iteration | Good | Faster |

### Production Quality

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $EACH_API_KEY" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Professional boudoir photograph, soft natural window light, elegant pose, high-end editorial quality"
      }
    ],
    "mode": "max",
    "enable_safety_checker": false
  }'
```

### Draft and Iteration

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $EACH_API_KEY" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Quick concept sketch, artistic nude silhouette, minimal style"
      }
    ],
    "mode": "eco",
    "enable_safety_checker": false
  }'
```

## Multi-Turn Sessions for Consistent Models

Use `session_id` to maintain character consistency across multiple images.

### Initial Generation

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $EACH_API_KEY" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Create a glamour portrait of an elegant brunette model, green eyes, professional studio lighting"
      }
    ],
    "session_id": "model-session-001",
    "mode": "max",
    "enable_safety_checker": false
  }'
```

### Follow-Up with Same Character

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $EACH_API_KEY" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Now show the same model in a boudoir setting, silk robe, romantic candlelight"
      }
    ],
    "session_id": "model-session-001",
    "mode": "max",
    "enable_safety_checker": false
  }'
```

## Disclaimer

**Age Verification Required**: This API feature is intended for adult users only (18+ or legal age in your jurisdiction).

**Platform Compliance**: Users are responsible for ensuring their use of generated content complies with:
- Local laws and regulations
- Platform terms of service where content is published
- Copyright and intellectual property laws
- Consent and ethical content creation guidelines

**Prohibited Content**: The API will not generate:
- Content depicting minors in any context
- Non-consensual scenarios
- Illegal content

**Terms of Service**: Use of this API constitutes agreement to Each Labs terms of service and acceptable use policy.

## Error Handling

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `safety_check_failed` | Safety checker still enabled | Ensure `enable_safety_checker: false` is in request |
| `content_policy_violation` | Request violates content policy | Revise prompt to comply with guidelines |
| `invalid_image_url` | Reference image URL inaccessible | Check URL accessibility and format |
| `rate_limit_exceeded` | Too many requests | Implement backoff and retry logic |

### Error Response Example

```json
{
  "error": {
    "code": "content_policy_violation",
    "message": "The requested content violates our acceptable use policy"
  }
}
```

## Related Skills

- [Image Generation](/skills/eachlabs-image-generation/SKILL.md) - General image generation with safety checks
- [Image Edit](/skills/eachlabs-image-edit/SKILL.md) - Edit and modify existing images
- [Video Generation](/skills/eachlabs-video-generation/SKILL.md) - Create video content
