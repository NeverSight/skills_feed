---
name: video-trimming
description: Trim, cut, and split videos using each::sense AI. Extract specific segments, remove intros/outros, create social media clips, detect scenes automatically, and batch process multiple videos.
metadata:
  author: eachlabs
  version: "1.0"
---

# Video Trimming

Trim, cut, and split videos using each::sense. This skill enables precise video editing operations including segment extraction, scene detection, silence removal, and batch processing for social media optimization.

## Features

- **Precise Trimming**: Cut videos to exact timestamps or durations
- **Segment Extraction**: Extract specific portions from the middle of videos
- **Intro/Outro Removal**: Clean up videos by removing unwanted beginnings or endings
- **Video Splitting**: Divide long videos into multiple shorter clips
- **Highlight Extraction**: Pull out key moments from longer content
- **Silence Removal**: Automatically detect and remove dead air or silent portions
- **Scene Detection**: Smart cuts based on visual scene changes
- **Social Media Optimization**: Trim to platform-specific lengths (15s, 30s, 60s)
- **Loop-Friendly Edits**: Create seamless loops for social media
- **Batch Processing**: Process multiple videos with consistent trimming rules

## Quick Start

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Trim this video to the first 30 seconds",
    "mode": "max",
    "video_urls": ["https://example.com/my-video.mp4"]
  }'
```

## Trimming Operations Reference

| Operation | Description | Example Use Case |
|-----------|-------------|------------------|
| Duration Trim | Cut to specific length from start | Social media clips |
| Timestamp Trim | Extract between start/end times | Interview segments |
| Intro Removal | Remove first N seconds | Clean up recordings |
| Outro Removal | Remove last N seconds | Remove end cards |
| Segment Extraction | Pull middle portion | Highlight reels |
| Scene Split | Divide by visual changes | Chapter creation |
| Silence Removal | Cut silent portions | Podcast editing |
| Batch Trim | Process multiple videos | Content repurposing |

## Use Case Examples

### 1. Trim Video to Specific Duration

Trim a video to a specific length from the beginning.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Trim this video to exactly 60 seconds, keeping the first minute only",
    "mode": "max",
    "video_urls": ["https://example.com/full-video.mp4"]
  }'
```

### 2. Cut Segment from Middle

Extract a specific portion from the middle of a video using timestamps.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Cut out the segment from 1:30 to 2:45 of this video. I want just that middle portion as a standalone clip.",
    "mode": "max",
    "video_urls": ["https://example.com/interview.mp4"]
  }'
```

### 3. Remove Intro and Outro

Clean up a video by removing unwanted intro and outro sections.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Remove the first 10 seconds (intro) and last 15 seconds (outro) from this video. Keep only the main content in the middle.",
    "mode": "max",
    "video_urls": ["https://example.com/youtube-video.mp4"]
  }'
```

### 4. Split Video into Multiple Clips

Divide a long video into several shorter segments.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Split this 5-minute video into five 1-minute clips. Each clip should be a separate output.",
    "mode": "max",
    "video_urls": ["https://example.com/long-video.mp4"]
  }'
```

### 5. Extract Highlight Moments

Pull out the best moments from a longer video.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Extract the most engaging or action-packed moments from this video. Create a highlight reel of the best 30 seconds.",
    "mode": "max",
    "video_urls": ["https://example.com/sports-footage.mp4"]
  }'
```

### 6. Remove Silence and Dead Air

Automatically detect and remove silent portions from a video.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Remove all silent portions and dead air from this video. Cut out any segments where there is no speaking or significant audio for more than 2 seconds.",
    "mode": "max",
    "video_urls": ["https://example.com/podcast-recording.mp4"]
  }'
```

### 7. Smart Scene Detection Cut

Use AI to detect scene changes and split the video accordingly.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Analyze this video and split it into separate clips based on scene changes. Each time the visual scene changes significantly, create a new clip.",
    "mode": "max",
    "video_urls": ["https://example.com/multi-scene-video.mp4"]
  }'
```

### 8. Batch Trim Multiple Videos

Process multiple videos with the same trimming rules using session continuity.

```bash
# First video
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Trim this video to 30 seconds from the start. We will process multiple videos with the same rule.",
    "session_id": "batch-trim-001",
    "mode": "eco",
    "video_urls": ["https://example.com/video1.mp4"]
  }'

# Second video (same session)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Apply the same 30-second trim to this video",
    "session_id": "batch-trim-001",
    "mode": "eco",
    "video_urls": ["https://example.com/video2.mp4"]
  }'

# Third video (same session)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "And the same for this one",
    "session_id": "batch-trim-001",
    "mode": "eco",
    "video_urls": ["https://example.com/video3.mp4"]
  }'
```

