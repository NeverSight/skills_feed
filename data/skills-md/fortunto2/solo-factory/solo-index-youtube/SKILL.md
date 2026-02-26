---
name: solo-index-youtube
description: Index YouTube channel videos and transcripts for semantic search. Use when user says "index YouTube", "add YouTube channel", "update video index", or "index transcripts". Works with solograph MCP (if available) or standalone via yt-dlp.
license: MIT
metadata:
  author: fortunto2
  version: "2.0.0"
  openclaw:
    emoji: "🎞️"
allowed-tools: Bash, Read, Glob, Grep, Write, AskUserQuestion, mcp__solograph__source_search, mcp__solograph__source_list, mcp__solograph__source_tags, mcp__solograph__source_related
argument-hint: "[channel handles or 'all']"
---

# /index-youtube

Index YouTube video transcripts into a searchable knowledge base. Supports two modes depending on available tools.

## Prerequisites

Check that yt-dlp is available:

```bash
which yt-dlp || echo "MISSING: install yt-dlp (brew install yt-dlp / pip install yt-dlp / pipx install yt-dlp)"
```

## Arguments

Parse `$ARGUMENTS` for channel handles or "all":
- If empty or "all": index all channels (from config or ask user)
- If one or more handles: index only those channels (e.g., `GregIsenberg ycombinator`)
- Optional flags: `-n <limit>` (max videos per channel, default 10), `--dry-run` (parse only)

## Mode Detection

Check which mode is available:

### Mode 1: With solograph MCP (recommended)

If MCP tools `source_search`, `source_list`, `source_tags` are available, use solograph for indexing and search.

**Setup (if not yet installed):**
```bash
# Install solograph
pip install solograph
# or
uvx solograph
```

**Indexing via solograph CLI:**
```bash
# Single channel
solograph-cli index-youtube -c GregIsenberg -n 10

# Multiple channels
solograph-cli index-youtube -c GregIsenberg -c ycombinator -n 10

# All channels (from channels.yaml in solograph config)
solograph-cli index-youtube -n 10

# Dry run (parse only, no DB writes)
solograph-cli index-youtube --dry-run
```

If `solograph-cli` is not on PATH, try:
```bash
uvx solograph-cli index-youtube -c <handle> -n 10
```

**Verification via MCP:**
- `source_list` — check that youtube source appears
- `source_search("startup idea", source="youtube")` — test semantic search
- `source_tags` — see auto-detected topics from transcripts
- `source_related(video_id)` — find related videos by tags

### Mode 2: Without MCP (standalone fallback)

If solograph MCP tools are NOT available, use yt-dlp directly to download transcripts and analyze them.

**Step 1: Download video list**
```bash
# Get recent video URLs from a channel
yt-dlp --flat-playlist --print url "https://www.youtube.com/@GregIsenberg/videos" | head -n 10
```

**Step 2: Download transcripts**
```bash
# Download auto-generated subtitles (no video download)
yt-dlp --write-auto-sub --sub-lang en --skip-download --sub-format vtt \
  -o "docs/youtube/%(channel)s/%(title)s.%(ext)s" \
  "<video-url>"
```

**Step 3: Convert VTT to readable text**
```bash
# Strip VTT formatting (timestamps, positioning)
sed '/^$/d; /^[0-9]/d; /^NOTE/d; /^WEBVTT/d; /-->/d' docs/youtube/channel/video.vtt | \
  awk '!seen[$0]++' > docs/youtube/channel/video.txt
```

**Step 4: Create index**

Read each transcript with the Read tool. For each video, extract:
- Title (from filename or yt-dlp metadata)
- Key topics and insights
- Actionable takeaways
- Timestamps for notable segments (if chapter markers exist)

Write a summary index to `docs/youtube/index.md`:

```markdown
# YouTube Knowledge Index

## Channel: {channel_name}

### {video_title}
- **URL:** {url}
- **Key topics:** {topic1}, {topic2}
- **Insights:** {summary}
- **Actionable:** {takeaway}
```

**Step 5: Search indexed content**

With transcripts saved as text files, use Grep to search:
```bash
# Search across all transcripts
grep -ri "startup idea" docs/youtube/
```

## Output

Report to the user:
1. Number of videos indexed
2. Number of transcripts downloaded (vs skipped — no transcript available)
3. How many had chapter markers
4. Index file location
5. How to search the indexed content (MCP tool or Grep command)

## Common Issues

### "MISSING: install yt-dlp"
**Cause:** yt-dlp not installed.
**Fix:** Run `brew install yt-dlp` (macOS), `pip install yt-dlp`, or `pipx install yt-dlp`.

### Videos skipped (no transcript)
**Cause:** Video has no auto-generated or manual subtitles.
**Fix:** This is expected — some videos lack transcripts. Only videos with available subtitles can be indexed.

### Rate limiting from YouTube
**Cause:** Too many requests in short time.
**Fix:** Reduce `-n` limit, add `--sleep-interval 2` to yt-dlp commands, or use `--cookies-from-browser chrome` for authenticated access.

### solograph-cli not found
**Cause:** solograph not installed or not on PATH.
**Fix:** Install with `pip install solograph` or `uvx solograph`. Check `which solograph-cli`.
