---
name: buzzsprout
description: Host podcasts with Buzzsprout - manage episodes, track analytics, and distribute to podcast platforms
category: video
---

# Buzzsprout Skill

## Overview
Enables Claude to use Buzzsprout for podcast hosting including managing episodes, viewing analytics, configuring podcast settings, and accessing distribution features.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/buzzsprout/install.sh | bash
```

Or manually:
```bash
cp -r skills/buzzsprout ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set BUZZSPROUT_EMAIL "your-email@example.com"
canifi-env set BUZZSPROUT_PASSWORD "your-password"
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
- Manage podcast episodes
- View download statistics and trends
- Configure podcast metadata
- Access directory distribution status
- Manage episode scheduling
- View affiliate and monetization data

## Usage Examples

### Example 1: Check Download Stats
```
User: "How many downloads did my podcast get this month?"
Claude: I'll pull up your download stats.
1. Opening Buzzsprout via Playwright MCP
2. Navigating to your podcast
3. Accessing statistics page
4. Filtering to this month
5. Summarizing total downloads and trends
```

### Example 2: Schedule Episode
```
User: "When is my next episode scheduled to publish?"
Claude: I'll check your schedule.
1. Opening your podcast dashboard
2. Viewing scheduled episodes
3. Finding next publication date
4. Confirming schedule details
```

### Example 3: Directory Status
```
User: "Is my podcast showing up on all directories?"
Claude: I'll check directory status.
1. Accessing directories section
2. Reviewing submission status
3. Checking Apple, Spotify, Google
4. Reporting any issues found
```

## Authentication Flow
1. Navigate to buzzsprout.com via Playwright MCP
2. Click "Sign In" and enter email
3. Enter password
4. Handle 2FA if required (via iMessage)
5. Maintain session for dashboard access

## Error Handling
- **Login Failed**: Retry up to 3 times, notify via iMessage
- **Session Expired**: Re-authenticate automatically
- **Rate Limited**: Implement exponential backoff
- **2FA Required**: Send iMessage notification
- **Stats Unavailable**: Check data processing status
- **Upload Failed**: Verify file format and size

## Self-Improvement Instructions
When Buzzsprout updates:
1. Document new hosting features
2. Update analytics display options
3. Track distribution platform changes
4. Log new monetization tools

## Notes
- Free tier has monthly upload limits
- Stats update every few hours
- Magic Mastering improves audio
- Affiliate marketplace available
- Transcriptions included on paid plans
