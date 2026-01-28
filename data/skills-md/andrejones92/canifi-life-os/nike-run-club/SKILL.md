---
name: nike-run-club
description: Track runs with Nike Run Club - view running history, achievements, and training progress
category: health
---

# Nike Run Club Skill

## Overview
Enables Claude to use Nike Run Club for running tracking including viewing run history, achievements, challenges, and training program progress.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/nike-run-club/install.sh | bash
```

Or manually:
```bash
cp -r skills/nike-run-club ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set NIKE_EMAIL "your-email@example.com"
canifi-env set NIKE_PASSWORD "your-password"
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
- View running history
- Check achievement badges
- Access run statistics
- View monthly/yearly totals
- Check challenge progress
- Access guided run history

## Usage Examples

### Example 1: Check Running Stats
```
User: "How many miles have I run this month?"
Claude: I'll check your monthly mileage.
1. Opening Nike Run Club via Playwright MCP
2. Accessing activity history
3. Summing this month's runs
4. Reporting total distance
```

### Example 2: View Achievements
```
User: "What running achievements have I unlocked?"
Claude: I'll show your achievements.
1. Navigating to achievements
2. Listing unlocked badges
3. Showing recent achievements
4. Noting next milestones
```

### Example 3: Check Recent Run
```
User: "How was my last run?"
Claude: I'll review your last run.
1. Accessing activity feed
2. Finding most recent run
3. Viewing pace and distance
4. Summarizing performance
```

## Authentication Flow
1. Navigate to nike.com via Playwright MCP
2. Click "Sign In" and enter email
3. Enter password
4. Handle 2FA if required (via iMessage)
5. Maintain session for data access

## Error Handling
- **Login Failed**: Retry up to 3 times, notify via iMessage
- **Session Expired**: Re-authenticate automatically
- **Rate Limited**: Implement exponential backoff
- **2FA Required**: Send iMessage notification
- **Sync Pending**: Wait for app sync
- **Run Not Found**: Check activity history

## Self-Improvement Instructions
When Nike Run Club updates:
1. Document new achievement types
2. Update challenge features
3. Track guided run additions
4. Log interface changes

## Notes
- Free running app
- Audio guided runs
- Global challenges
- Personal records tracking
- Integration with Nike ecosystem
