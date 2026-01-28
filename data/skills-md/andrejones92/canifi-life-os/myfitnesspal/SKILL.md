---
name: myfitnesspal
description: Track nutrition and calories with MyFitnessPal - log meals, monitor macros, and view food diary
category: health
---

# MyFitnessPal Skill

## Overview
Enables Claude to use MyFitnessPal for nutrition tracking including viewing food logs, checking calorie and macro totals, and accessing dietary history.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/myfitnesspal/install.sh | bash
```

Or manually:
```bash
cp -r skills/myfitnesspal ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set MYFITNESSPAL_EMAIL "your-email@example.com"
canifi-env set MYFITNESSPAL_PASSWORD "your-password"
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
- View daily food diary
- Check calorie and macro totals
- Access meal history
- View nutrition goals and progress
- Browse food database
- Check weight history

## Usage Examples

### Example 1: Check Daily Calories
```
User: "How many calories have I logged today?"
Claude: I'll check your daily totals.
1. Opening MyFitnessPal via Playwright MCP
2. Navigating to food diary
3. Viewing today's entries
4. Summing total calories
5. Reporting remaining vs goal
```

### Example 2: View Macro Breakdown
```
User: "What's my protein intake so far today?"
Claude: I'll check your macros.
1. Accessing today's diary
2. Viewing macro breakdown
3. Calculating protein total
4. Comparing to daily goal
```

### Example 3: Check Week Summary
```
User: "How did I do with my nutrition this week?"
Claude: I'll review your weekly nutrition.
1. Accessing nutrition reports
2. Viewing weekly summary
3. Calculating averages
4. Summarizing goal adherence
```

## Authentication Flow
1. Navigate to myfitnesspal.com via Playwright MCP
2. Click "Log In" and enter email
3. Enter password
4. Handle 2FA if required (via iMessage)
5. Maintain session for diary access

## Error Handling
- **Login Failed**: Retry up to 3 times, notify via iMessage
- **Session Expired**: Re-authenticate automatically
- **Rate Limited**: Implement exponential backoff
- **2FA Required**: Send iMessage notification
- **Data Unavailable**: Check for logged entries
- **Sync Error**: Refresh and retry

## Self-Improvement Instructions
When MyFitnessPal updates:
1. Document new diary features
2. Update nutrition display options
3. Track food database changes
4. Log new tracking metrics

## Notes
- Under Armour account system
- Large food database
- Premium features available
- Syncs with fitness devices
- Barcode scanning on mobile
