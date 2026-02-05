---
name: rss-aggregator
description: Aggregates and summarizes recent updates from a predefined list of RSS feeds. Use when the user asks for "recent updates", "what's new", or "RSS updates" within a specific timeframe.
---

# RSS Aggregator

This skill fetches and aggregates the latest updates from a curated list of RSS feeds defined in `references/feeds.opml`.

## Usage

When the user asks for updates (e.g., "recent updates", "last 3 days", "what's new"), use the `scripts/aggregate.py` script.

### Command

```bash
uv run --with feedparser scripts/aggregate.py --days <number_of_days>
```

If the user doesn't specify a timeframe, default to 3 days.

### Output

The script outputs a list of updates in the following format:
- Title
- Author
- Summary (300 characters)
- Update Time
- Link

## Configuration

The list of feeds is stored in `references/feeds.opml`.
