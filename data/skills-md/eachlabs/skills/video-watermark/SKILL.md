---
name: video-watermark
description: Add or remove watermarks from videos using each::sense AI. Add logo watermarks, text overlays, transparent watermarks, animated watermarks, and remove unwanted watermarks from TikTok, stock footage, and other sources.
metadata:
  author: eachlabs
  version: "1.0"
---

# Video Watermark

Add professional watermarks to your videos or remove unwanted watermarks using each::sense. This skill handles all watermarking needs including logo placement, text overlays, animated watermarks, and intelligent watermark removal.

## Features

- **Add Logo Watermark**: Place your brand logo on videos with customizable opacity and position
- **Add Text Watermark**: Add text overlays with custom fonts, colors, and styles
- **Transparent Watermark**: Semi-transparent watermarks that don't obstruct content
- **Position Control**: Place watermarks in corners, center, or custom positions
- **Animated Watermark**: Moving or pulsing watermarks for enhanced branding
- **Dynamic Watermark**: Watermarks that change position throughout the video
- **Remove Watermark**: Intelligently remove existing watermarks from videos
- **TikTok Watermark Removal**: Remove TikTok logos and usernames from videos
- **Stock Footage Cleanup**: Remove stock footage watermarks for licensed content
- **Batch Processing**: Apply watermarks to multiple videos efficiently

## Quick Start

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Add a logo watermark to this video in the bottom right corner with 50% opacity",
    "mode": "max",
    "image_urls": ["https://example.com/my-video.mp4", "https://example.com/my-logo.png"]
  }'
```

## Watermark Position Reference

| Position | Description | Best Use Case |
|----------|-------------|---------------|
| Bottom Right | Most common placement | Corporate videos, vlogs |
| Bottom Left | Alternative corner | When bottom right has content |
| Top Right | Upper corner | News-style, live streams |
| Top Left | Upper corner | Documentary style |
| Center | Middle of frame | Preview/draft watermarks |
| Full Frame | Diagonal across video | Stock footage protection |

## Use Case Examples

### 1. Add Logo Watermark

Add your brand logo to a video with customizable placement and opacity.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Add this logo as a watermark to the video. Place it in the bottom right corner with 40% opacity. Keep the logo small, about 10% of the video width.",
    "mode": "max",
    "image_urls": ["https://example.com/product-video.mp4", "https://example.com/company-logo.png"]
  }'
```

### 2. Add Text Watermark

Add text-based watermarks like copyright notices or channel names.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Add a text watermark to this video saying \"Copyright 2024 MyBrand\" in white text with black outline. Position it in the bottom left corner, make it subtle but readable.",
    "mode": "max",
    "image_urls": ["https://example.com/my-video.mp4"]
  }'
```

### 3. Add Transparent Watermark

Create subtle, semi-transparent watermarks that protect content without being intrusive.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Add a very subtle transparent watermark with my logo. Use only 20% opacity so it is barely visible but still present. Position in the bottom right corner.",
    "mode": "max",
    "image_urls": ["https://example.com/cinematic-video.mp4", "https://example.com/watermark-logo.png"]
  }'
```

### 4. Position Watermark (Corner and Center)

Precisely control watermark placement for different video styles.

```bash
# Corner placement for vlog style
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Add my channel logo in the top left corner of this video. Make it small and semi-transparent. The watermark should have a slight drop shadow for visibility on light backgrounds.",
    "mode": "max",
    "image_urls": ["https://example.com/vlog-video.mp4", "https://example.com/channel-logo.png"]
  }'

# Center placement for preview/draft
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Add a large DRAFT watermark text diagonally across the center of this video. Use white text with black stroke, 50% opacity. This is for preview purposes.",
    "mode": "max",
    "image_urls": ["https://example.com/preview-video.mp4"]
  }'
```

### 5. Animated Watermark

Add dynamic, animated watermarks that draw attention or add visual interest.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Add an animated watermark to this video. The logo should have a subtle pulsing glow effect. Place it in the bottom right corner. The animation should loop smoothly every 2 seconds.",
    "mode": "max",
    "image_urls": ["https://example.com/promo-video.mp4", "https://example.com/animated-logo.gif"]
  }'
```

### 6. Remove Watermark from Video

Intelligently remove existing watermarks while preserving video quality.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Remove the watermark from this video. There is a logo watermark in the bottom right corner that needs to be removed cleanly without affecting the rest of the video.",
    "mode": "max",
    "image_urls": ["https://example.com/watermarked-video.mp4"]
  }'
```

