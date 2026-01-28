---
name: garmin-connect
description: Track fitness with Garmin Connect - view activities, health metrics, and training data from Garmin devices
category: health
---

# Garmin Connect Skill

## Overview
Enables Claude to use Garmin Connect for fitness tracking including viewing activities, health metrics, training status, and data from Garmin wearables.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/garmin-connect/install.sh | bash
```

Or manually:
```bash
cp -r skills/garmin-connect ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set GARMIN_EMAIL "your-email@example.com"
canifi-env set GARMIN_PASSWORD "your-password"
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
- View activity history
- Check health metrics
- Access training status
- View sleep data
- Check body battery
- Access stress tracking

## Usage Examples

### Example 1: Check Training Status
```
User: "What's my Garmin training status?"
Claude: I'll check your training status.
1. Opening Garmin Connect via Playwright MCP
2. Navigating to training section
3. Viewing current status
4. Checking load and recovery
5. Summarizing recommendations
```

### Example 2: View Body Battery
```
User: "What's my body battery level?"
Claude: I'll check your body battery.
1. Accessing health stats
2. Viewing body battery
3. Checking current level
4. Showing daily pattern
```

### Example 3: Review Activities
```
User: "Show me my activities from this week"
Claude: I'll review your activities.
1. Opening activities section
2. Filtering to this week
3. Listing all activities
4. Summarizing totals
```

## Authentication Flow
1. Navigate to connect.garmin.com via Playwright MCP
2. Click "Sign In" and enter email
3. Enter password
4. Handle 2FA if required (via iMessage)
5. Maintain session for data access

## Error Handling
- **Login Failed**: Retry up to 3 times, notify via iMessage
- **Session Expired**: Re-authenticate automatically
- **Rate Limited**: Implement exponential backoff
- **2FA Required**: Send iMessage notification
- **Sync Required**: Check device connection
- **Data Delayed**: Note sync timing

## Self-Improvement Instructions
When Garmin Connect updates:
1. Document new health metrics
2. Update activity type support
3. Track training features
4. Log device compatibility changes

## Notes
- Syncs from Garmin devices
- Comprehensive health tracking
- Training load analysis
- Body battery unique feature
- GPS-based activities
