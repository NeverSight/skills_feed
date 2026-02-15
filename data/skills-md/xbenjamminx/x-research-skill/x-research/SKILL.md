---
name: x-research
description: >
  X/Twitter research agent powered by Composio (zero API cost).
  Searches X for real-time perspectives, discussions, product feedback,
  breaking news, and expert opinions. Supports reply monitoring,
  profile analysis, thread following, and watchlist tracking.
  Use when: (1) user says "x research", "search x for", "search twitter for",
  "what are people saying about", "check x for", "x search",
  "/x-research", (2) user wants to find replies, mentions, or engagement data,
  (3) user wants to monitor specific accounts or topics.
  NOT for: posting tweets (use cortana-post.py), account management.
---

# X Research

Agentic research over X/Twitter via Composio. Search, follow threads, deep-dive profiles, monitor accounts -- all at zero API cost.

## CLI Tool

All commands run from this skill directory:

```bash
cd ~/clawd/skills/x-research
```

### Search

```bash
bun run x-search.ts search "<query>" [options]
```

**Options:**
- `--sort likes|impressions|retweets|recent` -- sort order (default: likes)
- `--since 1h|3h|12h|1d|7d` -- time filter (default: last 7 days)
- `--min-likes N` -- filter by minimum likes
- `--min-impressions N` -- filter by minimum impressions
- `--pages N` -- pages to fetch, 1-5 (default: 1, 100 tweets/page)
- `--limit N` -- max results to display (default: 15)
- `--no-replies` -- exclude replies
- `--save` -- save results to `~/clawd/drafts/x-research-{slug}-{date}.md`
- `--json` -- raw JSON output
- `--markdown` -- markdown output for research docs

**Examples:**
```bash
bun run x-search.ts search "to:xBenJamminx" --sort likes --since 1d
bun run x-search.ts search "from:xBenJamminx" --sort recent
bun run x-search.ts search "(claude code OR cursor) automation" --pages 2 --save
bun run x-search.ts search "@CortanaOps" --min-likes 5
```

### Profile

```bash
bun run x-search.ts profile <username> [--count N] [--replies] [--json]
```

Fetches recent tweets from a specific user (excludes replies by default).

### Thread

```bash
bun run x-search.ts thread <tweet_id> [--pages N]
```

Fetches full conversation thread by root tweet ID.

### Single Tweet

```bash
bun run x-search.ts tweet <tweet_id> [--json]
```

### Watchlist

```bash
bun run x-search.ts watchlist                       # Show all
bun run x-search.ts watchlist add <user> [note]     # Add account
bun run x-search.ts watchlist remove <user>          # Remove account
bun run x-search.ts watchlist check                  # Check recent from all
```

Watchlist stored in `data/watchlist.json`.

### Cache

```bash
bun run x-search.ts cache clear    # Clear all cached results
```

15-minute TTL. Avoids re-fetching identical queries.

## Research Loop (Agentic)

When doing deep research (not just a quick search), follow this loop:

### 1. Decompose the Question into Queries

Turn the research question into 3-5 keyword queries using X search operators:

- **Core query**: Direct keywords for the topic
- **Expert voices**: `from:` specific known experts
- **Pain points**: Keywords like `(broken OR bug OR issue OR migration)`
- **Positive signal**: Keywords like `(shipped OR love OR fast OR benchmark)`
- **Links**: `url:github.com` or `url:` specific domains

### 2. Search and Extract

Run each query via CLI. After each, assess:
- Signal or noise? Adjust operators.
- Key voices worth searching `from:` specifically?
- Threads worth following via `thread` command?
- Linked resources worth deep-diving with `web_fetch`?

### 3. Follow Threads

When a tweet has high engagement or is a thread starter:
```bash
bun run x-search.ts thread <tweet_id>
```

### 4. Synthesize

Group findings by theme, not by query. Include engagement data and direct links.

### 5. Save

Use `--save` flag or save manually to `~/clawd/drafts/x-research-{topic-slug}-{YYYY-MM-DD}.md`.

## Reply Monitoring

To check replies to Ben:
```bash
bun run x-search.ts search "to:xBenJamminx" --sort likes --since 1d --limit 20
```

To check mentions of CortanaOps:
```bash
bun run x-search.ts search "@CortanaOps" --since 1d
```

## File Structure

```
skills/x-research/
├── SKILL.md           (this file)
├── x-search.ts        (CLI entry point)
├── lib/
│   ├── api.ts         (Composio API wrapper)
│   ├── cache.ts       (file-based cache, 15min TTL)
│   └── format.ts      (Telegram + markdown formatters)
├── data/
│   ├── watchlist.json  (accounts to monitor)
│   └── cache/          (auto-managed)
└── references/
    └── x-api.md        (X API endpoint reference)
```

## Credits

Forked from [rohunvora/x-research-skill](https://github.com/rohunvora/x-research-skill).
Adapted to use Composio instead of X API bearer token for zero-cost operation.
