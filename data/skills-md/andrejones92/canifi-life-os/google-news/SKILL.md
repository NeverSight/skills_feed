---
name: google-news
description: Stay informed with Google's AI-powered news aggregator and personalized headlines.
category: news
---
# Google News Skill

Stay informed with Google's AI-powered news aggregator and personalized headlines.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/google-news/install.sh | bash
```

Or manually:
```bash
cp -r skills/google-news ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set GOOGLE_ACCOUNT_EMAIL "your_email"
canifi-env set GOOGLE_ACCOUNT_PASSWORD "your_password"
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

1. **Personalized Headlines**: Get news personalized based on interests and search history
2. **Topic Coverage**: Follow topics for comprehensive coverage from multiple sources
3. **Full Coverage**: View complete story coverage with different perspectives
4. **Location News**: Get local news based on your location
5. **Fact Check**: Access fact-check labels and source credibility information

## Usage Examples

### Get Headlines
```
User: "Show me today's top headlines from Google News"
Assistant: Returns personalized top stories and breaking news
```

### Follow Topic
```
User: "Follow 'Climate Change' topic on Google News"
Assistant: Adds topic to your followed interests for ongoing coverage
```

### Full Coverage
```
User: "Show full coverage for the latest tech industry story"
Assistant: Returns multiple perspectives and sources for the story
```

### Local News
```
User: "What's happening in San Francisco today?"
Assistant: Returns local news for San Francisco area
```

## Authentication Flow

1. Uses Google account authentication
2. OAuth 2.0 for third-party access
3. Personalization requires signed-in account
4. Cross-device sync with Google account

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Auth Failed | Invalid Google credentials | Re-authenticate with Google |
| Region Limited | Content not available | Check regional restrictions |
| Rate Limited | Too many requests | Implement request throttling |
| Topic Not Found | Invalid topic ID | Search for valid topic |

## Notes

- Free service with Google account
- AI-powered story clustering
- Available in 120+ countries
- Newsstand for magazine subscriptions
- Web, iOS, and Android apps
- Privacy controls in Google account settings
