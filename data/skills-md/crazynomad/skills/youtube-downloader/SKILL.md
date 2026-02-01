---
name: youtube-downloader
description: Download videos from YouTube and 1000+ other sites using yt-dlp
---

# YouTube Video Downloader (yt-dlp)

Download videos from YouTube and 1000+ other sites using yt-dlp.

## Description

A powerful video downloader skill based on yt-dlp that supports YouTube, Bilibili, Twitter/X, TikTok, and many other platforms. Features include format selection, audio extraction, subtitle download, playlist support, and metadata preservation.

## When to Use

Use this skill when users:
- Provide YouTube URLs and want to download videos
- Mention "download video", "下载视频", "save video from YouTube"
- Want to extract audio from videos (MP3)
- Need to download playlists or channels
- Want subtitles/captions from videos
- Request video download from supported sites (Bilibili, Twitter, TikTok, etc.)

## Features

- **Multi-Platform Support**: YouTube, Bilibili, Twitter/X, TikTok, Vimeo, and 1000+ sites
- **Format Selection**: Choose video quality (1080p, 720p, 4K) or audio-only
- **Audio Extraction**: Extract audio as MP3, M4A, or other formats
- **Subtitle Download**: Auto-download subtitles in multiple languages
- **Playlist Support**: Download entire playlists or channels
- **Metadata Preservation**: Save video info, thumbnails, and descriptions
- **Resume Support**: Continue interrupted downloads
- **Progress Display**: Real-time download progress

## Usage

### Basic Syntax

```bash
python scripts/download_video.py "VIDEO_URL" [OPTIONS]
```

### Common Scenarios

**Download single video (best quality)**:
```bash
python scripts/download_video.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

**Download video in specific quality**:
```bash
python scripts/download_video.py "https://www.youtube.com/watch?v=VIDEO_ID" -f 1080
```

**Extract audio only (MP3)**:
```bash
python scripts/download_video.py "https://www.youtube.com/watch?v=VIDEO_ID" --audio-only
```

**Download with subtitles**:
```bash
python scripts/download_video.py "https://www.youtube.com/watch?v=VIDEO_ID" --subtitles
```

**Download playlist**:
```bash
python scripts/download_video.py "https://www.youtube.com/playlist?list=PLAYLIST_ID" --playlist
```

**Download N videos from playlist**:
```bash
python scripts/download_video.py "https://www.youtube.com/playlist?list=PLAYLIST_ID" --playlist -n 5
```

**Specify output directory**:
```bash
python scripts/download_video.py "URL" -o /path/to/output
```

### Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `url` | Video/Playlist URL (required) | - |
| `-o, --output` | Output directory | Current directory |
| `-f, --format` | Video quality: `best`, `1080`, `720`, `480`, `360` | `best` |
| `--audio-only` | Extract audio only (MP3) | False |
| `--subtitles` | Download subtitles | False |
| `--sub-lang` | Subtitle language(s) | `en,zh-Hans` |
| `--playlist` | Enable playlist download | False |
| `-n, --count` | Number of videos from playlist | All |
| `--metadata` | Save video metadata JSON | True |
| `--thumbnail` | Download thumbnail | False |
| `--cookies` | Path to cookies file (for age-restricted content) | None |

## Dependencies

```bash
# Install yt-dlp
pip install yt-dlp --break-system-packages

# For audio extraction (optional)
# macOS
brew install ffmpeg

# Ubuntu/Debian
apt-get install ffmpeg
```

## Output Structure

### Single Video
```
OutputDir/
├── Video Title [VIDEO_ID].mp4     # Video file
├── Video Title [VIDEO_ID].json    # Metadata (if --metadata)
├── Video Title [VIDEO_ID].jpg     # Thumbnail (if --thumbnail)
└── Video Title [VIDEO_ID].en.vtt  # Subtitles (if --subtitles)
```

### Playlist
```
OutputDir/
└── PlaylistName/
    ├── playlist_info.json
    ├── 001 - Video Title.mp4
    ├── 001 - Video Title.json
    ├── 002 - Another Video.mp4
    └── ...
