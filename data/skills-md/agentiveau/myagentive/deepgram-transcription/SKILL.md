---
name: deepgram-transcription
description: Transcribe audio and video files using the Deepgram API. This skill should be used when the user requests transcription of audio files (mp3, wav, m4a, aac) or video files (mp4, mov, avi, etc.). Handles large video files by extracting audio first to reduce upload size and processing time.
---

# Deepgram Transcription

## Overview

This skill enables efficient transcription of audio and video files using the Deepgram API. It automatically handles large video files by extracting audio first, reducing upload time and API costs. Outputs include both full JSON responses with timestamps and clean text transcripts.

## When to Use This Skill

Use this skill when:
- Transcribing audio files (mp3, wav, m4a, aac, etc.)
- Transcribing video files (mp4, mov, avi, mkv, etc.)
- Converting speech in media files to text
- Creating transcripts with or without timestamps
- Processing multiple recordings for documentation

## Core Workflow

### 1. Determine Input Type

First, identify the input file type:

**Audio files** (mp3, wav, m4a, aac):
- Can be transcribed directly
- Smaller file sizes, faster uploads

**Video files** (mp4, mov, avi, etc.):
- Should extract audio first for files >50MB
- Reduces upload time significantly (e.g., 190MB video → 3MB audio)
- No quality loss for transcription purposes

### 2. Extract Audio (For Video Files)

For video files, especially those larger than 50MB, extract audio before transcription:

```bash
ffmpeg -i input_video.mp4 -vn -acodec aac -b:a 128k output_audio.m4a -y
```

Parameters:
- `-vn`: No video (audio only)
- `-acodec aac`: AAC audio codec
- `-b:a 128k`: 128kbps bitrate (good quality, small size)
- `-y`: Overwrite output file

This reduces file size by ~98% while preserving speech quality.

### 3. Transcribe with Deepgram

Use the provided `scripts/transcribe.py` script for automated transcription:

```bash
scripts/transcribe.py input_file.mp4 \
  --api-key YOUR_DEEPGRAM_API_KEY \
  --output-dir ./transcripts \
  --extract-audio
```

Or use curl directly for manual control:

```bash
curl -X POST "https://api.deepgram.com/v1/listen?model=nova-2&smart_format=true" \
  -H "Authorization: Token YOUR_API_KEY" \
  -H "Content-Type: audio/mp4" \
  --data-binary @audio_file.m4a \
  -o transcription.json
```

### 4. Extract and Save Results

The transcription response includes:

**Full JSON** (with timestamps, confidence scores, metadata):
```json
{
  "results": {
    "channels": [{
      "alternatives": [{
        "transcript": "Full text here...",
        "words": [
          {"word": "hello", "start": 0.5, "end": 0.9, "confidence": 0.99}
        ]
      }]
    }]
  }
}
```

**Extract plain text transcript**:
```bash
cat transcription.json | python3 -c "import json, sys; data=json.load(sys.stdin); print(data['results']['channels'][0]['alternatives'][0]['transcript'])" > transcript.txt
```

## Using the Transcription Script

The `scripts/transcribe.py` provides a complete workflow:

### Basic Usage

```bash
# Transcribe a video file (auto-extracts audio)
scripts/transcribe.py video.mp4 --api-key YOUR_KEY --extract-audio

# Transcribe an audio file directly
scripts/transcribe.py audio.mp3 --api-key YOUR_KEY

# Specify output directory
scripts/transcribe.py video.mov --api-key YOUR_KEY --output-dir ./transcripts
```

### Advanced Options

```bash
# Use a different Deepgram model
scripts/transcribe.py file.mp4 --api-key YOUR_KEY --model whisper-large

# Disable smart formatting
scripts/transcribe.py file.mp4 --api-key YOUR_KEY --no-smart-format

# Custom audio bitrate when extracting
scripts/transcribe.py file.mp4 --api-key YOUR_KEY --extract-audio --audio-bitrate 192k
```

### Output Files

The script generates:
1. `{filename}_transcription.json` - Full Deepgram response with timestamps
2. `{filename}_transcript.txt` - Clean text transcript only

## Recommended Settings

**Deepgram Model**: `nova-2`
- Latest and most accurate model
- Good balance of speed and quality
- Handles various accents and audio quality

**Smart Formatting**: Enabled (default)
- Automatic punctuation
- Proper capitalization
- Number formatting
- Better readability

**Audio Bitrate**: 128kbps
- Excellent speech quality
- Small file size
- Fast uploads

## Common Scenarios

### Scenario 1: Single Video File

```bash
# User: "Transcribe this video recording"
scripts/transcribe.py recording.mp4 --api-key KEY --extract-audio
```

### Scenario 2: Multiple Screen Recordings

```bash
# Extract audio from all videos first
for f in *.mov; do
  ffmpeg -i "$f" -vn -acodec aac -b:a 128k "${f%.mov}_audio.m4a" -y
done

# Transcribe all audio files
for f in *_audio.m4a; do
  scripts/transcribe.py "$f" --api-key KEY --output-dir ./transcripts
done
```

### Scenario 3: Audio-Only File

```bash
# Direct transcription (no extraction needed)
scripts/transcribe.py podcast.mp3 --api-key KEY
```

## Troubleshooting

### File Access Issues

If encountering permission errors:
- Check file permissions: `ls -l filename`
- Ensure file exists: `file filename`
- Use absolute paths if needed

### Large File Uploads Timing Out

For very large files:
1. Always extract audio first (`--extract-audio`)
2. Increase timeout in script if needed
3. Consider splitting long recordings

### API Key Issues

- Verify API key is correct
- Check Deepgram account has available credits
- Ensure no extra spaces in key

## File Size Guidelines

| Input Type | Size | Recommendation |
|------------|------|----------------|
| Audio | Any | Transcribe directly |
| Video | < 50MB | Can transcribe directly |
| Video | 50-200MB | Extract audio first |
| Video | > 200MB | Must extract audio first |

## Resources

### scripts/transcribe.py

Complete Python script handling:
- Audio extraction from video
- Deepgram API calls
- Response parsing
- Output file generation

Execute without loading into context for efficiency.

### references/api_reference.md

Deepgram API documentation including:
- Available models and features
- API parameters and options
- Response format details
- Best practices

Load into context when needing detailed API information.
