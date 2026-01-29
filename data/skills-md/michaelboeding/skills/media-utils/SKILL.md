---
name: media-utils
description: >
  Internal utility skill for media assembly operations. NOT called directly by users.
  Used by producer skills (video-producer, podcast-producer, audio-producer, social-producer)
  to stitch, mix, and assemble final media outputs.
---

# Media Utilities

**Internal utilities for media assembly. Used by producer skills.**

These scripts wrap FFmpeg to provide reliable media operations.

## Prerequisites

- **FFmpeg** must be installed: `brew install ffmpeg` (macOS) or `apt install ffmpeg` (Linux)
- Check with: `python3 check_ffmpeg.py`

## Available Utilities

### audio_concat.py
Concatenate multiple audio files into one.

```bash
# Simple concatenation
python3 audio_concat.py -i intro.wav segment1.wav outro.wav -o podcast.mp3

# With crossfade between clips
python3 audio_concat.py -i track1.wav track2.wav --crossfade 2.0

# With normalization
python3 audio_concat.py -i *.wav -o mixed.mp3 --normalize
```

### audio_mix.py
Mix voice/narration with background music (with optional ducking).

```bash
# Voice + music with ducking (music lowers when voice plays)
python3 audio_mix.py --voice narration.wav --music background.mp3 -o final.mp3

# Adjust music volume (default: 0.3)
python3 audio_mix.py --voice voice.wav --music music.mp3 --music-volume 0.2

# No ducking
python3 audio_mix.py --voice voice.wav --music music.mp3 --no-duck

# With fade in/out on music
python3 audio_mix.py --voice voice.wav --music music.mp3 --fade-in 2 --fade-out 3
```

### video_concat.py
Concatenate multiple video clips.

```bash
# Simple concatenation
python3 video_concat.py -i clip1.mp4 clip2.mp4 clip3.mp4 -o final.mp4

# With fade transition
python3 video_concat.py -i *.mp4 -o final.mp4 --transition fade --duration 1.0

# Normalize to 1080p
python3 video_concat.py -i *.mp4 -o final.mp4 --resolution 1080p

# Available transitions: fade, dissolve, wipeleft, wiperight, slideup, slidedown
```

### video_audio_merge.py
Add audio track(s) to video.

```bash
# Replace video audio
python3 video_audio_merge.py --video clip.mp4 --audio voiceover.mp3 -o final.mp4

# Add voice + music with ducking
python3 video_audio_merge.py --video clip.mp4 --voice narration.wav --music bg.mp3

# Mix with existing video audio
python3 video_audio_merge.py --video clip.mp4 --audio music.mp3 --mix

# Audio sync offset
python3 video_audio_merge.py --video clip.mp4 --audio audio.mp3 --offset 0.5
```

### video_strip_audio.py
Remove audio from video files (for replacing with custom audio).

```bash
# Strip audio from single file
python3 video_strip_audio.py -i video.mp4 -o silent_video.mp4

# Strip audio from multiple files (batch mode)
python3 video_strip_audio.py -i clip1.mp4 clip2.mp4 clip3.mp4

# Strip with custom output directory
python3 video_strip_audio.py -i *.mp4 --output-dir ./silent/

# Re-encode video instead of copying
python3 video_strip_audio.py -i video.mp4 --reencode
```

### check_ffmpeg.py
Verify FFmpeg installation.

```bash
python3 check_ffmpeg.py
# ✅ FFmpeg is available!
#    ffmpeg version 6.0 ...
```

### report_to_pdf.py
Convert Markdown reports to professional PDF documents.

```bash
# Basic conversion
python3 report_to_pdf.py -i analysis.md -o analysis.pdf

# With custom title and executive style
python3 report_to_pdf.py -i report.md -o report.pdf --title "Q4 Market Analysis" --style executive

# Technical documentation with table of contents
python3 report_to_pdf.py -i docs.md -o docs.pdf --style technical --toc
```

**Available styles:**
| Style | Description |
|-------|-------------|
| `business` | Clean, professional (default) |
| `executive` | Executive summary with larger fonts |
| `technical` | Technical documentation |
| `minimal` | Minimal styling, maximum content |

**Requires:** `pip install markdown weasyprint`

## Usage by Producer Skills

These utilities are called by the producer skills to assemble final outputs:

```python
from pathlib import Path
import subprocess
import sys

# Get path to media-utils
UTILS_PATH = Path(__file__).parent.parent.parent / "media-utils" / "scripts"

def concat_audio(files: list, output: str):
    cmd = [
        sys.executable,
        str(UTILS_PATH / "audio_concat.py"),
        "-i", *files,
        "-o", output
    ]
    subprocess.run(cmd, check=True)
```

## Output Formats

| Utility | Default Output | Options |
|---------|----------------|---------|
| audio_concat | MP3 | Inherits from input |
| audio_mix | MP3 | MP3 |
| video_concat | MP4 (H.264) | MP4 |
| video_audio_merge | MP4 (H.264) | MP4 |
| video_strip_audio | MP4 (copy) | MP4 |