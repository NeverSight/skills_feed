---
name: medium-paywall-bypass
description: Use when user shares a Medium article URL behind a paywall and wants to read the full content. Also use for articles on Medium-hosted publications like towardsdatascience.com, betterprogramming.pub, levelup.gitconnected.com, etc.
---

# Medium Paywall Bypass

## Overview
Fetch paywalled Medium articles using free mirror services. Try services in order until one works.

## Service Priority

| Service | URL Pattern | WebFetch | curl | Notes |
|---------|-------------|----------|------|-------|
| **Freedium** | `https://freedium.cfd/{encoded_url}` | Yes | Yes | Best option, returns content directly |
| **Archive.today** | `https://archive.today/latest/{raw_url}` | No | Maybe | Often requires captcha |
| **RemovePaywalls** | `https://removepaywalls.com/{raw_url}` | No | No | Redirect page only, needs browser |
| **ReadMedium** | `https://readmedium.com/en/{encoded_url}` | No | No | Returns 403 programmatically |

- `{encoded_url}` = URL-encoded (slashes become %2F, @ becomes %40, etc.)
- `{raw_url}` = Original URL as-is

**For Claude Code: Use Freedium via WebFetch.** Other services require browser interaction.

## Workflow

```
1. User provides Medium URL
2. Try Freedium first via WebFetch
3. If blocked/empty, try next service
4. Extract and present article content
```

## Example Usage

Given: `https://medium.com/@user/some-article-abc123`

**WebFetch (recommended):**
```
URL: https://freedium.cfd/https%3A%2F%2Fmedium.com%2F%40user%2Fsome-article-abc123
Prompt: Extract the full article content
```

**curl fallback:**
```bash
curl -sL "https://freedium.cfd/https%3A%2F%2Fmedium.com%2F%40user%2Fsome-article-abc123"
```

## Medium-Hosted Domains

These domains use Medium's paywall system:
- `medium.com`, `*.medium.com`
- `towardsdatascience.com`
- `betterprogramming.pub`
- `levelup.gitconnected.com`
- `javascript.plainenglish.io`
- `uxdesign.cc`
- `hackernoon.com`
- `codeburst.io`
- `itnext.io`
- `proandroiddev.com`
- `infosecwriteups.com`

## Common Issues

| Problem | Solution |
|---------|----------|
| Freedium down | Try alternative mirror: `freedium-mirror.cfd` |
| Article not found | Article may be too new to be cached |
| Garbled HTML | Use WebFetch with prompt: "Extract the article text and format as markdown" |
| 403/blocked | Try curl with `dangerouslyDisableSandbox: true` |

## Quick Reference

```python
# URL encoding in Python
from urllib.parse import quote
encoded = quote(url, safe='')

# For WebFetch tool
freedium_url = f"https://freedium.cfd/{quote(medium_url, safe='')}"
```
