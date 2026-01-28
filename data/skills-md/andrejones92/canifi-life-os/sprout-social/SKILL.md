---
name: sprout-social
description: Manage professional social media with Sprout Social's enterprise platform.
category: marketing
---
# Sprout Social Skill

Manage professional social media with Sprout Social's enterprise platform.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/sprout-social/install.sh | bash
```

Or manually:
```bash
cp -r skills/sprout-social ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set SPROUT_API_KEY "your_api_key"
canifi-env set SPROUT_ACCESS_TOKEN "your_access_token"
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

1. **Publishing**: Schedule and publish across all social networks
2. **Smart Inbox**: Unified inbox for all social messages
3. **Social Listening**: Monitor brand mentions and sentiment
4. **Analytics**: Comprehensive reporting and analytics
5. **Employee Advocacy**: Manage employee social sharing

## Usage Examples

### Publish Post
```
User: "Schedule a LinkedIn post for the company page"
Assistant: Creates and schedules post
```

### Check Inbox
```
User: "Show me unread messages in Sprout Social inbox"
Assistant: Returns unread social messages
```

### Get Report
```
User: "Generate a social media report for last month"
Assistant: Creates report with key metrics
```

### Monitor Brand
```
User: "Show me recent brand mentions"
Assistant: Returns social listening results
```

## Authentication Flow

1. Get API credentials from Sprout Social
2. Implement OAuth 2.0 authorization
3. Request appropriate permissions
4. Store tokens securely

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Token expired | Refresh token |
| 403 Forbidden | Feature not available | Check plan tier |
| 404 Not Found | Resource not found | Verify ID |
| 429 Rate Limited | Too many requests | Implement backoff |

## Notes

- Enterprise-grade social management
- Advanced reporting features
- Social listening included
- Employee advocacy tools
- CRM integrations
- Premium pricing