### 9. Trim to Social Media Length

Optimize videos for specific social media platform requirements.

```bash
# Instagram Reels / TikTok (15 seconds)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Trim this video to exactly 15 seconds for Instagram Reels. Pick the most engaging 15-second segment.",
    "mode": "max",
    "video_urls": ["https://example.com/content.mp4"]
  }'

# YouTube Shorts (30 seconds)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 30-second clip optimized for YouTube Shorts from this video. Focus on the hook at the start.",
    "mode": "max",
    "video_urls": ["https://example.com/content.mp4"]
  }'

# Standard social clip (60 seconds)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Trim to 60 seconds maximum for Twitter/X. Keep the most important content.",
    "mode": "max",
    "video_urls": ["https://example.com/content.mp4"]
  }'
```

### 10. Loop-Friendly Trim

Create seamlessly looping video clips for social media.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Trim this video to create a seamless loop. Find a segment where the end flows naturally back to the beginning, ideally 5-10 seconds long for a satisfying social media loop.",
    "mode": "max",
    "video_urls": ["https://example.com/loopable-content.mp4"]
  }'
```

## Best Practices

### Trimming Tips
- **Be specific**: Provide exact timestamps (MM:SS or HH:MM:SS) when possible
- **Describe content**: If you do not know timestamps, describe what you want ("the part where they shake hands")
- **Buffer time**: Allow small buffers around cuts to avoid abrupt transitions
- **Check audio**: Ensure cuts do not happen mid-sentence or mid-note

### Performance Optimization
- **Use `eco` mode** for batch processing or quick iterations
- **Use `max` mode** for final exports and quality-critical content
- **Process shorter videos first** to verify settings before batch operations

### Social Media Guidelines

| Platform | Recommended Length | Notes |
|----------|-------------------|-------|
| TikTok | 15-60 seconds | Hook in first 3 seconds |
| Instagram Reels | 15-30 seconds | 90 seconds max |
| YouTube Shorts | 30-60 seconds | Under 60 seconds required |
| Twitter/X | 30-60 seconds | 2:20 max for standard accounts |
| LinkedIn | 30-90 seconds | Professional context |

## Prompt Tips for Video Trimming

When requesting video trims, include these details:

1. **Exact timing**: "from 0:45 to 1:30" or "first 30 seconds"
2. **Content reference**: "the interview segment" or "when the product demo starts"
3. **Output requirements**: "keep audio" or "I need 3 separate clips"
4. **Platform target**: "for Instagram Reels" or "YouTube Shorts optimized"
5. **Quality preference**: Use `mode: "max"` for finals, `mode: "eco"` for drafts

### Example Prompt Structure

```
"[Action] this video [timing/selection criteria].
[Additional requirements like output format, platform, etc.]"
```

Examples:
- "Trim this video to 30 seconds starting at 1:00"
- "Extract three 15-second highlights from different parts of this video"
- "Remove the first 5 seconds and last 10 seconds"

## Mode Selection

**"Do you want fast & cheap, or high quality?"**

| Mode | Best For | Speed | Quality |
|------|----------|-------|---------|
| `max` | Final exports, client deliverables, quality-critical | Slower | Highest |
| `eco` | Quick previews, batch processing, draft iterations | Faster | Good |

## Multi-Turn Editing Session

Use `session_id` to iterate on video edits:

```bash
# Initial trim
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Trim this video to the segment from 0:30 to 1:30",
    "session_id": "edit-session-001",
    "video_urls": ["https://example.com/raw-footage.mp4"]
  }'

# Adjust the trim
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Actually, extend the end by 10 more seconds to include the conclusion",
    "session_id": "edit-session-001"
  }'

# Request additional version
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a shorter 15-second version of this same segment for Instagram",
    "session_id": "edit-session-001"
  }'
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | Insufficient balance | Top up at eachlabs.ai |
| Timeout | Long video processing | Set client timeout to minimum 10 minutes |
| Invalid timestamp | Timestamp exceeds video length | Verify video duration first |
| Unsupported format | Video codec not supported | Convert to MP4/H.264 first |

## Related Skills

- `each-sense` - Core API documentation
- `video-generation` - Create videos from scratch
- `video-editing` - Advanced video editing operations
- `video-to-video` - Transform and style transfer videos
