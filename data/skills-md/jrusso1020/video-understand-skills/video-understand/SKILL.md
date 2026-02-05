---
name: video-understand
description: |
  Video understanding and transcription with intelligent multi-provider fallback. Use when: (1) Transcribing video or audio content, (2) Understanding video content including visual elements and scenes, (3) Analyzing YouTube videos by URL, (4) Extracting information from local video files, (5) Getting timestamps, summaries, or answering questions about video content. Automatically selects the best available provider based on configured API keys - prefers full video understanding (Gemini/OpenRouter) over ASR-only providers. Supports model selection per provider.
---

# Video Understanding

Multi-provider video understanding with automatic fallback and model selection.

## Quick Start

```bash
# Check available providers
python3 scripts/check_providers.py

# Process a video (auto-selects best provider)
python3 scripts/process_video.py "https://youtube.com/watch?v=..."
python3 scripts/process_video.py /path/to/video.mp4

# Custom prompt
python3 scripts/process_video.py video.mp4 -p "List all products shown with timestamps"

# Use specific provider/model
python3 scripts/process_video.py video.mp4 --provider openrouter -m google/gemini-3-pro-preview

# List available models
python3 scripts/process_video.py --list-models
```

## Provider Hierarchy

Automatically selects the best available provider:

| Priority | Provider | Capability | Env Var | Default Model |
|----------|----------|------------|---------|---------------|
| 1 | Gemini | Full video | `GEMINI_API_KEY` | gemini-3-flash-preview |
| 2 | Vertex AI | Full video | `GOOGLE_APPLICATION_CREDENTIALS` | gemini-3-flash-preview |
| 3 | OpenRouter | Full video | `OPENROUTER_API_KEY` | google/gemini-3-flash-preview |
| 4 | OpenAI | ASR only | `OPENAI_API_KEY` | whisper-1 |
| 5 | AssemblyAI | ASR + analysis | `ASSEMBLYAI_API_KEY` | best |
| 6 | Deepgram | ASR | `DEEPGRAM_API_KEY` | nova-2 |
| 7 | Groq | ASR (fast) | `GROQ_API_KEY` | whisper-large-v3-turbo |
| 8 | Local Whisper | ASR (offline) | None | base |

**Full video** = visual + audio analysis. **ASR** = audio transcription only.

## CLI Options

```
python3 scripts/process_video.py [OPTIONS] SOURCE

Arguments:
  SOURCE              YouTube URL, video URL, or local file path

Options:
  -p, --prompt TEXT   Custom prompt for video understanding
  --provider NAME     Force specific provider
  -m, --model NAME    Force specific model
  --asr-only          Force ASR-only mode (skip visual analysis)
  -o, --output FILE   Write JSON to file instead of stdout
  -q, --quiet         Suppress progress messages
  --list-models       Show available models per provider
  --list-providers    Show available providers as JSON
```

## Model Selection

Each provider supports multiple models. Use `--list-models` to see options:

```bash
python3 scripts/process_video.py --list-models
```

**OpenRouter models:**
- `google/gemini-3-flash-preview` (default) - Fast, free tier
- `google/gemini-3-pro-preview` - Higher quality

**Gemini models:**
- `gemini-3-flash-preview` (default) - Latest, fast
- `gemini-3-pro-preview` - Highest quality
- `gemini-2.5-flash` - Stable production fallback

**Local Whisper models:**
- `tiny`, `base` (default), `small`, `medium`, `large`, `large-v3`

## Quick Reference

| Task | Reference |
|------|-----------|
| **Setup & API keys** | [setup-guide.md](references/setup-guide.md) |
| Use Gemini for video | [gemini.md](references/gemini.md) |
| Use OpenRouter | [openrouter.md](references/openrouter.md) |
| ASR providers | [asr-providers.md](references/asr-providers.md) |
| Output JSON schema | [output-format.md](references/output-format.md) |
| Video sources & downloading | [video-sources.md](references/video-sources.md) |

## Verify Setup

```bash
python3 scripts/setup.py  # Check dependencies and API keys
```

## Output Format

All providers return consistent JSON:

```json
{
  "source": {
    "type": "youtube|url|local",
    "path": "...",
    "duration_seconds": 120.5,
    "size_mb": 15.2
  },
  "provider": "openrouter",
  "model": "google/gemini-3-flash-preview",
  "capability": "full_video",
  "response": "...",
  "transcript": [{"start": 0.0, "end": 2.5, "text": "..."}],
  "text": "Full transcript..."
}
```

## Features

- **Automatic provider selection** based on available API keys
- **Model selection** per provider with sensible defaults
- **Robust path handling** for macOS special characters and unicode
- **Progress output** (use `-q` for quiet mode)
- **File size warnings** for API limits
- **Auto-conversion** of video formats when needed
- **YouTube URL support** (direct or via download)

## Requirements

**For full video understanding:**
```bash
pip install google-generativeai  # Gemini
pip install openai               # OpenRouter
```

**For ASR fallback:**
```bash
brew install yt-dlp ffmpeg       # Video tools
pip install openai               # OpenAI Whisper
pip install groq                 # Groq Whisper
pip install assemblyai           # AssemblyAI
pip install deepgram-sdk         # Deepgram
pip install openai-whisper       # Local Whisper
```
