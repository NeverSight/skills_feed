---
name: x-api
description: Unified Twitter/X API client for retrieving user info and tweets via twitterapi.io. Supports user lookup and advanced tweet search with a clean Typer-based CLI and agent-friendly Python interface.
---

# X (Twitter) API Skill via twitterapi.io

A unified Twitter/X API client providing access to user information and advanced tweet search through twitterapi.io. Built with Typer for a clean CLI experience and designed to be agent-friendly for programmatic usage.

## CLI Usage

The unified client (`.claude/skills/x-api/src/twitter.py`) provides two subcommands with structured JSON output.

### 1. Get User Info

Retrieve user information by screen name. Returns a structured response with user information.

**Note**: The calculated fields (`last_tweet_date`, `last_reply_date`, `is_hebrew_writer`) are set to default values and require a separate search call using `search from:{username}` to populate.

```bash
python3 twitter.py userinfo <screenname>

# Example:
python3 twitter.py userinfo elonmusk
```

**Response Format:**

The userinfo command returns a `UserInfoResponse` Pydantic model with the following structure:

```json
{
  "status": "active",
  "profile": "https://pbs.twimg.com/profile_images/...",
  "blue_verified": true,
  "verification_type": "Business",
  "affiliates": {},
  "business_account": {},
  "desc": "User bio description",
  "name": "Display Name",
  "website": "example.com",
  "protected": false,
  "location": "Location",
  "following": 100,
  "followers": 1000,
  "statuses_count": 5000,
  "media_count": 50,
  "created_at": "2020-01-01T00:00:00.000Z",
  "last_tweet_date": null,
  "last_reply_date": null,
  "is_hebrew_writer": false
}
```

### 2. Search Tweets

Search for tweets matching a query with optional search type filtering. Returns a filtered response excluding `next_cursor`, and omitting `id` and `media` fields from each tweet.

```bash
python3 twitter.py search <query> [--type Top|Latest|Media|People|Lists]

# Basic Examples:
python3 twitter.py search "artificial intelligence" --type Latest
python3 twitter.py search SpaceX
python3 twitter.py search "developers" --type People
python3 twitter.py search "tech lists" --type Lists
```

**Response Format:**

The search command returns a `SearchResponse` Pydantic model with the following structure:

```json
{
  "timeline": [
    {
      "screen_name": "fishcatut",
      "bookmarks": 9,
      "favorites": 241,
      "created_at": "2023-09-16T18:08:33.000Z",
      "text": "What's going on here #cybertruck #tesla",
      "lang": "iw",
      "quotes": 14,
      "replies": 42,
      "retweets": 19
    }
  ]
}
```

#### Advanced Search Operators

The search endpoint supports Twitter's advanced search syntax for precise filtering:

**User Filters:**
```bash
# Posts from a specific user
python3 twitter.py search "from:elonmusk Tesla"

# Posts directed to a user
python3 twitter.py search "to:NASA space"
```

**Date Filters:**
```bash
# Posts since a specific date
python3 twitter.py search "AI since:2025-01-01"

# Posts within a date range
python3 twitter.py search "climate change since:2025-01-01 until:2025-01-31"

# Using Unix timestamps for precise timing
python3 twitter.py search "breaking news since_time:1704067200"
```

**Content Type Filters:**
```bash
# Posts with images only
python3 twitter.py search "sunset filter:images"

# Posts with videos
python3 twitter.py search "tutorial filter:videos"

# Posts with links
python3 twitter.py search "article filter:links"

# Reply posts only
python3 twitter.py search "question filter:replies"
```

**Language Filter:**
```bash
# Posts in specific language (ISO 639-1 codes)
python3 twitter.py search "technology lang:iw"
```

**Exclusion Operator:**
```bash
# Exclude specific terms (use minus operator)
python3 twitter.py search "from:NASA -Mars"
python3 twitter.py search "Python -snake"
```

**Combined Queries:**
```bash
# Complex multi-filter search
python3 twitter.py search "from:elonmusk since:2025-01-01 until:2025-01-07 Tesla -filter:replies"

# Search for content with media from specific user in date range
python3 twitter.py search "from:NASA filter:images since:2025-01-01"
```

## Common Use Cases

- **Research**: Retrieve and analyze user information, search for specific topics
- **Data Collection**: Gather tweets, replies, and user information for analysis
- **Validation**: Verify Twitter usernames or number of followers
- **Engagement Analysis**: Analyze replies and interactions on specific tweets

## Error Handling

Common error scenarios:
- **401 Unauthorized**: Invalid or missing API key - verify `XAPI_IO_API_KEY` is set in your `.env` file
- **429 Too Many Requests**: Rate limit exceeded - implement delays between requests
- **404 Not Found**: User/tweet not found - verify usernames are correct
- **500 Server Error**: twitterapi.io service issue - retry with exponential backoff

The `TwitterAPIClient` automatically handles these errors and provides clear error messages.

## Configuration

Set the following environment variable in your `.env` file:

```bash
XAPI_IO_API_KEY=your_api_key_here
```

You can obtain an API key from [twitterapi.io](https://twitterapi.io).
