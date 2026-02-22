---
name: ai-avatar-generation
description: Generate AI avatars from photos or text descriptions using each::sense. Create professional headshots, cartoon avatars, 3D characters, fantasy personas, gaming avatars, and consistent character designs for various platforms.
metadata:
  author: eachlabs
  version: "1.0"
---

# AI Avatar Generation

Generate stunning AI avatars using each::sense. Transform selfies into professional headshots, create cartoon or 3D avatars, design fantasy characters, and generate consistent avatars for gaming, social media, and professional use.

## Features

- **Professional Avatars**: Transform casual photos into polished headshots
- **Cartoon Avatars**: Convert photos to various cartoon and illustration styles
- **3D Avatars**: Generate 3D character renders from photos or descriptions
- **Fantasy Avatars**: Create wizard, knight, elf, and other fantasy personas
- **Sci-Fi Avatars**: Design futuristic, cyberpunk, and space-themed characters
- **Social Media Profiles**: Platform-optimized avatars for LinkedIn, Instagram, etc.
- **Gaming Avatars**: RPG characters, streamers, and gaming personas
- **Consistent Characters**: Generate the same character across multiple poses and styles

## Quick Start

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a professional avatar from this selfie, make it look like a corporate headshot with studio lighting",
    "mode": "max",
    "image_urls": ["https://example.com/my-selfie.jpg"]
  }'
```

## Avatar Styles & Use Cases

| Style | Best For | Output Quality |
|-------|----------|----------------|
| Professional Headshot | LinkedIn, corporate profiles, resumes | Photorealistic |
| Cartoon/Illustration | Social media, casual platforms, personal branding | Stylized |
| 3D Render | Gaming, metaverse, virtual worlds | 3D Character |
| Fantasy/Themed | Gaming profiles, creative communities, RPG | Artistic |
| Anime/Manga | Discord, streaming, anime communities | Anime style |
| Pixel Art | Gaming, retro platforms, NFTs | Pixel style |

## Use Case Examples

### 1. Professional Avatar from Selfie

Transform a casual selfie into a polished professional headshot suitable for LinkedIn or corporate profiles.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Transform this selfie into a professional corporate headshot. Clean studio background (soft gray gradient), perfect lighting, slight smile, confident expression. Make it suitable for LinkedIn. Keep my facial features recognizable but enhance to look polished and professional.",
    "mode": "max",
    "image_urls": ["https://example.com/my-selfie.jpg"]
  }'
```

### 2. Cartoon Style Avatar

Convert a photo into a fun cartoon or illustrated avatar.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Convert this photo into a Pixar-style cartoon avatar. Exaggerated friendly features, big expressive eyes, smooth colorful rendering. Keep the likeness recognizable but make it fun and animated. Bright cheerful background.",
    "mode": "max",
    "image_urls": ["https://example.com/my-photo.jpg"]
  }'
```

### 3. 3D Avatar Generation

Create a 3D rendered avatar character from a photo or description.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate a 3D rendered avatar based on this photo. Make it look like a high-quality video game character with clean topology, subsurface skin scattering, realistic hair rendering. Neutral pose, front-facing, clean dark studio background. Suitable for metaverse or gaming profile.",
    "mode": "max",
    "image_urls": ["https://example.com/reference-photo.jpg"]
  }'
```

### 4. Fantasy Themed Avatars (Wizard, Knight)

Create fantasy character avatars for gaming or creative communities.

```bash
# Wizard Avatar
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Transform this photo into a powerful wizard avatar. Add a mystical purple cloak with glowing runes, a long silver beard (if male) or flowing magical hair, ancient staff, and magical energy particles around the hands. Fantasy art style, dramatic lighting with magical glow. Epic RPG character portrait.",
    "mode": "max",
    "image_urls": ["https://example.com/my-photo.jpg"]
  }'

# Knight Avatar
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Transform this photo into a noble knight avatar. Shining silver armor with gold accents, red cape, battle-worn but heroic appearance. Medieval castle background with dramatic sunset. Keep my facial features but make me look like a legendary warrior. High fantasy art style.",
    "mode": "max",
    "image_urls": ["https://example.com/my-photo.jpg"]
  }'
```

### 5. Sci-Fi Themed Avatars

Design futuristic cyberpunk or space-themed character avatars.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Transform this photo into a cyberpunk avatar. Add neon circuit tattoos, cybernetic eye implant with glowing blue iris, futuristic collar with LED strips, slick dark hair with neon highlights. Dark city background with rain and neon signs. Blade Runner aesthetic, dramatic lighting.",
    "mode": "max",
    "image_urls": ["https://example.com/my-photo.jpg"]
  }'
```

### 6. Social Media Profile Avatars

Create platform-optimized avatars for various social networks.

```bash
# Instagram Profile Avatar
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a trendy Instagram profile avatar from this photo. Modern aesthetic, soft warm filter, slight glow effect, friendly approachable expression. 1:1 square format optimized for circular crop. Pastel gradient background. Keep it authentic but polished, influencer-style.",
    "mode": "max",
    "image_urls": ["https://example.com/my-photo.jpg"]
  }'

