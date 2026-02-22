---
name: video-format-conversion
description: Convert videos between formats, codecs, and aspect ratios using each::sense AI. Support for MP4, WebM, GIF, ProRes, and social media optimized outputs.
metadata:
  author: eachlabs
  version: "1.0"
---

# Video Format Conversion

Convert videos between formats, codecs, and aspect ratios using each::sense. This skill handles format conversion, codec transcoding, aspect ratio changes, and optimization for various platforms and use cases.

## Features

- **Format Conversion**: Convert between MP4, WebM, MOV, GIF, and more
- **Codec Transcoding**: H.264, H.265/HEVC, VP9, ProRes, and others
- **Aspect Ratio Changes**: 16:9 to 9:16, 1:1, 4:3, and custom ratios
- **Platform Optimization**: Instagram, TikTok, YouTube, Twitter optimized outputs
- **Web Streaming**: HLS-ready and web-optimized encoding
- **Quality Control**: Bitrate, resolution, and compression settings
- **Batch Processing**: Convert multiple videos in sequence

## Quick Start

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Convert this video to MP4 H.264 format optimized for web playback",
    "mode": "max",
    "image_urls": ["https://example.com/source-video.mov"]
  }'
```

## Supported Formats & Codecs

| Format | Codecs | Use Cases |
|--------|--------|-----------|
| MP4 | H.264, H.265/HEVC | Universal playback, web, mobile |
| WebM | VP9, VP8 | Web browsers, smaller file sizes |
| MOV | ProRes, H.264 | Professional editing, Apple ecosystem |
| GIF | - | Social media, previews, loops |
| MKV | H.264, H.265, VP9 | Archival, high quality |

## Aspect Ratios

| Ratio | Resolution | Use Case |
|-------|------------|----------|
| 16:9 | 1920x1080 | YouTube, standard landscape |
| 9:16 | 1080x1920 | TikTok, Instagram Reels, Stories |
| 1:1 | 1080x1080 | Instagram feed, Twitter |
| 4:3 | 1440x1080 | Classic TV, presentations |
| 4:5 | 1080x1350 | Instagram portrait posts |
| 21:9 | 2560x1080 | Cinematic ultrawide |

## Use Case Examples

### 1. Convert to MP4 (H.264)

Standard MP4 conversion with H.264 codec for maximum compatibility.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Convert this video to MP4 with H.264 codec. Use high quality settings with a bitrate suitable for 1080p playback. Maintain original aspect ratio.",
    "mode": "max",
    "image_urls": ["https://example.com/source-video.mov"]
  }'
```

### 2. Convert to WebM

WebM format with VP9 codec for efficient web delivery.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Convert this MP4 video to WebM format using VP9 codec. Optimize for web streaming with good quality at smaller file size. Target around 5 Mbps bitrate.",
    "mode": "max",
    "image_urls": ["https://example.com/source-video.mp4"]
  }'
```

### 3. Convert to GIF

Create animated GIF from video for social sharing and previews.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Convert this video to an animated GIF. Use the first 5 seconds, resize to 480px width, and optimize for file size under 10MB. Create a smooth loop if possible.",
    "mode": "eco",
    "image_urls": ["https://example.com/source-video.mp4"]
  }'
```

### 4. Convert 16:9 to 9:16 (Vertical)

Transform landscape video to vertical format for mobile platforms.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Convert this 16:9 landscape video to 9:16 vertical format. Use smart cropping to keep the main subject centered. Output as MP4 H.264 at 1080x1920 resolution.",
    "mode": "max",
    "image_urls": ["https://example.com/landscape-video.mp4"]
  }'
```

### 5. Convert to Square 1:1

Create square format video for Instagram feed and Twitter.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Convert this video to 1:1 square format at 1080x1080 resolution. Center crop the content and output as MP4 with H.264 codec optimized for social media.",
    "mode": "max",
    "image_urls": ["https://example.com/widescreen-video.mp4"]
  }'
```

### 6. Convert to 4:3

Classic 4:3 aspect ratio for presentations and legacy displays.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Convert this 16:9 video to 4:3 aspect ratio. Add letterboxing or pillarboxing as needed rather than cropping. Output at 1440x1080 resolution in MP4 format.",
    "mode": "eco",
    "image_urls": ["https://example.com/widescreen-video.mp4"]
  }'
```

### 7. Optimize for Web Streaming

Create web-optimized video with fast start and adaptive quality.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Optimize this video for web streaming. Convert to MP4 H.264 with faststart enabled for progressive download. Use 2-pass encoding, target 3-5 Mbps bitrate, AAC audio at 128kbps. Ensure moov atom is at the beginning for instant playback.",
    "mode": "max",
    "image_urls": ["https://example.com/raw-video.mov"]
  }'
```

