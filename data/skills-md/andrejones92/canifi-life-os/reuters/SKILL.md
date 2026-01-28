---
name: reuters
description: Access global news and real-time market data from Reuters news agency.
category: news
---
# Reuters Skill

Access global news and real-time market data from Reuters news agency.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/reuters/install.sh | bash
```

Or manually:
```bash
cp -r skills/reuters ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set REUTERS_API_KEY "your_api_key"
canifi-env set REUTERS_EMAIL "your_email"
canifi-env set REUTERS_PASSWORD "your_password"
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

1. **Breaking News**: Get real-time breaking news and developing stories
2. **Market Data**: Access real-time market data, quotes, and financial news
3. **World Coverage**: Read international news from Reuters global network
4. **Section Browsing**: Browse by World, Business, Markets, Technology sections
5. **Multimedia Content**: Access Reuters photos, videos, and graphics

## Usage Examples

### Get Breaking News
```
User: "Show me Reuters breaking news"
Assistant: Returns latest breaking news stories
```

### Market Updates
```
User: "What's happening in the markets according to Reuters?"
Assistant: Returns market news and major index movements
```

### Search Articles
```
User: "Search Reuters for news about climate summit"
Assistant: Returns relevant articles about climate negotiations
```

### Browse Section
```
User: "Show me Reuters Technology news"
Assistant: Returns latest tech industry coverage
```

## Authentication Flow

1. Reuters Connect API requires enterprise subscription
2. Consumer access via website with account
3. Browser automation for web access
4. API keys for Reuters Connect customers

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid credentials | Verify account or API key |
| 403 Forbidden | Enterprise feature | Upgrade to Reuters Connect |
| Rate Limited | Request limit exceeded | Implement backoff strategy |
| Not Found | Article unavailable | Check article ID |

## Notes

- Consumer website is free with registration
- Reuters Connect API for enterprise customers
- Real-time news wire for professional subscribers
- Available in multiple languages
- Part of Thomson Reuters
- Trusted source for breaking news
