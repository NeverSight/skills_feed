---
name: motion
description: AI-powered calendar and task management.
category: productivity
---
# Motion Skill

AI-powered calendar and task management.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/motion/install.sh | bash
```

Or manually:
```bash
cp -r skills/motion ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set MOTION_API_KEY "your_api_key"
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

1. **Auto-Scheduling**: AI plans your day
2. **Task Management**: Prioritize and track
3. **Meeting Scheduler**: Find optimal times
4. **Project Planning**: Allocate work time
5. **Team Coordination**: Balance workloads

## Usage Examples

### Add Task
```
User: "Add a task to finish the report by Friday"
Assistant: Schedules task optimally
```

### View Schedule
```
User: "What's my day look like?"
Assistant: Returns optimized schedule
```

### Reschedule
```
User: "Move my focus time to afternoon"
Assistant: Reorganizes schedule
```

### Add Project
```
User: "Plan time for the Q4 project"
Assistant: Allocates project time
```

## Authentication Flow

1. API key authentication
2. OAuth for calendar
3. Workspace access
4. Team permissions

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Auth Failed | Invalid key | Check API key |
| Calendar Error | Sync issue | Reconnect |
| Scheduling Conflict | No availability | Adjust priorities |
| Task Error | Missing info | Complete details |

## Notes

- AI scheduling engine
- Auto-rescheduling
- Focus time protection
- Team balancing
- API available
- Calendar sync
