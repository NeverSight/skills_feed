---
name: video-highlight-extraction
description: Extract highlights, best moments, and key clips from long videos using each::sense AI. Perfect for gaming highlights, sports clips, podcast moments, webinar summaries, meeting recaps, and auto-trailer generation.
metadata:
  author: eachlabs
  version: "1.0"
---

# Video Highlight Extraction

Extract the best moments and highlights from long-form video content using each::sense. This skill intelligently analyzes videos to identify and extract compelling clips, action sequences, emotional peaks, and key moments.

## Features

- **Smart Detection**: AI-powered analysis to find the most engaging moments
- **Gaming Highlights**: Extract kills, wins, clutch plays, and epic moments
- **Sports Clips**: Capture goals, touchdowns, dunks, and pivotal plays
- **Podcast Moments**: Find quotable segments and viral-worthy clips
- **Webinar Summaries**: Extract key points and actionable insights
- **Meeting Highlights**: Summarize decisions, action items, and key discussions
- **Event Highlights**: Concert peaks, wedding moments, travel adventures
- **Trailer Generation**: Auto-generate trailers from full-length content

## Quick Start

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Extract the 5 best highlight moments from this gaming video, focus on action sequences and wins",
    "mode": "max",
    "video_urls": ["https://example.com/gameplay-session.mp4"]
  }'
```

## Highlight Types & Use Cases

| Content Type | Focus Areas | Output Format |
|--------------|-------------|---------------|
| Gaming | Kills, wins, fails, reactions | Short clips (15-60s) |
| Sports | Scores, plays, celebrations | Highlight reel (30-90s) |
| Podcasts | Quotes, insights, debates | Clip compilations (30-120s) |
| Webinars | Key points, demos, Q&A | Summary clips (60-180s) |
| Meetings | Decisions, action items | Condensed recap (2-5min) |
| Concerts | Peaks, crowd moments | Best-of compilation |
| Weddings | Ceremony, reactions, speeches | Highlight reel |
| Travel | Scenic views, activities | Adventure montage |

## Use Case Examples

### 1. Extract Best Moments from Long Video

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Analyze this 2-hour video and extract the top 10 most engaging moments. Look for emotional peaks, funny moments, and visually impressive scenes. Create individual clips of 30-60 seconds each.",
    "mode": "max",
    "video_urls": ["https://example.com/long-form-content.mp4"]
  }'
```

### 2. Gaming Highlight Detection

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Extract gaming highlights from this Valorant stream. Find all clutch rounds, ace plays, and epic kills. Create a highlight reel with smooth transitions between clips.",
    "mode": "max",
    "video_urls": ["https://example.com/valorant-stream.mp4"]
  }'
```

### 3. Sports Highlight Extraction

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a sports highlight reel from this football game. Extract all touchdowns, big plays, interceptions, and celebration moments. Include 2 seconds before and after each key moment for context.",
    "mode": "max",
    "video_urls": ["https://example.com/football-game.mp4"]
  }'
```

### 4. Podcast Best Clips

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Find the most shareable clips from this podcast episode. Look for controversial takes, insightful moments, funny exchanges, and quotable statements. Extract 5-8 clips optimized for social media (under 60 seconds each).",
    "mode": "max",
    "video_urls": ["https://example.com/podcast-episode.mp4"]
  }'
```

### 5. Webinar Key Moments

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Extract key moments from this 90-minute webinar. Identify main talking points, important demonstrations, audience questions, and actionable takeaways. Create a 5-minute summary highlight reel.",
    "mode": "max",
    "video_urls": ["https://example.com/webinar-recording.mp4"]
  }'
```

### 6. Meeting Highlights

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a meeting highlight summary from this team call. Extract all decisions made, action items assigned, key discussion points, and any important announcements. Condense into a 3-minute recap video.",
    "mode": "eco",
    "video_urls": ["https://example.com/team-meeting.mp4"]
  }'
```

### 7. Concert Best Moments

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Extract the best moments from this concert recording. Find crowd singalongs, guitar solos, drum fills, artist interactions with crowd, and emotional peaks. Create a 4-minute highlight compilation with the most energetic parts.",
    "mode": "max",
    "video_urls": ["https://example.com/concert-full.mp4"]
  }'
```

