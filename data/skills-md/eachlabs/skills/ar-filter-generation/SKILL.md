---
name: ar-filter-generation
description: Generate AR filters and face effects using each::sense AI. Create face filters, beauty effects, makeup overlays, branded AR experiences, and 3D face tracking effects for social media platforms.
metadata:
  author: eachlabs
  version: "1.0"
---

# AR Filter Generation

Generate creative AR filters and face effects using each::sense. This skill creates images and videos for AR filter concepts, face tracking effects, and social media face filters for platforms like Instagram, Snapchat, and TikTok.

## Features

- **Face Filters**: Animal ears, noses, whiskers, and character overlays
- **Beauty Effects**: Skin smoothing, contouring, and enhancement filters
- **Makeup AR**: Virtual lipstick, eyeshadow, blush, and full makeup looks
- **Accessories**: Sunglasses, hats, jewelry, and wearable overlays
- **Background Effects**: Background replacement and blur effects
- **Face Distortion**: Funny face warping and comedic effects
- **Branded Filters**: Logo overlays and promotional AR experiences
- **3D Face Tracking**: Objects that follow facial movements

## Quick Start

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an AR filter concept showing a person with cute dog ears and a dog nose overlay, playful and fun style",
    "mode": "max"
  }'
```

## AR Filter Types & Use Cases

| Filter Type | Description | Platform Use |
|-------------|-------------|--------------|
| Face Filters | Animal overlays, character masks | Instagram, Snapchat, TikTok |
| Beauty Filters | Skin enhancement, face reshaping | All platforms |
| Makeup Effects | Virtual cosmetics application | Beauty brands, influencers |
| Accessories | Sunglasses, hats, jewelry | Fashion, retail |
| Background | Environment replacement | Video calls, content creation |
| Distortion | Funny face warps | Entertainment, viral content |
| Branded | Logo overlays, promotional | Marketing campaigns |
| 3D Objects | Face-tracked 3D elements | Gaming, entertainment |

## Use Case Examples

### 1. Face Filter Design (Dog Ears and Nose)

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an AR filter concept showing a young woman with realistic fluffy golden retriever dog ears on top of her head and a cute black dog nose overlay on her nose. Add subtle whisker dots on cheeks. The filter should look natural and integrate well with the face. Show front-facing selfie view.",
    "mode": "max"
  }'
```

### 2. Beauty Filter Effect

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a beauty AR filter effect showing before and after comparison. Show a person with the beauty filter applied: smooth skin, subtle face slimming, brightened eyes, soft glow effect, and enhanced jawline definition. Natural-looking enhancement, not overdone. Professional beauty app style.",
    "mode": "max"
  }'
```

### 3. Makeup AR Filter

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a virtual makeup AR filter concept. Show a woman with AR-applied makeup: bold red lipstick, smoky eye shadow in bronze and gold tones, defined eyebrows, subtle blush, and winged eyeliner. The makeup should look realistic as if professionally applied. Glamorous evening look. Front-facing portrait.",
    "mode": "max"
  }'
```

### 4. Sunglasses and Accessories Filter

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an AR try-on filter showing a person wearing virtual aviator sunglasses with gold frames and gradient lenses. Add a matching gold chain necklace and small hoop earrings. The accessories should look photorealistic and properly positioned on the face. Fashion e-commerce style visualization.",
    "mode": "max"
  }'
```

### 5. Background Replacement Filter

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an AR background replacement filter concept. Show a person in selfie view with their original background replaced by a tropical beach paradise - palm trees, turquoise water, golden sand, sunset sky. Clean edge detection around the person, natural lighting blend between subject and background.",
    "mode": "max"
  }'
```

### 6. Face Distortion / Funny Filter

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a funny face distortion AR filter. Show a person with comically enlarged eyes (anime style big), tiny mouth, and slightly enlarged forehead. Add sparkles around the eyes and a rainbow effect. Cute and comedic style like popular Snapchat filters. Exaggerated but still recognizable.",
    "mode": "max"
  }'
```

### 7. Branded AR Filter (Logo Overlay)

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a branded AR filter concept for a sports event. Show a person with face paint in team colors (blue and white stripes on cheeks), a virtual foam finger appearing next to their head, confetti particles falling, and a banner frame around the image that says GO TEAM. Celebratory sports fan atmosphere.",
    "mode": "max"
  }'
```

