---
name: constant-contact
description: Manage email marketing with Constant Contact's small business focused platform.
category: marketing
---
# Constant Contact Skill

Manage email marketing with Constant Contact's small business focused platform.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/constant-contact/install.sh | bash
```

Or manually:
```bash
cp -r skills/constant-contact ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set CONSTANT_CONTACT_API_KEY "your_api_key"
canifi-env set CONSTANT_CONTACT_ACCESS_TOKEN "your_access_token"
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

1. **Email Campaigns**: Create and send professional email campaigns
2. **Contact Management**: Import and manage contact lists
3. **Event Marketing**: Create and promote events with registration
4. **Social Posting**: Post to social media alongside email
5. **Reporting**: Track email performance and engagement

## Usage Examples

### Create Email
```
User: "Create a newsletter in Constant Contact"
Assistant: Creates email campaign with template
```

### Add Contact
```
User: "Add a new contact to my main list"
Assistant: Adds contact to specified list
```

### Create Event
```
User: "Create an event registration page for the webinar"
Assistant: Creates event with registration form
```

### View Report
```
User: "Show me last month's email performance"
Assistant: Returns campaign metrics and trends
```

## Authentication Flow

1. Register app in Constant Contact developer portal
2. Implement OAuth 2.0 authorization flow
3. Get access and refresh tokens
4. Use access token for API requests

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Token expired | Refresh access token |
| 403 Forbidden | Feature not available | Check subscription |
| 404 Not Found | Resource not found | Verify ID |
| 429 Rate Limited | Too many requests | Implement backoff |

## Notes

- Designed for small businesses
- Easy-to-use email editor
- Event marketing included
- Social media posting
- Phone support available
- 30-day free trial