# Discord/Gaming Avatar
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a cool Discord avatar from this photo. Anime-inspired style with bold outlines, vibrant colors, confident expression. Add gaming headphones, RGB lighting effects in the background. Square format, works well at small sizes. Energetic gamer aesthetic.",
    "mode": "max",
    "image_urls": ["https://example.com/my-photo.jpg"]
  }'
```

### 7. Gaming Avatars

Generate character avatars for gaming profiles and streaming.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an epic gaming avatar from this photo. Transform me into an RPG hero character - detailed armor, confident battle-ready pose, dramatic lighting with volumetric rays. Style similar to League of Legends or Valorant character art. High detail, vibrant colors, professional esports team portrait quality.",
    "mode": "max",
    "image_urls": ["https://example.com/my-photo.jpg"]
  }'
```

### 8. Multiple Avatar Variations

Generate several different style variations of the same person.

```bash
# Initial request - set up the session
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "I want to create multiple avatar variations from this photo. Start with a professional headshot version.",
    "mode": "max",
    "session_id": "avatar-variations-001",
    "image_urls": ["https://example.com/my-photo.jpg"]
  }'

# Second variation - cartoon style
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Now create a cartoon/illustrated version of the same person",
    "session_id": "avatar-variations-001"
  }'

# Third variation - 3D render
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 3D rendered version, like a video game character",
    "session_id": "avatar-variations-001"
  }'
```

### 9. Consistent Character Across Poses

Generate the same character in multiple poses while maintaining consistency.

```bash
# Define the character
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a character avatar based on this photo. Professional illustration style, clean lines, distinctive features. This will be my consistent character for multiple images. Front-facing portrait first.",
    "mode": "max",
    "session_id": "consistent-character-001",
    "image_urls": ["https://example.com/my-photo.jpg"]
  }'

# Same character, different pose
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate the same character in a 3/4 side view, looking confident with arms crossed. Maintain exact same style, colors, and features.",
    "session_id": "consistent-character-001"
  }'

# Same character, action pose
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Now show the same character waving hello, friendly expression. Keep all features consistent with previous images.",
    "session_id": "consistent-character-001"
  }'
```

### 10. Avatar with Custom Backgrounds

Create avatars with specific themed backgrounds.

```bash
# Beach/Travel themed
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an avatar from this photo with a beautiful tropical beach background. Sunset golden hour lighting, palm trees, ocean waves. Make it look like a premium travel profile picture. Professional color grading, dreamy atmosphere.",
    "mode": "max",
    "image_urls": ["https://example.com/my-photo.jpg"]
  }'

# Studio with colored backdrop
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a professional avatar from this photo with a vibrant gradient background (purple to blue). Studio lighting setup, clean and modern. Perfect for a creative professional or designer profile.",
    "mode": "max",
    "image_urls": ["https://example.com/my-photo.jpg"]
  }'

# Nature/Outdoor backdrop
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate an avatar with a mountain landscape background. Person in focus with bokeh effect on the scenic mountains behind. Adventure/outdoor enthusiast vibe. Natural lighting, authentic feel.",
    "mode": "max",
    "image_urls": ["https://example.com/my-photo.jpg"]
  }'
```

## Best Practices

### Photo Input Tips
- **Clear face visibility**: Ensure face is well-lit and clearly visible
- **Front-facing preferred**: Best results with front or slight angle photos
- **Good resolution**: Higher resolution input = better output quality
- **Neutral background**: Simpler backgrounds help isolate the subject

### Prompt Tips for Avatars
1. **Specify style clearly**: Cartoon, 3D, realistic, anime, etc.
2. **Describe desired features**: Lighting, expression, pose
3. **Mention the platform**: LinkedIn, Instagram, gaming - affects optimization
4. **Include background preferences**: Studio, gradient, themed, etc.
5. **Request consistency**: For multiple avatars, use session_id and reference previous outputs

### Style Consistency
For creating multiple avatars of the same person:
- Use `session_id` to maintain context across requests
- Reference previous generations when requesting new poses
- Be specific about which features to keep consistent

## Mode Selection

Ask your users before generating:

**"Do you want fast & cheap, or high quality?"**

| Mode | Best For | Speed | Quality |
|------|----------|-------|---------|
| `max` | Final avatars, professional headshots, detailed fantasy characters | Slower | Highest |
| `eco` | Quick previews, style exploration, bulk variations | Faster | Good |

## Multi-Turn Avatar Refinement

Use `session_id` to iterate and refine your avatar:

```bash
# Initial avatar
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a professional avatar from this photo",
    "session_id": "my-avatar-project",
    "image_urls": ["https://example.com/my-photo.jpg"]
  }'

# Refine based on feedback
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Make the lighting warmer and add a slight smile",
    "session_id": "my-avatar-project"
  }'

# Try a different style
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Can you make a cartoon version of this same avatar?",
    "session_id": "my-avatar-project"
  }'
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | Insufficient balance | Top up at eachlabs.ai |
| Content policy violation | Prohibited content | Ensure photo and prompt comply with content policies |
| Timeout | Complex generation | Set client timeout to minimum 10 minutes |
| Poor likeness | Low quality input | Use higher resolution, well-lit photo with clear face |

## Related Skills

- `each-sense` - Core API documentation
- `product-photo-generation` - E-commerce product shots
- `meta-ad-creative-generation` - Social media ad creatives
