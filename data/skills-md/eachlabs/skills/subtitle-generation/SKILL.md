---
name: subtitle-generation
description: Generate subtitles and captions for videos using each::sense AI. Create auto-generated subtitles, multi-language captions, animated TikTok-style text, SRT/VTT exports, speaker diarization, and burned-in subtitles.
metadata:
  author: eachlabs
  version: "1.0"
---

# Subtitle Generation

Generate professional subtitles and captions for videos using each::sense. This skill creates accurate transcriptions, multi-language subtitles, animated captions, and various export formats optimized for social media, video production, and accessibility.

## Features

- **Auto-Generated Subtitles**: Automatic speech-to-text transcription with accurate timing
- **Multi-Language Generation**: Generate subtitles in multiple languages from audio
- **Animated Captions**: TikTok/Instagram-style animated word-by-word captions
- **SRT/VTT Export**: Standard subtitle formats for editing and distribution
- **Speaker Diarization**: Identify and label different speakers in conversations
- **Subtitle Translation**: Translate existing subtitles to other languages
- **Burned-In Subtitles**: Render subtitles directly into video (hardcoded)
- **Karaoke Style**: Word-by-word highlighting for music and lyric videos
- **Timing Adjustment**: Fine-tune subtitle timing and synchronization
- **Batch Processing**: Generate subtitles for multiple videos at once

## Quick Start

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate subtitles for this video with accurate timestamps",
    "mode": "max",
    "file_urls": ["https://example.com/my-video.mp4"]
  }'
```

## Subtitle Formats & Outputs

| Format | Extension | Use Case |
|--------|-----------|----------|
| SRT | .srt | Universal, most video players and editors |
| VTT | .vtt | Web video, HTML5 players, YouTube |
| Burned-In | .mp4 | Social media, no player support needed |
| JSON | .json | Custom applications, programmatic access |
| ASS/SSA | .ass | Advanced styling, anime subtitles |

## Use Case Examples

### 1. Auto-Generate Subtitles from Video

Automatically transcribe speech from a video file with accurate word-level timestamps.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Transcribe this video and generate subtitles with accurate timestamps. Output as SRT format. The video contains English speech.",
    "mode": "max",
    "file_urls": ["https://example.com/interview-video.mp4"]
  }'
```

### 2. Multi-Language Subtitle Generation

Generate subtitles in multiple languages directly from the audio.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate subtitles for this video in English, Spanish, and French. Provide separate SRT files for each language. The original audio is in English.",
    "mode": "max",
    "file_urls": ["https://example.com/product-demo.mp4"]
  }'
```

### 3. Animated/Styled Captions (TikTok Style)

Create eye-catching animated captions with word-by-word highlighting, popular on TikTok and Instagram Reels.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Add TikTok-style animated captions to this video. Use bold white text with black outline, word-by-word pop animation, centered at the bottom third of the screen. Make it trendy and engaging.",
    "mode": "max",
    "file_urls": ["https://example.com/short-form-content.mp4"]
  }'
```

### 4. SRT/VTT Export

Generate clean subtitle files in standard formats for use in video editors or streaming platforms.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Transcribe this video and export subtitles in both SRT and VTT formats. Ensure proper line breaks (max 42 characters per line, 2 lines max). Include timestamps accurate to milliseconds.",
    "mode": "max",
    "file_urls": ["https://example.com/documentary.mp4"]
  }'
```

### 5. Speaker Diarization (Identify Speakers)

Generate subtitles that identify and label different speakers in conversations, interviews, or podcasts.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate subtitles for this podcast with speaker diarization. There are 2 speakers - identify them as Speaker 1 and Speaker 2 (or Host and Guest if you can determine roles). Format each line with the speaker label.",
    "mode": "max",
    "file_urls": ["https://example.com/podcast-episode.mp4"]
  }'
```

### 6. Subtitle Translation

Translate existing subtitles from one language to another while preserving timing.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Translate these English subtitles to Japanese. Preserve the original timing and format. Ensure natural Japanese phrasing rather than literal translation.",
    "mode": "max",
    "file_urls": ["https://example.com/original-subtitles.srt"]
  }'
```

### 7. Burned-In Subtitles

Render subtitles directly into the video file (hardcoded/embedded) so they appear without needing player support.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate subtitles for this video and burn them directly into the video. Use white text with black background box, Arial font, positioned at bottom center. Output a new video file with embedded subtitles.",
    "mode": "max",
    "file_urls": ["https://example.com/social-media-clip.mp4"]
  }'
```

### 8. Word-by-Word Karaoke Style

Create karaoke-style subtitles with word-by-word highlighting, perfect for music videos and lyric content.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create karaoke-style subtitles for this music video. Display lyrics with word-by-word highlighting as they are sung. Use a gradient color change effect (from white to yellow) for the currently sung word. Center the text on screen.",
    "mode": "max",
    "file_urls": ["https://example.com/music-video.mp4"]
  }'
