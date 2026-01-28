---
name: hubspot
description: Manage contacts, deals, and marketing automation with HubSpot's all-in-one CRM platform.
category: marketing
---
# HubSpot Skill

Manage contacts, deals, and marketing automation with HubSpot's all-in-one CRM platform.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/hubspot/install.sh | bash
```

Or manually:
```bash
cp -r skills/hubspot ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set HUBSPOT_API_KEY "your_api_key"
canifi-env set HUBSPOT_ACCESS_TOKEN "your_access_token"
canifi-env set HUBSPOT_PORTAL_ID "your_portal_id"
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

1. **Contact Management**: Create, update, and organize contacts with custom properties
2. **Deal Pipeline**: Manage sales deals through customizable pipeline stages
3. **Email Tracking**: Send tracked emails and view engagement metrics
4. **Task Management**: Create and manage sales tasks and follow-ups
5. **Marketing Automation**: Create email campaigns and automated workflows

## Usage Examples

### Create Contact
```
User: "Add John Smith to HubSpot with email john@company.com"
Assistant: Creates new contact with provided details
```

### Update Deal Stage
```
User: "Move the Acme Corp deal to 'Closed Won' in HubSpot"
Assistant: Updates deal stage in the pipeline
```

### Search Contacts
```
User: "Find all HubSpot contacts from TechCorp"
Assistant: Returns contacts matching company name
```

### Create Task
```
User: "Create a follow-up task for the Johnson deal tomorrow"
Assistant: Creates task linked to the deal
```

## Authentication Flow

1. Create app in HubSpot developer portal
2. Choose API key or OAuth 2.0 authentication
3. For OAuth, implement authorization code flow
4. Store tokens securely with refresh logic

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid or expired token | Refresh access token |
| 403 Forbidden | Insufficient scopes | Request additional permissions |
| 429 Rate Limited | Too many requests | Implement backoff (10 req/sec) |
| 404 Not Found | Object doesn't exist | Verify object ID |

## Notes

- Free CRM with limited features
- API rate limit: 100 requests per 10 seconds
- Starter tier for basic marketing tools
- Professional tier for advanced automation
- Enterprise tier for custom reporting
- Native integrations with 1000+ apps
