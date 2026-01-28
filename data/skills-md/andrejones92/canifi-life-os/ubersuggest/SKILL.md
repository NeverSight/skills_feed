---
name: ubersuggest
description: Research keywords and SEO with Neil Patel's Ubersuggest tool.
category: marketing
---
# Ubersuggest Skill

Research keywords and SEO with Neil Patel's Ubersuggest tool.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/ubersuggest/install.sh | bash
```

Or manually:
```bash
cp -r skills/ubersuggest ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set UBERSUGGEST_API_KEY "your_api_key"
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

1. **Keyword Ideas**: Generate keyword suggestions
2. **Traffic Analysis**: Estimate domain traffic
3. **Content Ideas**: Find popular content by topic
4. **Backlink Data**: Analyze backlink profiles
5. **Site Audit**: Basic technical SEO analysis

## Usage Examples

### Get Keywords
```
User: "Find keyword ideas for 'email marketing'"
Assistant: Returns keyword suggestions with metrics
```

### Traffic Estimate
```
User: "How much traffic does example.com get?"
Assistant: Returns estimated organic traffic
```

### Content Ideas
```
User: "Find popular content about productivity"
Assistant: Returns top-performing content
```

### Check Backlinks
```
User: "Show me backlinks for my domain"
Assistant: Returns backlink summary
```

## Authentication Flow

1. Get API key from Ubersuggest account
2. Use API key for authentication
3. Requests limited by plan
4. Free tier has limited access

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid API key | Verify credentials |
| 403 Forbidden | Limit reached | Upgrade plan |
| 404 Not Found | No data | Try different query |
| 429 Rate Limited | Too many requests | Wait and retry |

## Notes

- Created by Neil Patel
- Free tier available
- Affordable paid plans
- Chrome extension
- Simple interface
- Good for beginners
