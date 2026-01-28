---
name: paramount-plus
description: Stream Paramount+ content including CBS shows, movies, and live sports
category: entertainment
---

# Paramount+ Skill

## Overview
Enables Claude to interact with Paramount+ for streaming CBS content, Paramount movies, live sports, and Showtime content, with watchlist management and content discovery.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/paramount-plus/install.sh | bash
```

Or manually:
```bash
cp -r skills/paramount-plus ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set PARAMOUNT_PLUS_EMAIL "your-email@example.com"
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
- Browse CBS shows and Paramount movies
- Access live sports and news
- Manage watchlist and favorites
- View watch history and continue watching
- Access Showtime content (bundle subscribers)

## Usage Examples
### Example 1: Add to Watchlist
```
User: "Add Star Trek: Strange New Worlds to my Paramount+ list"
Claude: I'll add Star Trek: Strange New Worlds to your Paramount+ watchlist.
```

### Example 2: Live CBS
```
User: "What's on CBS live right now?"
Claude: I'll check the live CBS feed and show you the current programming.
```

### Example 3: Browse Movies
```
User: "Show me Paramount movies available to stream"
Claude: I'll browse the movies section for Paramount theatrical releases.
```

## Authentication Flow
1. Navigate to paramountplus.com via Playwright MCP
2. Click "Sign In" button
3. Enter email and password
4. Select profile if multiple exist
5. Maintain session for subsequent requests

## Error Handling
- Login Failed: Retry authentication up to 3 times, then notify via iMessage
- Session Expired: Re-authenticate automatically
- Rate Limited: Implement exponential backoff
- Content Unavailable: Check subscription tier
- Live Content: Verify scheduling and regional availability

## Self-Improvement Instructions
When encountering new UI patterns:
1. Document Paramount+ interface changes
2. Update selectors for new layouts
3. Track Showtime integration features
4. Monitor live content availability

## Notes
- Essential and Showtime bundle tiers
- Live local CBS station access
- NFL games on select plans
- Showtime content for bundle subscribers
