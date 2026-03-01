---
name: wolf-howl
description: >-
  HOWL v2 — Hunt, Optimize, Win, Learn. Nightly self-improvement loop for the
  WOLF autonomous trading strategy. Runs once per day (via cron) to review
  all trades from the last 24 hours, compute win rates, analyze signal quality
  correlation, evaluate DSL tier performance, identify missed opportunities,
  and produce concrete improvement suggestions for the wolf-strategy skill.
  v2 adds fee drag ratio (FDR) analysis, holding period bucketing, LONG vs
  SHORT regime detection, rotation cost tracking, cumulative drift detection,
  and gross vs net profit factor separation.
  Use when setting up daily trade review automation, analyzing trading
  performance, or improving an autonomous trading strategy through
  data-driven feedback loops.
  Requires Senpi MCP connection, mcporter CLI, and OpenClaw cron system.
---

# HOWL v2 — Hunt, Optimize, Win, Learn

The WOLF hunts all day. At night, it HOWLs — reviewing every kill and miss, sharpening its instincts, and waking up sharper tomorrow.

Automated daily retrospective with data-driven self-improvement suggestions for the WOLF strategy.

---

## Setup

Run the setup script to configure the nightly HOWL:

```bash
python3 scripts/howl-setup.py --wallet {WALLET} --chat-id {CHAT_ID}
```

The agent already knows wallet and chat ID — it just needs to create the cron. Optionally set run time (default: 23:55 local) and timezone.

---

## How It Works

The cron fires daily and spawns an isolated sub-agent that:

### 1. Gathers Data
- Reads `memory/YYYY-MM-DD.md` (today + yesterday)
- Reads `MEMORY.md` for cumulative context
- Reads all `dsl-state-WOLF-*.json` files (active = current positions, inactive = closed trades)
- Reads `wolf-strategy.json` for current config
- Reads `wolf-trade-counter.json` for FDR data (v5.1+)
- Queries Senpi trade history via mcporter
- Reads scanner script for current filter thresholds

### 2. Analyzes Each Closed Trade
For every trade: asset, direction, entry/exit price, PnL (gross and net), ROE, fees paid, duration, max ROE (high water), DSL tier reached, entry signal type and quality (reason count, rank jump, contrib velocity, trader count), SM conviction at entry vs exit, close trigger (DSL breach/Phase 1 auto-cut/stagnation/conviction collapse/rotation/manual).

### 3. Computes Metrics

**Core:**
- Win rate, avg winner vs avg loser PnL, profit factor (gross AND net)
- Total fees paid, fee drag ratio (fees / account value)
- Net PnL vs gross PnL — if gross is positive but net is negative, fees are the problem

**Signal Quality:**
- Signal quality correlation (do higher reason counts → better outcomes?)
- FIRST_JUMP vs IMMEDIATE_MOVER vs DEEP_CLIMBER win rates
- Entry rank vs outcome — are entries from rank #20-30 better than #10-20?

**DSL Performance:**
- Tier distribution (how many reached Tier 1/2/3/4 vs Phase 1 closes?)
- Phase 1 auto-cut count and savings (what would they have lost without the cut?)

**Holding Period Buckets (v2 — critical):**
- < 30 min: count, win rate, PnL, fees (expect: poor — rotations and panic cuts)
- 30-90 min: count, win rate, PnL, fees (expect: sweet spot)
- 90+ min: count, win rate, PnL, fees (expect: dead weight)

**Direction Analysis (v2):**
- LONG win rate, PnL, profit factor
- SHORT win rate, PnL, profit factor
- Flag if one direction is dramatically worse (regime mismatch)

