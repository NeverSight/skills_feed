---
name: pinterest-pin-generation
description: Generate Pinterest pin images using each::sense AI. Create standard pins, idea pins, product pins, recipe pins, infographics, and more optimized for Pinterest's formats and best practices.
metadata:
  author: eachlabs
  version: "1.0"
---

# Pinterest Pin Generation

Generate high-performing Pinterest pin images using each::sense. This skill creates visuals optimized for Pinterest's pin formats, aspect ratios, and platform best practices to maximize engagement and saves.

## Features

- **Standard Pins**: Vertical 2:3 images optimized for feed visibility
- **Idea Pins**: Multi-page story-style content covers
- **Product Pins**: E-commerce focused visuals with lifestyle context
- **Recipe Pins**: Food photography with step-by-step appeal
- **DIY/Tutorial Pins**: Instructional content with clear visual steps
- **Infographic Pins**: Data visualization and educational content
- **Quote Pins**: Inspirational and shareable text-based designs
- **Shopping Pins**: Catalog-ready product imagery
- **Video Pin Thumbnails**: Eye-catching covers for video content
- **Board Covers**: Cohesive collection thumbnails

## Quick Start

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 2:3 Pinterest pin for a home decor brand showing a cozy living room with warm lighting, minimalist Scandinavian style, space at top for text overlay",
    "mode": "max"
  }'
```

## Pinterest Pin Formats & Sizes

| Pin Type | Aspect Ratio | Recommended Size | Use Case |
|----------|--------------|------------------|----------|
| Standard Pin | 2:3 | 1000x1500 | General content, highest visibility |
| Idea Pin Cover | 9:16 | 1080x1920 | Story-style multi-page content |
| Square Pin | 1:1 | 1000x1000 | Product showcases, simple designs |
| Long Pin | 1:2.1 | 1000x2100 | Infographics, step-by-step guides |
| Video Thumbnail | 2:3 or 9:16 | 1000x1500 or 1080x1920 | Video content covers |
| Board Cover | 2:3 | 600x900 | Collection thumbnails |

## Use Case Examples

### 1. Standard Pin (2:3 Ratio)

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 2:3 vertical Pinterest pin for a travel blog about Santorini, Greece. Show the iconic white buildings with blue domes overlooking the sea, golden hour lighting, dreamy atmosphere. Leave space at the top third for text overlay like a blog title.",
    "mode": "max"
  }'
```

### 2. Idea Pin Cover

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 9:16 Idea Pin cover for a morning routine series. Show an aesthetic flat lay of coffee, journal, plants, and skincare products on a marble surface. Soft natural morning light, clean minimalist aesthetic. This is the cover image for a multi-page story.",
    "mode": "max"
  }'
```

### 3. Product Pin

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 2:3 Pinterest product pin for handmade ceramic mugs. Show a beautiful handcrafted mug with coffee, placed on a wooden table with soft natural light, cozy kitchen background slightly blurred. Lifestyle product photography style, warm and inviting mood.",
    "mode": "max"
  }'
```

### 4. Recipe Pin

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 2:3 Pinterest recipe pin for homemade chocolate chip cookies. Show freshly baked cookies on a cooling rack, some stacked, with melted chocolate visible, rustic wooden background. Food photography style with steam or warmth visible. Leave top portion clear for recipe title text.",
    "mode": "max"
  }'
```

### 5. DIY/Tutorial Pin

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 2:3 Pinterest pin for a DIY macrame wall hanging tutorial. Show the finished macrame piece hanging on a white wall with a plant nearby, bohemian aesthetic. The image should look like the final result of a craft project, inspiring and achievable. Space for tutorial title at top.",
    "mode": "max"
  }'
```

### 6. Infographic Pin

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1:2.1 long Pinterest infographic background for productivity tips. Design a clean, modern gradient background going from soft blue at top to teal at bottom, with subtle geometric patterns or icons related to productivity (clocks, checkmarks, calendars). Leave clear spaces for 5-6 text sections. Minimal and professional design.",
    "mode": "max"
  }'
```

### 7. Quote Pin

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 2:3 Pinterest quote pin background for motivational content. Show a serene nature scene - misty mountains at sunrise with soft pink and purple colors. The image should be slightly muted/faded to allow white text to be readable on top. Inspirational and calming mood.",
    "mode": "max"
  }'
```

### 8. Shopping Pin

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 2:3 Pinterest shopping pin for a summer dress collection. Show a floral maxi dress on a model in a garden setting, natural daylight, lifestyle fashion photography. The dress should be clearly visible and the main focus, styled with simple accessories. E-commerce catalog quality.",
    "mode": "max"
  }'
