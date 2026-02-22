---
name: video-speed-adjustment
description: Adjust video speed using each::sense AI. Create slow motion, time-lapse, hyperlapse, speed ramps, reverse effects, and cinematic slow-mo with frame interpolation for smooth playback.
metadata:
  author: eachlabs
  version: "1.0"
---

# Video Speed Adjustment

Adjust video playback speed using each::sense. This skill enables speed manipulation for creative effects including slow motion, time-lapse, hyperlapse, speed ramping, reverse playback, and frame interpolation for ultra-smooth slow-mo.

## Features

- **Slow Motion**: Reduce playback speed (0.25x to 0.75x) for dramatic effect
- **Speed Up**: Accelerate video (1.5x to 4x) for quick recaps
- **Time-Lapse**: Extreme speed increase (8x to 20x) for long processes
- **Hyperlapse**: Stabilized time-lapse with motion smoothing
- **Frame Interpolation**: AI-generated frames for smooth slow motion
- **Speed Ramp**: Variable speed within a single clip
- **Reverse Playback**: Play video backwards
- **High FPS Output**: 60fps or 120fps output for smooth playback

## Quick Start

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Speed up this video to 2x playback speed",
    "mode": "max",
    "video_url": "https://example.com/my-video.mp4"
  }'
```

## Speed Adjustment Reference

| Effect | Speed Factor | Use Case |
|--------|--------------|----------|
| Extreme Slow-Mo | 0.25x | Sports highlights, action details |
| Slow Motion | 0.5x | Dramatic moments, product reveals |
| Slight Slow | 0.75x | Subtle emphasis |
| Normal | 1x | Original speed |
| Slight Fast | 1.5x | Skip boring parts |
| Fast Forward | 2x | Quick overview |
| Very Fast | 4x | Process summaries |
| Time-Lapse | 10x-20x | Construction, cooking, travel |

## Use Case Examples

### 1. Speed Up Video 2x

Double the playback speed for a quick recap or to fit content into a shorter duration.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Speed up this video to 2x playback speed. Keep the audio pitch corrected.",
    "mode": "max",
    "video_url": "https://example.com/tutorial-video.mp4"
  }'
```

### 2. Slow Motion 0.5x

Create a half-speed slow motion effect for emphasis and drama.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 0.5x slow motion version of this video. Apply frame interpolation for smooth playback without stuttering.",
    "mode": "max",
    "video_url": "https://example.com/action-clip.mp4"
  }'
```

### 3. Time-Lapse Effect (10x Speed)

Transform regular footage into a time-lapse for showing long processes quickly.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 10x time-lapse effect from this video. This is footage of a sunset, compress the 30 minute recording into a 3 minute clip. Maintain smooth motion and remove audio.",
    "mode": "max",
    "video_url": "https://example.com/sunset-footage.mp4"
  }'
```

### 4. Smooth Slow Motion with Frame Interpolation

Use AI frame interpolation to create buttery-smooth slow motion from standard 30fps footage.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a smooth 0.25x slow motion video using AI frame interpolation. The source is 30fps footage - interpolate to 120fps first, then slow down to 0.25x for silky smooth playback. This is a skateboard trick that needs to look cinematic.",
    "mode": "max",
    "video_url": "https://example.com/skateboard-trick.mp4"
  }'
```

### 5. Speed Ramp (Variable Speed)

Create dynamic speed changes within a single clip - start slow, speed up, then slow down again.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Apply a speed ramp effect to this video: Start at 0.5x slow motion for the first 2 seconds (the jump), then ramp up to 2x speed for the middle section (the landing and walk), then back to 0.5x for the final trick. Create smooth transitions between speed changes.",
    "mode": "max",
    "video_url": "https://example.com/parkour-clip.mp4"
  }'
```

### 6. Reverse Video

Play the video backwards for creative effects or reveals.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Reverse this video so it plays backwards. This is a glass breaking - I want to show it reassembling. Keep the audio reversed as well for the effect.",
    "mode": "max",
    "video_url": "https://example.com/glass-breaking.mp4"
  }'
```

### 7. Hyperlapse Effect

Create a stabilized, smooth hyperlapse from handheld footage with speed increase.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a hyperlapse effect from this walking footage. Speed up to 8x while applying stabilization and motion smoothing. This is a walk through a city street - make it look like a professional hyperlapse with smooth camera movement.",
    "mode": "max",
    "video_url": "https://example.com/city-walk.mp4"
  }'
```

### 8. Slow Motion Sports Highlight

