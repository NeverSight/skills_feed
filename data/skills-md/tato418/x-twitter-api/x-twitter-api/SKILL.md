---
name: x-twitter-api
description: Interact with X (Twitter) API v2. Post tweets, search, engage, moderate, and analyze — all from your AI agent. Full 31-command skill for Twitter/X automation.
license: MIT
metadata:
  author: alberduris
  version: "1.0.0"
  tags: x, twitter, x-twitter, twitter-api, social-media, tweets, automation
allowed-tools: Bash(npm install), Bash(npm run build), Bash(node x.js)
---

X (Twitter) API v2 skill using the authenticated user's own developer credentials (OAuth 1.0a, pay-per-use). All commands go through a single entry point: `node x.js <command> [flags]`. Each command has its its own doc file with the full reference for flags and behavior.

[!SETUP] Before first use, check whether `./node_modules` exists. If it does NOT exist, run `npm install`. Then check whether `./dist/x.js` exists. If it does NOT exist, run `npm run build`. NEVER cd into the skill directory; use relative paths or --prefix to target it without changing your working directory.

[!COMMANDS]

Core:
a) `me` — authenticated user's own account data (profile, metrics, verification). @docs/me.md.
b) `search` — search posts by query (last 7 days or full archive). @docs/search.md.
c) `get` — retrieve one or more posts by ID. @docs/get.md.
d) `post` — create a tweet, reply, or quote tweet. @docs/post.md.
e) `delete` — delete a post owned by the authenticated user. @docs/delete.md.

Engagement:
f) `like` — like a post by tweet ID. @docs/like.md.
g) `unlike` — remove a like from a post. @docs/like.md.
h) `repost` — repost (retweet) a post. @docs/repost.md.
i) `unrepost` — remove a repost. @docs/repost.md.

Social:
j) `user` — look up user(s) by username or ID. @docs/user.md.
k) `follow` — follow a user by username or ID. @docs/follow.md.
l) `unfollow` — unfollow a user. @docs/follow.md.
m) `followers` — list a user's followers. @docs/followers.md.
n) `following` — list accounts a user follows. @docs/followers.md.

Feed:
o) `timeline` — your home timeline (reverse chronological). @docs/timeline.md.
p) `mentions` — posts that mention you. @docs/mentions.md.

Bookmarks:
q) `bookmark` — bookmark a post. @docs/bookmark.md.
r) `unbookmark` — remove a bookmark. @docs/bookmark.md.
s) `bookmarks` — list your bookmarks. @docs/bookmark.md.

Moderation:
t) `mute` — mute a user. @docs/mute.md.
u) `unmute` — unmute a user. @docs/mute.md.
v) `muted` — list muted accounts. @docs/mute.md.
w) `blocked` — list blocked accounts. @docs/blocked.md.
x) `hide-reply` — hide a reply to your post. @docs/hide-reply.md.

Analytics:
y) `likers` — users who liked a post. @docs/likers.md.
z) `reposters` — users who reposted a post. @docs/reposters.md.
aa) `quotes` — quote tweets of a post. @docs/quotes.md.
ab) `count` — count posts matching a query over time. @docs/count.md.
ac) `reposts-of-me` — reposts of your posts by others. @docs/reposts-of-me.md.

Discovery:
ad) `search-users` — search users by query. @docs/search-users.md.
ae) `trending` — trending topics (worldwide or personalized). @docs/trending.md.

[!PARAMETERS]

Core:
- `me`: No parameters
- `search`: query:string, [max_results?:number, since?:date, until?:date]
- `get`: id:string | ids:string[]
- `post`: text:string, [reply_to?:string, quote_id?:string]
- `delete`: id:string

Engagement:
- `like`: id:string
- `unlike`: id:string
- `repost`: id:string
- `unrepost`: id:string

Social:
- `user`: user:string, [expansions?:string, tweet_fields?:string, user_fields?:string]
- `follow`: user:string
- `unfollow`: user:string
- `followers`: [user?:string, max_results?:number, pagination_token?:string]
- `following`: [user?:string, max_results?:number, pagination_token?:string]

Feed:
- `timeline`: [max_results?:number, pagination_token?:string]
- `mentions`: [max_results?:number, pagination_token?:string]

Bookmarks:
- `bookmark`: id:string
- `unbookmark`: id:string
- `bookmarks`: [max_results?:number, pagination_token?:string]

Moderation:
- `mute`: user:string
- `unmute`: user:string
- `muted`: [max_results?:number, pagination_token?:string]
- `blocked`: [max_results?:number, pagination_token?:string]
- `hide-reply`: id:string

Analytics:
- `likers`: id:string, [max_results?:number, pagination_token?:string]
- `reposters`: id:string, [max_results?:number, pagination_token?:string]
- `quotes`: id:string, [max_results?:number, pagination_token?:string]
- `count`: query:string, [granularity?:string, start_time?:date, end_time?:date]
- `reposts-of-me`: [max_results?:number, pagination_token?:string]

Discovery:
- `search-users`: query:string, [max_results?:number]
- `trending`: [woeid?:number]

[!OUTPUT]

All commands return JSON with standard structure:
```json
{
  "success": boolean,
  "data": object | array | string,
  "error": string | null
}
```

Examples:
- Single object: `{"success": true, "data": {...}, "error": null}`
- Array response: `{"success": true, "data": [...], "error": null}`
- Error response: `{"success": false, "data": null, "error": "Error description"}`

[!ERRORS]

Standard error codes:
- `400` - Bad Request: Invalid parameters or malformed request
- `401` - Unauthorized: Invalid or expired credentials
- `403` - Forbidden: Access denied or insufficient permissions
- `404` - Not Found: Resource does not exist
- `429` - Too Many Requests: Rate limit exceeded
- `500` - Internal Server Error: X API server error
- `502` - Bad Gateway: X API unavailable
- `503` - Service Unavailable: X API overloaded

Error handling:
- Rate limit errors include `retry-after` header
- Authentication errors require credential refresh
- Validation errors include specific field issues

[!RATE-LIMITS]

X API v2 rate limits (OAuth 1.0a):
- User authentication: 50 requests per 15 minutes
- App authentication: 450 requests per 15 minutes (shared across all users)
- POST requests (tweets, likes, etc.): 300 requests per 3 hours

Best practices:
- Implement exponential backoff on 429 errors
- Cache timeline and search results when possible
- Batch requests where supported

[!CREDENTIALS]

Four OAuth 1.0a variables are REQUIRED: `X_API_KEY`, `X_API_SECRET`, `X_ACCESS_TOKEN`, `X_ACCESS_TOKEN_SECRET`. They resolve from the first source that provides them:

a) `.env.local` in cwd
b) `.env` in cwd
c) `.env.local` in the plugin directory
d) `.env` in the plugin directory
f) Environment variables

Obtain them from the X Developer Console (Apps > Keys and tokens).

Security notes:
- Never commit credentials to version control
- Use `.env` files for local development
- Rotate credentials if compromised
