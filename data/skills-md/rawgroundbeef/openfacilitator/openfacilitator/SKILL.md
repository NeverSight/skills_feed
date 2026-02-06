---
name: openfacilitator
description: >
  x402 payment integration via OpenFacilitator SDK. Use when implementing
  crypto payments, paywalls, API monetization, or tipping/transfer flows.
  Triggers: "x402", "OpenFacilitator", "crypto payments", "USDC payments",
  "paywall", "payment middleware", "verify and settle", "402 Payment Required".
  Supports EVM (Base, Ethereum, Polygon, Arbitrum, Avalanche, Sei, IoTeX, Peaq, X Layer)
  and Solana and Stacks chains.
---

# OpenFacilitator x402 SDK

Add x402 crypto payments to any TypeScript/JavaScript server. The SDK handles payment verification, on-chain settlement, and optional refund protection.

## Install

```bash
npm install @openfacilitator/sdk
```

Both ESM and CJS are supported. Package version: 1.0.0.

## Core Concept

x402 is an HTTP-native payment protocol. A server returns `402 Payment Required` with payment requirements. The client signs a payment and retries with an `X-PAYMENT` header. The server verifies and settles the payment on-chain.

The OpenFacilitator SDK provides two integration patterns:

1. **Middleware** (recommended) — Drop-in Express or Hono middleware that handles the full 402 flow automatically.
2. **Manual verify + settle** — Call `verify()` and `settle()` yourself for full control over business logic between verification and settlement.

## Quick Start — Middleware

### Express

```typescript
import { createPaymentMiddleware } from '@openfacilitator/sdk';
import type { PaymentContext } from '@openfacilitator/sdk';

const paymentMiddleware = createPaymentMiddleware({
  facilitator: 'https://pay.openfacilitator.io',
  getRequirements: () => ({
    scheme: 'exact',
    network: 'base',
    maxAmountRequired: '1000000', // $1 USDC (6 decimals)
    asset: '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913',
    payTo: '0xYOUR_WALLET_ADDRESS',
  }),
});

app.post('/api/resource', paymentMiddleware, (req, res) => {
  // Payment verified & settled. Access context:
  const { transactionHash, userWallet, amount } =
    (req as unknown as { paymentContext: PaymentContext }).paymentContext;
  res.json({ success: true, txHash: transactionHash });
});
```

### Hono

```typescript
import { honoPaymentMiddleware } from '@openfacilitator/sdk';
import type { PaymentContext } from '@openfacilitator/sdk';

// Declare paymentContext variable for type-safe c.get()
type Env = { Variables: { paymentContext: PaymentContext } };
const app = new Hono<Env>();

app.post('/api/resource', honoPaymentMiddleware({
  facilitator: 'https://pay.openfacilitator.io',
  getRequirements: (c) => ({
    scheme: 'exact',
    network: 'base',
    maxAmountRequired: '1000000',
    asset: '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913',
    payTo: '0xYOUR_WALLET_ADDRESS',
  }),
}), async (c) => {
  const ctx = c.get('paymentContext');
  return c.json({ success: true, txHash: ctx.transactionHash });
});
```

## Quick Start — Manual Verify + Settle

```typescript
import { OpenFacilitator } from '@openfacilitator/sdk';

const facilitator = new OpenFacilitator(); // defaults to pay.openfacilitator.io

const requirements = {
  scheme: 'exact',
  network: 'base',
  maxAmountRequired: '1000000',
  asset: '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913',
  payTo: '0xYOUR_WALLET_ADDRESS',
};

// 1. Verify the payment
const verifyResult = await facilitator.verify(paymentPayload, requirements);
if (!verifyResult.isValid) {
  throw new Error(verifyResult.invalidReason);
}

// 2. Your business logic here (create order, check inventory, etc.)

// 3. Settle on-chain (async — waits for confirmation)
const settleResult = await facilitator.settle(paymentPayload, requirements);
if (!settleResult.success) {
  throw new Error(settleResult.errorReason);
}
// settleResult.transaction = on-chain tx hash
```

## Pattern Selection Guide

| Use Case | Pattern | See |
|----------|---------|-----|
| Simple API paywall | Middleware | `references/patterns.md` §1-2 |
| Business logic between verify and settle | Manual verify + settle | `references/patterns.md` §3 |
| Per-request dynamic pricing | Middleware with dynamic `getRequirements` | `references/patterns.md` §4 |
| Refund protection | Either pattern + refund config | `references/patterns.md` §5 |
| Accept multiple chains | Either pattern + array requirements | `references/patterns.md` §6 |
| Build EVM payment payload (ERC-3009) | Client construction | `references/client-construction.md` §1 |
| Build Solana payment payload | Client construction | `references/client-construction.md` §2 |
| Server-side signing (Openfort/Privy/Turnkey) | Custodial pattern | `references/client-construction.md` §3 |
| Solana gas-free with fee payer | Fee payer integration | `references/client-construction.md` §2 |

## Key Facts

- **Amounts** are always in smallest units: `1000000` = $1 USDC (6 decimals).
- **Network IDs**: Use v1 short names (`base`, `solana`, `stacks`) in requirements. The SDK handles CAIP-2 conversion internally.
- **`settle()` is synchronous-feeling but async** — it waits for on-chain confirmation before returning the tx hash. No webhooks needed for settlement confirmation.
- **Payment header**: Clients send `X-PAYMENT` header containing base64-encoded JSON.
- **Default facilitator**: `https://pay.openfacilitator.io` (free, no account needed).
- **Refund protection** is opt-in via middleware config. Requires an API key from the dashboard.

## Common USDC Addresses

| Chain | Asset Address | Decimals |
|-------|--------------|----------|
| Base | `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` | 6 |
| Ethereum | `0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48` | 6 |
| Solana | `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v` | 6 |

See `references/schemas.md` for the full chain and token table.

## References

- `references/sdk-api.md` — Full TypeScript signatures, all exports, error classes
- `references/schemas.md` — Payment objects, requirements, chain/token details
- `references/patterns.md` — Complete working examples for every server-side integration pattern
- `references/client-construction.md` — How to BUILD payment payloads (ERC-3009, Solana SPL, fee payer, server-side signing)
- `references/troubleshooting.md` — Error handling, retries, edge cases
