---
name: sae-policy-guard
description: >
  Pre-trade risk assessment and policy enforcement for crypto trading using the
  Survivability-Aware Execution (SAE) framework. Use this skill before executing
  any crypto trade, when evaluating trader behavioral state (revenge trading,
  tilt, overconfidence, late-night impulsivity), when assessing market narrative
  risk, when computing position/leverage/frequency limits, when enforcing
  cool-down periods or staged execution, when auditing trading plugins or
  extensions for supply-chain risk, or when the user mentions risk management,
  survivability, blow-up prevention, liquidation avoidance, or trading discipline.
license: Apache-2.0
compatibility: >
  Requires Python 3.10+. Exchange-agnostic: accepts JSON input from any trading
  system. Optional internet access for live market or sentiment data.
---

# SAE Policy Guard

**Survivability-Aware Execution** is a trading execution gate: before an order is placed,
determine the maximum allowed risk budget and executable action set right now.

Core objective: minimize tail losses and liquidation probability — not maximize per-trade returns.
Three modules: **Trader-State Model**, **Market/Narrative Context**, **Policy Gate**.

## Quick Reference

| Task | Action | Script |
|---|---|---|
| Pre-trade risk check | Run full SAE pipeline | `trader_state.py` → `market_context.py` → `policy_gate.py` |
| Behavioral state only | Score trader patterns | `python scripts/trader_state.py --trades <file>` |
| Market context only | Assess environment | `python scripts/market_context.py --market <file>` |
| Compute constraints | Generate policy gate | `python scripts/policy_gate.py --trader-state <json> --market-context <json>` |
| Narrative firewall | Check narrative risk | `python scripts/market_context.py --market <file> --mode narrative` |
| Plugin/extension audit | Scan supply-chain risk | `python scripts/threat_audit.py --target <path>` |
| Replay evaluation | Backtest SAE decisions | `python scripts/replay_evaluate.py --trades <file>` |
| Full threat assessment | Run threat model | Follow threat assessment workflow below |

## Pre-Trade Assessment Workflow

Follow these 8 steps for every trade assessment. Do NOT skip steps.

### Step 1: Gather Trade Intent

Collect from the user:
- Asset (e.g., BTC-PERP, ETH/USDT)
- Direction: long or short
- Proposed size (USD or % of portfolio)
- Proposed leverage
- Order type (market, limit, stop)
- Rationale for the trade

If no explicit trade, assess current state for monitoring. If user cannot provide
trade history, use self-reported state with conservative defaults.

### Step 2: Score Trader Behavioral State

Run `scripts/trader_state.py` with the trader's recent trade history.

**Input format** — JSON array of trades:
```json
[
  {
    "timestamp": "2026-02-19T14:30:00Z",
    "asset": "BTC-PERP",
    "direction": "long",
    "size_usd": 5000,
    "leverage": 10,
    "pnl_usd": -450,
    "holding_minutes": 12,
    "was_stop_loss": false
  }
]
```

**Output** — JSON with scores (0.0–1.0) for six patterns:
- `revenge_trading`: loss → rapid re-entry with increased size
- `overconfidence`: win streak → size escalation
- `high_freq_switching`: excessive direction/asset changes
- `late_night_impulsivity`: trades outside normal hours
- `tilt_averaging`: adding to losing positions repeatedly
- `fomo_chasing`: entering after large price moves

Plus composite `risk_escalation_probability` (0.0–1.0).

If trade history is unavailable, ask the user about recent losses, current emotional
state, time of day, and how many trades they have made today. Apply conservative
defaults (risk_escalation_probability >= 0.5 when uncertain).

### Step 3: Assess Market/Narrative Context

Run `scripts/market_context.py` with current market data.

**Input format** — JSON:
```json
{
  "asset": "BTC-PERP",
  "candles_1h": [{"timestamp": "...", "open": 97000, "high": 97500, "low": 96800, "close": 97200, "volume": 1234567}],
  "funding_rate": 0.0003,
  "open_interest_usd": 15000000000,
  "orderbook_depth_bps_10": 5000000,
  "spread_bps": 1.2
}
```

Optional sentiment input:
```json
{
  "social_volume_24h": 45000,
  "social_volume_7d_avg": 12000,
  "sentiment_score": 0.82,
  "top_keywords": ["moon", "breakout", "ATH"]
}
```

**Output** — volatility_regime, liquidity_score, event_window, narrative_intensity,
error_amplification_score.

If market data is unavailable, ask the user to describe current conditions or
default to elevated caution (error_amplification_score = 0.5).

### Step 4: Compute Policy Gate Decision

Run `scripts/policy_gate.py` combining outputs from Steps 2 and 3, plus trade intent.

The script applies the **Policy Matrix** and outputs enforceable constraints:
- `gate_decision`: ALLOW / CONSTRAIN / COOL_DOWN / BLOCK
- `max_position_pct`: max position as % of portfolio
- `max_leverage`: max allowed leverage
- `max_trades_per_hour`: frequency budget
- `cool_down_minutes`: mandatory wait (0 if none)
- `staged_execution`: whether order must be split into tranches
- `stage_count`: number of tranches if staged
- `narrative_exclusion`: whether narrative firewall blocks this trade
- `policy_token_required`: whether forced confirmation is needed
- `violations`: list of specific constraint breaches
- `rationale`: human-readable explanation

