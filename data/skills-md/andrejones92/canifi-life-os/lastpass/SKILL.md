---
name: lastpass
description: Password management and secure digital vault.
category: utilities
---
# LastPass Skill

Password management and secure digital vault.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/lastpass/install.sh | bash
```

Or manually:
```bash
cp -r skills/lastpass ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set LASTPASS_EMAIL "your_email"
canifi-env set LASTPASS_PASSWORD "your_password"
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

1. **Access Passwords**: Retrieve stored credentials
2. **Store Items**: Save passwords and notes
3. **Password Generator**: Create secure passwords
4. **Shared Folders**: Manage team sharing
5. **Security Dashboard**: Monitor password health

## Usage Examples

### Get Password
```
User: "Get my Amazon password"
Assistant: Retrieves from vault
```

### Save Password
```
User: "Save this new account to LastPass"
Assistant: Stores credential
```

### Generate Password
```
User: "Create a secure password"
Assistant: Generates strong password
```

### Check Security
```
User: "Show my security score"
Assistant: Returns security dashboard data
```

## Authentication Flow

1. Account-based authentication
2. CLI available (lpass)
3. Browser automation backup
4. MFA supported

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Login Failed | Invalid credentials | Check account |
| Item Not Found | Wrong search | Verify name |
| Sync Error | Connection issue | Retry |
| MFA Required | 2FA enabled | Complete verification |

## Notes

- Free tier available
- CLI tool (lpass)
- Browser extensions
- Emergency access
- Dark web monitoring
- Secure notes
