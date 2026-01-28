---
name: acorns
description: View round-up investments, track portfolio growth, check recurring investments, and monitor Acorns accounts
category: finance
---

# Acorns Skill

## Overview
Enables Claude to access Acorns to view micro-investment portfolio from round-ups, check balance growth, monitor recurring investments, and track Acorns Later (retirement) accounts.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/acorns/install.sh | bash
```

Or manually:
```bash
cp -r skills/acorns ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set ACORNS_EMAIL "your-email@example.com"
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
- View Invest account balance and growth
- Check round-up activity and multiplier
- Monitor Later (IRA) account balance
- Track Early (kids) accounts if applicable
- Review portfolio allocation
- Check recurring investment status

## Usage Examples

### Example 1: Check Balances
```
User: "What's in my Acorns?"
Claude: I'll check your Acorns accounts.
- Opens acorns.com via Playwright MCP
- Logs into account
- Returns account summary:
  - Invest: $3,456.78
  - Later (IRA): $8,901.23
  - Spend (Debit): $234.56
- Total: $12,592.57
- Growth all-time: +$1,234 (+10.9%)
- Round-up multiplier: 2x
```

### Example 2: View Round-ups
```
User: "How much have I invested from round-ups?"
Claude: I'll check your round-up history.
- Navigates to activity section
- Round-ups this month: $67.89
- Round-up multiplier: 2x (invested $135.78)
- Recent round-ups:
  - Coffee $4.25 → $0.75 round-up
  - Grocery $47.82 → $0.18 round-up
  - Gas $52.01 → $0.99 round-up
- Total lifetime round-ups: $1,890.45
```

### Example 3: Check Portfolio
```
User: "What's my Acorns portfolio invested in?"
Claude: I'll show your portfolio allocation.
- Portfolio type: Aggressive
- Allocation:
  - Large Company Stocks (VOO): 40%
  - Small Company Stocks (VB): 20%
  - Int'l Stocks (VEA): 20%
  - Emerging Markets (VWO): 10%
  - Real Estate (VNQ): 5%
  - Bonds (BND): 5%
- ESG option: Not selected
```

## Authentication Flow
1. Navigate to acorns.com via Playwright MCP
2. Enter email address
3. Enter password
4. Handle 2FA via SMS
5. Verify dashboard loads
6. Maintain session for account access

## Error Handling
- Login Failed: Retry, check credentials
- 2FA Required: Complete SMS verification
- Account Restricted: Direct to support
- Session Expired: Re-authenticate automatically
- Rate Limited: Wait 60 seconds, retry
- App Only Feature: Note if unavailable on web

## Self-Improvement Instructions
After each interaction:
- Track round-up patterns
- Note portfolio changes
- Log recurring investment timing
- Document UI changes

Suggest updates when:
- Acorns updates interface
- New features added
- Portfolio options change
- Subscription tiers update

## Notes
- Claude CANNOT make deposits or withdrawals
- All access is read-only for security
- Acorns rounds up debit card purchases
- Multiplier increases round-up amounts
- Later is a retirement IRA account
- Early for kids' investment accounts
- Subscription: $3-5/month depending on tier
