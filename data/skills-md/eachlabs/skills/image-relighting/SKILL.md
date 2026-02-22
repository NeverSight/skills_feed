---
name: image-relighting
description: Relight photos and images using each::sense AI. Transform lighting conditions, add studio lighting, golden hour effects, dramatic shadows, neon glows, and match lighting to any environment.
metadata:
  author: eachlabs
  version: "1.0"
---

# Image Relighting

Transform the lighting in your photos using each::sense. This skill allows you to change lighting conditions, add professional studio setups, create dramatic effects, or match lighting to new backgrounds - all while preserving the original subject.

## Features

- **Studio Lighting**: Professional three-point lighting, Rembrandt, butterfly, and split lighting setups
- **Natural Light**: Golden hour, blue hour, overcast, and window light effects
- **Dramatic Effects**: Hard shadows, rim lighting, silhouettes, and chiaroscuro
- **Creative Lighting**: Neon glows, colored gels, disco lights, and artistic effects
- **Ring Light**: Beauty and portrait ring light effects
- **Cinematic**: Film noir, blockbuster movie, and moody cinematic lighting
- **Shadow Control**: Remove harsh shadows, soften existing light, fill in dark areas
- **Environment Matching**: Match subject lighting to a new background or scene

## Quick Start

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Add professional studio lighting to this portrait - soft key light from the left with subtle fill",
    "image_urls": ["https://example.com/portrait.jpg"],
    "mode": "max"
  }'
```

## Lighting Types Reference

| Lighting Style | Description | Best For |
|----------------|-------------|----------|
| Studio (3-point) | Key, fill, and back light setup | Professional portraits |
| Rembrandt | Triangle of light on cheek | Dramatic portraits |
| Butterfly | Light from above, shadow under nose | Beauty, glamour |
| Split | Half face lit, half in shadow | Dramatic, artistic |
| Ring Light | Even, shadowless front lighting | Beauty, social media |
| Golden Hour | Warm, soft directional light | Outdoor portraits, lifestyle |
| Blue Hour | Cool, soft ambient light | Moody, atmospheric |
| Window Light | Soft, directional natural light | Natural portraits |
| Neon/Colored | Vibrant colored lighting | Creative, editorial |
| Cinematic | High contrast, dramatic shadows | Film-like imagery |

## Use Case Examples

### 1. Add Studio Lighting

Transform a casual photo into a professionally lit portrait with classic three-point lighting setup.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Add professional studio lighting to this portrait. Use a soft key light from 45 degrees left, fill light from the right to reduce shadows, and a subtle hair light from behind. Keep the background dark for a classic studio look.",
    "image_urls": ["https://example.com/portrait.jpg"],
    "mode": "max"
  }'
```

### 2. Golden Hour / Sunset Lighting

Add warm, golden sunlight effect as if the photo was taken during the magic hour.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Relight this photo with golden hour lighting. Add warm, soft sunlight coming from the side, creating a beautiful golden glow on the skin. Include subtle lens flare and that magical sunset atmosphere.",
    "image_urls": ["https://example.com/outdoor-photo.jpg"],
    "mode": "max"
  }'
```

### 3. Dramatic Side Lighting

Create bold, dramatic portraits with strong directional light and deep shadows.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Apply dramatic side lighting to this portrait. Strong directional light from the left creating deep shadows on the right side of the face. High contrast, moody atmosphere, like a film noir character portrait.",
    "image_urls": ["https://example.com/headshot.jpg"],
    "mode": "max"
  }'
```

### 4. Soft Diffused Lighting

Create flattering, even lighting that minimizes harsh shadows and skin imperfections.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Relight this photo with soft, diffused lighting. Like shooting through a large softbox or on an overcast day. Even, flattering light with minimal shadows, perfect for beauty photography. Keep the skin looking natural and glowing.",
    "image_urls": ["https://example.com/beauty-shot.jpg"],
    "mode": "max"
  }'
```

### 5. Neon / Colored Lighting

Add vibrant, creative colored lighting for editorial or artistic effects.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Add neon lighting to this portrait. Cyberpunk style with pink/magenta light from the left and blue/cyan light from the right. Create that futuristic nightclub vibe with vibrant colored reflections on the skin and a dark background.",
    "image_urls": ["https://example.com/model-photo.jpg"],
    "mode": "max"
  }'
```

### 6. Natural Window Light

