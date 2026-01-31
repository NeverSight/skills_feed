---
name: youtube-harvester
description: Extract transcripts and metadata from YouTube videos
---


# YouTube Harvester Skill

> Extract and ingest YouTube video transcripts into RAG with proper chunking and metadata.

## Overview

YouTube is a rich source of tutorials, lectures, and explanations. This skill covers:
- Transcript extraction (manual and auto-generated)
- Timestamp-aware chunking
- Playlist and channel harvesting
- Metadata enrichment

## Prerequisites

```bash
# Install yt-dlp for video metadata and subtitles
pip install yt-dlp

# Install youtube-transcript-api for cleaner transcript access
pip install youtube-transcript-api

# Optional: for audio transcription fallback
pip install openai-whisper
```

## Extraction Methods

### Method 1: youtube-transcript-api (Recommended)

Best for clean transcript text with timestamps.

```python
#!/usr/bin/env python3
"""Extract YouTube transcripts using youtube-transcript-api."""

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import json
import re
from typing import Dict, List, Optional
from datetime import datetime

def extract_video_id(url: str) -> str:
    """Extract video ID from various YouTube URL formats."""
    patterns = [
        r'(?:v=|/v/|youtu\.be/)([a-zA-Z0-9_-]{11})',
        r'(?:embed/)([a-zA-Z0-9_-]{11})',
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    raise ValueError(f"Could not extract video ID from: {url}")


def get_transcript(video_id: str, languages: List[str] = ['en']) -> List[Dict]:
    """
    Fetch transcript for a video.

    Args:
        video_id: YouTube video ID
        languages: Preferred languages in order

    Returns:
        List of transcript segments with text, start, duration
    """
    try:
        # Try to get manual captions first
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

        try:
            transcript = transcript_list.find_manually_created_transcript(languages)
        except:
            # Fall back to auto-generated
            transcript = transcript_list.find_generated_transcript(languages)

        return transcript.fetch()

    except Exception as e:
        print(f"Error fetching transcript: {e}")
        return []


def format_timestamp(seconds: float) -> str:
    """Convert seconds to HH:MM:SS format."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


def get_video_metadata(video_id: str) -> Dict:
    """Get video metadata using yt-dlp."""
    import subprocess
    import json

    result = subprocess.run(
        ['yt-dlp', '--dump-json', '--no-download', f'https://youtube.com/watch?v={video_id}'],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        data = json.loads(result.stdout)
        return {
            'title': data.get('title'),
            'channel': data.get('channel'),
            'channel_id': data.get('channel_id'),
            'upload_date': data.get('upload_date'),
            'duration': data.get('duration'),
            'view_count': data.get('view_count'),
            'description': data.get('description', '')[:500],  # Truncate
            'tags': data.get('tags', [])[:10],  # Limit tags
        }
    return {}
```

### Method 2: yt-dlp Subtitles

Better for batch processing and when API limits are hit.

```bash
#!/bin/bash
# Extract subtitles using yt-dlp

VIDEO_URL="$1"
OUTPUT_DIR="${2:-.}"

# Download auto-generated subtitles
yt-dlp \
    --write-auto-sub \
    --sub-lang en \
    --sub-format vtt \
    --skip-download \
    --output "$OUTPUT_DIR/%(title)s.%(ext)s" \
    "$VIDEO_URL"

# Convert VTT to plain text
for vtt in "$OUTPUT_DIR"/*.vtt; do
    # Remove VTT formatting, keep just text
    sed -e '/^WEBVTT/d' \
        -e '/^Kind:/d' \
        -e '/^Language:/d' \
        -e '/^[0-9][0-9]:[0-9][0-9]/d' \
        -e '/-->/d' \
        -e 's/<[^>]*>//g' \
        -e '/^$/d' \
        "$vtt" > "${vtt%.vtt}.txt"
done
```

## Chunking Strategies

### Strategy 1: Time-Based Chunks

Split transcript into fixed time intervals.

```python
def chunk_by_time(
    transcript: List[Dict],
    chunk_duration: int = 300  # 5 minutes
) -> List[Dict]:
    """
    Chunk transcript by time intervals.

    Args:
        transcript: List of transcript segments
        chunk_duration: Seconds per chunk
    """
    chunks = []
    current_chunk = {
        'text': '',
        'start': 0,
        'end': 0,
        'segments': []
    }

    for segment in transcript:
        segment_start = segment['start']

        # Check if we need to start a new chunk
        if segment_start >= current_chunk['start'] + chunk_duration:
            if current_chunk['text']:
                chunks.append(current_chunk)

            current_chunk = {
                'text': '',
                'start': segment_start,
                'end': segment_start,
                'segments': []
            }

        current_chunk['text'] += ' ' + segment['text']
        current_chunk['end'] = segment['start'] + segment.get('duration', 0)
        current_chunk['segments'].append(segment)

    # Don't forget the last chunk
    if current_chunk['text']:
        chunks.append(current_chunk)

    return chunks
```

