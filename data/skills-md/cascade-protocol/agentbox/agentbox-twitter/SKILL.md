---
name: agentbox-twitter
description: "Twitter/X research via paid API: search tweets with 50+ operators, fetch tweets with threads/replies/quotes, get user profiles with tweets/followers/following. Uses x_payment tool for automatic USDC micropayments ($0.003/call). Use when: (1) searching tweets by keyword, user, or advanced operators, (2) fetching specific tweets by ID/URL with context, (3) looking up user profiles and their activity."
metadata: {"openclaw": {"emoji": "🐦", "requires": {"bins": ["openclaw"]}}}
---

# Twitter Research

Paid Twitter/X data API at `https://twitter.x402.agentbox.fyi`. Costs $0.003 USDC per call via x402 on Solana. Use the `x_payment` tool for all requests.

## Endpoints

### Search Tweets

Find tweets matching a query with 50+ advanced operators.

```
x_payment({
  "url": "https://twitter.x402.agentbox.fyi/search",
  "method": "GET",
  "params": "{\"q\": \"from:elonmusk AI\", \"type\": \"Latest\", \"limit\": 20}"
})
```

**Parameters:**

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| q | string | required | Search query with operators |
| type | "Latest" or "Top" | Latest | Sort by recency or popularity |
| limit | 1-200 | 20 | Max tweets to return |
| cursor | string | - | Pagination cursor from previous response |

**Search operators:**

| Operator | Example | Description |
|----------|---------|-------------|
| from:user | `from:elonmusk` | Tweets by user |
| to:user | `to:elonmusk` | Replies to user |
| @user | `@solana` | Mentioning user |
| min_faves:N | `min_faves:100` | Minimum likes |
| min_retweets:N | `min_retweets:50` | Minimum retweets |
| min_replies:N | `min_replies:10` | Minimum replies |
| filter:media | `filter:media` | Has media |
| filter:images | `filter:images` | Has images |
| filter:videos | `filter:videos` | Has video |
| filter:links | `filter:links` | Has links |
| filter:replies | `filter:replies` | Only replies |
| -filter:replies | `-filter:replies` | Exclude replies |
| since:date | `since:2025-01-01` | After date |
| until:date | `until:2025-12-31` | Before date |
| within_time:Nh | `within_time:24h` | Last N hours |
| lang:code | `lang:en` | Language filter |
| conversation_id:ID | `conversation_id:123` | In conversation |
| filter:self_threads | `from:user filter:self_threads` | User's thread replies |

Combine operators: `from:elonmusk AI min_faves:100 -filter:replies within_time:7d`

**Response:** `{ query, tweets[], count, hasMore, nextCursor, summary }`

The `summary` object includes: `totalLikes`, `totalRetweets`, `totalReplies`, `avgLikes`, `maxLikes`, `topTweetId`.

### Fetch Tweets

Get tweet(s) by ID or URL with optional thread, replies, and quotes.

```
x_payment({
  "url": "https://twitter.x402.agentbox.fyi/tweet/1585841080431321088",
  "method": "GET",
  "params": "{\"include\": \"thread,replies\", \"limit\": 50}"
})
```

**URL format:** `/tweet/{ref}` where ref is:
- Tweet ID: `1585841080431321088`
- Comma-separated IDs: `123,456,789` (batch fetch, no includes)

**Parameters:**

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| include | string | - | Comma-separated: `thread`, `replies`, `quotes` |
| limit | 1-200 | 50 | Max replies/quotes to return |

**Include options (single tweet only):**
- `thread` - author's self-reply chain in the conversation
- `replies` - replies from other users
- `quotes` - quote tweets of this tweet

**Response:** `{ tweets[], count, parent?, thread?, replies?, quotes? }`

If the fetched tweet is a reply, `parent` is auto-included with the replied-to tweet.

### Fetch Users

Get user profile(s) with optional tweets, followers, or following.

```
x_payment({
  "url": "https://twitter.x402.agentbox.fyi/user/elonmusk",
  "method": "GET",
  "params": "{\"include\": \"tweets\", \"limit\": 20}"
})
```

**URL format:** `/user/{ref}` where ref is:
- Username: `elonmusk` or `@elonmusk`
- User ID: `44196397`
- Comma-separated IDs: `123,456` (batch fetch, no includes)

**Parameters:**

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| include | string | - | Comma-separated: `tweets`, `followers`, `following` |
| limit | 1-200 | 50 | Max tweets/followers/following to return |
| include_replies | boolean | false | Include replies in user's tweets |

**Response (single):** `{ user, tweets?, followers?, following? }`
**Response (batch):** `{ users[], count, hasMore }`

## Usage Patterns

### Monitor a topic

```
x_payment({
  "url": "https://twitter.x402.agentbox.fyi/search",
  "method": "GET",
  "params": "{\"q\": \"x402 OR \\\"402 payment\\\" min_faves:5 within_time:24h\", \"type\": \"Latest\"}"
})
```

### Get a tweet with full context

```
x_payment({
  "url": "https://twitter.x402.agentbox.fyi/tweet/1585841080431321088",
  "method": "GET",
  "params": "{\"include\": \"thread,replies,quotes\", \"limit\": 20}"
})
```

### Research a user

```
x_payment({
  "url": "https://twitter.x402.agentbox.fyi/user/CoinbaseDev",
  "method": "GET",
  "params": "{\"include\": \"tweets\", \"limit\": 50}"
})
```

### Paginate results

Use `nextCursor` from a previous response:

```
x_payment({
  "url": "https://twitter.x402.agentbox.fyi/search",
  "method": "GET",
  "params": "{\"q\": \"from:elonmusk\", \"cursor\": \"DAABCgAB...\"}"
})
```

## Cost

Every call costs $0.003 USDC on Solana mainnet. Each paginated request is a separate call. Plan queries to minimize calls - use specific operators and reasonable limits.

## Errors

| HTTP | Meaning |
|------|---------|
| 400 | Invalid parameters (check query syntax) |
| 402 | Payment required (handled automatically by x_payment) |
| 404 | Tweet or user not found |
| 502 | Upstream API error |
