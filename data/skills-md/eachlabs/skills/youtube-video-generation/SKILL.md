---
name: youtube-video-generation
description: Generate YouTube videos and Shorts using each::sense AI. Create faceless videos, explainers, tutorials, product reviews, compilations, and more optimized for YouTube's formats and best practices.
metadata:
  author: eachlabs
  version: "1.0"
---

# YouTube Video Generation

Generate engaging YouTube content using each::sense. This skill creates videos optimized for YouTube's various formats including long-form videos, Shorts, and thumbnails.

## Features

- **Faceless Videos**: AI-generated content without on-camera presence
- **YouTube Shorts**: Vertical 9:16 content up to 3 minutes
- **Explainer Videos**: Educational content with visual aids
- **Product Reviews**: Showcase and review products with AI visuals
- **Tutorials**: Step-by-step how-to content
- **News Summaries**: Quick news recap videos
- **Compilations**: Curated content collections
- **Gaming Highlights**: Gaming clip compilations
- **ASMR/Relaxation**: Ambient and calming content
- **Channel Branding**: Intros, outros, and thumbnails

## Quick Start

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 30-second faceless YouTube video about the benefits of meditation, with calming visuals and text overlays",
    "mode": "max"
  }'
```

## YouTube Video Formats & Sizes

| Format | Aspect Ratio | Resolution | Max Duration | Use Case |
|--------|--------------|------------|--------------|----------|
| Long-form Video | 16:9 | 1920x1080 | Unlimited | Standard YouTube videos |
| YouTube Shorts | 9:16 | 1080x1920 | 3 minutes | Short-form vertical content |
| Thumbnail | 16:9 | 1280x720 | N/A | Video thumbnail image |

## Use Case Examples

### 1. Faceless YouTube Video Generation

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 60-second faceless YouTube video about 5 interesting facts about space. Use stunning space imagery, smooth transitions, and animated text overlays for each fact. Add a cinematic orchestral background music feel. 16:9 aspect ratio at 1920x1080.",
    "mode": "max"
  }'
```

### 2. YouTube Shorts from Script

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a YouTube Short (9:16, 1080x1920) from this script: \"Did you know that honey never spoils? Archaeologists found 3000-year-old honey in Egyptian tombs that was still edible!\" Use eye-catching visuals of honey, ancient Egypt, and include bold captions. Make it attention-grabbing for the first 2 seconds.",
    "mode": "max"
  }'
```

### 3. Explainer/Educational Video

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 2-minute educational explainer video about how photosynthesis works. Use animated diagrams, infographics, and step-by-step visualizations. Include a friendly voiceover style with clear explanations. 16:9 at 1920x1080. Target audience: middle school students.",
    "mode": "max"
  }'
```

### 4. Product Review Video

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 90-second product review video for wireless noise-canceling headphones. Show the product from multiple angles, highlight key features (battery life, noise cancellation, comfort), include pros and cons sections with graphics, and end with a rating. 16:9 at 1920x1080, modern tech review style.",
    "mode": "max"
  }'
```

### 5. Tutorial/How-To Video

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a step-by-step tutorial video on how to make the perfect pour-over coffee. Include numbered steps, close-up shots of equipment, water temperature graphics, timing indicators, and brewing tips. 16:9 at 1920x1080. Duration: 3 minutes. Clean, minimalist aesthetic.",
    "mode": "max"
  }'
```

### 6. News Summary Video

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 60-second news summary video template for a tech news channel. Include animated lower thirds, headline graphics, transition effects, and space for B-roll footage. Professional news broadcast style with modern graphics. 16:9 at 1920x1080. Blue and white color scheme.",
    "mode": "max"
  }'
```

### 7. Compilation Video

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 2-minute satisfying compilation video. Include various satisfying visuals: slime being pressed, perfect cake cutting, kinetic sand, soap cutting, and paint mixing. Smooth transitions between clips, no text overlays, relaxing ambient music vibe. 16:9 at 1920x1080.",
    "mode": "max"
  }'
```

### 8. Gaming Highlight Video

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 45-second gaming highlight intro/template video. Energetic style with glitch effects, neon colors, dynamic transitions, and space for gameplay clips. Include animated subscribe button, social media handles placeholder, and channel logo placement. 16:9 at 1920x1080. EDM/trap music energy.",
    "mode": "max"
  }'
```

### 9. ASMR/Relaxation Video

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 3-minute relaxation video for sleep and meditation. Slow-moving visuals of a peaceful forest with gentle rain, soft fog drifting through trees, and occasional wildlife. Very slow, calming transitions. No text, no sudden movements. 16:9 at 1920x1080. Ambient nature sounds.",
    "mode": "max"
  }'
```

