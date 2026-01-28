---
name: philips-hue
description: Control Philips Hue lights, create scenes, and manage lighting schedules
category: smarthome
---

# Philips Hue Skill

## Overview
Enables Claude to interact with Philips Hue for controlling smart lights, creating custom scenes, setting schedules, and syncing lights with entertainment.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/philips-hue/install.sh | bash
```

Or manually:
```bash
cp -r skills/philips-hue ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set HUE_EMAIL "your-email@example.com"
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
- Create and manage scenes
- Set schedules and timers
- Configure entertainment areas
- Manage Hue Bridge settings

## Usage Examples
### Example 1: Light Control
```
User: "Set the living room lights to warm white at 70%"
Claude: I'll adjust the living room Hue lights to warm white at 70% brightness.
```

### Example 2: Scene Activation
```
User: "Activate the Relax scene"
Claude: I'll activate the Relax scene across your Hue lights.
```

### Example 3: Schedule Creation
```
User: "Schedule bedroom lights to dim at 10pm"
Claude: I'll create a schedule to dim the bedroom lights at 10pm nightly.
```

## Authentication Flow
1. Navigate to meethue.com via Playwright MCP
2. Click "Sign In" button
3. Enter Philips Hue account credentials
4. Handle 2FA if enabled
5. Maintain session for subsequent requests

## Error Handling
- Login Failed: Retry authentication up to 3 times, then notify via iMessage
- Session Expired: Re-authenticate automatically
- 2FA Required: Wait for code via email
- Rate Limited: Implement exponential backoff
- Bridge Offline: Report bridge connectivity

## Self-Improvement Instructions
When encountering new UI patterns:
1. Document Hue app/web changes
2. Update selectors for new layouts
3. Track new bulb types and features
4. Monitor sync and entertainment updates

## Notes
- Requires Philips Hue Bridge
- Entertainment sync for movies/games
- Third-party integration support
- Accessories like motion sensors available
