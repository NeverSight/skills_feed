---
name: mailchimp
description: Manage email marketing campaigns and audience with Mailchimp's comprehensive platform.
category: marketing
---
# Mailchimp Skill

Manage email marketing campaigns and audience with Mailchimp's comprehensive platform.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/mailchimp/install.sh | bash
```

Or manually:
```bash
cp -r skills/mailchimp ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set MAILCHIMP_API_KEY "your_api_key"
canifi-env set MAILCHIMP_SERVER_PREFIX "us1"
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

1. **Campaign Management**: Create, schedule, and send email campaigns
2. **Audience Management**: Manage subscribers, segments, and tags
3. **Automation**: Set up automated email journeys and workflows
4. **Templates**: Create and manage reusable email templates
5. **Analytics**: Track campaign performance and engagement metrics

## Usage Examples

### Create Campaign
```
User: "Create a new Mailchimp campaign for the product launch"
Assistant: Creates campaign draft with settings
```

### Add Subscriber
```
User: "Add john@example.com to my newsletter list"
Assistant: Adds subscriber with optional merge fields
```

### View Stats
```
User: "Show me the stats for last week's campaign"
Assistant: Returns open rate, click rate, and engagement metrics
```

### Create Segment
```
User: "Create a segment of subscribers who opened the last 3 emails"
Assistant: Creates segment with engagement criteria
```

## Authentication Flow

1. Get API key from Mailchimp account settings
2. Extract server prefix from API key (e.g., us1)
3. Use API key for all authenticated requests
4. OAuth available for app marketplace

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid API key | Verify API key format |
| 403 Forbidden | Feature not available | Check plan tier |
| 404 Not Found | Resource doesn't exist | Verify ID |
| 429 Rate Limited | Too many requests | Implement backoff |

## Notes

- Free tier up to 500 contacts
- API key contains server prefix
- Extensive template library
- A/B testing available
- Landing pages included
- Integrations with 300+ apps
