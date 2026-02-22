---
name: video-background-removal
description: Remove, replace, or modify video backgrounds using each::sense AI. Create transparent backgrounds, virtual offices, green screen effects without green screens, blur effects, and professional video compositing.
metadata:
  author: eachlabs
  version: "1.0"
---

# Video Background Removal

Remove and replace video backgrounds using each::sense. This skill enables transparent backgrounds, virtual environments, professional compositing, and creative background effects for any video content.

## Features

- **Transparent Backgrounds**: Remove backgrounds completely for compositing
- **Solid Color Replacement**: Replace with any solid color (white, black, brand colors)
- **Image Backgrounds**: Composite subjects onto static image backgrounds
- **Video Backgrounds**: Place subjects into dynamic video backgrounds
- **Virtual Offices**: Professional meeting backgrounds for remote work
- **Green Screen Effect**: Achieve chroma key results without actual green screens
- **Background Blur**: Privacy-preserving blur effects for video calls
- **Animated Backgrounds**: Dynamic motion graphics behind subjects
- **Product Videos**: Clean product footage with removed/replaced backgrounds
- **Talking Head Videos**: Professional presenter backgrounds

## Quick Start

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Remove the background from this video and make it transparent",
    "mode": "max",
    "video_urls": ["https://example.com/my-video.mp4"]
  }'
```

## Use Case Examples

### 1. Remove Video Background (Transparent)

Create a video with transparent background for compositing in video editors.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Remove the background from this video completely. Output should have a transparent background so I can composite it in my video editor. Keep the subject cleanly isolated with smooth edges.",
    "mode": "max",
    "video_urls": ["https://example.com/presenter-video.mp4"]
  }'
```

### 2. Replace with Solid Color

Replace background with a clean solid color for professional content.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Replace the background of this video with a solid white background. Keep the subject sharp and well-isolated. Clean edges, professional look suitable for corporate presentations.",
    "mode": "max",
    "video_urls": ["https://example.com/interview-clip.mp4"]
  }'
```

### 3. Replace with Image Background

Composite subject onto a static image background.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Remove the background from this video and replace it with the provided image. Blend the subject naturally into the new scene with appropriate lighting and shadows.",
    "mode": "max",
    "video_urls": ["https://example.com/person-talking.mp4"],
    "image_urls": ["https://example.com/beach-sunset-background.jpg"]
  }'
```

### 4. Replace with Video Background

Create dynamic composites with moving video backgrounds.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Remove the background from my video and replace it with the second video as the new background. Sync the timing and make the composite look natural.",
    "mode": "max",
    "video_urls": [
      "https://example.com/foreground-subject.mp4",
      "https://example.com/cityscape-background.mp4"
    ]
  }'
```

### 5. Virtual Office Background

Create professional virtual meeting backgrounds.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Replace the background with a professional modern office environment. Clean minimalist design with bookshelves, plants, and soft natural lighting. Suitable for executive video calls and professional meetings.",
    "mode": "max",
    "video_urls": ["https://example.com/webcam-recording.mp4"]
  }'
```

### 6. Green Screen Replacement (Without Green Screen)

Achieve chroma key quality results from any video, no green screen needed.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Extract the person from this video as if it was shot on a green screen. Clean matte extraction with no background spill. Output with transparent background or green screen color for post-production keying.",
    "mode": "max",
    "video_urls": ["https://example.com/filmed-at-home.mp4"]
  }'
```

### 7. Blur Background in Video

Apply privacy-preserving background blur for video calls and content.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Apply a smooth gaussian blur to the background while keeping the person in focus. Moderate blur intensity - enough to hide details but keep sense of depth. Natural bokeh effect like a portrait mode camera.",
    "mode": "max",
    "video_urls": ["https://example.com/home-office-call.mp4"]
  }'
```

### 8. Replace with Animated Background

Add dynamic motion graphics or animated backgrounds.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Remove the background and replace it with an animated gradient background. Smooth flowing colors transitioning between blue and purple. Subtle movement, not distracting. Professional motion graphics style.",
    "mode": "max",
    "video_urls": ["https://example.com/content-creator.mp4"]
  }'
