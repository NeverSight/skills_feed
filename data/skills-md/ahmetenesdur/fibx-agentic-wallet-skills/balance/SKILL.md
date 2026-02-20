---
name: balance
description: Check wallet balances (native and ERC-20 tokens) on Base, Citrea, HyperEVM, or Monad.
license: MIT
compatibility: Requires Node.js 18+ and npx. Works with fibx CLI v0.3.6+.
metadata:
    version: 0.3.6
    author: ahmetenesdur
    category: wallet-data
allowed-tools:
    - Bash(npx fibx@latest balance *)
    - Bash(npx fibx@latest balance)
    - Bash(npx fibx@latest status)
---

# Check Balance

Fetch wallet holdings: native tokens and all ERC-20 tokens with non-zero balances.

## Prerequisites

- Active session required. If not authenticated, run `authenticate-wallet` skill first.

## Rules

1. If the user specifies a chain, you MUST include `--chain <name>`.
2. If the user does NOT specify a chain, default to `base` and state it: _"Checking your balance on Base."_
3. Use `--json` when the output will be consumed by another skill or pipeline.

## Chain Reference

| Chain    | Flag               | Native Token |
| -------- | ------------------ | ------------ |
| Base     | `--chain base`     | ETH          |
| Citrea   | `--chain citrea`   | cBTC         |
| HyperEVM | `--chain hyperevm` | HYPE         |
| Monad    | `--chain monad`    | MON          |

## Commands

```bash
npx fibx@latest balance [--chain <chain>] [--json]
```

## Parameters

| Parameter | Type   | Description                              | Required |
| --------- | ------ | ---------------------------------------- | -------- |
| `chain`   | string | `base`, `citrea`, `hyperevm`, or `monad` | No       |
| `json`    | flag   | Output as JSON                           | No       |

Default chain: `base`

## Examples

**User:** "Check my balance"

```bash
npx fibx@latest balance
```

**User:** "What's my Monad balance?"

```bash
npx fibx@latest balance --chain monad
```

## Error Handling

| Error               | Action                                                     |
| ------------------- | ---------------------------------------------------------- |
| `Not authenticated` | Run `authenticate-wallet` skill first.                     |
| `Network error`     | Retry once. If persistent, use `config` to set custom RPC. |
| `Rate limit / 429`  | Use `config` skill to set a custom RPC.                    |

## Related Skills

- Run this BEFORE `send` or `trade` to verify sufficient funds.
- Run this BEFORE `aave supply` to confirm available assets.
