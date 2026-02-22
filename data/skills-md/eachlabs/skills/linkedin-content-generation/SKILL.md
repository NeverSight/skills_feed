---
name: linkedin-content-generation
description: Generate LinkedIn content graphics using each::sense AI. Create professional post images, article headers, company banners, event promotions, thought leadership visuals, and personal brand content optimized for LinkedIn's professional audience.
metadata:
  author: eachlabs
  version: "1.0"
---

# LinkedIn Content Generation

Generate high-impact LinkedIn content graphics using each::sense. This skill creates professional images optimized for LinkedIn's formats, audience expectations, and best practices for B2B engagement.

## Features

- **Post Graphics**: Eye-catching images for feed posts and updates
- **Article Headers**: Professional header images for LinkedIn articles
- **Company Banners**: Brand-aligned banners for company pages
- **Event Promotions**: Graphics for webinars, conferences, and events
- **Thought Leadership**: Visuals for industry insights and expertise
- **Data Visualization**: Stats and infographic-style content
- **Team Announcements**: New hire, promotion, and team celebration graphics
- **Job Postings**: Attractive visuals for recruitment posts
- **Personal Brand**: Professional imagery for individual thought leaders

## Quick Start

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a LinkedIn post graphic about AI transformation in business, professional and modern style with blue color scheme",
    "mode": "max"
  }'
```

## LinkedIn Image Formats & Sizes

| Content Type | Aspect Ratio | Recommended Size | Use Case |
|--------------|--------------|------------------|----------|
| Feed Post (Single) | 1.91:1 | 1200x628 | Standard post images |
| Feed Post (Square) | 1:1 | 1080x1080 | High engagement posts |
| Feed Post (Portrait) | 4:5 | 1080x1350 | Maximum feed presence |
| Article Header | 1.91:1 | 1200x628 | LinkedIn article covers |
| Company Banner | 4:1 | 1128x191 | Company page header |
| Event Cover | 16:9 | 1600x900 | Event page images |
| Carousel Slide | 1:1 | 1080x1080 | Document/carousel posts |

## Use Case Examples

### 1. Professional Post Graphic

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1:1 LinkedIn post graphic about digital transformation. Show a professional in a modern office environment with digital elements and data visualizations floating around. Clean, corporate aesthetic with blue and white tones. Leave space at bottom for text overlay.",
    "mode": "max"
  }'
```

### 2. Article Header Image

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1200x628 LinkedIn article header image about leadership in remote work. Abstract professional design showing connected people icons, home office elements, and collaboration symbols. Corporate blue gradient background with modern geometric shapes.",
    "mode": "max"
  }'
```

### 3. Company Page Banner

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a LinkedIn company banner (1128x191 pixels, very wide 4:1 ratio) for a tech consulting firm. Abstract technology-themed design with circuit patterns, subtle gradient from dark blue to teal. Professional and innovative feel. No text, just visual elements.",
    "mode": "max"
  }'
```

### 4. Event Promotion Graphic

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 16:9 LinkedIn event cover for a virtual leadership summit. Show a professional conference stage setup with modern lighting, screens displaying abstract business graphics, and an audience silhouette. Premium corporate event atmosphere with purple and blue accent lighting.",
    "mode": "max"
  }'
```

### 5. Thought Leadership Visual

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1:1 thought leadership post image about the future of AI in healthcare. Show an abstract visualization of AI and medical imagery merging - neural network patterns combined with medical symbols, DNA helixes, and healthcare icons. Clean white background with blue and green accents. Professional and innovative.",
    "mode": "max"
  }'
```

### 6. Data/Stats Visualization Background

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1:1 LinkedIn post background for showcasing business statistics. Abstract data visualization design with subtle chart elements, graph lines, and percentage symbols in the background. Dark professional theme with glowing blue and green data points. Leave large center area for text overlay of actual statistics.",
    "mode": "max"
  }'
```

### 7. Team Announcement Graphic

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1:1 LinkedIn graphic template for a new team member announcement. Professional celebratory design with confetti elements, welcome banner style, and a prominent circular placeholder area for a profile photo. Corporate colors (blue and gold), warm and welcoming atmosphere.",
    "mode": "max"
  }'
```

### 8. Job Posting Visual

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 4:5 LinkedIn job posting graphic for a software engineering position. Show a modern tech workspace with developers collaborating, multiple screens with code, bright and energetic office environment. Diverse team, innovative startup atmosphere. Leave top portion for job title text.",
    "mode": "max"
  }'
