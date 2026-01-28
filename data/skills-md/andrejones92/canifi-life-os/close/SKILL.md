---
name: close
description: Manage sales with Close's communication-focused CRM for inside sales teams.
category: business
---
# Close Skill

Manage sales with Close's communication-focused CRM for inside sales teams.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/close/install.sh | bash
```

Or manually:
```bash
cp -r skills/close ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set CLOSE_API_KEY "your_api_key"
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

1. **Lead Management**: Create and manage leads with full activity history
2. **Email Automation**: Send automated email sequences and track opens
3. **Built-in Calling**: Make calls directly from CRM with call recording
4. **Smart Views**: Filter and segment leads with custom smart views
5. **Reporting**: Access sales reports and team performance metrics

## Usage Examples

### Create Lead
```
User: "Create a new lead in Close for DataFlow Inc"
Assistant: Creates lead with company information
```

### Log Call
```
User: "Log a 15-minute call with the DataFlow lead"
Assistant: Creates call activity with duration
```

### Start Sequence
```
User: "Add this lead to the follow-up email sequence"
Assistant: Enrolls lead in email sequence
```

### View Smart View
```
User: "Show me all hot leads from the past week"
Assistant: Returns leads matching smart view criteria
```

## Authentication Flow

1. Get API key from Close settings
2. Use Basic Auth with API key as username
3. Leave password empty
4. All requests authenticated with header

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid API key | Verify API key |
| 404 Not Found | Lead doesn't exist | Check lead ID |
| 429 Rate Limited | Too many requests | Implement throttling |
| 400 Bad Request | Invalid data format | Validate request |

## Notes

- Built for inside sales teams
- Native calling and SMS included
- Email open and click tracking
- No free tier, 14-day trial
- Power dialer for high-volume calling
- Predictive dialer in higher tiers
