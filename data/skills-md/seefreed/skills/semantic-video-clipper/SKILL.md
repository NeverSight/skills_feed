---
name: semantic-video-clipper
description: AI analyzes subtitles to identify optimal split points, then clips video segments using FFmpeg based on AI-provided cue indices. Use when asked to segment videos (e.g., .mp4) based on .vtt/.srt subtitles.
---

# Semantic Video Clipper

## Overview

Segment a long video into clips by having AI analyze subtitle semantics and identify natural topic boundaries. The lightweight Python script handles parsing, timing calculation, and FFmpeg clipping based on AI-provided segment indices. Output clips and matching subtitles with filenames `basename_<index>.*` in same directory as the source video.

## Workflow

### Step 1: AI Analysis
- Read full subtitle content (.vtt or .srt)
- Understand semantic flow and topic transitions
- Identify natural split points that:
  - Align with complete sentence endings
  - Occur at topic shifts (new concepts, examples, recaps)
  - Fit within duration constraints (typically 25-60 seconds)
- Return segment ranges as cue index pairs: `[(0, 12), (12, 25), (25, 40), ...]`

### Step 2: Python Script Execution
- Parse subtitles into Cue objects with timing
- Convert cue indices to time ranges
- Call FFmpeg in parallel to clip video segments
- Shift subtitle times so each segment starts at 00:00
- Save output files as `basename_1.mp4` + `basename_1.vtt`, `basename_2.*`, etc.

## Scripted execution

**Script location**: `skills/semantic-video-clipper/scripts/clip_video.py`

**Option 1: From skill directory** (recommended)

```bash
cd skills/semantic-video-clipper
python3 scripts/clip_video.py /path/video.mp4 /path/subtitles.vtt "0-12,12-25,25-40"
```

**Option 2: From any location**

```bash
python3 skills/semantic-video-clipper/scripts/clip_video.py /path/video.mp4 /path/subtitles.vtt "0-12,12-25,25-40"
```

The segments argument uses 0-based cue indices:
- `"0-12,12-25,25-40"` - Three segments: cues 0-11, 12-24, 25-39

Optional flags:

```bash
--workers 4          # Number of parallel workers (default: 4)
--dry-run            # Only print segment plan without clipping
```

## Dependencies

- `ffmpeg` (external - must be in PATH)

Notes:
- AI handles semantic analysis; Python script only handles parsing, timing, and FFmpeg clipping.
- Output files always land beside the source video, named with an underscore plus 1-based index.
- Parallel processing (`--workers`) provides 3-4x speedup for multi-clip videos.

