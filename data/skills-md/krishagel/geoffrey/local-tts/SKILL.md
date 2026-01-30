---
name: local-tts
version: 1.0.0
description: Local text-to-speech using MLX and Kokoro model
triggers:
  - local-tts
  - local tts
  - generate audio locally
  - kokoro tts
dependencies:
  - mlx-audio (via uv --with)
  - pydub (via uv --with)
---

# Local TTS Skill

Generate high-quality speech audio locally using Apple Silicon MLX acceleration and the Kokoro-82M model. No API keys or recurring costs.

## Quick Start

```bash
# Generate MP3 from text
uv run --with mlx-audio --with pydub skills/local-tts/scripts/generate_audio.py \
    --text "Hello, this is a test." \
    --output ~/Desktop/test.mp3

# Generate from file
uv run --with mlx-audio --with pydub skills/local-tts/scripts/generate_audio.py \
    --file /tmp/script.txt \
    --voice af_heart \
    --output ~/Desktop/podcast.mp3

# List available voices
uv run --with mlx-audio skills/local-tts/scripts/list_voices.py
```

## Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `--text` | One of text/file | - | Text to convert |
| `--file` | One of text/file | - | Path to text file |
| `--voice` | No | `af_heart` | Voice preset |
| `--output` | Yes | - | Output file path (.mp3, .wav) |
| `--model` | No | `Kokoro-82M-bf16` | Model to use |
| `--list-voices` | No | - | Show available voices |

## Voice Presets

### American English Female (prefix: af_)
- `af_heart` - Warm, friendly **(default)**
- `af_bella` - Soft, calm
- `af_nova` - Clear, professional
- `af_river` - Clear, confident
- `af_sarah` - Soft, expressive

### American English Male (prefix: am_)
- `am_adam` - Clear, professional
- `am_echo` - Deep, smooth
- `am_liam` - Articulate, conversational
- `am_michael` - Soft, measured

### British English (prefix: bf_, bm_)
- `bf_emma` - Clear, refined female
- `bm_daniel` - Clear, professional male
- `bm_george` - Distinguished male

See `references/voices.md` for full list.

## Output Format

```json
{
  "success": true,
  "file": "/Users/hagelk/Desktop/podcast.mp3",
  "voice": "af_heart",
  "model": "Kokoro-82M-bf16",
  "characters": 9824,
  "chunks": 20,
  "duration_seconds": 612.5,
  "generation_time": 45.2
}
```

## Performance

| Hardware | Speed | Notes |
|----------|-------|-------|
| M3 Pro 36GB | ~3-4x realtime | First run slower (model loading) |
| M1/M2 Mac Mini 8GB | ~1.5x realtime | Works well for briefings |
| M1/M2 Mac Mini 16GB | ~2x realtime | Comfortable headroom |

## Technical Details

- **Model**: Kokoro-82M-bf16 (~200MB download on first run)
- **Sample rate**: 24kHz mono
- **Chunking**: Text split at ~400 chars per chunk for quality
- **Concatenation**: Chunks joined seamlessly via pydub
- **Formats**: MP3, WAV, M4A, OGG

## Important Notes

1. **MUST use `--with` flags** - Do not use PEP 723 inline deps. mlx-audio requires uv's cached environment.

2. **First run is slower** - Model downloads ~200MB and espeak dependencies initialize.

3. **Model cached at**: `~/.cache/huggingface/hub/models--mlx-community--Kokoro-82M-bf16/`

## Integration with Morning Briefing

The morning-briefing skill uses this for podcast generation:

```bash
uv run --with mlx-audio --with pydub skills/local-tts/scripts/generate_audio.py \
    --file /tmp/morning_briefing_podcast.txt \
    --voice af_heart \
    --output ~/Desktop/morning_briefing.mp3
```
