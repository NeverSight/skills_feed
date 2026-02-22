---
name: social-carousel-generation
description: Generate social media carousel content using each::sense AI. Create educational slides, product showcases, storytelling sequences, tutorials, and more for Instagram, LinkedIn, Facebook, and other platforms.
metadata:
  author: eachlabs
  version: "1.0"
---

# Social Carousel Generation

Generate engaging social media carousel content using each::sense. This skill creates multi-slide visual content optimized for carousel posts on Instagram, LinkedIn, Facebook, Twitter/X, and other platforms.

## Features

- **Educational Carousels**: Tips, how-to guides, and informational content
- **Product Showcases**: Multi-angle product displays and feature highlights
- **Before/After**: Transformation and comparison visuals
- **Story Narratives**: Sequential storytelling across slides
- **Tutorials**: Step-by-step instructional content
- **Testimonials**: Customer quotes and social proof
- **Comparisons**: Side-by-side product or concept comparisons
- **Lists & Rankings**: Top 10s, rankings, and curated lists
- **Portfolio Displays**: Work showcases and case studies

## Quick Start

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 5-slide Instagram carousel about morning routine tips. Clean minimalist design with soft colors.",
    "mode": "max"
  }'
```

## Platform Specifications

| Platform | Aspect Ratio | Recommended Size | Max Slides | Notes |
|----------|--------------|------------------|------------|-------|
| Instagram | 1:1 | 1080x1080 | 10 | Most common format |
| Instagram | 4:5 | 1080x1350 | 10 | More vertical space |
| LinkedIn | 1:1 | 1080x1080 | 10 | Professional content |
| LinkedIn | 4:5 | 1080x1350 | 10 | Document-style posts |
| Facebook | 1:1 | 1080x1080 | 10 | Album or carousel ads |
| Twitter/X | 16:9 | 1200x675 | 4 | Landscape format |

## Use Case Examples

### 1. Educational Carousel (Tips/How-To)

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 6-slide Instagram carousel (1:1) teaching 5 productivity tips for remote workers. Slide 1: Eye-catching title slide with hook. Slides 2-6: One tip per slide with clean icons and brief text space. Use a modern gradient background (purple to blue), white text, minimalist style.",
    "mode": "max"
  }'
```

### 2. Product Showcase Carousel

```bash
# Slide 1 - Hero shot
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create slide 1 of 5 for a product showcase carousel (1:1 square). Premium wireless headphones hero shot - dramatic lighting, floating product, dark gradient background with subtle light rays. Space for brand logo at top.",
    "session_id": "headphones-carousel-001"
  }'

# Slide 2 - Detail shot (same session for consistency)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create slide 2 of 5. Close-up detail shot showing the premium materials and craftsmanship. Same visual style and lighting as slide 1.",
    "session_id": "headphones-carousel-001"
  }'

# Slide 3 - Lifestyle shot
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create slide 3 of 5. Lifestyle shot showing someone wearing the headphones in an urban setting. Maintain the premium dark aesthetic.",
    "session_id": "headphones-carousel-001"
  }'
```

### 3. Before/After Carousel

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 4-slide before/after carousel for a home renovation service. Slide 1: Title slide with \"Transformation Tuesday\" hook. Slide 2: Before image - outdated kitchen with old cabinets. Slide 3: After image - modern renovated kitchen, same angle. Slide 4: Call-to-action slide with space for contact info. Use 4:5 aspect ratio, consistent framing between before/after.",
    "mode": "max"
  }'
```

### 4. Story Narrative Carousel

```bash
# Create a story across multiple slides
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create slide 1 of 6 for a brand story carousel. Opening scene: A founder working late at night in a small garage, surrounded by prototypes and sketches. Warm lamp light, aspirational startup vibes. Cinematic style, 1:1 format. Leave space at bottom for caption overlay.",
    "session_id": "brand-story-001"
  }'

curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create slide 2 of 6. The journey continues - early team meeting in a coffee shop, 3-4 people huddled around a laptop, excited expressions. Same cinematic warmth and style.",
    "session_id": "brand-story-001"
  }'

curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create slide 3 of 6. Growth moment - first office space, small but professional, team of about 8 people celebrating. Maintain visual continuity.",
    "session_id": "brand-story-001"
  }'
```

### 5. Feature Highlight Carousel

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an 8-slide feature highlight carousel for a mobile app (1:1). Slide 1: App icon with tagline hook. Slides 2-7: Each featuring one key feature with a phone mockup showing the UI and an icon representing the feature. Slide 8: Download CTA with app store badges. Use a clean white background with brand accent color (teal), modern tech aesthetic.",
    "mode": "max"
  }'
```

### 6. Testimonial Carousel

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 5-slide testimonial carousel (1:1). Slide 1: Title \"What Our Customers Say\" with 5-star rating visual. Slides 2-4: Each slide shows a professional headshot placeholder (diverse representation), quote marks, space for testimonial text, and name/title area. Elegant cream background, gold accents, serif typography style. Slide 5: CTA with \"Join 10,000+ Happy Customers\".",
    "mode": "max"
  }'
```

### 7. Step-by-Step Tutorial Carousel

```bash
# Create each step with consistent styling
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create slide 1 of 7 for a recipe tutorial carousel (4:5). Title slide: \"Perfect Homemade Pizza in 6 Steps\" with appetizing hero image of finished pizza. Rustic kitchen aesthetic, warm tones, food photography style.",
    "session_id": "pizza-tutorial-001"
  }'

curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create slide 2 of 7. Step 1: Ingredients laid out on wooden cutting board - flour, yeast, tomatoes, mozzarella, basil. Overhead shot, same warm aesthetic. Include step number badge.",
    "session_id": "pizza-tutorial-001"
  }'

curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create slide 3 of 7. Step 2: Hands kneading pizza dough on floured surface. Action shot showing the technique. Consistent lighting and style.",
    "session_id": "pizza-tutorial-001"
  }'
```

### 8. Comparison Carousel

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 5-slide comparison carousel (1:1) for a SaaS product vs competitors. Slide 1: Title \"Why Choose Us?\" with versus graphic. Slides 2-4: Split-screen comparisons showing our product (green checkmarks, clean UI) vs competitors (red X marks, cluttered UI) for features like pricing, support, and ease of use. Slide 5: Summary table with winner badges. Modern tech style, dark mode aesthetic.",
    "mode": "max"
  }'
```

### 9. List/Ranking Carousel

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 7-slide ranking carousel (1:1) for \"Top 5 Travel Destinations 2024\". Slide 1: Eye-catching title with globe graphic and countdown teaser. Slides 2-6: Each destination with ranking number (5 to 1), stunning landscape image, and space for location name. Build anticipation toward #1. Slide 7: Reveal the winner with celebratory design. Use vibrant travel photography style, bold number overlays.",
    "mode": "max"
  }'
```

### 10. Portfolio Carousel

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create slide 1 of 6 for a design portfolio carousel (4:5). Cover slide: \"Recent Work\" title with abstract geometric shapes, modern sans-serif typography, black background with accent colors (coral, teal). Professional agency aesthetic.",
    "session_id": "portfolio-carousel-001"
  }'

curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create slide 2 of 6. Project showcase - mockup of a mobile app UI design displayed on a floating phone. Clean presentation, subtle shadow, same dark background with coral accent. Space for project name and brief description.",
    "session_id": "portfolio-carousel-001"
  }'

curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create slide 3 of 6. Brand identity project - logo mockups on business cards and stationery, arranged in an elegant flat lay. Consistent portfolio style.",
    "session_id": "portfolio-carousel-001"
  }'
```

## Best Practices

### Visual Consistency

- **Color Palette**: Maintain the same colors across all slides
- **Typography**: Use consistent fonts and text hierarchy
- **Layout**: Keep text and graphic positions predictable
- **Spacing**: Maintain uniform margins and padding

### Content Flow

- **Hook First**: Slide 1 must capture attention immediately
- **Clear Progression**: Each slide should flow naturally to the next
- **Value Per Slide**: Every slide should deliver value or advance the story
- **Strong CTA**: End with a clear call-to-action

### Platform Optimization

- **Safe Zones**: Keep important content away from edges (10% margin)
- **Text Readability**: Ensure text is legible at mobile sizes
- **Swipe Indicators**: Visual cues that encourage swiping
- **Standalone Value**: Each slide should work if viewed individually

## Prompt Tips for Carousels

When creating carousel content, include these details:

1. **Slide Count**: Specify total number of slides
2. **Format**: Mention aspect ratio (1:1, 4:5, 16:9)
3. **Platform**: Instagram, LinkedIn, Facebook, etc.
4. **Style**: Modern, minimalist, bold, elegant, etc.
5. **Color Scheme**: Specific colors or mood
6. **Content Structure**: What each slide should contain
7. **Text Placeholders**: Where text should appear

### Example Prompt Structure

```
"Create a [number]-slide [platform] carousel ([aspect ratio]).
Slide 1: [content description]
Slides 2-N: [content pattern]
Final slide: [CTA description]
Style: [visual style], [color scheme]."
```

## Mode Selection

Ask your users before generating:

**"Do you want fast & cheap, or high quality?"**

| Mode | Best For | Speed | Quality |
|------|----------|-------|---------|
| `max` | Final carousel posts, client deliverables | Slower | Highest |
| `eco` | Quick drafts, concept exploration, testing ideas | Faster | Good |

## Multi-Turn Carousel Creation

Use `session_id` to maintain consistency across slides:

```bash
# Start the carousel
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create slide 1 of 5 for a fitness tips carousel. Bold title slide with energetic colors.",
    "session_id": "fitness-carousel-project"
  }'

# Continue with same session
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create slide 2 - first fitness tip about morning stretches. Same style as slide 1.",
    "session_id": "fitness-carousel-project"
  }'

# Request adjustments
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "The colors are too bright. Regenerate slide 1 with more muted, earth tones.",
    "session_id": "fitness-carousel-project"
  }'
```

## Batch Generation

Generate multiple carousel variations:

```bash
# Version A - Minimalist
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 5-slide marketing tips carousel. Style: Clean minimalist, white background, black text, simple icons.",
    "mode": "eco"
  }'

# Version B - Bold & Colorful
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 5-slide marketing tips carousel. Style: Bold gradients, vibrant colors (pink, orange, purple), dynamic shapes.",
    "mode": "eco"
  }'

# Version C - Dark Mode
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 5-slide marketing tips carousel. Style: Dark mode, black background, neon accents, modern tech aesthetic.",
    "mode": "eco"
  }'
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | Insufficient balance | Top up at eachlabs.ai |
| Content policy violation | Prohibited content | Adjust prompt to comply with platform guidelines |
| Timeout | Complex generation | Set client timeout to minimum 10 minutes |
| Inconsistent styling | New session | Use same `session_id` for all carousel slides |

## Related Skills

- `each-sense` - Core API documentation
- `meta-ad-creative-generation` - Meta ad creatives
- `product-photo-generation` - E-commerce product shots
- `social-media-content` - General social media content
