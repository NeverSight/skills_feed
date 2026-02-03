---
name: youtube-transcript-summarizer
description: Extract YouTube video transcripts and generate AI-powered summaries in any language. Converts videos to structured markdown documents with summaries, key points, and timelines.
allowed-tools:
  - Read
  - Write
  - Bash
  - Glob
license: MIT
---

# YouTube Transcript Summarizer

Extract transcripts from YouTube videos and generate AI-powered summaries. Supports any source language and can output summaries in your preferred language.

## Requirements

```bash
pip install -r requirements.txt
# or: pip install youtube-transcript-api anthropic
```

- **ANTHROPIC_API_KEY** env var required for AI summarization
- **yt-dlp** (optional) for automatic video title fetching
- Python 3.7+

Cost depends on transcript length and current Claude API pricing.

## Usage

```bash
# Single video (default: English -> Korean)
python youtube_transcript_summarizer.py "https://www.youtube.com/watch?v=VIDEO_ID"

# Transcript only (no AI summary)
python youtube_transcript_summarizer.py "VIDEO_URL" --no-summary

# Japanese video with English summary
python youtube_transcript_summarizer.py "VIDEO_URL" --source-lang ja --target-lang en

# Auto-detect source language
python youtube_transcript_summarizer.py "VIDEO_URL" --source-lang auto --target-lang fr

# Batch processing
python youtube_transcript_summarizer.py --batch "urls.txt" --output-dir "summaries"

# Custom model and transcript limit
python youtube_transcript_summarizer.py "VIDEO_URL" --model claude-sonnet-4-5-20250929 --max-transcript-chars 30000
```

## CLI Options

| Option | Description | Default |
|--------|-------------|---------|
| `--title` | Custom video title | Auto-fetched via yt-dlp |
| `--source-lang` | Source transcript language | `en` |
| `--target-lang` | Output summary language | `ko` |
| `--output-dir` | Output directory | `outputs/summaries` |
| `--batch FILE` | Process multiple URLs from file | - |
| `--timeline-interval` | Timeline interval (minutes) | `5` |
| `--no-summary` | Skip AI summary | `false` |
| `--api-key` | Claude API key | `ANTHROPIC_API_KEY` env |
| `--model` | Claude model name | `claude-sonnet-4-5-20250929` |
| `--max-transcript-chars` | Max chars sent to Claude | `15000` |

## Supported Languages

`en`, `ko`, `ja`, `zh`, `es`, `fr`, `de`, `pt`, `ru`, `ar`, `hi`, `auto`

## Output Format

Files are named `YYYY-MM-DD VideoTitle.md` with YAML frontmatter:

```yaml
---
title: "Video Title"
source: "https://www.youtube.com/watch?v=ID"
created: YYYY-MM-DD HH:MM:SS
tags:
  - youtube-transcript
video_id: "ID"
source_lang: "en"
target_lang: "ko"
---
```

Sections: Summary, Key Points, Main Content, Timeline, Full Transcript.

## Claude Code Integration

```
Summarize this YouTube video: https://www.youtube.com/watch?v=VIDEO_ID
```
