---
name: nytimes
description: Access premium journalism and news coverage from The New York Times.
category: news
---
# New York Times Skill

Access premium journalism and news coverage from The New York Times.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/nytimes/install.sh | bash
```

Or manually:
```bash
cp -r skills/nytimes ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set NYTIMES_API_KEY "your_api_key"
canifi-env set NYTIMES_EMAIL "your_email"
canifi-env set NYTIMES_PASSWORD "your_password"
```

## Privacy & Authentication

**Your credentials, your choice.** Canifi LifeOS respects your privacy.

### Option 1: Manual Browser Login (Recommended)
If you prefer not to share credentials with Claude Code:
1. Complete the [Browser Automation Setup](/setup/automation) using CDP mode
2. Login to the service manually in the Playwright-controlled Chrome window
3. Claude will use your authenticated session without ever seeing your password

### Option 2: Environment Variables
If you're comfortable sharing credentials, you can store them locally:
```bash
canifi-env set SERVICE_EMAIL "your-email"
canifi-env set SERVICE_PASSWORD "your-password"
```

**Note**: Credentials stored in canifi-env are only accessible locally on your machine and are never transmitted.

## Capabilities

1. **Article Access**: Read articles across news, opinion, and feature sections
2. **Section Browsing**: Browse by section including World, Politics, Business, Tech
3. **Search Archives**: Search the complete NYT archive dating back to 1851
4. **Saved Articles**: Save articles to your account for later reading
5. **Newsletter Management**: Subscribe to and manage NYT newsletters

## Usage Examples

### Get Top Stories
```
User: "Show me today's top stories from the New York Times"
Assistant: Returns top headlines from the home section
```

### Search Articles
```
User: "Search NYT for articles about artificial intelligence from the last month"
Assistant: Returns matching articles with headlines and summaries
```

### Browse Section
```
User: "Show me the latest NYT Technology articles"
Assistant: Returns recent technology section articles
```

### Save Article
```
User: "Save this NYT article to my account"
Assistant: Saves article to your NYT saved list
```

## Authentication Flow

1. Register for API key at developer.nytimes.com
2. API key provides access to article search and top stories
3. Full article access requires subscription
4. Use credentials for authenticated features

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid API key | Verify API key |
| 403 Forbidden | Subscription required | Subscribe to access full articles |
| 429 Rate Limited | API limit exceeded | Wait and retry with backoff |
| 404 Not Found | Article not found | Check article URL or ID |

## Notes

- Free API tier: 500 requests/day, 5 requests/minute
- Subscription required for full article access
- Archive API covers 1851 to present
- Games and Cooking require separate subscriptions
- Wirecutter reviews included with subscription