```

### 9. Video Pin Thumbnail

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 2:3 Pinterest video thumbnail for a makeup tutorial. Show a close-up of a woman with beautiful eye makeup, soft ring light reflection in eyes, beauty photography style. The image should be eye-catching and make people want to watch the video. Professional makeup artistry showcase.",
    "mode": "max"
  }'
```

### 10. Board Cover Image

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 2:3 Pinterest board cover for a Wedding Inspiration board. Show an elegant flat lay with wedding elements - white flowers, gold rings, lace fabric, calligraphy card, on a soft marble background. Romantic, luxurious, cohesive aesthetic that represents wedding planning content.",
    "mode": "max"
  }'
```

## Best Practices

### Image Composition
- **Vertical Format**: Always use 2:3 or taller ratios for maximum feed visibility
- **Text Space**: Reserve top 20-30% for title overlays
- **Focal Point**: Place main subject in center or using rule of thirds
- **High Contrast**: Ensure images stand out in a busy feed
- **Mobile-First**: Design for mobile viewing (most Pinterest traffic)

### Content Strategy
- **Lifestyle Context**: Show products in use, not just isolated
- **Aspirational**: Create images people want to save and recreate
- **Seasonal Relevance**: Consider trending topics and seasons
- **Searchability**: Think about what users search for
- **Series Consistency**: Maintain visual style across related pins

### Technical Specifications
- **Resolution**: Minimum 1000px width for crisp display
- **File Format**: PNG or JPG, optimized for web
- **Safe Zones**: Keep critical content away from edges (Pinterest may crop)
- **Color**: Use vibrant, saturated colors that pop in feed

## Prompt Tips for Pinterest Pins

When creating Pinterest pin images, include these details in your prompt:

1. **Aspect Ratio**: Specify 2:3, 9:16, or 1:2.1 for optimal format
2. **Pin Type**: Mention if it's a product, recipe, tutorial, etc.
3. **Visual Style**: Aesthetic preference (minimal, bohemian, modern, rustic)
4. **Text Space**: Request areas for title/text overlays
5. **Mood**: Cozy, energetic, luxurious, calm, etc.
6. **Target Audience**: Who will save this pin?
7. **Photography Style**: Flat lay, lifestyle, portrait, product shot

### Example Prompt Structure

```
"Create a [aspect ratio] Pinterest [pin type] for [topic/product].
Show [visual description] with [style/aesthetic].
[Mood/lighting description].
[Text space requirements].
[Any additional Pinterest-specific requirements]."
```

## Mode Selection

Ask your users before generating:

**"Do you want fast & cheap, or high quality?"**

| Mode | Best For | Speed | Quality |
|------|----------|-------|---------|
| `max` | Final pins ready to publish, hero content | Slower | Highest |
| `eco` | Quick drafts, testing concepts, bulk creation | Faster | Good |

## Multi-Turn Creative Iteration

Use `session_id` to iterate on pin designs:

```bash
# Initial pin design
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 2:3 Pinterest pin for a fitness brand, showing healthy meal prep",
    "session_id": "fitness-pin-project"
  }'

# Iterate based on feedback
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Add more colorful vegetables and make the lighting brighter and more energetic",
    "session_id": "fitness-pin-project"
  }'

# Request variation
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create 2 more variations with different angles and compositions",
    "session_id": "fitness-pin-project"
  }'
```

## Seasonal Pin Batch Generation

Generate themed pin sets for seasonal content:

```bash
# Spring collection pin 1
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 2:3 spring Pinterest pin for a gardening blog - show colorful tulips in a garden, morning dew, fresh spring aesthetic",
    "session_id": "spring-collection",
    "mode": "eco"
  }'

# Spring collection pin 2
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create another spring pin for the same gardening blog - show someone planting seeds in a terracotta pot, hands in soil, same fresh spring aesthetic",
    "session_id": "spring-collection",
    "mode": "eco"
  }'
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | Insufficient balance | Top up at eachlabs.ai |
| Content policy violation | Prohibited content | Adjust prompt to comply with Pinterest content guidelines |
| Timeout | Complex generation | Set client timeout to minimum 10 minutes |

## Related Skills

- `each-sense` - Core API documentation
- `meta-ad-creative-generation` - Facebook & Instagram ad creatives
- `product-photo-generation` - E-commerce product shots
- `social-media-content-generation` - General social media visuals
