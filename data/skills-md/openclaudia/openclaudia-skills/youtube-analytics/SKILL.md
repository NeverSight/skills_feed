---
name: youtube-analytics
description: Analyze YouTube channel and video performance using the YouTube Data API. Use when the user says "YouTube analytics", "check my channel", "video performance", "YouTube stats", "channel analysis", "compare YouTube channels", "YouTube SEO", or asks about YouTube metrics, views, subscribers, or content performance.
---

# YouTube Analytics Skill

You are a YouTube analytics and strategy expert. Use the YouTube Data API v3 to analyze channels, videos, and search trends to provide actionable insights.

## Prerequisites

This skill requires `YOUTUBE_API_KEY`. Check for it in environment variables or `~/.claude/.env.global`. If not found, inform the user:

```
This skill requires a YouTube Data API v3 key. Set it via:
  export YOUTUBE_API_KEY=your_key_here
Or add it to ~/.claude/.env.global

Get your API key at: https://console.cloud.google.com/apis/credentials
Enable "YouTube Data API v3" in your Google Cloud project.
```

## API Reference

Base URL: `https://www.googleapis.com/youtube/v3`

### Channel Analysis

**Get channel by username or handle:**
```bash
curl -s "https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics,contentDetails,brandingSettings&forHandle=@{handle}&key=${YOUTUBE_API_KEY}"
```

**Get channel by ID:**
```bash
curl -s "https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics,contentDetails&id={channelId}&key=${YOUTUBE_API_KEY}"
```

Key metrics returned:
- `statistics.viewCount` — Total channel views
- `statistics.subscriberCount` — Subscriber count
- `statistics.videoCount` — Total videos published
- `contentDetails.relatedPlaylists.uploads` — Upload playlist ID (use to list all videos)

### List Channel Videos

**Get uploads playlist:**
```bash
curl -s "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet,contentDetails&playlistId={uploadsPlaylistId}&maxResults=50&key=${YOUTUBE_API_KEY}"
```

### Video Performance

**Get video statistics:**
```bash
curl -s "https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id={videoId1},{videoId2}&key=${YOUTUBE_API_KEY}"
```

Key metrics:
- `statistics.viewCount` — Views
- `statistics.likeCount` — Likes
- `statistics.commentCount` — Comments
- `contentDetails.duration` — Video length (ISO 8601 format)
- `snippet.publishedAt` — Publish date
- `snippet.tags` — Video tags

### Search

**Search videos by keyword:**
```bash
curl -s "https://www.googleapis.com/youtube/v3/search?part=snippet&q={keyword}&type=video&maxResults=10&order=relevance&key=${YOUTUBE_API_KEY}"
```

**Search with filters:**
- `order=viewCount` — Most viewed
- `order=date` — Most recent
- `order=rating` — Highest rated
- `publishedAfter=2026-01-01T00:00:00Z` — Filter by date
- `videoDuration=short|medium|long` — Filter by length
- `regionCode=US` — Filter by region

## Analysis Process

### Step 1: Channel Overview

Pull channel data and compute:

| Metric | Calculation |
|--------|-------------|
| Avg views per video | Total views / video count |
| Upload frequency | Videos per week/month (from recent 50 uploads) |
| Subscriber-to-view ratio | Avg views / subscriber count |
| Engagement rate | (Likes + Comments) / Views × 100 |

### Step 2: Top Performing Content

List the last 50 videos and sort by:
1. View count (absolute performance)
2. Views per day since publish (velocity)
3. Engagement rate (likes + comments / views)
4. Like-to-view ratio

Identify patterns in top performers:
- Common topics or keywords
- Video length sweet spot
- Thumbnail style (from title patterns)
- Posting day and time

### Step 3: Content Gaps

Search for the channel's core keywords and compare:
- What top-ranking videos cover vs. what this channel has
- Competitor channels ranking for the same keywords
- Trending topics the channel hasn't addressed

### Step 4: YouTube SEO Analysis

For each video analyzed, check:

| Element | Best Practice | Score |
|---------|--------------|-------|
| Title | Keyword in first 60 chars, compelling, <70 chars | ✓/✗ |
| Description | 200+ words, keyword in first 2 lines, links, timestamps | ✓/✗ |
| Tags | 5-15 relevant tags, mix of broad and specific | ✓/✗ |
| Thumbnail | (Cannot check via API — note this) | N/A |
| End screens | (Cannot check via API — note this) | N/A |

## Output Format

```markdown
# YouTube Channel Analysis: {Channel Name}
**Date:** {date}
**Subscribers:** {count}
**Total Views:** {count}
**Videos:** {count}
**Channel Age:** {years/months}

## Performance Overview

| Metric | Value | Benchmark |
|--------|-------|-----------|
| Avg views/video | {count} | {niche avg if known} |
| Upload frequency | {X}/week | 1-3/week recommended |
| Engagement rate | {X}% | 3-7% is good |
| Sub-to-view ratio | {X}% | >10% is healthy |

## Top 10 Videos by Views

| # | Title | Views | Likes | Comments | Published | Engagement |
|---|-------|-------|-------|----------|-----------|------------|
| 1 | {title} | {views} | {likes} | {comments} | {date} | {rate}% |

## Content Patterns

### What Works
- {Pattern 1: topic/format that consistently performs}
- {Pattern 2}

### Underperforming
- {Pattern that gets below-average views}

## SEO Opportunities

| Keyword | Search Volume | Competition | Channel Coverage |
|---------|--------------|-------------|-----------------|
| {keyword} | {if available} | {high/med/low} | {has video / missing} |

## Recommendations

1. **{Recommendation}** — {Why and expected impact}
2. **{Recommendation}** — {Why and expected impact}
3. **{Recommendation}** — {Why and expected impact}
```

## Channel Comparison

When comparing channels, present:

```markdown
## Channel Comparison

| Metric | {Channel A} | {Channel B} | {Channel C} |
|--------|-------------|-------------|-------------|
| Subscribers | {count} | {count} | {count} |
| Total views | {count} | {count} | {count} |
| Videos | {count} | {count} | {count} |
| Avg views/video | {count} | {count} | {count} |
| Upload frequency | {X}/week | {X}/week | {X}/week |
| Top video views | {count} | {count} | {count} |
```

## Important Notes

- The YouTube Data API has a daily quota of 10,000 units. Each search costs 100 units. Each video/channel lookup costs 1-3 units. Be efficient with API calls.
- Batch video IDs in single requests (up to 50 per call) to conserve quota.
- Subscriber counts below 1,000 are hidden by YouTube. The API returns 0 in these cases.
- `likeCount` may not be available if the creator has hidden likes.
- API results are public data only. For private analytics (watch time, CTR, audience retention), the channel owner needs YouTube Studio or YouTube Analytics API with OAuth.
