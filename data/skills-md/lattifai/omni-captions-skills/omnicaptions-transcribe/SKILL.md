---
name: omnicaptions-transcribe
description: Use when transcribing audio/video to text with timestamps, speaker labels, and chapters. Supports YouTube URLs and local files. Produces structured markdown output.
allowed-tools: Bash(omnicaptions:*)
---

# Gemini Transcription

Transcribe audio/video using Google Gemini API with structured markdown output.

## YouTube Video Workflow

**Important**: Check for existing captions before transcribing:

```
1. Check captions: yt-dlp --list-subs "URL"
2. Has caption → Use /omnicaptions:download to get existing captions (better quality)
3. No caption → Transcribe directly with URL (don't download first!)
```

**Confirm with user**: Before transcribing, ask if they want to check for existing captions first.

## URL & Local File Support

**Gemini natively supports YouTube URLs** - no need to download, just pass the URL directly:

```bash
# YouTube URL (recommended, no download needed)
omnicaptions transcribe "https://www.youtube.com/watch?v=VIDEO_ID"

# Local files
omnicaptions transcribe video.mp4
```

**Note**: Output defaults to current directory unless user specifies `-o`.

## When to Use

- **Video URLs** - YouTube, direct video links (Gemini native support)
- Transcribing podcasts, interviews, lectures
- Need verbatim transcript with timestamps and speaker labels
- Want auto-generated chapters from content
- Mixed-language audio (code-switching preserved)

## When NOT to Use

- **Video has existing captions** - Use `/omnicaptions:download` to get existing captions first
- Need real-time streaming transcription (use Whisper)
- Audio >2 hours (Gemini upload limit)
- Want translation instead of transcription

## Quick Reference

| Method | Description |
|--------|-------------|
| `transcribe(path)` | Transcribe file or URL (sync) |
| `translate(in, out, lang)` | Translate captions |
| `write(text, path)` | Save text to file |

## Setup

```bash
pip install https://github.com/lattifai/omni-captions-skills/raw/main/packages/lattifai_captions-0.1.0.tar.gz
pip install https://github.com/lattifai/omni-captions-skills/raw/main/packages/omnicaptions-0.1.0.tar.gz
```

## API Key

Priority: `GEMINI_API_KEY` env → `.env` file → `~/.config/omnicaptions/config.json`

If not set, ask user: `Please enter your Gemini API key (get from https://aistudio.google.com/apikey):`

Then run with `-k <key>`. Key will be saved to config file automatically.

## CLI Usage

**IMPORTANT**: CLI requires subcommand (`transcribe`, `translate`, `convert`)

```bash
# Transcribe (auto-output to same directory)
omnicaptions transcribe video.mp4              # → ./video_GeminiUnd.md
omnicaptions transcribe "https://youtu.be/abc" # → ./abc_GeminiUnd.md

# Specify output file or directory
omnicaptions transcribe video.mp4 -o output/   # → output/video_GeminiUnd.md
omnicaptions transcribe video.mp4 -o my.md     # → my.md

# Options
omnicaptions transcribe -m gemini-3-pro-preview video.mp4
omnicaptions transcribe -l zh video.mp4  # Force Chinese
```

| Option | Description |
|--------|-------------|
| `-k, --api-key` | Gemini API key (auto-prompted if missing) |
| `-o, --output` | Output file or directory (default: auto) |
| `-m, --model` | Model (default: gemini-3-flash-preview) |
| `-l, --language` | Force language (zh, en, ja) |
| `-t, --translate LANG` | Translate to language (one-step) |
| `--bilingual` | Bilingual output (with -t) |
| `-v, --verbose` | Verbose output |

## Bilingual Captions (Optional)

If user requests bilingual output, add `-t <lang> --bilingual`:

```bash
omnicaptions transcribe video.mp4 -t zh --bilingual
```

For precise timing, use separate workflow: transcribe → LaiCut → translate (see Related Skills).

## Output Format

```markdown
## Table of Contents
* [00:00:00] Introduction
* [00:02:15] Main Topic

## [00:00:00] Introduction

**Host:** Welcome to the show. [00:00:01]

**Guest:** Thanks for having me. [00:00:05]

[Applause] [00:00:08]
```

Key features:
- `## [HH:MM:SS] Title` chapter headers
- `**Speaker:**` labels (auto-detected)
- `[HH:MM:SS]` timestamp at paragraph end
- `[Event]` for non-speech (laughter, music)

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| No API key error | Use `-k YOUR_KEY` or follow the prompt |
| Empty response | Check file format (mp3/mp4/wav/m4a supported) |
| Upload timeout | File too large (>2GB); split first |
| Wrong language | Use `-l en` to force language |

## Related Skills

| Skill | Use When |
|-------|----------|
| `/omnicaptions:convert` | Convert output to SRT/VTT/ASS |
| `/omnicaptions:translate` | Translate (Gemini API or Claude native) |
| `/omnicaptions:download` | Download video/audio first |

### Workflow Examples

```bash
# Basic transcription
omnicaptions transcribe video.mp4
# → video_GeminiUnd.md

# Precise timing needed: transcribe → LaiCut align → convert
omnicaptions transcribe video.mp4
omnicaptions LaiCut video.mp4 video_GeminiUnd.md
# → video_GeminiUnd_LaiCut.json
omnicaptions convert video_GeminiUnd_LaiCut.json -o video_GeminiUnd_LaiCut.srt
```

> **Note**: For translation, use `/omnicaptions:translate` (default: Claude, optional: Gemini API)
