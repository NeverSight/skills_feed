---
name: x-user-timeline
version: 1.0.0
description: Get recent tweets from an X/Twitter user. Use when user asks "what has @username posted", "recent tweets from", "user's X posts", "show timeline for", "what is @user saying". Requires X_BEARER_TOKEN.
allowed-tools: Bash(curl:*), Bash(jq:*), Bash(${CLAUDE_PLUGIN_ROOT}:*)
---

# X User Timeline

Get recent tweets from a specific user.

## Setup

```bash
export X_BEARER_TOKEN="your-token"  # https://developer.x.com/en/portal/dashboard
```

## Usage

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/timeline.sh <username> [max_results]
```

## Examples

```bash
# Get 10 recent tweets (default)
${CLAUDE_PLUGIN_ROOT}/scripts/timeline.sh kurtwuckertjr

# Get 25 tweets
${CLAUDE_PLUGIN_ROOT}/scripts/timeline.sh kurtwuckertjr 25
```

## Response Fields

- `text` - Tweet content
- `created_at` - Post timestamp
- `public_metrics` - Likes, retweets, replies, views
- `author` - User info (expanded)

## Rate Limits

Free tier: 1,500 tweets/month, 10 requests per 15 minutes

## References

- https://docs.x.com/llms.txt
- https://developer.x.com/en/docs/x-api/tweets/timelines
