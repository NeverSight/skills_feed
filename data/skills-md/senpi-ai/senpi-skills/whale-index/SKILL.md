---
name: whale-index
description: >-
  Auto-mirror top Discovery traders on Hyperliquid. Scans top 50 traders,
  scores on PnL rank (35%), win rate (25%), consistency (20%), hold time (10%),
  drawdown (10%). Creates 2-5 mirror strategies with overlap checks.
  Daily rebalance with 2-day watch period before swaps.
  Use when setting up trader mirroring, copy trading, or portfolio
  auto-rebalancing based on Discovery leaderboard performance.
license: Apache-2.0
compatibility: >-
  Requires mcporter (configured with Senpi auth) and cron for daily monitoring.
metadata:
  author: jason-goldberg
  version: "1.0"
  platform: senpi
  exchange: hyperliquid
---

# Whale Index — Auto-Mirror Top Discovery Traders

Scan the Discovery leaderboard, score traders, create mirror strategies, and rebalance daily. Set your risk level and budget — the agent handles selection, allocation, monitoring, and swaps.

## 5-Step Flow

### Step 1: Onboard the User

Collect: budget, risk tolerance (conservative/moderate/aggressive).

| Budget | Slots |
|--------|-------|
| $500-$2k | 2 |
| $2k-$5k | 3 |
| $5k-$10k | 4 |
| $10k+ | 5 |

Risk mapping:

| Risk | Allowed Labels | Max Leverage |
|------|---------------|-------------|
| Conservative | ELITE only | 10x |
| Moderate | ELITE, RELIABLE | 15x |
| Aggressive | ELITE, RELIABLE, BALANCED | 25x |

### Step 2: Discover Traders

**2a. Pull candidates:** `discovery_top_traders(limit=50, timeframe="30d")`

**2b. Hard filters:**
- Consistency label matches risk level
- Risk label matches risk level
- Min 30d track record
- Not already in user's portfolio

**2c. Score remaining candidates:**

```
score = 0.35 × pnl_rank + 0.25 × win_rate + 0.20 × consistency + 0.10 × hold_time + 0.10 × drawdown
```

All components normalized 0-100.

**2d. Overlap check:** Compare active positions across selected traders. Flag >50% position overlap.

**2e. Allocation weighting:**
Score-weighted allocation with 35% cap per slot. Re-normalize after capping.

### Step 3: Present & Confirm

Show the user: trader address, rank, labels, win rate, allocation amount. Wait for approval before executing.

### Step 4: Execute

For each slot:
1. Create mirror strategy via `strategy_create_mirror`
2. Set strategy-level stop loss (-10% conservative, -15% moderate, -25% aggressive)
3. Confirm mirroring is active

### Step 5: Daily Monitoring (Cron)

See [references/daily-monitoring.md](references/daily-monitoring.md) for the complete daily check procedure, swap criteria, and rebalance logic.

**Swap criteria (ALL must be true):**
1. Degraded: dropped below rank 50 OR consistency fell OR inactive 48h+ OR drawdown 2× historical
2. Sustained: WATCH status for 2+ consecutive days (tracked via `watchCount`)
3. Better alternative: replacement scores ≥15% higher
4. User's strategy-level SL not hit

**Key principle:** The 2-day watch period prevents churn from temporary dips.

## Teardown

To exit: close all mirror strategies, return funds to main wallet.

## API Dependencies

- `discovery_top_traders` — trader leaderboard
- `strategy_create_mirror` — create mirror strategy
- `strategy_get_clearinghouse_state` — check positions
- `strategy_close_strategy` — teardown

## Fee Estimates

Mirror strategies incur the same trading fees as the mirrored trader's activity. Budget ~0.5-1% daily in fees for active traders.
