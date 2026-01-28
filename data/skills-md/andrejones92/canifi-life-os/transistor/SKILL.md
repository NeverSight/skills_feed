---
name: transistor
description: Host multiple podcasts with Transistor - manage shows, episodes, analytics, and private podcast feeds
category: video
---

# Transistor Skill

## Overview
Enables Claude to use Transistor for podcast hosting including managing multiple shows, viewing analytics, configuring private podcasts, and tracking subscriber data.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/transistor/install.sh | bash
```

Or manually:
```bash
cp -r skills/transistor ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set TRANSISTOR_EMAIL "your-email@example.com"
canifi-env set TRANSISTOR_PASSWORD "your-password"
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
- Manage multiple podcast shows
- View detailed download analytics
- Configure private podcast feeds
- Track subscriber metrics
- Manage episode publishing
- Access distribution settings

## Usage Examples

### Example 1: Compare Show Performance
```
User: "How are my different podcasts performing compared to each other?"
Claude: I'll compare your show analytics.
1. Opening Transistor via Playwright MCP
2. Accessing analytics dashboard
3. Pulling data for each show
4. Comparing downloads and trends
5. Summarizing performance differences
```

### Example 2: Check Subscriber Count
```
User: "How many subscribers does my private podcast have?"
Claude: I'll check subscriber data.
1. Opening your private podcast
2. Navigating to subscribers section
3. Counting active subscribers
4. Reporting subscriber statistics
```

### Example 3: View Episode Stats
```
User: "Which episode had the most downloads last month?"
Claude: I'll find your top episode.
1. Accessing analytics section
2. Filtering to last month
3. Sorting by downloads
4. Identifying top performer
```

## Authentication Flow
1. Navigate to transistor.fm via Playwright MCP
2. Click "Log in" and enter email
3. Enter password
4. Handle 2FA if required (via iMessage)
5. Maintain session for dashboard access

## Error Handling
- **Login Failed**: Retry up to 3 times, notify via iMessage
- **Session Expired**: Re-authenticate automatically
- **Rate Limited**: Implement exponential backoff
- **2FA Required**: Send iMessage notification
- **Analytics Delayed**: Note data refresh timing
- **Subscriber Error**: Verify feed configuration

## Self-Improvement Instructions
When Transistor updates:
1. Document new multi-show features
2. Update analytics capabilities
3. Track private podcast improvements
4. Log API and integration changes

## Notes
- Supports unlimited shows on all plans
- Private podcasts for paid content
- Detailed analytics per episode
- Integrates with email platforms
- White-label player available
