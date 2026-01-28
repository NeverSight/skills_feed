---
name: toggl
description: Simple and powerful time tracking with insights.
category: hr
---
# Toggl Track Skill

Simple and powerful time tracking with insights.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/toggl/install.sh | bash
```

Or manually:
```bash
cp -r skills/toggl ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set TOGGL_API_TOKEN "your_token"
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

1. **Time Tracking**: Start/stop timers
2. **Reports**: Generate time reports
3. **Projects**: Manage project tracking
4. **Insights**: AI-powered suggestions
5. **Calendar Integration**: Sync with calendars

## Usage Examples

### Start Timer
```
User: "Start tracking development time"
Assistant: Starts Toggl timer
```

### View Today
```
User: "How much have I worked today?"
Assistant: Returns daily time
```

### Get Report
```
User: "Show last week's report"
Assistant: Returns time breakdown
```

### Add Project
```
User: "Create a new project in Toggl"
Assistant: Creates project
```

## Authentication Flow

1. API token authentication
2. Basic auth with token
3. OAuth for integrations
4. Workspace-based

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Auth Failed | Invalid token | Check API token |
| Not Found | Wrong ID | Verify resource |
| Timer Conflict | Already running | Stop current |
| Forbidden | Workspace access | Check permissions |

## Notes

- AI insights (Toggl)
- Pomodoro timer
- Browser extension
- 100+ integrations
- Detailed reports
- Mobile apps