```

### Metadata Example

```json
{
  "title": "Video Title",
  "uploader": "Channel Name",
  "upload_date": "2024-01-15",
  "duration": 300,
  "view_count": 1000000,
  "description": "Video description...",
  "tags": ["tag1", "tag2"],
  "video_file": "Video Title [VIDEO_ID].mp4"
}
```

## Claude Integration

When user requests video download:

1. **Read skill documentation**:
   ```python
   view("/mnt/skills/user/youtube-downloader/SKILL.md")
   ```

2. **Install dependencies** (if needed):
   ```bash
   pip install yt-dlp --break-system-packages
   ```

3. **Execute download**:
   ```bash
   python /mnt/skills/user/youtube-downloader/scripts/download_video.py \
     "USER_URL" -o /mnt/user-data/outputs
   ```

4. **Present files** to user:
   ```python
   present_files(["/mnt/user-data/outputs/..."])
   ```

## Supported Platforms

### Major Platforms
- **YouTube**: Videos, Shorts, Playlists, Channels, Live streams
- **Bilibili**: Videos, Episodes (may need cookies)
- **Twitter/X**: Video tweets
- **TikTok**: Videos (may need cookies)
- **Vimeo**: Videos
- **Twitch**: VODs, Clips

### Full List
yt-dlp supports 1000+ sites. Run `yt-dlp --list-extractors` for full list.

## Common Issues

**Q: Age-restricted videos?**
A: Use `--cookies` with exported browser cookies: `--cookies cookies.txt`

**Q: Format not available?**
A: Some videos may not have all quality options. Script will auto-select best available.

**Q: Download speed slow?**
A: This is usually server-side throttling. Consider using a VPN or waiting.

**Q: Need to login for private videos?**
A: Export cookies from your browser after logging in, then use `--cookies`.

**Q: Audio extraction fails?**
A: Install ffmpeg: `brew install ffmpeg` (macOS) or `apt install ffmpeg` (Linux)

## Example Conversations

**User**: "帮我下载这个 YouTube 视频: https://www.youtube.com/watch?v=dQw4w9WgXcQ"

**Claude**:
```bash
# Install yt-dlp
pip install yt-dlp --break-system-packages

# Download video
python /mnt/skills/user/youtube-downloader/scripts/download_video.py \
  "https://www.youtube.com/watch?v=dQw4w9WgXcQ" \
  -o /mnt/user-data/outputs

# Present files
present_files([...])
```

---

**User**: "下载这个 YouTube 视频的音频，我只要 MP3"

**Claude**:
```bash
python /mnt/skills/user/youtube-downloader/scripts/download_video.py \
  "VIDEO_URL" \
  --audio-only \
  -o /mnt/user-data/outputs
```

---

**User**: "Download this playlist, but only the first 5 videos"

**Claude**:
```bash
python /mnt/skills/user/youtube-downloader/scripts/download_video.py \
  "PLAYLIST_URL" \
  --playlist -n 5 \
  -o /mnt/user-data/outputs
```

## How It Works

### Workflow

1. **URL Parsing**: Detect platform and content type (video/playlist)
2. **Format Selection**: Determine best available format based on user preference
3. **Download**: Stream video/audio with progress display
4. **Post-Processing**: Extract audio (if requested), embed subtitles
5. **Metadata**: Save video information to JSON

### Under the Hood

This skill wraps yt-dlp with sensible defaults:
- Automatic format selection for best quality
- Proper filename sanitization
- Retry logic for failed downloads
- Progress display with ETA

## Limitations

- Some sites may require authentication (cookies)
- Age-restricted content needs browser cookies
- Download speed depends on source server
- Some DRM-protected content cannot be downloaded
- Live streams can only be downloaded after they end (VOD)

## Legal Notice

This tool is for personal use only. Please respect:
- YouTube Terms of Service
- Copyright laws in your jurisdiction
- Content creators' rights

Only download content you have the right to access. Do not redistribute copyrighted material.

## Version History

**v1.0** (Current)
- Initial release with yt-dlp wrapper
- Support for video, audio, subtitles, playlists
- Metadata and thumbnail preservation
- Multi-platform support

## References

- [yt-dlp GitHub](https://github.com/yt-dlp/yt-dlp)
- [yt-dlp Documentation](https://github.com/yt-dlp/yt-dlp#readme)
- [Supported Sites](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md)
