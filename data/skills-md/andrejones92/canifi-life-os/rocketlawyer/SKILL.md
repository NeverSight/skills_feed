---
name: rocketlawyer
description: Access legal documents and attorney services with Rocket Lawyer's platform.
category: legal
---
# Rocket Lawyer Skill

Access legal documents and attorney services with Rocket Lawyer's platform.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/rocketlawyer/install.sh | bash
```

Or manually:
```bash
cp -r skills/rocketlawyer ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set ROCKETLAWYER_EMAIL "your_email"
canifi-env set ROCKETLAWYER_PASSWORD "your_password"
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

1. **Document Builder**: Create customized legal documents
2. **E-signatures**: Sign documents electronically
3. **Attorney Access**: Connect with attorneys for advice
4. **Document Storage**: Store and manage legal documents
5. **Legal Forms**: Access library of legal forms and templates

## Usage Examples

### Create Document
```
User: "Create a rental agreement in Rocket Lawyer"
Assistant: Starts document creation wizard
```

### Sign Document
```
User: "E-sign the completed contract"
Assistant: Initiates signing process
```

### Find Attorney
```
User: "Connect me with a business attorney"
Assistant: Initiates attorney matching
```

### View Documents
```
User: "Show me my saved legal documents"
Assistant: Returns document library
```

## Authentication Flow

1. Rocket Lawyer uses account authentication
2. No official public API
3. Browser automation for access
4. Session-based login

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Login Failed | Invalid credentials | Check email and password |
| Document Error | Creation failed | Retry or contact support |
| Session Expired | Timeout | Re-authenticate |
| Subscription Required | Feature locked | Upgrade membership |

## Notes

- Legal document platform
- Attorney network access
- Subscription-based pricing
- Free document previews
- No official API
- Business and personal focus
