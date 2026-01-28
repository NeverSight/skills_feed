---
name: amazon-alexa
description: Control Alexa-enabled devices, manage routines, and configure smart home settings
category: smarthome
---

# Amazon Alexa Skill

## Overview
Enables Claude to interact with Amazon Alexa for controlling smart home devices, managing routines, viewing activity history, and configuring Alexa skills and settings.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/amazon-alexa/install.sh | bash
```

Or manually:
```bash
cp -r skills/amazon-alexa ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set AMAZON_EMAIL "your-email@example.com"
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
- Create and manage routines
- View voice activity history
- Manage Alexa skills
- Configure device settings

## Usage Examples
### Example 1: Device Control
```
User: "Turn off all the lights through Alexa"
Claude: I'll send the command to turn off all connected lights via Alexa.
```

### Example 2: Create Routine
```
User: "Create a bedtime routine that turns off lights and sets thermostat to 68"
Claude: I'll create a new Alexa routine with those actions.
```

### Example 3: Check History
```
User: "What commands did I give Alexa today?"
Claude: I'll check your Alexa voice history for today's interactions.
```

## Authentication Flow
1. Navigate to alexa.amazon.com via Playwright MCP
2. Click "Sign In" button
3. Enter Amazon credentials
4. Handle 2FA if enabled
5. Maintain session for subsequent requests

## Error Handling
- Login Failed: Retry authentication up to 3 times, then notify via iMessage
- Session Expired: Re-authenticate with Amazon
- 2FA Required: Wait for code via SMS
- Rate Limited: Implement exponential backoff
- Device Offline: Report device status

## Self-Improvement Instructions
When encountering new UI patterns:
1. Document Alexa app web interface changes
2. Update selectors for new layouts
3. Track new smart home integrations
4. Monitor routine capability updates

## Notes
- Requires Amazon account
- Device compatibility varies
- Routines can trigger multiple actions
- Voice history can be deleted
