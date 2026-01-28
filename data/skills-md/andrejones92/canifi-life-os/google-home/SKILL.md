---
name: google-home
description: Control Google Home devices, manage automations, and configure smart home
category: google
---

# Google Home Skill

## Overview
Enables Claude to interact with Google Home for controlling smart home devices, creating automations, managing household members, and configuring Google Assistant settings.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/google-home/install.sh | bash
```

Or manually:
```bash
cp -r skills/google-home ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set GOOGLE_EMAIL "your-email@example.com"
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
- Control smart home devices
- Create and manage automations
- Manage household and members
- View device activity
- Configure Assistant preferences

## Usage Examples
### Example 1: Device Control
```
User: "Dim the living room lights to 50% through Google Home"
Claude: I'll adjust the living room lights to 50% brightness via Google Home.
```

### Example 2: Create Automation
```
User: "Create an automation that turns on porch light at sunset"
Claude: I'll create a new automation triggered by sunset for the porch light.
```

### Example 3: Check Devices
```
User: "What devices are connected to my Google Home?"
Claude: I'll list all devices connected to your Google Home ecosystem.
```

## Authentication Flow
1. Navigate to home.google.com via Playwright MCP
2. Click "Sign In" button
3. Enter Google credentials
4. Handle 2FA if enabled
5. Maintain session for subsequent requests

## Error Handling
- Login Failed: Retry authentication up to 3 times, then notify via iMessage
- Session Expired: Re-authenticate with Google
- 2FA Required: Wait for code via authenticator
- Rate Limited: Implement exponential backoff
- Device Offline: Report device connectivity

## Self-Improvement Instructions
When encountering new UI patterns:
1. Document Google Home app changes
2. Update selectors for new layouts
3. Track Matter device support
4. Monitor automation features

## Notes
- Works with Google Assistant
- Matter/Thread device support
- Family sharing available
- Integrates with Nest devices
