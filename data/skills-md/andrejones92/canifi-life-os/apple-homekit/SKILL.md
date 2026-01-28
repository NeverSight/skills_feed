---
name: apple-homekit
description: Control Apple HomeKit devices, manage scenes, and configure home automations
category: smarthome
---

# Apple HomeKit Skill

## Overview
Enables Claude to interact with Apple HomeKit for controlling smart home devices, creating scenes, managing automations, and organizing devices by room.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/apple-homekit/install.sh | bash
```

Or manually:
```bash
cp -r skills/apple-homekit ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set APPLE_ID_EMAIL "your-email@example.com"
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
- Control HomeKit-compatible devices
- Create and activate scenes
- Set up automations and triggers
- Organize devices by room
- Manage home members and access

## Usage Examples
### Example 1: Scene Activation
```
User: "Activate the Good Morning scene in HomeKit"
Claude: I'll activate your Good Morning scene via HomeKit.
```

### Example 2: Device Control
```
User: "Lock all doors through HomeKit"
Claude: I'll send the lock command to all HomeKit-connected door locks.
```

### Example 3: Create Automation
```
User: "Create an automation to turn on lights when I arrive home"
Claude: I'll create a location-based automation for your lights.
```

## Authentication Flow
1. Navigate to icloud.com/home via Playwright MCP
2. Sign in with Apple ID
3. Handle 2FA via trusted device
4. Select Home from iCloud apps
5. Maintain session for subsequent requests

## Error Handling
- Login Failed: Retry authentication up to 3 times, then notify via iMessage
- Session Expired: Re-authenticate with Apple ID
- 2FA Required: Wait for code from trusted device
- Rate Limited: Implement exponential backoff
- Device Unresponsive: Check device status and hub

## Self-Improvement Instructions
When encountering new UI patterns:
1. Document iCloud Home interface changes
2. Update selectors for new layouts
3. Track Matter device additions
4. Monitor automation capabilities

## Notes
- Requires Apple Home Hub (HomePod/Apple TV/iPad)
- HomeKit Secure Video for cameras
- Matter support expands compatibility
- Siri integration for voice control
