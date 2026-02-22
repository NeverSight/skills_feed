---
name: nansen-cli
description: Query the Nansen API for onchain analytics - Smart Money flows, wallet profiling, token analysis, and DeFi portfolio data. Use when analyzing crypto wallets, tracking smart money activity, or researching tokens.
license: MIT
metadata:
  author: nansen-ai
  version: "1.3.0"
compatibility: Requires Node.js 18+. Needs NANSEN_API_KEY environment variable or run `nansen login`.
---

# Nansen CLI

Command-line interface for the [Nansen API](https://docs.nansen.ai) - onchain analytics for crypto investors and AI agents.

## Setup

```bash
# Install globally
npm install -g nansen-cli

# Authenticate (interactive)
nansen login

# Or set environment variable
export NANSEN_API_KEY=your-api-key
```

Get your API key at [app.nansen.ai/api](https://app.nansen.ai/api).

## Commands

### Smart Money
Track sophisticated market participants:
```bash
nansen smart-money netflow --chain solana --pretty
nansen smart-money dex-trades --chain solana --labels "Smart Trader"
nansen smart-money holdings --chain solana
```

### Wallet Profiler
Analyze any wallet:
```bash
nansen profiler balance --address 0x123... --chain ethereum
nansen profiler labels --address 0x123... --chain ethereum
nansen profiler pnl --address 0x123... --chain ethereum
nansen profiler search --query "Vitalik"
```

### Token God Mode
Deep token analytics:
```bash
nansen token screener --chain solana --timeframe 24h
nansen token holders --token <address> --chain solana --smart-money
nansen token flows --token <address> --chain solana
nansen token pnl --token <address> --chain solana
```

### Portfolio
DeFi holdings analysis:
```bash
nansen portfolio defi --wallet 0x123...
```

## Output Formats

- **Default**: JSON (for AI agents)
- `--pretty`: Formatted JSON
- `--table`: Human-readable table
- `--stream`: NDJSON (one record per line)
- `--fields`: Filter specific fields

## Key Options

| Option | Description |
|--------|-------------|
| `--chain` | Blockchain (solana, ethereum, base, etc.) |
| `--chains` | Multiple chains as JSON array |
| `--limit` | Number of results |
| `--days` | Date range in days |
| `--sort` | Sort field (e.g., `value_usd:desc`) |
| `--smart-money` | Filter for Smart Money only |

## Supported Chains

ethereum, solana, base, bnb, arbitrum, polygon, optimism, avalanche, linea, scroll, zksync, mantle, ronin, sei, sonic, monad, hyperevm

## Smart Money Labels

Fund, Smart Trader, 30D Smart Trader, 90D Smart Trader, 180D Smart Trader, Smart HL Perps Trader

## Schema Introspection

Get the full API schema for programmatic use:
```bash
nansen schema --pretty
nansen schema smart-money --pretty
```

## Known Endpoint Issues

### Chain/Token-Specific Limitations
- `token holders --smart-money` — Fails with `UNSUPPORTED_FILTER` for tokens without smart money tracking (e.g., WCT on Optimism). Not all tokens have smart money data. Do not retry.
- `token flow-intelligence` — May return all-zero flows for tokens without significant smart money activity. This is normal, not an error.

### Credit Management
- `profiler labels` and `profiler balance` consume credits. Budget ~20 calls per session.
- `Insufficient credits` (403, code `CREDITS_EXHAUSTED`) is a hard stop — no retry will help.
- Check your Nansen dashboard for credit balance: [app.nansen.ai](https://app.nansen.ai).
- Run balance checks in batches of 3-4 to avoid burning credits on rate-limit retries.

### Error Codes to Watch
| Code | Meaning | Action |
|------|---------|--------|
| `UNSUPPORTED_FILTER` | Filter not available for this token/chain | Remove the filter and retry, or skip this token |
| `CREDITS_EXHAUSTED` | API credits depleted | Stop all API calls. Check dashboard. |
| `RATE_LIMITED` | Too many requests (429) | Wait and retry (automatic with default retry) |

## Examples

```bash
# Find trending Solana tokens with Smart Money activity
nansen token screener --chain solana --timeframe 24h --smart-money --pretty

# Check who's accumulating a specific token
nansen token holders --token So11111111111111111111111111111111111111112 --chain solana --smart-money --limit 20 --pretty

# Profile a whale wallet
nansen profiler balance --address Gu29tjXrVr9v5n42sX1DNrMiF3BwbrTm379szgB9qXjc --chain solana --pretty

# Track Smart Money flows into memecoins
nansen smart-money netflow --chain solana --labels "Smart Trader" --pretty
```
