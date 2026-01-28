---
name: xbox
description: Manage Xbox account, achievements, Game Pass, and gaming activity
category: gaming
---

# Xbox Skill

## Overview
Enables Claude to interact with Xbox for viewing game library, tracking achievements, managing Game Pass subscription, and connecting with Xbox Live friends.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/xbox/install.sh | bash
```

Or manually:
```bash
cp -r skills/xbox ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set XBOX_EMAIL "your-email@example.com"
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
- Track achievements and Gamerscore
- Browse Game Pass catalog
- Manage friends and clubs
- Access Xbox Store deals

## Usage Examples
### Example 1: Achievement Progress
```
User: "What achievements am I missing in Halo Infinite?"
Claude: I'll check your Halo Infinite achievements and show remaining ones.
```

### Example 2: Game Pass Browse
```
User: "What new games are on Game Pass?"
Claude: I'll check the latest additions to Xbox Game Pass.
```

### Example 3: Gamerscore
```
User: "What's my total Gamerscore?"
Claude: I'll check your Xbox profile for your current Gamerscore total.
```

## Authentication Flow
1. Navigate to xbox.com via Playwright MCP
2. Click "Sign In" button
3. Enter Microsoft account credentials
4. Handle 2FA if enabled
5. Maintain session for subsequent requests

## Error Handling
- Login Failed: Retry authentication up to 3 times, then notify via iMessage
- Session Expired: Re-authenticate with Microsoft
- 2FA Required: Wait for code via authenticator or email
- Rate Limited: Implement exponential backoff
- Game Pass: Verify subscription status

## Self-Improvement Instructions
When encountering new UI patterns:
1. Document Xbox interface changes
2. Update selectors for new layouts
3. Track Game Pass catalog changes
4. Monitor achievement system updates

## Notes
- Uses Microsoft account for login
- Game Pass includes PC and cloud gaming
- Smart Delivery provides cross-gen versions
- Play Anywhere enables PC and Xbox play
