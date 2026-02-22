---
name: video-stabilization
description: Stabilize shaky video footage using each::sense AI. Remove camera shake from handheld footage, action cameras, drones, and more with intelligent motion correction.
metadata:
  author: eachlabs
  version: "1.0"
---

# Video Stabilization

Stabilize shaky video footage using each::sense. This skill applies intelligent motion correction to remove camera shake, smooth handheld footage, and create professional-looking stable video from various sources.

## Features

- **Shake Removal**: Basic camera shake correction for mildly unstable footage
- **Handheld Stabilization**: Smooth out natural hand movement from phone/camera footage
- **Action Camera**: Stabilize high-motion GoPro and action camera footage
- **Walking/Running**: Fix bounce and shake from movement while filming
- **Drone Footage**: Smooth aerial footage affected by wind or vibration
- **Vehicle Footage**: Stabilize dashcam and in-car recording
- **Low Light**: Handle shaky footage shot in challenging lighting conditions
- **Lock Shot**: Aggressive stabilization for tripod-like results
- **Subtle Stabilization**: Preserve natural camera movement while reducing shake
- **Crop Optimization**: Balance stabilization strength with frame cropping

## Quick Start

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Stabilize this shaky video, remove the camera shake",
    "mode": "max",
    "video_urls": ["https://example.com/shaky-video.mp4"]
  }'
```

## Stabilization Modes

| Mode | Description | Best For |
|------|-------------|----------|
| Subtle | Light stabilization, keeps natural movement | Documentary, vlog style |
| Standard | Balanced shake removal | General purpose |
| Aggressive | Maximum stabilization, locked shot | Professional, tripod-like |

## Use Case Examples

### 1. Basic Shake Removal

Simple camera shake correction for mildly unstable footage.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Stabilize this video and remove the camera shake. Apply standard stabilization.",
    "mode": "max",
    "video_urls": ["https://example.com/shaky-footage.mp4"]
  }'
```

### 2. Handheld Footage Stabilization

Smooth out natural hand movement from smartphone or camera footage.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "This is handheld smartphone footage. Stabilize it to look smoother while keeping it natural, not too robotic. Remove the jitter from hand movement.",
    "mode": "max",
    "video_urls": ["https://example.com/handheld-phone-video.mp4"]
  }'
```

### 3. Action Camera Stabilization

Stabilize high-motion GoPro and action camera footage from extreme sports.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Stabilize this GoPro action camera footage. It has significant shake from mountain biking. Apply strong stabilization to smooth out the bumps while preserving the sense of motion.",
    "mode": "max",
    "video_urls": ["https://example.com/gopro-mtb-footage.mp4"]
  }'
```

### 4. Walking/Running Footage Fix

Remove bounce and vertical shake from footage shot while moving on foot.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Fix this walking footage. Remove the up and down bounce from each step while keeping the forward motion smooth. The camera was handheld while walking through a market.",
    "mode": "max",
    "video_urls": ["https://example.com/walking-market-footage.mp4"]
  }'
```

### 5. Drone Footage Smoothing

Smooth aerial footage affected by wind, vibration, or gimbal issues.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Stabilize this drone footage. There is micro-vibration and some wind shake affecting the shot. Make it smooth and cinematic for a real estate showcase video.",
    "mode": "max",
    "video_urls": ["https://example.com/drone-aerial-footage.mp4"]
  }'
```

### 6. Car/Vehicle Footage Stabilization

Stabilize dashcam, in-car, or vehicle-mounted camera footage.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Stabilize this dashcam footage from a car driving on rough roads. Remove the vibration and bumps from the road while keeping the driving perspective stable.",
    "mode": "max",
    "video_urls": ["https://example.com/dashcam-rough-road.mp4"]
  }'
```

### 7. Low Light Shaky Footage

Handle shaky footage shot in challenging low-light conditions.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Stabilize this low light concert footage. It was shot handheld at night with significant shake. Be careful with the stabilization as low light footage can show more artifacts. Prioritize smooth motion over aggressive correction.",
    "mode": "max",
    "video_urls": ["https://example.com/concert-lowlight-shaky.mp4"]
  }'
```

### 8. Aggressive Stabilization (Lock Shot)

Maximum stabilization for tripod-like locked shot results.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Apply aggressive stabilization to lock this shot completely. I want it to look like it was shot on a tripod. Remove all camera movement and shake. It is okay to crop more of the frame if needed for maximum stability.",
    "mode": "max",
    "video_urls": ["https://example.com/interview-handheld.mp4"]
  }'
