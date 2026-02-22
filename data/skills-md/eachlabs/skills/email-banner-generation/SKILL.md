---
name: email-banner-generation
description: Generate email marketing banners and headers using each::sense AI. Create newsletter headers, promotional banners, welcome emails, and seasonal campaigns optimized for email-safe dimensions and best practices.
metadata:
  author: eachlabs
  version: "1.0"
---

# Email Banner Generation

Generate high-converting email marketing banners and headers using each::sense. This skill creates images optimized for email clients with standard 600px width for maximum compatibility.

## Features

- **Newsletter Headers**: Professional headers for recurring newsletters
- **Promotional Banners**: Sale announcements and discount campaigns
- **Product Announcements**: New product and feature launch visuals
- **Welcome Emails**: First impression headers for new subscribers
- **Seasonal Campaigns**: Holiday and seasonal themed banners
- **Event Invitations**: Webinar, conference, and event headers
- **Flash Sale Banners**: Urgency-driven countdown style graphics
- **Testimonial Banners**: Customer review and social proof visuals
- **Email Signatures**: Professional branded signature banners

## Quick Start

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an email newsletter header, 600px wide, for a tech company weekly digest. Modern, clean design with blue gradient background.",
    "mode": "max"
  }'
```

## Email Banner Sizes & Best Practices

| Banner Type | Dimensions | Use Case |
|-------------|------------|----------|
| Standard Header | 600x200 | Newsletter headers, general announcements |
| Hero Banner | 600x300 | Promotional campaigns, product launches |
| Compact Header | 600x150 | Minimalist headers, signature banners |
| Full Feature | 600x400 | Product showcases, event invitations |
| Signature Banner | 600x100 | Email signature graphics |

**Note:** 600px width is the email-safe standard that renders correctly across all major email clients (Gmail, Outlook, Apple Mail, etc.).

## Use Case Examples

### 1. Newsletter Header

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 600x200px email newsletter header for a tech startup weekly digest. Clean modern design with subtle geometric patterns, dark blue to purple gradient background. Include space for logo on the left side. Professional and contemporary feel.",
    "mode": "max"
  }'
```

### 2. Promotional Sale Banner

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 600x300px promotional email banner for a 50% off summer sale. Bright, energetic design with coral and yellow colors. Include visual space for SALE headline text and shop now button. E-commerce fashion brand style.",
    "mode": "max"
  }'
```

### 3. Product Announcement Banner

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 600x300px email banner announcing a new smartphone launch. Premium tech aesthetic with dark background, subtle light rays, and space for product image placement. Apple-style minimalism with focus on elegance.",
    "mode": "max"
  }'
```

### 4. Welcome Email Header

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 600x250px welcome email header for a fitness app. Warm, inviting design with energetic person silhouette, sunrise gradient (orange to yellow), motivational atmosphere. Space for Welcome message and brand logo.",
    "mode": "max"
  }'
```

### 5. Holiday/Seasonal Banner

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 600x300px holiday email banner for Christmas sale campaign. Festive design with snow, pine trees silhouettes, red and gold color scheme. Elegant with subtle sparkles, space for holiday greeting text and discount badge.",
    "mode": "max"
  }'
```

### 6. Event Invitation Header

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 600x350px email header for a virtual conference invitation. Professional corporate design with abstract network visualization, deep blue and teal colors. Include visual areas for event name, date, and register button. Tech conference aesthetic.",
    "mode": "max"
  }'
```

### 7. New Collection Announcement

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 600x300px email banner for a fashion brand new spring collection launch. Elegant, high-fashion aesthetic with soft pastel colors (blush pink, sage green). Minimalist with space for NEW COLLECTION text overlay. Luxury brand feel.",
    "mode": "max"
  }'
```

### 8. Flash Sale Countdown Banner

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 600x250px flash sale email banner with urgency. Bold design with red and black colors, dynamic diagonal stripes or lightning bolt elements. Include visual space for countdown timer display boxes (hours:minutes:seconds). High energy, act now feeling.",
    "mode": "max"
  }'
```

### 9. Testimonial/Review Banner

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 600x280px email banner for customer testimonials section. Clean design with soft gradient background (light gray to white), space for circular customer photo placeholder, quote marks design element, 5-star rating visual. Trust-building, professional layout.",
    "mode": "max"
  }'
```

### 10. Email Signature Banner

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 600x100px email signature banner for a marketing agency. Sleek horizontal design with subtle gradient, space for company logo on left, social media icon placeholders on right. Professional, minimal, brand-forward design.",
    "mode": "max"
  }'
```

## Best Practices

### Email-Safe Design
- **Width**: Always use 600px width for maximum email client compatibility
- **File Size**: Keep images under 1MB for fast loading
- **Format**: PNG for graphics with transparency, JPG for photos
- **Alt Text**: Always include descriptive alt text for accessibility
- **Retina Support**: Consider 1200px width scaled to 600px for retina displays

### Visual Guidelines
- **Text Space**: Leave clear areas for text overlays
- **Contrast**: Ensure text areas have sufficient contrast
- **Brand Consistency**: Maintain consistent colors and style across campaigns
- **Mobile**: Design with mobile email clients in mind (single column)
- **Safe Zones**: Keep critical elements away from edges

### Content Tips
- **Clear Hierarchy**: Most important information should be immediately visible
- **Single Focus**: One main message per banner
- **CTA Visibility**: Ensure call-to-action areas stand out
- **Minimal Text**: Use supporting HTML text instead of image text when possible

## Prompt Tips for Email Banners

When creating email banners, include these details in your prompt:

1. **Dimensions**: Specify exact size (e.g., 600x300px)
2. **Banner Type**: Header, promotional, announcement, etc.
3. **Color Scheme**: Brand colors or desired palette
4. **Text Space**: Where headlines/CTAs will be placed
5. **Style**: Minimalist, bold, elegant, playful, etc.
6. **Industry**: E-commerce, SaaS, fitness, fashion, etc.

### Example Prompt Structure

```
"Create a [width]x[height]px email [banner type] for [industry/brand].
[Style description] with [color scheme].
Include space for [text elements like headline, CTA, logo].
[Mood/feeling] aesthetic."
```

## Mode Selection

Ask your users before generating:

**"Do you want fast & cheap, or high quality?"**

| Mode | Best For | Speed | Quality |
|------|----------|-------|---------|
| `max` | Final campaign banners, A/B testing winners | Slower | Highest |
| `eco` | Quick drafts, concept exploration, bulk variations | Faster | Good |

## Multi-Turn Creative Iteration

Use `session_id` to iterate on email banners:

```bash
# Initial banner
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 600x300px promotional email banner for Black Friday sale. Bold design with dark background.",
    "session_id": "email-campaign-bf2024"
  }'

# Iterate based on feedback
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Add more gold accents and make the design more premium looking. Include space for 70% OFF text.",
    "session_id": "email-campaign-bf2024"
  }'

# Request size variation
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a compact 600x150px version of this banner for email signature use.",
    "session_id": "email-campaign-bf2024"
  }'
```

## Campaign Batch Generation

Generate multiple variations for A/B testing:

```bash
# Variation A - Bold colors
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 600x300px email banner for spring sale - bold vibrant colors, energetic design",
    "mode": "eco"
  }'

# Variation B - Minimal design
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 600x300px email banner for spring sale - minimal clean design, soft pastels",
    "mode": "eco"
  }'

# Variation C - Photo-centric
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 600x300px email banner for spring sale - lifestyle photography style, person in spring setting",
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
- `meta-ad-creative-generation` - Meta/Facebook ad creatives
- `product-photo-generation` - E-commerce product shots
