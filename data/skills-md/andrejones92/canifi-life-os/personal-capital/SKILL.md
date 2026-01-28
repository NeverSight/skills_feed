---
name: personal-capital
description: View net worth, track investments, analyze spending, and monitor retirement progress on Empower Personal Capital
category: finance
---

# Empower Personal Capital Skill

## Overview
Enables Claude to access Empower Personal Capital to view comprehensive financial picture including net worth, investment performance, spending analysis, and retirement planning projections.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/personal-capital/install.sh | bash
```

Or manually:
```bash
cp -r skills/personal-capital ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set PERSONAL_CAPITAL_EMAIL "your-email@example.com"
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
- View total net worth across all accounts
- Monitor investment portfolio performance
- Analyze spending patterns and trends
- Check retirement planner projections
- Review asset allocation
- Track fee analyzer for investments

## Usage Examples

### Example 1: Check Net Worth
```
User: "What's my net worth on Personal Capital?"
Claude: I'll check your Personal Capital dashboard.
- Opens personalcapital.com via Playwright MCP
- Logs into account
- Returns Net Worth: $456,789.12
- Assets: $523,456.78
  - Cash: $45,678
  - Investments: $389,456
  - Property: $88,322
- Liabilities: $66,667.66
  - Mortgage: $62,345
  - Credit Cards: $4,322
- Change (30 days): +$12,345 (+2.78%)
```

### Example 2: Check Investments
```
User: "How are my investments performing?"
Claude: I'll review your investment performance.
- Navigates to Investing tab
- Portfolio value: $389,456.78
- Performance:
  - Today: +$1,234 (+0.32%)
  - YTD: +$34,567 (+9.74%)
  - 1 Year: +$45,678 (+13.2%)
- Asset allocation:
  - US Stocks: 55%
  - International: 20%
  - Bonds: 20%
  - Other: 5%
```

### Example 3: Retirement Projection
```
User: "Am I on track for retirement?"
Claude: I'll check your retirement planner.
- Navigates to Planning section
- Retirement age target: 65
- Projected success rate: 87%
- Monthly income at retirement: $8,500
- Current savings rate: 18%
- Recommendation: Increase savings by $200/mo for 95% success
```

## Authentication Flow
1. Navigate to home.personalcapital.com via Playwright MCP
2. Enter email address
3. Enter password
4. Handle 2FA via SMS or email
5. Wait for accounts to sync
6. Maintain session for dashboard access

## Error Handling
- Login Failed: Retry, check for security holds
- 2FA Required: Complete verification flow
- Account Sync Error: Note stale data timestamp
- Session Expired: Re-authenticate (frequent)
- Rate Limited: Wait 2 minutes, retry
- Linked Account Issue: Identify which needs reauth

## Self-Improvement Instructions
After each interaction:
- Track net worth trends
- Note portfolio allocation changes
- Log retirement projection accuracy
- Document UI changes

Suggest updates when:
- Personal Capital updates interface
- New planning tools added
- Account linking changes
- Wealth management features update

## Notes
- Personal Capital is now Empower
- Free tier includes all tracking tools
- Paid advisory for $100k+ portfolios
- Fee analyzer shows hidden investment costs
- Links to 401k, IRA, bank, credit cards
- Investment checkup compares to target allocation
- Can't make transactions, read-only
