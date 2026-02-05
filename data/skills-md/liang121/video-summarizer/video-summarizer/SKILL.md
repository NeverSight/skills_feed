---
name: video-summarizer
description: "Download videos from 1800+ platforms (YouTube, Bilibili, Twitter/X, TikTok, Vimeo, Instagram, etc.) and generate complete resource package with video, audio, subtitles, and AI summary. Actions: summarize, download, transcribe, extract video content. Platforms: youtube.com, bilibili.com, twitter.com, x.com, tiktok.com, vimeo.com, instagram.com, twitch.tv. Outputs: MP4 video, MP3 audio, VTT subtitles with timestamps, TXT transcript, MD AI summary. Auto-installs uv, yt-dlp, ffmpeg. Python dependencies managed by uv."
---

# Video Summarizer

## Overview

Download videos from any platform and generate a complete resource package including:
- Original video file (mp4)
- Audio file (mp3)
- Subtitle file (with timestamps, vtt/srt format)
- Summary file (summary.md)

Supports all 1800+ websites supported by yt-dlp.

## Trigger Conditions

When the user:
- Provides a video link and asks for a summary
- Says "summarize this video", "what's in this video"
- Asks to "extract video content", "transcribe video"
- Says "download this video"
- Provides a link from YouTube/Bilibili/Twitter/Vimeo/TikTok etc.

## Supported Platforms

- YouTube (youtube.com, youtu.be)
- Bilibili (bilibili.com, b23.tv)
- Twitter/X (x.com, twitter.com)
- Vimeo (vimeo.com)
- TikTok (tiktok.com)
- Instagram (instagram.com)
- Twitch (twitch.tv)
- And 1800+ other platforms (all sites supported by yt-dlp)

## Output Structure

All files are saved to `downloads/<video-title>/` in the **current working directory**:

```
./downloads/
└── <video-title>/
    ├── video.mp4          # Original video
    ├── audio.mp3          # Extracted audio
    ├── subtitle.vtt       # Subtitles with timestamps
    ├── transcript.txt     # Plain text transcript (no timestamps)
    └── summary.md         # Structured summary
```

## Workflow

### Step 1: Install Dependencies

Run the install script to check and install all dependencies:

```bash
bash "$SKILL_DIR/scripts/install_deps.sh"
```

This installs: uv (Python package manager), ffmpeg, yt-dlp, and checks Python version.
faster-whisper will be automatically managed by uv.

### Step 2: Get Video Info and Create Output Directory

```bash
# Get video title (sanitize special characters for folder name)
TITLE=$(yt-dlp --print "%(title)s" "VIDEO_URL" | sed 's/[/:*?"<>|]/_/g' | cut -c1-80)
DURATION=$(yt-dlp --print "%(duration)s" "VIDEO_URL")

# Create output directory
OUTPUT_DIR=./downloads/"$TITLE"
mkdir -p "$OUTPUT_DIR"
```

### Step 3: Download Video and Audio

```bash
# Download video (mp4 format, best quality up to 1080p)
yt-dlp -f "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080][ext=mp4]/best" \
  --merge-output-format mp4 \
  -o "$OUTPUT_DIR/video.%(ext)s" "VIDEO_URL"

# Extract audio (mp3 format)
yt-dlp -x --audio-format mp3 -o "$OUTPUT_DIR/audio.%(ext)s" "VIDEO_URL"
```

### Step 4: Get Subtitles

**Priority order:**

1. **Try downloading manual subtitles (best quality)**
```bash
yt-dlp --write-subs --sub-lang zh,en,zh-Hans,zh-Hant --skip-download \
  -o "$OUTPUT_DIR/subtitle" "VIDEO_URL"
```

2. **Try downloading auto-generated subtitles**
```bash
yt-dlp --write-auto-subs --sub-lang zh,en --skip-download \
  -o "$OUTPUT_DIR/subtitle" "VIDEO_URL"
```

3. **Use faster-whisper transcription when no subtitles available**

```bash
uv run "$SKILL_DIR/scripts/parallel_transcribe.py" \
  --input "$OUTPUT_DIR/audio.mp3" \
  --output-dir "$OUTPUT_DIR" \
  --model small \
  --language auto
```

The script automatically:
- Splits long audio files at silence points
- Uses multiple CPU cores for parallel transcription
- Outputs both `subtitle.vtt` and `transcript.txt`

**Transcription Options**:
| Option | Default | Description |
|--------|---------|-------------|
| `--model` | small | tiny/base/small/medium/large-v3 |
| `--language` | auto | Language code or 'auto' |
| `--workers` | CPU/2 | Number of parallel workers |
| `--min-segment` | 60 | Min duration (sec) to enable splitting |

### Step 5: Generate Plain Text Transcript

If subtitles were downloaded (not transcribed), convert to plain text:

```bash
if [[ ! -f "$OUTPUT_DIR/transcript.txt" ]]; then
  SUBTITLE_FILE=$(ls "$OUTPUT_DIR"/*.vtt "$OUTPUT_DIR"/*.srt 2>/dev/null | head -1)
  if [[ "$SUBTITLE_FILE" == *.vtt ]]; then
    sed '/^[0-9]/d; /^$/d; /-->/d; /^WEBVTT/d; /^Kind:/d; /^Language:/d; /^NOTE/d' \
      "$SUBTITLE_FILE" > "$OUTPUT_DIR/transcript.txt"
  elif [[ "$SUBTITLE_FILE" == *.srt ]]; then
    sed '/^[0-9]/d; /^$/d; /-->/d' "$SUBTITLE_FILE" > "$OUTPUT_DIR/transcript.txt"
  fi
fi
```

### Step 6: Generate Summary File

1. Read prompt template from `$SKILL_DIR/reference/summary-prompt.md`
2. Replace placeholders: `{{TITLE}}`, `{{PLATFORM}}`, `{{URL}}`, `{{DURATION}}`, `{{LANGUAGE}}`, `{{DOWNLOAD_TIME}}`, `{{TRANSCRIPT}}`
3. Generate summary and save to `$OUTPUT_DIR/summary.md`

## Platform-Specific Handling

### Bilibili
```bash
# Prioritize Chinese subtitles
yt-dlp --sub-lang zh-Hans,zh-Hant,zh ...
# If login required
yt-dlp --cookies-from-browser chrome "VIDEO_URL"
```

### Platforms Requiring Login
```bash
yt-dlp --cookies-from-browser chrome "VIDEO_URL"
# or firefox
yt-dlp --cookies-from-browser firefox "VIDEO_URL"
```

## Error Handling

### Cannot Get Subtitles
Use the parallel transcription script (Step 4, option 3).

### Video Too Long (>1 hour)
1. Ask user if they only need partial content
2. The parallel script handles long files automatically

### Unsupported Platform
```bash
yt-dlp --list-extractors | grep -i "platform-name"
```

## Notes

1. **Storage**: Files saved to `./downloads/` in current working directory
2. **Copyright**: For personal learning use only
3. **Network**: Some platforms may require proxy
4. **First Run**: Whisper model download required (~244MB for small)
5. **Parallel Processing**: Long audio (>60s) auto-splits at silence points
