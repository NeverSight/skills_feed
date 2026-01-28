---
name: activecampaign
description: Manage email marketing and CRM with ActiveCampaign's automation platform.
category: marketing
---
# ActiveCampaign Skill

Manage email marketing and CRM with ActiveCampaign's automation platform.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/activecampaign/install.sh | bash
```

Or manually:
```bash
cp -r skills/activecampaign ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set ACTIVECAMPAIGN_API_URL "your_account_url"
canifi-env set ACTIVECAMPAIGN_API_KEY "your_api_key"
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

1. **Contact Management**: Create and manage contacts with custom fields
2. **Email Automation**: Build complex automation workflows with triggers
3. **Campaign Sending**: Create and send email campaigns
4. **Deal Pipeline**: Manage sales deals and opportunities
5. **Site Tracking**: Track website visits and behavior

## Usage Examples

### Add Contact
```
User: "Add a new contact to ActiveCampaign for john@company.com"
Assistant: Creates contact with provided details
```

### Start Automation
```
User: "Add this contact to the onboarding automation"
Assistant: Enrolls contact in specified automation
```

### Create Campaign
```
User: "Create a newsletter campaign in ActiveCampaign"
Assistant: Creates campaign draft for editing
```

### Update Deal
```
User: "Move the TechCorp deal to 'Negotiation' stage"
Assistant: Updates deal pipeline stage
```

## Authentication Flow

1. Get API URL and key from ActiveCampaign settings
2. URL is account-specific (yourname.api-us1.com)
3. Use API key in request header
4. All requests require both URL and key

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid API key | Verify API key |
| 403 Forbidden | Feature not available | Check plan |
| 404 Not Found | Resource not found | Verify ID |
| 422 Validation Error | Invalid data | Check request format |

## Notes

- Combined email marketing and CRM
- Powerful automation builder
- Machine learning features
- Site and event tracking
- Salesforce integration
- 850+ integrations available
