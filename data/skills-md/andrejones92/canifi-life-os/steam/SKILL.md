---
name: steam
description: Manage Steam game library, wishlist, and track gaming activity
category: gaming
---

# Steam Skill

## Overview
Enables Claude to interact with Steam for managing game library, tracking wishlist sales, viewing gaming activity, and discovering new games through the Steam store.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/steam/install.sh | bash
```

Or manually:
```bash
cp -r skills/steam ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set STEAM_USERNAME "your-steam-username"
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
- Browse and manage game library
- Track wishlist and sale notifications
- View gaming activity and playtime stats
- Discover games through store recommendations
- Check friend activity and game updates

## Usage Examples
### Example 1: Wishlist Management
```
User: "Are any of my Steam wishlist games on sale?"
Claude: I'll check your Steam wishlist for current discounts and deals.
```

### Example 2: Library Overview
```
User: "What games do I have on Steam that I haven't played?"
Claude: I'll review your library and find games with zero playtime.
```

### Example 3: Friend Activity
```
User: "What are my friends playing on Steam?"
Claude: I'll check your friends list for current gaming activity.
```

## Authentication Flow
1. Navigate to store.steampowered.com via Playwright MCP
2. Click "Login" button
3. Enter Steam credentials
4. Handle Steam Guard 2FA (email or mobile)
5. Maintain session cookies for future access

## Error Handling
- Login Failed: Retry authentication up to 3 times, then notify via iMessage
- Session Expired: Re-authenticate with Steam
- Steam Guard: Wait for 2FA code via email or authenticator
- Rate Limited: Implement exponential backoff
- Profile Private: Request user to adjust privacy settings

## Self-Improvement Instructions
When encountering new UI patterns:
1. Document Steam interface changes
2. Update selectors for new layouts
3. Track sale event patterns
4. Monitor new store features

## Notes
- Steam Guard provides 2FA security
- Profile privacy settings affect visibility
- Family sharing allows library sharing
- Remote play enables streaming games
