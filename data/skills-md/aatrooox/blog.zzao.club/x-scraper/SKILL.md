---
name: x-scraper
description: Scrape public posts from X.com (Twitter) users. Extracts text content, timestamps, engagement metrics (views, likes, retweets, replies), and generates direct post links. Use when user asks to scrape/fetch/analyze X.com posts or Twitter data, or mentions "整理@某人的发言" or "看看某人在X上说了什么".
---

# X.com Post Scraper

Extracts recent posts from X.com users with full engagement data using authenticated cookies.

## Quick Start

**Basic command**:
```bash
cd .opencode/skills/x-scraper/scripts
python3 scraper.py <username> [count]
```

**Example**:
```bash
python3 scraper.py example_user 15
```

**Output**: `/tmp/x_{username}_posts.json`

---

## Prerequisites

Before first use, verify environment requirements:

1. **Python 3.11+**: Check with `python3 --version`
2. **Playwright**: Check with `python3 -c "import playwright"`
3. **Cookie file**: Check with `ls /tmp/x_cookies_pw.json`

**If any prerequisite is missing**, see [references/setup.md](references/setup.md) for detailed installation and configuration guide.

---

## Common Workflows

### First-time setup
See [references/setup.md](references/setup.md) for complete environment configuration.

### Daily scraping
```bash
python3 scraper.py <username> [count]
```

### Custom cookie file
```bash
python3 scraper.py <username> [count] --cookie-file /path/to/cookies.json
```

### Troubleshooting
If scraper fails, see [references/troubleshooting.md](references/troubleshooting.md) for common issues and solutions.

---

## Output Format

```json
{
  "index": 1,
  "username": "example_user",
  "postId": "1234567890123456789",
  "publishTime": "2025-12-03T18:28:32.000Z",
  "postLink": "https://x.com/example_user/status/1234567890123456789",
  "textContent": "Post text content...",
  "views": "471K",
  "likes": "1.1K",
  "retweets": "153",
  "replies": "44"
}
```

**Key fields**:
- `postLink` - Direct URL to post
- `publishTime` - ISO 8601 timestamp
- `views/likes/retweets/replies` - Abbreviated metrics (K, M)

---

## When to Use This Skill

Trigger when user requests:
- "整理 @某人 最近的发言"
- "看看某人在X上说了什么"
- "Scrape X.com posts from @username"
- "Get latest tweets from user"
- "Analyze X user's recent posts"

---

## Available Scripts

### `scraper.py` - Main scraper
```bash
python3 scraper.py <username> [count] [--cookie-file <path>]
```
- Scrapes user timeline with replies
- Default count: 10 posts
- Default cookie: `/tmp/x_cookies_pw.json`

### `convert_cookies.py` - Cookie converter
```bash
python3 convert_cookies.py <input-file> [output-file]
```
- Converts Cookie-Editor JSON to Playwright format
- Required before first scraping

---

## Reference Documents

- **[setup.md](references/setup.md)** - Complete environment setup guide (Python, Playwright, cookies)
- **[troubleshooting.md](references/troubleshooting.md)** - Error diagnosis and solutions
- **[usage.md](references/usage.md)** - Detailed usage examples and advanced options

---

## Limitations

- Requires X.com authentication cookies
- Cookies expire (~7 days), need re-export
- Rate limits may apply
- Cannot access private/protected accounts
