---
name: video-color-grading
description: Apply professional color grading and correction to videos using each::sense AI. Create cinematic looks, film emulations, color corrections, and stylized grades for any video content.
metadata:
  author: eachlabs
  version: "1.0"
---

# Video Color Grading

Apply professional color grading and color correction to videos using each::sense. This skill enables cinematic looks, film stock emulations, mood-based color treatments, and technical color corrections.

## Features

- **Cinematic Grades**: Hollywood-style color treatments for narrative content
- **Film Emulation**: Kodak, Fuji, and other classic film stock looks
- **Look Development**: Orange & teal, moody dark, bright & airy styles
- **Color Correction**: Fix white balance, exposure, and color cast issues
- **Vintage/Retro**: 80s, 90s, VHS, and nostalgic color treatments
- **Black & White**: Cinematic monochrome conversions with tone control
- **HDR Enhancement**: Dynamic range expansion and tone mapping
- **Color Matching**: Match color grades between different clips

## Quick Start

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Apply a cinematic color grade to this video with teal shadows and warm highlights",
    "mode": "max",
    "video_urls": ["https://example.com/my-video.mp4"]
  }'
```

## Color Grading Styles

| Style | Description | Best For |
|-------|-------------|----------|
| Cinematic | Crushed blacks, color contrast, film-like | Narrative, drama |
| Orange & Teal | Warm skin tones, cool backgrounds | Action, blockbuster |
| Film Emulation | Kodak/Fuji film stock characteristics | Indie, music videos |
| Moody Dark | Low-key, desaturated, atmospheric | Thriller, horror |
| Bright & Airy | Lifted shadows, soft pastels | Weddings, lifestyle |
| Vintage/Retro | Faded, warm, nostalgic | Music videos, commercials |
| Black & White | Cinematic monochrome | Art films, dramatic |
| HDR Enhanced | Extended dynamic range, vivid | Nature, travel |

## Use Case Examples

### 1. Cinematic Color Grade

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Apply a cinematic color grade to this video. I want crushed blacks, slightly desaturated midtones, and a subtle teal push in the shadows with warm highlights. Make it look like a modern Hollywood film.",
    "mode": "max",
    "video_urls": ["https://example.com/raw-footage.mp4"]
  }'
```

### 2. Film Emulation (Kodak Vision3)

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Color grade this video to look like it was shot on Kodak Vision3 500T film stock. I want that classic film look with natural skin tones, rich shadows, and subtle grain. Tungsten balanced with warm color science.",
    "mode": "max",
    "video_urls": ["https://example.com/digital-footage.mp4"]
  }'
```

### 3. Orange and Teal Look

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Apply the classic orange and teal color grade to this video. Push warm orange tones into the skin and highlights, and cool teal into the shadows and backgrounds. Make it punchy like a Michael Bay film but not over the top.",
    "mode": "max",
    "video_urls": ["https://example.com/action-scene.mp4"]
  }'
```

### 4. Vintage/Retro Color Grade

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Give this video a vintage 1980s look. Faded blacks, warm color cast, reduced saturation with boosted reds and yellows. Add subtle softness and that nostalgic analog feel. Think retro music video aesthetic.",
    "mode": "max",
    "video_urls": ["https://example.com/modern-footage.mp4"]
  }'
```

### 5. Black and White Conversion

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Convert this video to cinematic black and white. I want high contrast with deep blacks and bright highlights. Focus on dramatic tonal separation. Think classic film noir or modern prestige drama. Rich monochrome, not flat.",
    "mode": "max",
    "video_urls": ["https://example.com/color-footage.mp4"]
  }'
```

### 6. Color Correction (Fix White Balance)

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "This video was shot with incorrect white balance - it has a strong orange/yellow color cast from tungsten lighting. Please correct the white balance to neutral, fix the skin tones to look natural, and balance the overall exposure. Keep it looking natural, just properly corrected.",
    "mode": "max",
    "video_urls": ["https://example.com/bad-white-balance.mp4"]
  }'
```

### 7. Match Color Between Clips

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "I have two video clips that need to match. The first video is my reference with the color grade I like. Please apply the same color grade to the second video so they look consistent when edited together. Match the contrast, saturation, color temperature, and overall tone.",
    "mode": "max",
    "video_urls": [
      "https://example.com/reference-clip.mp4",
      "https://example.com/clip-to-match.mp4"
    ]
  }'
```

### 8. Moody Dark Grade

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Apply a moody, dark color grade to this video. I want crushed shadows, desaturated colors with selective color pops, and a cold blue-green tint. Think David Fincher or Denis Villeneuve - atmospheric and brooding. Low-key lighting feel even if the original is brighter.",
    "mode": "max",
    "video_urls": ["https://example.com/scene-footage.mp4"]
  }'
