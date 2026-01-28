---
name: statefarm
description: Manage State Farm insurance policies with local agent support.
category: insurance
---
# State Farm Skill

Manage State Farm insurance policies with local agent support.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/statefarm/install.sh | bash
```

Or manually:
```bash
cp -r skills/statefarm ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set STATEFARM_EMAIL "your_email"
canifi-env set STATEFARM_PASSWORD "your_password"
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

1. **View Policies**: Access all insurance policies
2. **File Claims**: Submit and track claims
3. **Agent Connect**: Contact your local agent
4. **Drive Safe**: View telematics data
5. **Pocket Agent**: Access mobile features

## Usage Examples

### View Policy
```
User: "Show my State Farm auto policy"
Assistant: Returns policy details
```

### Contact Agent
```
User: "Get my State Farm agent's contact info"
Assistant: Returns agent details
```

### File Claim
```
User: "File a home insurance claim"
Assistant: Starts claim process
```

### View Drive Safe
```
User: "Show my Drive Safe & Save score"
Assistant: Returns driving data
```

## Authentication Flow

1. Account-based authentication
2. No official API
3. Browser automation required
4. Agent network integration

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Login Failed | Invalid credentials | Check account |
| Agent Not Found | Assignment issue | Contact support |
| Claim Error | Missing info | Complete details |
| Payment Failed | Billing issue | Update method |

## Notes

- Agent-based model
- Drive Safe & Save program
- Bundle discounts
- No public API
- Mobile app available
- Bank products available
