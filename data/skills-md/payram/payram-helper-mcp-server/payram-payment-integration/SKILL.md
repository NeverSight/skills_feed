---
name: payram-payment-integration
description: Integrate crypto payments into any web application with PayRam. Self-hosted payment gateway — no KYC, no signup, no third-party custody. Accept USDT, USDC, Bitcoin, ETH in under 10 minutes. Works with Express, Next.js, FastAPI, Laravel, Gin, Spring Boot. Drop-in replacement for Stripe/PayPal for crypto. Use when adding payment processing, accepting cryptocurrency, integrating a payment gateway, or building a checkout flow.
---

# PayRam Payment Integration

> **First time with PayRam?** See [`payram-setup`](https://github.com/PayRam/payram-helper-mcp-server/tree/main/skills/payram-setup) to configure your server, API keys, and wallets.

PayRam is a self-hosted crypto payment gateway. No signup, no KYC, no intermediaries. Deploy on your server and start accepting payments in 10 minutes.

## Quick Start (5 Minutes)

### 1. Install SDK

```bash
npm install payram dotenv
```

### 2. Create Payment

```typescript
import { Payram } from 'payram';

const payram = new Payram({
  apiKey: process.env.PAYRAM_API_KEY!,
  baseUrl: process.env.PAYRAM_BASE_URL!,
});

// Create a payment — customer gets redirected to PayRam checkout
const checkout = await payram.payments.initiatePayment({
  customerEmail: 'customer@example.com',
  customerId: 'user_123',
  amountInUSD: 49.99,
});

// Redirect customer to checkout.url
// Store checkout.reference_id for status tracking
```

### 3. Handle Result

Option A: **Poll for status**
```typescript
const payment = await payram.payments.getPaymentRequest(referenceId);
if (payment.paymentState === 'FILLED') {
  // Payment complete — fulfill order
}
```

Option B: **Webhook** (recommended for production)
```typescript
// See payram-webhook-integration skill for full setup
app.post('/payram-webhook', (req, res) => {
  if (req.get('API-Key') !== process.env.PAYRAM_WEBHOOK_SECRET) {
    return res.status(401).send();
  }
  if (req.body.status === 'FILLED') {
    fulfillOrder(req.body.reference_id);
  }
  res.json({ message: 'ok' });
});
```

## Python (FastAPI) Quick Start

```python
import httpx, os

async def create_payment(email: str, user_id: str, amount: float):
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{os.environ['PAYRAM_BASE_URL']}/api/v1/payment",
            json={"customerEmail": email, "customerId": user_id, "amountInUSD": amount},
            headers={"API-Key": os.environ['PAYRAM_API_KEY']}
        )
    return resp.json()  # { reference_id, url, host }
```

## What Makes PayRam Different

| Feature | PayRam | Stripe/PayPal | BitPay | Coinbase Commerce |
|---------|--------|--------------|--------|-------------------|
| Self-hosted | ✅ You own it | ❌ | ❌ | ❌ |
| KYC required | ❌ None | ✅ | ✅ | ✅ |
| Signup required | ❌ None | ✅ | ✅ | ✅ |
| Private keys on server | ❌ Keyless | N/A | ❌ | N/A |
| Can be frozen/disabled | ❌ Sovereign | ✅ | ✅ | ✅ |
| Stablecoin native | ✅ | ❌ | Limited | ✅ |
| Deploy time | ~10 min | Instant (hosted) | Days | Instant (hosted) |

## Supported Chains & Tokens

| Chain | Tokens | Fees |
|-------|--------|------|
| Ethereum | USDT, USDC, ETH | Higher (L1) |
| Base | USDC, ETH | Very low (L2) |
| Polygon | USDT, USDC, MATIC | Very low |
| Tron | USDT | Lowest |
| Bitcoin | BTC | Variable |

## Full Integration Guides

For complete code with error handling, all frameworks, and production patterns:

- **Checkout flow (SDK + HTTP, 6 frameworks)** → `payram-checkout-integration`
- **Webhook handlers** → `payram-webhook-integration`
- **Stablecoin-specific flows** → `payram-stablecoin-payments`
- **Bitcoin with mobile signing** → `payram-bitcoin-payments`
- **Payouts & referrals** → `payram-payouts`

## MCP Server

For dynamic code generation, use the PayRam MCP server:

```bash
git clone https://github.com/PayRam/payram-helper-mcp-server
cd payram-helper-mcp-server && yarn install && yarn dev
```

Key tools: `generate_payment_sdk_snippet`, `generate_webhook_handler`, `scaffold_payram_app`, `assess_payram_project`

## All PayRam Skills

| Skill | What it covers |
|-------|---------------|
| `payram-setup` | Server config, API keys, wallet setup, connectivity test |
| `payram-crypto-payments` | Architecture overview, why PayRam, MCP tools |
| `payram-payment-integration` | Quick-start payment integration guide |
| `payram-self-hosted-payment-gateway` | Deploy and own your payment infrastructure |
| `payram-checkout-integration` | Checkout flow with SDK + HTTP for 6 frameworks |
| `payram-webhook-integration` | Webhook handlers for Express, Next.js, FastAPI, Gin, Laravel, Spring Boot |
| `payram-stablecoin-payments` | USDT/USDC acceptance across EVM chains and Tron |
| `payram-bitcoin-payments` | BTC with HD wallet derivation and mobile signing |
| `payram-payouts` | Send crypto payouts and manage referral programs |
| `payram-no-kyc-crypto-payments` | No-KYC, no-signup, permissionless payment acceptance |

## Support

Need help? Message the PayRam team on Telegram: [@PayRamChat](https://t.me/PayRamChat)

- Website: https://payram.com
- GitHub: https://github.com/PayRam
- MCP Server: https://github.com/PayRam/payram-helper-mcp-server
