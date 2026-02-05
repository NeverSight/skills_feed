---
name: fluxa-agent-wallet
description: >-
  FluxA Agent Wallet integration via CLI. Enables agents to make x402 payments
  for paid APIs, send USDC payouts to any wallet, and create payment links to receive
  payments — all through a standalone Node.js CLI tool. Use when the user asks about
  crypto payments, x402, USDC transfers, payment links, or interacting with the
  FluxA Agent Wallet.
---

# FluxA Agent Wallet

FluxA Agent Wallet lets AI agents perform onchain financial operations — payments, payouts, and payment links — without managing private keys. This skill uses the **FluxA CLI** (`fluxa-cli.bundle.js`), a standalone Node.js script requiring no npm installation.

## Setup

The CLI bundle is located at `scripts/fluxa-cli.bundle.js` within this skill directory. It requires Node.js v18+.

```bash
node scripts/fluxa-cli.bundle.js <command> [options]
```

All commands output JSON to stdout:

```json
{ "success": true, "data": { ... } }
```

Or on error:

```json
{ "success": false, "error": "Error message" }
```

Exit code `0` = success, `1` = failure.

## Capabilities

| Capability | What it does | When to use |
|------------|-------------|-------------|
| **x402 Payment (v3)** | Pay for APIs using the x402 protocol with intent mandates | Agent hits HTTP 402, needs to pay for API access |
| **Payout** | Send USDC to any wallet address | Agent needs to transfer funds to a recipient |
| **Payment Link** | Create shareable URLs to receive payments | Agent needs to charge users, create invoices, sell content |

## Prerequisites — Register Agent ID

Before any operation, the agent must have an Agent ID. Register once:

```bash
node scripts/fluxa-cli.bundle.js init \
  --email "agent@example.com" \
  --name "My AI Agent" \
  --client "Agent v1.0"
```

Or pre-configure via environment variables:

```bash
export AGENT_ID="ag_xxxxxxxxxxxx"
export AGENT_TOKEN="tok_xxxxxxxxxxxx"
export AGENT_JWT="eyJhbGciOiJ..."
```

Verify status:

```bash
node scripts/fluxa-cli.bundle.js status
```

The CLI automatically refreshes expired JWTs.

## Quick Decision Guide

- Need to **pay for an API** that returned HTTP 402? → See [X402-PAYMENT.md](X402-PAYMENT.md)
- Need to **send funds** to a wallet address? → See [PAYOUT.md](PAYOUT.md)
- Need to **receive payments** via a shareable link? → See [PAYMENT-LINK.md](PAYMENT-LINK.md)

## Amount Format

All amounts are in **smallest units** (atomic units). For USDC (6 decimals):

| Human-readable | Atomic units |
|---------------|-------------|
| 0.01 USDC | `10000` |
| 0.10 USDC | `100000` |
| 1.00 USDC | `1000000` |
| 10.00 USDC | `10000000` |

## All Commands

| Command | Description |
|---------|-------------|
| `status` | Check agent configuration |
| `init` | Register agent ID |
| `mandate-create` | Create an intent mandate |
| `mandate-status` | Query mandate status |
| `x402-v3` | Execute x402 v3 payment |
| `payout` | Create a payout |
| `payout-status` | Query payout status |
| `paymentlink-create` | Create a payment link |
| `paymentlink-list` | List payment links |
| `paymentlink-get` | Get payment link details |
| `paymentlink-update` | Update a payment link |
| `paymentlink-delete` | Delete a payment link |
| `paymentlink-payments` | View payments received via a link |

## Environment Variables

| Variable | Description |
|----------|-------------|
| `AGENT_ID` | Pre-configured agent ID |
| `AGENT_TOKEN` | Pre-configured agent token |
| `AGENT_JWT` | Pre-configured agent JWT |
| `AGENT_EMAIL` | Email for auto-registration |
| `AGENT_NAME` | Agent name for auto-registration |
| `CLIENT_INFO` | Client info for auto-registration |
| `FLUXA_DATA_DIR` | Custom data directory (default: `~/.fluxa-ai-wallet-mcp`) |
| `WALLET_API` | Wallet API base URL (default: `https://walletapi.fluxapay.xyz`) |
| `AGENT_ID_API` | Agent ID API base URL (default: `https://agentid.fluxapay.xyz`) |
