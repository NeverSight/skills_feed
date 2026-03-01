---
name: emerging-movers
description: >-
  Lightweight scanner tracking Smart Money market concentration across all
  Hyperliquid assets. Flags assets accelerating up the ranks before they
  become crowded top-3 plays. IMMEDIATE_MOVER signal fires on 10+ rank
  jumps with quality filters (erratic history, velocity gate, trader count
  floor, max leverage check). One API call per scan, runs every 60 seconds.
  Use when detecting SM rotations, finding emerging opportunities early,
  or monitoring rank acceleration patterns.
license: Apache-2.0
compatibility: >-
  Requires python3 and cron. Single API call per scan via mcporter.
  Optional: max-leverage.json for leverage filtering.
metadata:
  author: jason-goldberg
  version: "3.1"
  platform: senpi
  exchange: hyperliquid
---

# Emerging Movers Detector v3.1

Tracks Smart Money market concentration across all Hyperliquid assets and flags assets accelerating up the ranks before they become crowded top-3 plays. By the time an asset hits the top of the SM leaderboard, the easy money is gone. This catches the trajectory.

**One API call per scan. Near-zero LLM tokens. Runs every 60 seconds.**

## How It Works

### The SM Profit Concentration Leaderboard

Senpi's `leaderboard_get_markets` returns all assets ranked by percentage of total Smart Money profit in the last 4-hour rolling window. This isn't trader count — it's where the money is actually flowing.

```
#1  ETH SHORT   31.4%  286 traders
#2  BTC SHORT   25.1%  436 traders
#3  HYPE SHORT  24.2%  330 traders
...
#36 ASTER SHORT  0.2%   18 traders  ← 60s later: #13, 0.82%, 65 traders
```

The script tracks this leaderboard over time and detects acceleration.

## Detection Signals

### Immediate Action Signals (v3+)

| Signal | Condition | Priority |
|--------|-----------|----------|
| **IMMEDIATE_MOVER** | 10+ rank jump from #25+ in ONE scan | Highest — act now |
| **NEW_ENTRY_DEEP** | Appears in top 20 from nowhere | Very high |
| **CONTRIB_EXPLOSION** | 3x+ contribution increase in one scan | Very high |
| **DEEP_CLIMBER** | 5+ rank jump from #25+ | High |

### Trend Signals

| Signal | Condition |
|--------|-----------|
| NEW_ENTRY | First appearance in top 50 |
| RANK_UP | Jumped 2+ positions in one scan |
| CLIMBING | 3+ positions up over several scans |
| ACCEL | Contribution % increasing scan-over-scan |
| STREAK | Consistently climbing every check |
| VELOCITY | Sustained positive contribution growth |

### v3.1 Quality Filters

These prevent false IMMEDIATE signals that looked great on rank jump alone but failed on execution:

| Filter | Rule | Rationale |
|--------|------|-----------|
| **Erratic rank** | >5 rank reversals in history → `erratic: true`, downgraded | Bouncing ranks are noise |
| **Velocity gate** | contribVelocity < 0.03 → `lowVelocity: true`, excluded from IMMEDIATE | No momentum behind the move |
| **Trader count floor** | <10 traders → SKIP IMMEDIATE | Single whale risk |
| **Max leverage check** | max leverage < 10x → SKIP | Not worth the limited position sizing |

See [references/quality-filters.md](references/quality-filters.md) for implementation details and real-world examples.

## Architecture

```
┌────────────────────────────────────┐
│ Cron: every 60 seconds             │
├────────────────────────────────────┤
│ scripts/emerging-movers.py         │
│ • Loads scan history from JSON     │
│ • Fetches leaderboard (1 API call) │
│ • Parses top 50 markets            │
│ • Compares with previous scans     │
│ • Detects signals + v3.1 filters   │
│ • Saves updated history            │
│ • Outputs JSON with alerts         │
├────────────────────────────────────┤
│ Agent reads output:                │
│ • IMMEDIATE alerts → evaluate now  │
│ • Deep climbers → queue for review │
│ • No alerts → silent               │
└────────────────────────────────────┘
```

## Files

| File | Purpose |
|------|---------|
| `scripts/emerging-movers.py` | Scanner script |
| `emerging-movers-history.json` | Auto-managed scan history (last 60 scans) |
| `max-leverage.json` | Optional: asset max leverage reference |

## Output

See [references/output-schema.md](references/output-schema.md) for the complete JSON schema.

Key top-level fields: `alerts[]`, `topMovers[]`, `immediateMovers[]`, `deepClimbers[]`, `scanCount`, `timestamp`.

Per-alert fields: `asset`, `direction`, `rank`, `prevRank`, `contribution`, `traderCount`, `reasons[]`, `contribVelocity`, `isImmediate`, `isDeepClimber`, `erratic`, `lowVelocity`.

## Cron Setup

```
*/1 * * * * python3 scripts/emerging-movers.py
```

### Agent Response Logic

- `isImmediate: true` + `erratic: false` + `lowVelocity: false` → **Evaluate immediately** for entry via Scanner
- `isDeepClimber: true` → Queue for next scanner run
- `erratic: true` or `lowVelocity: true` → Log but do not act
- No alerts → Silent

## Companion Recipes

- **opportunity-scanner** — use Scanner to deep-dive assets flagged by Emerging Movers
- **autonomous-trading** — full loop integrating Emerging Movers as entry trigger
- **wolf-strategy** — uses IMMEDIATE_MOVER as primary entry signal
