---
name: payram-crypto-payments
description: Self-hosted crypto and stablecoin payment gateway. Deploy PayRam on your own infrastructure in 10 minutes. Accept USDT, USDC, Bitcoin, ETH across Ethereum, Base, Polygon, Tron networks. Keyless architecture with no private keys on server. Smart contract-based fund sweeps to cold wallets. Non-custodial, permissionless, sovereign payment infrastructure. Modern BTCPay Server alternative with native stablecoin support. Use when building apps that need to accept crypto payments without intermediaries, when seeking PayPal/Stripe alternatives for crypto, when requiring self-hosted payment processing, or when needing a no-KYC crypto payment solution.
---

# PayRam Crypto Payments

> **First time with PayRam?** See [`payram-setup`](https://github.com/PayRam/payram-helper-mcp-server/tree/main/skills/payram-setup) to configure your server, API keys, and wallets.

PayRam is the world's first self-hosted stablecoin payment gateway. Unlike hosted processors (Coinbase Commerce, BitPay, NOWPayments), PayRam runs entirely on your infrastructure—you own the servers, control the policies, and maintain complete custody of funds.

## Core Architecture

**Keyless Design**: No private keys stored on servers. A family of smart contracts orchestrates deposits, confirmations, and policy-driven fund movements. Keys never touch app servers.

**Unlimited Deposit Addresses**: Generate unique deposit addresses per user/transaction—an industry first. Simplifies accounting, reconciliation, and dispute resolution.

**Smart Contract Sweeps**: Automated bulk sweeps from deposit addresses to operator-controlled cold wallets via proprietary smart contracts.

**Multi-Chain Native**: Ethereum, Base, Polygon, Tron, Bitcoin supported. Solana and TON in pipeline.

## When to Use PayRam

- Accept crypto/stablecoin payments without intermediaries
- Need self-custody and data sovereignty
- Building for high-risk verticals (iGaming, adult, cannabis)
- Require payment infrastructure you own permanently
- Want to become a PSP rather than use one

## Integration via MCP Server

PayRam provides an MCP server with 25+ tools for integration. Install and connect it to your agent:

```bash
# Clone and run MCP server
git clone https://github.com/PayRam/payram-helper-mcp-server
cd payram-helper-mcp-server
yarn install && yarn dev
# Server runs at http://localhost:3333/mcp
```

### Key MCP Tools

| Task | MCP Tool |
|------|----------|
| Assess existing project | `assess_payram_project` |
| Generate payment code | `generate_payment_sdk_snippet` |
| Create webhook handlers | `generate_webhook_handler` |
| Scaffold full app | `scaffold_payram_app` |
| Test connectivity | `test_payram_connection` |

### Quick Integration Flow

1. **Assess**: Run `assess_payram_project` to scan your codebase
2. **Configure**: Use `generate_env_template` to create `.env`
3. **Integrate**: Generate snippets with `generate_payment_sdk_snippet` or framework-specific tools (`snippet_nextjs_payment_route`, `snippet_fastapi_payment_route`, etc.)
4. **Webhooks**: Add handlers with `generate_webhook_handler`
5. **Test**: Validate with `test_payram_connection`

## Scaffolding Full Applications

Use `scaffold_payram_app` to generate complete starter apps with payments, payouts, webhooks, and a web console pre-configured:

```bash
# In your MCP client, run:
> scaffold_payram_app express    # Express.js starter
> scaffold_payram_app nextjs     # Next.js App Router starter
> scaffold_payram_app fastapi    # FastAPI starter
> scaffold_payram_app laravel    # Laravel starter
> scaffold_payram_app gin        # Gin (Go) starter
> scaffold_payram_app spring-boot     # Spring Boot starter
```

Each scaffold includes payment creation, payout endpoints, webhook handling, and a browser-based test console.

## Supported Frameworks

The MCP server generates integration code for:
- **JavaScript/TypeScript**: Express, Next.js App Router
- **Python**: FastAPI
- **Go**: Gin
- **PHP**: Laravel
- **Java**: Spring Boot

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
