---
name: tx-status
description: Check the on-chain status of a transaction and get the block explorer link. Supports Base, Citrea, HyperEVM, and Monad.
license: MIT
compatibility: Requires Node.js 18+ and npx. Works with fibx CLI v0.3.6+.
metadata:
    version: 0.3.6
    author: ahmetenesdur
    category: utility
allowed-tools:
    - Bash(npx fibx@latest tx-status *)
---

# Transaction Status

Fetch on-chain receipt data for a transaction hash: status, block number, gas used, and explorer link.

## Prerequisites

- A valid transaction hash (starts with `0x`).
- No authentication required — this is a public chain query.

## Rules

1. You MUST use the same `--chain` flag that was used for the original transaction. A Base tx hash will not be found on Monad.
2. Use this skill AFTER every `send` or `trade` to verify success.

## Commands

```bash
npx fibx@latest tx-status <hash> [--chain <chain>] [--json]
```

## Parameters

| Parameter | Type   | Description                              | Required |
| --------- | ------ | ---------------------------------------- | -------- |
| `hash`    | string | Transaction hash (`0x...`)               | Yes      |
| `chain`   | string | `base`, `citrea`, `hyperevm`, or `monad` | No       |
| `json`    | flag   | Output as JSON                           | No       |

Default chain: `base`.

## Examples

**User:** "Did my transaction go through?"

```bash
npx fibx@latest tx-status 0x123...abc
```

**User:** "Check tx 0xabc...def on Monad"

```bash
npx fibx@latest tx-status 0xabc...def --chain monad
```

## JSON Output Structure

```json
{
	"status": "success",
	"blockNumber": "12345",
	"gasUsed": "21000",
	"from": "0x...",
	"to": "0x...",
	"explorerLink": "https://basescan.org/tx/0x...",
	"chain": "base"
}
```

## Error Handling

| Error                   | Action                                                |
| ----------------------- | ----------------------------------------------------- |
| `Transaction not found` | Verify you are querying the correct chain.            |
| `Pending`               | Transaction is still in the mempool — wait and retry. |
| `Rate limit / 429`      | Use `config` skill to set a custom RPC.               |