```

### 9. Subtitle Timing Adjustment

Fine-tune subtitle timing for better synchronization with audio.

```bash
# First, upload video and generate initial subtitles
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate subtitles for this video",
    "mode": "max",
    "session_id": "subtitle-timing-project",
    "file_urls": ["https://example.com/video-with-delay.mp4"]
  }'

# Then adjust timing in the same session
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "The subtitles are appearing 500 milliseconds too early. Shift all subtitle timings forward by 500ms and regenerate the SRT file.",
    "session_id": "subtitle-timing-project"
  }'
```

### 10. Batch Subtitle Generation

Generate subtitles for multiple videos in a single workflow.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate English subtitles for all these videos. Output SRT files for each. Use consistent formatting across all videos: max 2 lines, 42 characters per line, minimum 1 second display time per subtitle.",
    "mode": "max",
    "file_urls": [
      "https://example.com/episode-01.mp4",
      "https://example.com/episode-02.mp4",
      "https://example.com/episode-03.mp4"
    ]
  }'
```

## Best Practices

### Transcription Quality
- **Clear Audio**: Best results with clear speech and minimal background noise
- **Language Hint**: Specify the source language for better accuracy
- **Speaker Count**: Mention number of speakers for better diarization
- **Context**: Provide context about the content (technical terms, names) for accuracy

### Subtitle Formatting
- **Line Length**: Keep lines under 42 characters for readability
- **Duration**: Each subtitle should display for 1-7 seconds
- **Lines Per Subtitle**: Maximum 2 lines per subtitle block
- **Reading Speed**: Target 150-180 words per minute for comfortable reading

### Animated Captions
- **Font Choice**: Bold, sans-serif fonts work best for short-form content
- **Contrast**: Use outlines or shadows for visibility on any background
- **Position**: Keep safe zones clear for platform UI elements
- **Animation**: Subtle animations are more readable than dramatic effects

### Translation
- **Cultural Adaptation**: Request localization, not just translation
- **Timing Flexibility**: Some languages need more time to read
- **Character Limits**: CJK languages often need fewer characters per line

## Prompt Tips for Subtitle Generation

When requesting subtitles, include these details in your prompt:

1. **Source Language**: What language is spoken in the video?
2. **Target Format**: SRT, VTT, burned-in, or animated?
3. **Style Requirements**: Font, color, position, animation
4. **Speaker Info**: Number of speakers, roles if known
5. **Special Terms**: Technical vocabulary, names, brands
6. **Output Languages**: Single language or multiple translations

### Example Prompt Structure

```
"Generate [format] subtitles for this video.
Source language: [language].
[Number] speakers: [roles if known].
Style: [font, color, position requirements].
Special terms to recognize: [names, technical words].
Additional requirements: [line length, timing, etc.]"
```

## Mode Selection

Ask your users before generating:

**"Do you want fast & cheap, or high quality?"**

| Mode | Best For | Speed | Quality |
|------|----------|-------|---------|
| `max` | Final subtitles, professional content, accuracy-critical | Slower | Highest |
| `eco` | Quick drafts, review copies, bulk processing | Faster | Good |

## Multi-Turn Subtitle Refinement

Use `session_id` to iterate on subtitle generation:

```bash
# Initial subtitle generation
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate subtitles for this video with speaker identification",
    "session_id": "subtitle-project-001",
    "file_urls": ["https://example.com/interview.mp4"]
  }'

# Refine based on feedback
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Change Speaker 1 label to John and Speaker 2 to Sarah. Also fix the spelling of TensorFlow wherever it appears.",
    "session_id": "subtitle-project-001"
  }'

# Add styling and export
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Now create a burned-in version with the corrected subtitles. Use yellow text for John and cyan for Sarah.",
    "session_id": "subtitle-project-001"
  }'
```

## Language Support

each::sense supports subtitle generation in 50+ languages including:

| Language | Code | Notes |
|----------|------|-------|
| English | en | US, UK, AU variants |
| Spanish | es | Latin American and European |
| French | fr | France and Canadian |
| German | de | |
| Japanese | ja | |
| Korean | ko | |
| Chinese | zh | Simplified and Traditional |
| Arabic | ar | RTL support |
| Hindi | hi | |
| Portuguese | pt | Brazilian and European |

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | Insufficient balance | Top up at eachlabs.ai |
| Transcription quality low | Poor audio quality | Provide cleaner audio source |
| Language detection failed | Mixed languages or unclear speech | Specify source language explicitly |
| Timeout | Long video or complex processing | Set client timeout to minimum 10 minutes |

## Client Configuration

**Important**: Subtitle generation can take significant time for long videos.

- **Minimum timeout**: 10 minutes (600 seconds)
- **Recommended**: Set timeout based on video length (2-3 minutes per minute of video)
- **Streaming**: Use SSE event handling to show progress

## Related Skills

- `each-sense` - Core API documentation
- `video-generation` - Generate videos with built-in captions
- `voice-audio` - Audio processing and speech synthesis
- `video-edit` - Video editing and post-production
