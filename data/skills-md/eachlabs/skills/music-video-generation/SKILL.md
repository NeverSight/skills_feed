---
name: music-video-generation
description: Generate music videos using each::sense AI. Create visualizers, lyric videos, animated music videos, concert visuals, and genre-specific aesthetics synchronized to audio.
metadata:
  author: eachlabs
  version: "1.0"
---

# Music Video Generation

Generate stunning music videos using each::sense. This skill creates visualizers, lyric videos, animated sequences, and cinematic music videos synchronized to your audio tracks.

## Features

- **Audio Visualizers**: Reactive visual patterns synced to audio frequencies
- **Lyric Videos**: Animated typography with song lyrics
- **Abstract Visuals**: Artistic, non-representational video content
- **Artist Performance**: Simulated artist or band performance footage
- **Animated Music Videos**: Cartoon, anime, or stylized animation
- **Concert Visuals**: LED wall content and stage projections
- **Album Art Animation**: Bring static album artwork to life
- **Beat-Synced Content**: Visuals that react to rhythm and tempo
- **Genre-Specific Aesthetics**: Hip-hop, EDM, rock, pop styling

## Quick Start

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an audio visualizer video with neon geometric shapes that pulse to the beat, dark background with vibrant colors",
    "mode": "max"
  }'
```

## Video Formats & Aspect Ratios

| Platform | Aspect Ratio | Resolution | Use Case |
|----------|--------------|------------|----------|
| YouTube | 16:9 | 1920x1080 | Standard music video |
| YouTube Shorts | 9:16 | 1080x1920 | Vertical clips, previews |
| Instagram Reels | 9:16 | 1080x1920 | Social promotion |
| TikTok | 9:16 | 1080x1920 | Viral clips |
| Square | 1:1 | 1080x1080 | Instagram feed, Spotify Canvas |
| Ultrawide | 21:9 | 2560x1080 | Concert LED walls |

## Use Case Examples

### 1. Audio Visualizer from Track

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 16:9 audio visualizer video. Circular waveform in the center with particles emanating outward on each beat. Deep purple and electric blue color palette. Dark space background with subtle stars. 10 seconds loop.",
    "mode": "max"
  }'
```

### 2. Lyric Video Generation

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a lyric video for the lyrics: \"Running through the night, chasing starlight, we are infinite tonight\". Animated text appearing word by word with a dreamy night sky background. Stars twinkling, soft gradient from dark blue to purple. Modern sans-serif font with subtle glow effect. 16:9 aspect ratio.",
    "mode": "max"
  }'
```

### 3. Abstract Music Visuals

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate abstract music visuals for an ambient electronic track. Flowing liquid metal morphing shapes, iridescent surfaces reflecting rainbow colors, slow hypnotic movement. Think art installation meets music video. 16:9, 15 seconds.",
    "mode": "max"
  }'
```

### 4. Artist Performance Video

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a music video showing a female singer performing on a dark stage. Dramatic spotlight lighting, smoke effects, cinematic camera movement circling the performer. She is wearing an elegant black dress, passionate emotional performance. 16:9 widescreen, film grain aesthetic.",
    "mode": "max"
  }'
```

### 5. Animated Music Video (Anime Style)

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an anime-style animated music video. A young character with colorful hair running through a neon-lit cyberpunk city at night. Dynamic action poses, speed lines, rain effects. Japanese anime aesthetic like Studio Trigger. High energy and dramatic. 16:9.",
    "mode": "max"
  }'
```

### 6. Concert LED Wall Visuals

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate concert visuals for LED wall projection. Abstract geometric patterns - triangles and hexagons morphing and pulsing. High contrast black and white with occasional bursts of red. Designed for live performance, loopable, high impact visuals that work on massive screens. 21:9 ultrawide aspect ratio.",
    "mode": "max"
  }'
```

### 7. Album Art Animation (Spotify Canvas)

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a Spotify Canvas style animation from album art concept. A surreal landscape with floating islands and waterfalls going upward. Soft pastel colors - pink clouds, turquoise water, golden sunset light. Subtle parallax motion, dreamy and ethereal mood. 9:16 vertical format, 8 second seamless loop.",
    "mode": "max"
  }'
```

### 8. Beat-Synced Visuals

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create beat-synced visuals for a 120 BPM track. Geometric shapes (cubes, spheres, pyramids) that flash and transform on each beat. Strobe-like intensity changes. Black background with neon pink, cyan, and yellow shapes. High energy, rave aesthetic. Design cuts to happen every 0.5 seconds to match tempo. 16:9.",
    "mode": "max"
  }'
