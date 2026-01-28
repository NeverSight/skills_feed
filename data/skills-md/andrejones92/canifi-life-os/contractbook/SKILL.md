---
name: contractbook
description: Manage contracts with Contractbook's automated contract lifecycle platform.
category: legal
---
# Contractbook Skill

Manage contracts with Contractbook's automated contract lifecycle platform.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/contractbook/install.sh | bash
```

Or manually:
```bash
cp -r skills/contractbook ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set CONTRACTBOOK_API_KEY "your_api_key"
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

1. **Contract Creation**: Create contracts from templates with automation
2. **E-signatures**: Collect digital signatures securely
3. **Contract Repository**: Store and organize all contracts
4. **Automation**: Automate contract workflows and approvals
5. **Analytics**: Track contract metrics and insights

## Usage Examples

### Create Contract
```
User: "Create an NDA using the standard template"
Assistant: Creates contract from template
```

### Send for Signature
```
User: "Send the employment contract for signing"
Assistant: Sends contract for e-signature
```

### Search Contracts
```
User: "Find all contracts expiring this quarter"
Assistant: Returns contracts matching criteria
```

### Set Reminder
```
User: "Remind me 30 days before the contract renews"
Assistant: Sets renewal reminder
```

## Authentication Flow

1. Generate API key in Contractbook settings
2. Use API key for authentication
3. Bearer token in request header
4. Workspace-scoped access

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid API key | Verify credentials |
| 403 Forbidden | No access | Check permissions |
| 404 Not Found | Contract not found | Verify contract ID |
| 429 Rate Limited | Too many requests | Wait and retry |

## Notes

- Contract lifecycle management
- Template library included
- Version control
- Approval workflows
- Integration with tools
- European data hosting
