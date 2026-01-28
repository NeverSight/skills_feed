---
name: discord-nitro
description: Manage Discord Nitro subscription, server boosts, and premium features
category: gaming
---

# Discord Nitro Skill

## Overview
Enables Claude to interact with Discord for managing Nitro subscription benefits, server boosts, custom emoji usage, and premium features like higher upload limits.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/discord-nitro/install.sh | bash
```

Or manually:
```bash
cp -r skills/discord-nitro ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set DISCORD_EMAIL "your-email@example.com"
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
- View Nitro subscription status
- Manage server boosts allocation
- Track free game perks and rewards
- View Nitro-exclusive features
- Check boost level on servers

## Usage Examples
### Example 1: Subscription Status
```
User: "When does my Discord Nitro renew?"
Claude: I'll check your Nitro subscription status and renewal date.
```

### Example 2: Server Boosts
```
User: "Which servers am I boosting?"
Claude: I'll check where your Nitro boosts are currently allocated.
```

### Example 3: Perks Check
```
User: "What Nitro perks do I have?"
Claude: I'll list your current Discord Nitro benefits and features.
```

## Authentication Flow
1. Navigate to discord.com via Playwright MCP
2. Click "Login" button
3. Enter Discord credentials
4. Handle 2FA via authenticator or SMS
5. Maintain session for subsequent requests

## Error Handling
- Login Failed: Retry authentication up to 3 times, then notify via iMessage
- Session Expired: Re-authenticate with Discord
- 2FA Required: Wait for code via authenticator
- Rate Limited: Implement exponential backoff
- Subscription Lapsed: Note feature limitations

## Self-Improvement Instructions
When encountering new UI patterns:
1. Document Discord web app changes
2. Update selectors for new layouts
3. Track Nitro perk additions
4. Monitor boost system changes

## Notes
- Nitro vs Nitro Basic tiers
- Server boosts enhance servers
- 2 boosts included with Nitro
- Profile customization features