Simulate beautiful, soft natural light coming through a window.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Relight this portrait with natural window light. Soft, directional daylight coming from a large window on the left side. Create gentle shadows and that beautiful, airy natural light photographers love. Slightly cool color temperature.",
    "image_urls": ["https://example.com/indoor-portrait.jpg"],
    "mode": "max"
  }'
```

### 7. Ring Light Effect

Add the signature ring light look popular in beauty and social media content.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Apply ring light effect to this selfie. Even, frontal lighting with that signature circular catchlight in the eyes. Minimize shadows under the nose and chin, create that beauty influencer look with glowing, even skin illumination.",
    "image_urls": ["https://example.com/selfie.jpg"],
    "mode": "max"
  }'
```

### 8. Cinematic Lighting

Create movie-quality lighting with dramatic contrast and atmosphere.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Apply cinematic lighting to this portrait. Hollywood movie style with strong key light, deep shadows, and subtle rim light separating the subject from background. Moody and atmospheric like a scene from a thriller. Add subtle haze/atmosphere in the air.",
    "image_urls": ["https://example.com/actor-photo.jpg"],
    "mode": "max"
  }'
```

### 9. Remove Harsh Shadows

Fix poorly lit photos by softening or removing unflattering harsh shadows.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Remove the harsh shadows from this photo. The midday sun created unflattering dark shadows under the eyes and nose. Relight it with softer, more even lighting while keeping a natural outdoor look. Fill in the shadow areas without making it look flat.",
    "image_urls": ["https://example.com/harsh-shadow-photo.jpg"],
    "mode": "max"
  }'
```

### 10. Match Lighting to Background

Adjust subject lighting to seamlessly match a new environment or composited background.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Relight this person to match the beach sunset background. The subject was photographed indoors with flat lighting, but needs to look like they are actually on the beach during golden hour. Match the warm color temperature, add rim lighting from the setting sun behind them, and ensure the shadows are consistent with the background lighting direction.",
    "image_urls": [
      "https://example.com/subject-indoor.jpg",
      "https://example.com/beach-sunset-background.jpg"
    ],
    "mode": "max"
  }'
```

## Multi-Turn Lighting Refinement

Use `session_id` to iteratively refine lighting across multiple requests:

```bash
# Initial relighting
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Add dramatic studio lighting to this portrait with strong shadows",
    "image_urls": ["https://example.com/portrait.jpg"],
    "session_id": "lighting-session-001"
  }'

# Refine the result
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "The shadows are too harsh. Can you soften them slightly while keeping the dramatic feel? Also add a subtle blue rim light on the shadow side.",
    "session_id": "lighting-session-001"
  }'

# Try a variation
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create another version with warmer color temperature, like tungsten lighting",
    "session_id": "lighting-session-001"
  }'
```

## Mode Selection

Ask your users before generating:

**"Do you want fast & cheap, or high quality?"**

| Mode | Best For | Speed | Quality |
|------|----------|-------|---------|
| `max` | Final deliverables, client work, portfolio images | Slower | Highest |
| `eco` | Quick previews, testing lighting ideas, batch processing | Faster | Good |

## Prompt Tips for Best Results

When requesting relighting, include these details for best results:

1. **Light Direction**: Specify where the light is coming from (left, right, above, behind)
2. **Light Quality**: Hard/soft, diffused, specular
3. **Color Temperature**: Warm (golden), cool (blue), neutral, or specific colors
4. **Shadow Intensity**: Deep shadows, subtle shadows, shadowless
5. **Mood/Atmosphere**: Dramatic, romantic, professional, edgy
6. **Reference Style**: "Like a Vogue editorial" or "Film noir style"

### Example Prompt Structure

```
"Relight this [subject type] with [lighting style].
Light coming from [direction] with [quality] shadows.
[Color temperature] color temperature.
Mood: [atmosphere description].
[Additional requirements]"
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | Insufficient balance | Top up at eachlabs.ai |
| Content policy violation | Prohibited content | Ensure image complies with content policies |
| Timeout | Complex generation | Set client timeout to minimum 10 minutes |
| Poor lighting results | Vague prompt | Be more specific about light direction, quality, and mood |

## Related Skills

- `each-sense` - Core API documentation
- `product-photo-generation` - E-commerce product lighting
- `portrait-enhancement` - Portrait retouching and enhancement
- `background-replacement` - Change backgrounds with matched lighting
