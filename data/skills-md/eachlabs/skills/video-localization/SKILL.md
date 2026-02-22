---
name: video-localization
description: Localize and dub videos using each::sense AI. Translate audio, generate subtitles, clone voices, and create lip-synced multilingual versions of your video content.
metadata:
  author: eachlabs
  version: "1.0"
---

# Video Localization

Localize and dub videos into multiple languages using each::sense. This skill handles audio translation, voice cloning, lip synchronization, and subtitle generation for global content distribution.


## Features

- **AI Dubbing**: Translate and dub video audio into any language
- **Voice Cloning**: Preserve speaker identity across languages
- **Lip Sync**: Synchronize lip movements with translated audio
- **Subtitle Generation**: Auto-generate subtitles in source or target languages
- **Multi-Language Versions**: Create localized versions for multiple markets
- **Marketing Localization**: Adapt ad content for regional audiences
- **E-Learning Translation**: Translate training and educational content
- **YouTube Localization**: Prepare videos for international audiences

## Quick Start

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Dub this English video into Spanish with lip sync",
    "mode": "max",
    "video_urls": ["https://example.com/my-video.mp4"]
  }'
```

## Supported Languages

| Language | Code | Dubbing | Subtitles | Voice Cloning |
|----------|------|---------|-----------|---------------|
| English | en | Yes | Yes | Yes |
| Spanish | es | Yes | Yes | Yes |
| French | fr | Yes | Yes | Yes |
| German | de | Yes | Yes | Yes |
| Italian | it | Yes | Yes | Yes |
| Portuguese | pt | Yes | Yes | Yes |
| Chinese | zh | Yes | Yes | Yes |
| Japanese | ja | Yes | Yes | Yes |
| Korean | ko | Yes | Yes | Yes |
| Hindi | hi | Yes | Yes | Yes |
| Arabic | ar | Yes | Yes | Yes |

## Use Case Examples

### 1. English to Spanish Dubbing

Basic dubbing with natural voice synthesis.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Translate and dub this English video into Spanish. Use a natural-sounding voice that matches the original speaker tone and energy.",
    "mode": "max",
    "video_urls": ["https://example.com/english-video.mp4"]
  }'
```

### 2. Video Translation with Lip Sync

Full localization with lip movement synchronization for professional results.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Translate this video from English to French with full lip sync. The lip movements should match the French audio perfectly. Maintain the original background music and sound effects.",
    "mode": "max",
    "video_urls": ["https://example.com/presentation-video.mp4"]
  }'
```

### 3. Subtitle Generation

Generate accurate subtitles in source or translated languages.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate subtitles for this video. First transcribe the English audio, then create Spanish subtitles. Output both SRT files and a video with burned-in Spanish subtitles.",
    "mode": "max",
    "video_urls": ["https://example.com/interview.mp4"]
  }'
```

### 4. Multi-Language Video Versions

Create localized versions for multiple markets in a single workflow.

```bash
# Start multi-language localization session
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "I need to localize this product video into Spanish, French, and German. Start with Spanish dubbing with lip sync.",
    "mode": "max",
    "session_id": "localization-project-001",
    "video_urls": ["https://example.com/product-demo.mp4"]
  }'

# Continue with French version
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Now create the French version with the same quality settings.",
    "mode": "max",
    "session_id": "localization-project-001"
  }'

# Continue with German version
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Finally, create the German version.",
    "mode": "max",
    "session_id": "localization-project-001"
  }'
```

### 5. Voice Cloning for Dubbing

Preserve the original speaker's voice characteristics in the dubbed version.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Dub this video from English to Japanese using voice cloning. Clone the original speaker voice so they sound like themselves speaking Japanese. Maintain their unique voice characteristics, tone, and speaking style.",
    "mode": "max",
    "video_urls": ["https://example.com/ceo-message.mp4"]
  }'
```

### 6. Marketing Video Localization

Adapt marketing content for regional audiences with cultural considerations.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Localize this marketing video for the Latin American market. Translate to Spanish with a neutral Latin American accent, not Spain Spanish. Apply lip sync and ensure the messaging resonates with the target audience. Keep the energy and excitement of the original.",
    "mode": "max",
    "video_urls": ["https://example.com/brand-ad.mp4"]
  }'
```

### 7. Training Video Translation

Translate corporate training and educational content.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Translate this employee training video from English to Mandarin Chinese. Use clear, professional narration suitable for corporate training. Include both dubbed audio and Chinese subtitles for accessibility. Technical terms should be accurately translated.",
    "mode": "max",
    "video_urls": ["https://example.com/onboarding-training.mp4"]
  }'
