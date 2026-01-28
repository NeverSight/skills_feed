---
name: lawpay
description: Process legal payments with LawPay's attorney payment processing platform.
category: legal
---
# LawPay Skill

Process legal payments with LawPay's attorney payment processing platform.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/lawpay/install.sh | bash
```

Or manually:
```bash
cp -r skills/lawpay ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set LAWPAY_API_KEY "your_api_key"
canifi-env set LAWPAY_SECRET_KEY "your_secret_key"
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

1. **Payment Processing**: Accept credit card and eCheck payments
2. **Trust Accounting**: Properly handle client trust funds
3. **Payment Links**: Send payment requests via email
4. **Recurring Billing**: Set up recurring payment plans
5. **Reporting**: Access payment reports and reconciliation

## Usage Examples

### Send Payment Request
```
User: "Send a payment request for $5000 to the client"
Assistant: Creates and sends payment link
```

### Process Payment
```
User: "Charge the client's card on file"
Assistant: Processes payment transaction
```

### View Transactions
```
User: "Show me this month's payment transactions"
Assistant: Returns transaction history
```

### Setup Recurring
```
User: "Set up a monthly payment plan for $1000"
Assistant: Creates recurring billing schedule
```

## Authentication Flow

1. Get API credentials from LawPay dashboard
2. Use API key and secret for authentication
3. Test mode available for development
4. Compliant with bar associations

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid credentials | Verify API keys |
| 400 Bad Request | Invalid payment data | Check card details |
| 402 Payment Failed | Card declined | Try different payment |
| 429 Rate Limited | Too many requests | Wait and retry |

## Notes

- Designed for legal industry
- ABA recommended
- Trust account compliant
- PCI compliant
- Integrates with legal software
- Bar association approved
