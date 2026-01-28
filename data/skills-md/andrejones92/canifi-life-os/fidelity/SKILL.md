---
name: fidelity
description: View investment accounts, check portfolio performance, monitor 401k, and research funds on Fidelity
category: finance
---

# Fidelity Skill

## Overview
Enables Claude to access Fidelity to view investment accounts, check portfolio performance, monitor retirement accounts, and research investment options. Note: Claude cannot execute trades.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/fidelity/install.sh | bash
```

Or manually:
```bash
cp -r skills/fidelity ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set FIDELITY_USERNAME "your-username"
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
- View all linked Fidelity accounts
- Check portfolio value and performance
- Monitor 401k and IRA balances
- Research mutual funds and ETFs
- View dividend history
- Check contribution limits and progress

## Usage Examples

### Example 1: Check Account Balances
```
User: "What are my Fidelity balances?"
Claude: I'll check your Fidelity accounts.
- Opens fidelity.com via Playwright MCP
- Logs into account
- Returns account summary:
  - Brokerage: $125,678.90
  - Roth IRA: $67,890.12
  - 401(k): $234,567.89
  - HSA: $8,765.43
- Total: $436,902.34
- Today's change: +$2,345.67 (+0.54%)
```

### Example 2: Check 401k Performance
```
User: "How's my 401k doing?"
Claude: I'll check your 401k account.
- Navigates to 401k section
- Balance: $234,567.89
- YTD return: +12.3%
- Contributions this year: $18,500
- Employer match: $5,550
- Remaining contribution room: $4,500
- Asset allocation: 80% stocks, 20% bonds
```

### Example 3: Research Fund
```
User: "Tell me about FXAIX"
Claude: I'll look up that Fidelity fund.
- Searches for FXAIX
- Fidelity 500 Index Fund
- Expense ratio: 0.015%
- 5-year return: 11.2% annualized
- Morningstar rating: 5 stars
- Minimum investment: $0
- Tracks S&P 500 index
```

## Authentication Flow
1. Navigate to fidelity.com via Playwright MCP
2. Enter username
3. Enter password
4. Handle security questions or 2FA
5. May require VIP Access or Symantec token
6. Maintain session for account access

## Error Handling
- Login Failed: Retry, check username format
- 2FA Required: Complete VIP Access or SMS
- Account Locked: Direct to Fidelity support
- Session Expired: Re-authenticate (security)
- Rate Limited: Wait 2 minutes, retry
- Market Closed: Show last closing values

## Self-Improvement Instructions
After each interaction:
- Track portfolio performance queries
- Note common fund research patterns
- Log contribution tracking accuracy
- Document UI changes

Suggest updates when:
- Fidelity updates interface
- New account types added
- Research tools change
- Auth requirements update

## Notes
- Claude CANNOT execute trades
- All access is read-only for security
- VIP Access app may be required for 2FA
- BrokerageLink for 401k self-direction
- Cash Management account is like checking
- Zero expense ratio index funds available
- Tax documents available in February
