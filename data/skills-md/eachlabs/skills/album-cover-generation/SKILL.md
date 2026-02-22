---
name: album-cover-generation
description: Generate professional music album covers using each::sense AI. Create artwork for hip-hop, rock, pop, electronic, jazz, classical, indie albums, singles, EPs, and Spotify canvas visuals.
metadata:
  author: eachlabs
  version: "1.0"
---

# Album Cover Generation

Generate stunning, professional album artwork using each::sense. This skill creates high-quality visuals for music releases across all genres, optimized for streaming platforms, digital distribution, and physical media.

## Features

- **Full Album Covers**: Standard 3000x3000 px artwork for all platforms
- **Singles Artwork**: Eye-catching visuals for single releases
- **EP Covers**: Cohesive artwork for extended plays
- **Spotify Canvas**: Vertical animated visuals for streaming
- **Genre-Specific Styles**: Hip-hop, rock, pop, electronic, jazz, classical, indie
- **Multi-Turn Iteration**: Refine artwork through conversation
- **Consistent Branding**: Maintain artist visual identity across releases

## Quick Start

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 3000x3000 album cover for a hip-hop album called \"Midnight Dreams\". Dark city skyline at night, neon lights reflecting on wet streets, cinematic and moody atmosphere.",
    "mode": "max"
  }'
```

## Album Cover Formats & Sizes

| Format | Aspect Ratio | Recommended Size | Use Case |
|--------|--------------|------------------|----------|
| Album Cover | 1:1 | 3000x3000 px | Standard for all platforms |
| Single Artwork | 1:1 | 3000x3000 px | Single releases |
| EP Cover | 1:1 | 3000x3000 px | Extended play releases |
| Spotify Canvas | 9:16 | 1080x1920 px | Animated vertical video |
| Vinyl Cover | 1:1 | 3000x3000 px | Physical vinyl packaging |
| CD Booklet | 1:1 | 3000x3000 px | Physical CD packaging |

## Use Case Examples

### 1. Hip-Hop/Rap Album Cover

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 3000x3000 hip-hop album cover for \"Street Chronicles\". Urban environment with graffiti walls, gold chains aesthetic, dark moody lighting with purple and gold accents. Leave space at bottom for artist name and album title. Gritty, authentic street vibe.",
    "mode": "max"
  }'
```

### 2. Rock/Metal Album Cover

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 3000x3000 heavy metal album cover for \"Eternal Flames\". Epic dark fantasy scene with a burning skull, lightning storms, gothic cathedral ruins in the background. High contrast, dramatic red and black color scheme. Classic metal album art style like Iron Maiden or Metallica.",
    "mode": "max"
  }'
```

### 3. Pop Album Cover

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 3000x3000 pop album cover for \"Sunshine State\". Bright, colorful aesthetic with pastel gradients (pink, blue, yellow). Abstract geometric shapes, playful and energetic mood. Modern, clean design that appeals to Gen-Z. Think Dua Lipa or Ariana Grande album vibes.",
    "mode": "max"
  }'
```

### 4. Electronic/EDM Album Cover

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 3000x3000 electronic music album cover for \"Neon Pulse\". Futuristic cyberpunk cityscape, glowing neon lights in cyan and magenta, digital glitch effects, synthwave aesthetic. Dark background with vibrant light trails. High-tech, immersive club atmosphere.",
    "mode": "max"
  }'
```

### 5. Jazz Album Cover

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 3000x3000 jazz album cover for \"Blue Notes After Dark\". Classic Blue Note Records inspired design. Abstract illustration of a saxophone player silhouette, smoky jazz club atmosphere. Two-tone color palette (deep blue and cream). Minimalist, sophisticated, vintage 1960s jazz aesthetic.",
    "mode": "max"
  }'
```

### 6. Classical Album Cover

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 3000x3000 classical music album cover for \"Symphonic Visions\". Elegant and timeless design featuring a grand concert hall interior with golden chandeliers, velvet curtains. Soft, warm lighting. Refined and prestigious aesthetic suitable for an orchestra recording. Deutsche Grammophon style.",
    "mode": "max"
  }'
```

### 7. Indie/Alternative Album Cover

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 3000x3000 indie album cover for \"Suburban Daydreams\". Nostalgic, dreamy aesthetic with faded film photography look. Empty suburban street at golden hour, lo-fi grainy texture. Melancholic but beautiful mood. Think Bon Iver, Phoebe Bridgers, or The National album art style.",
    "mode": "max"
  }'
```

### 8. Single Artwork

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 3000x3000 single artwork for a song called \"Heartbeat\". Minimalist design with a stylized anatomical heart in neon red against a pure black background. Simple, bold, and immediately recognizable. Modern and striking for streaming thumbnail visibility.",
    "mode": "max"
  }'
