---
name: mention
description: Monitor brand mentions and social conversations with Mention's listening platform.
category: marketing
---
# Mention Skill

Monitor brand mentions and social conversations with Mention's listening platform.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/mention/install.sh | bash
```

Or manually:
```bash
cp -r skills/mention ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set MENTION_ACCESS_TOKEN "your_access_token"
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

1. **Brand Monitoring**: Track brand mentions across web and social
2. **Competitive Analysis**: Monitor competitor mentions and activity
3. **Influencer Finding**: Discover relevant influencers by topic
4. **Alert Management**: Set up real-time alerts for mentions
5. **Reporting**: Generate mention reports and analytics

## Usage Examples

### Create Alert
```
User: "Create a Mention alert for our brand name"
Assistant: Sets up monitoring alert with keywords
```

### View Mentions
```
User: "Show me today's brand mentions"
Assistant: Returns recent mentions with sentiment
```

### Analyze Competitor
```
User: "How is our competitor being mentioned this week?"
Assistant: Returns competitor mention analysis
```

### Generate Report
```
User: "Create a monthly mention report"
Assistant: Generates report with trends and insights
```

## Authentication Flow

1. Get access token from Mention settings
2. Use Bearer token for API requests
3. OAuth available for integrations
4. Token provides account access

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid token | Verify access token |
| 403 Forbidden | Alert limit reached | Upgrade plan |
| 404 Not Found | Alert not found | Check alert ID |
| 429 Rate Limited | Too many requests | Implement backoff |

## Notes

- Web and social monitoring
- Real-time alerts via email/Slack
- Sentiment analysis included
- Boolean search support
- Export to CSV/PDF
- Free trial available