```

### 9. Industry Insight Graphic

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1.91:1 LinkedIn post image about fintech industry trends. Abstract financial technology visualization with blockchain nodes, digital currency symbols, and banking icons interconnected. Gradient from navy to electric blue, futuristic but professional. Suitable for a market analysis post.",
    "mode": "max"
  }'
```

### 10. Personal Brand Content

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1:1 personal brand LinkedIn post image for a business coach sharing advice. Show a professional speaking or presenting, confident pose, modern minimalist office background with motivational elements. Warm, approachable lighting. Space at bottom for quote text overlay.",
    "mode": "max"
  }'
```

## Best Practices

### Professional Aesthetics
- **Color Palette**: Stick to professional colors - blues, grays, white, with accent colors
- **Clean Design**: Avoid clutter; LinkedIn audience prefers polished, minimal designs
- **Brand Consistency**: Maintain consistent visual identity across all content
- **Text Space**: Leave clear areas for headlines, stats, or quotes

### Content Guidelines
- **Professional Tone**: Content should feel business-appropriate
- **High Resolution**: Always generate at recommended sizes for crisp display
- **Mobile-First**: Most LinkedIn users browse on mobile - ensure clarity at smaller sizes
- **Accessibility**: Use good contrast ratios for any overlaid text

### Engagement Optimization
- **Visual Hierarchy**: Guide the eye to key elements
- **Emotional Connection**: Use human elements for higher engagement
- **Brand Recognition**: Include subtle brand elements when appropriate

## Prompt Tips for LinkedIn Content

When creating LinkedIn content, include these details in your prompt:

1. **Format**: Specify aspect ratio (1:1, 1.91:1, 4:5, 16:9)
2. **Content Type**: Post, article header, banner, event, etc.
3. **Industry**: Tech, finance, healthcare, consulting, etc.
4. **Mood**: Professional, innovative, warm, authoritative
5. **Color Scheme**: Corporate blues, brand colors, etc.
6. **Text Space**: Where you need room for copy overlay
7. **Target Audience**: Executives, developers, HR, etc.

### Example Prompt Structure

```
"Create a [aspect ratio] LinkedIn [content type] for [industry/topic].
Show [visual description] with [mood/style].
Color scheme: [colors].
[Additional requirements like text space, brand elements, etc.]"
```

## Mode Selection

Ask your users before generating:

**"Do you want fast & cheap, or high quality?"**

| Mode | Best For | Speed | Quality |
|------|----------|-------|---------|
| `max` | Final content, important posts, brand materials | Slower | Highest |
| `eco` | Quick drafts, concept exploration, batch testing | Faster | Good |

## Multi-Turn Content Iteration

Use `session_id` to iterate on LinkedIn content:

```bash
# Initial graphic
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1:1 LinkedIn post about SaaS growth strategies, professional blue theme",
    "session_id": "linkedin-saas-post"
  }'

# Iterate based on feedback
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Make it more dynamic with upward trending graph elements and add some green accent colors for growth theme",
    "session_id": "linkedin-saas-post"
  }'

# Request variation
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an alternative version with a darker background for A/B testing",
    "session_id": "linkedin-saas-post"
  }'
```

## Carousel Content Generation

Generate multiple slides for LinkedIn carousel posts:

```bash
# Slide 1 - Cover
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create slide 1 of 5 for a LinkedIn carousel about productivity tips. Cover slide design - bold, attention-grabbing with abstract productivity imagery. 1:1 format, dark blue background with orange accents.",
    "session_id": "productivity-carousel",
    "mode": "max"
  }'

# Slide 2 - Content slide
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create slide 2 of 5 maintaining the same visual style. Show time management concept with clock and calendar elements. Leave space for tip text.",
    "session_id": "productivity-carousel",
    "mode": "max"
  }'
```

## Batch Content Generation

Generate multiple variations for content testing:

```bash
# Variation A - Abstract style
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1:1 LinkedIn post about cloud computing - abstract geometric style with cloud and server icons",
    "mode": "eco"
  }'

# Variation B - Photo-realistic style
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1:1 LinkedIn post about cloud computing - photo-realistic data center with blue lighting",
    "mode": "eco"
  }'

# Variation C - Minimal style
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1:1 LinkedIn post about cloud computing - minimal line art style with simple cloud icon",
    "mode": "eco"
  }'
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | Insufficient balance | Top up at eachlabs.ai |
| Content policy violation | Prohibited content | Adjust prompt to comply with professional content guidelines |
| Timeout | Complex generation | Set client timeout to minimum 10 minutes |

## Related Skills

- `each-sense` - Core API documentation
- `meta-ad-creative-generation` - Meta (Facebook/Instagram) ad creatives
- `google-ad-creative-generation` - Google Ads creatives
- `product-photo-generation` - E-commerce product shots
