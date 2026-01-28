---
name: peacock
description: Stream Peacock content including NBCUniversal shows, movies, and live sports
category: entertainment
---

# Peacock Skill

## Overview
Enables Claude to interact with Peacock for streaming NBCUniversal content, live sports, news, and managing watchlist with access to free and premium tiers.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/peacock/install.sh | bash
```

Or manually:
```bash
cp -r skills/peacock ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set PEACOCK_EMAIL "your-email@example.com"
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
- Browse movies, TV shows, and originals
- Access live sports and news channels
- Manage "My Stuff" watchlist
- View watch history and continue watching
- Explore free vs premium content

## Usage Examples
### Example 1: Add to Watchlist
```
User: "Add The Office to my Peacock watchlist"
Claude: I'll add The Office to your My Stuff list on Peacock.
```

### Example 2: Live Sports
```
User: "What sports are live on Peacock right now?"
Claude: I'll check the live section for currently airing sports events.
```

### Example 3: Free Content
```
User: "What can I watch free on Peacock?"
Claude: I'll browse the free tier content available without Premium subscription.
```

## Authentication Flow
1. Navigate to peacocktv.com via Playwright MCP
2. Click "Sign In" button
3. Enter email and password
4. Select profile if applicable
5. Maintain session for subsequent requests

## Error Handling
- Login Failed: Retry authentication up to 3 times, then notify via iMessage
- Session Expired: Re-authenticate automatically
- Rate Limited: Implement exponential backoff
- Content Unavailable: Check subscription tier (Free vs Premium)
- Live Content: Verify scheduling and availability

## Self-Improvement Instructions
When encountering new UI patterns:
1. Document Peacock interface changes
2. Update selectors for new layouts
3. Track free vs premium content changes
4. Monitor live event scheduling

## Notes
- Free tier available with ads
- Premium and Premium Plus tiers
- Live sports require Premium
- Some content has next-day availability
