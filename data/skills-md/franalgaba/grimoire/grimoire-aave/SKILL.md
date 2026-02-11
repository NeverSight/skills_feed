---
name: grimoire-aave
description: Fetches Aave V3 public market data using the Grimoire venue CLI. Use when you need Aave health checks, chain listings, market metadata, or reserve info.
---

# Grimoire Aave Skill

Use this skill to query Aave V3 metadata and reserve snapshots for strategy inputs.

Preferred invocations:

- `grimoire venue aave ...`
- `npx -y @grimoirelabs/cli venue aave ...` (no-install)
- `bun run packages/cli/src/index.ts venue aave ...` (repo-local)
- `grimoire-aave ...` (direct binary from `@grimoirelabs/venues`)

## Commands

- `grimoire venue aave health [--format <json|table>]`
- `grimoire venue aave chains [--format <json|table>]`
- `grimoire venue aave markets --chain <id> [--user <address>] [--format <json|table>]`
- `grimoire venue aave market --chain <id> --address <market> [--user <address>] [--format <json|table>]`
- `grimoire venue aave reserve --chain <id> --market <address> --token <address> [--format <json|table>]`
- `grimoire venue aave reserves --chain <id> [--market <address>] [--asset <symbol|address>] [--format <json|table|spell>]`

## Examples

```bash
grimoire venue aave health
grimoire venue aave health --format table
grimoire venue aave chains
grimoire venue aave markets --chain 1 --format table
grimoire venue aave market --chain 1 --address 0x87870Bca3F3fD6335C3F4ce8392D69350B4fA4E2
grimoire venue aave reserve --chain 1 --market 0x87870Bca3F3fD6335C3F4ce8392D69350B4fA4E2 --token 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48
grimoire venue aave reserves --chain 1 --asset USDC --format table
grimoire venue aave reserves --chain 1 --asset USDC --format spell
```

Use `--format spell` to emit a `params:` block for spell inputs.

## Supported Chains

| Chain | Market Address |
|-------|---------------|
| Ethereum (1) | `0x87870Bca3F3fD6335C3F4ce8392D69350B4fA4E2` |
| Base (8453) | `0xA238Dd80C259a72e81d7e4664a9801593F98d1c5` |

## Amount Format

The `@aave/client` SDK uses different amount formats per action:

| Action | Format | Example (0.1 USDC) |
|--------|--------|---------------------|
| supply | `value: "0.1"` | Human-readable BigDecimal |
| borrow | `value: "0.1"` | Human-readable BigDecimal |
| withdraw | `value: { exact: "100000" }` | Raw amount in `exact` wrapper |
| repay | `value: { exact: "100000" }` | Raw amount in `exact` wrapper |

The adapter handles this conversion automatically.

## Notes

- Read-only metadata endpoints only.
- Outputs JSON/table; `reserves` also supports `--format spell`.
