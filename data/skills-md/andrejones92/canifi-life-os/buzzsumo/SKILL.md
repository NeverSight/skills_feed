---
name: buzzsumo
description: Research content performance and discover trending topics with BuzzSumo.
category: marketing
---
# BuzzSumo Skill

Research content performance and discover trending topics with BuzzSumo.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/buzzsumo/install.sh | bash
```

Or manually:
```bash
cp -r skills/buzzsumo ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set BUZZSUMO_API_KEY "your_api_key"
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

1. **Content Analysis**: Analyze most-shared content by topic
2. **Competitor Research**: Monitor competitor content performance
3. **Influencer Discovery**: Find influencers by topic
4. **Trend Monitoring**: Track trending topics and content
5. **Alert Setup**: Set up content and mention alerts

## Usage Examples

### Find Trending Content
```
User: "What's the most shared content about AI this week?"
Assistant: Returns top-performing AI content
```

### Analyze Competitor
```
User: "Show me top-performing content from competitor.com"
Assistant: Returns competitor's best content by shares
```

### Find Influencers
```
User: "Find top influencers in the marketing space"
Assistant: Returns influencer list with metrics
```

### Create Alert
```
User: "Alert me when competitors publish new content"
Assistant: Sets up content monitoring alert
```

## Authentication Flow

1. Get API key from BuzzSumo account
2. Use API key in request parameters
3. Key provides access to all endpoints
4. Rate limits vary by plan

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid API key | Verify API key |
| 403 Forbidden | Quota exceeded | Wait for reset or upgrade |
| 404 Not Found | No results found | Adjust search query |
| 429 Rate Limited | Too many requests | Wait and retry |

## Notes

- Content research and analysis
- Backlink data included
- Question analyzer for Q&A
- Facebook page analyzer
- Chrome extension available
- Free trial with limited searches
