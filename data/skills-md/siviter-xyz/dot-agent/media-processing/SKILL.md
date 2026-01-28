---
name: media-processing
description: Media processing utilities for images, audio, and video using FFmpeg and ImageMagick. Use when working with media conversion, optimization, or batch processing tasks.
---

# Media Processing

Tools and workflows for working with images, audio, and video in a repeatable, scriptable way using standard CLI tools (FFmpeg, ImageMagick) and Python helpers.

## When to Use

- Working with image batches (thumbnails, resizing, format conversion)
- Converting media between formats (video ↔ audio ↔ image)
- Optimizing video size while maintaining acceptable quality
- Preparing assets for web, mobile, or archival use
- Designing or refining CLI workflows around FFmpeg/ImageMagick

## Key Principles

- **CLI-first workflows**: Prefer command-line tools (FFmpeg, ImageMagick) and scripts that can be automated in CI or local tooling.
- **Deterministic scripts**: Scripts should be safe to run repeatedly with predictable output paths and options.
- **Non-destructive defaults**: Default to writing outputs to new files/directories rather than overwriting originals.
- **Cross-platform friendly**: Keep examples and scripts usable on Linux, macOS, and Windows where possible.
- **Agent-agnostic**: Guidance should work with any coding agent (Cursor, Claude, Copilot, etc.), not one specific environment.

## Capabilities

- **Image workflows**
  - Batch resize and thumbnail generation
  - Aspect-ratio–aware resizing (fit, fill, cover, exact)
  - Optional watermarking
  - Format conversion (e.g., PNG → WebP, JPEG)

- **Media conversion**
  - Detects media type (video, audio, image) from extension
  - Uses FFmpeg for video/audio, ImageMagick for images
  - Quality presets for `web`, `archive`, and `mobile` use cases
  - Batch conversion with dry-run and verbose modes

- **Video optimization**
  - Resolution and frame-rate adjustments
  - Single-pass (CRF) or two-pass encoding
  - Audio bitrate tuning
  - Basic before/after comparison (size, bitrate, resolution, FPS)

## Scripts

Scripts live in `scripts/` and are intended to be run directly from a shell:

- `batch_resize.py`
  - Batch image resizing with multiple strategies (`fit`, `fill`, `cover`, `exact`, `thumbnail`)
  - Optional watermark overlay
  - Supports parallel processing and dry-run mode

- `media_convert.py`
  - Unified conversion tool for video, audio, and images
  - Automatically picks FFmpeg or ImageMagick
  - Uses quality presets (`web`, `archive`, `mobile`)
  - Supports batch conversion and format changes (e.g., `.mov` → `.mp4`, `.wav` → `.mp3`)

- `video_optimize.py`
  - Focused on video size/quality trade-offs
  - Resolution caps, FPS reduction, CRF tuning, optional two-pass encoding
  - Optional comparison summary between original and optimized outputs

See `scripts/requirements.txt` for environment expectations (Python 3.10+, FFmpeg, ImageMagick) and system installation hints.

## Usage Guidelines

- **Check dependencies first**
  - Ensure `ffmpeg` and `ffprobe` are installed and on `PATH` for video/audio tasks.
  - Ensure `magick` (ImageMagick) is installed and on `PATH` for image tasks.

- **Prefer dry-runs when exploring**
  - Use `--dry-run` and/or `--verbose` flags on scripts to inspect generated commands before running them.

- **Keep originals**
  - Point outputs to a separate directory on first runs (e.g., `--output ./out/`) to avoid accidental overwrites.

- **Document workflows**
  - When you find good command lines or script invocations, promote them into project scripts (e.g., `just`, `npm scripts`, or CI jobs) so they’re repeatable.

## References

For deeper tool-specific notes (placeholders for now, extend as needed), see:
- `references/ffmpeg-encoding.md` – FFmpeg encoding patterns and flags
- `references/ffmpeg-filters.md` – Common filter graphs (scale, crop, audio filters)
- `references/ffmpeg-streaming.md` – Streaming-friendly settings and HLS/DASH tips
- `references/format-compatibility.md` – Container/codec compatibility notes (web, mobile, desktop)
- `references/imagemagick-batch.md` – Batch image processing patterns with ImageMagick
- `references/imagemagick-editing.md` – Image editing operations (crop, resize, composite, text, etc.)

