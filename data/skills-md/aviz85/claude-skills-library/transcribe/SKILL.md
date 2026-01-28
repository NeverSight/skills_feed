---
name: transcribe
description: "Transcribe audio/video to SRT subtitles using ElevenLabs Scribe v2. Use for: transcription, subtitles, captions, SRT generation."
---

# Transcribe

Generate SRT subtitle files from audio/video using ElevenLabs Scribe v2.

## Quick Start

```bash
cd ~/.claude/skills/transcribe/scripts

# Basic transcription (auto-detect language)
npx ts-node transcribe.ts -i /path/to/video.mp4 -o /path/to/output.srt

# Specify language
npx ts-node transcribe.ts -i /path/to/video.mp4 -o /path/to/output.srt -l en

# Custom subtitle length (max words per entry)
npx ts-node transcribe.ts -i /path/to/video.mp4 -o /path/to/output.srt --max-words 6

# Custom max duration per subtitle
npx ts-node transcribe.ts -i /path/to/video.mp4 -o /path/to/output.srt --max-duration 4.0
```

## Options

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--input` | `-i` | (required) | Input audio/video file |
| `--output` | `-o` | (required) | Output SRT file path |
| `--language` | `-l` | auto | Language code (en, he, ar, etc.) |
| `--max-words` | | 5 | Max words per subtitle entry |
| `--max-duration` | | 3.0 | Max seconds per subtitle entry |
| `--max-chars` | | 70 | Max characters per subtitle entry |
| `--timing-offset` | | 0.25 | Timing offset in seconds |
| `--json` | | false | Also output raw transcript JSON |

## Language Codes

- `en` - English
- `he` - Hebrew
- `ar` - Arabic
- `es` - Spanish
- `fr` - French
- `de` - German
- `ru` - Russian
- `zh` - Chinese
- `ja` - Japanese
- (or omit for auto-detection)

## Output

The script generates:
1. `.srt` file - Standard subtitle file
2. `.json` file (optional) - Raw transcript with word-level timestamps

## Environment

API key stored in `scripts/.env`:
```
ELEVENLABS_API_KEY=your_key_here
```
