---
name: mercury
description: Banking for startups with powerful financial tools.
category: finance
---
# Mercury Skill

Banking for startups with powerful financial tools.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/mercury/install.sh | bash
```

Or manually:
```bash
cp -r skills/mercury ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set MERCURY_API_KEY "your_api_key"
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

1. **View Accounts**: Check balances and activity
2. **Send Payments**: ACH, wire, and checks
3. **Manage Cards**: Issue and control debit cards
4. **Treasury**: Earn yield on deposits
5. **Financial Insights**: Runway and analytics

## Usage Examples

### Check Balance
```
User: "What's my Mercury balance?"
Assistant: Returns account balance
```

### Send Wire
```
User: "Send a wire to this vendor"
Assistant: Initiates wire transfer
```

### View Runway
```
User: "How long is my runway?"
Assistant: Returns financial projection
```

### Issue Card
```
User: "Create a virtual debit card"
Assistant: Issues new card
```

## Authentication Flow

1. API key authentication
2. OAuth for integrations
3. Bank-level security
4. Multi-approval workflows

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Auth Failed | Invalid key | Check API key |
| Transfer Failed | Insufficient funds | Add funds |
| Card Error | Limit reached | Request increase |
| Approval Needed | Multi-sig required | Get approval |

## Notes

- Startup banking
- FDIC insured
- Treasury yield
- Virtual cards
- Full API
- Accounting integrations
