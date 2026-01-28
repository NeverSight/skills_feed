---
name: sofi
description: View SoFi accounts, check high-yield savings, monitor loans, and track investment portfolio
category: finance
---

# SoFi Skill

## Overview
Enables Claude to access SoFi to view banking, investing, and loan accounts, check high-yield savings rates, monitor loan payments, and track SoFi Invest portfolio.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/sofi/install.sh | bash
```

Or manually:
```bash
cp -r skills/sofi ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set SOFI_EMAIL "your-email@example.com"
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
- View SoFi Money (checking/savings) balances
- Check SoFi Invest portfolio
- Monitor student loan refinancing status
- Track personal loan payments
- View SoFi Relay credit monitoring
- Check SoFi credit card status

## Usage Examples

### Example 1: Check All Accounts
```
User: "What's in my SoFi accounts?"
Claude: I'll check your SoFi dashboard.
- Opens sofi.com via Playwright MCP
- Logs into account
- Returns account summary:
  - SoFi Checking: $5,678.90 (direct deposit active)
  - SoFi Savings: $25,000.00 (4.50% APY)
  - SoFi Invest: $12,345.67
  - Student Loan: $45,678 remaining
- Total assets: $43,024.57
- SoFi points: 12,500
```

### Example 2: Check Investment Portfolio
```
User: "How's my SoFi Invest doing?"
Claude: I'll check your investment account.
- Navigates to SoFi Invest
- Portfolio value: $12,345.67
- Today: +$89.45 (+0.73%)
- Holdings:
  - Active Invest: $8,000 (self-managed)
  - Automated: $4,345 (robo-managed)
- Crypto: $567.89 in Bitcoin
- IPO access: Eligible
```

### Example 3: Check Loan Status
```
User: "What's my student loan balance?"
Claude: I'll check your loan details.
- Navigates to Loans section
- Student Loan Refinance:
  - Balance: $45,678.90
  - Interest rate: 4.99% fixed
  - Monthly payment: $567
  - Next payment: Jan 15
  - Months remaining: 96
- Autopay discount: Active (-0.25%)
```

## Authentication Flow
1. Navigate to sofi.com via Playwright MCP
2. Enter email address
3. Enter password
4. Handle 2FA via SMS or app push
5. Verify dashboard loads
6. Maintain session for account access

## Error Handling
- Login Failed: Retry, check credentials
- 2FA Required: Complete SMS verification
- Account Locked: Direct to support
- Session Expired: Re-authenticate automatically
- Rate Limited: Wait 60 seconds, retry
- Feature Unavailable: Note which products enrolled

## Self-Improvement Instructions
After each interaction:
- Track account check patterns
- Note loan monitoring frequency
- Log APY rate changes
- Document UI changes

Suggest updates when:
- SoFi updates interface
- New products added
- Interest rates change
- Member benefits update

## Notes
- Claude CANNOT make transactions
- All access is read-only for security
- SoFi is a full financial services company
- Member benefits include rate discounts
- Relay for free credit monitoring
- SoFi Stadium naming rights (events)
- Direct deposit unlocks highest APY
