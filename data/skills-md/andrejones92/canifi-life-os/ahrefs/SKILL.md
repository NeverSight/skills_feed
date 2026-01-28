---
name: ahrefs
description: Research backlinks and SEO with Ahrefs' comprehensive SEO toolkit.
category: marketing
---
# Ahrefs Skill

Research backlinks and SEO with Ahrefs' comprehensive SEO toolkit.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/ahrefs/install.sh | bash
```

Or manually:
```bash
cp -r skills/ahrefs ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set AHREFS_API_TOKEN "your_api_token"
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

1. **Backlink Analysis**: Analyze backlink profiles and referring domains
2. **Keyword Explorer**: Research keywords with metrics
3. **Site Explorer**: Analyze organic traffic and top pages
4. **Content Explorer**: Find popular content by topic
5. **Rank Tracker**: Monitor keyword rankings

## Usage Examples

### Analyze Backlinks
```
User: "Show me backlinks for example.com"
Assistant: Returns backlink profile with metrics
```

### Keyword Research
```
User: "Research keywords for 'content marketing'"
Assistant: Returns keyword ideas with difficulty and volume
```

### Top Pages
```
User: "What are the top performing pages on competitor.com?"
Assistant: Returns top pages by organic traffic
```

### Find Content
```
User: "Find popular content about SEO"
Assistant: Returns top-shared content on the topic
```

## Authentication Flow

1. Get API token from Ahrefs account
2. Use Bearer token authentication
3. Credits consumed per request
4. Rate limits apply

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid token | Verify API token |
| 403 Forbidden | No credits | Add more credits |
| 404 Not Found | No data | Check domain/keyword |
| 429 Rate Limited | Too many requests | Wait and retry |

## Notes

- Industry-leading backlink database
- Trillion-link index
- Hourly updated rankings
- Content explorer for research
- Site audit tool
- Subscription-based pricing
