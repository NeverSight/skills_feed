---
name: vanguard
description: View investment accounts, check portfolio performance, monitor retirement funds, and research Vanguard funds
category: finance
---

# Vanguard Skill

## Overview
Enables Claude to access Vanguard to view investment accounts, check portfolio performance, monitor retirement accounts, and research Vanguard's low-cost index funds. Note: Claude cannot execute trades.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/vanguard/install.sh | bash
```

Or manually:
```bash
cp -r skills/vanguard ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set VANGUARD_USERNAME "your-username"
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
- View all Vanguard accounts and balances
- Check portfolio performance and returns
- Monitor IRA and brokerage accounts
- Research Vanguard funds and ETFs
- View cost basis and tax lots
- Check dividend reinvestment status

## Usage Examples

### Example 1: Check Portfolio
```
User: "What's my Vanguard portfolio worth?"
Claude: I'll check your Vanguard accounts.
- Opens investor.vanguard.com via Playwright MCP
- Logs into account
- Returns: Total Balance: $567,890.12
  - Traditional IRA: $234,567.89
  - Roth IRA: $89,012.34
  - Brokerage: $244,309.89
- Today: +$3,456.78 (+0.61%)
- YTD return: +8.9%
```

### Example 2: View Holdings
```
User: "What funds am I holding?"
Claude: I'll show your fund holdings.
- Navigates to holdings view
- Portfolio breakdown:
  - VTSAX (Total Stock): $280,000 (49%)
  - VTIAX (Int'l Stock): $120,000 (21%)
  - VBTLX (Total Bond): $100,000 (18%)
  - VFIAX (500 Index): $67,890 (12%)
- Weighted expense ratio: 0.05%
- Dividend yield: 1.8%
```

### Example 3: Research Fund
```
User: "Tell me about VTI"
Claude: I'll look up VTI details.
- Searches for VTI
- Vanguard Total Stock Market ETF
- Expense ratio: 0.03%
- AUM: $1.4 trillion
- 10-year return: 11.5% annualized
- Holdings: 4,000+ US stocks
- Top holdings: Apple, Microsoft, Amazon
```

## Authentication Flow
1. Navigate to investor.vanguard.com via Playwright MCP
2. Enter username
3. Enter password
4. Handle security code via SMS or email
5. May require security questions
6. Maintain session for account access

## Error Handling
- Login Failed: Retry, check username format
- 2FA Required: Complete SMS/email verification
- Account Frozen: Direct to Vanguard support
- Session Expired: Re-authenticate (short sessions)
- Rate Limited: Wait 2 minutes, retry
- Maintenance: Try again during market hours

## Self-Improvement Instructions
After each interaction:
- Track portfolio queries
- Note fund comparison patterns
- Log performance tracking accuracy
- Document UI changes

Suggest updates when:
- Vanguard updates interface
- New fund offerings added
- Account features change
- Auth requirements update

## Notes
- Claude CANNOT execute trades
- All access is read-only for security
- Vanguard known for low expense ratios
- Admiral shares require $3k minimum
- ETF versions often have even lower costs
- Automatic investment plans available
- Tax-loss harvesting at year end
