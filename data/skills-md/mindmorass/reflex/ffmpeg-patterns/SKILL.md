---
name: ffmpeg-patterns
description: FFmpeg video and audio processing patterns. Use when transcoding video/audio, extracting clips, adding filters, merging media, creating thumbnails, or batch processing media files.
---

# FFmpeg Patterns

Best practices for video and audio processing with FFmpeg.

## Basic Operations

### Transcode Video

```bash
# Convert to MP4 (H.264 + AAC)
ffmpeg -i input.mov -c:v libx264 -preset medium -crf 23 \
       -c:a aac -b:a 128k output.mp4

# Convert to WebM (VP9 + Opus)
ffmpeg -i input.mp4 -c:v libvpx-vp9 -crf 30 -b:v 0 \
       -c:a libopus -b:a 128k output.webm

# Convert to HLS for streaming
ffmpeg -i input.mp4 -codec: copy -start_number 0 \
       -hls_time 10 -hls_list_size 0 -f hls output.m3u8
```

### Extract Audio

```bash
# Extract audio to MP3
ffmpeg -i video.mp4 -vn -acodec mp3 -ab 192k audio.mp3

# Extract audio to WAV (uncompressed)
ffmpeg -i video.mp4 -vn -acodec pcm_s16le audio.wav

# Extract audio from specific time range
ffmpeg -i video.mp4 -ss 00:01:00 -t 00:00:30 -vn audio.mp3
```

### Trim and Cut

```bash
# Cut from timestamp to duration
ffmpeg -i input.mp4 -ss 00:01:30 -t 00:02:00 -c copy output.mp4

# Cut from start to end timestamp
ffmpeg -i input.mp4 -ss 00:01:30 -to 00:03:30 -c copy output.mp4

# Fast seek (put -ss before -i for large files)
ffmpeg -ss 00:10:00 -i large_video.mp4 -t 00:05:00 -c copy clip.mp4
```

## Video Filters

### Resize and Scale

```bash
# Scale to specific dimensions
ffmpeg -i input.mp4 -vf "scale=1920:1080" output.mp4

# Scale preserving aspect ratio (fit within)
ffmpeg -i input.mp4 -vf "scale=1920:1080:force_original_aspect_ratio=decrease" output.mp4

# Scale with padding (letterbox/pillarbox)
ffmpeg -i input.mp4 -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2" output.mp4

# Scale to 50%
ffmpeg -i input.mp4 -vf "scale=iw/2:ih/2" output.mp4
```

### Speed Adjustment

```bash
# Speed up video 2x (with audio pitch correction)
ffmpeg -i input.mp4 -filter_complex "[0:v]setpts=0.5*PTS[v];[0:a]atempo=2.0[a]" \
       -map "[v]" -map "[a]" output.mp4

# Slow down video 0.5x
ffmpeg -i input.mp4 -filter_complex "[0:v]setpts=2.0*PTS[v];[0:a]atempo=0.5[a]" \
       -map "[v]" -map "[a]" output.mp4

# Extreme slow motion (0.25x) - chain atempo filters
ffmpeg -i input.mp4 -filter_complex "[0:v]setpts=4.0*PTS[v];[0:a]atempo=0.5,atempo=0.5[a]" \
       -map "[v]" -map "[a]" output.mp4
```

### Crop and Overlay

```bash
# Crop video (width:height:x:y)
ffmpeg -i input.mp4 -vf "crop=640:480:100:50" output.mp4

# Crop center to 16:9
ffmpeg -i input.mp4 -vf "crop=ih*16/9:ih" output.mp4

# Add watermark
ffmpeg -i video.mp4 -i watermark.png \
       -filter_complex "overlay=W-w-10:H-h-10" output.mp4

# Add text overlay
ffmpeg -i input.mp4 -vf "drawtext=text='Hello World':fontsize=24:fontcolor=white:x=10:y=10" output.mp4
```

### Color and Effects

```bash
# Adjust brightness, contrast, saturation
ffmpeg -i input.mp4 -vf "eq=brightness=0.1:contrast=1.2:saturation=1.3" output.mp4

# Convert to grayscale
ffmpeg -i input.mp4 -vf "colorchannelmixer=.3:.4:.3:0:.3:.4:.3:0:.3:.4:.3" output.mp4

# Add fade in/out
ffmpeg -i input.mp4 -vf "fade=t=in:st=0:d=2,fade=t=out:st=8:d=2" output.mp4

# Blur video
ffmpeg -i input.mp4 -vf "boxblur=5:1" output.mp4
```

## Audio Processing

### Volume and Normalization

```bash
# Adjust volume
ffmpeg -i input.mp4 -af "volume=1.5" output.mp4

# Normalize audio (loudnorm)
ffmpeg -i input.mp4 -af "loudnorm=I=-16:TP=-1.5:LRA=11" output.mp4

# Detect silence
ffmpeg -i input.mp4 -af "silencedetect=noise=-30dB:d=0.5" -f null -
```

### Audio Filters

```bash
# Remove background noise
ffmpeg -i input.mp4 -af "afftdn=nf=-25" output.mp4

# Add echo
ffmpeg -i input.mp4 -af "aecho=0.8:0.88:60:0.4" output.mp4

# High-pass filter (remove low frequencies)
ffmpeg -i input.mp4 -af "highpass=f=200" output.mp4

# Low-pass filter (remove high frequencies)
ffmpeg -i input.mp4 -af "lowpass=f=3000" output.mp4
```

