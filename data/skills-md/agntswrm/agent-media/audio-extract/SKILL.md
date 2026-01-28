---
name: audio-extract
description: Extracts audio track from a video file. Use when you need to get audio from video, prepare audio for transcription, or separate audio from video content. Runs locally with no API key required.
---

# Audio Extract

Extracts the audio track from a video file. This is a local operation using the bundled ffmpeg binary - no API keys or external services required.

## Command

```bash
agent-media audio extract --in <path> [options]
```

## Inputs

| Option | Required | Description |
|--------|----------|-------------|
| `--in` | Yes | Input video file path or URL (supports mp4, webm, mkv, avi, mov) |
| `--format` | No | Output audio format: `mp3` (default) or `wav` |
| `--out` | No | Output path, filename or directory (default: ./) |

## Output

Returns a JSON object with the extracted audio file:

```json
{
  "ok": true,
  "media_type": "audio",
  "action": "extract",
  "provider": "local",
  "output_path": "extracted_123_abc.mp3",
  "mime": "audio/mpeg",
  "bytes": 24779
}
```

## Examples

Extract audio as MP3 (default):
```bash
agent-media audio extract --in video.mp4
```

Extract audio as WAV:
```bash
agent-media audio extract --in video.mp4 --format wav
```

Custom output directory:
```bash
agent-media audio extract --in video.mp4 --out ./audio-files
```

## Use Case: Video Transcription Workflow

Since transcription services work best with audio files (smaller uploads, faster processing), use this workflow:

```bash
# Step 1: Extract audio from video (local, instant)
agent-media audio extract --in interview.mp4 --format mp3
# Output: extracted_xxx.mp3

# Step 2: Transcribe the audio (cloud API)
agent-media audio transcribe --in extracted_xxx.mp3 --provider fal
```

## Provider

This action uses the **local** provider with bundled ffmpeg (via `ffmpeg-static`). No API keys required.
