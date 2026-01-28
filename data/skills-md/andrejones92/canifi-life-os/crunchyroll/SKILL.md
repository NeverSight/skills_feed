---
name: crunchyroll
description: Stream anime on Crunchyroll, manage watchlist, and track simulcasts
category: entertainment
---

# Crunchyroll Skill

## Overview
Enables Claude to interact with Crunchyroll for streaming anime, managing watchlist, tracking simulcast releases, and discovering new series based on genres and preferences.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/crunchyroll/install.sh | bash
```

Or manually:
```bash
cp -r skills/crunchyroll ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set CRUNCHYROLL_EMAIL "your-email@example.com"
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
- Browse and stream anime series and movies
- Manage Crunchylists and watchlist
- Track simulcast schedule and new episodes
- Access manga library (Premium)
- View watch history and continue watching

## Usage Examples
### Example 1: Add to Watchlist
```
User: "Add Jujutsu Kaisen to my Crunchyroll list"
Claude: I'll add Jujutsu Kaisen to your Crunchyroll watchlist.
```

### Example 2: Check Simulcasts
```
User: "What anime is airing today?"
Claude: I'll check the simulcast calendar for today's new episode releases.
```

### Example 3: Genre Browse
```
User: "Find me some good isekai anime"
Claude: I'll browse the isekai genre and recommend highly-rated series.
```

## Authentication Flow
1. Navigate to crunchyroll.com via Playwright MCP
2. Click "Log In" button
3. Enter email and password
4. Select profile if applicable
5. Maintain session for subsequent requests

## Error Handling
- Login Failed: Retry authentication up to 3 times, then notify via iMessage
- Session Expired: Re-authenticate automatically
- Rate Limited: Implement exponential backoff
- Content Unavailable: Check regional restrictions or subscription tier
- Simulcast Timing: Verify episode release schedule

## Self-Improvement Instructions
When encountering new UI patterns:
1. Document Crunchyroll interface changes
2. Update selectors for new layouts
3. Track seasonal anime additions
4. Monitor simulcast schedule accuracy

## Notes
- Free tier has ads and limited access
- Premium removes ads and adds features
- Simulcast times based on Japan release
- Merged with Funimation library
