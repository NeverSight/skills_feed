---
name: savvycal
description: Beautiful scheduling that lets recipients overlay their calendar.
category: productivity
---
# SavvyCal Skill

Beautiful scheduling that lets recipients overlay their calendar.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/savvycal/install.sh | bash
```

Or manually:
```bash
cp -r skills/savvycal ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set SAVVYCAL_API_KEY "your_api_key"
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

1. **Create Links**: Generate scheduling pages
2. **View Meetings**: Check scheduled events
3. **Personalized Scheduling**: Custom recipient experience
4. **Team Coordination**: Collective availability
5. **Calendar Overlay**: Show availability comparison

## Usage Examples

### Get Link
```
User: "Get my SavvyCal link"
Assistant: Returns scheduling URL
```

### View Schedule
```
User: "Show my upcoming SavvyCal meetings"
Assistant: Returns scheduled events
```

### Create Link
```
User: "Create a new scheduling link"
Assistant: Generates personalized link
```

### Check Availability
```
User: "When am I free next week?"
Assistant: Returns available slots
```

## Authentication Flow

1. API key authentication
2. OAuth for integrations
3. Calendar sync required
4. Webhook support

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Auth Failed | Invalid key | Check API key |
| Link Not Found | Deleted | Create new link |
| Calendar Error | Sync issue | Reconnect calendar |
| Conflict | Overlap | Check availability |

## Notes

- Recipient-first design
- Calendar overlay feature
- Personalized links
- Round robin
- API available
- Zapier integration
