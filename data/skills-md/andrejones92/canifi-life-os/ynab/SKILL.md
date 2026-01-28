---
name: ynab
description: Manage zero-based budgets, track spending, and assign every dollar a job with You Need A Budget
category: finance
---

# YNAB Skill

## Overview
Enables Claude to access YNAB's zero-based budgeting system to view budget categories, check available funds, track spending, and help maintain financial discipline using YNAB's methodology.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/ynab/install.sh | bash
```

Or manually:
```bash
cp -r skills/ynab ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set YNAB_EMAIL "your-email@example.com"
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
- View budget category balances and availability
- Check spending against assigned amounts
- Track Age of Money metric
- Review recent transactions
- Identify overspent categories
- Monitor savings goals progress

## Usage Examples

### Example 1: Check Budget Overview
```
User: "How much do I have available for dining out?"
Claude: I'll check your YNAB budget.
- Opens app.ynab.com via Playwright MCP
- Navigates to current month budget
- Returns: Dining Out: $127.45 available
- Assigned this month: $300
- Spent so far: $172.55
- Activity: 8 transactions
```

### Example 2: Check Overspent Categories
```
User: "Am I overspent in any categories?"
Claude: I'll review your budget status.
- Scans all category groups
- Overspent categories (red):
  - Auto Maintenance: -$145.00 (unexpected repair)
  - Clothing: -$67.50
- Underfunded (yellow):
  - Subscriptions: Needs $12.99 more
- Ready to Assign: $0 (fully budgeted)
- Suggests: Cover from Dining Out or Emergency Fund
```

### Example 3: Check Age of Money
```
User: "What's my Age of Money?"
Claude: I'll check your YNAB metrics.
- Navigates to reports section
- Age of Money: 45 days
- Trend: Up from 38 days last month
- Interpretation: On average, money sits 45 days before spent
- Goal: 30+ days means living on last month's income
- You're ahead of the curve!
```

## Authentication Flow
1. Navigate to app.ynab.com via Playwright MCP
2. Click "Log In" and enter email
3. Enter password
4. Handle 2FA if enabled
5. Select correct budget if multiple
6. Maintain session for budget access

## Error Handling
- Login Failed: Retry, check password reset
- Budget Not Found: List available budgets
- Sync Pending: Wait for bank connections
- Session Expired: Re-authenticate automatically
- Rate Limited: Wait 60 seconds, retry
- 2FA Required: Complete verification flow

## Self-Improvement Instructions
After each interaction:
- Track budget category patterns
- Note Age of Money trends
- Log common overspending areas
- Document UI changes

Suggest updates when:
- YNAB updates interface
- New features released
- Methodology guidance changes
- Report types added

## Notes
- YNAB uses zero-based budgeting (every dollar assigned)
- "Give every dollar a job" is core philosophy
- Roll with the punches: move money between categories
- Age of Money indicates financial buffer
- Subscription: $14.99/month or $99/year
- Bank connections via Plaid integration
