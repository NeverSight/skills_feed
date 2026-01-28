---
name: brandwatch
description: Monitor and analyze social data with Brandwatch's enterprise social intelligence platform.
category: marketing
---
# Brandwatch Skill

Monitor and analyze social data with Brandwatch's enterprise social intelligence platform.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/brandwatch/install.sh | bash
```

Or manually:
```bash
cp -r skills/brandwatch ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set BRANDWATCH_API_KEY "your_api_key"
canifi-env set BRANDWATCH_PROJECT_ID "your_project_id"
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

1. **Social Listening**: Monitor conversations across social and web
2. **Consumer Research**: Analyze consumer trends and insights
3. **Crisis Management**: Detect and respond to brand crises
4. **Influencer Analysis**: Identify and analyze influencers
5. **Dashboards**: Create custom analytics dashboards

## Usage Examples

### Create Query
```
User: "Create a Brandwatch query for our product launch"
Assistant: Sets up monitoring query with filters
```

### Analyze Sentiment
```
User: "What's the sentiment around our brand this week?"
Assistant: Returns sentiment analysis and trends
```

### Find Influencers
```
User: "Find top influencers talking about our industry"
Assistant: Returns influencer list with metrics
```

### Create Dashboard
```
User: "Create a dashboard for campaign monitoring"
Assistant: Sets up dashboard with key metrics
```

## Authentication Flow

1. Get API credentials from Brandwatch
2. Use API key for authentication
3. Project ID scopes data access
4. OAuth for enterprise integrations

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid API key | Verify credentials |
| 403 Forbidden | No project access | Check project permissions |
| 404 Not Found | Query not found | Verify query ID |
| 429 Rate Limited | Too many requests | Implement backoff |

## Notes

- Enterprise social intelligence
- Historical data access
- AI-powered insights
- Image recognition
- Custom dashboards
- Premium pricing