### Strategy 2: Topic-Based Chunks

Split when topic appears to change (silence gaps or topic markers).

```python
def chunk_by_topic(
    transcript: List[Dict],
    gap_threshold: float = 5.0,  # Seconds of silence indicating topic change
    min_chunk_size: int = 100    # Minimum words per chunk
) -> List[Dict]:
    """
    Chunk transcript by topic boundaries.

    Uses gaps in speech and sentence boundaries to identify topic changes.
    """
    chunks = []
    current_chunk = {
        'text': '',
        'start': 0,
        'end': 0,
        'word_count': 0
    }

    prev_end = 0

    for segment in transcript:
        segment_start = segment['start']
        gap = segment_start - prev_end
        word_count = len(segment['text'].split())

        # Check for topic boundary
        is_boundary = (
            gap > gap_threshold and
            current_chunk['word_count'] >= min_chunk_size
        )

        if is_boundary:
            if current_chunk['text']:
                chunks.append(current_chunk)

            current_chunk = {
                'text': '',
                'start': segment_start,
                'end': segment_start,
                'word_count': 0
            }

        current_chunk['text'] += ' ' + segment['text']
        current_chunk['end'] = segment_start + segment.get('duration', 0)
        current_chunk['word_count'] += word_count
        prev_end = current_chunk['end']

    if current_chunk['text']:
        chunks.append(current_chunk)

    return chunks
```

### Strategy 3: Semantic Chunks

Use embeddings to find natural topic boundaries.

```python
def chunk_by_semantics(
    transcript: List[Dict],
    similarity_threshold: float = 0.7,
    window_size: int = 5
) -> List[Dict]:
    """
    Chunk based on semantic similarity between segments.

    Groups semantically similar consecutive segments together.
    """
    from sentence_transformers import SentenceTransformer
    import numpy as np

    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Combine segments into windows for more stable embeddings
    windows = []
    for i in range(0, len(transcript), window_size):
        window_text = ' '.join(
            s['text'] for s in transcript[i:i+window_size]
        )
        windows.append({
            'text': window_text,
            'start': transcript[i]['start'],
            'end': transcript[min(i+window_size-1, len(transcript)-1)]['start'],
            'segments': transcript[i:i+window_size]
        })

    # Get embeddings
    embeddings = model.encode([w['text'] for w in windows])

    # Find boundaries where similarity drops
    chunks = []
    current_chunk = windows[0].copy() if windows else None

    for i in range(1, len(windows)):
        similarity = np.dot(embeddings[i-1], embeddings[i]) / (
            np.linalg.norm(embeddings[i-1]) * np.linalg.norm(embeddings[i])
        )

        if similarity < similarity_threshold:
            # Topic boundary detected
            if current_chunk:
                chunks.append(current_chunk)
            current_chunk = windows[i].copy()
        else:
            # Continue current chunk
            current_chunk['text'] += ' ' + windows[i]['text']
            current_chunk['end'] = windows[i]['end']
            current_chunk['segments'].extend(windows[i]['segments'])

    if current_chunk:
        chunks.append(current_chunk)

    return chunks
```

## Full Harvesting Pipeline