### Step 5: Present Policy Gate to User

Format output using `assets/policy-report-template.md`. Clearly show:
- The gate decision with visual emphasis
- All enforced constraints in a table
- Any violations (proposed vs. allowed)
- The rationale explaining why

For each decision type:
- **ALLOW**: Confirm trade is within budget. Show any advisory notes.
- **CONSTRAIN**: Show adjusted parameters. Trade may proceed only with constrained values.
- **COOL_DOWN**: Show countdown and what conditions must change. No execution until period expires.
- **BLOCK**: Explain why and when the block expires. No execution permitted.

### Step 6: Handle Overrides (Policy Token)

If `policy_token_required` is true:
1. Present a structured confirmation listing all risk factors flagged
2. Require the user to explicitly acknowledge each risk factor
3. Record the override decision for behavioral tracking
4. An override does NOT remove constraints — it only allows proceeding within the constrained parameters

**CRITICAL**: A BLOCK decision cannot be overridden. Only CONSTRAIN and COOL_DOWN support policy tokens.

### Step 7: Post-Trade Recording

After execution or non-execution, log:
- `trade_id`, `sae_decision`, `constraints_applied`, `override_used`, `actual_outcome`

This data feeds back into Step 2 for future assessments. Recommend the user maintain
a local trade journal JSON file for continuous improvement.

### Step 8: Periodic Review

On request or at regular intervals, run `scripts/replay_evaluate.py` to assess SAE
effectiveness. Report: tail-risk reduction, false-block rate, lead time.
See `references/evaluation-protocol.md` for methodology.

## Policy Matrix

The policy gate maps (trader_risk_band × market_risk_band) to constraints:

| Trader Risk | Market Risk | Decision | Position Cap | Leverage Cap | Cool-Down | Staged | Narrative Block |
|---|---|---|---|---|---|---|---|
| Low (<0.3) | Low (<0.3) | ALLOW | 100% | 100% | 0 min | No | No |
| Low | Medium (0.3–0.6) | CONSTRAIN | 75% | 75% | 0 min | No | No |
| Low | High (>0.6) | CONSTRAIN | 50% | 50% | 0 min | 2 tranches | If narrative >0.8 |
| Medium (0.3–0.6) | Low | CONSTRAIN | 75% | 75% | 0 min | No | No |
| Medium | Medium | CONSTRAIN | 50% | 50% | 15 min | 2 tranches | If narrative >0.7 |
| Medium | High | COOL_DOWN | 25% | 25% | 30 min | 3 tranches | If narrative >0.6 |
| High (>0.6) | Low | CONSTRAIN | 50% | 50% | 15 min | 2 tranches | No |
| High | Medium | COOL_DOWN | 25% | 25% | 30 min | 3 tranches | If narrative >0.5 |
| High | High | BLOCK | 0% | 0% | 60 min | N/A | Yes |

All thresholds configurable via `assets/config-schema.yaml`.

## Narrative Firewall

The narrative firewall predicts whether current market narrative will trigger
loss-of-control behavior — NOT whether price will move.

Signals:
- Social volume anomaly (current vs. 7-day average)
- Keyword clustering around euphoria/panic themes
- Correlation with this trader's historical loss patterns
- Volatility regime during narrative spike

When `narrative_exclusion` triggers:
- Trade is blocked regardless of other factors
- User receives explanation of which narrative signals fired
- Exclusion expires when narrative intensity drops below threshold or after configurable timeout
- Check with `--mode narrative` for standalone narrative assessment

## Threat Assessment Workflow

For auditing trading system plugins, bots, or extensions:

1. Run `python scripts/threat_audit.py --target <plugin-path>`
2. The scanner checks three threat classes:
   - **Supply-chain / Plugin Risk**: obfuscated code, eval/exec, dynamic imports, unexpected network calls, credential access
   - **Prompt Injection / Manipulation**: unvalidated external data paths, template injection, adversarial content patterns
   - **Data Leakage / Identity Risk**: credential logging, strategy exposure, unencrypted key storage, sensitive data in logs
3. Format output using `assets/threat-assessment-template.md`
4. Present findings with severity ratings and recommendations
5. See `references/threat-model.md` for the full taxonomy

## Configuration

All thresholds are configurable. Copy `assets/config-schema.yaml`, modify values,
and pass with `--config <path>` to any script.

Key configurable parameters:
- Risk score thresholds per gate level
- Cool-down durations
- Position/leverage caps per gate level
- Narrative intensity thresholds
- Trader normal trading hours and timezone
- Behavioral pattern weights
- Event calendar entries

## Enforcement Rules

**These are not suggestions. They are constraints.**

1. When `gate_decision` is BLOCK: the agent MUST refuse to execute the trade. No exceptions. No overrides.
2. When `gate_decision` is COOL_DOWN: the agent MUST impose the actual time delay. No early release.
3. When `gate_decision` is CONSTRAIN: the agent MUST adjust trade parameters to fit constraints before execution.
4. When `policy_token_required` is true: the agent MUST obtain explicit user confirmation before proceeding.
5. All decisions and overrides MUST be logged for behavioral tracking.
6. The skill does not predict price direction or recommend trades. It only gates execution.
7. All behavioral data stays local. No trade history is transmitted externally.
