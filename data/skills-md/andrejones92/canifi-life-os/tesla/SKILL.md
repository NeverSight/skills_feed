---
name: tesla
description: Manage your Tesla vehicle, charging, and energy products.
category: automotive
---
# Tesla Skill

Manage your Tesla vehicle, charging, and energy products.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/tesla/install.sh | bash
```

Or manually:
```bash
cp -r skills/tesla ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set TESLA_EMAIL "your_email"
canifi-env set TESLA_PASSWORD "your_password"
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

1. **Vehicle Control**: Lock, unlock, climate, and more
2. **Charging Status**: Monitor charging and find Superchargers
3. **Location Track**: View vehicle location
4. **Energy Products**: Manage Powerwall and Solar
5. **Service Schedule**: Book service appointments

## Usage Examples

### Check Charge
```
User: "What's my Tesla's battery level?"
Assistant: Returns charge status and range
```

### Climate Control
```
User: "Preheat my Tesla"
Assistant: Turns on climate control
```

### Find Supercharger
```
User: "Find nearest Supercharger"
Assistant: Returns nearby charging locations
```

### Lock Vehicle
```
User: "Lock my Tesla"
Assistant: Locks vehicle doors
```

## Authentication Flow

1. Tesla account authentication
2. OAuth2 token-based access
3. Third-party API wrappers available
4. MFA may be required

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Login Failed | Invalid credentials | Check account |
| Vehicle Asleep | Car in deep sleep | Wake vehicle |
| Command Failed | Connectivity issue | Retry |
| Token Expired | Session timeout | Re-authenticate |

## Notes

- Unofficial API (reverse-engineered)
- Vehicle control features
- Energy product management
- Mobile app required for setup
- Rate limits apply
- Some features require premium connectivity
