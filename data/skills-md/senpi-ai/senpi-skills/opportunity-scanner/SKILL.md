---
name: opportunity-scanner
description: >-
  4-stage funnel that screens all 500+ Hyperliquid perps down to the top
  trading opportunities. Scores setups 0-400 across smart money, market
  structure, technicals, and funding. BTC macro filter, hourly trend gate
  (counter-trend = hard skip), cross-scan momentum tracking. Near-zero LLM
  tokens — all computation in Python.
  Use when scanning for new trading opportunities on Hyperliquid, evaluating
  setups, or checking market conditions.
license: Apache-2.0
compatibility: >-
  Requires python3, mcporter (configured with Senpi auth), and cron.
  Hyperliquid perps only. Uses ThreadPoolExecutor for parallel candle fetches.
metadata:
  author: jason-goldberg
  version: "5.0"
  platform: senpi
  exchange: hyperliquid
---

# Opportunity Scanner v5

521 perps on Hyperliquid. Fetching candles + computing technicals for all = 500k+ tokens. This scanner screens everything but only burns tokens on real opportunities.

**All computation in Python. Near-zero LLM tokens.**

## The 4-Stage Funnel

### Stage 0: BTC Macro Context
Source: BTC 4h + 1h candles (2 API calls).
Output: `btc_trend` (strong_down/down/neutral/up/strong_up) and a `macro_modifier` applied to all final scores. Configurable via `scanner-config.json`.

### Stage 1: Bulk Screen (~0 LLM tokens)
Source: Single API call — `metaAndAssetCtxs`.
Filter: 24h volume > $500K (configurable).
Output: ~70 assets that pass minimum liquidity.

### Stage 2: Smart Money + Freshness Overlay (~0 LLM tokens)
Sources: `leaderboard_get_markets` + `leaderboard_get_top` (limit=100).
Two entries per asset (long + short) — keeps dominant side.
Freshness: `avgAtPeak` (>85% = live, <50% = stale), `nearPeakPct`.
Filter: Top 15-16 by quick score. Force-include top 8 SM assets.

### Stage 3: Deep Dive — Multi-Timeframe (~0 LLM tokens)
Parallel candle fetches via ThreadPoolExecutor (~20s vs ~60s sequential).

| Timeframe | Period | Candles | Purpose |
|---|---|---|---|
| 4h | 7 days | ~42 | Macro trend (EMA 5/13 crossover) |
| 1h | 24h | ~24 | **Hourly trend structure** + RSI, volume, S/R, patterns |
| 15m | 6h | ~24 | Entry: RSI, patterns, momentum, volume divergence |

**v5: Hourly Trend Classification** — analyzes swing highs/lows in 1h data to classify as UP/DOWN/NEUTRAL. See [references/hourly-trend.md](references/hourly-trend.md) for the algorithm.

**This is the #1 gate for all trade decisions.** NEVER open a LONG on `hourlyTrend: "DOWN"` or a SHORT on `hourlyTrend: "UP"`.

Per-TF error recovery: if 15m fetch fails, analysis continues with 4h+1h data.

### Stage 4: Cross-Scan Momentum
Saves results to `scan-history.json`. Computes `scoreDelta` (change from last scan) and `scanStreak` (consecutive appearances).

## 4-Pillar Scoring (25% each, 0-400 total)

See [references/scoring.md](references/scoring.md) for the complete point breakdowns.

### Pillar 1: Smart Money (25%)
PnL contribution tiers, trader count (v5: 400+ = +30 pts), acceleration, freshness. Trader count separates real signals from noise — conviction 4 with 130 traders caused whipsaws, conviction 4 with 400+ was consistently real.

### Pillar 2: Market Structure (25%)
Volume, volume surge, open interest, OI/volume ratio.

### Pillar 3: Technicals (25%)
4h trend alignment, **1h trend structure** (v5), RSI multi-TF convergence, volume confirmation, candlestick patterns, momentum. **Counter-trend on hourly: -30 points** (v5).

### Pillar 4: Funding (25%)
Neutral funding is best (+40). Favorable extreme is strong (+35). Unfavorable extreme hurts (-20).

### BTC Macro Modifier
Applied to final scores. Penalizes alt LONGs during BTC downtrend, boosts SHORTs (and vice versa). All modifiers configurable.

## Hard Disqualifiers (v5)

These cause an opportunity to be **skipped entirely**, not just penalized:

| Condition | Rationale |
|---|---|
| **Counter-trend on hourly** | SM conviction on a 1-min bounce doesn't override a 2-week downtrend. $346 lesson. |
| Extreme RSI (< 20 for SHORTs, > 80 for LONGs) | Reversal imminent |
| Counter-trend on 4h with strength > 50 | Strong macro against you |
| Volume dying (ratio < 0.5 on both TFs) | No liquidity |
| Funding heavily against you (> 50% ann) | Fee drag kills profits |
| BTC macro headwind > 30 pts | Market-wide risk |

## Architecture

```
┌──────────────────────────────────────────┐
│  Stage 0: BTC macro (2 API calls)        │
├──────────────────────────────────────────┤
│  Stage 1: metaAndAssetCtxs → ~70 assets  │
├──────────────────────────────────────────┤
│  Stage 2: SM + freshness → top 15-16     │
├──────────────────────────────────────────┤
│  Stage 3: parallel candle fetch + v5     │
│  hourly trend classification             │
├──────────────────────────────────────────┤
│  Stage 4: cross-scan momentum            │
├──────────────────────────────────────────┤
│  v5: Hard disqualifier check             │
├──────────────────────────────────────────┤
│  Final: scored JSON → LLM formats report │
│  Total: ~5k LLM tokens                  │
└──────────────────────────────────────────┘
```

## Files

| File | Purpose |
|---|---|
| `scripts/opportunity-scan-v5.py` | Python pipeline — fetches, scores, applies hourly gate |
| `scripts/opportunity-report.sh` | Wrapper — runs pipeline + outputs LLM prompt |
| `scanner-config.json` | User prefs: risk, leverage, macro modifiers |
| `scan-history.json` | Auto-maintained: last 12 scans for cross-scan tracking |
| `active-positions.json` | Current positions (conflict flags) |

## Config Schema

See [references/config-schema.md](references/config-schema.md) for the complete config with all options.

## Output Format

See [references/output-schema.md](references/output-schema.md) for the full output JSON schema.

Key fields per opportunity: `asset`, `direction`, `leverage`, `finalScore`, `hourlyTrend`, `trendAligned`, `pillarScores`, `smartMoney`, `technicals`, `funding`, `risks`, `scoreDelta`, `scanStreak`.

Disqualified assets reported separately with `reason` and `wouldHaveScored` for transparency.

## Source Code

See [references/source-code-v5.md](references/source-code-v5.md) for the v5 additions to the Python scanner (hourly trend classification, scoring changes, hard disqualifier logic).

## Cron Setup

Run every 10-30 minutes (time-aware scheduling optional):
```
python3 scripts/opportunity-scan-v5.py | python3 scripts/opportunity-report.sh
```

## Migration from v4

Drop-in replacement. All v5 features have sensible defaults:
- Hourly trend gate active by default (set `hourlyTrendGate: false` to disable)
- Counter-trend hourly penalty is -30 points (configurable)
- `hourlyTrend` and `trendAligned` added to output
- `disqualifiedAssets` shows what was filtered
- SM trader count 400+ tier added automatically
