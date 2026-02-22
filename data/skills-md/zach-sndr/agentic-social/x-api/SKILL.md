---
name: x-api
description: |
    X (Twitter) API v2 integration for posting tweets, replies, quotes, managing posts, sending DMs, searching tweets, and retrieving timeline/user activity.

    Use when the user needs to interact with X (Twitter) API:
    - Post content: tweets, replies, quotes, posts with media
    - Manage posts: delete, retweet, like
    - Direct Messages: send DMs with optional media attachments
    - Search: search tweets by keyword, hashtag, user, with filters
    - Retrieve data: user recent activity, home timeline
    - Extract tweet IDs from URLs

    Requires OAuth 1.0a credentials: X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_SECRET.
---

# X API Skill

Interact with X (Twitter) API v2 through Python scripts and client library.

## Quick Start

Set up credentials in `/root/.env`:
```
X_API_KEY=your_api_key_here
X_API_SECRET=your_api_secret_here
X_ACCESS_TOKEN=your_access_token_here
X_ACCESS_SECRET=your_access_token_secret_here
```

Or set environment variables directly:
```bash
export X_API_KEY=your_api_key_here
export X_API_SECRET=your_api_secret_here
export X_ACCESS_TOKEN=your_access_token_here
export X_ACCESS_SECRET=your_access_token_secret_here
```

## Available Scripts

All scripts are located in `scripts/` directory and can be run directly.

### Posting Content

**Post a tweet:**
```bash
python3 scripts/post_tweet.py "Hello world!"
```

**Post a reply:**
```bash
python3 scripts/post_reply.py "Reply text" "https://x.com/user/status/123456789"
```

**Post a quote tweet:**
```bash
python3 scripts/post_quote.py "Quote comment" "https://x.com/user/status/123456789"
```

**Post with media:**
```bash
python3 scripts/post_with_media.py "Caption" /path/to/image.jpg
```

### Managing Posts

**Delete a post:**
```bash
python3 scripts/delete_post.py "https://x.com/user/status/123456789"
# or with just the ID:
python3 scripts/delete_post.py "123456789"
```

**Retweet:**
```bash
python3 scripts/retweet.py "https://x.com/user/status/123456789"
```

**Like a post:**
```bash
python3 scripts/like_post.py "https://x.com/user/status/123456789"
```

### Direct Messages

**Send a DM:**
```bash
python3 scripts/send_dm.py username "Message text"
```

**Send a DM with media:**
```bash
python3 scripts/send_dm.py username "Check this out" /path/to/image.jpg
```

### Retrieving Data

**Get user's recent activity:**
```bash
# Last 2 hours
python3 scripts/recent_activity.py elonmusk 2hrs

# Last 8 hours, 20 posts
python3 scripts/recent_activity.py nasa 8hrs 20

# Last 1 day
python3 scripts/recent_activity.py github 1d 50
```

**Get home timeline:**
```bash
# Last 10 posts (default)
python3 scripts/get_timeline.py

# Last 20 posts
python3 scripts/get_timeline.py 20

# Exclude replies and retweets
python3 scripts/get_timeline.py 30 replies,retweets
```

**Search tweets:**
```bash
# Basic search
python3 scripts/search_tweets.py "#python"

# Search by user
python3 scripts/search_tweets.py "from:nasa"

# Search with time filter (last 24 hours)
python3 scripts/search_tweets.py "machine learning" 20 24h

# Complex search with hashtag filter
python3 scripts/search_tweets.py "#crypto has:images" 10
```

## Python Client Library

For advanced usage, import the client directly:

```python
from scripts.x_api_client import get_client

client = get_client()

# Post a tweet
result = client.post_tweet("Hello!")

# Post with media
result = client.post_with_media("Caption", "/path/to/image.jpg")

# Get user posts
posts = client.get_user_posts("username", "2hrs", max_results=20)

# Get timeline
timeline = client.get_timeline(count=50)
```

### Client Methods

