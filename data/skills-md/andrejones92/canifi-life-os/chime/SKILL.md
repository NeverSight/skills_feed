---
name: chime
description: View Chime checking and savings, check SpotMe status, and monitor account activity
category: finance
---

# Chime Skill

## Overview
Enables Claude to access Chime to view checking and savings account balances, check SpotMe overdraft protection status, monitor transactions, and track automatic savings.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/chime/install.sh | bash
```

Or manually:
```bash
cp -r skills/chime ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set CHIME_EMAIL "your-email@example.com"
canifi-env set CHIME_PHONE "+1234567890"
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
- View Spending Account balance
- Check Savings Account and APY
- Monitor SpotMe limit and usage
- View recent transactions
- Check direct deposit status
- Track automatic savings transfers

## Usage Examples

### Example 1: Check Balances
```
User: "What's my Chime balance?"
Claude: I'll check your Chime accounts.
- Opens chime.com via Playwright MCP
- Logs into account
- Returns: Spending Account: $1,234.56
- Savings Account: $5,678.90 (2.00% APY)
- SpotMe: $200 available
- Total: $6,913.46
- Next direct deposit: Friday
```

### Example 2: Check SpotMe
```
User: "What's my SpotMe limit?"
Claude: I'll check your SpotMe status.
- Navigates to SpotMe section
- SpotMe limit: $200
- Currently used: $0
- Available: $200
- Tip settings: $2 default
- Eligibility: Based on $200+ monthly direct deposit
```

### Example 3: View Transactions
```
User: "Show my recent Chime transactions"
Claude: I'll display your recent activity.
- Navigates to transactions
- Recent activity:
  - Jan 6: -$45.67 Amazon (Spending)
  - Jan 5: +$1,500 Direct Deposit
  - Jan 4: +$25 Save When I Get Paid
  - Jan 3: -$89.00 Target (Spending)
- Auto-Save this week: $50
```

## Authentication Flow
1. Navigate to chime.com via Playwright MCP
2. Enter email or phone number
3. Enter password
4. Handle 2FA via SMS (required)
5. Verify dashboard loads
6. Maintain session for account access

## Error Handling
- Login Failed: Retry with phone number
- 2FA Required: Complete SMS verification
- Account Locked: Direct to support
- Session Expired: Re-authenticate (short sessions)
- Rate Limited: Wait 60 seconds, retry
- App-Only Feature: Note limitations

## Self-Improvement Instructions
After each interaction:
- Track balance check patterns
- Note SpotMe usage
- Log auto-save effectiveness
- Document UI changes

Suggest updates when:
- Chime updates interface
- SpotMe limits change
- New features added
- APY rates update

## Notes
- Claude CANNOT make transactions
- All access is read-only for security
- Chime is online-only bank (no branches)
- SpotMe requires regular direct deposit
- Get paid up to 2 days early
- No overdraft fees
- 60,000+ fee-free ATMs
