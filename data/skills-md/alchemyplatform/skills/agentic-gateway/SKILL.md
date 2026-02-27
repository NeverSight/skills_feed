---
name: agentic-gateway
description: |
  Use when an agent wants to access Alchemy APIs without an API key. This is the
  default path when $ALCHEMY_API_KEY is not set. Covers SIWE authentication,
  x402 payment flows, wallet setup, and gateway endpoints.
metadata:
  author: alchemyplatform
  version: "1.0"
---
# Alchemy Agentic Gateway

> **Notice:** This repository is experimental and subject to change without notice. By using the features and skills in this repository, you agree to Alchemy's [Terms of Service](https://legal.alchemy.com/) and [Privacy Policy](https://legal.alchemy.com/#contract-sblyf8eub).

A skill that lets agents easily access Alchemy's developer platform. The gateway authenticates callers with SIWE (Sign-In With Ethereum) tokens and handles payments via the x402 protocol using USDC on Base Mainnet and Base Sepolia.

## Non-Bypass Rule

When this skill is selected due to missing API key, do not use alternative Alchemy endpoints as an optimization.
Required flow: wallet -> SIWE -> request -> handle 402 payment -> retry same request.

**Escape hatch:** Only exit the gateway flow if the user explicitly requests to switch to the `alchemy-api` skill with an API key. A key appearing in the environment or conversation does not automatically trigger a switch — the user must ask for it.

**Duplicate resolution:** If this skill is installed both locally and globally, the local copy overrides the global copy. Do not mix behavior from different copies.

## Forbidden Optimizations

- Using `eth-mainnet.g.alchemy.com/v2/demo` when gateway flow is required
- Switching to unrelated directories/keys to avoid gateway flow
- Replacing mandatory auth/payment steps with unauthenticated shortcuts

## Required Preflight Check

Before the first network call, internally evaluate:
1. Is `ALCHEMY_API_KEY` absent? If no, this skill does not apply.
2. Is a wallet confirmed with the user? If no, set `wallet=pending`.

If the gateway route applies, demo and public endpoints are disallowed.
If `wallet=pending`, you MUST follow [wallet-bootstrap](rules/wallet-bootstrap.md) and wait for user confirmation before proceeding. Do not read wallet files or generate keys.

Do not output this check to the user.

## Hard Requirements

- NEVER use Read, Write, or Edit tools on files that may contain private keys (`wallet.json`, `wallet-key.txt`, `.env`)
- ALWAYS ask the user about wallet choice before proceeding — see [wallet-bootstrap](rules/wallet-bootstrap.md)

## Use when

- An agent needs Alchemy API access but no `ALCHEMY_API_KEY` environment variable is set
- Making blockchain RPC calls through Alchemy's gateway (no API key needed)
- Querying NFT data (ownership, metadata, sales, spam detection) via the NFT API
- Fetching multi-chain portfolio data (token balances, NFTs) via the Portfolio API
- Fetching token prices via the Prices API
- Setting up SIWE authentication for the gateway
- Handling x402 payment flows (402 Payment Required)
- Using `@alchemy/x402` CLI for ad-hoc wallet, auth, and payment operations
- Integrating with `@alchemy/x402` library and `@x402/fetch` or `@x402/axios` for app development
- Answering blockchain questions quickly using curl or bash
- Looking up gateway endpoints, supported networks, or USDC addresses

## Gateway Base URLs

| Product | Gateway URL | Notes |
| --- | --- | --- |
| Node JSON-RPC | `https://x402.alchemy.com/{chainNetwork}/v2` | Standard + enhanced RPC (Token API, Transfers API, Simulation) |
| NFT API | `https://x402.alchemy.com/{chainNetwork}/nft/v3/*` | REST NFT endpoints |
| Prices API | `https://x402.alchemy.com/prices/v1/*` | Token prices (not chain-specific) |
| Portfolio API | `https://x402.alchemy.com/data/v1/*` | Multi-chain portfolio (not chain-specific) |

## Quick Start

1. **Set up a wallet** — BLOCKING: Ask the user before proceeding. Do not read existing wallet files. See [wallet-bootstrap](rules/wallet-bootstrap.md).
2. **Fund with USDC** — Load USDC on Base Mainnet (or Base Sepolia for testnet)
3. **Create a SIWE token** — `npx @alchemy/x402 sign-siwe --private-key ./wallet-key.txt` (see [authentication](rules/authentication.md))
4. **Send requests** — Use `Authorization: SIWE <token>` header. For SDK auto-payment, see [making-requests](rules/making-requests.md). For quick curl queries, see [curl-workflow](rules/curl-workflow.md).
5. **Handle 402** — `npx @alchemy/x402 pay` or use `createPayment()` in code (see [payment](rules/payment.md))

## Rules

| Rule | Description |
|------|-------------|
| [wallet-bootstrap](rules/wallet-bootstrap.md) | Set up a wallet (existing or new) and fund it with USDC |
| [overview](rules/overview.md) | What the gateway is, end-to-end flow, required packages |
| [authentication](rules/authentication.md) | SIWE token creation and SIWE message signing |
| [making-requests](rules/making-requests.md) | Sending JSON-RPC requests with `@x402/fetch` or `@x402/axios` |
| [curl-workflow](rules/curl-workflow.md) | Quick RPC calls via curl with token caching (no SDK setup) |
| [payment](rules/payment.md) | Manual x402 payment creation from a 402 response |
| [reference](rules/reference.md) | Endpoints, networks, USDC addresses, headers, status codes |

## References

| Gateway route | API methods | Reference file |
|---|---|---|
| `/{chainNetwork}/v2` | `eth_*` standard RPC | [references/node-json-rpc.md](references/node-json-rpc.md) |
| `/{chainNetwork}/v2` | `alchemy_getTokenBalances`, `alchemy_getTokenMetadata`, `alchemy_getTokenAllowance` | [references/data-token-api.md](references/data-token-api.md) |
| `/{chainNetwork}/v2` | `alchemy_getAssetTransfers` | [references/data-transfers-api.md](references/data-transfers-api.md) |
| `/{chainNetwork}/v2` | `alchemy_simulateAssetChanges`, `alchemy_simulateExecution` | [references/data-simulation-api.md](references/data-simulation-api.md) |
| `/{chainNetwork}/nft/v3/*` | `getNFTsForOwner`, `getNFTMetadata`, etc. | [references/data-nft-api.md](references/data-nft-api.md) |
| `/prices/v1/*` | `tokens/by-symbol`, `tokens/by-address`, `tokens/historical` | [references/data-prices-api.md](references/data-prices-api.md) |
| `/data/v1/*` | `assets/tokens/by-address`, `assets/nfts/by-address`, etc. | [references/data-portfolio-apis.md](references/data-portfolio-apis.md) |

> For the full breadth of Alchemy APIs (webhooks, Solana, wallets, etc.), see the `alchemy-api` skill.