**Posting:**
- `post_tweet(text, reply_to_id=None, quote_tweet_id=None, media_ids=None, reply_settings=None)`
- `post_reply(text, parent_post_link, **kwargs)`
- `post_quote(text, child_post_link, **kwargs)`
- `post_with_media(text, media_location, **kwargs)`

**Managing:**
- `delete_post(post_link)`
- `retweet(child_post_link, user_id=None)`
- `like_post(post_link, user_id=None)`

**DMs:**
- `send_dm(recipient_handle, text, media_path=None)`

**Retrieving:**
- `get_user_posts(username, timeframe=None, max_results=10)`
- `get_timeline(count=10, user_id=None, exclude=None)`
- `search_tweets(query, max_results=10, start_time=None, end_time=None, since_id=None, until_id=None)`

**Utilities:**
- `extract_tweet_id(tweet_url_or_id)` - Extract ID from URL
- `get_user_id_from_username(username)` - Get numeric user ID
- `upload_media(media_path, media_category="tweet_image")` - Upload media

## Authentication

This skill uses OAuth 1.0a authentication (user context) with HMAC-SHA256 signature generation.

Required credentials (get these from the X Developer Portal):
- `X_API_KEY` - Consumer Key (API Key)
- `X_API_SECRET` - Consumer Secret (API Secret)
- `X_ACCESS_TOKEN` - Access Token
- `X_ACCESS_SECRET` - Access Token Secret

These credentials are automatically loaded from:
1. Environment variables
2. `/root/.env` file
3. Legacy `TWITTER_*` environment variables (for compatibility)

Required permissions/scopes for your access token:
- `tweet.write` - Post and repost
- `tweet.read` - View posts
- `users.read` - View users
- `dm.write` - Send DMs
- `like.write` - Like posts
- `media.write` - Upload media

## API Endpoints Used

| Function | Endpoint |
|----------|----------|
| Post/Reply/Quote | `POST /2/tweets` |
| Delete | `DELETE /2/tweets/{id}` |
| Retweet | `POST /2/users/{id}/retweets` |
| Like | `POST /2/users/{id}/likes` |
| Send DM | `POST /2/dm_conversations/with/{participant_id}/messages` |
| User Posts | `GET /2/users/{id}/tweets` |
| Timeline | `GET /2/users/{id}/timelines/reverse_chronological` |
| Search | `GET /2/tweets/search/recent` |
| Upload Media | `POST /2/media/upload` |
| User by Username | `GET /2/users/by/username/{username}` |
| Me (current user) | `GET /2/users/me` |

## Error Handling

The client provides clear error messages:
- `XAPIAuthenticationError` - Invalid or missing credentials
- `XAPIRateLimitError` - Rate limit exceeded
- `XAPIClientError` - General API errors

## Time Format

The `timeframe` parameter accepts formats like:
- `2hrs`, `8hrs`, `24hrs` - Hours
- `1d`, `2d` - Days
- `1w`, `2w` - Weeks
- `30min` - Minutes

## Search Operators

The search query supports X (Twitter) API v2 search operators:

| Operator | Example | Description |
|----------|---------|-------------|
| `from:username` | `from:nasa` | Tweets from specific user |
| `to:username` | `to:elonmusk` | Tweets replying to user |
| `@username` | `@openclaw` | Tweets mentioning user |
| `#hashtag` | `#python` | Tweets with hashtag |
| `"phrase"` | `"machine learning"` | Exact phrase match |
| `AND` | `ai AND ethics` | Both keywords |
| `OR` | `cat OR dog` | Either keyword |
| `-keyword` | `crypto -scam` | Exclude keyword |
| `has:images` | `#sunset has:images` | Tweets with images |
| `has:videos` | `has:videos` | Tweets with videos |
| `has:links` | `has:links` | Tweets with links |
| `lang:xx` | `lang:en` | Language filter (ISO 639-1) |
| `is:verified` | `is:verified` | Only verified users |
| `min_retweets:N` | `min_retweets:5` | Minimum retweets |
| `min_faves:N` | `min_faves:10` | Minimum likes |
| `is:reply` | `is:reply` | Only replies |
| `is:quote_tweet` | `is:quote_tweet` | Only quote tweets |
