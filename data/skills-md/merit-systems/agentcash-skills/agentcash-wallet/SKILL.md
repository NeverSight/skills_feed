---
name: agentcash-wallet
description: |
  Manage your agentcash wallet and call any x402-protected API with automatic payment. No API keys, no subscriptions — just a funded wallet (USDC on Base).

  USE FOR:
  - Checking wallet balance before API calls
  - Redeeming invite codes for free credits
  - Getting deposit address for USDC
  - Discovering endpoints and pricing on any x402-protected origin
  - Making paid API requests via the agentcash CLI
  - Troubleshooting payment failures

  TRIGGERS:
  - "balance", "wallet", "funds", "credits", "x402"
  - "redeem", "invite code", "promo code"
  - "deposit", "add funds", "top up"
  - "discover", "endpoints", "what APIs", "pricing"
  - "insufficient balance", "payment failed"
---

# agentcash Wallet & Paid APIs

Call any x402-protected API with automatic payment. Payment is the authentication — no API keys or subscriptions needed.

## Setup

If the agentcash CLI is not yet installed, see [rules/getting-started.md](rules/getting-started.md) for installation and wallet setup.

## Wallet Management

Your wallet is auto-created on first use and stored at `~/.agentcash/wallet.json`.

### Check Balance

```bash
npx agentcash wallet info
```

Returns wallet address, USDC balance, and deposit link. Always check before expensive operations.

### Redeem Invite Code

```bash
npx agentcash wallet redeem YOUR_CODE
```

One-time use per code. Credits added instantly. Run `npx agentcash wallet info` after to verify.

### Deposit USDC

1. Get your wallet address via `npx agentcash wallet info`
2. Send USDC on **Base network** (eip155:8453) to that address
3. Or use the deposit UI: `https://x402scan.com/mcp/deposit/<wallet-address>`

**Important**: Only Base network USDC. Other networks or tokens will be lost.

## Calling Paid APIs

### 1. Discover endpoints

```bash
npx agentcash discover https://stableenrich.dev
```

Returns all endpoints, pricing, and usage instructions. **Read the `instructions` field** — it has critical endpoint-specific guidance.

### 2. Check schema (optional)

```bash
npx agentcash check https://stableenrich.dev/api/apollo/people-search
```

Returns full request/response JSON schemas and pricing for a specific endpoint.

### 3. Make a paid request

```bash
npx agentcash fetch https://stableenrich.dev/api/apollo/people-search -m POST -b '{"person_titles": ["CEO"], "person_locations": ["San Francisco"]}'
```

Payment is automatic: sends request, gets 402 challenge, signs USDC payment, retries with credential, returns result. Payments settle only on success (2xx) — failed requests cost nothing.

## Available Services

| Origin | Service | What it does |
|---|---|---|
| `https://stableenrich.dev` | StableEnrich | Research APIs: Apollo (people/org), Exa (web search), Firecrawl (scraping), Grok (X/Twitter), Google Maps, Clado (LinkedIn), Serper (news/shopping), WhitePages, Reddit, Hunter (email verification), Influencer enrichment |
| `https://stableupload.dev` | StableUpload | Pay-per-upload file hosting. 10MB/$0.02, 100MB/$0.20, 1GB/$2.00. 6-month TTL |
| `https://stablestudio.dev` | StableStudio | AI image/video generation: GPT Image, Flux, Grok, Nano Banana, Sora, Veo, Seedance, Wan |
| `https://stablesocial.dev` | StableSocial | Social media data: TikTok, Instagram, X/Twitter, Facebook, Reddit, LinkedIn. $0.06/call, async two-step |
| `https://stableemail.dev` | StableEmail | Send emails ($0.02), forwarding inboxes ($1/mo), custom subdomains ($5) |
| `https://stablephone.dev` | StablePhone | AI phone calls ($0.54), phone numbers ($20), top-ups ($15) |
| `https://stablejobs.dev` | StableJobs | Job search via Coresignal |

Run `npx agentcash discover <origin>` on any origin to see its full endpoint catalog.

## Quick Reference

| Task | Command |
|------|---------|
| Check balance | `npx agentcash wallet info` |
| Redeem code | `npx agentcash wallet redeem <code>` |
| Discover endpoints | `npx agentcash discover <url>` |
| Check pricing/schema | `npx agentcash check <url>` |
| Paid POST request | `npx agentcash fetch <url> -m POST -b '{...}'` |
| Paid GET request | `npx agentcash fetch <url>` |

## Tips

- Always discover first — the `instructions` field has critical endpoint-specific patterns and required parameters.
- Payments settle only on success (2xx) — failed requests cost nothing.
- Use `npx agentcash check <url>` when unsure about request/response format.
- Add `--format json` for machine-readable output, `--format pretty` for human-readable.
- Add `-v` for verbose output to see payment details.
- Network: Base (eip155:8453), Currency: USDC.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Command not found" | Run `npm install -g agentcash` |
| "Insufficient balance" | Check balance, deposit USDC or redeem invite code |
| "Payment failed" | Transient error — retry the request |
| "Invalid invite code" | Code already used or doesn't exist |
| Balance not updating | Wait for Base network confirmation (~2 sec) |
