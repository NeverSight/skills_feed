---
name: omnicaptions-download
description: Use when downloading videos, audio, or captions from YouTube and other video platforms. Supports quality selection.
allowed-tools: Bash(omnicaptions:*)
---

# Download from Video Platforms

Download videos, audio, and captions from YouTube and 1000+ video platforms using yt-dlp.

## Confirmation Required

**IMPORTANT**: Before executing any download, you MUST confirm with the user using AskUserQuestion:

1. Show the URL to download
2. Show the quality setting (audio/video)
3. Show the output directory
4. Ask for confirmation

Example confirmation:
```
Ready to download:
- URL: https://youtube.com/watch?v=xxx
- Type: Audio only / Video (1080p)
- Save to: Current directory

Confirm download?
```

Only proceed with the download command after user confirms.

## When to Use

- Download YouTube videos/audio for offline use
- Extract captions from video platforms
- Get audio for local transcription or editing

## When NOT to Use

- Just need transcription (use `/omnicaptions:transcribe` - Gemini handles URLs directly)
- Converting existing caption formats (use `/omnicaptions:convert`)

## Setup

```bash
pip install https://github.com/lattifai/omni-captions-skills/raw/main/packages/lattifai_captions-0.1.0.tar.gz
pip install https://github.com/lattifai/omni-captions-skills/raw/main/packages/omnicaptions-0.1.0.tar.gz
```

## CLI Usage

**Note**: By default, files are saved to the current working directory. Do not specify `-o` unless the user explicitly requests a different location.

```bash
# Download audio only (default, saves to current directory)
omnicaptions download "https://www.youtube.com/watch?v=VIDEO_ID"

# Download video (1080p recommended)
omnicaptions download "https://youtube.com/watch?v=VIDEO_ID" -q 1080p

# Only use -o when user explicitly requests a different location
omnicaptions download "https://youtube.com/watch?v=VIDEO_ID" -o ./downloads/
```

| Option | Description |
|--------|-------------|
| `-o, --output` | Output directory (default: current) |
| `-q, --quality` | Quality: `audio` (default), `best`, `1080p`, `720p`, `480p`, `360p` |
| `-v, --verbose` | Verbose output |

## Quality Presets

| Preset | Description |
|--------|-------------|
| `audio` | Audio only (m4a/mp3), smallest size |
| `1080p` | 1080p video + audio (recommended for video) |
| `720p` | 720p video + audio |
| `480p` | 480p video + audio |
| `360p` | 360p video + audio |
| `best` | Best available quality (may be 4K+, very large) |

## Output

Downloads produce:
- **Audio/Video file**: `.m4a`, `.mp4`, etc.
- **Captions** (if available): `.vtt` or `.srt`
- **Metadata**: `.meta.json` (video resolution, title, etc. for ASS font scaling)

```
Video: ./VIDEO_ID.mp4
Audio: ./VIDEO_ID.m4a
Caption: ./VIDEO_ID.en.vtt
Metadata: ./VIDEO_ID.meta.json  # Used by convert for auto font size
Title: Video Title Here
```

The `.meta.json` file stores video resolution, which `omnicaptions convert` uses to auto-calculate font size for ASS karaoke output.

## Supported Platforms

YouTube, Bilibili, Vimeo, Twitter/X, and [1000+ sites](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md).

## Related Skills

| Skill | Use When |
|-------|----------|
| `/omnicaptions:transcribe` | Transcribe downloaded audio/video |
| `/omnicaptions:translate` | Translate captions with Gemini |
| `/omnicaptions:translate` | Translate captions with Claude (no API) |
| `/omnicaptions:convert` | Convert caption format |

### Workflow Examples

**Important**: Generate bilingual captions AFTER LaiCut alignment. Preserve language tag in filename.

```bash
# Has caption: download → LaiCut align (JSON) → convert → translate
omnicaptions download "https://youtube.com/watch?v=xxx"
# → xxx.en.vtt
omnicaptions LaiCut xxx.mp4 xxx.en.vtt
# → xxx.en_LaiCut.json
omnicaptions convert xxx.en_LaiCut.json -o xxx.en_LaiCut.srt
# → xxx.en_LaiCut_Claude_zh.srt (after translate)

# No caption: download → transcribe → LaiCut align (JSON) → convert → translate
omnicaptions download "https://youtube.com/watch?v=xxx"
omnicaptions transcribe xxx.mp4
# → xxx_GeminiUnd.md
omnicaptions LaiCut xxx.mp4 xxx_GeminiUnd.md
# → xxx_GeminiUnd_LaiCut.json
omnicaptions convert xxx_GeminiUnd_LaiCut.json -o xxx_GeminiUnd_LaiCut.srt
# → xxx_GeminiUnd_LaiCut_Claude_zh.srt (after translate)
```