```

### 8. YouTube Video Localization

Prepare content for international YouTube audiences.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Localize this YouTube video for Portuguese-speaking audiences (Brazilian Portuguese). Dub the narration with lip sync, generate Portuguese subtitles in SRT format, and create a localized thumbnail with Portuguese text overlay.",
    "mode": "max",
    "video_urls": ["https://example.com/youtube-tutorial.mp4"]
  }'
```

### 9. Ad Creative Localization

Adapt advertising content for different regional markets.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Localize this 30-second ad for the German market. Translate and dub to German with lip sync. Ensure the call-to-action is culturally appropriate. Keep the same pacing and emotional impact as the original English version.",
    "mode": "max",
    "video_urls": ["https://example.com/product-ad-30s.mp4"]
  }'
```

### 10. E-Learning Content Translation

Translate educational courses and learning materials.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Translate this e-learning module from English to Korean. The instructor should be dubbed with voice cloning to maintain authenticity. Generate Korean subtitles and ensure all on-screen text references are noted for manual localization. Educational terminology must be accurately translated.",
    "mode": "max",
    "video_urls": ["https://example.com/course-module-1.mp4"]
  }'
```

## Best Practices

### Video Quality
- **Source Quality**: Use high-quality source videos (1080p or higher recommended)
- **Clear Audio**: Ensure source audio is clear with minimal background noise
- **Single Speaker**: Best results with single-speaker content; multi-speaker requires more processing

### Dubbing Tips
- **Natural Pacing**: AI adjusts speech rate to match lip movements
- **Preserve Emotion**: Original emotional tone is maintained in translations
- **Background Audio**: Original music and sound effects are preserved

### Lip Sync Optimization
- **Face Visibility**: Ensure speaker's face is clearly visible
- **Consistent Lighting**: Well-lit faces produce better lip sync results
- **Front-Facing**: Best results with front-facing or slight angle shots

### Subtitle Best Practices
- **Reading Speed**: Subtitles are timed for comfortable reading
- **Line Breaks**: Proper segmentation for readability
- **Timing Sync**: Accurate sync with audio and scene changes

## Mode Selection

Choose the appropriate mode based on your needs:

| Mode | Best For | Speed | Quality |
|------|----------|-------|---------|
| `max` | Final production, client deliverables, broadcast | Slower | Highest quality lip sync and voice |
| `eco` | Drafts, internal review, quick previews | Faster | Good quality, faster turnaround |

**Recommendation**: Use `eco` mode for initial reviews and `max` mode for final deliverables.

## Multi-Turn Localization Workflow

Use `session_id` to iterate on localization projects:

```bash
# Initial localization request
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Dub this video into Spanish with lip sync",
    "session_id": "dubbing-project-xyz",
    "video_urls": ["https://example.com/source-video.mp4"]
  }'

# Request adjustments based on review
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "The voice sounds too formal. Can you make it more conversational and energetic?",
    "session_id": "dubbing-project-xyz"
  }'

# Add subtitles to the approved version
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Add Spanish subtitles to this dubbed version",
    "session_id": "dubbing-project-xyz"
  }'
```

## Batch Localization

Process multiple videos or languages efficiently:

```bash
# Use eco mode for batch processing drafts
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create Spanish dubbed versions of these 3 marketing videos with subtitles",
    "mode": "eco",
    "video_urls": [
      "https://example.com/video1.mp4",
      "https://example.com/video2.mp4",
      "https://example.com/video3.mp4"
    ]
  }'
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | Insufficient balance | Top up at eachlabs.ai |
| `Video too long` | Source video exceeds limits | Split into shorter segments |
| `Audio not detected` | No speech in video | Ensure video contains speech audio |
| `Face not detected` | No visible face for lip sync | Use videos with visible speakers |
| Timeout | Complex generation | Set client timeout to minimum 10 minutes |

## Technical Notes

- **Client Timeout**: Set HTTP client timeout to minimum 10 minutes for video processing
- **Video Length**: Optimal length is under 10 minutes per segment for best results
- **Output Format**: Generated videos are MP4 with H.264 encoding
- **Subtitle Format**: SRT files are provided for subtitle outputs

## Related Skills

- `each-sense` - Core API documentation
- `video-generation` - Create original video content
- `video-edit` - Edit and enhance videos
- `voice-audio` - Voice synthesis and audio generation
