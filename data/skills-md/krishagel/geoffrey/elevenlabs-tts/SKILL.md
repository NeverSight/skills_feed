---
name: elevenlabs-tts
description: Generate high-quality audio from text using Eleven Labs API. Use for podcasts, narration, voice-overs, and audio summaries.
triggers:
  - "generate audio"
  - "text to speech"
  - "create podcast"
  - "eleven labs"
  - "make audio"
  - "narrate"
  - "voice over"
allowed-tools: Read, Write, Bash
version: 1.0.0
---

# Eleven Labs Text-to-Speech

Generate high-quality audio from text using the Eleven Labs API. Ideal for podcast-style summaries, narration, and voice-overs.

## Quick Start

```bash
# Generate audio with default voice (Rachel)
uv run scripts/generate_audio.py --text "Hello, this is a test."

# Generate from a text file
uv run scripts/generate_audio.py --file report.txt --output ~/Desktop/report.mp3

# Use a specific voice
uv run scripts/generate_audio.py --text "Breaking news..." --voice Josh

# List available voices
uv run scripts/list_voices.py
```

## Scripts

### generate_audio.py

Main script for TTS generation.

**Arguments:**
| Argument | Description | Default |
|----------|-------------|---------|
| `--text` | Text content to convert | - |
| `--file` | Path to text file | - |
| `--voice` | Voice name or ID | Rachel |
| `--model` | Model ID | eleven_multilingual_v2 |
| `--output` | Output file path | ~/Desktop/audio_TIMESTAMP.mp3 |

**Features:**
- Auto-chunks text >10k characters at sentence boundaries
- Concatenates chunks into single MP3
- Returns JSON with metadata (file path, voice, model, char count, chunks)

### list_voices.py

Fetch and display available voices.

**Arguments:**
| Argument | Description | Default |
|----------|-------------|---------|
| `--all` | Show all voices (not just premade) | false |
| `--json` | Output as JSON | false |

## Curated Voices

Six voices selected for variety (see `references/voices.md` for details):

| Voice | Style | Best For |
|-------|-------|----------|
| **Rachel** | Calm, clear | Narration, podcasts (default) |
| **Bella** | Soft, gentle | Storytelling, meditation |
| **Elli** | Young, expressive | Casual content, tutorials |
| **Josh** | Deep, authoritative | News, professional content |
| **Adam** | Middle-aged, clear | Business, documentaries |
| **Antoni** | Warm, versatile | General purpose |

Use `list_voices.py` to discover additional voices.

## Models

| Model | ID | Best For | Char Limit |
|-------|-----|----------|------------|
| **Multilingual v2** | `eleven_multilingual_v2` | Long-form (default) | 10,000 |
| Flash v2.5 | `eleven_flash_v2_5` | Quick, real-time | 40,000 |
| Turbo v2.5 | `eleven_turbo_v2_5` | Balanced | 40,000 |
| Eleven v3 | `eleven_v3` | Maximum expression | 3,000 |

## Environment Setup

Requires `ELEVENLABS_API_KEY` in:
```
~/Library/Mobile Documents/com~apple~CloudDocs/Geoffrey/secrets/.env
```

## Examples

### Daily Summary Podcast
```bash
# Generate individual segments
uv run scripts/generate_audio.py --file weather.txt --voice Rachel --output ~/Desktop/weather.mp3
uv run scripts/generate_audio.py --file news.txt --voice Josh --output ~/Desktop/news.mp3
uv run scripts/generate_audio.py --file calendar.txt --voice Bella --output ~/Desktop/calendar.mp3
```

### Long Report
```bash
# Auto-chunks long text, concatenates into single file
uv run scripts/generate_audio.py --file quarterly_report.txt --model eleven_turbo_v2_5 --output report.mp3
```

### Quick Test
```bash
uv run scripts/generate_audio.py --text "Testing one two three" --voice Adam
```

## Output

Default: `~/Desktop/audio_YYYY-MM-DD_HHMMSS.mp3`

Script returns JSON:
```json
{
  "success": true,
  "file": "/Users/user/Desktop/audio_2026-01-23_143022.mp3",
  "voice": "Rachel",
  "model": "eleven_multilingual_v2",
  "characters": 1234,
  "chunks": 1
}
```

## Limitations

- Character limits vary by model (see table above)
- One voice per generation (multi-voice requires separate files)
- Output format: MP3 only
