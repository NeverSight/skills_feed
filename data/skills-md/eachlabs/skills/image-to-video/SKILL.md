---
name: image-to-video
description: Transform static images into dynamic videos using each::sense AI. Create animations, Ken Burns effects, cinemagraphs, product showcases, and motion graphics from still photos.
metadata:
  author: eachlabs
  version: "1.0"
---

# Image to Video Animation

Transform static images into captivating videos using each::sense. This skill animates still photos with natural motion, Ken Burns effects, cinemagraphs, and cinematic movements.

## Features

- **Photo Animation**: Bring still photos to life with realistic motion
- **Ken Burns Effect**: Smooth pan and zoom movements for storytelling
- **Cinemagraph Creation**: Subtle looping animations in specific areas
- **Product Showcases**: Dynamic 360-degree style product presentations
- **Portrait Animation**: Natural facial movements and expressions
- **Landscape Animation**: Moving clouds, flowing water, swaying trees
- **Parallax 3D Effect**: Depth-based motion for immersive visuals
- **Logo Animation**: Animate static logos with brand-appropriate motion
- **Art Animation**: Bring paintings and artwork to life
- **Social Media Motion**: Eye-catching animated content for engagement

## Quick Start

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Animate this photo with subtle natural movement, make it feel alive",
    "image_urls": ["https://example.com/photo.jpg"],
    "mode": "max"
  }'
```

## Use Case Examples

### 1. Animate Still Photo

Transform a static photograph into a living moment with natural motion.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Animate this photo with gentle, natural movement. Add subtle motion like hair moving slightly, clothes flowing, and ambient movement. Keep it realistic and cinematic, 5 seconds.",
    "image_urls": ["https://example.com/portrait-photo.jpg"],
    "mode": "max"
  }'
```

### 2. Ken Burns Effect (Pan/Zoom)

Create documentary-style pan and zoom movements for storytelling.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Apply Ken Burns effect to this image. Start zoomed out showing the full scene, then slowly zoom into the main subject in the center. Smooth, cinematic movement over 8 seconds.",
    "image_urls": ["https://example.com/landscape-scene.jpg"],
    "mode": "max"
  }'
```

### 3. Cinemagraph Creation

Create mesmerizing looping animations with isolated motion.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a cinemagraph from this coffee shop image. Keep the person still but animate only the steam rising from the coffee cup. Create a seamless loop, 3 seconds.",
    "image_urls": ["https://example.com/coffee-shop.jpg"],
    "mode": "max"
  }'
```

### 4. Product Showcase Animation

Create dynamic product presentations with rotating or revealing motion.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Animate this product photo into a showcase video. Add subtle camera orbit movement around the product, dramatic lighting transitions, and a premium feel. 6 seconds, perfect for e-commerce.",
    "image_urls": ["https://example.com/product-watch.jpg"],
    "mode": "max"
  }'
```

### 5. Portrait Animation (Subtle Movement)

Add natural, subtle movements to portrait photos.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Animate this portrait with very subtle, natural movement. Add gentle breathing motion, slight eye movement, and micro-expressions. Keep it realistic and not exaggerated - like a living photograph. 4 seconds.",
    "image_urls": ["https://example.com/headshot.jpg"],
    "mode": "max"
  }'
```

### 6. Landscape Animation (Clouds, Water)

Bring nature scenes to life with environmental motion.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Animate this landscape photo. Make the clouds drift slowly across the sky, add gentle ripples to the lake water, and subtle movement in the trees from a light breeze. Peaceful, serene mood. 10 seconds loop.",
    "image_urls": ["https://example.com/mountain-lake.jpg"],
    "mode": "max"
  }'
```

### 7. Parallax 3D Effect Video

Create depth-based motion for an immersive 3D feel.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 3D parallax effect video from this image. Separate the foreground, midground, and background layers and move them at different speeds to create depth. Subtle camera drift that reveals the 3D space. 5 seconds.",
    "image_urls": ["https://example.com/street-scene.jpg"],
    "mode": "max"
  }'
```

