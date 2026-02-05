---
name: grimoire-morpho-blue
description: Fetches Morpho Blue public deployment metadata using the Grimoire venue CLI. Use when you need contract addresses or adapter info.
---

# Grimoire Morpho Blue Skill

Use the Grimoire CLI to read Morpho Blue deployment data.

Preferred:

- `grimoire venue morpho-blue ...`

If you installed `@grimoirelabs/venues` directly, you can also use `grimoire-morpho-blue`.

## Commands

- `grimoire venue morpho-blue info [--format <json|table>]`
- `grimoire venue morpho-blue addresses [--chain <id>] [--format <json|table>]`
- `grimoire venue morpho-blue vaults [--chain <id>] [--asset <symbol>] [--min-tvl <usd>] [--min-apy <decimal>] [--min-net-apy <decimal>] [--sort <field>] [--order <asc|desc>] [--limit <n>] [--format <json|table|spell>]`

## Examples

```bash
grimoire venue morpho-blue info --format table
grimoire venue morpho-blue addresses --chain 1
grimoire venue morpho-blue addresses --chain 8453
grimoire venue morpho-blue vaults --chain 8453 --asset USDC --min-tvl 5000000 --format table
grimoire venue morpho-blue vaults --chain 8453 --asset USDC --min-tvl 5000000 --format spell
```

## Default Markets (Base)

The adapter ships with pre-configured markets for Base (chain 8453):

| Market | Collateral | LLTV |
|--------|-----------|------|
| cbBTC/USDC | cbBTC | 86% |
| WETH/USDC | WETH | 86% |

When no collateral is specified in a spell, the first matching market by loan token is selected.

## Notes

- Outputs JSON plus a human-readable table.
- Uses the SDK's chain address registry.