```

### 9. Product Video Background Removal

Clean product footage for e-commerce and marketing.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Remove the background from this product video. The product is a rotating sneaker on a turntable. Make the background pure white for e-commerce use. Maintain all product details, reflections, and shadows.",
    "mode": "max",
    "video_urls": ["https://example.com/product-360-spin.mp4"]
  }'
```

### 10. Talking Head Background Swap

Professional presenter and talking head video backgrounds.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Replace the background in this talking head video with a professional studio setting. Dark backdrop with subtle colored accent lighting like a podcast studio or news desk. Keep the presenter well-lit and naturally composited.",
    "mode": "max",
    "video_urls": ["https://example.com/youtube-video.mp4"]
  }'
```

## Multi-Turn Workflow Example

Use `session_id` to iterate on background replacements across multiple requests.

```bash
# Initial background removal
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Remove the background from this video of me presenting",
    "session_id": "bg-removal-project-001",
    "video_urls": ["https://example.com/presentation.mp4"]
  }'

# Iterate with different background
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Now replace it with a modern tech office background instead",
    "session_id": "bg-removal-project-001"
  }'

# Fine-tune the result
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "The edges look a bit rough around my hair. Can you refine the matte for better edge quality?",
    "session_id": "bg-removal-project-001"
  }'
```

## Mode Selection

Choose the appropriate mode based on your needs:

| Mode | Best For | Speed | Quality |
|------|----------|-------|---------|
| `max` | Final production videos, client deliverables | Slower | Highest quality, best edge detection |
| `eco` | Quick previews, concept testing, drafts | Faster | Good quality, suitable for review |

**Recommendation:** Use `eco` mode for testing backgrounds and `max` mode for final renders.

## Best Practices

### For Clean Extractions
- **Lighting**: Well-lit subjects extract better than low-light footage
- **Contrast**: Higher contrast between subject and background helps
- **Movement**: Slower movements produce cleaner mattes
- **Hair/Fine Details**: Request "refined edges" for subjects with complex hair

### For Natural Composites
- **Lighting Match**: Request backgrounds that match your footage lighting
- **Color Grading**: Ask for color matching between subject and background
- **Shadows**: Request natural shadow placement for grounded composites
- **Depth of Field**: Match background blur to your camera's depth of field

### For Professional Results
- Specify your use case (corporate, social media, broadcast)
- Mention output requirements (resolution, format)
- Request specific background styles that match your brand

## Prompt Tips

When requesting background removal/replacement, include:

1. **Source Description**: What's in your video (person, product, etc.)
2. **Background Goal**: Transparent, solid color, specific scene, blur
3. **Quality Requirements**: Edge quality, shadow handling, reflections
4. **Use Case**: Where will this video be used
5. **Style Matching**: Lighting, color tone, atmosphere

### Example Prompt Structure

```
"Remove/replace the background from this [subject type] video.
[New background description or transparent/solid color].
[Edge quality and compositing requirements].
For use in [context/platform]."
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | Insufficient balance | Top up at eachlabs.ai |
| Timeout | Video processing takes time | Set client timeout to minimum 10 minutes |
| Poor edge quality | Complex hair/fine details | Request "refined edge detection" in prompt |
| Subject detection failed | Low contrast footage | Try with better lit footage or specify subject location |

## Timeout Configuration

Video background removal is computationally intensive. Configure your HTTP client with adequate timeout:

- **Minimum recommended timeout**: 10 minutes (600 seconds)
- **For longer videos**: Increase proportionally (1 minute timeout per 10 seconds of video)

```bash
# Example with explicit timeout using curl
curl --max-time 600 -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Remove background from this video",
    "mode": "max",
    "video_urls": ["https://example.com/long-video.mp4"]
  }'
```

## Related Skills

- `each-sense` - Core API documentation
- `product-video-generation` - E-commerce video creation
- `video-generation` - AI video generation
- `image-background-removal` - Static image background removal