### 8. Travel Video Highlights

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a travel highlight reel from my vacation footage. Extract the most scenic views, exciting activities, local food experiences, and memorable moments. Make a 2-minute shareable video with dynamic pacing.",
    "mode": "max",
    "video_urls": ["https://example.com/vacation-footage.mp4"]
  }'
```

### 9. Wedding Highlight Reel

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a wedding highlight reel from the full ceremony and reception footage. Extract the vows, first kiss, first dance, cake cutting, bouquet toss, speeches with emotional reactions, and candid guest moments. Create a 5-minute cinematic highlight video.",
    "mode": "max",
    "video_urls": ["https://example.com/wedding-full.mp4"]
  }'
```

### 10. Auto-Generate Trailer from Movie

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate a 2-minute trailer from this feature film. Select the most dramatic moments, action sequences, emotional beats, and visually stunning shots. Build tension with the pacing - start slow, build to climax. Avoid major spoilers but hint at the story.",
    "mode": "max",
    "video_urls": ["https://example.com/feature-film.mp4"]
  }'
```

## Mode Selection

Ask your users before processing:

**"Do you want fast & cheap, or high quality?"**

| Mode | Best For | Speed | Quality |
|------|----------|-------|---------|
| `max` | Final highlight reels, client deliverables, trailer cuts | Slower | Highest |
| `eco` | Quick previews, meeting recaps, internal reviews | Faster | Good |

## Multi-Turn Highlight Refinement

Use `session_id` to iterate on extracted highlights:

```bash
# Initial extraction
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Extract highlights from this gaming stream, focus on the best plays",
    "session_id": "highlight-project-001",
    "video_urls": ["https://example.com/stream.mp4"]
  }'

# Refine selection
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Remove the third clip and find more moments with team fights",
    "session_id": "highlight-project-001"
  }'

# Adjust timing
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Make each clip shorter, around 15-20 seconds, and add transitions between them",
    "session_id": "highlight-project-001"
  }'
```

## Platform-Optimized Clips

Generate highlights optimized for different platforms:

```bash
# YouTube Shorts / TikTok (vertical 9:16)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Extract viral-worthy moments and format them as vertical 9:16 clips for TikTok/YouTube Shorts. Each clip should be 15-30 seconds with a strong hook in the first 2 seconds.",
    "mode": "max",
    "video_urls": ["https://example.com/content.mp4"]
  }'

# Twitter/X (square 1:1)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create square 1:1 highlight clips optimized for Twitter. Under 2 minutes each, punchy and shareable.",
    "mode": "max",
    "video_urls": ["https://example.com/content.mp4"]
  }'
```

## Highlight Detection Parameters

Customize what the AI looks for:

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Extract highlights with the following criteria: prioritize moments with high audio energy (cheering, music peaks), visual motion (fast action, camera movement), and emotional expressions (laughter, surprise). Skip any slow or static segments. Create 8 clips of 20-40 seconds each.",
    "mode": "max",
    "video_urls": ["https://example.com/event-footage.mp4"]
  }'
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | Insufficient balance | Top up at eachlabs.ai |
| `Video too long` | Exceeds processing limits | Split into smaller segments |
| `Unsupported format` | Video codec not supported | Convert to MP4 H.264 |
| Timeout | Long video processing | Set client timeout to minimum 10 minutes |

**Important:** Video highlight extraction can take significant time for long videos. Always set your HTTP client timeout to at least 10 minutes to avoid premature disconnection.

## Best Practices

### Input Video
- **Format**: MP4 with H.264 codec works best
- **Quality**: Higher resolution enables better moment detection
- **Length**: For videos over 2 hours, consider processing in segments

### Prompt Tips
- Specify the number of highlights you want
- Describe the types of moments to look for
- Mention desired clip length
- Indicate output format requirements (aspect ratio, duration)

### Output Optimization
- Use `max` mode for final deliverables
- Use `eco` mode for quick previews and iteration
- Leverage `session_id` for multi-turn refinement

## Related Skills

- `each-sense` - Core API documentation
- `video-generation` - Generate new video content
- `video-edit` - Edit and modify existing videos
