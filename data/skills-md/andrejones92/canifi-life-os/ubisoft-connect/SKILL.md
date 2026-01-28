---
name: ubisoft-connect
description: Manage Ubisoft Connect library, rewards, and achievements
category: gaming
---

# Ubisoft Connect Skill

## Overview
Enables Claude to interact with Ubisoft Connect for managing game library, earning and spending Ubisoft rewards, tracking achievements, and connecting with other players.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/ubisoft-connect/install.sh | bash
```

Or manually:
```bash
cp -r skills/ubisoft-connect ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set UBISOFT_EMAIL "your-email@example.com"
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
- Browse Ubisoft game library
- Earn and redeem Ubisoft rewards
- Track in-game challenges and achievements
- Manage friend connections
- Access Ubisoft Store deals

## Usage Examples
### Example 1: Rewards Check
```
User: "How many Ubisoft rewards points do I have?"
Claude: I'll check your Ubisoft Connect account for available Units.
```

### Example 2: Game Challenges
```
User: "What challenges are available in Assassin's Creed?"
Claude: I'll check the Ubisoft Connect challenges for Assassin's Creed.
```

### Example 3: Library Overview
```
User: "What Ubisoft games do I own?"
Claude: I'll browse your Ubisoft Connect library.
```

## Authentication Flow
1. Navigate to ubisoft.com via Playwright MCP
2. Click "Log In" button
3. Enter Ubisoft credentials
4. Handle 2FA if enabled
5. Maintain session for subsequent requests

## Error Handling
- Login Failed: Retry authentication up to 3 times, then notify via iMessage
- Session Expired: Re-authenticate with Ubisoft
- 2FA Required: Wait for code via email or app
- Rate Limited: Implement exponential backoff
- Service Unavailable: Check Ubisoft server status

## Self-Improvement Instructions
When encountering new UI patterns:
1. Document Ubisoft Connect changes
2. Update selectors for new layouts
3. Track rewards system updates
4. Monitor new game integrations

## Notes
- Units currency for in-game rewards
- Cross-game progression tracking
- Weekly and daily challenges
- Smart Intel for game tips