```

### 9. Bright and Airy Grade

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Give this video a bright and airy look perfect for wedding or lifestyle content. Lift the shadows, add soft pastel tones, slightly warm skin tones, and reduce contrast for that dreamy quality. Clean, fresh, and romantic feeling. Keep it natural but elevated.",
    "mode": "max",
    "video_urls": ["https://example.com/wedding-footage.mp4"]
  }'
```

### 10. HDR Enhancement

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Enhance this video with HDR-style color grading. Expand the dynamic range, bring out detail in both shadows and highlights, boost color vibrancy without oversaturation. Make skies more dramatic, colors more vivid, and overall image more impactful. Great for landscape and travel footage.",
    "mode": "max",
    "video_urls": ["https://example.com/landscape-video.mp4"]
  }'
```

## Best Practices

### Color Grading Tips
- **Reference Images**: Describe a specific film or visual reference for consistent results
- **Be Specific**: Mention shadow color, highlight warmth, contrast level, saturation
- **Skin Tones**: Always mention if preserving natural skin tones is important
- **Mood First**: Start with the emotion/mood you want, then technical details

### Technical Considerations
- **Source Quality**: Better source footage yields better grading results
- **Consistency**: Use `session_id` to grade multiple clips with the same look
- **Preview First**: Use `eco` mode for quick previews, `max` for final output

### Common Terminology
| Term | Description |
|------|-------------|
| Lift | Adjusts shadow brightness |
| Gamma | Adjusts midtone brightness |
| Gain | Adjusts highlight brightness |
| Crush | Deepening blacks beyond pure black |
| Push | Adding color tint to a tonal range |
| Color Cast | Unwanted color tint across image |

## Mode Selection

Ask your users before generating:

**"Do you want fast & cheap, or high quality?"**

| Mode | Best For | Speed | Quality |
|------|----------|-------|---------|
| `max` | Final deliverables, client work | Slower | Highest |
| `eco` | Quick previews, look exploration, drafts | Faster | Good |

## Multi-Turn Creative Iteration

Use `session_id` to iterate on color grades:

```bash
# Initial grade
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Apply a cinematic teal and orange grade to this video",
    "session_id": "color-grade-project-001",
    "video_urls": ["https://example.com/my-video.mp4"]
  }'

# Refine the grade
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "The teal is too strong in the shadows. Can you reduce it and add more warmth to the skin tones?",
    "session_id": "color-grade-project-001"
  }'

# Apply to additional clips
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Apply the same grade we developed to this new clip",
    "session_id": "color-grade-project-001",
    "video_urls": ["https://example.com/second-clip.mp4"]
  }'
```

## Batch Color Grading

Grade multiple clips with the same look:

```bash
# Grade first clip and establish look
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Apply a moody cinematic grade to this video - this will be my hero look for the project",
    "session_id": "music-video-grade",
    "video_urls": ["https://example.com/clip-01.mp4"]
  }'

# Apply same look to remaining clips
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Apply the same color grade to these additional clips for consistency",
    "session_id": "music-video-grade",
    "video_urls": [
      "https://example.com/clip-02.mp4",
      "https://example.com/clip-03.mp4",
      "https://example.com/clip-04.mp4"
    ]
  }'
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | Insufficient balance | Top up at eachlabs.ai |
| Content policy violation | Prohibited content | Ensure video complies with content policies |
| Timeout | Complex video processing | Set client timeout to minimum 10 minutes |
| Video too long | Exceeds processing limits | Split video into shorter segments |

## Prompt Tips for Color Grading

When requesting color grades, include these details:

1. **Reference**: Film, director, or visual style reference
2. **Mood**: The emotional tone (moody, bright, dramatic, soft)
3. **Shadow Treatment**: Color and depth (crushed, lifted, tinted)
4. **Highlight Treatment**: Warmth, rolloff, color
5. **Saturation**: Overall and selective color intensity
6. **Contrast**: High, low, or specific curve shape
7. **Skin Tones**: Natural, warm, or stylized

### Example Prompt Structure

```
"Apply a [style] color grade to this video.
I want [shadow description] shadows and [highlight description] highlights.
The mood should be [mood/emotion].
Reference: [film or visual reference].
[Specific requirements like skin tones, saturation, etc.]"
```

## Related Skills

- `each-sense` - Core API documentation
- `video-generation` - Generate videos from scratch
- `video-editing` - Edit and modify video content
- `image-color-grading` - Color grade still images
