---
name: grimoire-uniswap
description: Retrieves Uniswap router metadata using the Grimoire venue CLI. Use when you need router addresses, adapter information, or Uniswap V3/V4 details.
---

# Grimoire Uniswap Skill

Use this skill to inspect Uniswap metadata and produce token/pool snapshots for spells.

Preferred invocations:

- `grimoire venue uniswap ...`
- `npx -y @grimoirelabs/cli venue uniswap ...` (no-install)
- `bun run packages/cli/src/index.ts venue uniswap ...` (repo-local)
- `grimoire-uniswap ...` (direct binary from `@grimoirelabs/venues`)

## Commands

- `grimoire venue uniswap info [--format <json|table>]`
- `grimoire venue uniswap routers [--chain <id>] [--format <json|table>]`
- `grimoire venue uniswap tokens [--chain <id>] [--symbol <sym>] [--address <addr>] [--source <url>] [--format <json|table|spell>]`
- `grimoire venue uniswap pools --chain <id> --token0 <address|symbol> --token1 <address|symbol> [--fee <bps>] [--limit <n>] [--source <url>] [--format <json|table|spell>] [--endpoint <url>] [--graph-key <key>] [--subgraph-id <id>] [--rpc-url <url>] [--factory <address>]`

If you provide `--rpc-url` (or `RPC_URL`) and omit `--endpoint`/`--graph-key`, pools uses onchain factory lookups instead of The Graph.

## Examples

```bash
grimoire venue uniswap info --format table
grimoire venue uniswap routers
grimoire venue uniswap routers --chain 1
grimoire venue uniswap tokens --chain 1 --symbol USDC --format spell
grimoire venue uniswap pools --chain 1 --token0 USDC --token1 WETH --fee 3000 --format spell
grimoire venue uniswap pools --chain 8453 --token0 USDC --token1 WETH --fee 500 --rpc-url $RPC_URL --format table
grimoire venue uniswap pools --chain 8453 --token0 USDC --token1 WETH --fee 500 --graph-key $GRAPH_API_KEY --subgraph-id <id> --format table
```

Use `--format spell` on `tokens` or `pools` to emit a `params:` snapshot block.

## Supported Adapters

| Adapter | Router | Approval Flow |
|---------|--------|---------------|
| `@uniswap_v3` | SwapRouter02 | Standard ERC20 approve |
| `@uniswap_v4` | Universal Router | Permit2 |

## Notes

- CLI currently exposes V3 metadata. V4 adapter is available programmatically via `createUniswapV4Adapter()`.
- Outputs JSON/table; `tokens` and `pools` also support `--format spell`.
- Only metadata is exposed (no on-chain quote endpoints).
