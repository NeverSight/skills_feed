---
name: ffmpeg-cli
description: FFmpeg CLI reference for video and audio processing, format conversion, filtering, and media automation. Use when converting video formats, resizing or cropping video, trimming by time, replacing or extracting audio, mixing audio tracks, overlaying text or images, burning subtitles, creating GIFs, generating thumbnails, building slideshows, changing playback speed, encoding with H264/H265/VP9, setting CRF/bitrate, using GPU acceleration, creating storyboards, or running ffprobe. Covers filter_complex, stream selectors, -map, -c copy, seeking, scale, pad, crop, concat, drawtext, zoompan, xfade.
allowed-tools: Bash, Read, Glob, Grep, Write, Edit
---

# FFmpeg CLI Reference

## Contents

- [Dependencies](#dependencies)
- [Glossary of flags and filters](#glossary-of-flags-and-filters)
- [Converting formats](#converting-formats)
- [Resizing and padding](#resizing-and-padding)
- [Trim by time](#trim-by-time)
- [Verification and inspection](#verification-and-inspection)
- [Reference files](#reference-files)

## Dependencies

Verify ffmpeg is installed:

```sh
ffmpeg -version
```

Install if missing:

```sh
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg

# Windows (scoop)
scoop install ffmpeg
```

## Glossary of flags and filters

[Filtering reference](https://ffmpeg.org/ffmpeg-filters.html#Filtering-Introduction)

| Flag/Filter | Purpose |
|---|---|
| `-vf` (also `-filter:v`) | Video filter |
| `-af` (also `-filter:a`) | Audio filter |
| `-filter_complex` | Complex filter graph for multi-stream filtering |
| `[0]` | All streams from first input (0-based) |
| `[0:v]` | Video stream from first input |
| `[1:a]` | Audio stream from second input |
| `0:v:0` | First input, first video stream |
| `0:a:1` | First input, second audio stream |
| `[name]` | Named stream, used with `-filter_complex` |
| `-map [name]` | [Select stream for output](https://trac.ffmpeg.org/wiki/Map) |
| `-y` | Auto-overwrite output files without confirmation |

[Expression evaluations](https://ffmpeg.org/ffmpeg-all.html#Expression-Evaluation): `if`, `lte`, `gte` and more.

## Converting formats

Remux MP4 to MKV (no re-encoding):

```sh
ffmpeg -i input.mp4 -c copy output.mkv
```

MKV and MP4 are both containers for H264/H265 video and AAC/MP3 audio. Video quality is determined by the codec, not the container. MKV supports multiple video streams; MP4 has wider device support.

Remux MP4 to MOV:

```sh
ffmpeg -i input.mp4 -c copy output.mov
```

Encode MP4 to AVI (re-encodes):

```sh
ffmpeg -i input.mp4 output.avi
```

## Resizing and padding

Upscale to 1080x1920, preserve aspect ratio, black padding:

```sh
ffmpeg -i input.mp4 -vf "scale=w=1080:h=1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:color=black,setsar=1:1" output.mp4
```

**scale** options:

- `force_original_aspect_ratio=decrease` - auto-decrease output dimensions to fit aspect ratio
- `force_original_aspect_ratio=increase` - auto-increase dimensions
- `scale=w=1080:h=-1` - let ffmpeg pick correct height for aspect ratio
- `scale=w=1080:h=-2` - force dimensions divisible by 2

[scale reference](https://trac.ffmpeg.org/wiki/Scaling)

**pad** options:

- `pad=width:height:x:y:color` - x:y is top-left corner position
- `(ow-iw)/2:(oh-ih)/2` centres the video; negative values also centre
- [pad reference](https://ffmpeg.org/ffmpeg-filters.html#pad)

**setsar=1:1** ensures 1:1 pixel aspect ratio. Prevents ffmpeg from compensating for ratio changes. [setsar reference](https://ffmpeg.org/ffmpeg-filters.html#setdar_002c-setsar)

Two scaled outputs from one input (horizontal + vertical with logo overlay):

```sh
ffmpeg -i input.mp4 -i logo.png \
  -filter_complex "[0:v]split=2[s0][s1]; \
    [s0]scale=w=1920:h=1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=black,setsar=1:1[out1]; \
    [s1]scale=w=720:h=1280:force_original_aspect_ratio=decrease,pad=720:1280:(ow-iw)/2:(oh-ih)/2:color=black,setsar=1:1[s2]; \
    [s2][1]overlay=(main_w-overlay_w)/2:(main_w-overlay_w)/5[out2]" \
  -map [out1] -map 0:a output_youtube.mp4 \
  -map [out2] -map 0:a output_shorts.mp4
```

## Trim by time

```sh
ffmpeg -i input.mp4 -ss 00:00:10 -to 00:00:25 output.mp4
```

For faster but less accurate trimming, see the **Input/output seeking** section in `references/encoding-and-settings.md`. For the `-c copy` trade-offs when trimming, see `references/core-concepts.md`.

## Verification and inspection

List supported formats:

```sh
ffmpeg -formats
```

List supported codecs:

```sh
ffmpeg -codecs
```

### ffprobe

[ffprobe](https://ffmpeg.org/ffprobe.html) provides structured metadata about media files.

Show detailed stream information:

```sh
ffprobe -show_streams -i input.mp4
```

Verify moov atom position (faststart):

```sh
ffprobe -v trace -i input.mp4
```

Look for `type:'moov'` near the beginning of output to confirm faststart is applied.

## Reference files

Load these on demand with the Read tool when the task requires deeper coverage.

| File | Topics |
|---|---|
| `references/core-concepts.md` | `-c copy` (remux vs transcode), input/output seeking, encoding quick ref (H264/H265/VP9 CRF ranges), GPU acceleration overview, `format=yuv420p`, `-movflags +faststart` |
| `references/audio-processing.md` | Replace audio, extract audio, mix audio, combine MP3 tracks, crossfade, change audio format, merge and normalise |
| `references/advanced-editing.md` | Playback speed, FPS change, jump cuts, video cropping for social, drawtext overlay, subtitles (burn/embed/extract), combine media (overlay, logo, background, concat intro/main/outro, vstack) |
| `references/asset-generation.md` | Image to video, slideshow with fade, Ken Burns (zoompan), GIFs, video compilation with fades, thumbnails (single/multiple/scene), image thumbnails, storyboards (scene tile/keyframe/Nth frame) |
| `references/encoding-and-settings.md` | Optimised daily command, H264 (libx264) deep-dive, H265 (libx265) Apple compat, VP9 (libvpx-vp9) constant quality, 1-pass vs 2-pass, `-c copy` detailed, seeking detailed, GPU detailed (Nvidia/Intel/AMD) |
