---
name: grimoire-hyperliquid
description: Queries Hyperliquid public market data using the Grimoire venue CLI. Use when you need mid prices, L2 order books, or open orders.
---

# Grimoire Hyperliquid Skill

Use the Grimoire CLI for public Hyperliquid market data.

Preferred:

- `grimoire venue hyperliquid ...`

If you installed `@grimoirelabs/venues` directly, you can also use `grimoire-hyperliquid`.

## When to use

- Fetch Hyperliquid mid prices, books, or metadata for quick VM prototyping.
- Produce snapshot `params` blocks with `--format spell` for VM runs.

## Prerequisites

- Global CLI: `npm i -g @grimoirelabs/cli`
- No install: `npx -y @grimoirelabs/cli venue hyperliquid ...`

## VM snapshot usage

Use `--format spell` to emit a VM-ready `params:` block you can paste into a spell.

## Commands

- `grimoire venue hyperliquid mids [--format <json|table|spell>]`
- `grimoire venue hyperliquid l2-book --coin <symbol> [--format <json|table|spell>]`
- `grimoire venue hyperliquid open-orders --user <address> [--format <json|table|spell>]`
- `grimoire venue hyperliquid meta [--format <json|table|spell>]`
- `grimoire venue hyperliquid spot-meta [--format <json|table|spell>]`

## Examples

```bash
grimoire venue hyperliquid mids --format table
grimoire venue hyperliquid mids --format spell
grimoire venue hyperliquid l2-book --coin BTC
grimoire venue hyperliquid l2-book --coin BTC --format spell
grimoire venue hyperliquid open-orders --user 0x0000000000000000000000000000000000000000
grimoire venue hyperliquid meta
```

## Notes

- Outputs JSON plus a human-readable table.
- Use `--format spell` for VM-ready snapshots.
- Uses Hyperliquid Info endpoints only (no authenticated actions).
