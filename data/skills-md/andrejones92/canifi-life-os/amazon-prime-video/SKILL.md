---
name: amazon-prime-video
description: Stream Amazon Prime Video content, manage watchlist, and access Prime channels
category: entertainment
---

# Amazon Prime Video Skill

## Overview
Enables Claude to interact with Amazon Prime Video for streaming movies and TV shows, managing watchlist, accessing Prime channels, and discovering content included with Prime membership.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/amazon-prime-video/install.sh | bash
```

Or manually:
```bash
cp -r skills/amazon-prime-video ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set AMAZON_EMAIL "your-email@example.com"
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
- Browse Prime-included movies and TV shows
- Manage personal watchlist
- Access Prime Video Channels subscriptions
- View watch history and continue watching
- Search and filter by genre, year, or rating

## Usage Examples
### Example 1: Add to Watchlist
```
User: "Add The Boys to my Prime Video watchlist"
Claude: I'll add The Boys to your Prime Video watchlist.
```

### Example 2: Find Free Content
```
User: "What good movies are free with Prime right now?"
Claude: I'll browse Prime-included movies and highlight highly-rated options.
```

### Example 3: Check Channels
```
User: "What channels do I have on Prime Video?"
Claude: I'll check your Prime Video Channels subscriptions and list active add-ons.
```

## Authentication Flow
1. Navigate to primevideo.com via Playwright MCP
2. Click "Sign In" button
3. Enter Amazon email and password
4. Handle 2FA via SMS or authenticator app
5. Maintain session for subsequent requests

## Error Handling
- Login Failed: Retry authentication up to 3 times, then notify via iMessage
- Session Expired: Re-authenticate automatically
- 2FA Required: Wait for code via iMessage
- Rate Limited: Implement exponential backoff
- Content Unavailable: Distinguish between rentals and Prime-included

## Self-Improvement Instructions
When encountering new UI patterns:
1. Document Prime Video interface changes
2. Update selectors for new layouts
3. Track Prime-included vs rental content
4. Monitor channel availability changes

## Notes
- Requires Amazon Prime membership for included content
- Additional rentals and purchases available
- Prime Channels are separate subscriptions
- X-Ray feature provides additional content info