**Other:**
- Slot utilization (% time filled vs empty)
- Dead weight duration (how long losers sat before cut)
- Missed opportunities (top movers we didn't trade)
- Rotation count and net cost (fees paid for rotation trades)

### 4. Identifies Patterns

- Entry patterns distinguishing winners from losers
- DSL effectiveness (too tight? too loose?)
- Stagnation thresholds (cutting dead weight fast enough?)
- Scanner filter accuracy (catching right signals?)
- Position sizing optimization
- Timing patterns
- **Fee drag pattern** (v2): Is the agent overtrading? How many trades before FDR hits 10%?
- **Holding period pattern** (v2): Are short-hold trades systematically worse?
- **Direction bias** (v2): Is the agent fighting the trend? LONGs in a selloff = disaster.
- **Monster trades** (v2): Did a few big winners save the day? How many trades produced 80% of PnL?

### 5. Produces Report
Saves full report to `memory/howl-YYYY-MM-DD.md` with:
- Summary stats (trades, win rate, gross PnL, net PnL, fees, FDR, profit factor gross/net)
- Trade log table
- Holding period buckets breakdown
- Direction breakdown (LONG vs SHORT)
- What worked / what didn't (data-backed)
- Pattern insights
- Recommended improvements (high/medium/low confidence)
- Config change suggestions

### 6. Updates Memory & Delivers
- Appends distilled summary to `MEMORY.md`
- Sends concise Telegram summary to user
- **Drift check** (v2): If 3+ consecutive HOWLs suggest the same change, escalate urgency in the report

---

## Report Format

See `references/report-template.md` for the exact output format.

---

## v2 Analysis Additions

These were discovered by running HOWL v1 on live WOLF v5 trading data and finding blind spots:

### Fee Drag Ratio Analysis
The single biggest insight from the first HOWL: **fees ate an entire profitable day.** 32 trades × $32 avg = $1,034 in fees (18.3% of account). Gross PnL was +$888, but net was -$146. HOWL must compute and prominently display FDR alongside PnL. If gross PF > 1.0 but net PF < 1.0, the recommendation is fewer, higher-quality trades — not better entries.

### Holding Period Buckets
Trades bucketed by hold time revealed that < 30 min trades were systematically terrible (-$705 combined) while 60-90 min trades were the sweet spot (+$704, 57% WR). HOWL must bucket every trade and flag if < 30 min trades are negative contributors.

### Direction Regime Detection
4W/12L on LONGs (25% WR, PF 0.05) vs profitable SHORTs. HOWL must split metrics by direction and flag when one side is dramatically underperforming — this indicates a regime mismatch (trading LONGs in a selloff).

### Monster Trade Dependency
3 Tier 4 trades produced +$1,443 while everything else combined was -$556. HOWL must identify what % of PnL came from top N trades and whether the strategy would survive without them.

### Rotation Cost Tracking
Each rotation costs ~$65 (close fee + open fee). HOWL must track rotation count, total rotation cost, and whether rotations produced net positive outcomes.

---

## Rules
- Every recommendation must be backed by data from the last 24h
- Don't change things that are working — if win rate is high, don't fix what isn't broken
- Small incremental improvements > big overhauls
- If < 3 trades in 24h, still analyze "why so few?" — don't just skip. Was the FDR gate locked? Was the market dead? Were signals filtered too aggressively?
- Compare today vs cumulative stats to spot trends
- Be brutally honest — no sugarcoating losses
- **Always separate gross vs net.** A "profitable" strategy that loses money after fees is not profitable.
- **Flag regime mismatches early.** If LONGs are 0-for-5, say "stop taking LONGs" — don't wait for 0-for-12.

---

## Customization

Edit `references/analysis-prompt.md` to adjust what the sub-agent analyzes. The prompt is read by the sub-agent at runtime, so changes take effect on the next HOWL without restarting crons.

---

## Files

| File | Purpose |
|------|---------|
| `scripts/howl-setup.py` | Setup wizard — creates the nightly HOWL cron |
| `references/analysis-prompt.md` | Full sub-agent analysis prompt (editable) |
| `references/report-template.md` | Output report format |
