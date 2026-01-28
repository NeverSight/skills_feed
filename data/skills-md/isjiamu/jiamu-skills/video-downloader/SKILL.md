---
name: video-downloader
description: Download videos from 1000+ websites (YouTube, Bilibili, Twitter/X, TikTok, etc.) using yt-dlp. Use this skill when users provide video URLs and want to download videos, extract audio, or need help with video download issues.
---

# Video Downloader

## Overview

Download videos from YouTube, Bilibili, Twitter/X, TikTok, and 1000+ other websites using yt-dlp. Supports multiple quality options, audio extraction, and automatic format selection.

## When to Use This Skill

Invoke this skill when users:
- Provide a video URL and want to download it
- Ask to download videos from any website
- Want to extract audio from online videos
- Need to download videos in specific quality (1080p, 4K, etc.)
- Request help with video download issues

## Quick Start

When a user provides a video URL:

```bash
# Run the bundled download script
python3 scripts/download.py "VIDEO_URL"
```

Default output: `~/Downloads/Videos/`

## Prerequisites

### Install yt-dlp

```bash
# macOS
brew install yt-dlp

# Cross-platform (pip)
pip install yt-dlp

# Update to latest version
brew upgrade yt-dlp  # or: pip install --upgrade yt-dlp
```

### Verify Installation

```bash
which yt-dlp && yt-dlp --version
```

## Common Download Commands

### Basic Download (Best Quality)

```bash
yt-dlp -P ~/Downloads/Videos "VIDEO_URL"
```

### Specific Quality

```bash
# Best quality up to 1080p
yt-dlp -f "bestvideo[height<=1080]+bestaudio/best" -P ~/Downloads/Videos "VIDEO_URL"

# Best quality up to 720p
yt-dlp -f "bestvideo[height<=720]+bestaudio/best" -P ~/Downloads/Videos "VIDEO_URL"

# Best available (including 4K)
yt-dlp -f "bestvideo+bestaudio/best" -P ~/Downloads/Videos "VIDEO_URL"
```

### Audio Only (MP3)

```bash
yt-dlp -x --audio-format mp3 -P ~/Downloads/Videos "VIDEO_URL"
```

### List Available Formats

```bash
yt-dlp -F "VIDEO_URL"
```

### Download with Subtitles

```bash
yt-dlp --write-subs --sub-lang zh,en -P ~/Downloads/Videos "VIDEO_URL"
```

### Playlist Download

```bash
yt-dlp -P ~/Downloads/Videos "PLAYLIST_URL"
```

## Bundled Script Reference

### scripts/download.py

Convenience wrapper with sensible defaults:

```bash
# Basic usage
python3 scripts/download.py "VIDEO_URL"

# Options
python3 scripts/download.py "VIDEO_URL" -o ~/Desktop          # Custom output
python3 scripts/download.py "VIDEO_URL" -f 1080               # Max 1080p
python3 scripts/download.py "VIDEO_URL" -a                    # Audio only (MP3)
python3 scripts/download.py "VIDEO_URL" -F                    # List formats
python3 scripts/download.py "VIDEO_URL" --subs                # With subtitles
```

## Supported Websites (Examples)

| Platform | Example URL Pattern |
|----------|---------------------|
| YouTube | `youtube.com/watch?v=`, `youtu.be/` |
| Bilibili | `bilibili.com/video/` |
| Twitter/X | `twitter.com/*/status/`, `x.com/*/status/` |
| TikTok | `tiktok.com/@*/video/` |
| Vimeo | `vimeo.com/` |
| Twitch | `twitch.tv/videos/` |
| Instagram | `instagram.com/p/`, `instagram.com/reel/` |
| Facebook | `facebook.com/watch/` |

Full list: https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md

## Platform-Specific Notes

### YouTube

For high-quality (1080p+) YouTube downloads, you may need:

1. **Browser cookies** (recommended):
```bash
yt-dlp --cookies-from-browser chrome "VIDEO_URL"
```

2. **PO token provider** (for persistent access):
See `references/platform-tips.md` for setup instructions.

### Bilibili

```bash
# Download with best quality
yt-dlp --cookies-from-browser chrome "https://www.bilibili.com/video/BV..."
```

### Twitter/X

```bash
# Usually works without authentication
yt-dlp "https://twitter.com/user/status/123456789"
```

## Troubleshooting

### "Video unavailable" or "Sign in required"

Use browser cookies:
```bash
yt-dlp --cookies-from-browser chrome "VIDEO_URL"
```

### Only Low Quality Available

1. Update yt-dlp: `brew upgrade yt-dlp`
2. Use browser cookies for authentication
3. Check available formats: `yt-dlp -F "VIDEO_URL"`

### Download Speed Issues

```bash
# Limit concurrent fragments
yt-dlp --concurrent-fragments 3 "VIDEO_URL"

# Use specific format to avoid merging
yt-dlp -f best "VIDEO_URL"
```

### Network Errors (China/Proxy)

```bash
# Use proxy
yt-dlp --proxy socks5://127.0.0.1:1080 "VIDEO_URL"

# Or set environment variable
export ALL_PROXY=socks5://127.0.0.1:1080
yt-dlp "VIDEO_URL"
```

## Output Format

Default filename template: `%(title)s [%(id)s].%(ext)s`

Custom template:
```bash
yt-dlp -o "%(uploader)s - %(title)s.%(ext)s" "VIDEO_URL"
```

## Further Reading

- **Platform Tips**: See `references/platform-tips.md` for site-specific guidance
- **yt-dlp Documentation**: https://github.com/yt-dlp/yt-dlp
- **Supported Sites**: https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md
