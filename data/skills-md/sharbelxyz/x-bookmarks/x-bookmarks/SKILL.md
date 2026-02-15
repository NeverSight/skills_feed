---
name: x-bookmarks
version: 1.1.0
description: >
  Fetch, summarize, and manage X/Twitter bookmarks via bird CLI or X API v2.
  Use when: (1) user says "check my bookmarks", "what did I bookmark", "bookmark digest",
  "summarize my bookmarks", "x bookmarks", "twitter bookmarks", (2) user wants a periodic
  digest of saved tweets, (3) user wants to categorize, search, or analyze their bookmarks,
  (4) scheduled bookmark digests via cron.
  Auth: bird CLI with browser cookies, OR X API v2 with OAuth 2.0 tokens.
requires:
  env:
    - AUTH_TOKEN: "X/Twitter auth token (from browser cookies, for bird CLI auth)"
    - CT0: "X/Twitter CSRF token (from browser cookies, for bird CLI auth)"
    - X_API_BEARER_TOKEN: "Optional: X API v2 Bearer token (alternative to bird CLI)"
  bins:
    - bird: "bird-cli (npm i -g bird-cli) - preferred backend"
  files:
    - .env.bird: "Optional: stores AUTH_TOKEN and CT0 for bird CLI"
    - ~/.config/x-bookmarks/tokens.json: "OAuth 2.0 tokens for X API v2 backend"
security:
  credentials: >
    This skill accesses X/Twitter bookmarks, which requires authentication.
    Two methods are supported: (1) bird CLI using browser cookies (AUTH_TOKEN/CT0 env vars
    sourced from .env.bird), or (2) X API v2 with OAuth 2.0 tokens stored locally.
    All credentials are stored locally on the user's machine and never transmitted
    to third parties. The user must explicitly provide or authorize credentials.
  permissions:
    - read: "X/Twitter bookmarks (read-only access)"
    - write: "Local files only (bookmark state, token storage)"
---

# X Bookmarks v2

Turn X/Twitter bookmarks from a graveyard of good intentions into actionable work.

**Core philosophy:** Don't just summarize — propose actions the agent can execute.

## Data Source Selection

This skill supports **two backends**. Pick the first one that works:

### 1. bird CLI (preferred if available)
- Fast, no API key needed, uses browser cookies
- Install: `npm install -g bird-cli`
- Test: `bird whoami` — if this prints a username, you're good

### 2. X API v2 (fallback)
- Works without bird CLI
- Requires an X Developer account + OAuth 2.0 app
- Setup: see [references/auth-setup.md](references/auth-setup.md) → "X API Setup"

### Auto-detection logic

```
1. Check if `bird` command exists → try `bird whoami`
2. If bird works → use bird CLI path
3. If not → check for X API tokens (~/.config/x-bookmarks/tokens.json)
4. If tokens exist → use X API path (auto-refresh)
5. If neither → guide user through setup (offer both options)
```

## Fetching Bookmarks

### Via bird CLI

```bash
# Latest 20 bookmarks (default)
bird bookmarks --json

# Specific count
bird bookmarks -n 50 --json

# All bookmarks (paginated)
bird bookmarks --all --json

# With thread context
bird bookmarks --include-parent --thread-meta --json

# With Chrome cookie auth
bird --chrome-profile "Default" bookmarks --json

# With manual tokens
bird --auth-token "$AUTH_TOKEN" --ct0 "$CT0" bookmarks --json
```

If user has a `.env.bird` file or env vars `AUTH_TOKEN`/`CT0`, source them first: `source .env.bird`

### Via X API v2

```bash
# First-time setup (opens browser for OAuth)
python3 scripts/x_api_auth.py --client-id "YOUR_CLIENT_ID" --client-secret "YOUR_SECRET"

# Fetch bookmarks (auto-refreshes token)
python3 scripts/fetch_bookmarks_api.py -n 20

# All bookmarks
python3 scripts/fetch_bookmarks_api.py --all

# Since a specific tweet
python3 scripts/fetch_bookmarks_api.py --since-id "1234567890"

# Pretty print
python3 scripts/fetch_bookmarks_api.py -n 50 --pretty
```

The API script outputs the **same JSON format** as bird CLI, so all downstream workflows work identically.

