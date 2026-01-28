---
name: lifx
description: Control LIFX smart bulbs and light strips
category: smarthome
---

# LIFX Skill

## Overview
Enables Claude to interact with LIFX for controlling WiFi-connected smart bulbs and light strips, creating scenes, and setting schedules without requiring a hub.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/lifx/install.sh | bash
```

Or manually:
```bash
cp -r skills/lifx ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set LIFX_EMAIL "your-email@example.com"
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
- Control individual lights and groups
- Set colors and color temperature
- Create and activate scenes
- Set schedules and timers
- Configure effects and themes

## Usage Examples
### Example 1: Light Control
```
User: "Set the LIFX lights to blue at 80%"
Claude: I'll adjust your LIFX lights to blue at 80% brightness.
```

### Example 2: Scene Activation
```
User: "Activate the Movie Night scene"
Claude: I'll activate your Movie Night LIFX scene.
```

### Example 3: Effects
```
User: "Enable the candle effect on the bedroom LIFX"
Claude: I'll start the candle flicker effect on your bedroom LIFX bulb.
```

## Authentication Flow
1. Navigate to cloud.lifx.com via Playwright MCP
2. Click "Sign In" button
3. Enter LIFX credentials
4. Handle verification if required
5. Maintain session for subsequent requests

## Error Handling
- Login Failed: Retry authentication up to 3 times, then notify via iMessage
- Session Expired: Re-authenticate automatically
- Verification Required: Complete email verification
- Rate Limited: Implement exponential backoff
- Light Offline: Check WiFi connectivity

## Self-Improvement Instructions
When encountering new UI patterns:
1. Document LIFX app/cloud changes
2. Update selectors for new layouts
3. Track new bulb and effect features
4. Monitor firmware updates

## Notes
- No hub required - WiFi direct
- Bright 1100+ lumen bulbs
- Built-in effects and themes
- Works with Alexa, Google, HomeKit