### 8. Holiday Themed Filter

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a Christmas holiday AR filter. Show a person wearing a virtual Santa hat, with a red Rudolph nose overlay, snowflakes falling around them, and a subtle frost effect on the edges of the frame. Add twinkling lights in the background. Festive and cheerful holiday spirit.",
    "mode": "max"
  }'
```

### 9. Game-Style Filter (Among Us)

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a gaming-inspired AR filter in the style of Among Us. Transform the person into a crewmate character - their face visible through a space helmet visor, wearing the iconic colored spacesuit (red), with a small pet companion floating nearby. Add a spaceship interior background. Fun and recognizable gaming aesthetic.",
    "mode": "max"
  }'
```

### 10. 3D Object Face Tracking Filter

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 3D face tracking AR filter concept. Show a person with a 3D floating crown hovering above their head that follows head movement, 3D butterflies orbiting around them, and magical sparkle particles emanating from their eyes. The 3D elements should have realistic lighting and shadows. Fantasy magical theme.",
    "mode": "max"
  }'
```

## Best Practices

### Face Filter Design
- **Natural Integration**: Filters should blend seamlessly with facial features
- **Proper Tracking Points**: Design around standard face landmark positions (eyes, nose, mouth, forehead)
- **Lighting Consistency**: Match filter lighting with typical selfie lighting conditions
- **Scale Appropriateness**: Elements should be proportional to face size

### Platform Considerations
- **Instagram/TikTok**: Vertical 9:16 format, mobile-first design
- **Snapchat**: Consider lens studio capabilities and limitations
- **Video Calls**: Subtle effects that work at lower resolutions

### Performance Tips
- **Simplicity**: Fewer elements = better real-time performance
- **Transparency**: Use proper alpha channels for overlays
- **Animation**: Consider how static designs translate to animated filters

## Mode Selection

Ask your users before generating:

**"Do you want fast & cheap, or high quality?"**

| Mode | Best For | Speed | Quality |
|------|----------|-------|---------|
| `max` | Final filter concepts, client presentations, portfolio work | Slower | Highest |
| `eco` | Quick drafts, concept exploration, brainstorming variations | Faster | Good |

## Multi-Turn Creative Iteration

Use `session_id` to iterate on filter designs:

```bash
# Initial filter concept
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a cat face AR filter with whiskers and cat ears",
    "session_id": "cat-filter-project"
  }'

# Iterate based on feedback
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Make the ears more realistic and fluffy, add a pink nose, and include subtle face contouring to make cheeks more cat-like",
    "session_id": "cat-filter-project"
  }'

# Request variation
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a variation with black cat features instead of tabby, and add glowing yellow eyes effect",
    "session_id": "cat-filter-project"
  }'
```

## Filter Collection Generation

Generate multiple related filters for a campaign:

```bash
# Filter 1 - Dog
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an AR filter with golden retriever dog ears and nose, cute and playful",
    "mode": "eco",
    "session_id": "animal-filter-pack"
  }'

# Filter 2 - Cat
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Now create a matching cat filter with the same style - tabby cat ears and whiskers",
    "mode": "eco",
    "session_id": "animal-filter-pack"
  }'

# Filter 3 - Bunny
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Complete the pack with a bunny filter - long floppy ears and a pink bunny nose",
    "mode": "eco",
    "session_id": "animal-filter-pack"
  }'
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | Insufficient balance | Top up at eachlabs.ai |
| Content policy violation | Prohibited content | Adjust prompt to comply with platform guidelines |
| Timeout | Complex generation | Set client timeout to minimum 10 minutes |

## Prompt Tips for AR Filters

When creating AR filter concepts, include these details in your prompt:

1. **Filter Type**: Specify the category (face filter, beauty, makeup, etc.)
2. **Elements**: List all overlay elements needed (ears, nose, accessories)
3. **Style**: Realistic, cartoonish, minimal, elaborate
4. **Positioning**: Where elements appear relative to facial features
5. **Effects**: Particles, glow, color grading, distortion
6. **Platform**: Target platform if specific requirements exist
7. **Mood**: Fun, glamorous, scary, festive, etc.

### Example Prompt Structure

```
"Create a [filter type] AR filter showing [subject description].
Include [overlay elements] with [style/aesthetic].
Add [effects/particles] and [additional features].
[Platform/mood requirements]."
```

## Related Skills

- `each-sense` - Core API documentation
- `product-photo-generation` - Product visualization
- `video-generation` - Video content creation
- `image-generation` - General image creation