```python
#!/usr/bin/env python3
"""Complete YouTube harvesting pipeline."""

import json
from typing import List, Dict, Optional
from datetime import datetime

async def harvest_youtube_video(
    url: str,
    collection: str,
    chunk_strategy: str = "time",  # time, topic, semantic
    chunk_size: int = 300
) -> Dict:
    """
    Harvest a single YouTube video into RAG.

    Args:
        url: YouTube video URL
        collection: Target RAG collection
        chunk_strategy: How to chunk the transcript
        chunk_size: Size parameter for chunking

    Returns:
        Harvest report
    """
    video_id = extract_video_id(url)

    # Get metadata
    metadata = get_video_metadata(video_id)
    if not metadata:
        return {"status": "error", "error": "Could not fetch metadata"}

    # Get transcript
    transcript = get_transcript(video_id)
    if not transcript:
        return {"status": "error", "error": "No transcript available"}

    # Chunk based on strategy
    if chunk_strategy == "time":
        chunks = chunk_by_time(transcript, chunk_size)
    elif chunk_strategy == "topic":
        chunks = chunk_by_topic(transcript)
    elif chunk_strategy == "semantic":
        chunks = chunk_by_semantics(transcript)
    else:
        chunks = chunk_by_time(transcript, chunk_size)

    # Ingest each chunk
    ingested = 0
    for i, chunk in enumerate(chunks):
        chunk_metadata = {
            "source_type": "youtube",
            "source_url": url,
            "video_id": video_id,
            "title": metadata.get("title"),
            "channel": metadata.get("channel"),
            "upload_date": metadata.get("upload_date"),
            "duration_seconds": metadata.get("duration"),
            "timestamp_start": format_timestamp(chunk["start"]),
            "timestamp_end": format_timestamp(chunk["end"]),
            "chunk_index": i,
            "total_chunks": len(chunks),
            "harvested_at": datetime.now().isoformat()
        }

        await ingest(
            content=chunk["text"].strip(),
            collection=collection,
            metadata=chunk_metadata,
            doc_id=f"yt_{video_id}_chunk_{i}"
        )
        ingested += 1

    return {
        "status": "success",
        "video_id": video_id,
        "title": metadata.get("title"),
        "chunks": ingested,
        "collection": collection
    }


async def harvest_youtube_playlist(
    playlist_url: str,
    collection: str,
    **kwargs
) -> Dict:
    """Harvest all videos in a playlist."""
    import subprocess

    # Get playlist video IDs
    result = subprocess.run(
        ['yt-dlp', '--flat-playlist', '--print', 'id', playlist_url],
        capture_output=True,
        text=True
    )

    video_ids = result.stdout.strip().split('
')

    results = []
    for video_id in video_ids:
        url = f"https://youtube.com/watch?v={video_id}"
        result = await harvest_youtube_video(url, collection, **kwargs)
        results.append(result)

    success = sum(1 for r in results if r.get("status") == "success")

    return {
        "status": "success",
        "videos_processed": len(video_ids),
        "videos_succeeded": success,
        "videos_failed": len(video_ids) - success,
        "details": results
    }


async def harvest_youtube_channel(
    channel_url: str,
    collection: str,
    max_videos: int = 50,
    **kwargs
) -> Dict:
    """Harvest recent videos from a channel."""
    import subprocess

    # Get recent video IDs from channel
    result = subprocess.run(
        ['yt-dlp', '--flat-playlist', '--print', 'id',
         '--playlist-end', str(max_videos), channel_url],
        capture_output=True,
        text=True
    )

    video_ids = result.stdout.strip().split('
')

    results = []
    for video_id in video_ids:
        if video_id:
            url = f"https://youtube.com/watch?v={video_id}"
            result = await harvest_youtube_video(url, collection, **kwargs)
            results.append(result)

    success = sum(1 for r in results if r.get("status") == "success")

    return {
        "status": "success",
        "videos_processed": len(video_ids),
        "videos_succeeded": success,
        "collection": collection
    }
```

## Metadata Schema

```yaml
# YouTube video chunk metadata
source_type: youtube
source_url: https://youtube.com/watch?v=...
video_id: dQw4w9WgXcQ
title: "Video Title"
channel: "Channel Name"
channel_id: UC...
upload_date: "20240101"
duration_seconds: 930
timestamp_start: "05:30"
timestamp_end: "10:00"
chunk_index: 2
total_chunks: 12
harvested_at: "2024-01-01T12:00:00Z"
tags: [tag1, tag2]
```

## Error Handling

| Error | Handling |
|-------|----------|
| No transcript available | Log, skip, note in report |
| Private/deleted video | Skip with error note |
| Age-restricted | May need authentication |
| Rate limited | Back off, retry with delay |
| API quota exceeded | Switch to yt-dlp method |

## Usage Examples

```python
# Single video
result = await harvest_youtube_video(
    url="https://youtube.com/watch?v=VIDEO_ID",
    collection="ml_tutorials",
    chunk_strategy="topic"
)

# Playlist
result = await harvest_youtube_playlist(
    playlist_url="https://youtube.com/playlist?list=PLAYLIST_ID",
    collection="course_lectures",
    chunk_strategy="time",
    chunk_size=600  # 10-minute chunks
)

# Channel (recent videos)
result = await harvest_youtube_channel(
    channel_url="https://youtube.com/@ChannelName",
    collection="channel_content",
    max_videos=20
)
```

## Refinement Notes

> Track improvements as you use this skill.

- [ ] Transcript extraction tested
- [ ] Chunking strategies compared
- [ ] Metadata enrichment working
- [ ] Playlist harvesting tested
- [ ] Channel following implemented
- [ ] Error handling robust
