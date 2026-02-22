---
name: video-noise-reduction
description: Reduce noise and grain from videos using each::sense AI. Denoise low light footage, remove high ISO grain, enhance security camera video, restore old footage, and improve webcam quality.
metadata:
  author: eachlabs
  version: "1.0"
---

# Video Noise Reduction

Reduce noise, grain, and artifacts from videos using each::sense. This skill handles low light footage, high ISO grain, security camera enhancement, old footage restoration, and various denoising tasks while preserving important details.

## Features

- **Low Light Denoising**: Clean up footage shot in dim conditions
- **High ISO Grain Removal**: Remove digital noise from high sensitivity recordings
- **Security Camera Enhancement**: Improve clarity of surveillance footage
- **Old Footage Restoration**: Restore vintage or degraded video
- **Webcam Quality Improvement**: Enhance video call recordings
- **Night Mode Cleanup**: Fix noisy night vision or low light phone footage
- **Compression Artifact Removal**: Clean up heavily compressed video
- **Film Grain Removal**: Remove unwanted grain from film scans
- **Detail Preservation**: Denoise while maintaining sharpness and texture

## Quick Start

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Denoise this video, reduce the grain while keeping details sharp",
    "mode": "max",
    "video_urls": ["https://example.com/noisy-video.mp4"]
  }'
```

## Denoising Parameters

| Parameter | Description | Use Case |
|-----------|-------------|----------|
| Strength | How aggressively to remove noise | Light for subtle cleanup, heavy for very noisy footage |
| Detail Preservation | Balance between smoothing and sharpness | Higher for footage with important textures |
| Temporal Consistency | Reduce flickering between frames | Essential for video to avoid artifacts |
| Color Denoising | Clean chroma noise separately | Useful for high ISO color noise |

## Use Case Examples

### 1. Low Light Video Denoising

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "This video was shot in very low light conditions. Please denoise it while maintaining natural skin tones and avoiding the plastic look. Keep the atmospheric mood but reduce the heavy grain.",
    "mode": "max",
    "video_urls": ["https://example.com/low-light-indoor.mp4"]
  }'
```

### 2. High ISO Grain Removal

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Remove the high ISO digital noise from this video. It was shot at ISO 12800 and has significant luminance and color noise. Clean it up while preserving edge details and facial features.",
    "mode": "max",
    "video_urls": ["https://example.com/high-iso-concert.mp4"]
  }'
```

### 3. Security Camera Enhancement

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Enhance this security camera footage. Reduce the noise and compression artifacts, improve clarity so faces and license plates are more readable. The footage is from a night vision camera.",
    "mode": "max",
    "video_urls": ["https://example.com/security-cam-footage.mp4"]
  }'
```

### 4. Old Footage Restoration

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Restore this old family video from the 90s. Remove the tape noise, reduce flickering, clean up the color bleeding, and improve overall clarity. Keep it looking natural, not overly processed.",
    "mode": "max",
    "video_urls": ["https://example.com/vhs-family-video.mp4"]
  }'
```

### 5. Webcam Quality Improvement

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Improve this webcam recording quality. It has noise from the small sensor and poor lighting. Denoise the footage, reduce the graininess, and make the speaker look clearer for a professional presentation.",
    "mode": "max",
    "video_urls": ["https://example.com/zoom-recording.mp4"]
  }'
```

### 6. Night Mode Video Cleanup

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Clean up this night mode video shot on a smartphone. Remove the excessive noise reduction artifacts, smooth out the blotchy areas, and fix the color noise in the shadows while keeping highlights intact.",
    "mode": "max",
    "video_urls": ["https://example.com/iphone-night-mode.mp4"]
  }'
```

### 7. Compression Artifact Removal

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Remove compression artifacts from this video. It was heavily compressed and has visible blocking, banding, and mosquito noise around edges. Clean it up to look like higher quality footage.",
    "mode": "max",
    "video_urls": ["https://example.com/compressed-video.mp4"]
  }'
```

### 8. Film Grain Removal

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Remove the film grain from this scanned 16mm footage. I want a clean digital look without the organic grain texture. Preserve the original colors and contrast but give it a smooth modern appearance.",
    "mode": "max",
    "video_urls": ["https://example.com/16mm-film-scan.mp4"]
  }'
