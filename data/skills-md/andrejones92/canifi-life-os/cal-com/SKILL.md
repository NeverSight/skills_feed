---
name: cal-com
description: Open-source scheduling infrastructure for everyone.
category: productivity
---
# Cal.com Skill

Open-source scheduling infrastructure for everyone.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/cal-com/install.sh | bash
```

Or manually:
```bash
cp -r skills/cal-com ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set CALCOM_API_KEY "your_api_key"
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

1. **Event Types**: Create and manage meeting types
2. **Bookings**: View and manage scheduled events
3. **Availability**: Set working hours
4. **Team Scheduling**: Round robin and collective
5. **Workflows**: Automate booking actions

## Usage Examples

### Get Bookings
```
User: "Show my Cal.com bookings"
Assistant: Returns scheduled meetings
```

### Create Event Type
```
User: "Create a 45-minute consultation event"
Assistant: Sets up event type
```

### Update Availability
```
User: "Set my availability to weekdays only"
Assistant: Updates schedule
```

### Cancel Booking
```
User: "Cancel tomorrow's meeting"
Assistant: Cancels and notifies
```

## Authentication Flow

1. API key authentication
2. OAuth available
3. Self-hosting option
4. Webhook support

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Auth Failed | Invalid key | Check API key |
| Not Found | Resource missing | Verify ID |
| Validation Error | Bad input | Check parameters |
| Conflict | Time taken | Choose new slot |

## Notes

- Open source
- Self-hostable
- Full API
- Workflows
- Team features
- White-label option
