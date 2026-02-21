---
name: poster-design-generation
description: Generate professional poster designs using each::sense AI. Create movie posters, event posters, motivational posters, product launch visuals, vintage designs, travel posters, and more with AI-powered creative generation.
metadata:
  author: eachlabs
  version: "1.0"
---

# Poster Design Generation

Generate stunning, professional poster designs using each::sense. This skill creates high-quality poster artwork for movies, events, products, travel, sports, social causes, and various creative applications.

## Features

- **Movie Posters**: Cinematic key art with dramatic compositions and typography space
- **Event/Concert Posters**: Eye-catching promotional materials for live events
- **Motivational Posters**: Inspirational designs with impactful imagery
- **Product Launch Posters**: Commercial visuals for product announcements
- **Minimalist Art Posters**: Clean, modern aesthetic designs
- **Vintage/Retro Posters**: Classic styles from various eras
- **Travel Destination Posters**: Tourism and wanderlust-inspiring visuals
- **Sports Event Posters**: Dynamic athletic promotional materials
- **Educational/Infographic Posters**: Information-rich visual designs
- **Social Cause Posters**: Awareness and advocacy campaign visuals

## Quick Start

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a dramatic movie poster for a sci-fi thriller, dark atmosphere with neon accents, leave space at top for title",
    "mode": "max"
  }'
```

## Common Poster Sizes & Formats

| Type | Aspect Ratio | Recommended Size | Use Case |
|------|--------------|------------------|----------|
| Movie Poster | 2:3 | 1080x1620 | Theater posters, key art |
| Event Poster | 11:17 | 1100x1700 | Concert flyers, event promos |
| Square Poster | 1:1 | 1080x1080 | Social media, album art |
| Horizontal | 16:9 | 1920x1080 | Digital displays, banners |
| Vertical | 9:16 | 1080x1920 | Mobile, digital signage |
| A-Series | ~1:1.414 | 2480x3508 (A4) | Print posters |

## Use Case Examples

### 1. Movie Poster Design

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 2:3 movie poster for a psychological thriller. A silhouette of a man standing at the edge of a foggy cliff, moody blue and grey tones, cinematic lighting with dramatic shadows. Leave space at the top third for the movie title and bottom for credits. Hollywood blockbuster quality.",
    "mode": "max"
  }'
```

### 2. Event/Concert Poster

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Design an 11:17 concert poster for an electronic music festival. Vibrant neon colors, abstract geometric shapes, laser beams and light effects, futuristic cyberpunk aesthetic. Include visual space for artist names at the top and event details at the bottom. High energy, rave culture vibes.",
    "mode": "max"
  }'
```

### 3. Motivational Poster

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an inspirational motivational poster. A lone climber reaching the summit of a mountain at sunrise, golden light breaking through clouds, epic landscape vista. Vertical 2:3 format with space at the bottom for an inspirational quote. Awe-inspiring, triumphant mood.",
    "mode": "max"
  }'
```

### 4. Product Launch Poster

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Design a sleek product launch poster for a new smartphone. The phone floating in center with dynamic light trails and particle effects around it, dark premium background with subtle gradient. Modern tech aesthetic, Apple-style minimalism. 2:3 vertical format with space for product name and tagline.",
    "mode": "max"
  }'
```

### 5. Minimalist Art Poster

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a minimalist art poster in the style of Scandinavian design. Simple geometric shapes, limited color palette of terracotta, sage green, and cream. Abstract composition suggesting a landscape. Clean lines, modern aesthetic suitable for home decor. 3:4 vertical format.",
    "mode": "max"
  }'
```

### 6. Vintage/Retro Poster

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Design a vintage 1950s travel poster style artwork. Classic American diner scene with neon signs, chrome details, and a classic car. Retro color palette with faded pastels, mid-century illustration style with visible brush strokes. Include decorative border typical of the era. 2:3 format.",
    "mode": "max"
  }'
```

### 7. Travel Destination Poster

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a travel poster for Tokyo, Japan. Cherry blossoms in the foreground, Mount Fuji in the distance, traditional temples mixed with modern skyscrapers. Warm sunset colors, dreamy wanderlust aesthetic. Art deco travel poster style with bold shapes. 2:3 vertical with space for destination name at bottom.",
    "mode": "max"
  }'
```

