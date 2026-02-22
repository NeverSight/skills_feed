---
name: google-ad-creative-generation
description: Generate Google Ads creatives using each::sense AI. Create display ads, YouTube thumbnails, Discovery ads, Performance Max assets, and responsive display ads optimized for Google's ad formats and best practices.
metadata:
  author: eachlabs
  version: "1.0"
---

# Google Ad Creative Generation

Generate high-converting Google Ads creatives using each::sense. This skill creates images and videos optimized for Google's ad placements, formats, and best practices across Display Network, YouTube, Discovery, and Performance Max campaigns.

## Features

- **Display Ads**: Static images for Google Display Network in all standard sizes
- **YouTube Thumbnails**: Custom thumbnails for video ads and organic content
- **Discovery Ads**: Native-looking images for Gmail, Discover feed, and YouTube home
- **Performance Max**: Multi-format assets for automated Google campaigns
- **Responsive Display**: Multiple assets for Google's ML-optimized ad delivery
- **Shopping Ads**: Product-focused creatives for e-commerce campaigns
- **App Campaign Ads**: Visuals optimized for app install campaigns
- **Video Ads**: Short-form video content for YouTube placements

## Quick Start

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a Google Display ad banner for a SaaS product, 300x250 medium rectangle, showing a clean dashboard interface with professional blue color scheme",
    "mode": "max"
  }'
```

## Google Ads Formats & Sizes

### Display Network

| Format | Size (px) | Aspect Ratio | Use Case |
|--------|-----------|--------------|----------|
| Medium Rectangle | 300x250 | 1.2:1 | Most common, high inventory |
| Large Rectangle | 336x280 | 1.2:1 | Premium placements |
| Leaderboard | 728x90 | 8:1 | Header/footer placements |
| Mobile Leaderboard | 320x50 | 6.4:1 | Mobile header |
| Half Page | 300x600 | 1:2 | High visibility sidebar |
| Large Mobile Banner | 320x100 | 3.2:1 | Mobile interstitial |
| Billboard | 970x250 | 3.9:1 | Premium desktop header |
| Wide Skyscraper | 160x600 | 1:3.75 | Sidebar placements |

### YouTube & Video

| Format | Size/Ratio | Use Case |
|--------|------------|----------|
| Custom Thumbnail | 1280x720 (16:9) | Video thumbnails, companion banners |
| In-Feed Thumbnail | 1200x628 | YouTube Discovery ads |
| Bumper Ad | 6 sec, 16:9 | Short unskippable ads |
| Skippable In-Stream | 15-30 sec, 16:9 | Pre-roll, mid-roll ads |

### Discovery & Performance Max

| Format | Size (px) | Aspect Ratio | Use Case |
|--------|-----------|--------------|----------|
| Square | 1200x1200 | 1:1 | Discovery feed, Performance Max |
| Landscape | 1200x628 | 1.91:1 | Gmail, Discover, YouTube |
| Portrait | 960x1200 | 4:5 | Mobile-first placements |

### Responsive Display Ads

| Asset Type | Recommended Sizes | Notes |
|------------|-------------------|-------|
| Landscape Image | 1200x628 | Required, 1.91:1 ratio |
| Square Image | 1200x1200 | Required, 1:1 ratio |
| Logo (Landscape) | 512x128 | Optional, 4:1 ratio |
| Logo (Square) | 128x128 | Recommended, 1:1 ratio |

## Use Case Examples

### 1. Display Banner Ad (Medium Rectangle)

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 300x250 Google Display ad for an online course platform. Show a person learning on laptop, modern gradient background in purple and blue, leave space for headline text at top and CTA button at bottom.",
    "mode": "max"
  }'
```

### 2. YouTube Custom Thumbnail

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 16:9 YouTube thumbnail for a tech review video. Show a smartphone floating with dramatic lighting, bold contrasting colors, leave right side clear for text overlay. Eye-catching and clickable style.",
    "mode": "max"
  }'
```

### 3. Discovery Ad (Gmail/Discover)

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1.91:1 landscape Discovery ad for a travel agency. Show a stunning beach destination with turquoise water, aspirational vacation vibes. Native content feel, not overly promotional. 1200x628 pixels.",
    "mode": "max"
  }'
```

### 4. Shopping Ad Product Image

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a product image for Google Shopping. Show wireless headphones on pure white background, multiple angles visible, clean e-commerce style. High detail, professional product photography look.",
    "mode": "max"
  }'
```

### 5. App Campaign Ad

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1:1 square ad for a fitness app install campaign. Show app interface mockup on phone screen with workout tracking visible, energetic person exercising in background. Vibrant orange and black brand colors.",
    "mode": "max"
  }'
```

### 6. Responsive Display Ad Set

```bash
# Landscape asset (required)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1200x628 landscape image for responsive display ads. Insurance company - show a happy family in front of their home, warm and trustworthy feeling, soft natural lighting. Leave clear space for headline overlay.",
    "session_id": "responsive-insurance-001"
  }'

# Square asset (required)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1200x1200 square version of the same insurance ad. Same family, same style, recomposed for square format.",
    "session_id": "responsive-insurance-001"
  }'
```

### 7. Performance Max Multi-Asset

```bash
# Asset 1 - Square
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1:1 square image for Performance Max campaign. E-commerce fashion brand - show model wearing casual summer dress, lifestyle outdoor setting, Instagram-worthy aesthetic.",
    "session_id": "pmax-fashion-001",
    "mode": "max"
  }'

# Asset 2 - Landscape
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1.91:1 landscape version for the same fashion campaign, same model and dress, wider scene showing more environment.",
    "session_id": "pmax-fashion-001",
    "mode": "max"
  }'

# Asset 3 - Portrait
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 4:5 portrait version for mobile placements, same fashion campaign, vertical composition focusing on the dress.",
    "session_id": "pmax-fashion-001",
    "mode": "max"
  }'
```

