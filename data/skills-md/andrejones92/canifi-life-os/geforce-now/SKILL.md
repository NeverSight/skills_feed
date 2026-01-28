---
name: geforce-now
description: Manage GeForce NOW cloud gaming, library sync, and streaming settings
category: gaming
---

# GeForce NOW Skill

## Overview
Enables Claude to interact with GeForce NOW for managing cloud gaming sessions, syncing game libraries from various stores, and optimizing streaming settings.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/geforce-now/install.sh | bash
```

Or manually:
```bash
cp -r skills/geforce-now ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set NVIDIA_EMAIL "your-email@example.com"
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
- View synced game library
- Check queue times and availability
- Manage connected store accounts
- View session history
- Check membership tier benefits

## Usage Examples
### Example 1: Library Check
```
User: "What games can I play on GeForce NOW?"
Claude: I'll check your synced library of compatible games.
```

### Example 2: Queue Status
```
User: "How long is the GeForce NOW queue?"
Claude: I'll check the current queue times for your membership tier.
```

### Example 3: Connected Accounts
```
User: "Which stores are linked to my GeForce NOW?"
Claude: I'll check which game stores are connected to your account.
```

## Authentication Flow
1. Navigate to play.geforcenow.com via Playwright MCP
2. Click "Log In" button
3. Enter NVIDIA credentials
4. Handle 2FA if enabled
5. Maintain session for subsequent requests

## Error Handling
- Login Failed: Retry authentication up to 3 times, then notify via iMessage
- Session Expired: Re-authenticate with NVIDIA
- 2FA Required: Wait for code via email
- Rate Limited: Implement exponential backoff
- Game Unavailable: Check publisher support

## Self-Improvement Instructions
When encountering new UI patterns:
1. Document GeForce NOW interface changes
2. Update selectors for new layouts
3. Track supported game additions
4. Monitor tier benefit changes

## Notes
- Free tier has queue and session limits
- Priority and Ultimate tiers available
- Games must be owned on linked stores
- RTX support on higher tiers
