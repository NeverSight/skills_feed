---
name: fetch-youtube-auto-closed-captions
description: Download YouTube auto-generated closed captions (VTT) with yt-dlp when a user provides a YouTube URL or video ID and wants auto-subs/transcripts; includes checking for yt-dlp and offering install guidance if missing.
---

# YouTube auto captions via yt-dlp

Use this skill to fetch auto-generated English captions from YouTube using yt-dlp.

## Workflow

1. Accept a YouTube URL or video ID from the user.
2. Check if `yt-dlp` is available.
3. If missing, ask the user if they want help installing it and offer install commands.
4. Run the download command or the bundled script to write auto-subs in VTT and a readable transcript in TXT.

## Preferred command

Use exactly this command when running manually:

```bash
yt-dlp \
  --skip-download \
  --write-auto-subs \
  --sub-lang en \
  --sub-format vtt \
  https://www.youtube.com/watch?v=VIDEO_ID
```

## Bundled script

Use `scripts/download_auto_captions.sh` to handle URL or ID input and an optional output directory. It writes both `.vtt` and a cleaned `.txt` transcript (timestamps/tags stripped, common non-speech cues removed, merged into sentences):

```bash
bash scripts/download_auto_captions.sh <url-or-id> [output-dir]
```

## Install guidance (ask first)

If `yt-dlp` is not installed, ask the user whether to install and then offer one of:

- macOS (Homebrew): `brew install yt-dlp`
- Python (pipx): `pipx install yt-dlp`
- Python (pip): `python3 -m pip install -U yt-dlp`

## Notes

- Output files are written as `.vtt` subtitles and `.txt` transcripts in the chosen directory.
- Auto-subs depend on what YouTube provides; some videos may not have auto-generated captions.
