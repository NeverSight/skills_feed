---
name: x-api
displayName: X/Twitter API
description: Read and post to X/Twitter via API. Check mentions, post tweets, search. Uses OAuth 2.0 user context with token refresh.
version: 0.1.0
author: joel
tags:
  - social
  - x
  - twitter
  - api
---

# X/Twitter API Skill

Basic X (Twitter) API access for the @joelclaw account until a proper CLI is built (ADR-0119).

## Authentication

OAuth 1.0a User Context. **Tokens do not expire** — no refresh dance needed.

### Secrets (in agent-secrets)

- `x_consumer_key` — API Key (OAuth 1.0a consumer key)
- `x_consumer_secret` — API Key Secret (OAuth 1.0a consumer secret)
- `x_access_token` — Access Token (OAuth 1.0a, format: `numeric-alphanumeric`)
- `x_access_token_secret` — Access Token Secret (OAuth 1.0a)

### Signing requests

OAuth 1.0a requires cryptographic signing. Use `requests-oauthlib` (Python) or equivalent:

```bash
export CK=$(secrets lease x_consumer_key)
export CS=$(secrets lease x_consumer_secret)
export AT=$(secrets lease x_access_token)
export ATS=$(secrets lease x_access_token_secret)

uv run --with requests-oauthlib python3 << 'PYEOF'
import os
from requests_oauthlib import OAuth1Session

client = OAuth1Session(
    os.environ['CK'],
    client_secret=os.environ['CS'],
    resource_owner_key=os.environ['AT'],
    resource_owner_secret=os.environ['ATS'],
)

r = client.get("https://api.twitter.com/2/users/me")
print(r.json())
PYEOF
```

### Revoke leases after use

```bash
secrets revoke --all
```

## Account Info

- **Account**: @joelclaw
- **User ID**: 2022779096049311744
- **Scopes**: Read and write (OAuth 1.0a app permissions)

## Common Operations

All operations require OAuth 1.0a signing. Use the Python pattern from Authentication section above, then:

### Common API calls (inside OAuth1Session)

```python
# Check mentions
r = client.get("https://api.twitter.com/2/users/2022779096049311744/mentions",
    params={"max_results": 10, "tweet.fields": "created_at,author_id,text",
            "expansions": "author_id", "user.fields": "username,name"})

# Get my timeline
r = client.get("https://api.twitter.com/2/users/2022779096049311744/tweets",
    params={"max_results": 10, "tweet.fields": "created_at,public_metrics"})

# Post a tweet
r = client.post("https://api.twitter.com/2/tweets", json={"text": "your tweet"})

# Reply to a tweet
r = client.post("https://api.twitter.com/2/tweets",
    json={"text": "@user reply", "reply": {"in_reply_to_tweet_id": "TWEET_ID"}})

# Search recent tweets
r = client.get("https://api.twitter.com/2/tweets/search/recent",
    params={"query": "joelclaw", "max_results": 10, "tweet.fields": "created_at,author_id,text"})

# Get user by username
r = client.get("https://api.twitter.com/2/users/by/username/USERNAME",
    params={"user.fields": "description,public_metrics"})

# Follow a user
my_id = "2022779096049311744"
r = client.post(f"https://api.twitter.com/2/users/{my_id}/following",
    json={"target_user_id": "TARGET_USER_ID"})

# Delete a tweet
r = client.delete("https://api.twitter.com/2/tweets/TWEET_ID")
```

## Rate Limits

- Mentions: 180 requests / 15 min
- Post tweet: 200 tweets / 15 min (app-level)
- Search: 180 requests / 15 min
- User lookup: 300 requests / 15 min

## Rules

- **Never engage with shitcoin/scam mentions.** Ignore them entirely.
- **Never post financial advice or token endorsements.**
- **Joel approves all tweets before posting** unless explicitly told otherwise.
- **Always revoke leases after use** — don't leave secrets in memory.
- **OAuth 1.0a tokens don't expire** — no refresh needed. If auth fails, tokens were regenerated in the developer portal.