```

### 9. Subtle Stabilization (Keep Natural Movement)

Preserve natural camera movement while only reducing noticeable shake.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Apply subtle stabilization to this documentary footage. I want to keep the natural handheld feel and intentional camera movements, but remove only the unwanted micro-shakes and jitter. Do not make it look too smooth or artificial.",
    "mode": "max",
    "video_urls": ["https://example.com/documentary-handheld.mp4"]
  }'
```

### 10. Stabilize and Crop Optimization

Balance stabilization strength with minimal frame cropping.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Stabilize this footage but optimize for minimal cropping. The framing is important and I cannot lose too much of the edges. Find the best balance between stabilization quality and preserving the original frame as much as possible.",
    "mode": "max",
    "video_urls": ["https://example.com/tight-framing-shaky.mp4"]
  }'
```

## Mode Selection

Ask your users before processing:

**"Do you want fast processing or maximum quality?"**

| Mode | Best For | Speed | Quality |
|------|----------|-------|---------|
| `max` | Final deliverables, professional projects | Slower | Highest |
| `eco` | Quick previews, draft reviews, high volume | Faster | Good |

## Multi-Turn Stabilization Workflow

Use `session_id` to iterate on stabilization settings:

```bash
# Initial stabilization
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Stabilize this shaky video footage",
    "session_id": "stabilize-project-001",
    "video_urls": ["https://example.com/shaky-video.mp4"]
  }'

# Request adjustment
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "The stabilization is too aggressive, it looks artificial. Can you apply a more subtle stabilization that keeps some natural movement?",
    "session_id": "stabilize-project-001"
  }'

# Further refinement
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Good, but now there is too much cropping. Can you reduce the crop while maintaining similar stabilization?",
    "session_id": "stabilize-project-001"
  }'
```

## Batch Processing Multiple Videos

Process multiple videos with consistent settings:

```bash
# Video 1
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Stabilize this video with medium strength stabilization",
    "mode": "eco",
    "video_urls": ["https://example.com/clip1.mp4"]
  }'

# Video 2
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Stabilize this video with medium strength stabilization",
    "mode": "eco",
    "video_urls": ["https://example.com/clip2.mp4"]
  }'

# Video 3
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Stabilize this video with medium strength stabilization",
    "mode": "eco",
    "video_urls": ["https://example.com/clip3.mp4"]
  }'
```

## Best Practices

### Input Video Quality
- **Resolution**: Higher resolution footage gives better stabilization results
- **Frame Rate**: Higher frame rates (60fps+) provide smoother stabilization
- **Codec**: Use high-quality source files, avoid heavily compressed inputs

### Stabilization Settings
- **Start Subtle**: Begin with lighter stabilization and increase if needed
- **Consider Cropping**: More aggressive stabilization requires more cropping
- **Match Style**: Keep stabilization consistent across clips in the same project

### Common Scenarios

| Scenario | Recommended Approach |
|----------|---------------------|
| Interview/talking head | Aggressive/lock shot |
| Documentary/vlog | Subtle, natural feel |
| Sports/action | Medium, preserve motion |
| Drone/aerial | Medium to aggressive |
| Walking tour | Medium, reduce bounce |
| Low light | Subtle, avoid artifacts |

## Prompt Tips for Video Stabilization

When requesting stabilization, include these details:

1. **Source Type**: What camera/device captured the footage?
2. **Shake Cause**: Walking, vehicle, wind, handheld, etc.
3. **Desired Result**: Lock shot, natural feel, smooth but dynamic
4. **Cropping Tolerance**: Is the framing critical or flexible?
5. **Use Case**: Social media, professional, documentary, etc.

### Example Prompt Structure

```
"Stabilize this [source type] footage.
The shake is caused by [cause].
I want [desired result] stabilization.
[Cropping preference].
This is for [use case]."
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | Insufficient balance | Top up at eachlabs.ai |
| Video format not supported | Incompatible codec | Convert to MP4/H.264 |
| Timeout | Long video processing | Set client timeout to minimum 10 minutes |
| Excessive cropping | Too much shake | Use subtle mode or accept more crop |

## Related Skills

- `each-sense` - Core API documentation
- `video-edit` - General video editing capabilities
- `video-generation` - AI video generation
