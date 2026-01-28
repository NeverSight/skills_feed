---
name: copper
description: Manage relationships with Copper CRM built for Google Workspace.
category: business
---
# Copper Skill

Manage relationships with Copper CRM built for Google Workspace.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/copper/install.sh | bash
```

Or manually:
```bash
cp -r skills/copper ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set COPPER_API_KEY "your_api_key"
canifi-env set COPPER_USER_EMAIL "your_email"
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

1. **Contact Sync**: Automatic contact sync with Gmail and Google Contacts
2. **Pipeline Management**: Visual pipeline with drag-and-drop deals
3. **Email Integration**: Deep Gmail integration with automatic logging
4. **Activity Tracking**: Automatic activity capture from Google Workspace
5. **Project Management**: Track post-sale projects and deliverables

## Usage Examples

### Create Contact
```
User: "Add a new contact in Copper from my last Gmail conversation"
Assistant: Creates contact with email thread context
```

### Update Opportunity
```
User: "Move the Google Cloud deal to 'Negotiation' stage"
Assistant: Updates opportunity stage
```

### Log Activity
```
User: "Log yesterday's meeting with the Google team"
Assistant: Creates activity record with details
```

### Find Related
```
User: "Show me all opportunities for TechCorp in Copper"
Assistant: Returns company's opportunities
```

## Authentication Flow

1. Get API key from Copper settings
2. Include API key and user email in headers
3. All requests require both headers
4. No OAuth, uses API key authentication

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid credentials | Verify API key and email |
| 422 Unprocessable | Invalid data | Check request format |
| 429 Rate Limited | Too many requests | Wait and retry |
| 404 Not Found | Record not found | Verify record ID |

## Notes

- Built specifically for Google Workspace
- Automatic Gmail sync and logging
- Chrome extension for sidebar access
- No manual data entry required
- Project management post-sale
- Works inside Gmail interface
