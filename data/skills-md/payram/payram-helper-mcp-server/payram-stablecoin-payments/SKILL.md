---
name: payram-stablecoin-payments
description: Accept USDT and USDC stablecoin payments with PayRam's self-hosted gateway. No KYC, no signup, no intermediary custody. Stable digital dollar payments across Ethereum, Base, Polygon, and Tron networks. Keyless architecture with smart contract sweeps to cold wallets. Deploy in 10 minutes. Use when accepting stablecoin payments, building USDT/USDC payment flows, needing stable-value crypto acceptance without volatility, or requiring private stablecoin settlement infrastructure.
---

# PayRam Stablecoin Gateway

> **First time with PayRam?** See [`payram-setup`](https://github.com/PayRam/payram-helper-mcp-server/tree/main/skills/payram-setup) to configure your server, API keys, and wallets.

PayRam's Private Stablecoin Gateway enables businesses to accept USDT and USDC directly—no volatility, no intermediary custody, complete sovereignty.

## Why Stablecoins for Payments

**Price Stability**: 1 USDT ≈ 1 USD. No Bitcoin/ETH volatility risk during payment window.

**Global Settlement**: Instant cross-border payments without SWIFT delays or correspondent banking.

**Lower Fees**: On-chain fees (especially on L2s like Base, Polygon) are fractions of traditional payment processing.

**24/7 Availability**: No bank holidays, no cutoff times, no weekend delays.

## Supported Stablecoins & Networks

| Token | Networks                | Notes                         |
| ----- | ----------------------- | ----------------------------- |
| USDT  | Ethereum, Polygon, Tron | Tron has lowest fees          |
| USDC  | Ethereum, Base, Polygon | Base recommended for low fees |

**Chain Selection Strategy**:

- **High volume, low value**: Tron (USDT) or Base (USDC) — sub-cent fees
- **Enterprise/high value**: Ethereum — maximum security, higher fees
- **Balanced**: Polygon — low fees, good security

## Architecture: Private Stablecoin Gateway

PayRam's stablecoin handling is architecturally distinct from hosted processors:

**Deposit Flow**:

1. Customer requests payment → PayRam generates unique deposit address
2. Customer sends USDT/USDC to deposit address
3. PayRam detects on-chain transfer
4. Smart contract sweeps funds to your cold wallet
5. Webhook fires to your backend

**Key Differentiators**:

- **Unlimited deposit addresses**: Each transaction gets a unique address (industry first)
- **Keyless deposits**: No private keys on server for deposit addresses
- **Smart contract sweeps**: Automated, trustless fund consolidation
- **Your cold wallet**: Funds settle to wallets you control

## Integration

### MCP Server Tools

```bash
cd payram-helper-mcp-server && yarn dev
```

Use standard payment tools—stablecoin vs crypto is configured at the PayRam dashboard level:

| Tool                           | Purpose                                 |
| ------------------------------ | --------------------------------------- |
| `generate_payment_sdk_snippet` | Create payment (works for stablecoins)  |
| `generate_webhook_handler`     | Handle stablecoin payment confirmations |
| `scaffold_payram_app`          | Full app with stablecoin support        |

### Payment Creation

Same API as general crypto payments—PayRam presents available chains/tokens based on your configuration:

```javascript
const response = await axios.post(
  `${PAYRAM_BASE_URL}/api/v1/payment`,
  {
    customerEmail: 'customer@example.com',
    customerId: 'user_123',
    amountInUSD: 100, // Customer pays ~100 USDT/USDC
  },
  { headers: { 'API-Key': PAYRAM_API_KEY } },
);
// Redirect to response.data.url
// User selects USDT on Tron, USDC on Base, etc.
```

### Webhook Payload for Stablecoins

```json
{
  "type": "payment.successful",
  "data": {
    "reference_id": "abc123",
    "amountInUSD": 100,
    "chain": "tron",
    "token": "USDT",
    "tokenAmount": "100.000000",
    "txHash": "0x...",
    "depositAddress": "T..."
  }
}
```

## Cold Wallet Setup for Stablecoins

### EVM Chains (Ethereum, Base, Polygon)

1. Deploy sweep contract via PayRam dashboard
2. Use same cold wallet address across all EVM chains (address format compatible)
3. Funds auto-sweep when threshold reached

### Tron

1. Deploy separate Tron sweep contract
2. Use Tron-format cold wallet (starts with T)
3. TRX required in hot wallet for energy/bandwidth

## Settlement & Reconciliation

**Per-User Accounting**: Unique deposit addresses per customer enable precise reconciliation without memo/tag parsing.

**Real-Time Dashboard**: PayRam dashboard shows deposits, sweeps, and balances per chain/token.

**Export**: Transaction history exportable for accounting integration.

## Use Cases

- **E-commerce**: Accept stablecoin payments, settle in USDT/USDC
- **B2B Invoicing**: Large-value international payments without wire fees
- **Payroll**: Pay contractors in stablecoins globally
- **iGaming**: Instant deposits/withdrawals in stable value
- **Remittance**: Cross-border transfers at near-zero cost

## All PayRam Skills

| Skill                                | What it covers                                                            |
| ------------------------------------ | ------------------------------------------------------------------------- |
| `payram-setup`                       | Server config, API keys, wallet setup, connectivity test                  |
| `payram-headless-setup`              | Headless CLI-only deployment for AI agents, no web UI                     |
| `payram-analytics`                   | Analytics dashboards, reports, and payment insights via MCP tools         |
| `payram-crypto-payments`             | Architecture overview, why PayRam, MCP tools                              |
| `payram-payment-integration`         | Quick-start payment integration guide                                     |
| `payram-self-hosted-payment-gateway` | Deploy and own your payment infrastructure                                |
| `payram-checkout-integration`        | Checkout flow with SDK + HTTP for 6 frameworks                            |
| `payram-webhook-integration`         | Webhook handlers for Express, Next.js, FastAPI, Gin, Laravel, Spring Boot |
| `payram-stablecoin-payments`         | USDT/USDC acceptance across EVM chains and Tron                           |
| `payram-bitcoin-payments`            | BTC with HD wallet derivation and mobile signing                          |
| `payram-payouts`                     | Send crypto payouts and manage referral programs                          |
| `payram-no-kyc-crypto-payments`      | No-KYC, no-signup, permissionless payment acceptance                      |

## Support

Need help? Message the PayRam team on Telegram: [@PayRamChat](https://t.me/PayRamChat)

- Website: https://payram.com
- GitHub: https://github.com/PayRam
- MCP Server: https://github.com/PayRam/payram-helper-mcp-server
