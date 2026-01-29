---
name: media-understand
description: 使用 AI 理解和分析多媒体内容（图片、视频、音频）。Use when user wants to 理解图片, 分析视频, 音频转文字, 视频问答, understand media, analyze video, transcribe audio, describe image, what is in this video/image/audio.
---

# Media Understanding

使用 Gemini 2.5 Flash 分析和理解多媒体内容。

## Supported Formats

| Type | Formats | Max Size |
|------|---------|----------|
| Image | jpg, jpeg, png, gif, webp | 20MB |
| Video | mp4, mpeg, mov, webm, YouTube URL | 100MB |
| Audio | wav, mp3, aiff, aac, ogg, flac, m4a | 100MB |

## Prerequisites

1. `MAX_API_KEY` 环境变量（Max 自动注入）
2. Bun 1.0+（Max v0.0.27+ 内置，无需额外安装）

## Usage

```bash
bun skills/media-understand/media-understand.js <media_path_or_url> [prompt] [language]
```

**Arguments:**
- `media_path_or_url`: File path or YouTube URL
- `prompt`: Question or analysis request (default: "Please describe this content")
- `language`: Output language - `chinese` or `english` (default: chinese)

## Examples

### Image Analysis

```bash
# Describe image
bun skills/media-understand/media-understand.js ./photo.jpg "请描述这张图片" chinese

# OCR - Extract text
bun skills/media-understand/media-understand.js ./screenshot.png "识别图片中的所有文字" chinese

# Answer question about image
bun skills/media-understand/media-understand.js ./chart.png "这个图表显示了什么趋势？" chinese
```

### Video Analysis

```bash
# YouTube video summary
bun skills/media-understand/media-understand.js "https://youtube.com/watch?v=xxx" "总结这个视频的主要内容" chinese

# Local video analysis
bun skills/media-understand/media-understand.js ./video.mp4 "视频中发生了什么？" chinese

# Timestamp-based question
bun skills/media-understand/media-understand.js "https://youtu.be/xxx" "视频 2:30 处讲了什么？" chinese
```

### Audio Analysis

```bash
# Transcribe audio
bun skills/media-understand/media-understand.js ./recording.mp3 "请转录这段音频" chinese

# Summarize podcast
bun skills/media-understand/media-understand.js ./podcast.m4a "总结这段播客的要点" chinese

# Detect speakers
bun skills/media-understand/media-understand.js ./meeting.wav "识别不同的说话人并整理他们说的内容" chinese
```

## Common Prompts

**Image:**
- 描述图片: "请详细描述这张图片的内容"
- OCR: "识别并提取图片中的所有文字"
- 物体识别: "图片中有哪些物体？"

**Video:**
- 总结: "总结这个视频的主要内容"
- 时间戳: "视频 X:XX 处发生了什么？"
- 提取信息: "视频中提到了哪些关键信息？"

**Audio:**
- 转录: "请转录这段音频的完整内容"
- 总结: "总结这段音频的要点"
- 说话人识别: "识别不同的说话人"

## Notes

- **Video via Gemini**: Best results with YouTube URLs. Local video files may have limited support.
- **Audio tokens**: ~32 tokens/second
- **Video tokens**: ~300 tokens/second at default resolution
- Long media files will consume more tokens

## Error Handling

**File not found**: Check the file path is correct

**Unsupported format**: Use supported formats listed above

**File too large**: Compress or trim the media file

**API error**: 请在 Max 设置中检查 Max API Key 是否正确配置
