---
name: send-usdc
description: Send USDC to an Ethereum address or ENS name. Use when you or the user want to send money, pay someone, transfer USDC, tip, donate, or send funds to a wallet address or .eth name. Covers phrases like "send $5 to", "pay 0x...", or "transfer to vitalik.eth".
user-invocable: true
disable-model-invocation: false
allowed-tools: ["Bash(npx awal@latest status*)", "Bash(npx awal@latest send *)", "Bash(npx awal@latest balance*)"]
---

# Sending USDC

Use the `npx awal@latest send` command to transfer USDC from the wallet to any Ethereum address or ENS name on Base.

## Confirm wallet is initialized and authed

```bash
npx awal@latest status
```

If the wallet is not authenticated, refer to the `authenticate-wallet` skill.

## Command Syntax

```bash
npx awal@latest send <amount> <recipient> [--chain <chain>] [--json]
```

## Arguments

| Argument    | Description                                                                                                                                                                                                                          |
| ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `amount`    | Amount to send: '$1.00', '1.00', or atomic units (1000000 = $1). Always single-quote amounts that use `$` to prevent bash variable expansion. If the number looks like atomic units (no decimal or > 100), treat as atomic units. Assume that people won't be sending more than 100 USDC the majority of the time |
| `recipient` | Ethereum address (0x...) or ENS name (vitalik.eth)                                                                                                                                                                                   |

## Options

| Option           | Description                        |
| ---------------- | ---------------------------------- |
| `--chain <name>` | Blockchain network (default: base) |
| `--json`         | Output result as JSON              |

## Examples

```bash
# Send $1.00 USDC to an address
npx awal@latest send 1 0x1234...abcd

# Send $0.50 USDC to an ENS name
npx awal@latest send 0.50 vitalik.eth

# Send with dollar sign prefix (note the single quotes)
npx awal@latest send '$5.00' 0x1234...abcd

# Get JSON output
npx awal@latest send 1 vitalik.eth --json
```

## ENS Resolution

ENS names are automatically resolved to addresses via Ethereum mainnet. The command will:

1. Detect ENS names (any string containing a dot that isn't a hex address)
2. Resolve the name to an address
3. Display both the ENS name and resolved address in the output

## Prerequisites

- Must be authenticated (`npx awal@latest awal status` to check, `npx awal@latest awal auth login` to sign in, see skill `authenticate-wallet` for more information)
- Wallet must have sufficient USDC balance (`npx awal balance` to check)

## Error Handling

Common errors:

- "Not authenticated" - Run `awal auth login <email>` first
- "Insufficient balance" - Check balance with `awal balance`
- "Could not resolve ENS name" - Verify the ENS name exists
- "Invalid recipient" - Must be valid 0x address or ENS name