### 10. Channel Intro/Outro Generation

```bash
# Create channel intro
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 5-second YouTube channel intro for a cooking channel called \"Kitchen Creations\". Animated logo reveal with steam/smoke effects, wooden textures, warm colors. Include a brief jingle spot. Professional but inviting. 16:9 at 1920x1080.",
    "session_id": "cooking-channel-branding"
  }'

# Create matching outro (same session for consistency)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Now create a matching 10-second outro for the same channel. Include animated end screen with subscribe button, two video placeholders for suggested videos, and social media icons. Match the style and colors of the intro we just created.",
    "session_id": "cooking-channel-branding"
  }'
```

## Best Practices

### Long-form Videos (16:9)
- **Hook viewers early**: First 5-10 seconds are critical for retention
- **Consistent pacing**: Maintain visual interest with scene changes every 5-10 seconds
- **Clear structure**: Use visual chapters and segment markers
- **End screens**: Design for YouTube's end screen overlay (last 20 seconds)
- **Thumbnails**: Create compelling 1280x720 thumbnails that stand out

### YouTube Shorts (9:16)
- **Vertical optimization**: Design for full-screen mobile viewing
- **Instant hook**: Capture attention in the first 1-2 seconds
- **Loop-friendly**: Create seamless loops when possible
- **Bold text**: Use large, readable captions for sound-off viewing
- **Keep it snappy**: Even though 3 minutes is allowed, 30-60 seconds often performs best

### Thumbnails
- **High contrast**: Use colors that pop against YouTube's white/dark UI
- **Readable text**: Limit to 3-5 words maximum
- **Faces work**: Expressive faces increase click-through rates
- **Consistent branding**: Maintain channel aesthetic across thumbnails

## Prompt Tips for YouTube Videos

When creating YouTube content, include these details in your prompt:

1. **Format**: Specify long-form (16:9) or Shorts (9:16)
2. **Resolution**: 1920x1080 for videos, 1280x720 for thumbnails
3. **Duration**: Be specific about video length
4. **Style**: Describe the visual aesthetic (cinematic, minimal, energetic, etc.)
5. **Content Type**: Faceless, tutorial, review, compilation, etc.
6. **Target Audience**: Who is this video for?
7. **Text/Captions**: Whether to include text overlays
8. **Music/Mood**: Describe the audio atmosphere

### Example Prompt Structure

```
"Create a [duration] [format] YouTube [video type] about [topic].
Include [visual elements] with [style/aesthetic].
Target audience: [demographic].
[Additional requirements like text overlays, music style, transitions, etc.]
Resolution: [1920x1080 or 1080x1920]"
```

## Mode Selection

Ask your users before generating:

**"Do you want fast & cheap, or high quality?"**

| Mode | Best For | Speed | Quality |
|------|----------|-------|---------|
| `max` | Final videos, published content, high production value | Slower | Highest |
| `eco` | Quick drafts, concept testing, storyboard visualization | Faster | Good |

## Multi-Turn Creative Iteration

Use `session_id` to iterate on video content:

```bash
# Initial video concept
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 30-second YouTube Short about morning productivity tips",
    "session_id": "productivity-short-001"
  }'

# Iterate based on feedback
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Make the transitions faster and add more energetic text animations. Also add a stronger hook in the first 2 seconds.",
    "session_id": "productivity-short-001"
  }'

# Create thumbnail for the video
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a thumbnail for this video at 1280x720. Make it eye-catching with bold text saying \"5 AM ROUTINE\" and show a sunrise with productivity imagery.",
    "session_id": "productivity-short-001"
  }'
```

## Content Series Generation

Generate consistent content for a video series:

```bash
# Episode 1
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create episode 1 of a \"World Mysteries\" series - focus on the Bermuda Triangle. 2 minutes, dramatic documentary style, 16:9 at 1920x1080.",
    "session_id": "world-mysteries-series",
    "mode": "max"
  }'

# Episode 2 (same session for style consistency)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create episode 2 about Stonehenge. Keep the same visual style, intro, and format as episode 1.",
    "session_id": "world-mysteries-series",
    "mode": "max"
  }'
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | Insufficient balance | Top up at eachlabs.ai |
| Content policy violation | Prohibited content | Adjust prompt to comply with content policies |
| Timeout | Complex/long video generation | Set client timeout to minimum 10 minutes |

## Related Skills

- `each-sense` - Core API documentation
- `meta-ad-creative-generation` - Meta/Facebook ad creatives
- `tiktok-ad-creative-generation` - TikTok ad creatives
- `video-generation` - General video generation
