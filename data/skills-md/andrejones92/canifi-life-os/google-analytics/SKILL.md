---
name: google-analytics
description: Track website and app analytics with Google Analytics 4's comprehensive platform.
category: analytics
---
# Google Analytics Skill

Track website and app analytics with Google Analytics 4's comprehensive platform.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/google-analytics/install.sh | bash
```

Or manually:
```bash
cp -r skills/google-analytics ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set GOOGLE_ANALYTICS_PROPERTY_ID "your_property_id"
canifi-env set GOOGLE_CLIENT_ID "your_client_id"
canifi-env set GOOGLE_CLIENT_SECRET "your_client_secret"
canifi-env set GOOGLE_REFRESH_TOKEN "your_refresh_token"
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

1. **Traffic Analysis**: Monitor website traffic, sources, and user behavior
2. **Conversion Tracking**: Track goals, events, and e-commerce conversions
3. **Audience Insights**: Understand user demographics and interests
4. **Real-time Data**: View live user activity on your properties
5. **Custom Reports**: Create custom reports and explorations

## Usage Examples

### Get Traffic Overview
```
User: "Show me website traffic for the last 7 days"
Assistant: Returns sessions, users, and pageviews
```

### View Top Pages
```
User: "What are my top performing pages?"
Assistant: Returns pages by views and engagement
```

### Check Conversions
```
User: "How many conversions did we get this month?"
Assistant: Returns conversion counts by goal
```

### Real-time Users
```
User: "How many users are on the site right now?"
Assistant: Returns real-time user count and activity
```

## Authentication Flow

1. Create project in Google Cloud Console
2. Enable Analytics API
3. Set up OAuth 2.0 credentials
4. Implement authorization code flow

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Token expired | Refresh access token |
| 403 Forbidden | No property access | Check permissions |
| 404 Not Found | Invalid property ID | Verify property ID |
| 429 Rate Limited | Quota exceeded | Wait for quota reset |

## Notes

- GA4 is the current version
- Universal Analytics deprecated
- Free tier with data limits
- BigQuery export available
- Custom dimensions supported
- Audience export to Google Ads
