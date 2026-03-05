---
name: nansen-prediction-market
description: Polymarket prediction market analytics — screener, OHLCV, orderbook, holders, trades, PnL. Use when researching prediction markets, checking market prices, or analyzing trader positions.
allowed-tools: Bash(nansen:*)
---

# Prediction Market Analytics (Polymarket)

All commands: `nansen research prediction-market <sub> [options]` (alias: `nansen research pm <sub>`)

No `--chain` flag needed — Polymarket runs on Polygon.

## Screeners

```bash
# Top markets by 24h volume
nansen research pm market-screener --sort-by volume_24hr --limit 20

# Search for specific markets
nansen research pm market-screener --query "bitcoin" --limit 10

# Find resolved/closed markets
nansen research pm market-screener --status closed --limit 10

# Screen events (groups of related markets)
nansen research pm event-screener --sort-by volume_24hr --limit 20
```

Sort options: `volume_24hr`, `volume`, `volume_1wk`, `volume_1mo`, `liquidity`, `open_interest`, `unique_traders_24h`, `age_hours`

Screeners return active/open markets by default. Use `--status closed` for resolved markets.

## OHLCV & Orderbook

```bash
nansen research pm ohlcv --market-id 654412 --sort period_start:desc --limit 50
nansen research pm orderbook --market-id 654412
```

## Holders & Positions

```bash
nansen research pm top-holders --market-id 654412 --limit 10
nansen research pm position-detail --market-id 654412 --limit 20
```

## Trades

```bash
# Trades for a specific market
nansen research pm trades-by-market --market-id 654412 --limit 20

# Trades for a specific address
nansen research pm trades-by-address --address 0x1234... --limit 20
```

## PnL

```bash
# PnL leaderboard for a market
nansen research pm pnl-by-market --market-id 654412 --limit 20

# PnL breakdown for a trader
nansen research pm pnl-by-address --address 0x1234...
```

## Categories

```bash
nansen research pm categories --pretty
```

## Flags

| Flag | Purpose |
|------|---------|
| `--market-id` | Market ID (required for most endpoints) |
| `--address` | EVM address (for trades-by-address, pnl-by-address) |
| `--sort-by` | Screener sort field (e.g. `volume_24hr`) |
| `--sort` | Sort field:direction for non-screener endpoints |
| `--query` | Search text (screeners only) |
| `--status` | `active` or `closed` (screeners only, default: active) |
| `--limit` | Number of results |
| `--fields` | Select specific fields |
| `--table` | Human-readable table output |
| `--format csv` | CSV export |

## Notes

- All address endpoints expect Polygon (EVM) addresses.
- `--market-id` is a numeric ID from the screener, not a slug.
- Non-screener endpoints (ohlcv, trades, pnl, etc.) work with any market ID regardless of status.
