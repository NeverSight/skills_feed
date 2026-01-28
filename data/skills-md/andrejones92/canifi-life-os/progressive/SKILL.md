---
name: progressive
description: Manage Progressive insurance policies with Snapshot and Name Your Price.
category: insurance
---
# Progressive Skill

Manage Progressive insurance policies with Snapshot and Name Your Price.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/progressive/install.sh | bash
```

Or manually:
```bash
cp -r skills/progressive ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set PROGRESSIVE_EMAIL "your_email"
canifi-env set PROGRESSIVE_PASSWORD "your_password"
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
2. **Snapshot Data**: View driving behavior data
3. **File Claims**: Submit and track claims
4. **Name Your Price**: Get customized quotes
5. **Bundle Management**: Manage multi-policy bundles

## Usage Examples

### View Snapshot
```
User: "Show my Snapshot driving score"
Assistant: Returns driving behavior data
```

### Get Quote
```
User: "Name your price for auto insurance at $100/month"
Assistant: Returns matching coverage options
```

### File Claim
```
User: "File a claim for my fender bender"
Assistant: Starts claim process
```

### View Bundle
```
User: "Show my bundled policies"
Assistant: Returns all bundled coverage
```

## Authentication Flow

1. Account-based authentication
2. No official API
3. Browser automation required
4. Snapshot device integration

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Login Failed | Invalid credentials | Check account |
| Snapshot Error | Device issue | Reconnect device |
| Quote Failed | Criteria not met | Adjust parameters |
| Claim Error | Missing info | Complete form |

## Notes

- Snapshot telematics program
- Name Your Price tool
- Bundle discounts
- No public API
- Mobile app available
- Usage-based pricing
