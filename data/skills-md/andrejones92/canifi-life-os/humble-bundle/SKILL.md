---
name: humble-bundle
description: Manage Humble Bundle purchases, Choice subscription, and charity bundles
category: gaming
---

# Humble Bundle Skill

## Overview
Enables Claude to interact with Humble Bundle for managing game library, browsing current bundles, accessing Humble Choice games, and tracking charitable contributions.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/humble-bundle/install.sh | bash
```

Or manually:
```bash
cp -r skills/humble-bundle ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set HUMBLE_EMAIL "your-email@example.com"
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
- Browse and purchase game bundles
- Manage Humble Choice subscription
- View purchase history and keys
- Track charitable contribution totals
- Access Humble Games Collection

## Usage Examples
### Example 1: Current Bundles
```
User: "What bundles are available on Humble Bundle?"
Claude: I'll check the current Humble Bundles available for purchase.
```

### Example 2: Humble Choice
```
User: "What games are in Humble Choice this month?"
Claude: I'll check the current Humble Choice monthly selection.
```

### Example 3: Key Library
```
User: "What unclaimed keys do I have on Humble?"
Claude: I'll check your Humble Bundle library for unredeemed game keys.
```

## Authentication Flow
1. Navigate to humblebundle.com via Playwright MCP
2. Click "Log In" button
3. Enter email and password
4. Handle 2FA if enabled
5. Maintain session for subsequent requests

## Error Handling
- Login Failed: Retry authentication up to 3 times, then notify via iMessage
- Session Expired: Re-authenticate automatically
- 2FA Required: Wait for code via email
- Rate Limited: Implement exponential backoff
- Key Revealed: Cannot hide keys once shown

## Self-Improvement Instructions
When encountering new UI patterns:
1. Document Humble Bundle interface changes
2. Update selectors for new layouts
3. Track bundle timing and themes
4. Monitor Choice changes

## Notes
- Bundles support charity donations
- Choice subscription for monthly games
- Keys redeemable on Steam/Epic/etc
- Trove/Collection for DRM-free games