## Combining Media

### Concatenate Videos

```bash
# Create file list
cat > files.txt << EOF
file 'video1.mp4'
file 'video2.mp4'
file 'video3.mp4'
EOF

# Concatenate (same codec)
ffmpeg -f concat -safe 0 -i files.txt -c copy output.mp4

# Concatenate (different codecs - re-encode)
ffmpeg -f concat -safe 0 -i files.txt -c:v libx264 -c:a aac output.mp4
```

### Merge Audio and Video

```bash
# Replace audio track
ffmpeg -i video.mp4 -i audio.mp3 -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 output.mp4

# Mix audio tracks
ffmpeg -i video.mp4 -i background.mp3 \
       -filter_complex "[0:a][1:a]amerge=inputs=2[a]" \
       -map 0:v -map "[a]" -c:v copy -ac 2 output.mp4

# Add audio to silent video
ffmpeg -i silent_video.mp4 -i audio.mp3 -c:v copy -c:a aac -shortest output.mp4
```

### Picture-in-Picture

```bash
# Overlay smaller video
ffmpeg -i main.mp4 -i overlay.mp4 \
       -filter_complex "[1:v]scale=320:-1[pip];[0:v][pip]overlay=W-w-10:H-h-10" \
       output.mp4

# Side by side
ffmpeg -i left.mp4 -i right.mp4 \
       -filter_complex "[0:v]scale=640:-1[l];[1:v]scale=640:-1[r];[l][r]hstack" \
       output.mp4
```

## Thumbnails and Screenshots

```bash
# Single screenshot at timestamp
ffmpeg -i video.mp4 -ss 00:00:10 -vframes 1 thumbnail.jpg

# Generate thumbnails every N seconds
ffmpeg -i video.mp4 -vf "fps=1/10" thumbnails_%03d.jpg

# Generate thumbnail sheet/sprite
ffmpeg -i video.mp4 -vf "fps=1/5,scale=160:-1,tile=5x5" sprite.jpg

# Best quality thumbnail
ffmpeg -i video.mp4 -ss 00:00:10 -vframes 1 -q:v 2 thumbnail.jpg
```

## Streaming Formats

### HLS (HTTP Live Streaming)

```bash
# Basic HLS
ffmpeg -i input.mp4 -c:v libx264 -c:a aac \
       -hls_time 10 -hls_playlist_type vod \
       -hls_segment_filename "segment_%03d.ts" \
       playlist.m3u8

# Multi-bitrate HLS
ffmpeg -i input.mp4 \
       -filter_complex "[0:v]split=3[v1][v2][v3]; \
       [v1]scale=1920:1080[v1out]; \
       [v2]scale=1280:720[v2out]; \
       [v3]scale=854:480[v3out]" \
       -map "[v1out]" -map 0:a -c:v libx264 -b:v 5M -c:a aac -b:a 192k \
       -hls_time 10 -hls_playlist_type vod 1080p.m3u8 \
       -map "[v2out]" -map 0:a -c:v libx264 -b:v 2M -c:a aac -b:a 128k \
       -hls_time 10 -hls_playlist_type vod 720p.m3u8 \
       -map "[v3out]" -map 0:a -c:v libx264 -b:v 1M -c:a aac -b:a 96k \
       -hls_time 10 -hls_playlist_type vod 480p.m3u8
```

### DASH (Dynamic Adaptive Streaming)

```bash
ffmpeg -i input.mp4 -c:v libx264 -c:a aac \
       -f dash -seg_duration 10 \
       -use_template 1 -use_timeline 1 \
       manifest.mpd
```

## Batch Processing

```bash
# Convert all MP4s to WebM
for f in *.mp4; do
    ffmpeg -i "$f" -c:v libvpx-vp9 -crf 30 -c:a libopus "${f%.mp4}.webm"
done

# Resize all images in directory
for f in *.jpg; do
    ffmpeg -i "$f" -vf "scale=1280:-1" "resized_$f"
done

# Extract audio from multiple videos
for f in *.mp4; do
    ffmpeg -i "$f" -vn -c:a mp3 -b:a 192k "${f%.mp4}.mp3"
done
```

## Hardware Acceleration

```bash
# NVIDIA NVENC (encoding)
ffmpeg -i input.mp4 -c:v h264_nvenc -preset fast output.mp4

# NVIDIA NVDEC (decoding) + NVENC
ffmpeg -hwaccel cuda -i input.mp4 -c:v h264_nvenc output.mp4

# macOS VideoToolbox
ffmpeg -i input.mp4 -c:v h264_videotoolbox -b:v 5M output.mp4

# Intel QuickSync
ffmpeg -i input.mp4 -c:v h264_qsv output.mp4
```

## Useful Probing Commands

```bash
# Get video info
ffprobe -v quiet -print_format json -show_format -show_streams video.mp4

# Get duration
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 video.mp4

# Get resolution
ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0 video.mp4

# Get codec
ffprobe -v error -select_streams v:0 -show_entries stream=codec_name -of default=noprint_wrappers=1:nokey=1 video.mp4
```

## References

- [FFmpeg Documentation](https://ffmpeg.org/documentation.html)
- [FFmpeg Filters](https://ffmpeg.org/ffmpeg-filters.html)
- [FFmpeg Wiki](https://trac.ffmpeg.org/wiki)
