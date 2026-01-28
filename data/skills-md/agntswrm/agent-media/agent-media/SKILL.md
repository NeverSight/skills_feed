---
name: agent-media
description: Agent-first media toolkit for image, video, and audio processing. Use when you need to resize, convert, generate images, remove backgrounds, extract audio, transcribe speech, or generate videos. All commands return deterministic JSON output.
---

# Agent Media

Agent Media is an agent-first media toolkit that provides CLI-accessible commands for image, video, and audio processing. All commands produce deterministic, machine-readable JSON output.

## Available Commands

### Image Commands
- `agent-media image resize` - Resize an image
- `agent-media image convert` - Convert image format
- `agent-media image remove-background` - Remove image background
- `agent-media image generate` - Generate image from text

### Audio Commands
- `agent-media audio extract` - Extract audio from video
- `agent-media audio transcribe` - Transcribe audio to text

### Video Commands
- `agent-media video generate` - Generate video from text or image

## Output Format

All commands return JSON to stdout:

```json
{
  "ok": true,
  "media_type": "image",
  "action": "resize",
  "provider": "local",
  "output_path": "output_123.webp",
  "mime": "image/webp",
  "bytes": 12345
}
```

On error:

```json
{
  "ok": false,
  "error": {
    "code": "INVALID_INPUT",
    "message": "input file not found"
  }
}
```

## Providers

- **local** - Default provider using Sharp (resize, convert) and Transformers.js (remove-background, transcribe)
- **fal** - fal.ai provider (generate, edit, remove-background, transcribe, video)
- **replicate** - Replicate API (generate, edit, remove-background, transcribe, video)
- **runpod** - Runpod API (generate, edit)
- **ai-gateway** - Vercel AI Gateway (generate, edit)

## Provider Selection

1. Explicit: `--provider <name>`
2. Auto-detect from environment variables
3. Fallback to local provider

## Environment Variables

- `AGENT_MEDIA_DIR` - Custom output directory
- `FAL_API_KEY` - Enable fal provider
- `REPLICATE_API_TOKEN` - Enable replicate provider
- `RUNPOD_API_KEY` - Enable runpod provider
- `AI_GATEWAY_API_KEY` - Enable ai-gateway provider
