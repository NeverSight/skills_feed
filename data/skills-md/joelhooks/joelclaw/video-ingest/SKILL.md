---
name: video-ingest
description: "Download, transcribe, and summarize videos via the Inngest pipeline. Use when the user asks to grab/download/transcribe/ingest a video, save a YouTube video, or process any video URL. Also handles batch ingest of multiple URLs. This skill triggers the durable Inngest workflow — do NOT run yt-dlp, mlx-whisper, or scp manually."
---

# Video Ingest — via Inngest Pipeline

Videos are ingested through the Inngest event bus. **Do not run yt-dlp, mlx-whisper, scp, or create vault notes manually.** The pipeline handles everything: download → NAS transfer → transcription → vault note → summary enrichment.

## Quick Start

```bash
joelclaw send pipeline/video.download -d '{"url":"URL_HERE"}'
```

That's it. The event chain handles the rest.

Alternative (raw curl):

```bash
curl -s -X POST "http://localhost:8288/e/37aa349b89692d657d276a40e0e47a15" \
  -H "Content-Type: application/json" \
  -d '{"name":"pipeline/video.download","data":{"url":"URL_HERE"}}'
```

## Pipeline Flow

```
pipeline/video.download        — you send this
    ↓
video-download function        — yt-dlp → /tmp → NAS transfer
    ↓ emits
pipeline/video.downloaded      — logged by system-logger
pipeline/transcript.process    — auto-triggered
    ↓
transcript-process function    — mlx-whisper (M4 Pro, ~5min/hr of video)
    ↓ emits
pipeline/transcript.processed  — logged
content/summarize              — auto-triggered
    ↓
content-summarize function     — pi enrichment → vault note with summary
    ↓ emits
content/summarized             — logged, done
```

## Before Sending: Health Check

Always verify the pipeline is healthy before sending events:

```bash
# Inngest server
curl -s http://localhost:8288/health

# Worker (should show functions including video-download)
curl -s http://localhost:3111/ | python3 -c "
import json,sys
d=json.load(sys.stdin)
fns = [f.get('id','?') for f in d.get('functions',[])]
print(f'Worker OK — {len(fns)} functions: {', '.join(fns)}')
"

# Docker container running
docker ps --filter ancestor=inngest/inngest --format "table {{.Status}}\t{{.Ports}}"
```

If the worker is down:
```bash
kubectl -n joelclaw rollout restart deployment/system-bus-worker
kubectl -n joelclaw rollout status deployment/system-bus-worker --timeout=180s
joelclaw refresh
```

## Monitoring a Run

### Watch progress in real-time

```bash
# Worker logs — shows step execution + failures
kubectl logs -n joelclaw deploy/system-bus-worker -f

# Docker logs — shows event dispatch
docker logs -f $(docker ps -q --filter ancestor=inngest/inngest) 2>&1 | grep -v DEBUG
```

### Check if events fired

```bash
# Look for the video's events in Docker logs
docker logs $(docker ps -q --filter ancestor=inngest/inngest) 2>&1 | grep -i "video\|transcript\|summarize" | tail -20
```

### Dashboard

Open http://localhost:8288 in browser — shows functions, events, runs with per-step traces.

### Verify completion

```bash
# Check if vault note was created
ls -la ~/Vault/Resources/videos/*SLUG*

# Check system log for pipeline entries
tail -10 ~/Vault/system/system-log.jsonl | grep -i video
```

## Batch Ingest

Send multiple events. Inngest queues and processes them with concurrency control:

```bash
joelclaw send pipeline/video.download -d '{"url":"https://youtube.com/watch?v=XXXX"}'
joelclaw send pipeline/video.download -d '{"url":"https://youtube.com/watch?v=YYYY"}'
joelclaw send pipeline/video.download -d '{"url":"https://youtube.com/watch?v=ZZZZ"}'
```

## Manual Transcript (Non-YouTube)

For audio files already on disk, or raw text from Granola/Fathom:

```bash
# From audio file
joelclaw send pipeline/transcript.process -d '{"source":"manual","audioPath":"/path/to/audio.mp4","title":"Recording Title","slug":"recording-title"}'

# From raw text (Granola, Fathom, etc.)
joelclaw send pipeline/transcript.process -d '{"source":"granola","text":"transcript text...","title":"Meeting Title","slug":"meeting-title"}'
```

## Re-run Summary Only

If the vault note exists but needs a better summary:

```bash
joelclaw send content/summarize -d '{"vaultPath":"/Users/joel/Vault/Resources/videos/SLUG.md"}'
```

## Options

| Field | Default | Description |
|-------|---------|-------------|
| `url` | required | YouTube or video URL |
| `maxQuality` | `"1080"` | Max video resolution: `"720"`, `"1080"`, `"4k"` |

## Where Things End Up

| What | Location |
|------|----------|
| Video + metadata | NAS: `/volume1/home/joel/video/YYYY/SLUG/` |
| Vault note | `~/Vault/Resources/videos/SLUG.md` |
| Daily note link | `~/Vault/Daily/YYYY-MM-DD.md` under `## Videos` |
| System log entry | `~/Vault/system/system-log.jsonl` |

## Troubleshooting

If events are accepted (200 OK) but nothing happens:

1. **Check Docker→worker connectivity** — the most common issue:
   ```bash
   docker logs $(docker ps -q --filter ancestor=inngest/inngest) 2>&1 | grep -E "ERROR|Unable" | tail -5
   ```
   If you see "Unable to reach SDK URL" → see the inngest skill's serveHost gotcha.

2. **Check worker is actually running**:
   ```bash
   kubectl get deploy -n joelclaw system-bus-worker
   kubectl get pods -n joelclaw -l app=system-bus-worker
   ```

3. **Check worker errors for the specific function**:
   ```bash
   kubectl logs -n joelclaw deploy/system-bus-worker --tail=80
   ```

4. **Use inngest-debug skill** for deep inspection of specific run IDs via GraphQL.

## What NOT to Do

- ❌ Don't run `yt-dlp` directly — the pipeline handles download + NAS transfer
- ❌ Don't run `mlx_whisper` directly — the pipeline handles transcription
- ❌ Don't `scp` to NAS manually — the pipeline handles transfer
- ❌ Don't create vault notes manually — the pipeline creates them with proper frontmatter
- ❌ Don't use codex/background tasks for video processing — Inngest is durable and has retries
