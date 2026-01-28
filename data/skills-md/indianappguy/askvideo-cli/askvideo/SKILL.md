---
name: askvideo
description: Chat with any YouTube video using AI. Use this skill when users share YouTube URLs and want summaries, answers, or information extracted from video content. Triggers on YouTube links, video summarization requests, or questions about video tutorials.
license: MIT
metadata:
  author: IndianAppGuy
  version: "1.0.5"
---

# AskVideo - Chat with YouTube Videos

Get information, summaries, and answers from any YouTube video using AI.

## When to Use This Skill

Use this skill when:
- User shares a YouTube URL and asks questions about it
- User wants to summarize a YouTube video
- User asks "what's in this video?"
- User wants to extract information from video content
- User needs to understand a tutorial, lecture, or presentation
- User asks about timestamps or specific topics in a video

**Keywords:** YouTube, video summary, video transcript, explain video, what's in this video, video content, video tutorial

## Prerequisites

The `askvideo` CLI must be installed and authenticated:

```bash
# Check if installed
which askvideo

# If not installed
npm install -g askvideo

# Authenticate (first time only - requires user's email)
askvideo login
```

## Commands

### Ask a Single Question (Recommended for Agents)

Use `--simple` flag for clean, non-streaming output:

```bash
askvideo ask "<question>" --url "<youtube-url>" --simple
```

**Examples:**
```bash
# Get a summary
askvideo ask "Summarize this video in 3 bullet points" --url "https://youtube.com/watch?v=VIDEO_ID" --simple

# Ask specific questions
askvideo ask "What are the main topics covered?" --url "https://youtube.com/watch?v=VIDEO_ID" --simple

# Extract information
askvideo ask "List all the tools mentioned in this video" --url "https://youtube.com/watch?v=VIDEO_ID" --simple

# Get timestamps
askvideo ask "At what timestamp do they discuss pricing?" --url "https://youtube.com/watch?v=VIDEO_ID" --simple
```

### Ask About an Already-Indexed Video

If the video was previously processed, use the video ID for faster responses:

```bash
askvideo ask "<question>" --id <video-id> --simple
```

### List User's Indexed Videos

```bash
askvideo videos
```

### Check Credits

```bash
askvideo credits
```

## Workflow for Agents

1. **When user shares a YouTube URL with a question:**
   ```bash
   askvideo ask "<user's question>" --url "<url>" --simple
   ```

2. **For multiple questions about the same video:**
   - First query will index the video (takes 30-60 seconds)
   - Subsequent queries are instant
   - Use `--id` flag if you have the video ID

3. **If credits are exhausted:**
   - Run `askvideo credits` to check remaining credits
   - Inform user they need to upgrade at https://askvideo.ai/pricing

## Response Format

The CLI returns plain text answers. Present them to the user in a clear format:

```
Based on the video:

[AI response from askvideo]
```

## Error Handling

| Error | Solution |
|-------|----------|
| "Authentication required" | Run `askvideo login` |
| "No video credits remaining" | User needs to upgrade plan |
| "No message credits remaining" | User needs to upgrade plan |
| "Failed to fetch transcript" | Video may not have captions |

## Supported Video Types

- Standard YouTube videos with captions/transcripts
- YouTube Shorts
- Unlisted videos (if URL is provided)

## Limitations

- Requires video to have a transcript (auto-generated or manual captions)
- Free plan: 1 video + 10 messages per month
- Video processing takes 30-60 seconds on first query

## Examples for Common Tasks

### Summarize a Video
```bash
askvideo ask "Give me a comprehensive summary of this video with key takeaways" --url "URL" --simple
```

### Explain a Tutorial
```bash
askvideo ask "Explain the step-by-step process shown in this tutorial" --url "URL" --simple
```

### Extract Code/Commands
```bash
askvideo ask "List all the code snippets or commands mentioned in this video" --url "URL" --simple
```

### Find Specific Information
```bash
askvideo ask "What does the speaker say about [topic]?" --url "URL" --simple
```

### Get Video Outline
```bash
askvideo ask "Create an outline of all topics covered with timestamps if mentioned" --url "URL" --simple
```

## Links

- Website: https://askvideo.ai
- npm Package: https://npmjs.com/package/askvideo
- Support: https://askvideo.ai/support
