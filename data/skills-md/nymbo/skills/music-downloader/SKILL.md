---
name: music-downloader
description: This skill should be used when users need to download audio or music from online platforms like YouTube, SoundCloud, Spotify, or other streaming services. It provides yt-dlp and spotdl command templates for high-quality audio extraction, playlist downloads, metadata embedding, and multi-platform support.
---

# Music Downloader

## Overview

This skill enables downloading high-quality audio from various platforms (YouTube, SoundCloud, Spotify, etc.) using yt-dlp and spotdl. It provides command templates for single tracks, playlists, albums, and advanced features like metadata embedding, thumbnail extraction, and format conversion.

If the user did not provide a specific link to a song or playlist, you must search the web using tools in your environment to find what the user is looking for. 

When using the `Web_Search` tool, set the Search Type to `videos` and prefer official YouTube links.


## When to Use This Skill

Use this skill when users request:
- Downloading audio/music from YouTube, SoundCloud, Spotify, or other platforms
- Extracting audio from videos in MP3, Opus, or other formats
- Downloading entire playlists or albums
- High-quality audio with metadata and album art
- Batch downloading multiple tracks
- Converting video content to audio files

## Quick Start

**Most Common Use Case - Download MP3 from YouTube:**
```bash
yt-dlp -f bestaudio --extract-audio --audio-format mp3 --audio-quality 0 -o "%(title)s.%(ext)s" "VIDEO_URL"
```

**Download from Spotify:**
```bash
spotdl --audio-quality 320k --embed-metadata --output "{artist}/{title}.{ext}" "SPOTIFY_TRACK_URL"
```

**Note:** If you encounter issues, try downloading or updating yt-dlp via pip: `pip install --upgrade yt-dlp`

## General Commands

## List Available Formats
```bash
yt-dlp -F "URL"
```

## Download MP3 at Max Quality
```shell
yt-dlp -f bestaudio --extract-audio --audio-format mp3 --audio-quality 0 --postprocessor-args "-b:a 320k" -o "%(title)s.%(ext)s" "https://www.youtube.com/watch?v=xYJki23aeTQ&ab_channel=OnlyRealHipHop49"
```

## Basic High-Quality MP3 Download
```shell
yt-dlp -f bestaudio --extract-audio --audio-format mp3 --audio-quality 0 -o "%(title)s.%(ext)s" "VIDEO_URL"
```

## Download Custom Bitrate
```shell
yt-dlp -f bestaudio --extract-audio --audio-format mp3 --postprocessor-args "-b:a 192k" -o "%(title)s.%(ext)s" "VIDEO_URL"
```

## Download and add Metadata Tags
```shell
yt-dlp -f bestaudio --extract-audio --audio-format mp3 --audio-quality 0 --embed-metadata -o "%(title)s.%(ext)s" "VIDEO_URL"
```

## Download Entire Playlist
```shell
yt-dlp -f bestaudio --extract-audio --audio-format mp3 --audio-quality 0 -o "%(playlist_title)s/%(title)s.%(ext)s" "PLAYLIST_URL"
```

## Download Playlist (Specific Range)
```shell
yt-dlp --playlist-items 1-5 -f bestaudio --extract-audio --audio-format mp3 --audio-quality 0 -o "%(playlist_title)s/%(title)s.%(ext)s" "PLAYLIST_URL"
```

## Download HQ from SoundCloud
```shell
yt-dlp -f bestaudio --extract-audio --audio-format mp3 --audio-quality 0 -o "SoundCloud/%(uploader)s - %(title)s.%(ext)s" "SOUNDCLOUD_TRACK_URL"

```

## Embed Album Art Automatically
```shell
yt-dlp -f bestaudio --extract-audio --audio-format mp3 --embed-thumbnail --audio-quality 0 -o "%(title)s.%(ext)s" "VIDEO_URL"
```

## Download Specific Formats
*Opus instead of MP3*
```shell
yt-dlp -f bestaudio --extract-audio --audio-format opus -o "%(title)s.%(ext)s" "VIDEO_URL"
```

## Skip Already Downloaded Files
```shell
yt-dlp --download-archive "downloaded.txt" -f bestaudio --extract-audio --audio-format mp3 --audio-quality 0 -o "%(title)s.%(ext)s" "VIDEO_URL"
```

## Download Multiple Individual Files
```shell
yt-dlp -f bestaudio --extract-audio --audio-format mp3 --audio-quality 0 --add-metadata --embed-thumbnail --write-description --postprocessor-args "-b:a 320k" -o "%(title)s.%(ext)s" "https://www.youtube.com/watch?v=xYJki23aeTQ&ab_channel=OnlyRealHipHop49" "https://www.youtube.com/watch?v=xKJaew2gMSo&ab_channel=OnlyRealHipHop49" "https://www.youtube.com/watch?v=zLJkO3RnWUk&ab_channel=OnlyRealHipHop49"
```

