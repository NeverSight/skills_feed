---
name: xint-rs
description: >
  Fast X Intelligence CLI (Rust) — search, analyze, and engage on X/Twitter from the terminal.
  Use when: (1) user says "x research", "search x for", "search twitter for", "what are people saying about",
  "what's twitter saying", "check x for", "x search", "search x", (2) user wants real-time monitoring with "watch",
  (3) user needs AI-powered analysis with Grok ("analyze", "sentiment"), (4) user needs intelligence reports ("report"),
  (5) user wants to track followers ("diff"), (6) user needs trending topics ("trends").
  Also supports: bookmarks, likes, following (OAuth), x-search, collections, CSV/JSON/JSONL export.
  Non-goals: Not for posting tweets, not for DMs, not for enterprise features.
credentials:
  - name: X_BEARER_TOKEN
    description: X API v2 bearer token for search, profile, thread, tweet, trends
    required: true
  - name: XAI_API_KEY
    description: xAI API key for Grok analysis, article fetching, sentiment, x-search, collections
    required: false
  - name: XAI_MANAGEMENT_API_KEY
    description: xAI Management API key for collections management
    required: false
  - name: X_CLIENT_ID
    description: X OAuth 2.0 client ID for user-context operations (bookmarks, likes, following, diff)
    required: false
required_env_vars:
  - X_BEARER_TOKEN
requiredEnvVars:
  - X_BEARER_TOKEN
primary_credential: X_BEARER_TOKEN
primaryCredential: X_BEARER_TOKEN
security:
  always: false
  autonomous: false
  local_data_dir: data/
  network_endpoints:
    - https://api.x.com
    - https://x.com
    - https://api.x.ai
---

# xint — X Intelligence CLI (Rust)

Fast, zero-dependency binary for X/Twitter search, analysis, and engagement from the terminal. All output goes to stdout (pipe-friendly).

## Security Considerations

This skill requires sensitive credentials. Follow these guidelines:

### Credentials
- **X_BEARER_TOKEN**: Required for X API. Treat as a secret - only set in environment or `.env` file
- **XAI_API_KEY**: Optional, needed for AI analysis. Also a secret
- **X_CLIENT_ID**: Optional, needed for OAuth. Less sensitive but don't expose publicly
- **XAI_MANAGEMENT_API_KEY**: Optional, for collections management

### File Writes
- This skill writes to its own `data/` directory: cache, exports, snapshots, OAuth tokens
- OAuth tokens stored with restrictive permissions (chmod 600)
- Review exported data before sharing - may contain sensitive search queries

### Webhooks
- `watch` and `stream` can send data to webhook endpoints
- Remote endpoints must use `https://` (`http://` is accepted only for localhost/loopback)
- Optional host allowlist: `XINT_WEBHOOK_ALLOWED_HOSTS=hooks.example.com,*.internal.example`
- Avoid sending sensitive search queries or token-bearing URLs to third-party destinations

### Runtime Notes
- This document is descriptive; it does not modify runtime/system prompts
- Network listeners are opt-in (`mcp --sse`) and disabled by default
- Webhook delivery is opt-in (`--webhook`) and disabled by default

### Installation
- For required tools: prefer OS package managers over `curl | bash` when possible
- Verify any installer scripts before running

### MCP Server (Optional)
- `xint mcp` starts a local MCP server exposing xint commands as tools
- Default mode is stdio/local integration; no inbound web server unless `--sse` is explicitly enabled
- Respect `--policy read_only|engagement|moderation` and budget guardrails

## Setup

Requires env vars (in `.env` or exported):
- `X_BEARER_TOKEN` — for search, profile, tweet, thread, trends, watch, report
- `X_CLIENT_ID` — for OAuth commands (bookmarks, likes, following, diff)
- `XAI_API_KEY` — for AI analysis (analyze, report, x-search, collections upload/search)
- `XAI_MANAGEMENT_API_KEY` — for collections management (list, create, ensure, add-document)

OAuth setup (one-time): `xint auth setup`

## Commands

### Search & Discovery
```bash
xint search "AI agents" --limit 10            # Search recent tweets
xint search "AI agents" --quick               # Fast mode (1 page, 10 max, 1hr cache)
xint search "AI agents" --quality             # Min 10 likes filter
xint search "AI agents" --since 1d --sort likes
xint search "from:elonmusk" --limit 5
xint search "AI agents" --json                # JSON output
xint search "AI agents" --jsonl               # One JSON per line
xint search "AI agents" --csv                 # CSV output
xint search "AI agents" --sentiment           # AI sentiment analysis (needs XAI_API_KEY)
xint search "AI agents" --save                # Save to data/exports/
```

### Monitoring
```bash
xint watch "AI agents" -i 5m                  # Poll every 5 minutes
xint watch "@elonmusk" -i 30s                 # Watch user (auto-expands to from:)
xint watch "bitcoin" --webhook https://hooks.example.com/ingest  # POST new tweets to webhook
xint watch "topic" --jsonl                    # Machine-readable output
```

