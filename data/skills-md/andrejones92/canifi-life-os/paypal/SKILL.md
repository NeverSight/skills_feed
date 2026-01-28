---
name: paypal
description: Check balance, view transactions, monitor activity, and review invoices on PayPal
category: finance
---

# PayPal Skill

## Overview
Enables Claude to access PayPal to check balance, view transaction history, monitor account activity, and review invoices or subscriptions. Note: Claude cannot send money or make transactions.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/paypal/install.sh | bash
```

Or manually:
```bash
cp -r skills/paypal ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set PAYPAL_EMAIL "your-email@example.com"
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
- Check PayPal balance in all currencies
- View recent transaction history
- Monitor account notifications and alerts
- Review active subscriptions
- Check invoice status (sent/received)
- View linked accounts and cards

## Usage Examples

### Example 1: Check Balance
```
User: "What's my PayPal balance?"
Claude: I'll check your PayPal balance.
- Opens paypal.com via Playwright MCP
- Logs into account
- Returns: PayPal Balance: $1,234.56 USD
- Other currencies:
  - EUR: €45.00
  - GBP: £0.00
- Available to withdraw: $1,234.56
- Pending: $0.00
```

### Example 2: Review Subscriptions
```
User: "What subscriptions do I have through PayPal?"
Claude: I'll check your active subscriptions.
- Navigates to automatic payments
- Active subscriptions:
  - Netflix: $15.99/month, next: Jan 15
  - Spotify: $10.99/month, next: Jan 20
  - Adobe CC: $54.99/month, next: Feb 1
- Total monthly: $81.97
- Can provide cancellation links if needed
```

### Example 3: View Recent Activity
```
User: "Show my recent PayPal transactions"
Claude: I'll pull up your activity.
- Navigates to activity section
- Recent transactions:
  - Jan 6: -$89.99 to Amazon (purchase)
  - Jan 5: +$250.00 from Client (invoice)
  - Jan 4: -$15.99 to Netflix (subscription)
  - Jan 3: +$50.00 from John (payment received)
- This month: +$194.02 net
```

## Authentication Flow
1. Navigate to paypal.com via Playwright MCP
2. Click "Log In" and enter email
3. Enter password
4. Handle 2FA via SMS or authenticator
5. May require security questions
6. Maintain session for account access

## Error Handling
- Login Failed: Retry, check for security holds
- 2FA Required: Complete verification flow
- Account Limited: Direct to resolution center
- Session Expired: Re-authenticate (frequent)
- Rate Limited: Wait 2 minutes, retry
- Unusual Activity: May require additional verification

## Self-Improvement Instructions
After each interaction:
- Track balance check patterns
- Note subscription monitoring
- Log common transaction types
- Document UI changes

Suggest updates when:
- PayPal updates interface
- New features added
- Security flow changes
- Invoice features update

## Notes
- Claude CANNOT send money or make payments
- All access is read-only for security
- PayPal has strong fraud protection
- Multiple currencies supported
- Business vs personal account differences
- Buyer/seller protection varies
- Instant transfer available for fee
