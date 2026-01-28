---
name: clockify
description: Free time tracking for teams and individuals.
category: hr
---
# Clockify Skill

Free time tracking for teams and individuals.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/clockify/install.sh | bash
```

Or manually:
```bash
cp -r skills/clockify ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set CLOCKIFY_API_KEY "your_api_key"
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

1. **Track Time**: Start and stop timers
2. **Log Entries**: Add manual time entries
3. **View Reports**: Generate time reports
4. **Manage Projects**: Organize work
5. **Team Tracking**: Monitor team hours

## Usage Examples

### Start Timer
```
User: "Start tracking time on Project X"
Assistant: Starts timer
```

### Stop Timer
```
User: "Stop my timer"
Assistant: Stops and logs time
```

### View Report
```
User: "Show this week's time report"
Assistant: Returns time summary
```

### Log Entry
```
User: "Log 2 hours to client meeting"
Assistant: Creates time entry
```

## Authentication Flow

1. API key authentication
2. Workspace-based
3. Full REST API
4. Webhook support

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Auth Failed | Invalid key | Check API key |
| Project Not Found | Wrong ID | Verify project |
| Timer Running | Existing timer | Stop first |
| Rate Limited | Too many requests | Slow down |

## Notes

- Free unlimited tracking
- Detailed reporting
- Project management
- Team features
- Integrations
- Mobile apps
