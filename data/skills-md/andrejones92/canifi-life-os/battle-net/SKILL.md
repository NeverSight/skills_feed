---
name: battle-net
description: Manage Battle.net account, Blizzard games, and Activision titles
category: gaming
---

# Battle.net Skill

## Overview
Enables Claude to interact with Battle.net for managing Blizzard and Activision game library, tracking achievements, managing friends, and accessing game-specific features.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/battle-net/install.sh | bash
```

Or manually:
```bash
cp -r skills/battle-net ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set BATTLENET_EMAIL "your-email@example.com"
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
- View Blizzard/Activision game library
- Track achievements across games
- Manage Battle.net friends list
- View game statistics and progress
- Access Blizzard Shop deals

## Usage Examples
### Example 1: Game Library
```
User: "What Blizzard games do I own?"
Claude: I'll check your Battle.net account for owned games.
```

### Example 2: Friend Activity
```
User: "What are my Battle.net friends playing?"
Claude: I'll check your friends list for current gaming activity.
```

### Example 3: Game Stats
```
User: "What's my Overwatch 2 rank?"
Claude: I'll check your Overwatch 2 competitive statistics.
```

## Authentication Flow
1. Navigate to battle.net via Playwright MCP
2. Click "Log In" button
3. Enter Battle.net credentials
4. Handle Authenticator 2FA
5. Maintain session for subsequent requests

## Error Handling
- Login Failed: Retry authentication up to 3 times, then notify via iMessage
- Session Expired: Re-authenticate with Battle.net
- 2FA Required: Wait for Authenticator code
- Rate Limited: Implement exponential backoff
- Region Selection: Handle regional account differences

## Self-Improvement Instructions
When encountering new UI patterns:
1. Document Battle.net interface changes
2. Update selectors for new layouts
3. Track game-specific feature changes
4. Monitor new game additions

## Notes
- Blizzard Authenticator recommended for 2FA
- Regional differences in availability
- Cross-game social features
- Blizzard Balance for purchases
