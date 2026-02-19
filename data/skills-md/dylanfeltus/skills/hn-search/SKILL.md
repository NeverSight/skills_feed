---
name: hn-search
description: Search and monitor Hacker News stories, comments, and users via the free Algolia API. Use when the user asks about HN discussions, wants to find posts about a topic, or monitor HN for mentions. No API key required.
---

# Hacker News Search

Search and monitor Hacker News stories, comments, and users via the Algolia HN Search API. No API key required.

## When to Use

- User asks about Hacker News discussions on a topic
- User wants to find HN posts about a company, product, or technology
- User wants to monitor HN for mentions of something
- User asks "what's trending on HN" or "what did HN think about X"
- User wants to find Show HN / Ask HN / Launch HN posts

## API Overview

**Base URL:** `https://hn.algolia.com/api/v1`

Two search endpoints:
- `/search` — Relevance-sorted (best for finding specific topics)
- `/search_by_date` — Date-sorted (best for monitoring / recent activity)

**Rate Limits:** 10,000 requests/hour (generous, no auth needed)

## How to Search

### Step 1: Build the URL

```
https://hn.algolia.com/api/v1/search?query=QUERY&tags=TAG&hitsPerPage=N&numericFilters=FILTERS
```

### Step 2: Fetch with `web_fetch`

Use `web_fetch` to call the API. Response is JSON.

### Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `query` | Search terms (URL-encoded) | `query=openai+gpt` |
| `tags` | Filter by type (see below) | `tags=story` |
| `hitsPerPage` | Results per page (max 1000) | `hitsPerPage=20` |
| `page` | Page number (0-indexed) | `page=0` |
| `numericFilters` | Numeric filters (see below) | `numericFilters=points>100` |

### Tag Filters

Use `tags` to filter by content type:

| Tag | Description |
|-----|-------------|
| `story` | Stories only |
| `comment` | Comments only |
| `show_hn` | Show HN posts |
| `ask_hn` | Ask HN posts |
| `front_page` | Currently on front page |
| `author_USERNAME` | Posts by a specific user |
| `story_ID` | Comments on a specific story |

**Combine tags** with commas (AND) or parentheses with commas (OR):
- `tags=story,show_hn` → Show HN stories (AND)
- `tags=(story,comment)` → Stories OR comments

### Numeric Filters

| Filter | Description |
|--------|-------------|
| `points>N` | Minimum points/upvotes |
| `num_comments>N` | Minimum comments |
| `created_at_i>TIMESTAMP` | After Unix timestamp |
| `created_at_i<TIMESTAMP` | Before Unix timestamp |

Combine with commas: `numericFilters=points>100,num_comments>50`

### Date Ranges

To search within a time window, use Unix timestamps with `created_at_i`:

Calculate the current Unix timestamp first (e.g., via `exec: date +%s`), then subtract:

| Window | Subtract from now |
|--------|------------------|
| Last 24 hours | `- 86400` |
| Last 7 days | `- 604800` |
| Last 30 days | `- 2592000` |

Example: if now is `1705312200`, last 7 days = `numericFilters=created_at_i>1704707400`

## Response Format

Each hit contains:

```json
{
  "objectID": "12345",
  "title": "Story Title",
  "url": "https://example.com/article",
  "author": "username",
  "points": 150,
  "num_comments": 42,
  "created_at": "2024-01-15T10:30:00Z",
  "created_at_i": 1705312200,
  "story_text": "Text for Ask HN / Show HN (HTML)",
  "_tags": ["story", "author_username", "story_12345"]
}
```

For comments, hits also include:
```json
{
  "comment_text": "The comment body (HTML)",
  "story_id": 12345,
  "story_title": "Parent Story Title",
  "story_url": "https://example.com",
  "parent_id": 12344
}
```

The response wrapper includes:
```json
{
  "hits": [...],
  "nbHits": 1000,
  "page": 0,
  "nbPages": 50,
  "hitsPerPage": 20
}
```

## Constructing HN Links

- **Story:** `https://news.ycombinator.com/item?id={objectID}`
- **Comment:** `https://news.ycombinator.com/item?id={objectID}`
- **User:** `https://news.ycombinator.com/user?id={author}`

## Step-by-Step Instructions

### Searching for Stories on a Topic

1. URL-encode the query
2. Fetch: `https://hn.algolia.com/api/v1/search?query=YOUR_QUERY&tags=story&hitsPerPage=10`
3. Parse the JSON response
4. For each hit, present: title, points, num_comments, author, date, HN link, and original URL

### Finding Recent/Trending Discussions

1. Calculate Unix timestamp for your time window (e.g., 7 days ago)
2. Fetch: `https://hn.algolia.com/api/v1/search?query=YOUR_QUERY&tags=story&numericFilters=points>50,created_at_i>TIMESTAMP&hitsPerPage=10`
3. Sort results by points or comments for "trending"

### Getting Comments on a Story

1. Get the story's objectID from a search
2. Fetch: `https://hn.algolia.com/api/v1/search?tags=comment,story_STORYID&hitsPerPage=20`
3. Present comment_text, author, points for each

### Monitoring a Topic (Show Recent Mentions)

1. Use `/search_by_date` instead of `/search`
2. Fetch: `https://hn.algolia.com/api/v1/search_by_date?query=YOUR_QUERY&tags=(story,comment)&hitsPerPage=20`
3. Results are newest-first — useful for "what's new about X on HN"

### Finding a User's Posts

1. Fetch: `https://hn.algolia.com/api/v1/search?tags=author_USERNAME,story&hitsPerPage=20`
2. For their comments: `tags=author_USERNAME,comment`

## Output Format

Present results as a clean list:

```
### HN Results for "query" (N total)

1. **Story Title** (150 pts, 42 comments)
   By username · Jan 15, 2024
   🔗 https://example.com/article
   💬 https://news.ycombinator.com/item?id=12345

2. ...
```

For comments:
```
### HN Comments on "Story Title"

1. **username** (12 pts) · Jan 15, 2024
   > First ~200 chars of the comment text...
   💬 https://news.ycombinator.com/item?id=12345
```

## Error Handling

- **Empty results:** Tell the user no results were found. Suggest broadening the query or removing filters.
- **API error / timeout:** Retry once. If still failing, inform the user the HN search API may be temporarily down.
- **Rate limited (429):** Unlikely at 10k/hr, but if hit, wait 60 seconds and retry.
- **Malformed response:** Check the URL construction — common issues are unencoded special characters in the query.

## Examples

### Example 1: "What's HN saying about Rust?"

```
Fetch: https://hn.algolia.com/api/v1/search?query=rust+programming&tags=story&hitsPerPage=5&numericFilters=points>50
```

### Example 2: "Find Show HN posts about AI agents from the last month"

```
# Calculate timestamp for 30 days ago, then:
Fetch: https://hn.algolia.com/api/v1/search_by_date?query=ai+agents&tags=show_hn&numericFilters=created_at_i>TIMESTAMP&hitsPerPage=10
```

### Example 3: "What has pg posted recently?"

```
Fetch: https://hn.algolia.com/api/v1/search_by_date?tags=author_pg&hitsPerPage=10
```

## Data Source

[Algolia HN Search API](https://hn.algolia.com/api) — Free, no authentication required.
Indexes all public Hacker News content in near real-time.
