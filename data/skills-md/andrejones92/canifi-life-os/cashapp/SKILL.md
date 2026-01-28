---
name: cashapp
description: Check balance, view transactions, monitor Bitcoin holdings, and review Cash Card activity on Cash App
category: finance
---

# Cash App Skill

## Overview
Enables Claude to access Cash App to check balance, view transaction history, monitor Bitcoin holdings, and review Cash Card activity. Note: Claude cannot send money or make transactions.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/cashapp/install.sh | bash
```

Or manually:
```bash
cp -r skills/cashapp ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set CASHAPP_EMAIL "your-email@example.com"
canifi-env set CASHAPP_PHONE "+1234567890"
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
- Check Cash App balance
- View Bitcoin holdings and value
- Review recent transaction history
- Monitor Cash Card spending
- Check Boost offers available
- View direct deposit information

## Usage Examples

### Example 1: Check Balances
```
User: "What's in my Cash App?"
Claude: I'll check your Cash App balances.
- Opens cash.app via Playwright MCP
- Logs into account
- Returns: Cash Balance: $523.45
- Bitcoin holdings: 0.00125 BTC ($52.34)
- Total value: $575.79
- Cash Card: Active, linked to balance
```

### Example 2: View Transactions
```
User: "Show my recent Cash App activity"
Claude: I'll pull up your transaction history.
- Navigates to activity section
- Recent transactions:
  - Jan 6: +$100 from Mom (cash)
  - Jan 5: -$45.67 at Target (Cash Card)
  - Jan 4: -$12.99 at Spotify (recurring)
  - Jan 3: +$500 direct deposit
- This week: +$541.34 net
```

### Example 3: Check Bitcoin
```
User: "How's my Bitcoin on Cash App?"
Claude: I'll check your Bitcoin holdings.
- Navigates to Bitcoin section
- Holdings: 0.00125 BTC
- Current value: $52.34
- Change today: +$1.23 (+2.4%)
- Purchase history:
  - Dec 15: Bought 0.001 BTC at $41,500
  - Nov 20: Bought 0.00025 BTC at $38,200
- Total invested: $48.75, current: $52.34
```

## Authentication Flow
1. Navigate to cash.app via Playwright MCP
2. Enter phone number or email
3. Receive and enter verification code via SMS
4. No persistent password - code-based auth
5. May require additional verification
6. Session maintained briefly

## Error Handling
- Login Failed: Retry with alternate contact method
- Code Not Received: Resend verification code
- Account Locked: Direct to Cash App support
- Session Expired: Re-authenticate (code-based)
- Rate Limited: Wait 2 minutes, retry
- Device Not Recognized: Additional verification needed

## Self-Improvement Instructions
After each interaction:
- Track balance check patterns
- Note Bitcoin interest
- Log Cash Card usage patterns
- Document UI changes

Suggest updates when:
- Cash App updates interface
- New features added
- Boost program changes
- Bitcoin features expand

## Notes
- Claude CANNOT send money or buy Bitcoin
- All access is read-only for security
- Cash App uses code-based authentication (no password)
- Boosts provide Cash Card discounts
- Direct deposit up to 2 days early
- Bitcoin can be withdrawn to external wallet
- Stocks feature also available
