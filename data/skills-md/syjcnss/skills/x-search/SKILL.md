---
name: x-search
description: Search and analyze X/Twitter posts using xAI's Grok API with real-time social media data. Use when the user needs to (1) search X/Twitter for specific topics, keywords, or trends, (2) analyze sentiment or discussions on X, (3) find posts from specific users or time periods, (4) research what people are saying about companies/products/events on X, or (5) gather social media insights from Twitter/X platform.
---

# X Search

Search X (Twitter) posts using xAI's Grok API with keyword search, semantic search, user filtering, and date range capabilities.

## Quick Start

Basic X search:

```bash
scripts/x_search.sh "What are people saying about AI?"
```

## Environment Setup

Required environment variables:
- `XAI_API_KEY`: Your xAI API key (required)
- `XAI_API_HOST`: API host URL (optional, defaults to https://api.x.ai)

## Search Options

### Date Range Filtering

Restrict search to specific time period:

```bash
scripts/x_search.sh "AI developments" --from-date 2025-01-01 --to-date 2025-02-06
```

### User Handle Filtering

Search only specific users (max 10):

```bash
scripts/x_search.sh "latest updates" --allowed-handles elonmusk,gdb
```

Exclude specific users (max 10):

```bash
scripts/x_search.sh "tech news" --excluded-handles spamaccount,bot123
```

Note: Cannot use both `--allowed-handles` and `--excluded-handles` in the same request.

### Media Understanding

Enable image analysis in posts:

```bash
scripts/x_search.sh "AI art trends" --enable-images
```

Enable video analysis in posts:

```bash
scripts/x_search.sh "product demos" --enable-videos
```

### Combined Options

All options can be combined:

```bash
scripts/x_search.sh "climate change discussion" \
  --from-date 2025-01-01 \
  --excluded-handles climateskeptic \
  --enable-images
```

### Enable Reasoning Model

Use `--thinking` flag to switch to the reasoning model for deeper analysis:

```bash
scripts/x_search.sh "complex topic requiring deep analysis" --thinking
```

This uses `grok-4-1-fast-reasoning` instead of the default `grok-4-1-fast-non-reasoning`.

## Output Format

The script automatically parses the JSON response and outputs:
1. **Text content**: Grok's formatted analysis and findings
2. **Citations**: List of X post URLs with reference numbers

Example output:
```
## Response:

[Analysis text with inline citation markers]

## Citations:
[1] https://x.com/i/status/...
[2] https://x.com/i/status/...
```

## Usage Notes

- Default model: `grok-4-1-fast-non-reasoning` for fast search responses
- With `--thinking` flag: `grok-4-1-fast-reasoning` for deeper reasoning
- The script uses curl to query the xAI Responses API endpoint
- Output is automatically parsed with jq for readability
- Date format: ISO8601 (YYYY-MM-DD)
- Handle limits: 10 maximum for allowed/excluded lists
