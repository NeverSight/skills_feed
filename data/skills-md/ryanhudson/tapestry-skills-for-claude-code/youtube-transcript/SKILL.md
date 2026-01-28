---
name: youtube-transcript
description: This skill should be used when the user provides a YouTube URL and wants to "download transcript", "get captions", "get subtitles", "transcribe video", or extract text content from a YouTube video. Handles manual subtitles, auto-generated captions, and Whisper transcription as fallback.
allowed-tools: Bash,Read,Write
---

# YouTube Transcript Downloader

Extract transcripts from YouTube videos using yt-dlp. Supports manual subtitles, auto-generated captions, and Whisper transcription as a last resort.

## Prerequisites

This skill requires [UV](https://docs.astral.sh/uv/) for dependency management. Run from the tapestry-skills project root.

## Workflow

```
URL → Validate → Check yt-dlp → List Subtitles → Download → Convert to Text → Save
```

**Priority order**:
1. Manual subtitles (highest quality)
2. Auto-generated captions (usually available)
3. Whisper transcription (requires user consent)

## Security Requirements

All security utilities are available via UV from the project root.

### URL Validation

```bash
# Validate YouTube URL (must also be a valid YouTube domain)
if [[ ! "$URL" =~ ^https?://(www\.)?(youtube\.com|youtu\.be)/ ]]; then
    echo "Error: Not a valid YouTube URL"
    exit 1
fi

# Run general security validation (SSRF protection, etc.)
uv run tapestry-validate-url "$URL" || exit 1
```

### Filename Sanitization

```bash
# Use tapestry sanitization utility
SAFE_TITLE=$(uv run tapestry-sanitize-filename "$VIDEO_TITLE")
```

## Step 1: Check yt-dlp Installation

yt-dlp is included in the project dependencies. Use via UV:

```bash
# yt-dlp is available through uv run
uv run yt-dlp --version
```

## Step 2: Check Available Subtitles

Always check what's available first:

```bash
uv run yt-dlp --list-subs "$URL"
```

Look for:
- `Available subtitles` (manual, higher quality)
- `Available automatic captions` (auto-generated)

## Step 3: Download Subtitles

### Try Manual First

```bash
TEMP_DIR=$(mktemp -d)
trap "rm -rf '$TEMP_DIR'" EXIT

if uv run yt-dlp --write-sub --skip-download --sub-langs en -o "$TEMP_DIR/transcript" "$URL" 2>/dev/null; then
    echo "Downloaded manual subtitles"
else
    # Fall back to auto-generated
    uv run yt-dlp --write-auto-sub --skip-download --sub-langs en -o "$TEMP_DIR/transcript" "$URL"
    echo "Downloaded auto-generated captions"
fi
```

## Step 4: Convert VTT to Clean Text

Use the tapestry VTT converter which handles deduplication automatically:

```bash
VIDEO_TITLE=$(uv run yt-dlp --print "%(title)s" "$URL" 2>/dev/null)
SAFE_TITLE=$(uv run tapestry-sanitize-filename "$VIDEO_TITLE")

VTT_FILE=$(find "$TEMP_DIR" -name "*.vtt" | head -n 1)

# Convert VTT to clean text (handles deduplication, HTML tags, entities)
uv run tapestry-vtt-to-text "$VTT_FILE" --output "${SAFE_TITLE}.txt"

echo "Saved: ${SAFE_TITLE}.txt"
```

## Whisper Transcription (Last Resort)

**Only offer when no subtitles are available. Requires explicit user consent.**

### Check File Size First

```bash
DURATION=$(uv run yt-dlp --print "%(duration)s" "$URL" 2>/dev/null)
TITLE=$(uv run yt-dlp --print "%(title)s" "$URL" 2>/dev/null)

echo "No subtitles available for: $TITLE"
echo "Duration: $((DURATION / 60)) minutes"
echo ""
echo "Download audio and transcribe with Whisper? (requires ~1-3GB for model)"
echo "Type 'yes' to proceed:"
```

**Wait for explicit "yes" before proceeding.**

### Download and Transcribe

```bash
TEMP_DIR=$(mktemp -d)
trap "rm -rf '$TEMP_DIR'" EXIT

# Download audio only
uv run yt-dlp -x --audio-format mp3 -o "$TEMP_DIR/audio.%(ext)s" "$URL"

# Transcribe with Whisper (installs on first use)
uv run --with openai-whisper whisper "$TEMP_DIR/audio.mp3" --model base --output_format vtt --output_dir "$TEMP_DIR"

# Convert VTT to text
VTT_FILE=$(find "$TEMP_DIR" -name "*.vtt" | head -n 1)
uv run tapestry-vtt-to-text "$VTT_FILE" --output "${SAFE_TITLE}.txt"
```

## Complete Workflow Script

```bash
#!/bin/bash
set -e

URL="$1"

# Validate YouTube URL
if [[ ! "$URL" =~ ^https?://(www\.)?(youtube\.com|youtu\.be)/ ]]; then
    echo "Error: Not a valid YouTube URL"
    exit 1
fi

# Run security validation
uv run tapestry-validate-url "$URL" || exit 1

# Get video info
VIDEO_TITLE=$(uv run yt-dlp --print "%(title)s" "$URL" 2>/dev/null)
SAFE_TITLE=$(uv run tapestry-sanitize-filename "$VIDEO_TITLE")

echo "Video: $VIDEO_TITLE"
echo ""

# Create temp directory
TEMP_DIR=$(mktemp -d)
trap "rm -rf '$TEMP_DIR'" EXIT

# Try to download subtitles
echo "Checking for subtitles..."
if uv run yt-dlp --write-sub --skip-download --sub-langs en -o "$TEMP_DIR/transcript" "$URL" 2>/dev/null; then
    echo "Found manual subtitles"
elif uv run yt-dlp --write-auto-sub --skip-download --sub-langs en -o "$TEMP_DIR/transcript" "$URL" 2>/dev/null; then
    echo "Found auto-generated captions"
else
    echo "No subtitles available"
    # Offer Whisper option here (with user consent)
    exit 1
fi

# Find VTT file
VTT_FILE=$(find "$TEMP_DIR" -name "*.vtt" | head -n 1)

if [ -z "$VTT_FILE" ]; then
    echo "Error: No VTT file found"
    exit 1
fi

# Convert to clean text
uv run tapestry-vtt-to-text "$VTT_FILE" --output "${SAFE_TITLE}.txt"

WORD_COUNT=$(wc -w < "${SAFE_TITLE}.txt" | tr -d ' ')

echo ""
echo "Transcript saved: ${SAFE_TITLE}.txt"
echo "Words: $WORD_COUNT"
```

## Error Handling

| Issue | Solution |
|-------|----------|
| UV not installed | Install with `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| Invalid URL | Reject non-YouTube URLs |
| No subtitles | Offer Whisper with user consent |
| Private/restricted video | Inform user, cannot access |
| SSL errors | Try `--no-check-certificate` (with warning) |
| Download timeout | Retry or inform user |

## Dependencies

All dependencies are managed via UV and `pyproject.toml`:

- **yt-dlp**: YouTube downloads (pinned version)
- **openai-whisper** (optional): For videos without subtitles

## Security Reference

For complete security guidelines: `../shared/references/security-guidelines.md`
