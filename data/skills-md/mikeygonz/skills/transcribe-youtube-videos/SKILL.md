---
name: transcribe-youtube-videos
description: Fetch transcripts from YouTube videos. Use when the user shares a YouTube URL, references a video, wants to know what someone said in a video, or needs video content as text.
compatibility: Requires Python 3.x (auto-installs youtube-transcript-api on first run)
metadata:
  author: mikeygonz
  version: "1.1"
---

# Transcribe YouTube Videos

Fetch transcripts from any YouTube video. No API key required.

## When to Activate

- User shares a YouTube URL and wants to discuss its content
- User asks "what did they say about X in this video?"
- User references a video and needs the transcript
- User wants to summarize, quote, or analyze video content

## Workflow

### Step 1: Extract Video ID

Parse the YouTube URL to extract the video ID. Handle these formats:
- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `VIDEO_ID` (direct ID)

### Step 2: Fetch Transcript

Run this single command that handles installation and fetching in one shot:

```bash
python3 -c "
try:
    from youtube_transcript_api import YouTubeTranscriptApi
except ImportError:
    import subprocess, sys
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--user', '-q', 'youtube-transcript-api'])
    except subprocess.CalledProcessError:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--break-system-packages', '-q', 'youtube-transcript-api'])
    from youtube_transcript_api import YouTubeTranscriptApi

def fmt_time(seconds):
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    return f'{h}:{m:02d}:{s:02d}' if h else f'{m}:{s:02d}'

api = YouTubeTranscriptApi()
transcript = api.fetch('VIDEO_ID')

# Print with timestamps every ~30 seconds for navigation
last_ts = -30
for entry in transcript:
    if entry.start - last_ts >= 30:
        print(f'\n[{fmt_time(entry.start)}]')
        last_ts = entry.start
    print(entry.text)
"
```

Replace `VIDEO_ID` with the extracted ID.

**Features:**
- Self-installs dependency on first run (handles macOS Homebrew Python)
- Adds timestamp markers every ~30 seconds for easy video navigation
- Clean output without per-line timestamps (reduces noise)

### Step 2b: Fetch Without Timestamps (Optional)

If you just need raw text without any timestamps:

```bash
python3 -c "
try:
    from youtube_transcript_api import YouTubeTranscriptApi
except ImportError:
    import subprocess, sys
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--user', '-q', 'youtube-transcript-api'])
    except subprocess.CalledProcessError:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--break-system-packages', '-q', 'youtube-transcript-api'])
    from youtube_transcript_api import YouTubeTranscriptApi

api = YouTubeTranscriptApi()
transcript = api.fetch('VIDEO_ID')
for entry in transcript:
    print(f"{entry.start}: {entry.text}")
"
```

### Step 3: Format Output

Present the transcript with:
1. A header indicating the video URL
2. The full transcript text (without timestamps for readability)
3. Optionally offer to save to a file if it's long

## Error Handling

If the transcript fetch fails:
1. Check if the video has captions enabled
2. Try fetching auto-generated captions with language fallback:

```bash
python3 -c "
from youtube_transcript_api import YouTubeTranscriptApi
api = YouTubeTranscriptApi()
transcript_list = api.list(video_id='VIDEO_ID')
print('Available transcripts:')
for t in transcript_list:
    print(f'  - {t.language} ({t.language_code})')
"
```

## Dependencies

Requires `youtube-transcript-api` Python package. The fetch script auto-installs it on first run, handling:
- Standard Python environments (`--user` install)
- macOS Homebrew Python (`--break-system-packages` fallback)

Manual install if needed:
```bash
pip3 install --user youtube-transcript-api
# or on macOS with Homebrew Python:
pip3 install --break-system-packages youtube-transcript-api
```
