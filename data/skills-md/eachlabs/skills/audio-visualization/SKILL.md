---
name: audio-visualization
description: Generate audio visualization videos using each::sense AI. Create waveforms, spectrum analyzers, particle effects, 3D visualizations, and beat-synced animations from audio files.
metadata:
  author: eachlabs
  version: "1.0"
---

# Audio Visualization

Generate stunning audio visualization videos using each::sense. This skill creates dynamic visual representations of audio including waveforms, spectrum analyzers, particle effects, 3D visualizations, and beat-synced animations.

## Features

- **Waveform Visualizers**: Classic oscilloscope-style audio waveforms
- **Spectrum Analyzers**: Frequency bar visualizations with customizable styles
- **Circular Visualizers**: Radial audio-reactive designs
- **Particle Systems**: Audio-driven particle effects and explosions
- **3D Visualizations**: Immersive three-dimensional audio landscapes
- **Abstract Reactives**: Artistic, abstract audio-responsive visuals
- **Podcast Waveforms**: Clean, minimal waveforms for podcasts and voice content
- **Music Videos**: Full music video visualizers with effects
- **Beat-Synced Animations**: Animations perfectly timed to beats and rhythm
- **Branded Visualizers**: Custom branded audio visualizations

## Quick Start

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a neon waveform visualizer video for this electronic music track, purple and cyan colors, 16:9 format",
    "mode": "max",
    "audio_urls": ["https://example.com/music-track.mp3"]
  }'
```

## Visualization Styles

| Style | Description | Best For |
|-------|-------------|----------|
| Waveform | Classic oscilloscope wave patterns | Music, podcasts, voice |
| Spectrum Bars | Frequency analyzer bars | EDM, electronic music |
| Circular | Radial audio-reactive rings | Album art, social media |
| Particle | Audio-driven particle systems | Dramatic, energetic tracks |
| 3D Landscape | Three-dimensional terrain/shapes | Immersive content |
| Abstract | Artistic fluid/geometric patterns | Creative, artistic videos |
| Minimal | Clean, simple waveforms | Podcasts, interviews |

## Use Case Examples

### 1. Waveform Visualizer

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a smooth waveform visualizer video for this audio. Use a gradient from electric blue to pink, dark background, 1080p 16:9 format. The waveform should be centered and react smoothly to the audio frequencies.",
    "mode": "max",
    "audio_urls": ["https://example.com/song.mp3"]
  }'
```

### 2. Spectrum Analyzer Bars

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate a spectrum analyzer visualization with vertical bars that react to the music. EDM style with neon green and yellow gradient bars on a black background. Add glow effects and mirror reflection at the bottom. 1920x1080 landscape video.",
    "mode": "max",
    "audio_urls": ["https://example.com/edm-track.mp3"]
  }'
```

### 3. Circular Audio Visualizer

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a circular audio visualizer with radial bars emanating from the center. Place an album art placeholder in the center circle. Use warm orange and red colors with a subtle pulsing glow effect. Square 1:1 format for social media.",
    "mode": "max",
    "audio_urls": ["https://example.com/album-track.mp3"]
  }'
```

### 4. Particle-Based Visualizer

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate an audio-reactive particle system visualization. Particles should explode outward on bass hits and swirl gently during quieter sections. Use a cosmic color palette with blues, purples, and white sparkles. Deep space background. 16:9 HD video.",
    "mode": "max",
    "audio_urls": ["https://example.com/electronic.mp3"]
  }'
```

### 5. 3D Audio Visualization

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 3D audio visualization with a geometric landscape that responds to the music. The terrain should rise and fall with the frequencies, camera slowly moving forward through the scene. Synthwave aesthetic with neon grid lines, pink and cyan lighting. 1080p cinematic format.",
    "mode": "max",
    "audio_urls": ["https://example.com/synthwave.mp3"]
  }'
```

### 6. Abstract Reactive Visuals

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate abstract audio-reactive visuals with fluid, organic shapes that morph and flow with the music. Use a dreamy color palette with soft pastels transitioning through the spectrum. The visuals should feel like living art, responding to both rhythm and melody. Vertical 9:16 format for Instagram Reels.",
    "mode": "max",
    "audio_urls": ["https://example.com/ambient-track.mp3"]
  }'
```

### 7. Podcast Waveform Video

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a clean, minimal podcast waveform video. Simple horizontal waveform bar in the center that responds to voice audio. White waveform on a dark gray background. Leave space at the top for a podcast title and bottom for episode info. Professional and clean look. Square 1:1 format.",
    "mode": "eco",
    "audio_urls": ["https://example.com/podcast-episode.mp3"]
  }'
```

### 8. Music Video Visualizer

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a full music video visualizer combining multiple effects. Start with abstract flowing shapes, transition to particle bursts during the chorus, and include subtle waveform elements throughout. High energy, colorful, psychedelic style matching the energetic music. 1920x1080 landscape format, full track length.",
    "mode": "max",
    "audio_urls": ["https://example.com/full-song.mp3"]
  }'