```

### 9. EP Cover

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 3000x3000 EP cover for a 5-track R&B EP called \"Velvet Nights\". Luxurious, sensual aesthetic with deep purple velvet textures, soft ambient lighting, rose petals. Intimate and romantic mood. High-end, premium feel for an R&B/soul artist.",
    "mode": "max"
  }'
```

### 10. Spotify Canvas (Vertical Animated)

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 9:16 vertical video for Spotify Canvas, 8 seconds long. Looping animation of abstract colorful paint swirls flowing upward, psychedelic and hypnotic movement. Vibrant colors (orange, pink, purple) blending smoothly. Seamless loop for continuous playback on Spotify.",
    "mode": "max"
  }'
```

## Best Practices

### Design Principles
- **Thumbnail Clarity**: Design must be recognizable at small sizes (300x300 thumbnails)
- **Text Placement**: Leave 10-15% margin for artist name and album title
- **Color Contrast**: Use high contrast to stand out in streaming platform grids
- **Genre Authenticity**: Match visual style to the music genre expectations
- **Consistency**: Maintain visual identity across single and album releases

### Technical Requirements
- **Resolution**: Always request 3000x3000 for maximum quality
- **Aspect Ratio**: Standard album covers must be 1:1 square
- **Safe Zones**: Keep critical elements away from edges (may be cropped on some platforms)
- **File Delivery**: Output URLs provide high-resolution PNG/JPG files

### Platform Considerations
- **Spotify**: Requires 1:1 square, recommends 3000x3000
- **Apple Music**: Requires 1:1 square, supports up to 4000x4000
- **YouTube Music**: Requires 1:1 square
- **Bandcamp**: Supports various ratios but 1:1 recommended
- **Spotify Canvas**: Requires 9:16 vertical video, 3-8 seconds, loops seamlessly

## Prompt Tips for Album Covers

When creating album artwork, include these details in your prompt:

1. **Genre**: Specify the music genre for appropriate visual style
2. **Album/Song Title**: Include the title for thematic inspiration
3. **Mood**: Dark, uplifting, nostalgic, energetic, melancholic, etc.
4. **Color Palette**: Specific colors or color scheme preferences
5. **Visual Elements**: Key imagery, symbols, or scenes
6. **Style Reference**: Mention similar artists or album art styles
7. **Text Space**: Request space for title and artist name placement

### Example Prompt Structure

```
"Create a [size] [genre] album cover for [title].
[Visual description] with [mood/atmosphere].
[Color scheme]. [Style reference].
[Additional requirements like text space, effects, etc.]"
```

## Mode Selection

Ask your users before generating:

**"Do you want fast & cheap, or high quality?"**

| Mode | Best For | Speed | Quality |
|------|----------|-------|---------|
| `max` | Final release artwork, commercial releases | Slower | Highest |
| `eco` | Quick concepts, draft exploration, A/B testing | Faster | Good |

## Multi-Turn Creative Iteration

Use `session_id` to iterate on album artwork:

```bash
# Initial concept
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 3000x3000 album cover for an ambient electronic album. Minimal, atmospheric, space theme.",
    "session_id": "album-project-001"
  }'

# Refine based on feedback
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Make it darker with more contrast. Add subtle star field in the background and a gradient from deep blue to black.",
    "session_id": "album-project-001"
  }'

# Request variations
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create 2 more variations with different color schemes - one in purple tones and one in warm orange/red sunset colors.",
    "session_id": "album-project-001"
  }'
```

## Cohesive Release Strategy

Generate matching artwork for album, singles, and promotional materials:

```bash
# Main album cover
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 3000x3000 album cover for \"Fragments\" by an indie band. Shattered mirror aesthetic with warm golden light fragments. Artistic and abstract.",
    "session_id": "fragments-album-campaign"
  }'

# Single artwork (same session for consistency)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create single artwork for the lead single from the same album. Use the same visual language but focus on a single large fragment. Maintain the color palette.",
    "session_id": "fragments-album-campaign"
  }'

# Spotify Canvas
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 9:16 Spotify Canvas video using the same shattered mirror aesthetic. Slow motion fragments floating and rotating, 6 seconds, seamless loop.",
    "session_id": "fragments-album-campaign"
  }'
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | Insufficient balance | Top up at eachlabs.ai |
| Content policy violation | Prohibited content | Adjust prompt to comply with content guidelines |
| Timeout | Complex generation | Set client timeout to minimum 10 minutes |

## Related Skills

- `each-sense` - Core API documentation
- `product-photo-generation` - Product photography for merchandise
- `social-media-content` - Social media promotional graphics
