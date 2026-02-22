---
name: read-x
description: Read X/Twitter posts and articles — no API key, no auth, no browser needed. Uses FxTwitter API to fetch full tweet content, media, engagement stats, and long-form articles.
---

# Read X

Fetch full content from X/Twitter posts and articles — no API key, no auth, no browser needed.

## How It Works

Use the [FxTwitter API](https://github.com/FixTweet/FxTwitter) — a public, no-auth API that returns full tweet JSON including embedded articles, media, and engagement stats.

## Endpoint

```
https://api.fxtwitter.com/{username}/status/{tweet_id}
```

## When to Use

- User shares an x.com or twitter.com URL
- User asks to read/summarize an X post or article
- User shares a thread or long-form X article

## When NOT to Use

- User just wants to post/reply on X (this is read-only)
- URL is not a post (e.g., x.com/username profile page)

## How to Fetch

Use `web_fetch` on the fxtwitter URL:

```
web_fetch: https://api.fxtwitter.com/{username}/status/{tweet_id}
```

### Extracting from the URL

Given: `https://x.com/elonmusk/status/1234567890`
- username: `elonmusk`
- tweet_id: `1234567890`
- API URL: `https://api.fxtwitter.com/elonmusk/status/1234567890`

## Response Structure

The API returns JSON with:

- `tweet.text` — tweet text
- `tweet.author` — author info (name, handle, followers, bio)
- `tweet.likes`, `tweet.retweets`, `tweet.views` — engagement
- `tweet.article` — full long-form article content (if present)
  - `tweet.article.title` — article title
  - `tweet.article.content.blocks[]` — article body (block-based, like Draft.js)
    - Each block has `text`, `type` (unstyled, header-two, blockquote, atomic), and `inlineStyleRanges` (Bold, Italic)
- `tweet.media` — attached images/videos
- `tweet.replying_to` — if it's a reply, who it's replying to

## Rendering Articles

When `tweet.article` exists, render it as clean markdown:
- `header-two` → `## heading`
- `blockquote` → `> quote`
- `Bold` inline style → `**bold**`
- `Italic` inline style → `*italic*`
- `atomic` with DIVIDER entity → `---`
- Links in `entityMap` → `[text](url)`

## Limitations

- Read-only (no posting, liking, replying)
- Some tweets may be unavailable (deleted, protected accounts)
- Rate limits exist but are generous for casual use
- Threads: each tweet is a separate request (follow `replying_to` chain)