### 8. Convert to Apple ProRes

Professional ProRes format for video editing workflows.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Convert this video to Apple ProRes 422 format in a MOV container. Maintain original resolution and frame rate. This is for professional editing in Final Cut Pro and DaVinci Resolve.",
    "mode": "max",
    "image_urls": ["https://example.com/compressed-video.mp4"]
  }'
```

### 9. Convert for Social Media (Instagram/TikTok)

Platform-optimized video for Instagram Reels and TikTok.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Convert this video for Instagram Reels and TikTok. Use 9:16 aspect ratio at 1080x1920, MP4 H.264 codec, 30fps, and optimize for mobile playback. Keep file size under 100MB and duration under 60 seconds.",
    "mode": "max",
    "image_urls": ["https://example.com/source-video.mov"]
  }'
```

### 10. Batch Convert Multiple Videos

Process multiple videos in a single session with consistent settings.

```bash
# Start batch conversion session
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "I need to convert multiple videos to MP4 H.264 format at 1080p. All videos should use the same encoding settings: H.264 High Profile, 8 Mbps bitrate, AAC audio at 192kbps. Start with this first video.",
    "session_id": "batch-convert-001",
    "mode": "eco",
    "image_urls": ["https://example.com/video1.mov"]
  }'

# Continue with second video (same session)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Convert the next video with the same settings.",
    "session_id": "batch-convert-001",
    "mode": "eco",
    "image_urls": ["https://example.com/video2.mov"]
  }'

# Continue with third video
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Convert this one too, same format.",
    "session_id": "batch-convert-001",
    "mode": "eco",
    "image_urls": ["https://example.com/video3.mov"]
  }'
```

## Mode Selection

Ask your users before converting:

**"Do you want fast & cheap, or high quality?"**

| Mode | Best For | Speed | Quality |
|------|----------|-------|---------|
| `max` | Final deliverables, ProRes, professional workflows | Slower | Highest |
| `eco` | Quick previews, batch processing, draft conversions | Faster | Good |

## Multi-Turn Conversion Session

Use `session_id` to maintain context for iterative conversions:

```bash
# Initial conversion
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Convert this video to MP4 for YouTube at 1080p",
    "session_id": "youtube-upload-project",
    "image_urls": ["https://example.com/raw-footage.mov"]
  }'

# Request different format from same source
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Now create a vertical version of that same video for YouTube Shorts at 9:16",
    "session_id": "youtube-upload-project"
  }'

# Request thumbnail extraction
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Extract a thumbnail from the best frame of that video",
    "session_id": "youtube-upload-project"
  }'
```

## Platform-Specific Settings

### YouTube
- Format: MP4 (H.264)
- Resolution: 1080p or 4K
- Frame rate: Match source (24, 30, or 60fps)
- Bitrate: 8-12 Mbps for 1080p, 35-45 Mbps for 4K

### Instagram Reels / TikTok
- Format: MP4 (H.264)
- Aspect ratio: 9:16
- Resolution: 1080x1920
- Duration: Under 60 seconds (Reels) / 3 minutes (TikTok)
- File size: Under 100MB

### Twitter/X
- Format: MP4 (H.264)
- Aspect ratio: 16:9, 1:1, or 9:16
- Resolution: Up to 1920x1200
- Duration: Up to 2:20 (140 seconds)
- File size: Under 512MB

### LinkedIn
- Format: MP4 (H.264)
- Aspect ratio: 16:9 or 1:1
- Resolution: 1080p maximum
- Duration: 10 minutes maximum

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | Insufficient balance | Top up at eachlabs.ai |
| Timeout | Large video file or complex conversion | Set client timeout to minimum 10 minutes |
| Unsupported format | Source format not recognized | Convert to intermediate format first |
| File too large | Video exceeds size limits | Compress or split video before conversion |

## Best Practices

### Quality
- Use `max` mode for final deliverables and professional outputs
- Use `eco` mode for previews and batch processing
- Specify target bitrate for predictable file sizes
- Request 2-pass encoding for better quality at lower bitrates

### Performance
- Set client timeout to minimum 10 minutes for video processing
- Use `eco` mode for faster turnaround on large batches
- Process shorter clips when testing settings

### Compatibility
- H.264 is the most universally compatible codec
- WebM/VP9 offers better compression but less device support
- ProRes is ideal for editing workflows but creates large files
- Always test output on target devices/platforms

## Related Skills

- `each-sense` - Core API documentation
- `video-generation` - Generate videos from text/images
- `video-editing` - Edit and enhance existing videos