```

### 9. Beat-Synced Animation

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate a beat-synced animation where geometric shapes pulse, rotate, and transform exactly on the beat. Sharp, precise animations on every kick drum and snare hit. Minimal black and white design with red accent flashes on the strongest beats. Perfect sync is critical. 16:9 HD video.",
    "mode": "max",
    "audio_urls": ["https://example.com/drum-track.mp3"]
  }'
```

### 10. Custom Branded Visualizer

```bash
# Initial branded visualizer
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a branded audio visualizer for a record label. Use brand colors: deep purple (#6B21A8) and gold (#F59E0B). Include a circular visualizer with space in the center for a logo. Add a subtle animated gradient background. Professional, premium feel. 1:1 square format for social media.",
    "mode": "max",
    "audio_urls": ["https://example.com/label-release.mp3"],
    "session_id": "branded-viz-001"
  }'

# Iterate on the design
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Add more gold particle sparkles that react to high frequencies, and make the purple glow more intense on bass hits",
    "session_id": "branded-viz-001"
  }'
```

## Best Practices

### Audio Quality
- **File Formats**: MP3, WAV, FLAC, AAC supported
- **Sample Rate**: 44.1kHz or higher recommended
- **Clear Audio**: Clean audio produces better visualizations
- **Volume Levels**: Normalized audio prevents clipping in visuals

### Visual Design
- **Contrast**: High contrast between visuals and background
- **Color Harmony**: Use complementary or analogous color schemes
- **Responsiveness**: Match visual intensity to audio dynamics
- **Safe Zones**: Leave margins for platform UI overlays

### Format Guidelines

| Platform | Aspect Ratio | Resolution | Notes |
|----------|--------------|------------|-------|
| YouTube | 16:9 | 1920x1080 | Landscape, full HD |
| Instagram Post | 1:1 | 1080x1080 | Square format |
| Instagram Reels | 9:16 | 1080x1920 | Vertical, Stories compatible |
| TikTok | 9:16 | 1080x1920 | Vertical format |
| Spotify Canvas | 9:16 | 720x1280 | 3-8 second loops |
| SoundCloud | 16:9 | 1280x720 | Waveform style popular |

## Prompt Tips for Audio Visualization

Include these details in your prompts:

1. **Visualization Type**: Waveform, spectrum, circular, particle, 3D, abstract
2. **Color Scheme**: Specific colors, gradients, or palette style
3. **Background**: Solid, gradient, animated, space, etc.
4. **Effects**: Glow, blur, reflection, particles, trails
5. **Reactivity**: What responds to bass, mids, highs, beats
6. **Format**: Aspect ratio and resolution
7. **Style**: EDM, minimal, psychedelic, corporate, etc.
8. **Branding**: Space for logos, text overlays

### Example Prompt Structure

```
"Create a [visualization type] for [audio type/genre].
Use [color scheme] with [background style].
Add [effects] that react to [audio elements].
[Format and resolution]. [Style description]."
```

## Mode Selection

**"Do you want fast & cheap, or high quality?"**

| Mode | Best For | Speed | Quality |
|------|----------|-------|---------|
| `max` | Final releases, music videos, premium content | Slower | Highest |
| `eco` | Drafts, previews, social media clips, podcasts | Faster | Good |

## Multi-Turn Creative Iteration

Use `session_id` to iterate on visualizations:

```bash
# Initial visualization
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a spectrum analyzer visualization for this EDM track",
    "audio_urls": ["https://example.com/track.mp3"],
    "session_id": "viz-project-001"
  }'

# Refine colors
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Change the color scheme to cyan and magenta, add more glow",
    "session_id": "viz-project-001"
  }'

# Add effects
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Add particle trails on the peaks and a subtle mirror reflection",
    "session_id": "viz-project-001"
  }'
```

## Batch Generation for Multiple Tracks

```bash
# Track 1
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a circular visualizer for this track, purple and blue colors",
    "mode": "eco",
    "audio_urls": ["https://example.com/track1.mp3"]
  }'

# Track 2 (same style)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a circular visualizer for this track, same purple and blue style as track1",
    "mode": "eco",
    "audio_urls": ["https://example.com/track2.mp3"]
  }'
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | Insufficient balance | Top up at eachlabs.ai |
| Audio processing failed | Unsupported format or corrupted file | Use MP3/WAV, check file integrity |
| Timeout | Long audio or complex visualization | Set client timeout to minimum 10 minutes |
| Sync issues | Complex beat detection | Provide clear, well-mastered audio |

## Related Skills

- `each-sense` - Core API documentation
- `music-generation` - AI music creation
- `video-generation` - General video creation
- `video-editing` - Post-production editing
