---
name: fitbit
description: Track health metrics with Fitbit - view activity, sleep, heart rate, and wellness data
category: health
---

# Fitbit Skill

## Overview
Enables Claude to use Fitbit for health and wellness tracking including viewing activity data, sleep patterns, heart rate, and other health metrics.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/fitbit/install.sh | bash
```

Or manually:
```bash
cp -r skills/fitbit ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set FITBIT_EMAIL "your-email@example.com"
canifi-env set FITBIT_PASSWORD "your-password"
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
- View daily activity stats
- Check sleep patterns and quality
- Access heart rate data
- View step counts and goals
- Check weight and body metrics
- Access exercise history

## Usage Examples

### Example 1: Check Daily Activity
```
User: "How many steps have I taken today?"
Claude: I'll check your step count.
1. Opening Fitbit via Playwright MCP
2. Accessing today's dashboard
3. Viewing step total
4. Comparing to daily goal
```

### Example 2: View Sleep Data
```
User: "How did I sleep last night?"
Claude: I'll check your sleep data.
1. Navigating to sleep section
2. Viewing last night's sleep
3. Checking sleep stages
4. Summarizing sleep quality
```

### Example 3: Check Heart Rate
```
User: "What's my resting heart rate trend?"
Claude: I'll analyze your heart rate data.
1. Accessing heart rate section
2. Viewing resting HR history
3. Calculating trends
4. Summarizing changes
```

## Authentication Flow
1. Navigate to fitbit.com via Playwright MCP
2. Click "Log In" and enter email
3. Enter password
4. Handle Google login if connected
5. Complete 2FA if required (via iMessage)

## Error Handling
- **Login Failed**: Retry up to 3 times, notify via iMessage
- **Session Expired**: Re-authenticate automatically
- **Rate Limited**: Implement exponential backoff
- **2FA Required**: Send iMessage notification
- **Sync Required**: Note data may be outdated
- **Device Offline**: Report last sync time

## Self-Improvement Instructions
When Fitbit updates:
1. Document new health metrics
2. Update dashboard navigation
3. Track new device features
4. Log Google integration changes

## Notes
- Now owned by Google
- Syncs from Fitbit devices
- Premium features available
- Multiple health metrics
- Sleep tracking detailed