## Download and Automatically Split by Chapters
```shell
yt-dlp -f bestaudio --extract-audio --audio-format mp3 --audio-quality 0 --split-chapters -o "%(title)s.%(ext)s" "VIDEO_URL"
```

## Extract Only a Portion of a Video (by Time)
```shell
yt-dlp -f bestvideo+bestaudio --external-downloader ffmpeg --external-downloader-args "ffmpeg_i:-ss 00:01:00 -to 00:05:00" -o "%(title)s.%(ext)s" "VIDEO_URL"
```

## Update Metadata of Existing Files
```shell
yt-dlp --download-archive "downloaded.txt" --skip-download --embed-metadata --embed-thumbnail --write-description "VIDEO_URL"
```

## Auto-Rename Duplicate Files
```shell
yt-dlp -f bestaudio --extract-audio --audio-format mp3 --audio-quality 0 --force-overwrites -o "%(title)s.%(ext)s" "VIDEO_URL"
```

## Download from a URL List File
```shell
yt-dlp -a "urls.txt" -f bestaudio --extract-audio --audio-format mp3 --audio-quality 0 -o "%(title)s.%(ext)s"
```

## Download and Limit Download Speed
```shell
yt-dlp -f bestaudio --extract-audio --audio-format mp3 --audio-quality 0 --rate-limit 1M -o "%(title)s.%(ext)s" "VIDEO_URL"
```

## Download from Vimeo
```shell
yt-dlp -f bestaudio --extract-audio --audio-format mp3 --audio-quality 0 -o "Vimeo/%(uploader)s - %(title)s.%(ext)s" "VIMEO_VIDEO_URL"
```

## Download from Facebook
```shell
yt-dlp -f bestaudio --extract-audio --audio-format mp3 --audio-quality 0 -o "Facebook/%(uploader)s - %(title)s.%(ext)s" "FACEBOOK_VIDEO_URL"
```

## Download from Instagram
```shell
yt-dlp -f bestaudio --extract-audio --audio-format mp3 --audio-quality 0 -o "Instagram/%(uploader)s - %(title)s.%(ext)s" "INSTAGRAM_VIDEO_URL"
```

## Download from Twitter
```shell
yt-dlp -f bestaudio --extract-audio --audio-format mp3 --audio-quality 0 -o "Twitter/%(uploader)s - %(title)s.%(ext)s" "TWITTER_VIDEO_URL"
```

## Download from TikTok
```shell
yt-dlp -f bestaudio --extract-audio --audio-format mp3 --audio-quality 0 -o "TikTok/%(uploader)s - %(title)s.%(ext)s" "TIKTOK_VIDEO_URL"
```

## Download from Reddit
```shell
yt-dlp -f bestaudio --extract-audio --audio-format mp3 --audio-quality 0 -o "Reddit/%(uploader)s - %(title)s.%(ext)s" "REDDIT_VIDEO_URL"
```

## Download from Dailymotion
```shell
yt-dlp -f bestaudio --extract-audio --audio-format mp3 --audio-quality 0 -o "Dailymotion/%(uploader)s - %(title)s.%(ext)s" "DAILYMOTION_VIDEO_URL"
```

## Download YouTube Transcript as Text
```shell
yt-dlp --write-auto-subs --sub-lang en --skip-download -o "%(title)s.%(ext)s" "VIDEO_URL"
```

## Download YouTube Transcript as Markdown
```shell
yt-dlp --write-auto-subs --sub-lang en --skip-download --convert-subs srt -o "%(title)s.md" "VIDEO_URL"
```

## Download Video Info and Save as JSON
```shell
yt-dlp --write-info-json --skip-download -o "%(title)s.json" "VIDEO_URL"
```

## List Available Formats without Downloading
```shell
yt-dlp -F "VIDEO_URL"
```

## Download from YouTube Age-Restricted Content
```shell
yt-dlp --username "YOUR_YOUTUBE_EMAIL" --password "YOUR_PASSWORD" -f bestvideo+bestaudio -o "%(title)s.%(ext)s" "AGE_RESTRICTED_VIDEO_URL"
```

---

# SoundCloud Commands

## List Available Formats
```bash
yt-dlp -F "URL"
```

## Download High-Quality MP3 from SoundCloud
```bash
yt-dlp -f bestaudio --extract-audio --audio-format mp3 --audio-quality 0 -o "SoundCloud/%(uploader)s - %(title)s.%(ext)s" "SOUNDCLOUD_TRACK_URL"
```

## Download HQ with Metadata from SoundCloud
```bash
yt-dlp -f bestaudio --extract-audio --audio-format mp3 --audio-quality 0 --embed-metadata -o "SoundCloud/%(uploader)s - %(title)s.%(ext)s" "SOUNDCLOUD_TRACK_URL"
```

## Download Entire Playlist from SoundCloud
```bash
yt-dlp -f bestaudio --extract-audio --audio-format mp3 --audio-quality 0 -o "SoundCloud/%(playlist_title)s/%(title)s.%(ext)s" "SOUNDCLOUD_PLAYLIST_URL"
```