```

### 9. Preserve Detail While Denoising

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Denoise this nature documentary footage. It has noise from shooting at dusk. Important: preserve fine details like animal fur texture, feather patterns, and grass blades. Only remove noise, do not smooth out real textures.",
    "mode": "max",
    "video_urls": ["https://example.com/wildlife-footage.mp4"]
  }'
```

### 10. Batch Denoise Multiple Clips

```bash
# First clip
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "I have several clips from the same shoot that need denoising. Starting with clip 1 - apply moderate noise reduction suitable for low light indoor footage. Remember these settings for the next clips.",
    "session_id": "batch-denoise-project-001",
    "video_urls": ["https://example.com/project/clip-01.mp4"]
  }'

# Second clip (same session for consistency)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Apply the same denoising settings to clip 2 from the same project. Keep the results consistent with the first clip.",
    "session_id": "batch-denoise-project-001",
    "video_urls": ["https://example.com/project/clip-02.mp4"]
  }'

# Third clip (same session)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Continue with clip 3, same settings as before.",
    "session_id": "batch-denoise-project-001",
    "video_urls": ["https://example.com/project/clip-03.mp4"]
  }'
```

## Best Practices

### Denoising Guidelines
- **Start Conservative**: Begin with lighter denoising and increase if needed
- **Preserve Motion**: Ensure temporal consistency to avoid flickering artifacts
- **Watch Skin Tones**: Aggressive denoising can create unnatural "plastic" skin
- **Maintain Texture**: Real textures (fabric, hair, foliage) should be preserved
- **Check Dark Areas**: Shadows often contain the most noise - focus there

### Input Considerations
- **Higher Resolution Source**: Better input quality yields better results
- **Uncompressed Preferred**: Work with least compressed source available
- **Color Space**: Maintain original color space when possible
- **Frame Rate**: Temporal denoising works better with higher frame rates

### Output Quality
- **Preview First**: Test on a short section before processing full video
- **Compare A/B**: Check before/after to ensure details are preserved
- **Export Settings**: Use high quality export to avoid reintroducing artifacts

## Prompt Tips for Video Denoising

When requesting video noise reduction, include these details:

1. **Noise Type**: Describe the kind of noise (grain, digital, compression, etc.)
2. **Source**: How was it captured (camera type, ISO, lighting conditions)
3. **Priority Areas**: What details must be preserved (faces, text, textures)
4. **Desired Look**: Natural vs. heavily processed, film vs. digital
5. **Problem Areas**: Specific issues to address (shadows, highlights, motion)

### Example Prompt Structure

```
"Denoise this [source type] video.
The noise is caused by [reason - low light/high ISO/compression].
Priority: preserve [important details like faces, text, textures].
Remove [specific noise types] while keeping [what to preserve].
[Any additional requirements]"
```

## Mode Selection

Ask your users before processing:

**"Do you want fast processing or maximum quality?"**

| Mode | Best For | Speed | Quality |
|------|----------|-------|---------|
| `max` | Final deliverables, client work, important footage | Slower | Highest |
| `eco` | Quick previews, test runs, bulk processing drafts | Faster | Good |

## Multi-Turn Iterative Denoising

Use `session_id` to refine denoising results:

```bash
# Initial denoise attempt
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Denoise this low light interview footage",
    "session_id": "interview-denoise-project",
    "video_urls": ["https://example.com/interview-raw.mp4"]
  }'

# Request adjustment
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "The skin looks too smooth and plastic. Can you redo it with more detail preservation? Keep some natural skin texture while still removing the noise.",
    "session_id": "interview-denoise-project"
  }'

# Fine-tune specific areas
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Better! But the background still has some noise. Can you apply stronger denoising to the out-of-focus background while keeping the subject sharp?",
    "session_id": "interview-denoise-project"
  }'
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | Insufficient balance | Top up at eachlabs.ai |
| Timeout | Video processing takes time | Set client timeout to minimum 10 minutes |
| Unsupported format | Codec not supported | Convert to MP4 H.264 before processing |
| File too large | Video exceeds size limits | Split into shorter segments |

## Related Skills

- `each-sense` - Core API documentation
- `video-upscaling` - Increase video resolution
- `video-enhancement` - General video quality improvement
- `video-stabilization` - Remove camera shake