**Token management is automatic:** tokens are stored in `~/.config/x-bookmarks/tokens.json` and refreshed via the saved refresh_token. If refresh fails, the agent should guide the user to re-run `x_api_auth.py`.

### Environment variable override

If the user already has a Bearer token (e.g., from another tool), they can skip the OAuth dance:
```bash
X_API_BEARER_TOKEN="your_token" python3 scripts/fetch_bookmarks_api.py -n 20
```

## JSON Output Format (both backends)

Each bookmark returns:
```json
{
  "id": "tweet_id",
  "text": "tweet content",
  "createdAt": "2026-02-11T01:00:06.000Z",
  "replyCount": 46,
  "retweetCount": 60,
  "likeCount": 801,
  "bookmarkCount": 12,
  "viewCount": 50000,
  "author": { "username": "handle", "name": "Display Name" },
  "media": [{ "type": "photo|video", "url": "..." }],
  "quotedTweet": { "id": "..." }
}
```

## Core Workflows

### 1. Action-First Digest (Primary Use Case)

The key differentiator: don't just summarize, **propose actions the agent can execute**.

1. Fetch bookmarks (bird or API, auto-detected)
2. Parse and categorize by topic (auto-detect: crypto, AI, marketing, tools, personal, etc.)
3. For EACH category, propose specific actions:
   - **Tool/repo bookmarks** → "I can test this, set it up, or analyze the code"
   - **Strategy/advice bookmarks** → "Here are the actionable steps extracted — want me to implement any?"
   - **News/trends** → "This connects to [user's work]. Here's the angle for content"
   - **Content ideas** → "This would make a great tweet/video in your voice. Here's a draft"
   - **Questions/discussions** → "I can research this deeper and give you a summary"
4. Flag stale bookmarks (>2 weeks old) — "Use it or lose it"
5. Deliver categorized digest with actions

Format output as:
```
📂 CATEGORY (count)
• Bookmark summary (@author)
→ 🤖 I CAN: [specific action the agent can take]
```

### 2. Scheduled Digest (Cron)

Set up a recurring bookmark check. Suggest this cron config to the user:

```
Schedule: daily or weekly
Payload: "Check my X bookmarks for new saves since last check.
  Fetch bookmarks, compare against last digest, summarize only NEW ones.
  Categorize and propose actions. Deliver to me."
```

Track state by saving the most recent bookmark ID processed. Store in workspace:
`memory/bookmark-state.json` → `{ "lastSeenId": "...", "lastDigestAt": "..." }`

### 3. Content Recycling

When user asks for content ideas from bookmarks:
1. Fetch recent bookmarks
2. Identify high-engagement tweets (>500 likes) with frameworks, tips, or insights
3. Rewrite key ideas in the user's voice (if voice data available)
4. Suggest posting times based on the bookmark's original engagement

### 4. Pattern Detection

When user has enough bookmark history:
1. Fetch all bookmarks (`--all`)
2. Cluster by topic/keywords
3. Report: "You've bookmarked N tweets about [topic]. Want me to go deeper?"
4. Suggest: research reports, content series, or tools based on patterns

### 5. Bookmark Cleanup

For stale bookmarks:
1. Identify bookmarks older than a threshold (default: 30 days)
2. For each: extract the TL;DR and one actionable takeaway
3. Present: "Apply it today or clear it"
4. User can unbookmark via: `bird unbookmark <tweet-id>` (bird only)

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `bird: command not found` | bird CLI not installed | Use X API path instead, or `npm i -g bird-cli` |
| "No Twitter cookies found" | Not logged into X in browser | Log into x.com in Chrome/Firefox, or use X API |
| EPERM on Safari cookies | macOS permissions | Use Chrome/Firefox or X API instead |
| Empty results | Cookies/token expired | Re-login or re-run `x_api_auth.py` |
| Rate limit (429) | Too many API requests | Wait and retry, use `--count` to limit |
| "No X API token found" | Haven't run auth setup | Run `x_api_auth.py --client-id YOUR_ID` |
| Token refresh failed | Refresh token expired | Re-run `x_api_auth.py` to re-authorize |

## Tips

- Start with `-n 20` for quick digests, `--all` for deep analysis
- bird: Use `--include-parent` for thread context on replies
- API: includes `bookmarkCount` and `viewCount` (bird may not)
- Bookmark folders supported via bird `--folder-id <id>`
- Both backends output identical JSON — workflows are backend-agnostic
