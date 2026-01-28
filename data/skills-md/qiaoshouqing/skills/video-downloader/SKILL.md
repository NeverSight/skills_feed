---
name: video-downloader
description: "Download videos using yt-dlp. Use when user asks to download video, download audio, download subtitles, or provides a video URL from YouTube, Bilibili, Twitter, etc."
version: "1.0.0"
metadata:
  author: qiaoshouqing
---

# Video Downloader - Download Videos with yt-dlp

Download videos, audio, or subtitles from YouTube, Bilibili, Twitter, and 1000+ other sites using yt-dlp.

## When to Use

- User asks to download a video
- User asks to download or extract audio
- User asks to download subtitles
- User provides a video URL (YouTube, Bilibili, Twitter, etc.)
- User wants to specify video quality (720p, 1080p, etc.)

## Prerequisites - Auto Install

**IMPORTANT:** Before any download, check and install dependencies automatically.

### Step 0: Check and Install Dependencies

```bash
# Check if yt-dlp is installed, install if missing
if ! command -v yt-dlp &>/dev/null; then
  echo "Installing yt-dlp..."
  brew install yt-dlp
fi

# Check if ffmpeg is installed, install if missing
if ! command -v ffmpeg &>/dev/null; then
  echo "Installing ffmpeg..."
  brew install ffmpeg
fi

# Verify installation
yt-dlp --version && echo "yt-dlp: ready"
ffmpeg -version 2>&1 | head -1 && echo "ffmpeg: ready"
```

Run this check **every time** before downloading. Install automatically without asking user.

## Instructions for Agent

### Step 1: Ensure Dependencies Installed

Run the prerequisite check above. If yt-dlp or ffmpeg is missing, install via `brew install yt-dlp ffmpeg`.

### Step 2: Parse User Intent

Identify what the user wants:
| User Intent | Keywords |
|-------------|----------|
| Video (default) | "download", "video" |
| Audio only | "audio", "mp3", "music", "extract audio" |
| Video + Subtitles | "with subtitles", "embed subtitles" |
| Subtitles only | "only subtitles", "subtitles only", "just subtitles" |
| Specific quality | "720p", "1080p", "4k", "best", "worst" |

### Step 3: Build Command

Base command structure:
```bash
yt-dlp [OPTIONS] "URL"
```

**Common options by intent:**

1. **Basic video download** (best quality):
```bash
yt-dlp -o "%(title)s.%(ext)s" "URL"
```

2. **Audio only (MP3)**:
```bash
yt-dlp -x --audio-format mp3 -o "%(title)s.%(ext)s" "URL"
```

3. **Specific quality** (e.g., 720p):
```bash
yt-dlp -f "bestvideo[height<=720]+bestaudio/best[height<=720]" -o "%(title)s.%(ext)s" "URL"
```

4. **Video with embedded subtitles**:
```bash
yt-dlp --write-subs --sub-lang en,zh-Hans,zh-Hant --embed-subs -o "%(title)s.%(ext)s" "URL"
```

5. **Subtitles only** (no video):
```bash
yt-dlp --write-subs --write-auto-subs --sub-lang en,zh-Hans,zh-Hant --skip-download -o "%(title)s" "URL"
```

### Step 4: Execute and Report

Run the command and report:
- File name and location
- File size (if available)
- Any warnings or errors

## Command Reference

| Task | Command |
|------|---------|
| Best quality video | `yt-dlp "URL"` |
| Audio (MP3) | `yt-dlp -x --audio-format mp3 "URL"` |
| Audio (M4A) | `yt-dlp -x --audio-format m4a "URL"` |
| 720p video | `yt-dlp -f "bv[height<=720]+ba/b[height<=720]" "URL"` |
| 1080p video | `yt-dlp -f "bv[height<=1080]+ba/b[height<=1080]" "URL"` |
| 4K video | `yt-dlp -f "bv[height<=2160]+ba/b[height<=2160]" "URL"` |
| With subtitles | `yt-dlp --write-subs --embed-subs "URL"` |
| Subtitles only | `yt-dlp --write-subs --write-auto-subs --skip-download "URL"` |
| List formats | `yt-dlp -F "URL"` |
| Playlist | `yt-dlp -o "%(playlist_index)s-%(title)s.%(ext)s" "PLAYLIST_URL"` |

## Response Guidelines

- Always confirm what will be downloaded before starting
- Show download progress or final result
- Report the output file name and location
- If download fails, explain the error and suggest solutions

## Error Handling

| Error | Solution |
|-------|----------|
| `yt-dlp: command not found` | Auto-install: `brew install yt-dlp` |
| `ffmpeg not found` | Auto-install: `brew install ffmpeg` |
| `Video unavailable` | Check if URL is correct or video is region-locked |
| `Private video` | Cannot download private videos without authentication |
| `Format not available` | Use `yt-dlp -F URL` to list available formats |
| `No subtitles found` | Try `--write-auto-subs` for auto-generated subtitles |
| `brew: command not found` | Install Homebrew first: `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"` |