## Download Entire Playlist from SoundCloud with Metadata
```bash
yt-dlp -f bestaudio --extract-audio --audio-format mp3 --audio-quality 0 --embed-metadata --add-metadata --embed-thumbnail -o "%(playlist_title)s/%(title)s.%(ext)s" "SOUNDCLOUD_PLAYLIST_URL"
```

## Download Multiple Playlists with Metadata
```bash
yt-dlp -f bestaudio --extract-audio --audio-format mp3 --audio-quality 0 --embed-metadata --add-metadata --embed-thumbnail -o "SoundCloud/%(playlist_title)s/%(title)s.%(ext)s" "x" "x" "x" "x" "x" "x" "x"
```

## Download Playlist with Specific Range
```bash
yt-dlp --playlist-items 1-5 -f bestaudio --extract-audio --audio-format mp3 --audio-quality 0 -o "SoundCloud/%(playlist_title)s/%(title)s.%(ext)s" "SOUNDCLOUD_PLAYLIST_URL"
```

## Download and Embed Album Art
```bash
yt-dlp -f bestaudio --extract-audio --audio-format mp3 --audio-quality 0 --embed-thumbnail -o "SoundCloud/%(uploader)s - %(title)s.%(ext)s" "SOUNDCLOUD_TRACK_URL"
```

## Skip Downloading Already Downloaded SoundCloud Files
```bash
yt-dlp --download-archive "downloaded_soundcloud.txt" -f bestaudio --extract-audio --audio-format mp3 --audio-quality 0 -o "SoundCloud/%(uploader)s - %(title)s.%(ext)s" "SOUNDCLOUD_TRACK_URL"
```

## Download Multiple Tracks from SoundCloud
```bash
yt-dlp -f bestaudio --extract-audio --audio-format mp3 --audio-quality 0 -o "SoundCloud/%(uploader)s - %(title)s.%(ext)s" "SOUNDCLOUD_TRACK_URL_1" "SOUNDCLOUD_TRACK_URL_2" "SOUNDCLOUD_TRACK_URL_3"
```

## Limit Download Speed for SoundCloud
```bash
yt-dlp -f bestaudio --extract-audio --audio-format mp3 --audio-quality 0 --rate-limit 1M -o "SoundCloud/%(uploader)s - %(title)s.%(ext)s" "SOUNDCLOUD_TRACK_URL"
```

## Download from SoundCloud and Split by Chapters (if available)
```bash
yt-dlp -f bestaudio --extract-audio --audio-format mp3 --audio-quality 0 --split-chapters -o "SoundCloud/%(uploader)s - %(title)s.%(ext)s" "SOUNDCLOUD_TRACK_URL"
```

## Download SoundCloud Track and Extract a Specific Portion
```bash
yt-dlp -f bestaudio --external-downloader ffmpeg --external-downloader-args "ffmpeg_i:-ss 00:01:00 -to 00:05:00" -o "SoundCloud/%(uploader)s - %(title)s.%(ext)s" "SOUNDCLOUD_TRACK_URL"
```

## Update Metadata of Existing SoundCloud Downloads
```bash
yt-dlp --download-archive "downloaded_soundcloud.txt" --skip-download --embed-metadata --embed-thumbnail "SOUNDCLOUD_TRACK_URL"
```

## Auto-Rename Duplicate SoundCloud Files
```bash
yt-dlp -f bestaudio --extract-audio --audio-format mp3 --audio-quality 0 --force-overwrites -o "SoundCloud/%(uploader)s - %(title)s.%(ext)s" "SOUNDCLOUD_TRACK_URL"
```

## Download from SoundCloud URL List File
```bash
yt-dlp -a "soundcloud_urls.txt" -f bestaudio --extract-audio --audio-format mp3 --audio-quality 0 -o "SoundCloud/%(uploader)s - %(title)s.%(ext)s"
```

---

# SpotifyDL Commands

## Download Single Song
```bash
spotdl --audio-quality 320k --embed-metadata --output "{artist}/{title}.{ext}" "SPOTIFY_TRACK_URL"
```
## Download Entire Playlist
```bash
spotdl --playlist "SPOTIFY_PLAYLIST_URL" --audio-quality 320k --embed-metadata --output "{playlist}/{title}.{ext}"
```
## Download Entire Album
```bash
spotdl --album "SPOTIFY_ALBUM_URL" --audio-quality 320k --embed-metadata --output "{album}/{title}.{ext}"
```
## Download Multiple Albums & Playlists at Once
```bash
spotdl --playlist "SPOTIFY_PLAYLIST_URL1" "SPOTIFY_PLAYLIST_URL2" --audio-quality 320k --embed-metadata --output "{playlist}/{title}.{ext}"
spotdl --album "SPOTIFY_ALBUM_URL1" "SPOTIFY_ALBUM_URL2" --audio-quality 320k --embed-metadata --output "{album}/{title}.{ext}"
```