### 8. Sports Event Poster

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Design a dynamic basketball championship poster. Action shot of a player mid-dunk, explosive energy with motion blur and particle effects, dramatic stadium lighting. Bold colors - deep blue and orange. High contrast, intense competitive spirit. 11:17 format with space for event title and date.",
    "mode": "max"
  }'
```

### 9. Educational/Infographic Poster

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an educational poster about the solar system. Visually stunning representation of planets in orbit around the sun, accurate relative sizes and colors, space background with stars and nebulae. Scientific but visually appealing, suitable for a classroom or museum. 16:9 horizontal format with areas for planet labels.",
    "mode": "max"
  }'
```

### 10. Social Cause/Awareness Poster

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Design a powerful environmental awareness poster about ocean conservation. A beautiful sea turtle swimming through crystal clear water, but with subtle hints of pollution in the background. Emotional, thought-provoking imagery that inspires action. Blue and green tones. 2:3 vertical format with space for campaign message.",
    "mode": "max"
  }'
```

## Best Practices

### Composition & Layout
- **Typography Space**: Always request space for titles, headlines, and text overlays
- **Safe Zones**: Leave margins for print bleeding and important content
- **Focal Point**: Define a clear visual hierarchy and center of attention
- **Balance**: Specify if you want symmetrical or asymmetrical composition

### Visual Style
- **Color Palette**: Mention specific colors or mood-based palettes (warm, cool, vibrant, muted)
- **Lighting**: Describe lighting direction, quality, and atmosphere
- **Style Reference**: Reference art movements, eras, or specific design styles
- **Texture**: Request specific textures (grain, noise, paper, digital clean)

### Format Guidelines
- **Aspect Ratio**: Always specify the desired ratio for your use case
- **Resolution**: Higher resolution for print, standard for digital
- **Orientation**: Vertical (portrait) is standard for most posters

## Prompt Tips for Poster Design

When creating poster designs, include these details in your prompt:

1. **Purpose**: What is the poster for? (movie, event, product, etc.)
2. **Format**: Specify aspect ratio (2:3, 11:17, 1:1, etc.)
3. **Style**: Art style or era (minimalist, vintage, modern, etc.)
4. **Subject**: Main visual elements and composition
5. **Color Palette**: Specific colors or mood-based palette
6. **Typography Space**: Where text will be placed
7. **Mood/Atmosphere**: Emotional tone of the design

### Example Prompt Structure

```
"Create a [format/ratio] [type] poster for [purpose].
[Visual description of main subject and composition].
[Style and aesthetic references].
[Color palette and lighting].
Leave space at [position] for [text elements]."
```

## Mode Selection

Ask your users before generating:

**"Do you want fast & cheap, or high quality?"**

| Mode | Best For | Speed | Quality |
|------|----------|-------|---------|
| `max` | Final poster designs, print-ready artwork | Slower | Highest |
| `eco` | Quick drafts, concept exploration, style testing | Faster | Good |

## Multi-Turn Creative Iteration

Use `session_id` to iterate on poster designs:

```bash
# Initial concept
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a movie poster for a horror film, dark forest setting with fog",
    "session_id": "horror-poster-001",
    "mode": "max"
  }'

# Refine the design
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Add a creepy abandoned house in the background, and make the color palette more red and black",
    "session_id": "horror-poster-001"
  }'

# Request variations
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create 2 more variations with different compositions - one more minimal, one more intense",
    "session_id": "horror-poster-001"
  }'
```

## Poster Series Generation

Generate consistent poster series for campaigns:

```bash
# Series poster 1
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create poster 1 of 4 for a summer music festival series. Beach sunset theme, vibrant orange and pink. Feature a DJ silhouette.",
    "session_id": "festival-series-2024",
    "mode": "max"
  }'

# Series poster 2 (maintains consistency)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create poster 2 of 4 for the same series. Same color palette and style, but feature a live band on stage.",
    "session_id": "festival-series-2024"
  }'
```

## Using Reference Images

Enhance poster generation with reference images:

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a movie poster using this actor photo as the main character. Dramatic noir style, high contrast black and white with one accent color (red). Add rain effects and city silhouette in background.",
    "mode": "max",
    "image_urls": ["https://example.com/actor-portrait.jpg"]
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
- `meta-ad-creative-generation` - Social media ad creatives
- `product-photo-generation` - E-commerce product shots
- `image-generation` - General image generation
