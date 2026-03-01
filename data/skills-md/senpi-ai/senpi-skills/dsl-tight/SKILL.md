---
name: dsl-tight
description: >-
  Opinionated trailing stop loss preset for Hyperliquid perps with tighter
  defaults than DSL v4. 4 tiers with per-tier breach counts that tighten as
  profit grows (3→2→2→1), auto-calculated price floors from entry and leverage,
  stagnation take-profit that closes if ROE ≥8% but high-water stalls for 1 hour.
  Same ROE-based engine as DSL v4 — different defaults, fewer knobs.
  Use when you want aggressive profit protection with minimal configuration.
license: Apache-2.0
compatibility: >-
  Requires python3, mcporter (configured with Senpi auth), and cron.
  Hyperliquid perp positions only. Uses the same dsl-v4.py script as
  the dsl-dynamic-stop-loss skill.
metadata:
  author: jason-goldberg
  version: "1.0"
  platform: senpi
  exchange: hyperliquid
---

# DSL-Tight — Opinionated Stop-Loss Preset

A tighter, more opinionated variant of DSL for aggressive profit protection. Same ROE-based engine as DSL v4 (`PnL / margin × 100`) — all tier triggers automatically account for leverage.

**Key difference from DSL v4:** DSL v4 is the configurable engine with maximum flexibility. DSL-Tight is the "just works" preset — fewer knobs, tighter defaults, per-tier breach counts, stagnation exits, and auto-calculated floors.

## Core Concept

All thresholds defined in ROE. The script auto-converts to price levels:
```
price_floor = entry × (1 ± lockPct / 100 / leverage)
```

## How It Works

### Phase 1 — Absolute Floor (Stop-Loss)
- 5% ROE trailing floor
- 3 consecutive breaches required
- Auto-calculated absolute floor from entry/leverage/retrace

### Phase 2 — Tiered Profit Lock
4 tiers that lock an increasing percentage of the high-water move:

| Tier | Trigger ROE | Lock % of HW Move | Breaches to Close |
|------|-------------|--------------------|--------------------|
| 1 | 10% | 50% | 3 |
| 2 | 20% | 65% | 2 |
| 3 | 40% | 75% | 2 |
| 4 | 75% | 85% | 1 |

Per-tier breach counts tighten as profit grows — at Tier 4 (75% ROE), a single breach closes immediately.

### Stagnation Take-Profit
Auto-closes if:
- ROE ≥ 8% AND
- High-water mark hasn't improved for 1 hour

Catches winners that stall — takes the profit rather than waiting for a reversal.

## Breach Mechanics

- Hard decay only (breach count resets to 0 on recovery)
- Per-tier breach requirements (3→2→2→1) replace the global Phase 1/Phase 2 split
- Floor is always: `max(tier_floor, trailing_floor)` for LONG, `min()` for SHORT

## State File Schema

```json
{
  "active": true,
  "asset": "HYPE",
  "direction": "LONG",
  "leverage": 10,
  "entryPrice": 28.87,
  "size": 1890.28,
  "wallet": "0xYourStrategyWalletAddress",
  "strategyId": "uuid",
  "phase": 1,
  "phase1": {
    "retraceThreshold": 0.05,
    "consecutiveBreachesRequired": 3
  },
  "phase2TriggerTier": 0,
  "phase2": {
    "retraceThreshold": 0.015,
    "consecutiveBreachesRequired": 3
  },
  "tiers": [
    {"triggerPct": 10, "lockPct": 5, "retrace": 0.015, "breachesRequired": 3},
    {"triggerPct": 20, "lockPct": 13, "retrace": 0.012, "breachesRequired": 2},
    {"triggerPct": 40, "lockPct": 30, "retrace": 0.010, "breachesRequired": 2},
    {"triggerPct": 75, "lockPct": 64, "retrace": 0.006, "breachesRequired": 1}
  ],
  "breachDecay": "hard",
  "stagnation": {
    "enabled": true,
    "minRoePct": 8,
    "maxStaleSec": 3600
  },
  "currentTierIndex": -1,
  "tierFloorPrice": null,
  "highWaterPrice": 28.87,
  "floorPrice": null,
  "currentBreachCount": 0,
  "createdAt": "2026-02-23T10:00:00Z"
}
```

### Field Reference

| Field | Purpose |
|-------|---------|
| `phase1.absoluteFloor` | **Not needed** — auto-calculated from entry, leverage, retrace |
| `tiers[].breachesRequired` | Per-tier breach count (replaces global phase2 setting) |
| `tiers[].retrace` | Per-tier trailing stop tightness |
| `stagnation.enabled` | Enable stagnation take-profit |
| `stagnation.minRoePct` | Minimum ROE to trigger stagnation check |
| `stagnation.maxStaleSec` | Max seconds HW can be stale before auto-close |

## Cron Setup

Same as DSL v4:
```
DSL_STATE_FILE=/data/workspace/dsl-tight-HYPE.json python3 scripts/dsl-v4.py
```

Every 3 minutes per position. Script location: `scripts/dsl-v4.py` (same script as DSL v4).

## Key Safety Features

- `CLOSE_NO_POSITION` graceful handling — if position already closed, deactivate cleanly
- Auto-calculated floors eliminate manual math errors
- Per-tier breach tightening means large profits get maximum protection
- Stagnation TP prevents stalled winners from reversing

## Example Walkthrough

10x LONG entry at $28.87:

1. **Phase 1**: Floor auto-calculated ~$28.73. Price rises, HW tracks.
2. **Tier 1 at 10% ROE** ($29.16): Floor locks at ~$29.01, 3 breaches to close.
3. **Tier 2 at 20% ROE** ($29.45): Floor locks at ~$29.24, now only 2 breaches.
4. **Stagnation**: Price stalls at 12% ROE for 65 min → auto-closed with profit.
5. **Tier 4 at 75% ROE** ($31.04): Floor at ~$30.71. Single breach = instant close.

## Script Location

Uses the same `dsl-v4.py` script from the `dsl-dynamic-stop-loss` skill. Install that skill first, then use this state file template for the tighter preset.
