---
name: instagram-content-generation
description: Generate Instagram content using each::sense AI. Create feed posts, stories, reels covers, carousels, quote graphics, and brand visuals optimized for Instagram's formats and engagement best practices.
metadata:
  author: eachlabs
  version: "1.0"
---

# Instagram Content Generation

Generate engaging Instagram content using each::sense. This skill creates images and videos optimized for Instagram's various placements, formats, and visual best practices.

## Features

- **Feed Posts**: Square 1:1 images for maximum compatibility
- **Stories & Reels**: Vertical 9:16 content for immersive full-screen experiences
- **Carousel Posts**: Multiple cohesive images for storytelling
- **Quote Graphics**: Typography-focused content for engagement
- **Product Showcases**: E-commerce and product-focused visuals
- **Behind-the-Scenes**: Authentic, candid-style content
- **Announcement Graphics**: Event and launch promotional content
- **Lifestyle Flat Lays**: Curated product arrangements
- **Brand Aesthetic Grid**: Cohesive visual identity across posts

## Quick Start

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1:1 Instagram feed post for a coffee brand showing a latte with beautiful latte art, morning light, cozy cafe vibes",
    "mode": "max"
  }'
```

## Instagram Formats & Sizes

| Placement | Aspect Ratio | Recommended Size | Use Case |
|-----------|--------------|------------------|----------|
| Feed Post | 1:1 | 1080x1080 | Standard feed posts, maximum compatibility |
| Feed Post | 4:5 | 1080x1350 | Vertical feed posts, more screen real estate |
| Stories | 9:16 | 1080x1920 | Full-screen temporary content |
| Reels | 9:16 | 1080x1920 | Full-screen video content |
| Reel Cover | 9:16 | 1080x1920 | Thumbnail for Reels |
| Carousel | 1:1 | 1080x1080 | Multi-image swipeable posts |

## Use Case Examples

### 1. Feed Post (1:1 Square)

Classic square format for Instagram feed with maximum compatibility across all placements.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1:1 square Instagram feed post for a sustainable fashion brand. Show a model in casual earth-toned clothing against a natural outdoor background. Warm, authentic aesthetic with soft natural lighting. Clean composition suitable for a curated Instagram grid.",
    "mode": "max"
  }'
```

### 2. Story (9:16 Vertical)

Full-screen vertical content optimized for Instagram Stories.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 9:16 Instagram Story for a yoga studio. Show a serene meditation scene with a person in lotus position, soft morning light streaming through windows, calming pastel colors. Leave safe zones at top and bottom for Instagram UI elements and swipe-up area.",
    "mode": "max"
  }'
```

### 3. Reel Cover Image

Eye-catching thumbnail that represents the Reel content and encourages clicks.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 9:16 Reel cover image for a cooking tutorial. Show an appetizing finished dish (pasta with fresh basil) from above, vibrant colors, food photography style. The image should be eye-catching and make viewers want to watch the full Reel. Leave space at bottom for the Reel title overlay.",
    "mode": "max"
  }'
```

### 4. Carousel Post (Multiple Images)

Create cohesive multi-image posts that tell a story or showcase multiple products.

```bash
# First carousel image - Cover slide
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1:1 carousel image 1 of 5 for a skincare brand. This is the cover slide showing all 5 products arranged beautifully with soft pink and white aesthetic, clean minimal background, soft shadows. Premium feel.",
    "session_id": "skincare-carousel-001",
    "mode": "max"
  }'

# Second carousel image - Product detail
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create carousel image 2 of 5. Show the cleanser product close-up with water droplets and fresh ingredients like cucumber slices. Same aesthetic and lighting as the first image.",
    "session_id": "skincare-carousel-001",
    "mode": "max"
  }'

# Third carousel image - Another product
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create carousel image 3 of 5. Show the moisturizer with a soft texture swatch, dewy fresh feel. Maintain visual consistency with previous images.",
    "session_id": "skincare-carousel-001",
    "mode": "max"
  }'
```

### 5. Quote Graphics

Typography-focused content that drives engagement and shares.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1:1 Instagram quote graphic with the text: \"Success is not final, failure is not fatal: it is the courage to continue that counts.\" Use a minimalist design with elegant serif typography on a soft gradient background (light beige to warm cream). Add subtle decorative elements like thin lines or small botanical illustrations. Suitable for a motivational or business coaching account.",
    "mode": "max"
  }'
```

### 6. Product Showcase Post

E-commerce focused content that highlights products in lifestyle context.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 4:5 Instagram product showcase for wireless headphones. Show the headphones being worn by a stylish person in an urban setting, walking through a modern city. Lifestyle photography style with natural lighting, premium aspirational feel. The product should be clearly visible but feel natural in the scene.",
    "mode": "max"
  }'
```

### 7. Behind-the-Scenes Content

Authentic, candid-style content that builds connection with the audience.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1:1 behind-the-scenes Instagram post for a bakery. Show a baker in the kitchen early morning, hands covered in flour, kneading dough. Warm golden lighting, authentic and candid feel - not overly polished. Capture the passion and craft of artisan baking. Documentary photography style.",
    "mode": "max"
  }'
