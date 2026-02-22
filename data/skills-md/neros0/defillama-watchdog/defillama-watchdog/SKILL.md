---
name: defillama-watchdog
description: DeFi protocol monitoring with alerts for TVL drops, capital rotation, hacks, bridge surges, unlocks, and revenue. Runs checks on demand or scheduled.
version: 1.0.0
author: defillama-watchdog
license: MIT
tags:
  - defi
  - defillama
  - tvl
  - alerts
  - monitoring
requires:
  - network
allowed-tools:
  - Bash(python3 scripts/watchdog.py)
  - Bash(python3 scripts/capital_flow.py)
  - Bash(python3 scripts/bridge_monitor.py)
  - Bash(python3 scripts/metrics_guard.py)
  - Bash(python3 scripts/true_growth.py)
  - Bash(python3 scripts/unlocks_monitor.py)
  - Bash(python3 scripts/revenue_guard.py)
  - Bash(python3 scripts/full_briefing.py)
---

# DeFiLlama Protocol Watchdog

Monitor DeFi protocols for TVL drops, capital rotation, security risks, and market opportunities.

## When to Use

- User wants to **monitor** or **track** specific protocols (e.g., "watch Aave", "alert me if Uniswap drops")
- User asks for a **security audit**, **risk check**, or **full briefing**
- User wants **rotation alerts** or **sentiment updates** (capital flow analysis)
- User wants to check **if protocols were hacked** (portfolio safety)

**Don't use** for one-off queries like "what is Aave's TVL?" — answer those directly.

## Available Commands

All commands run from the skill root. Add `--json` for structured output.

| Command                              | Purpose                            | Output Signals                               |
| ------------------------------------ | ---------------------------------- | -------------------------------------------- |
| `python3 scripts/watchdog.py`        | Check TVL drops                    | `ALERT:` or `HEARTBEAT_OK`                   |
| `python3 scripts/capital_flow.py`    | Capital rotation & sentiment       | `ROTATION:`, `SENTIMENT:`, or `HEARTBEAT_OK` |
| `python3 scripts/bridge_monitor.py`  | Bridge volume surges               | `BRIDGE_SURGE:` or `HEARTBEAT_OK`            |
| `python3 scripts/metrics_guard.py`   | Portfolio vs Recent Hacks          | `EMERGENCY:` or `HEARTBEAT_OK`               |
| `python3 scripts/true_growth.py`     | Smart money (TVL down, inflows up) | `BULLISH_DIVERGENCE:` or `HEARTBEAT_OK`      |
| `python3 scripts/unlocks_monitor.py` | Token unlock risks                 | `DUMP_RISK:` or `HEARTBEAT_OK`               |
| `python3 scripts/revenue_guard.py`   | Revenue/fee growth                 | `VALUE:` or `HEARTBEAT_OK`                   |
| `python3 scripts/full_briefing.py`   | Run all checks                     | All signals combined                         |

## How to Respond

### When User Requests a Check

1. **Run the appropriate script(s)**
2. **Parse the output signals**:
   - `HEARTBEAT_OK` = All clear
   - `ALERT:` = TVL dropped beyond threshold
   - `EMERGENCY:` = Portfolio protocol was hacked
   - `ROTATION:` = Capital moving between chains
   - `SENTIMENT:` = Risk-on/risk-off signal
   - `BRIDGE_SURGE:` = Bridge volume spike (hot chain)
   - `BULLISH_DIVERGENCE:` = TVL down but inflows up
   - `DUMP_RISK:` = Large unlock coming
   - `VALUE:` = Revenue growing faster than price
3. **Synthesize results** into 2-5 sentences explaining what happened and why it matters

### Response Pattern for Alerts

When you detect a risk signal:

1. **Lead with the key finding** (TVL drop, hack, rotation)
2. **Add context** from other signals:
   - If `ALERT:` → run `capital_flow.py` to check if it's rotation or protocol-specific
   - If portfolio exists → run `metrics_guard.py` to check hack risk
   - Optionally run other checks for depth (unlocks, inflows, revenue)
3. **Give a clear takeaway** (what should the user do?)

### Example Synthesis

**Bad:** "ALERT: AAVE V3 TVL dropped by 12.3%. ROTATION: Stablecoin supply on Ethereum shrank 1.5%."

**Good:** "Aave V3 TVL dropped 12.3% in the last period. This appears linked to broader capital rotation — stablecoin supply on Ethereum is down while Solana is growing. Not protocol-specific risk, but watch for continued outflows."

## Common User Requests

### "Alert me if [protocol] drops more than X%"

- Ensure `config.json` has correct `watch_list` (use DefiLlama slugs) and `threshold`
- Explain the watchdog runs on schedule and will alert when breached

### "Run a security audit" / "Full briefing" / "Risk check"

- Run `python3 scripts/full_briefing.py`
- Synthesize all output signals into one narrative

### "Any capital rotation?" / "Sentiment update?"

- Run `python3 scripts/capital_flow.py`
- Report `ROTATION:` and `SENTIMENT:` signals, or say "no significant moves"

### "Were any of my protocols hacked?"

- Run `python3 scripts/metrics_guard.py`
- Requires `assets/portfolio.json` (DefiLlama protocol IDs)
- Report `EMERGENCY:` immediately if found

### "Manual check now"

- Run `python3 scripts/watchdog.py`
- Report results or confirm "all within threshold"

## Configuration

**File:** `config.json` in skill root

Key settings:

- `watch_list`: Array of DefiLlama protocol slugs (e.g., `["aave-v3", "uniswap", "lido"]`)
- `threshold`: Decimal for alert threshold (e.g., `0.10` = 10% drop)
- `risk_level`: `"high"` (5%), `"standard"` (10%), `"low"` (15%)
- Feature toggles: `capital_flow.enabled`, `metrics_guard.enabled`, `bridge.enabled`, etc.

**Portfolio tracking:** Create `assets/portfolio.json` with DefiLlama protocol IDs for hack/unlock alerts.

**Pro features:** Some features (inflows, unlocks) need `DEFILLAMA_PRO_API_KEY` in environment. Most features work without any API key.

## Important Notes

- Protocol slugs must match DefiLlama exactly (check defillama.com/protocols)
- Scripts store state in `assets/` directory (TVL history, bridge data, etc.)
- All scripts exit 0 and print to stdout — parse the signal lines
- Latency: Alerts arrive after DefiLlama updates (~5-15 min) + next check cycle
- No API key required for: TVL, capital flow, hacks, bridge, revenue
- Pro API key needed for: inflows (true_growth), unlocks (unlocks_monitor)

## Output Style

- **Keep it concise:** 2-5 sentence summaries
- **Lead with action:** "Aave dropped 12%" not "The system detected..."
- **Provide context:** Explain if it's rotation, hack risk, or protocol-specific
- **Skip if quiet:** Don't report `HEARTBEAT_OK` unless user asked for status
- **Handle errors gracefully:** If script fails, tell user to run manually
