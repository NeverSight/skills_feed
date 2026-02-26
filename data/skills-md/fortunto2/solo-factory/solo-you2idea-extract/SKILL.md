---
name: solo-you2idea-extract
description: Extract startup ideas from YouTube videos via solograph MCP — index, search, and analyze video transcripts for business ideas. Multi-MCP coordination pattern (YouTube source → analysis → storage). Use when user says "extract ideas from YouTube", "index YouTube video", "find startup ideas in video", "analyze YouTube for ideas", or "what ideas are in this video". Do NOT use for general YouTube watching (no skill needed) or content creation (use /content-gen).
license: MIT
metadata:
  author: fortunto2
  version: "2.0.0"
  openclaw:
    emoji: "💡"
allowed-tools: Read, Grep, Bash, Glob, Write, Edit, AskUserQuestion, mcp__solograph__source_search, mcp__solograph__source_list, mcp__solograph__source_tags, mcp__solograph__source_related, mcp__solograph__kb_search, mcp__solograph__web_search
argument-hint: "[video-url or channel-name or 'analyze <query>']"
---

# /you2idea-extract

Extract startup ideas from YouTube videos. Two operating modes depending on available tools.

## Mode Detection

Check which tools are available:
- **With solograph MCP**: use `source_search`, `source_list`, `source_tags`, `source_related` for indexed corpus
- **Without MCP (standalone)**: use yt-dlp + Read for transcript analysis

## MCP Tools (if available)

- `source_search(query, source="youtube")` — semantic search over indexed videos
- `source_list()` — check indexed video counts
- `source_tags()` — auto-detected topics with confidence scores
- `source_related(video_url)` — find related videos by shared tags
- `kb_search(query)` — cross-reference with knowledge base
- `web_search(query)` — discover new videos to index

## Steps

### Mode 1: Index + Analyze (with solograph MCP)

1. **Parse input** from `$ARGUMENTS`:
   - URL (`https://youtube.com/watch?v=...`) → single video index
   - Channel name (`GregIsenberg`) → channel batch index
   - Query text → search existing corpus (skip to step 4)
   - If empty, ask: "Video URL, channel name, or search query?"

2. **Index video(s)** via solograph:
   ```bash
   # Install if needed
   pip install solograph  # or: uvx solograph

   # Single video
   solograph-cli index-youtube -u "$URL"

   # Channel batch (needs web search for discovery)
   solograph-cli index-youtube -c "$CHANNEL" -n 5
   ```

3. **Verify indexing** — `source_list()` to confirm new video count. `source_tags()` for topic distribution.

4. **Search corpus** — `source_search(query="startup ideas", source="youtube")`.

5. **Cross-reference** — `kb_search(query)` for related existing opportunities (if knowledge base available).

6. **Extract insights** — for each relevant video chunk:
   - Identify the startup idea mentioned
   - Note timestamp and speaker context
   - Rate idea potential (specificity, market evidence, feasibility)
   - Flag ideas that match trends or validated patterns

7. **Write results** to `docs/youtube-ideas.md` or print summary.

### Mode 2: Standalone (without MCP)

1. **Parse input** — same as Mode 1 step 1.

2. **Download transcript** via yt-dlp:
   ```bash
   # Check yt-dlp is available
   command -v yt-dlp >/dev/null 2>&1 && echo "yt-dlp: ok" || echo "Install: pip install yt-dlp"

   # Download subtitles only (no video)
   yt-dlp --write-auto-sub --sub-lang en --skip-download -o "transcript" "$URL"

   # Convert VTT to plain text
   sed '/^$/d; /^[0-9]/d; /-->/d; /WEBVTT/d; /Kind:/d; /Language:/d' transcript.en.vtt | sort -u > transcript.txt
   ```

3. **Read transcript** — Read the transcript.txt file.

4. **Analyze for startup ideas:**
   - Scan for business opportunities, pain points, product ideas
   - Note approximate timestamps from VTT cues
   - Rate each idea on specificity and market potential
   - Cross-reference with WebSearch for market validation

5. **For channel analysis** — download multiple video transcripts:
   ```bash
   # Get video list from channel
   yt-dlp --flat-playlist --print "%(id)s %(title)s" "https://youtube.com/@$CHANNEL" | head -10

   # Download transcripts for top videos
   for id in $VIDEO_IDS; do
     yt-dlp --write-auto-sub --sub-lang en --skip-download -o "transcripts/%(id)s" "https://youtube.com/watch?v=$id"
   done
   ```

6. **Write results** to `docs/youtube-ideas.md` with format:
   ```markdown
   # YouTube Ideas — [Channel/Video]
   Date: YYYY-MM-DD

   ## Idea 1: [Name]
   - **Source:** [Video title] @ [timestamp]
   - **Problem:** [What pain point]
   - **Solution:** [What they propose]
   - **Market signal:** [Evidence of demand]
   - **Potential:** [High/Medium/Low] — [why]

   ## Idea 2: ...
   ```

## Common Issues

### yt-dlp not found
**Fix:** `pip install yt-dlp` or `brew install yt-dlp`

### No subtitles available
**Cause:** Video has no auto-generated or manual captions.
**Fix:** Try `--sub-lang en,ru` for multiple languages. Some videos only have auto-generated subs.

### solograph MCP not available
**Fix:** Skills work in standalone mode (yt-dlp + Read). For indexed search across many videos, install solograph: `pip install solograph`. For enhanced web search, set up [SearXNG](https://github.com/fortunto2/searxng-docker-tavily-adapter) (private, self-hosted, free).

### Too many ideas, hard to prioritize
**Fix:** Use `/validate` on the top 3 ideas to score them through STREAM framework.