### 8. Logo Animation from Static

Transform a static logo into an animated intro.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Animate this logo for a video intro. Create a smooth reveal animation - the logo assembles or fades in with elegant motion. Add subtle shine or glow effect. Professional and modern style. 3 seconds.",
    "image_urls": ["https://example.com/company-logo.png"],
    "mode": "max"
  }'
```

### 9. Art Animation (Paintings Come Alive)

Bring artwork and paintings to life with artistic motion.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Animate this painting and bring it to life. Add flowing motion to the water in the scene, make the figures move subtly, and add atmospheric effects like floating particles or shifting light. Maintain the painterly style. 8 seconds.",
    "image_urls": ["https://example.com/oil-painting.jpg"],
    "mode": "max"
  }'
```

### 10. Social Media Motion Graphic

Create scroll-stopping animated content for social media.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Turn this static social media graphic into an eye-catching animated post. Add dynamic motion to the elements - pulsing, floating, or sliding effects. Make it loop seamlessly for Instagram. High energy, attention-grabbing. 3 seconds loop.",
    "image_urls": ["https://example.com/social-graphic.png"],
    "mode": "max"
  }'
```

## Mode Selection

| Mode | Best For | Speed | Quality |
|------|----------|-------|---------|
| `max` | Final videos, client deliverables, high-quality animations | Slower | Highest |
| `eco` | Quick previews, concept testing, bulk processing | Faster | Good |

## Multi-Turn Creative Iteration

Use `session_id` to iterate on your animations:

```bash
# Initial animation
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Animate this beach photo with waves and palm trees moving",
    "image_urls": ["https://example.com/beach.jpg"],
    "session_id": "beach-animation-001"
  }'

# Iterate based on feedback
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Make the waves more dramatic and add some birds flying in the sky",
    "session_id": "beach-animation-001"
  }'

# Request a variation
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a sunset version with golden hour lighting",
    "session_id": "beach-animation-001"
  }'
```

## Animation Tips

### For Natural Motion
- Request specific types of movement (breathing, hair, clothes)
- Specify the mood (calm, energetic, dramatic)
- Keep durations reasonable (3-10 seconds for most cases)

### For Cinemagraphs
- Identify the specific element that should move
- Request seamless looping
- Keep the moving area small and isolated

### For Ken Burns
- Specify start and end framing
- Indicate zoom direction (in/out) and pan direction
- Use longer durations for smoother movement

### For Product Shots
- Request orbiting or rotating camera movements
- Ask for lighting enhancements
- Specify the platform (e-commerce, social media, ads)

## Prompt Tips

When creating animations, include these details:

1. **Motion Type**: What kind of movement (subtle, dramatic, flowing)
2. **Duration**: How long the video should be (3-10 seconds typical)
3. **Looping**: Whether it should loop seamlessly
4. **Focus Area**: What elements should move vs. stay still
5. **Style**: Cinematic, professional, playful, etc.
6. **Purpose**: Social media, ads, website, presentation

### Example Prompt Structure

```
"Animate this [image type] with [motion description].
[Specific elements to animate].
[Style/mood]. [Duration] seconds.
[Additional requirements like looping, aspect ratio]."
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | Insufficient balance | Top up at eachlabs.ai |
| Image not accessible | Invalid or private URL | Use publicly accessible image URLs |
| Timeout | Complex animation | Set client timeout to minimum 10 minutes |
| Content policy violation | Prohibited content | Adjust image or prompt to comply with policies |

## Client Timeout Requirements

Video generation can take several minutes depending on complexity and duration. Configure your HTTP client with:

- **Minimum timeout**: 10 minutes (600 seconds)
- **Recommended**: 15 minutes for longer videos

## Related Skills

- `each-sense` - Core API documentation and SSE event reference
- `meta-ad-creative-generation` - Animated ads for Meta platforms
- `product-photo-generation` - Source images for animation
- `video-generation` - Text-to-video generation