### 8. YouTube Bumper Ad

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 6 second 16:9 bumper ad video for a car dealership. Quick cuts showing sleek new car exterior, interior dashboard, driving on highway. End with logo frame. Fast-paced, cinematic quality.",
    "mode": "max"
  }'
```

### 9. Leaderboard Banner

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 728x90 leaderboard banner for a web hosting company. Horizontal layout with server imagery on left, gradient blue tech background. Leave center-right area for headline and CTA. Modern and professional.",
    "mode": "max"
  }'
```

### 10. Remarketing Ad (with Product Image)

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 300x250 remarketing display ad featuring this watch product. Place the watch prominently with a lifestyle background showing success and sophistication. Add visual urgency elements suggesting limited availability.",
    "mode": "max",
    "image_urls": ["https://example.com/product-watch.jpg"]
  }'
```

## Best Practices

### Display Ads
- **Brand Consistency**: Use consistent colors, fonts, and visual style across all sizes
- **Clear Hierarchy**: Establish visual hierarchy - image, headline, CTA
- **Minimal Text**: Let imagery do the heavy lifting; Google prefers image-focused ads
- **High Contrast**: Ensure readability across different website backgrounds
- **CTA Visibility**: Make call-to-action buttons stand out clearly

### YouTube Thumbnails
- **Face Forward**: Human faces with eye contact increase click-through rates
- **Bold Colors**: Use contrasting colors that pop against YouTube's white interface
- **Readable Text**: If adding text, ensure it's legible at small sizes
- **Emotional Expression**: Show strong emotions to trigger curiosity
- **Avoid Clutter**: Keep composition simple and focused

### Discovery Ads
- **Native Feel**: Design to blend with organic content, not look like ads
- **Aspirational Imagery**: Use lifestyle images that inspire action
- **High Quality**: Discovery placements favor premium-looking content
- **Mobile-First**: Design for mobile screens where most Discovery traffic comes from

### Performance Max
- **Asset Variety**: Provide multiple images in different ratios for ML optimization
- **Consistent Branding**: Maintain visual consistency across all asset variations
- **Test Different Styles**: Mix lifestyle and product-focused images
- **Avoid Text in Images**: Google's ML works better with text-free images

### Responsive Display
- **Test All Combinations**: Design images that work with any headline/description
- **Safe Zones**: Keep important elements away from edges (15% margin)
- **Scalability**: Ensure images look good from 300px to 1200px wide

## Prompt Tips for Google Ads

When creating Google ad creatives, include these details in your prompt:

1. **Exact Dimensions**: Specify pixel size or aspect ratio (300x250, 1.91:1, etc.)
2. **Ad Format**: Mention if it's for Display, YouTube, Discovery, or Performance Max
3. **Product/Service**: Clearly describe what you're advertising
4. **Visual Focus**: What should be the main visual element?
5. **Color Scheme**: Brand colors or desired palette
6. **Text Space**: Request space for headlines, descriptions, or CTAs
7. **Style Reference**: Professional, playful, minimal, bold, etc.

### Example Prompt Structure

```
"Create a [dimensions] [ad format] for [product/service].
Show [visual description] with [color scheme/style].
Leave space for [text elements].
[Additional requirements like brand guidelines, urgency, etc.]"
```

## Mode Selection

Ask your users before generating:

**"Do you want fast & cheap, or high quality?"**

| Mode | Best For | Speed | Quality |
|------|----------|-------|---------|
| `max` | Final ad creatives, Performance Max assets, A/B testing winners | Slower | Highest |
| `eco` | Quick drafts, concept exploration, bulk banner variations | Faster | Good |

## Multi-Turn Creative Iteration

Use `session_id` to iterate on ad creatives:

```bash
# Initial creative
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 300x250 display ad for a fintech app, modern and trustworthy",
    "session_id": "fintech-display-001"
  }'

# Iterate based on feedback
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Make the background darker, add subtle grid pattern, more techy feel",
    "session_id": "fintech-display-001"
  }'

# Generate size variations
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Now create a 728x90 leaderboard version with the same style",
    "session_id": "fintech-display-001"
  }'
```

## Banner Size Batch Generation

Generate multiple banner sizes for a campaign:

```bash
# Medium Rectangle
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 300x250 display ad for online shoe store, lifestyle shot of running shoes in action",
    "session_id": "shoe-campaign-001",
    "mode": "eco"
  }'

# Leaderboard
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 728x90 leaderboard version, same shoe campaign style, horizontal layout",
    "session_id": "shoe-campaign-001",
    "mode": "eco"
  }'

# Half Page
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 300x600 half page version, vertical layout showcasing the shoes",
    "session_id": "shoe-campaign-001",
    "mode": "eco"
  }'
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | Insufficient balance | Top up at eachlabs.ai |
| Content policy violation | Prohibited content | Adjust prompt to comply with Google Ads policies |
| Timeout | Complex generation | Set client timeout to minimum 10 minutes |
| Dimension mismatch | Invalid size requested | Use standard Google Ads dimensions from the table above |

## Related Skills

- `each-sense` - Core API documentation
- `meta-ad-creative-generation` - Meta (Facebook/Instagram) ad creatives
- `tiktok-ad-creative-generation` - TikTok ad creatives
- `product-photo-generation` - E-commerce product shots
