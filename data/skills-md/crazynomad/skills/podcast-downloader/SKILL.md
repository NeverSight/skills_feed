---
name: podcast-downloader
description: Download podcast episodes from Apple Podcasts using iTunes API with RSS fallback
---

# Apple Podcast Downloader (API Enhanced)

Download podcast episodes from Apple Podcasts using iTunes API with RSS fallback.

## Description

Enhanced podcast downloader that prioritizes iTunes API for faster, more reliable downloads compared to traditional RSS parsing. Automatically detects region codes (cn/us/jp), supports multiple fallback methods, and includes rich metadata extraction.

## When to Use

Use this skill when users:
- Provide Apple Podcast URLs and want to download episodes
- Mention "download podcast", "下载播客", "get podcast audio"
- Want to save podcast episodes locally
- Need podcast metadata (title, date, duration, description)

## Features

- **iTunes API Priority**: 3-5x faster than RSS parsing
- **Smart Region Detection**: Auto-extracts country code from URL
- **Multiple Fallback Methods**:
  1. Direct API query (fastest)
  2. List search (fast)
  3. RSS feed parsing (reliable fallback)
- **Rich Metadata**: Saves episode info, release date, duration, description
- **User-Agent Support**: Resolves 403 errors
- **Progress Display**: Real-time download progress with MB/percentage

## Usage

### Basic Syntax

```bash
python scripts/download_podcast.py "APPLE_PODCAST_URL" [-n COUNT] [-o OUTPUT_DIR]
```

### Common Scenarios

**Download specific episode** (URL with `?i=` parameter):
```bash
python scripts/download_podcast.py "https://podcasts.apple.com/cn/podcast/id1711052890?i=1000744375610"
```

**Download latest N episodes**:
```bash
python scripts/download_podcast.py "https://podcasts.apple.com/cn/podcast/id1711052890" -n 5
```

**Download all available episodes** (up to 200):
```bash
python scripts/download_podcast.py "https://podcasts.apple.com/us/podcast/id123456789"
```

**Specify output directory**:
```bash
python scripts/download_podcast.py "URL" -n 10 -o /mnt/user-data/outputs
```

### Arguments

- `url` (required): Apple Podcast URL
- `-n, --count`: Number of latest episodes to download (default: all available)
- `-o, --output`: Output directory (default: current directory)

## Dependencies

```bash
pip install requests feedparser --break-system-packages
```

## Output Structure

```
PodcastName/
├── podcast_info.json          # Podcast metadata
├── 001 - Episode Title.m4a    # Audio file
├── 001 - Episode Title.json   # Episode metadata
├── 002 - Episode Title.m4a
└── ...
```

### Metadata Examples

**podcast_info.json**:
```json
{
  "podcast_name": "Podcast Name",
  "artist": "Author Name",
  "country": "cn",
  "total_episodes": 272,
  "download_date": "2026-01-13T14:30:00"
}
```

**Episode metadata**:
```json
{
  "title": "Episode Title",
  "release_date": "2025-01-10",
  "duration_minutes": 40,
  "description": "Episode description...",
  "audio_file": "001 - Episode Title.m4a"
}
```

## Claude Integration

When user requests podcast download:

1. **Read skill documentation**:
   ```python
   view("/mnt/skills/user/podcast-downloader-v2/SKILL.md")
   ```

2. **Install dependencies** (if needed):
   ```bash
   pip install requests feedparser --break-system-packages
   ```

3. **Execute download**:
   ```bash
   python /mnt/skills/user/podcast-downloader-v2/scripts/download_podcast.py \
     "USER_URL" -n COUNT -o /mnt/user-data/outputs
   ```

4. **Present files** to user:
   ```python
   present_files(["/mnt/user-data/outputs/PodcastName/..."])
   ```

## How It Works

### Workflow

1. **URL Parsing**: Extract podcast ID, episode ID (if present), region code
2. **Data Retrieval** (priority order):
   - Method A: Direct API query for specific episode (fastest)
   - Method B: Fetch episode list and search (fast)
   - Method C: Parse RSS feed (fallback)
3. **Download**: Stream audio with progress display, save metadata

### API Endpoints

- Query episode: `https://itunes.apple.com/lookup?id={episode_id}&entity=podcastEpisode&country={country}`
- Query list: `https://itunes.apple.com/lookup?id={podcast_id}&entity=podcastEpisode&country={country}&limit=200`
- Get RSS: `https://itunes.apple.com/lookup?id={podcast_id}&country={country}&entity=podcast`

## Limitations

- iTunes API limit: 200 episodes maximum per request
- Only supports Apple Podcasts (not Spotify, Google Podcasts, etc.)
- Requires internet connection
- Audio format depends on podcast source (usually .m4a or .mp3)

## Common Issues

**Q: Can't find old episodes?**  
A: iTunes API returns max 200 recent episodes. Script automatically falls back to RSS for older content.

**Q: Getting 403 errors?**  
A: User-Agent headers are included to prevent most 403 errors. If persists, may be source restriction.

**Q: Which regions are supported?**  
A: All Apple Podcasts regions (cn, us, jp, uk, etc.). Auto-detected from URL.

## Example Conversation

**User**: "帮我下载这个播客的最新 3 集: https://podcasts.apple.com/cn/podcast/id1711052890"

**Claude**:
```bash
# View skill
view("/mnt/skills/user/podcast-downloader-v2/SKILL.md")

# Install dependencies
pip install requests feedparser --break-system-packages

# Download
python /mnt/skills/user/podcast-downloader-v2/scripts/download_podcast.py \
  "https://podcasts.apple.com/cn/podcast/id1711052890" \
  -n 3 \
  -o /mnt/user-data/outputs

# Present files
present_files([...])
```

## Version History

**v2.0** (Current)
- iTunes API as primary data source
- Auto region detection
- Multiple fallback methods
- User-Agent support for 403 prevention
- Rich metadata saving
- Improved progress display

**v1.0** (Original)
- RSS feed parsing
- Basic download functionality

## References

See `/references/` directory for:
- `usage_guide.md`: Detailed usage instructions and examples
- `technical_details.md`: In-depth technical documentation
- `api_reference.md`: iTunes API documentation

## License

Personal use tool. Please respect Apple Podcasts terms of service. For personal listening and learning only.
