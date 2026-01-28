---
name: smartthings
description: Control SmartThings hub and devices, manage automations and scenes
category: smarthome
---

# SmartThings Skill

## Overview
Enables Claude to interact with Samsung SmartThings for controlling connected devices, creating automations, managing scenes, and integrating various smart home protocols.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/smartthings/install.sh | bash
```

Or manually:
```bash
cp -r skills/smartthings ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set SAMSUNG_EMAIL "your-email@example.com"
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
- Control Z-Wave and Zigbee devices
- Create automations and scenes
- Monitor device status
- Manage SmartThings hub
- Integrate third-party devices

## Usage Examples
### Example 1: Device Control
```
User: "Turn on the garage door sensor through SmartThings"
Claude: I'll check the status and control the garage door via SmartThings.
```

### Example 2: Create Automation
```
User: "Create an automation to notify me when motion is detected at night"
Claude: I'll create a SmartThings automation for nighttime motion alerts.
```

### Example 3: Scene Management
```
User: "Run my Away scene in SmartThings"
Claude: I'll activate your Away scene to set all devices appropriately.
```

## Authentication Flow
1. Navigate to my.smartthings.com via Playwright MCP
2. Click "Sign In" button
3. Enter Samsung account credentials
4. Handle 2FA if enabled
5. Maintain session for subsequent requests

## Error Handling
- Login Failed: Retry authentication up to 3 times, then notify via iMessage
- Session Expired: Re-authenticate with Samsung
- 2FA Required: Wait for code via email
- Rate Limited: Implement exponential backoff
- Hub Offline: Report hub connectivity status

## Self-Improvement Instructions
When encountering new UI patterns:
1. Document SmartThings interface changes
2. Update selectors for new layouts
3. Track new device integrations
4. Monitor automation feature updates

## Notes
- Supports Z-Wave, Zigbee, WiFi, Matter
- Samsung device deep integration
- Third-party device compatibility
- Requires SmartThings Hub for some devices
