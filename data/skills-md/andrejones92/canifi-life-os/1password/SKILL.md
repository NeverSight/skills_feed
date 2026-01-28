---
name: 1password
description: Secure password management and credential storage.
category: utilities
---
# 1Password Skill

Secure password management and credential storage.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/1password/install.sh | bash
```

Or manually:
```bash
cp -r skills/1password ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set OP_SERVICE_ACCOUNT_TOKEN "your_token"
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

1. **Get Passwords**: Retrieve stored credentials
2. **Store Secrets**: Save new passwords securely
3. **Generate Passwords**: Create strong passwords
4. **Share Vaults**: Manage shared access
5. **Security Audit**: Check password health

## Usage Examples

### Get Password
```
User: "Get my Netflix password"
Assistant: Retrieves credential from vault
```

### Generate Password
```
User: "Generate a strong password"
Assistant: Creates secure password
```

### Check Security
```
User: "Run a security audit"
Assistant: Returns Watchtower report
```

### Share Item
```
User: "Share this password with team"
Assistant: Updates vault sharing
```

## Authentication Flow

1. Service account token authentication
2. CLI integration available
3. Connect Server for automation
4. Biometric unlock supported

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Auth Failed | Invalid token | Check service account |
| Item Not Found | Wrong name/vault | Verify item exists |
| Access Denied | Permissions | Check vault access |
| Vault Locked | Timeout | Re-authenticate |

## Notes

- Zero-knowledge encryption
- CLI and Connect Server
- Family and team plans
- Watchtower security
- Cross-platform sync
- Browser extensions
