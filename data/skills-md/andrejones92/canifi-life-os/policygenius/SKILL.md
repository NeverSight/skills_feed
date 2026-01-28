---
name: policygenius
description: Compare and buy insurance from top carriers in one place.
category: insurance
---
# Policygenius Skill

Compare and buy insurance from top carriers in one place.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/policygenius/install.sh | bash
```

Or manually:
```bash
cp -r skills/policygenius ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set POLICYGENIUS_EMAIL "your_email"
canifi-env set POLICYGENIUS_PASSWORD "your_password"
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

1. **Compare Quotes**: Compare rates from multiple carriers
2. **Life Insurance**: Get term life quotes
3. **Home Insurance**: Compare homeowners policies
4. **Auto Insurance**: Find best auto rates
5. **Disability Insurance**: Income protection quotes

## Usage Examples

### Compare Life Insurance
```
User: "Compare term life insurance quotes"
Assistant: Returns quotes from multiple carriers
```

### Get Home Quote
```
User: "Find homeowners insurance quotes"
Assistant: Returns comparison of policies
```

### Compare Auto
```
User: "Compare auto insurance rates"
Assistant: Returns carrier comparisons
```

### Check Application
```
User: "What's my application status?"
Assistant: Returns application progress
```

## Authentication Flow

1. Account-based authentication
2. No official API
3. Browser automation required
4. Multi-carrier integration

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Login Failed | Invalid credentials | Check account |
| Quote Error | Eligibility issue | Adjust criteria |
| Application Error | Missing info | Complete form |
| Carrier Error | Availability | Try different carrier |

## Notes

- Insurance marketplace
- Independent comparison
- Licensed advisors available
- Multiple carrier quotes
- No public API
- Free service
