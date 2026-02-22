---
name: controller-cli
description: Execute Starknet transactions using Cartridge Controller sessions with human-authorized policies. Use when the user wants to execute Starknet smart contract transactions, transfer tokens on Starknet, interact with gaming contracts, query contract state, check token balances, look up Cartridge usernames/addresses, or manage session-based authentication.
---

# Controller CLI

Manage Cartridge Controller sessions and execute Starknet transactions through a secure human-in-the-loop workflow.

## Prerequisites

Controller CLI must be installed:

```bash
curl -fsSL https://raw.githubusercontent.com/cartridge-gg/controller-cli/main/install.sh | bash
```

## Session Workflow

Sessions use keypair-based auth where humans authorize specific contracts/methods via browser, then the agent executes transactions within those constraints.

1. **Check status** — `controller session status --json`
2. **Authorize session** (if needed) — `controller session auth --file policy.json --json` (generates keypair + user must authorize via browser URL)
3. **Execute transactions** — `controller execute <contract> <entrypoint> <calldata> --json`

## Commands

### Session Management

```bash
controller session auth --file policy.json --json    # Generate keypair and authorize a new session
controller session auth --preset loot-survivor --json # Use a preset policy
controller session status --json                      # Check session status and expiration
controller session list --json                        # List all active sessions
controller session list --limit 20 --page 2 --json   # Paginated session list
controller session clear --yes                        # Clear all session data
```

The `session auth` command generates a keypair, outputs an authorization URL, and polls for up to 6 minutes until the user authorizes in their browser.

### Execute Transaction

Single call (positional args):

```bash
controller execute <contract> <entrypoint> <calldata> [--wait] [--timeout <secs>] --json
```

Multiple calls from file:

```bash
controller execute --file calls.json [--wait] --json
```

### Read-Only Call (no session required)

```bash
controller call <contract> <entrypoint> <calldata> --chain-id SN_SEPOLIA --json
controller call --file calls.json --chain-id SN_SEPOLIA --json
```

### Transaction Status

```bash
controller transaction <hash> --chain-id SN_SEPOLIA [--wait] --json
```

### Transaction Receipt

```bash
controller receipt <hash> --chain-id SN_SEPOLIA [--wait] --json
```

Returns full receipt: execution status, fee, events, messages, and execution resources.

### Token Balances

```bash
controller balance --json                    # All non-zero token balances
controller balance eth --json                # Specific token balance
controller balance --chain-id SN_MAIN --json # Query mainnet balances
```

Built-in tokens: ETH, STRK, USDC, USD.e, LORDS, SURVIVOR, WBTC. Add custom tokens via `controller config set token.<SYMBOL> <address>`.

### Account Username

```bash
controller username --json    # Display username for active session account
```

### Username/Address Lookup

```bash
controller lookup --usernames shinobi,sensei --json
controller lookup --addresses 0x123...,0x456... --json
```

### Configuration

```bash
controller config set <key> <value>    # Set a config value
controller config get <key> --json     # Get a config value
controller config list --json          # List all config values
```

Valid keys: `rpc-url`, `keychain-url`, `api-url`, `storage-path`, `json-output`, `colors`, `callback-timeout`, `token.<symbol>`.

## Calldata Format

- Values are comma-separated
- Hex: `0x64` (standard hex felt)
- Decimal: `100` (auto-converted)
- `u256:` prefix: `u256:1000000000000000000` (auto-splits into low/high 128-bit felts)
- `str:` prefix: `str:hello` (Cairo short string encoding)
- Manual u256: split into low,high — e.g., 100 tokens = `0x64,0x0`

## Policy File Format

See [references/policy-examples.md](references/policy-examples.md) for complete examples.

```json
{
  "contracts": {
    "<contract_address>": {
      "name": "Contract Name",
      "methods": [
        { "name": "transfer", "entrypoint": "transfer", "description": "Transfer tokens" }
      ]
    }
  }
}
```

## Multi-Call File Format

```json
{
  "calls": [
    {
      "contractAddress": "<contract_address>",
      "entrypoint": "transfer",
      "calldata": ["0xRECIPIENT", "0x64", "0x0"]
    }
  ]
}
```

## Common Contracts (Sepolia)

| Token | Address |
|-------|---------|
| ETH   | `0x049d36570d4e46f48e99674bd3fcc84644ddd6b96f7c741b1562b82f9e004dc7` |
| STRK  | `0x04718f5a0fc34cc1af16a1cdee98ffb20c31f5cd61d6ab07201858f4287c938d` |

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| NoSession | No keypair found | Run `controller session auth --file policy.json` |
| SessionExpired | Session expired | Run `controller session auth --file policy.json` |
| ManualExecutionRequired | No authorized session | Authorize session with appropriate policies |
| PolicyViolation | Transaction not in allowed policies | Authorize new session with expanded policies |

## Important Notes

- Always use `--json` flag for machine-readable output
- Sessions expire — always check status before transactions
- Human authorization is required for all sessions (cannot be bypassed)
- Sepolia transactions are automatically subsidized (no gas needed)
- Contract addresses must be 32-byte hex with `0x` prefix