### Profiles & Tweets
```bash
xint profile elonmusk                         # User profile + recent tweets
xint profile elonmusk --json                  # JSON output
xint tweet 1234567890                         # Fetch single tweet
xint thread 1234567890                        # Fetch conversation thread
```

### Article Fetching (requires XAI_API_KEY)

Fetch and extract full article content from any URL using xAI's web_search tool. Also supports extracting linked articles from X tweets.

```bash
# Fetch article content
xint article "https://example.com"

# Fetch + analyze with AI
xint article "https://example.com" --ai "Summarize key takeaways"

# Auto-extract article from X tweet URL and analyze
xint article "https://x.com/user/status/123456789" --ai "What are the main points?"

# Full content without truncation
xint article "https://example.com" --full

# JSON output
xint article "https://example.com" --json
```

### Trends
```bash
xint trends                                   # Worldwide trending
xint trends us                              # US trends
xint trends --json                          # JSON output
xint trends --locations                     # List supported locations
```

### AI Analysis (requires XAI_API_KEY)
```bash
xint analyze "What's the sentiment around AI?"
xint analyze --tweets saved.json              # Analyze tweets from file
cat tweets.json | xint analyze --pipe         # Analyze from stdin
xint analyze "question"                              # Free-form analysis request
```

### Intelligence Reports
```bash
xint report "AI agents"                       # Full report with AI summary
xint report "AI agents" -a @user1,@user2      # Track specific accounts
xint report "AI agents" -s                    # Include sentiment analysis
xint report "AI agents" --save                # Save to data/exports/
```

### Follower Tracking (requires OAuth)
```bash
xint diff @username                           # Snapshot followers, diff vs previous
xint diff @username --following               # Track following instead
xint diff @username --history                 # Show snapshot history
```

### Bookmarks & Engagement (requires OAuth)
```bash
xint bookmarks                                # List bookmarks
xint bookmarks --since 1d                     # Recent bookmarks
xint bookmark 1234567890                      # Save tweet
xint unbookmark 1234567890                    # Remove bookmark
xint likes                                    # List liked tweets
xint like 1234567890                          # Like a tweet
xint unlike 1234567890                        # Unlike a tweet
xint following                                # List accounts you follow
```

### Cost Tracking
```bash
xint costs                                    # Today's API costs
xint costs week                               # Last 7 days
xint costs month                              # Last 30 days
xint costs budget 2.00                        # Set $2/day budget
```

### Watchlist
```bash
xint watchlist                                # List watched accounts
xint watchlist add @username "competitor"     # Add with note
xint watchlist remove @username               # Remove
xint watchlist check @username                # Check if watched
```

### xAI X Search (no cookies/GraphQL)

Search X via xAI's hosted x_search tool. No bearer token or cookies needed — only `XAI_API_KEY`.

```bash
# Create a queries file
echo '["AI agents", "solana"]' > queries.json

# Run search scan → markdown report + JSON payload
xint x-search --queries-file queries.json --out-md report.md --out-json raw.json

# Date range filter
xint x-search --queries-file queries.json --from-date 2026-02-01 --to-date 2026-02-15

# Emit memory candidates (deduped against existing workspace sources)
xint x-search --queries-file queries.json --workspace /path/to/workspace --emit-candidates

# Custom model
xint x-search --queries-file queries.json --model grok-3
```

### xAI Collections Knowledge Base

Upload documents, manage collections, and semantic-search via xAI Files + Collections APIs.

```bash
# List existing collections
xint collections list

# Create or find a collection
xint collections ensure --name "research-kb"

# Upload a file to xAI
xint collections upload --path ./report.md

# Semantic search across documents
xint collections search --query "AI agent frameworks"

# Sync a directory to a collection (upload + attach)
xint collections sync-dir --collection-name "kb" --dir ./docs --glob "*.md" --limit 50
```

### Utilities
```bash
xint auth setup                               # OAuth setup (interactive)
xint auth setup --manual                      # Manual paste mode
xint auth status                              # Show auth info
xint auth refresh                             # Force token refresh
xint cache clear                              # Clear cached data
```

## Output Formats

Most commands support `--json` for raw JSON. Search also supports:
- `--jsonl` — one JSON object per line (great for piping)
- `--csv` — spreadsheet-compatible
- `--markdown` — formatted for reports

## Piping

```bash
xint search "topic" --jsonl | jq '.username'
xint search "topic" --json | xint analyze --pipe "summarize these"
xint search "topic" --csv > export.csv
```

## Cost Awareness

X API costs ~$0.005/tweet read. Budget system prevents runaway costs:
- Default: $1.00/day limit
- Set custom: `xint costs budget <amount>`
- Watch command auto-stops at budget limit