```

### 9. Genre-Specific Aesthetics (Hip-Hop)

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a hip-hop music video aesthetic. Urban street scene at night, street lights with lens flares, graffiti walls, luxury cars in background. Slow motion rain falling. Moody cinematic color grading - teal shadows and orange highlights. Trap music vibe, high production value look. 16:9 widescreen.",
    "mode": "max"
  }'
```

### 10. Story-Driven Music Video

```bash
# Part 1: Opening scene
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create the opening scene of a narrative music video. A lonely figure standing at a train station at dawn. Empty platform, morning mist, warm golden light breaking through clouds. Melancholic mood, cinematic widescreen composition. The character is looking at a departing train. 16:9.",
    "session_id": "music-video-story-001",
    "mode": "max"
  }'

# Part 2: Middle scene (same session for consistency)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create the next scene continuing our music video story. The same character is now walking through a sunlit field of wildflowers. Memories and flashbacks - double exposure effect showing happy moments. Bittersweet emotion, hope emerging. Maintain the same cinematic color grading and style.",
    "session_id": "music-video-story-001",
    "mode": "max"
  }'

# Part 3: Final scene
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create the final climactic scene of our music video. The character reunites with a loved one on a rooftop at sunset. City skyline in background, warm embrace, emotional payoff. Golden hour lighting, lens flares, cinematic slow motion. End on a hopeful note with them looking at the horizon together.",
    "session_id": "music-video-story-001",
    "mode": "max"
  }'
```

## Best Practices

### Visual Design
- **Color Consistency**: Maintain a cohesive color palette throughout the video
- **Motion Pacing**: Match visual intensity to music energy levels
- **Safe Zones**: For social platforms, keep key elements away from edges
- **Loop Points**: Design seamless loops for visualizers and short clips
- **Text Readability**: For lyric videos, ensure text contrasts with background

### Technical Considerations
- **Beat Timing**: Specify BPM when possible for beat-synced content
- **Duration**: Keep clips between 5-30 seconds for optimal generation
- **Looping**: Request seamless loops explicitly for repeated playback
- **Platform Specs**: Always specify aspect ratio for target platform

### Genre Guidelines
| Genre | Visual Style | Color Palette | Motion |
|-------|-------------|---------------|--------|
| EDM/Electronic | Geometric, neon, futuristic | Bright neons, RGB | Fast, energetic |
| Hip-Hop/Rap | Urban, luxury, cinematic | Dark with gold/teal | Slow-mo, dramatic |
| Rock/Metal | Gritty, high contrast | Dark, red, monochrome | Intense, chaotic |
| Pop | Colorful, polished, fun | Bright, pastel | Smooth, bouncy |
| Ambient/Chill | Abstract, flowing | Soft gradients | Slow, hypnotic |
| Indie/Alternative | Vintage, artistic | Muted, film tones | Organic, natural |

## Prompt Tips for Music Videos

When creating music videos, include these details:

1. **Genre/Mood**: What type of music and emotional tone
2. **Visual Style**: Realistic, animated, abstract, etc.
3. **Color Palette**: Specific colors or general mood
4. **Aspect Ratio**: 16:9, 9:16, 1:1, or 21:9
5. **Duration**: How long the clip should be
6. **Motion Style**: Fast cuts, slow motion, smooth, etc.
7. **Key Elements**: What should appear in the video
8. **Loop Requirement**: Whether it needs to loop seamlessly

### Example Prompt Structure

```
"Create a [duration] [genre] music video in [aspect ratio].
Visual style: [style description].
Show [key visual elements].
Color palette: [colors].
Mood: [emotional tone].
[Additional requirements like looping, beat-sync, etc.]"
```

## Mode Selection

**"Do you want fast & cheap, or high quality?"**

| Mode | Best For | Speed | Quality |
|------|----------|-------|---------|
| `max` | Final releases, official videos, premium content | Slower | Highest |
| `eco` | Quick concepts, social clips, iteration | Faster | Good |

## Multi-Turn Creative Iteration

Use `session_id` to iterate and build upon your music video:

```bash
# Initial concept
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a visualizer with glowing orbs floating in space",
    "session_id": "visualizer-project-001"
  }'

# Refine based on result
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Add more particle trails to the orbs and make the colors shift from blue to purple",
    "session_id": "visualizer-project-001"
  }'

# Create variation
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a more intense version of this for the chorus section with faster movement",
    "session_id": "visualizer-project-001"
  }'
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | Insufficient balance | Top up at eachlabs.ai |
| Content policy violation | Prohibited content | Adjust prompt to comply with content policies |
| Timeout | Complex generation | Set client timeout to minimum 10 minutes |

## Related Skills

- `each-sense` - Core API documentation
- `video-generation` - General video generation
- `image-generation` - Static artwork and stills
- `audio-generation` - Music and sound creation