Create dramatic slow motion from sports footage with emphasis on key moments.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a slow motion sports highlight from this basketball footage. Apply 0.3x slow motion with frame interpolation for smooth playback. Focus on making the dunk look dramatic and cinematic. Output at 60fps for smooth viewing.",
    "mode": "max",
    "video_url": "https://example.com/basketball-dunk.mp4"
  }'
```

### 9. Fast Forward Boring Parts

Speed up specific sections while keeping others at normal speed.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "This is a cooking tutorial video. Speed up the waiting/cooking parts to 4x (like when the food is just sitting in the oven or boiling) but keep the active cooking instruction parts at normal 1x speed. Make the speed transitions smooth.",
    "mode": "max",
    "video_url": "https://example.com/cooking-tutorial.mp4"
  }'
```

### 10. Cinematic Slow-Mo with 60fps Output

Create film-quality slow motion with high frame rate output for professional results.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a cinematic slow motion video at 0.4x speed. Use AI frame interpolation to generate smooth intermediate frames and output at 60fps. This is a fashion model walking on a runway - add slight motion blur for a filmic look. The result should look like it was shot with a high-speed camera.",
    "mode": "max",
    "video_url": "https://example.com/runway-walk.mp4"
  }'
```

## Multi-Turn Speed Adjustment Workflow

Use `session_id` to iterate on speed adjustments:

```bash
# Initial speed adjustment
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a slow motion version of this video at 0.5x speed",
    "session_id": "speed-project-001",
    "video_url": "https://example.com/action-scene.mp4"
  }'

# Request further adjustment
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "The slow motion looks good but I want it even slower - make it 0.25x with frame interpolation for smoothness",
    "session_id": "speed-project-001"
  }'

# Add additional effect
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Now add a speed ramp at the end - gradually speed up from 0.25x to 2x over the last 3 seconds",
    "session_id": "speed-project-001"
  }'
```

## Best Practices

### Slow Motion
- **Source Frame Rate**: Higher source FPS (60fps, 120fps) produces better slow motion
- **Frame Interpolation**: Use AI interpolation for smooth results from 30fps sources
- **Output FPS**: Request 60fps output for smooth playback on modern displays
- **Avoid Extreme Slow-Mo**: Going below 0.25x may produce artifacts

### Speed Up / Time-Lapse
- **Audio Handling**: Remove audio for extreme speed-ups (4x+) or use pitch correction
- **Motion Blur**: Add slight motion blur for smoother fast-forward appearance
- **Stabilization**: Apply stabilization for handheld footage before speed-up

### Speed Ramps
- **Smooth Transitions**: Request gradual speed changes over 0.5-2 seconds
- **Mark Key Moments**: Describe which parts should be slow vs fast
- **Audio Sync**: Consider how speed changes affect audio/music sync

### Quality Tips
- **Mode Selection**: Use `max` for final exports, `eco` for previews
- **Resolution**: Higher resolution sources produce better results
- **Compression**: Request high bitrate output for quality retention

## Mode Selection

| Mode | Best For | Speed | Quality |
|------|----------|-------|---------|
| `max` | Final exports, client deliverables, portfolio work | Slower | Highest |
| `eco` | Quick previews, testing speed values, drafts | Faster | Good |

## Prompt Tips for Speed Adjustment

When requesting speed adjustments, include these details:

1. **Speed Factor**: Specify exact multiplier (0.5x, 2x, 10x)
2. **Frame Interpolation**: Request if needed for smooth slow motion
3. **Output FPS**: Specify desired frame rate (30fps, 60fps, 120fps)
4. **Audio Handling**: Keep, remove, pitch correct, or reverse
5. **Transitions**: For speed ramps, describe how transitions should feel
6. **Quality Priority**: Mention if smoothness or detail is more important

### Example Prompt Structure

```
"[Speed effect] this video to [speed factor].
[Frame interpolation requirement].
Output at [fps] for [use case].
[Audio handling instruction].
[Additional quality requirements]."
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | Insufficient balance | Top up at eachlabs.ai |
| Timeout | Long video processing | Set client timeout to minimum 10 minutes |
| Choppy slow motion | No frame interpolation | Request AI frame interpolation |
| Audio pitch issues | Speed change without correction | Request pitch correction or remove audio |

## Technical Notes

- **Client Timeout**: Set HTTP client timeout to minimum 10 minutes for video processing
- **Video Length**: Longer videos take proportionally more time to process
- **Frame Interpolation**: Adds processing time but dramatically improves slow motion quality
- **Maximum Speed**: Practical range is 0.1x to 20x depending on source footage

## Related Skills

- `each-sense` - Core API documentation
- `video-stabilization` - Stabilize shaky footage
- `video-editing` - General video editing capabilities
- `video-generation` - Generate new video content
