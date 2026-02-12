---
name: search-x
description: Search X/Twitter in real-time using Grok or X API. Find tweets, trends, and discussions with citations.
homepage: https://docs.x.ai
user-invocable: true
disable-model-invocation: true
triggers:
  - search x
  - search twitter
  - find tweets
  - what's on x about
  - x search
  - twitter search
metadata:
  clawdbot:
    emoji: "🔍"
    primaryEnv: XAI_API_KEY
    requires:
      bins: [node]
      env: [XAI_API_KEY]
---

# Search X

Real-time X/Twitter search with two modes:
1. **xAI Grok** (default) — AI-powered search with x_search tool, up to 30 days
2. **X API** (`--x-api`) — Native X search, up to 7 days, pay-per-use

## Setup

### Option 1: xAI API (default)

```bash
export XAI_API_KEY="xai-YOUR-KEY"
```
Get your key at: https://console.x.ai

### Option 2: X API (native)

```bash
export X_BEARER_TOKEN="YOUR-BEARER-TOKEN"
```
Get your token at: https://console.x.com

**Note:** X API uses pay-per-usage pricing. No subscription needed.

## Commands

### Basic Search (xAI Grok)
```bash
node {baseDir}/scripts/search.js "AI video editing"
```

### Native X API Search
```bash
node {baseDir}/scripts/search.js --x-api "AI video editing"
node {baseDir}/scripts/search.js --x-api --max 50 "trending topic"  # More results
```

### Filter by Time
```bash
node {baseDir}/scripts/search.js --days 7 "breaking news"
node {baseDir}/scripts/search.js --days 1 "trending today"
node {baseDir}/scripts/search.js --x-api --days 7 "news"  # X API max is 7 days
```

### Filter by Handles
```bash
node {baseDir}/scripts/search.js --handles @elonmusk,@OpenAI "AI announcements"
node {baseDir}/scripts/search.js --exclude @bots "real discussions"
```

### Output Options
```bash
node {baseDir}/scripts/search.js --json "topic"        # Full JSON response
node {baseDir}/scripts/search.js --compact "topic"     # Just tweets, no fluff
node {baseDir}/scripts/search.js --links-only "topic"  # Just X links
```

## Example Usage in Chat

**User:** "Search X for what people are saying about Claude Code"
**Action:** Run search with query "Claude Code"

**User:** "Find tweets from @remotion_dev in the last week"
**Action:** Run search with --handles @remotion_dev --days 7

**User:** "What's trending about AI on Twitter today?"
**Action:** Run search with --days 1 "AI trending"

**User:** "Search X for Remotion best practices, last 30 days"
**Action:** Run search with --days 30 "Remotion best practices"

## How It Works

### xAI Grok Mode (default)
Uses xAI's Responses API (`/v1/responses`) with the `x_search` tool:
- Model: `grok-4-1-fast` (optimized for agentic search)
- Up to 30 days of history
- AI-powered result formatting with citations
- Returns real tweets with URLs

### X API Mode (--x-api)
Uses X's native search API (`/2/tweets/search/recent`):
- Up to 7 days of history
- Pay-per-usage pricing (no subscription)
- Raw tweet data with metrics
- Up to 100 results per query

## Response Format

Each result includes:
- **@username** (display name)
- Tweet content
- Date/time
- Engagement metrics (X API mode)
- Direct link to tweet

## Environment Variables

**xAI Mode:**
- `XAI_API_KEY` - Your xAI API key (required for default mode)
- `SEARCH_X_MODEL` - Model override (default: grok-4-1-fast)
- `SEARCH_X_DAYS` - Default days to search (default: 30)

**X API Mode:**
- `X_BEARER_TOKEN` - Your X API Bearer Token
- `TWITTER_BEARER_TOKEN` - Alternative env var name

## Security & Permissions

**What this skill does:**
- Calls xAI's `/v1/responses` endpoint (Grok mode) or X's `/2/tweets/search/recent` endpoint (X API mode)
- Returns public tweet data with URLs and citations
- All requests go only to `api.x.ai` or `api.x.com`

**What this skill does NOT do:**
- Does not post, like, retweet, or modify any X/Twitter content
- Does not access your X/Twitter account or DMs
- Does not read config files or access the local filesystem
- Does not send credentials to any third-party endpoint
- Cannot be invoked autonomously by the agent (`disable-model-invocation: true`)

Review `scripts/search.js` before first use to verify behavior.
