---
name: x-tweet-fetch
version: 1.0.0
description: Fetch a specific tweet by URL or ID. Use when user shares an X/Twitter URL (https://x.com/... or https://twitter.com/...), asks "get this tweet", "fetch tweet", "what does this tweet say", "read this X post". Requires X_BEARER_TOKEN.
allowed-tools: Bash(curl:*), Bash(jq:*), Bash(${CLAUDE_PLUGIN_ROOT}:*)
---

# X Tweet Fetch

Get a specific tweet by URL or ID.

## Setup

```bash
export X_BEARER_TOKEN="your-token"  # https://developer.x.com/en/portal/dashboard
```

## Usage

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/fetch.sh <url_or_id>
```

## Examples

```bash
# By URL
${CLAUDE_PLUGIN_ROOT}/scripts/fetch.sh "https://x.com/kurtwuckertjr/status/1234567890"

# By ID
${CLAUDE_PLUGIN_ROOT}/scripts/fetch.sh 1234567890
```

## Response Fields

- `text` - Tweet content
- `created_at` - Post timestamp
- `public_metrics` - Likes, retweets, replies, views
- `author` - User info (expanded)
- `entities` - URLs, mentions, hashtags

## References

- https://docs.x.com/llms.txt
- https://developer.x.com/en/docs/x-api/tweets/lookup
