---
name: reclaim
description: AI calendar assistant for time management and scheduling.
category: productivity
---
# Reclaim Skill

AI calendar assistant for time management and scheduling.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/reclaim/install.sh | bash
```

Or manually:
```bash
cp -r skills/reclaim ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set RECLAIM_API_KEY "your_api_key"
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

1. **Habits**: Schedule recurring routines
2. **Tasks**: Auto-schedule to-dos
3. **Smart Meetings**: Find optimal times
4. **Buffer Time**: Protect focus blocks
5. **Team Analytics**: View time allocation

## Usage Examples

### Add Habit
```
User: "Schedule 30 min daily exercise"
Assistant: Creates flexible habit block
```

### Add Task
```
User: "Schedule time to review documents"
Assistant: Finds optimal slot
```

### View Analytics
```
User: "How am I spending my time?"
Assistant: Returns time breakdown
```

### Set Buffer
```
User: "Add buffer time between meetings"
Assistant: Configures meeting buffers
```

## Authentication Flow

1. API key authentication
2. OAuth for Google Calendar
3. Slack integration
4. Team workspace

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Auth Failed | Invalid key | Check API key |
| Calendar Error | Sync issue | Reconnect |
| Conflict | No availability | Adjust priorities |
| Habit Error | Configuration | Review settings |

## Notes

- Flexible time blocking
- Smart 1:1s
- Slack status sync
- Team scheduling links
- API available
- Free tier
