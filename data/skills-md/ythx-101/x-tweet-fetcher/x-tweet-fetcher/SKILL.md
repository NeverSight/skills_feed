---
name: x-tweet-fetcher
description: >
  Fetch tweets from X/Twitter without login or API keys.
  Supports regular tweets, long tweets, quoted tweets, and full X Articles.
  Zero dependencies, zero configuration.
---

# X Tweet Fetcher

Fetch tweets from X/Twitter without authentication. Uses FxTwitter API.

## What It Can Fetch

| Content Type | Support |
|-------------|---------|
| Regular tweets | ✅ Full text + stats |
| Long tweets (Twitter Blue) | ✅ Full text |
| X Articles (long-form) | ✅ Complete article text |
| Quoted tweets | ✅ Included |
| Stats (likes/RT/views) | ✅ Included |

## Usage

### CLI

```bash
# JSON output
python3 scripts/fetch_tweet.py --url "https://x.com/user/status/123456"

# Pretty JSON
python3 scripts/fetch_tweet.py --url "https://x.com/user/status/123456" --pretty

# Text only (human readable)
python3 scripts/fetch_tweet.py --url "https://x.com/user/status/123456" --text-only
```

### From Agent Code

```python
from scripts.fetch_tweet import fetch_tweet

result = fetch_tweet("https://x.com/user/status/123456")
tweet = result["tweet"]

# Regular tweet
print(tweet["text"])

# X Article (long-form)
if tweet["is_article"]:
    print(tweet["article"]["title"])
    print(tweet["article"]["full_text"])  # Complete article
    print(tweet["article"]["word_count"])
```

## Output Format

```json
{
  "url": "https://x.com/user/status/123",
  "username": "user",
  "tweet_id": "123",
  "tweet": {
    "text": "Tweet content...",
    "author": "Display Name",
    "screen_name": "username",
    "likes": 100,
    "retweets": 50,
    "bookmarks": 25,
    "views": 10000,
    "replies_count": 30,
    "created_at": "Mon Jan 01 12:00:00 +0000 2026",
    "is_note_tweet": false,
    "is_article": true,
    "article": {
      "title": "Article Title",
      "full_text": "Complete article content...",
      "word_count": 4847,
      "char_count": 27705
    }
  }
}
```

## Requirements

- Python 3.7+
- No external packages (stdlib only)
- No API keys
- No login required

## How It Works

Uses [FxTwitter](https://github.com/FxEmbed/FxEmbed) public API (`api.fxtwitter.com`) which proxies X/Twitter content. Articles are returned as structured blocks and reassembled into full text.

## Limitations

- Cannot fetch reply threads (only reply counts available via `replies_count` field)
  - Reply content would require browser automation dependencies (Camofox/Nitter)
  - These were removed to maintain zero-dependency architecture
  - `--replies` flag exists but returns an explanatory error message
- Cannot fetch deleted or private tweets
- Rate limits depend on FxTwitter service availability
- If FxTwitter goes down, the skill won't work (no fallback)

## File Structure

```
skills/x-tweet-fetcher/
├── SKILL.md              (this file)
└── scripts/
    └── fetch_tweet.py    (single file, zero deps)
```