### 7. Remove TikTok Watermark

Remove TikTok logos and username watermarks from downloaded videos.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Remove the TikTok watermark from this video. There is a TikTok logo and username in the corner that needs to be removed. Preserve the original video quality and ensure no artifacts remain.",
    "mode": "max",
    "image_urls": ["https://example.com/tiktok-video.mp4"]
  }'
```

### 8. Remove Stock Footage Watermark

Remove watermarks from stock footage that you have licensed.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Remove the stock footage watermark from this video. It has a repeating diagonal text watermark across the entire frame saying the stock site name. I have licensed this footage and need a clean version.",
    "mode": "max",
    "image_urls": ["https://example.com/stock-footage-preview.mp4"]
  }'
```

### 9. Add Dynamic Watermark (Changes Position)

Add watermarks that move or change position throughout the video to prevent easy removal.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Add a dynamic watermark to this video that changes position every 5 seconds. The watermark should move between all four corners of the video. Use my logo with 30% opacity. This makes the watermark harder to remove.",
    "mode": "max",
    "image_urls": ["https://example.com/protected-content.mp4", "https://example.com/brand-logo.png"]
  }'
```

### 10. Batch Watermark Multiple Videos

Apply consistent watermarks across multiple videos in a session.

```bash
# First video in batch
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "I need to add the same watermark to multiple videos. Start with this first video. Add my logo in the bottom right corner with 35% opacity. Remember these settings for the next videos.",
    "session_id": "batch-watermark-001",
    "mode": "eco",
    "image_urls": ["https://example.com/video-1.mp4", "https://example.com/company-logo.png"]
  }'

# Second video (same session for consistency)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Apply the same watermark settings to this second video.",
    "session_id": "batch-watermark-001",
    "mode": "eco",
    "image_urls": ["https://example.com/video-2.mp4"]
  }'

# Third video (same session)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Apply the same watermark settings to this third video.",
    "session_id": "batch-watermark-001",
    "mode": "eco",
    "image_urls": ["https://example.com/video-3.mp4"]
  }'
```

## Best Practices

### Adding Watermarks
- **Opacity**: Use 20-40% opacity for subtle branding, 50-70% for visible protection
- **Size**: Keep logo watermarks at 5-15% of video width for professional look
- **Position**: Bottom corners are standard; avoid center unless for drafts/previews
- **Contrast**: Add shadow or outline to watermarks for visibility on varied backgrounds
- **Consistency**: Use the same watermark settings across all your content

### Removing Watermarks
- **Quality**: Higher quality source videos yield better removal results
- **Simple backgrounds**: Watermarks over simple/uniform areas are easier to remove
- **Multiple watermarks**: Specify all watermark locations for comprehensive removal
- **Legal use**: Only remove watermarks from content you own or have licensed

## Mode Selection

Ask your users before generating:

**"Do you want fast & cheap, or high quality?"**

| Mode | Best For | Speed | Quality |
|------|----------|-------|---------|
| `max` | Final output, professional content, watermark removal | Slower | Highest |
| `eco` | Batch processing, drafts, testing placement | Faster | Good |

## Multi-Turn Watermark Iteration

Use `session_id` to refine watermark placement:

```bash
# Initial watermark
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Add my logo watermark to this video in the bottom right corner",
    "session_id": "watermark-project-001",
    "image_urls": ["https://example.com/my-video.mp4", "https://example.com/logo.png"]
  }'

# Adjust based on feedback
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "The watermark is too large and too opaque. Make it 50% smaller and reduce opacity to 25%",
    "session_id": "watermark-project-001"
  }'

# Final adjustment
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Move it slightly more to the center to avoid the video controls overlay area",
    "session_id": "watermark-project-001"
  }'
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | Insufficient balance | Top up at eachlabs.ai |
| Content policy violation | Prohibited content | Ensure content complies with terms of service |
| Timeout | Long video processing | Set client timeout to minimum 10 minutes |
| Invalid video format | Unsupported format | Convert to MP4, MOV, or WebM |
| Watermark not detected | AI cannot locate watermark | Specify watermark location more precisely |

## Related Skills

- `each-sense` - Core API documentation
- `video-generation` - Create videos from scratch
- `video-edit` - General video editing capabilities
- `image-edit` - Image watermarking and editing