```

### 8. Announcement Graphics

Event launches, sales, and promotional announcement content.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1:1 Instagram announcement graphic for a summer sale. Bold, eye-catching design with tropical vibes - palm leaves, bright colors (coral, turquoise, sunny yellow). Leave clear space for text overlay that will say \"SUMMER SALE - UP TO 50% OFF\". Modern, fresh, energetic aesthetic suitable for a fashion brand.",
    "mode": "max"
  }'
```

### 9. Lifestyle Flat Lay

Curated overhead product arrangements popular for lifestyle and product brands.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1:1 Instagram flat lay for a travel brand. Overhead shot of travel essentials arranged aesthetically: passport, sunglasses, straw hat, camera, map, coffee cup, and small succulent. Marble or light wood surface background. Clean, organized, Pinterest-worthy composition with soft natural lighting. Wanderlust aesthetic.",
    "mode": "max"
  }'
```

### 10. Brand Aesthetic Grid

Create cohesive visuals that contribute to a unified Instagram grid aesthetic.

```bash
# First grid image
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1:1 Instagram post for a minimalist home decor brand. Show a clean, modern living room corner with a simple plant, neutral tones (white, beige, light gray), lots of negative space. This is part of a cohesive grid aesthetic - keep colors muted and style consistent. Scandinavian interior design influence.",
    "session_id": "home-decor-grid",
    "mode": "max"
  }'

# Second grid image - maintaining consistency
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create another 1:1 post for the same minimalist home decor brand. Show a bedroom detail - perhaps a textured throw on a bed with a small nightstand. Same color palette and aesthetic as the previous image to maintain grid cohesion.",
    "session_id": "home-decor-grid",
    "mode": "max"
  }'

# Third grid image
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a third 1:1 post continuing the grid aesthetic. Show a close-up of a ceramic vase with dried pampas grass. Same minimalist, neutral, Scandinavian-inspired style.",
    "session_id": "home-decor-grid",
    "mode": "max"
  }'
```

## Best Practices

### Feed Posts
- **Grid Planning**: Consider how individual posts look together in your profile grid
- **Consistent Editing**: Maintain consistent color grading and style across posts
- **1:1 vs 4:5**: Use 1:1 for maximum compatibility, 4:5 for more visual impact
- **Focal Point**: Place key elements in the center for thumbnail cropping

### Stories
- **Safe Zones**: Keep important content away from top 15% and bottom 20% for UI elements
- **Vertical Thinking**: Design specifically for vertical, not cropped horizontal
- **Interactive Areas**: Leave space for polls, questions, and stickers
- **Bold and Clear**: Content should be readable quickly

### Carousels
- **Hook First**: Make the first image compelling enough to encourage swiping
- **Visual Flow**: Create a narrative or logical progression
- **Consistent Style**: Maintain same filters, fonts, and aesthetic throughout
- **End with CTA**: Use the last slide for call-to-action or summary

### Reels Covers
- **Thumbnail Appeal**: Design for small preview in the Reels tab
- **Clear Subject**: Avoid busy backgrounds that get lost at small sizes
- **Text Readable**: If using text, ensure it is legible at thumbnail size

## Prompt Tips for Instagram Content

When creating Instagram content, include these details in your prompt:

1. **Format**: Specify aspect ratio (1:1, 4:5, 9:16)
2. **Content Type**: Feed post, Story, Reel cover, carousel slide number
3. **Brand/Niche**: What type of account is this for?
4. **Aesthetic**: Minimalist, bold, vintage, modern, etc.
5. **Color Palette**: Specific colors or general mood (warm, cool, neutral)
6. **Composition**: Flat lay, portrait, lifestyle, close-up, etc.
7. **Text Space**: If you need room for captions or overlay text

### Example Prompt Structure

```
"Create a [aspect ratio] Instagram [content type] for a [brand/niche].
Show [visual description] with [aesthetic/mood].
[Color and style preferences].
[Additional requirements like text space, grid consistency, etc.]"
```

## Mode Selection

Ask your users before generating:

**"Do you want fast & cheap, or high quality?"**

| Mode | Best For | Speed | Quality |
|------|----------|-------|---------|
| `max` | Final content, portfolio posts, important campaigns | Slower | Highest |
| `eco` | Quick drafts, content planning, A/B testing concepts | Faster | Good |

## Multi-Turn Content Iteration

Use `session_id` to iterate on content and maintain visual consistency:

```bash
# Initial concept
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1:1 Instagram post for a jewelry brand, elegant and minimal",
    "session_id": "jewelry-content"
  }'

# Iterate based on feedback
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Make it more luxurious, add soft bokeh background with golden tones",
    "session_id": "jewelry-content"
  }'

# Request Story version
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Now create a 9:16 Story version of this same visual style",
    "session_id": "jewelry-content"
  }'
```

## Content Calendar Batch Generation

Generate multiple pieces of content for planning:

```bash
# Monday motivation
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1:1 motivational Monday post for a fitness brand - energetic gym scene, morning workout vibes",
    "mode": "eco"
  }'

# Wednesday product feature
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1:1 product showcase for the same fitness brand - protein shake in a gym bag flat lay",
    "mode": "eco"
  }'

# Friday lifestyle
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1:1 lifestyle post for the same fitness brand - friends laughing after a workout, feel-good Friday vibes",
    "mode": "eco"
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
- `meta-ad-creative-generation` - Meta (Facebook & Instagram) ad creatives
- `product-photo-generation` - E-commerce product shots
- `tiktok-ad-creative-generation` - TikTok content creation
