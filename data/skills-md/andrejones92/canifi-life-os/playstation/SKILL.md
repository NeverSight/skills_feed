---
name: playstation
description: Manage PlayStation Network account, trophies, and game library
category: gaming
---

# PlayStation Skill

## Overview
Enables Claude to interact with PlayStation Network for viewing game library, tracking trophies, managing friends, and accessing PlayStation Store.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/playstation/install.sh | bash
```

Or manually:
```bash
cp -r skills/playstation ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set PSN_EMAIL "your-email@example.com"
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
- View game library and purchases
- Track trophy progress and achievements
- Manage friends and gaming groups
- Browse PlayStation Store
- Check PS Plus membership benefits

## Usage Examples
### Example 1: Trophy Progress
```
User: "How close am I to the platinum in Spider-Man?"
Claude: I'll check your trophy progress for Spider-Man and show remaining trophies.
```

### Example 2: PS Plus Games
```
User: "What games are free with PS Plus this month?"
Claude: I'll check the current PS Plus monthly games available to claim.
```

### Example 3: Library Overview
```
User: "What PlayStation games do I own?"
Claude: I'll browse your PlayStation game library across all platforms.
```

## Authentication Flow
1. Navigate to store.playstation.com via Playwright MCP
2. Click "Sign In" button
3. Enter PSN email and password
4. Handle 2FA via authenticator or SMS
5. Maintain session for subsequent requests

## Error Handling
- Login Failed: Retry authentication up to 3 times, then notify via iMessage
- Session Expired: Re-authenticate with PSN
- 2FA Required: Wait for code via authenticator
- Rate Limited: Implement exponential backoff
- Region Restrictions: Note content availability

## Self-Improvement Instructions
When encountering new UI patterns:
1. Document PlayStation Store changes
2. Update selectors for new layouts
3. Track PS Plus game additions
4. Monitor trophy system updates

## Notes
- PS Plus required for monthly games
- Trophy sync from console may delay
- Cross-buy enables multi-platform access
- PS Now merged into PS Plus Premium
