---
name: social-intelligence
description: |
  Search and monitor social media using X/Twitter (via Grok) and Reddit APIs.

  USE FOR:
  - Searching X/Twitter posts by keywords or hashtags
  - Finding X/Twitter users by criteria
  - Getting a user's recent posts
  - Searching Reddit posts and discussions
  - Getting comments from Reddit threads
  - Social media monitoring and research

  TRIGGERS:
  - "twitter", "X", "tweets", "posts on X"
  - "reddit", "subreddit", "reddit discussion"
  - "what are people saying", "social media", "sentiment"
  - "trending", "viral", "popular posts"
  - "user's posts", "timeline", "recent activity"

  Use `npx agentcash fetch` for Grok (X) and Reddit endpoints. All endpoints are $0.02 per call.

  IMPORTANT: Use exact endpoint paths from the Quick Reference table below.
---

# Social Intelligence with x402 APIs

Access X/Twitter (via Grok) and Reddit through x402-protected endpoints.

## Setup

See [rules/getting-started.md](rules/getting-started.md) for installation and wallet setup.

## Quick Reference

| Task | Endpoint | Price | Description |
|------|----------|-------|-------------|
| Search X posts | `https://stableenrich.dev/api/grok/x-search` | $0.02 | Search tweets by keywords |
| Find X users | `https://stableenrich.dev/api/grok/user-search` | $0.02 | Search users by criteria |
| Get user posts | `https://stableenrich.dev/api/grok/user-posts` | $0.02 | Recent posts from user |
| Search Reddit | `https://stableenrich.dev/api/reddit/search` | $0.02 | Search Reddit posts |
| Get comments | `https://stableenrich.dev/api/reddit/post-comments` | $0.02 | Comments on a post |

See [rules/rate-limits.md](rules/rate-limits.md) for usage guidance.

## X/Twitter via Grok

### Search Posts

Search for X posts by keywords:

```bash
npx agentcash fetch https://stableenrich.dev/api/grok/x-search -m POST -b '{"query": "AI agents"}'
```

**Parameters:**
- `query` - Search keywords (required)

**Returns:**
- Post text and author info
- Engagement metrics (likes, retweets, replies)
- Timestamps and URLs
- Media attachments

### Search Users

Find X users matching criteria:

```bash
npx agentcash fetch https://stableenrich.dev/api/grok/user-search -m POST -b '{"query": "AI researcher San Francisco"}'
```

**Returns:**
- Username and display name
- Bio/description
- Follower/following counts
- Verification status
- Profile links

### Get User's Posts

Fetch recent posts from a specific user:

```bash
npx agentcash fetch https://stableenrich.dev/api/grok/user-posts -m POST -b '{"username": "elonmusk"}'
```

**Parameters:**
- `username` - X username without @ (required)

**Returns:** Recent posts with full engagement metrics.

## Reddit

### Search Posts

Search Reddit for posts:

```bash
npx agentcash fetch https://stableenrich.dev/api/reddit/search -m POST -b '{"query": "best programming languages 2024"}'
```

**Parameters:**
- `query` - Search terms (required)
- `subreddit` - Limit to specific subreddit
- `sort` - relevance, hot, new, top
- `time` - hour, day, week, month, year, all

**Returns:**
- Post title and content
- Author and subreddit
- Upvotes and comment count
- Post URL

### Search in Subreddit

```bash
npx agentcash fetch https://stableenrich.dev/api/reddit/search -m POST -b '{
  "query": "typescript vs javascript",
  "subreddit": "programming",
  "sort": "top",
  "time": "year"
}'
```

### Get Post Comments

Get comments from a Reddit post:

```bash
npx agentcash fetch https://stableenrich.dev/api/reddit/post-comments -m POST -b '{"postUrl": "https://reddit.com/r/programming/comments/abc123/..."}'
```

**Returns:**
- Comment text and author
- Upvotes/downvotes
- Reply threads
- Comment timestamps

## Workflows

### Standard

- [ ] (Optional) Check balance: `npx agentcash wallet info`
- [ ] Use `npx agentcash discover https://stableenrich.dev` to list all endpoints
- [ ] Use `npx agentcash check <endpoint-url>` to see expected parameters and pricing
- [ ] Call endpoint with `npx agentcash fetch`
- [ ] Parse and present results

### Brand Monitoring

- [ ] (Optional) Check balance: `npx agentcash wallet info`
- [ ] Search X for brand mentions
- [ ] Search Reddit for discussions
- [ ] Summarize sentiment and key mentions

```bash
npx agentcash fetch https://stableenrich.dev/api/grok/x-search -m POST -b '{"query": "YourBrand OR @YourBrand"}'
```

```bash
npx agentcash fetch https://stableenrich.dev/api/reddit/search -m POST -b '{"query": "YourBrand", "sort": "new"}'
```

### Competitor Research

- [ ] Search Reddit for competitor reviews
- [ ] Search X for competitor mentions
- [ ] Analyze common complaints and praise

```bash
npx agentcash fetch https://stableenrich.dev/api/reddit/search -m POST -b '{"query": "competitor name review", "sort": "top", "time": "year"}'
```

### Influencer Discovery

- [ ] Define criteria (topic, follower range)
- [ ] Search for matching users
- [ ] Get recent posts for top candidates

```bash
npx agentcash fetch https://stableenrich.dev/api/grok/user-search -m POST -b '{"query": "tech blogger 100k followers"}'
```

### Community Sentiment

- [ ] Identify relevant subreddit
- [ ] Search for discussions on topic
- [ ] Get comments from top posts
- [ ] Synthesize overall sentiment

```bash
npx agentcash fetch https://stableenrich.dev/api/reddit/search -m POST -b '{"query": "new feature name", "subreddit": "relevant_community", "sort": "hot"}'
```

```bash
npx agentcash fetch https://stableenrich.dev/api/reddit/post-comments -m POST -b '{"postUrl": "https://reddit.com/..."}'
```

## Response Data

### X/Twitter Post Fields
- `text` - Post content
- `author` - Username, display name, verified status
- `metrics` - Likes, retweets, replies, quotes, views
- `createdAt` - Timestamp
- `url` - Link to post
- `media` - Attached images/videos

### X/Twitter User Fields
- `username` - Handle without @
- `displayName` - Full name
- `description` - Bio
- `followers` / `following` - Counts
- `verified` - Verification status
- `profileImageUrl` - Avatar

### Reddit Post Fields
- `title` - Post title
- `selftext` - Post body (for text posts)
- `author` - Username
- `subreddit` - Subreddit name
- `score` - Upvotes minus downvotes
- `numComments` - Comment count
- `url` - Link to post
- `createdUtc` - Timestamp

### Reddit Comment Fields
- `body` - Comment text
- `author` - Username
- `score` - Net upvotes
- `replies` - Nested replies
- `createdUtc` - Timestamp

## Cost Estimation

| Task | Calls | Cost |
|------|-------|------|
| Quick X search | 1 | $0.02 |
| User profile + posts | 2 | $0.04 |
| Reddit thread + comments | 2 | $0.04 |
| Full monitoring scan | 4-6 | $0.08-0.12 |
