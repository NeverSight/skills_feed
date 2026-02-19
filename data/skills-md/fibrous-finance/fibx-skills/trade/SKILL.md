---
name: trade
description: Swap tokens using Fibrous aggregation on Base, Citrea, HyperEVM, or Monad. Finds optimal route, simulates before execution.
license: MIT
compatibility: Requires Node.js 18+ and npx. Works with fibx CLI v0.3.5+.
metadata:
    version: 0.3.5
    author: ahmetenesdur
    category: transaction
allowed-tools:
    - Bash(npx fibx@latest trade *)
    - Bash(npx fibx@latest status)
    - Bash(npx fibx@latest balance *)
    - Bash(npx fibx@latest balance)
    - Bash(npx fibx@latest tx-status *)
---

# Trade / Swap Tokens

Exchange one token for another via Fibrous aggregation. The CLI finds the best route, handles token approvals, simulates the swap, and executes.

> **Note:** Automatically detects and executes **Wrap** (Native -> Wrapped) and **Unwrap** (Wrapped -> Native) operations directly via contract calls, bypassing aggregation to save gas.

## Prerequisites

- Active session required.
- Sufficient balance of the source token + gas fees.

## Rules

1. BEFORE any trade, you MUST run `npx fibx@latest status` and `npx fibx@latest balance` to verify connectivity and source token balance.
2. If the user specifies a chain, you MUST include `--chain <name>`. If not specified, default to `base` and state it.
3. Default slippage is **0.5%**. To change it, you MUST ask the user for confirmation before using `--slippage`.
4. The CLI defaults to **exact approval** for ERC-20 tokens. NEVER use `--approve-max` unless the user explicitly requests it.
5. AFTER a successful trade, you MUST verify the transaction using `tx-status` with the same `--chain` flag.

## Chain Reference

| Chain    | Flag               | Native Token |
| -------- | ------------------ | ------------ |
| Base     | `--chain base`     | ETH          |
| Citrea   | `--chain citrea`   | cBTC         |
| HyperEVM | `--chain hyperevm` | HYPE         |
| Monad    | `--chain monad`    | MON          |

## Commands

```bash
npx fibx@latest trade <amount> <from_token> <to_token> [--chain <chain>] [--slippage <n>] [--approve-max] [--json]
```

## Parameters

| Parameter     | Type   | Description                              | Required |
| ------------- | ------ | ---------------------------------------- | -------- |
| `amount`      | number | Amount of source token to swap           | Yes      |
| `from_token`  | string | Source token symbol (e.g. `ETH`, `USDC`) | Yes      |
| `to_token`    | string | Target token symbol (e.g. `USDC`, `DAI`) | Yes      |
| `chain`       | string | `base`, `citrea`, `hyperevm`, or `monad` | No       |
| `slippage`    | number | Slippage tolerance in % (e.g. `1.0`)     | No       |
| `approve-max` | flag   | Use infinite approval instead of exact   | No       |
| `json`        | flag   | Output as JSON                           | No       |

Default chain: `base`. Default slippage: `0.5`.

## Examples

**User:** "Swap 0.1 ETH for USDC"

```bash
npx fibx@latest status
npx fibx@latest balance
npx fibx@latest trade 0.1 ETH USDC
npx fibx@latest tx-status <hash>
```

**User:** "Buy USDC with 1 MON on Monad"

```bash
npx fibx@latest status
npx fibx@latest balance --chain monad
npx fibx@latest trade 1 MON USDC --chain monad
npx fibx@latest tx-status <hash> --chain monad
```

**User:** "Wrap 1 ETH to WETH on Base"

```bash
npx fibx@latest status
npx fibx@latest balance
npx fibx@latest trade 1 ETH WETH --chain base
npx fibx@latest tx-status <hash>
```

**User:** "Unwrap 0.5 wMON on Monad"

```bash
npx fibx@latest status
npx fibx@latest balance --chain monad
npx fibx@latest trade 0.5 wMON MON --chain monad
npx fibx@latest tx-status <hash> --chain monad
```

## Error Handling

| Error                  | Action                                                        |
| ---------------------- | ------------------------------------------------------------- |
| `No route found`       | Liquidity may be too low or pair doesn't exist on the chain.  |
| `Insufficient balance` | Check `balance` and suggest a smaller amount.                 |
| `Slippage exceeded`    | Price moved unfavorably — suggest retrying with `--slippage`. |
| `Simulation failed`    | Route is invalid or would revert. Do not retry blindly.       |
| `Not authenticated`    | Run `authenticate-wallet` skill first.                        |
| `Rate limit / 429`     | Use `config` skill to set a custom RPC.                       |
