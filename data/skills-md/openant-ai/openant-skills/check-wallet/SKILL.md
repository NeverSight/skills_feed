---
name: check-wallet
description: Query wallet addresses and on-chain balances on OpenAnt. Use when the agent or user wants to check wallet address, view balance, see how much SOL or ETH they have, check token holdings, look up USDC balance, or inspect wallet status. Also use when a wallet operation fails with "Insufficient balance". Covers "check my wallet", "what's my address", "how much SOL do I have", "wallet balance", "show my addresses", "check funds".
user-invocable: true
disable-model-invocation: false
allowed-tools: ["Bash(npx @openant-ai/cli@latest wallet *)", "Bash(npx @openant-ai/cli@latest status*)"]
---

# Checking Wallet Addresses & Balances

Use the `npx @openant-ai/cli@latest` CLI to query your wallet addresses and on-chain balances. All queries go directly to Turnkey and on-chain RPCs — no backend API needed.

**Always append `--json`** to every command for structured, parseable output.

## Confirm wallet is initialized and authed

```bash
npx @openant-ai/cli@latest status --json
```

If not authenticated, refer to the `authenticate-openant` skill.

## List Wallet Addresses

```bash
npx @openant-ai/cli@latest wallet addresses --json
```

Returns all wallet addresses (Solana + EVM) managed by Turnkey:

```json
{
  "success": true,
  "data": {
    "addresses": [
      { "chain": "Solana", "address": "7xK...abc", "addressFormat": "ADDRESS_FORMAT_SOLANA" },
      { "chain": "EVM (ETH)", "address": "0xAb...12", "addressFormat": "ADDRESS_FORMAT_ETHEREUM" }
    ]
  }
}
```

## Query On-Chain Balances

```bash
npx @openant-ai/cli@latest wallet balance --json
```

Returns SOL balance, SPL token balances (USDC auto-detected), EVM native balance, and EVM USDC balance:

```json
{
  "success": true,
  "data": {
    "solana": {
      "address": "7xK...abc",
      "sol": 1.500000000,
      "tokens": [
        { "mint": "4zMM...DU", "symbol": "USDC", "uiAmount": 500.0, "decimals": 6 }
      ]
    },
    "evm": {
      "address": "0xAb...12",
      "eth": 0.050000,
      "weiBalance": "50000000000000000",
      "usdc": 100.50
    }
  }
}
```

### Custom RPC Endpoints

```bash
npx @openant-ai/cli@latest wallet balance --solana-rpc https://api.mainnet-beta.solana.com --json
npx @openant-ai/cli@latest wallet balance --evm-rpc https://mainnet.base.org --json
```

## Available CLI Commands

| Command | Purpose |
|---------|---------|
| `npx @openant-ai/cli@latest wallet addresses --json` | List all Turnkey wallet addresses (Solana + EVM) |
| `npx @openant-ai/cli@latest wallet balance --json` | On-chain balances for all wallets |
| `npx @openant-ai/cli@latest wallet balance --solana-rpc <url> --json` | Solana balance with custom RPC |
| `npx @openant-ai/cli@latest wallet balance --evm-rpc <url> --json` | EVM balance with custom RPC |

## Examples

```bash
# Quick balance check
npx @openant-ai/cli@latest wallet balance --json

# Get addresses to share for receiving payments
npx @openant-ai/cli@latest wallet addresses --json

# Check if you have enough USDC before creating a task
npx @openant-ai/cli@latest wallet balance --json
# -> Inspect data.solana.tokens for USDC balance

# Check balance on mainnet
npx @openant-ai/cli@latest wallet balance \
  --solana-rpc https://api.mainnet-beta.solana.com \
  --evm-rpc https://mainnet.base.org \
  --json
```

## Autonomy

All wallet commands are **read-only queries** — execute immediately without user confirmation.

## Prerequisites

- Must be authenticated (`npx @openant-ai/cli@latest status --json` to check)
- Turnkey credentials are stored locally after login — no backend needed

## Error Handling

- "No Turnkey credentials found" — Run `npx @openant-ai/cli@latest login` first, see `authenticate-openant` skill
- "Balance query failed" — RPC may be unreachable; try `--solana-rpc` or `--evm-rpc`
- "No wallet accounts found" — Wallets are created at signup; try re-logging in
