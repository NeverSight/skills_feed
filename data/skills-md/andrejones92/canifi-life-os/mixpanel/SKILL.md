---
name: mixpanel
description: Track product analytics and user behavior with Mixpanel's event-based platform.
category: analytics
---
# Mixpanel Skill

Track product analytics and user behavior with Mixpanel's event-based platform.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/mixpanel/install.sh | bash
```

Or manually:
```bash
cp -r skills/mixpanel ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set MIXPANEL_TOKEN "your_project_token"
canifi-env set MIXPANEL_API_SECRET "your_api_secret"
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

1. **Event Tracking**: Track custom events and user actions
2. **User Analytics**: Analyze user behavior and cohorts
3. **Funnel Analysis**: Build and analyze conversion funnels
4. **Retention Reports**: Track user retention over time
5. **A/B Testing**: Run experiments and analyze results

## Usage Examples

### Track Event
```
User: "Track a 'Purchase Complete' event in Mixpanel"
Assistant: Sends event with properties to Mixpanel
```

### View Funnel
```
User: "Show me the checkout funnel conversion rate"
Assistant: Returns funnel steps and conversion rates
```

### Analyze Retention
```
User: "What's our user retention for the past month?"
Assistant: Returns retention cohort analysis
```

### User Profile
```
User: "Show me activity for user john@company.com"
Assistant: Returns user profile and event history
```

## Authentication Flow

1. Get project token from Mixpanel settings
2. Get API secret for export APIs
3. Token for tracking, secret for reading
4. Service account for server-side access

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid credentials | Verify token/secret |
| 403 Forbidden | No project access | Check permissions |
| 400 Bad Request | Invalid query | Fix query syntax |
| 429 Rate Limited | Too many requests | Implement backoff |

## Notes

- Event-based analytics platform
- Free tier up to 100K users
- Real-time data processing
- Data warehouse integration
- SDKs for all platforms
- GDPR compliant
