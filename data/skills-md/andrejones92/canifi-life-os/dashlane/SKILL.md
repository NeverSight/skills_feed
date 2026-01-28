---
name: dashlane
description: Password manager with dark web monitoring and VPN.
category: utilities
---
# Dashlane Skill

Password manager with dark web monitoring and VPN.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/dashlane/install.sh | bash
```

Or manually:
```bash
cp -r skills/dashlane ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set DASHLANE_EMAIL "your_email"
canifi-env set DASHLANE_PASSWORD "your_password"
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

1. **Access Passwords**: Retrieve credentials
2. **Store Logins**: Save new passwords
3. **Password Health**: Security scoring
4. **Dark Web Monitor**: Breach detection
5. **Secure Notes**: Store sensitive info

## Usage Examples

### Get Password
```
User: "Get my Twitter password"
Assistant: Retrieves from Dashlane
```

### Check Breaches
```
User: "Have any of my accounts been breached?"
Assistant: Returns dark web monitoring results
```

### Password Health
```
User: "Show my password health score"
Assistant: Returns security analysis
```

### Save Note
```
User: "Save this secure note"
Assistant: Stores in Dashlane
```

## Authentication Flow

1. Account-based authentication
2. CLI available
3. Browser automation backup
4. Biometric support

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Login Failed | Invalid credentials | Check account |
| Item Not Found | Search miss | Verify name |
| Sync Error | Connection | Retry |
| Premium Required | Feature limit | Upgrade plan |

## Notes

- Dark web monitoring
- Password health
- VPN included (premium)
- Identity dashboard
- No public API
- Form autofill
