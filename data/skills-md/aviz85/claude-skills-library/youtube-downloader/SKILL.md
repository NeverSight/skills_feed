---
name: youtube-downloader
description: "Download YouTube videos with quality presets. Use for: download youtube, yt download, video download, youtube to whatsapp, youtube mp3."
version: "1.0.0"
author: aviz85
tags:
  - youtube
  - video
  - download
  - media
---

# YouTube Video Downloader

Download YouTube videos with quality control, optimized for sharing on WhatsApp and other platforms.

## Requirements

**This skill requires Python to be installed on your system.**

- Python 3.9+ (required)
- yt-dlp (`pip install yt-dlp`)
- ffmpeg (for audio extraction)

> **First time setup?** Read [SETUP.md](./SETUP.md) for detailed installation instructions for Windows, macOS, and Linux.

## Quick Start

```bash
cd ~/.claude/skills/youtube-downloader/scripts

# Download for WhatsApp (144p, small file)
python download.py "https://www.youtube.com/watch?v=VIDEO_ID" --quality whatsapp

# Download standard quality (480p)
python download.py "https://www.youtube.com/watch?v=VIDEO_ID" --quality standard

# Download high quality (720p)
python download.py "https://www.youtube.com/watch?v=VIDEO_ID" --quality high

# Download best quality available
python download.py "https://www.youtube.com/watch?v=VIDEO_ID" --quality best

# List available formats
python download.py "https://www.youtube.com/watch?v=VIDEO_ID" --list
```

## Quality Presets

| Preset | Resolution | Max Size | Use Case |
|--------|-----------|----------|----------|
| `whatsapp` | 144p | ~10MB | WhatsApp sharing (default) |
| `standard` | 480p | ~50MB | General use |
| `high` | 720p | ~100MB | Good quality |
| `best` | Best available | Varies | Maximum quality |

## Options

| Option | Description |
|--------|-------------|
| `--quality` / `-q` | Quality preset (whatsapp/standard/high/best) |
| `--output` / `-o` | Output directory (default: current dir) |
| `--list` / `-l` | List available formats without downloading |
| `--audio-only` / `-a` | Extract audio only (MP3) |

## Examples

```bash
# Download and send to WhatsApp
python download.py "https://youtube.com/watch?v=xxx" -q whatsapp
# Then use WhatsApp skill to send

# Download to specific folder
python download.py "https://youtube.com/watch?v=xxx" -o ~/Downloads

# Audio only (for podcasts/music)
python download.py "https://youtube.com/watch?v=xxx" --audio-only
```

## WhatsApp Size Limits

- **16MB**: Direct video sharing limit
- **2GB**: Document sharing limit (preserves quality)

For videos over 16MB, either:
1. Use lower quality preset
2. Send as document (not video)
