---
name: wealthfront
description: View automated portfolio, check cash account, monitor tax-loss harvesting, and track goals on Wealthfront
category: finance
---

# Wealthfront Skill

## Overview
Enables Claude to access Wealthfront to view robo-advisor managed portfolios, check high-yield cash account balances, monitor tax-loss harvesting activity, and track financial goals.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/wealthfront/install.sh | bash
```

Or manually:
```bash
cp -r skills/wealthfront ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set WEALTHFRONT_EMAIL "your-email@example.com"
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
- View investment account balances and allocation
- Check cash account balance and APY
- Monitor tax-loss harvesting activity
- Track financial goals progress
- Review portfolio risk score
- Check automatic rebalancing history

## Usage Examples

### Example 1: Check Portfolio
```
User: "How's my Wealthfront portfolio?"
Claude: I'll check your Wealthfront accounts.
- Opens wealthfront.com via Playwright MCP
- Logs into account
- Returns: Total Managed: $125,678.90
- Cash Account: $45,000.00 (4.50% APY)
- Investment Account: $80,678.90
  - US Stocks: 35% ($28,237)
  - Foreign Stocks: 25% ($20,169)
  - Bonds: 25% ($20,169)
  - Real Estate: 15% ($12,101)
- YTD return: +7.8%
```

### Example 2: Check Tax-Loss Harvesting
```
User: "How much has Wealthfront saved in taxes?"
Claude: I'll check your tax-loss harvesting.
- Navigates to tax section
- Tax-loss harvesting this year: $3,456
- Estimated tax savings: $862 (25% bracket)
- Harvests performed: 12 times
- Direct indexing active: Yes
- Additional savings from direct indexing: $1,234
```

### Example 3: Track Goal
```
User: "How's my house down payment goal?"
Claude: I'll check your goal progress.
- Navigates to goals
- House Down Payment goal:
  - Target: $80,000 by 2026
  - Current: $52,345 (65%)
  - Monthly contribution: $1,500
  - On track: Yes, projected $82,000 by goal date
- Suggests: Stay the course
```

## Authentication Flow
1. Navigate to wealthfront.com via Playwright MCP
2. Enter email address
3. Enter password
4. Handle 2FA via SMS or authenticator
5. Verify dashboard loads
6. Maintain session for account access

## Error Handling
- Login Failed: Retry, check for security holds
- 2FA Required: Complete verification flow
- Account Restricted: Direct to support
- Session Expired: Re-authenticate automatically
- Rate Limited: Wait 2 minutes, retry
- Market Closed: Show last portfolio update

## Self-Improvement Instructions
After each interaction:
- Track portfolio performance queries
- Note goal tracking usage
- Log tax-loss harvesting frequency
- Document UI changes

Suggest updates when:
- Wealthfront updates interface
- New features added
- Cash account APY changes
- Portfolio strategies update

## Notes
- Claude CANNOT make deposits or withdrawals
- All access is read-only for security
- Wealthfront is automated investing (robo-advisor)
- Cash account is high-yield savings
- Tax-loss harvesting automatic above $100k
- Direct indexing above $100k for more tax efficiency
- Path financial planning tool available
