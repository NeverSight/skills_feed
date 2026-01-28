---
name: supadata
description: Supadata API via curl. Use this skill to extract transcripts from YouTube/TikTok/Instagram videos and scrape web content to markdown.
vm0_secrets:
  - SUPADATA_API_KEY
---

# Supadata API

Use the Supadata API via direct `curl` calls to **extract video transcripts** and **scrape web content** for AI applications.

> Official docs: `https://docs.supadata.ai/`

---

## When to Use

Use this skill when you need to:

- **Extract transcripts** from YouTube, TikTok, Instagram, X (Twitter), Facebook videos
- **Scrape web pages** to markdown format for AI processing
- **Get video/channel metadata** from social platforms
- **Crawl websites** to extract content from multiple pages

---

## Prerequisites

1. Sign up at [Supadata Dashboard](https://dash.supadata.ai/)
2. API key is automatically generated on signup (no credit card required)
3. Store your API key in environment variable

```bash
export SUPADATA_API_KEY="your-api-key"
```

### Pricing

- Transcript fetch (existing): 1 credit
- Transcript generation (AI): 2 credits/minute
- Free tier available

---


> **Important:** When using `$VAR` in a command that pipes to another command, wrap the command containing `$VAR` in `bash -c '...'`. Due to a Claude Code bug, environment variables are silently cleared when pipes are used directly.
> ```bash
> bash -c 'curl -s "https://api.example.com" -H "Authorization: Bearer $API_KEY"' | jq .
> ```

## How to Use

All examples below assume you have `SUPADATA_API_KEY` set.

The base URL for the API is:

- `https://api.supadata.ai/v1`

Authentication uses the `x-api-key` header.

---

### 1. Get YouTube Video Transcript

Extract transcript from a YouTube video:

Write to `/tmp/supadata_url.txt`:

```
https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

```bash
bash -c 'curl -s "https://api.supadata.ai/v1/transcript" -H "x-api-key: ${SUPADATA_API_KEY}" -G --data-urlencode "url@/tmp/supadata_url.txt" -d "text=true"'
```

**Parameters:**

- `url`: Video URL (required)
- `text`: Return plain text (`true`) or timestamped chunks (`false`, default)
- `lang`: Preferred language (ISO 639-1 code, e.g., `en`, `zh`)
- `mode`: `native` (existing only), `generate` (AI), `auto` (default)

---

### 2. Get Transcript with Timestamps

Get transcript with timing information:

```bash
bash -c 'curl -s "https://api.supadata.ai/v1/transcript" -H "x-api-key: ${SUPADATA_API_KEY}" -G --data-urlencode "url@/tmp/supadata_url.txt" -d "text=false"' | jq '.content[:3]'
```

Response format:
```json
{
  "content": [
  {"text": "Hello", "offset": 0, "duration": 1500, "lang": "en"}
  ],
  "lang": "en",
  "availableLangs": ["en", "es", "zh"]
}
```

---

### 3. Get TikTok/Instagram/X Transcript

Extract transcript from other platforms:

```bash
# TikTok
bash -c 'curl -s "https://api.supadata.ai/v1/transcript" -H "x-api-key: ${SUPADATA_API_KEY}" -G --data-urlencode "url@/tmp/supadata_url.txt" -d "text=true"'

# Instagram Reel
bash -c 'curl -s "https://api.supadata.ai/v1/transcript" -H "x-api-key: ${SUPADATA_API_KEY}" -G --data-urlencode "url@/tmp/supadata_url.txt" -d "text=true"'
```

Supported platforms: YouTube, TikTok, Instagram, X (Twitter), Facebook

---

### 4. Native Transcript Only (Save Credits)

Fetch only existing transcripts without AI generation:

```bash
bash -c 'curl -s "https://api.supadata.ai/v1/transcript" -H "x-api-key: ${SUPADATA_API_KEY}" -G --data-urlencode "url@/tmp/supadata_url.txt" -d "text=true" -d "mode=native"'
```

Use `mode=native` to avoid AI generation costs (1 credit vs 2 credits/min).

---

### 5. Get YouTube Channel Metadata

Get channel information:

```bash
bash -c 'curl -s "https://api.supadata.ai/v1/youtube/channel" -H "x-api-key: ${SUPADATA_API_KEY}" -G --data-urlencode "id=@mkbhd"' | jq '{name, subscriberCount, videoCount}
```

Accepts channel URL, channel ID, or handle (e.g., `@mkbhd`).

---

### 6. Get YouTube Video Metadata

Get video information:

```bash
bash -c 'curl -s "https://api.supadata.ai/v1/youtube/video" -H "x-api-key: ${SUPADATA_API_KEY}" -G --data-urlencode "url@/tmp/supadata_url.txt"' | jq '{title, viewCount, likeCount, duration}
```

---

### 7. Get Social Media Metadata

Get metadata from any supported platform:

```bash
bash -c 'curl -s "https://api.supadata.ai/v1/metadata" -H "x-api-key: ${SUPADATA_API_KEY}" -G --data-urlencode "url@/tmp/supadata_url.txt"'
```

Works with YouTube, TikTok, Instagram, X, Facebook posts.

---

### 8. Scrape Web Page to Markdown

Extract web page content:

```bash
bash -c 'curl -s "https://api.supadata.ai/v1/web/scrape" -H "x-api-key: ${SUPADATA_API_KEY}" -G --data-urlencode "url@/tmp/supadata_url.txt"'
```

Returns page content in Markdown format, ideal for AI processing.

---

### 9. Map Website Links

Get all links from a website:

```bash
bash -c 'curl -s "https://api.supadata.ai/v1/web/map" -H "x-api-key: ${SUPADATA_API_KEY}" -G --data-urlencode "url@/tmp/supadata_url.txt"' | jq '.urls[:10]'
```

---

### 10. Crawl Website (Async)

Start a crawl job for multiple pages.

Write to `/tmp/supadata_request.json`:

```json
{
  "url": "https://example.com",
  "maxPages": 10
}
```

Then run:

```bash
# Start crawl
JOB_ID="$(bash -c 'curl -s "https://api.supadata.ai/v1/web/crawl" -X POST -H "x-api-key: ${SUPADATA_API_KEY}" -H "Content-Type: application/json" -d @/tmp/supadata_request.json' | jq -r '.jobId')"

echo "Job ID: ${JOB_ID}"

# Check status
bash -c 'curl -s "https://api.supadata.ai/v1/web/crawl/<your-job-id>" -H "x-api-key: ${SUPADATA_API_KEY}"' | jq '{status, pagesCompleted}'
```

Status values: `queued`, `active`, `completed`, `failed`

---

### 11. Translate Transcript

Translate a YouTube transcript to another language:

```bash
bash -c 'curl -s "https://api.supadata.ai/v1/youtube/transcript/translate" -H "x-api-key: ${SUPADATA_API_KEY}" -G --data-urlencode "url@/tmp/supadata_url.txt" -d "lang=zh" -d "text=true"'
```

---

## Response Handling

**Synchronous (HTTP 200):** Direct result returned.

**Asynchronous (HTTP 202):** Returns `jobId` for polling:
```json
{"jobId": "abc123"}
```

Poll the job endpoint until status is `completed`.

---

## Guidelines

1. **Use `mode=native` to save credits**: Only fetches existing transcripts
2. **URL encode parameters**: Use `--data-urlencode` for URLs
3. **Check available languages**: Response includes `availableLangs` array
4. **Handle async responses**: Some requests return job IDs for polling
5. **Max file size**: 1GB for direct file URLs
6. **Supported formats**: MP4, WEBM, MP3, FLAC, MPEG, M4A, OGG, WAV
