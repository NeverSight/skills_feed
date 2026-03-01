---
name: autonomous-trading
description: >-
  Give your agent a budget, a target, and a deadline — it does the rest.
  Orchestrates DSL + Opportunity Scanner + Emerging Movers into a full
  autonomous trading loop on Hyperliquid. Race condition prevention,
  conviction collapse cuts, cross-margin buffer math, speed filter.
  3 risk profiles: conservative, moderate, aggressive.
  Use when setting up autonomous trading, creating a trading strategy,
  or running a scan-evaluate-trade-protect loop.
license: Apache-2.0
compatibility: >-
  Requires python3, mcporter, and cron. Depends on dsl-dynamic-stop-loss,
  opportunity-scanner, and emerging-movers skills.
metadata:
  author: jason-goldberg
  version: "6.0"
  platform: senpi
  exchange: hyperliquid
---

# Autonomous Trading v6

Give your agent a budget, a target, and a deadline — then let it trade. The agent creates a strategy wallet, scans for opportunities, opens positions, protects profits with DSL, and enforces risk controls.

## Prerequisites

Install these companion skills first:

1. **dsl-dynamic-stop-loss** — trailing stops, auto-closing, per-tier retrace
2. **opportunity-scanner** — market scanning, scoring, hourly trend gate
3. **emerging-movers** — SM rotation detection, IMMEDIATE_MOVER signals

**Minimum budget:** $500 (recommend $1k+)

## Known Bugs & Gotchas

See [references/bugs-and-gotchas.md](references/bugs-and-gotchas.md) — critical issues from live trading including the `dryRun` bug, phantom closes, XYZ DEX margin type, Tier 1 lock misconception, and scanner leverage vs actual max.

## The Flow

### Step 1: Ask the User

Collect: budget, target, deadline, risk tolerance (conservative/moderate/aggressive), asset preferences.

### Step 2: Calculate the Playbook

See [references/risk-rules.md](references/risk-rules.md) for complete risk rules by profile.

**v6 Core Rules:**

**The #1 Rule — Hourly Trend Alignment.** ALL trades must confirm with hourly candle structure. Counter-trend = hard skip, no exceptions. This single rule prevents the majority of losing trades.

**Max Leverage Check.** Always check `max-leverage.json` before entering. Scanner leverage is conservative, not actual max.

**Concentration Over Diversification.** At small account sizes ($500-$10k), 2-4 high-conviction positions beat 6 mediocre ones. Cross-margin math: 4 positions → 80.6% margin buffer, 2 positions → 89.7%.

**Every Slot Must Maximize ROI.** Empty slot > mediocre position. If a position isn't working, cut it and free the slot.

**Speed Filter.** Best moves happen FAST (XRP hit Tier 3 in 19 min, XMR Tier 2 in 37 min). Slow movers are suspects.

### Directional Exposure Guard
Before opening, check total LONG vs SHORT notional. Cap at 70% in one direction.

### Position Sizing by Score
| Scanner Score | Position Size |
|---|---|
| 250+ | Up to max per-position |
| 200-250 | 75% of max |
| 175-200 | 50% of max |
| < 175 | Skip |

### Step 3: Create the Strategy

```
strategy_create_strategy(budgetUsd, leverageType, riskLabel)
```

Returns `strategyId` + `walletAddress`. Fund the wallet.

### Step 4: Create the Playbook File

JSON config tracking: risk profile, position limits, score thresholds, active positions, trade journal. See [references/playbook-schema.md](references/playbook-schema.md).

### Step 5: Set Up Cron Jobs

**Race Condition Prevention (v6 — CRITICAL)**

Multiple cron jobs (scanner, SM flip, DSL) can all try to close the same position. When ANY job closes a position:

```python
# 1. Close the position
result = close_position(wallet, asset)

# 2. Immediately deactivate DSL state file
state["active"] = False
save_state(state)

# 3. Disable DSL cron for this asset
disable_cron(f"dsl-{asset}")
```

All three steps MUST happen in the same action. This prevents phantom closes.

**Cron Schedule:**

| Job | Interval | Purpose |
|---|---|---|
| Opportunity Scanner | 10-30 min (time-aware) | Find setups |
| DSL Monitor | 2-3 min per position | Trailing stops |
| SM Flip Detector | 5 min | Conviction changes |
| Portfolio Update | 15 min | Reporting |

See [references/cron-setup.md](references/cron-setup.md) for detailed cron configuration, time-aware scheduling, and SM flip detection logic.

### Step 6: The Trading Loop

```
SCAN → EVALUATE → TRADE → PROTECT → REPEAT

For each scan result:
1. Check hourly trend alignment (HARD REQUIREMENT)
2. Check directional exposure guard
3. Check max leverage via max-leverage.json
4. Score ≥ 175? → Size by score tier
5. Open position → Create DSL state → Start DSL cron
6. Journal the trade (scanner snapshot at entry)
```

### v6: Dead Weight Cutting

| Condition | Action |
|---|---|
| SM conviction drops 4→1 (e.g., 220→24 traders in 10 min) | Cut immediately |
| Dead weight at conviction 0 | Cut immediately — free the slot |
| Position stagnant, better opportunity available | Rotate |

### Step 7: Safety Rails

**Hard Stops (automatic):**
- Daily loss limit hit → stop trading for the day
- Total drawdown hard stop → close all positions, alert user
- DSL breach → auto-close (handled by script)

**What the Agent Should NEVER Do:**
- Trade counter-trend on hourly
- Exceed position size limits
- Override DSL
- Average down on a losing position
- Ignore the directional exposure guard

### Step 8: Lessons from the Field

See [references/lessons.md](references/lessons.md) for what works, what doesn't, retrace tuning, and fee awareness from live trading.

## API Reference

See [references/api-tools.md](references/api-tools.md) for the key Senpi tools used by this recipe.
