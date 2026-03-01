---
name: senpi-getting-started-guide
description: >
  Guides users through their first trade on Senpi/Hyperliquid. Walks through
  discovery (top traders), creating a mirror strategy with a chosen trader,
  monitoring, and closing the strategy. Use when user says "let's trade",
  "first trade", "teach me to trade", "how do I trade", or when state is
  AWAITING_FIRST_TRADE. Can also run when state is not READY (e.g. after
  entrypoint Step 3); then prompts for wallet funding before starting when
  needed. Requires Senpi MCP to be connected.
compatibility: OpenClaw, Hyperclaw, Claude Code
metadata:
  author: Senpi
  version: 1.0.0
  homepage: https://agents.senpi.ai
---

# Getting Started: Your First Trade

Guide users through their first complete trade on Hyperliquid via Senpi. This skill teaches the core loop: **discover top traders** → **create a strategy** that mirrors a chosen trader → **monitor** → **close strategy**.

**Prerequisites (agent-only):** Senpi MCP connected. Onboarding complete (see state check below). Wallet funded for creating a strategy; if not yet funded, show a funding reminder and do not start until balance ≥ $100 or user confirms they funded.

**User-facing rule:** Never show the user internal details. Do **not** mention state names (e.g. UNFUNDED, READY, FRESH), file paths (e.g. state.json, ~/.config/senpi), step codes (e.g. STRATEGY_CREATED), or MCP/tool names. Use only plain, friendly language (e.g. "You're all set to start", "Fund your wallet to begin", "Your strategy is running").

**Minimum strategy budget:** Use **$100** as the minimum when creating the first-trade mirror strategy. Do not suggest or use $50 or any amount below $100.

---

## Prerequisites

Before starting the tutorial, verify:

1. **MCP Connected** — Senpi MCP server is configured and accessible.
2. **Onboarding complete** — If not complete (state FRESH or ONBOARDING), redirect with a user-friendly message only (see below). Do not mention "state" or "onboarding" to the user.
3. **Wallet funded (for creating a strategy)** — If not yet funded, show a single friendly funding reminder; do not start the tutorial until balance ≥ $100 or user confirms they funded.

Ensure state file exists; if missing, create it and redirect. **When redirecting, tell the user only:** "You need to complete setup first. Say **'set up Senpi'** or **'connect to Senpi'** to get started." Do not mention state file, FRESH, or any internal state.

```bash
# Ensure state file exists (per state lifecycle); if missing, create and redirect
if [ ! -f ~/.config/senpi/state.json ]; then
  mkdir -p ~/.config/senpi
  cat > ~/.config/senpi/state.json << 'STATEEOF'
{
  "version": "1.0.0",
  "state": "FRESH",
  "error": null,
  "onboarding": {
    "step": "IDENTITY",
    "startedAt": null,
    "completedAt": null,
    "identityType": null,
    "subject": null,
    "walletGenerated": false,
    "existingAccount": false
  },
  "account": {},
  "wallet": { "funded": false },
  "firstTrade": { "completed": false, "skipped": false },
  "mcp": { "configured": false }
}
STATEEOF
  # Tell user only (do not echo internal messages):
  # "You need to complete setup first. Say 'set up Senpi' or 'connect to Senpi' to get started."
  exit 1
fi

STATE=$(cat ~/.config/senpi/state.json | node -p "JSON.parse(require('fs').readFileSync(0,'utf8')).state")
if [ "$STATE" = "FRESH" ] || [ "$STATE" = "ONBOARDING" ]; then
  # Tell user only (do not echo "User needs to complete onboarding" or state names):
  # "You need to complete setup first. Say 'set up Senpi' or 'connect to Senpi' to get started."
  exit 1
fi
```

---

## Triggers

Start this tutorial when:

- User says: "let's trade", "first trade", "teach me to trade", "how do I trade", "make a trade"
- State is `AWAITING_FIRST_TRADE` and user sends a trading-related message
- User explicitly asks for trading guidance

**Do NOT start if:** MCP not connected — then tell the user to set up Senpi first (do not mention MCP or state). If user says "skip tutorial", set state to READY and show the skip message from [references/next-steps.md](references/next-steps.md). If wallet has less than $100 when starting, do not create a strategy until funded; use the funding reminder below (user-friendly wording only).

---

## Tutorial Flow

Follow steps in order. Reference files contain display copy, state schemas, and error handling.

### When the wallet isn’t funded yet (before Step 1)

If the user asked for the first-trade guide (e.g. "let's trade") but the wallet is not yet funded:

1. **Check balance** — Use MCP to fetch portfolio/balance.
2. **If balance < $100:** Do **not** start the introduction. Show **one clear, user-friendly message** only:
   - Your **trading wallet address** (from state; do not say "agent wallet" or "state.json").
   - That they need to send at least **$100 USDC** on a supported network (Base, Arbitrum, Optimism, Polygon, or Ethereum).
   - "Once you’ve sent the funds, say **'I funded my wallet'** or **'let’s trade'** and we’ll start the tutorial."
3. **If balance ≥ $100:** Update state (AWAITING_FIRST_TRADE, wallet.funded true), then proceed to Step 1.

If onboarding is not complete (state FRESH or ONBOARDING), tell the user only: "Complete setup first — say **'set up Senpi'** to get started." Do not say "onboarding", "state", or "User needs to complete onboarding first."

### Step 1: Introduction

Display the trade cycle. **When showing the 4-step list to the user, use this exact wording:**

> 1️⃣ **Discover** — Find top-performing traders on Hyperliquid  
> 2️⃣ **Create a strategy** — Mirror a chosen trader's positions ($100 budget)  
> 3️⃣ **Monitor** — Watch how the strategy performs  
> 4️⃣ **Close** — Exit when you're ready  

Recommend a **$100 minimum** budget for the first strategy and include a short risk disclaimer. Ask user to say **"yes"** to continue or **"skip"** if experienced.

Update state: set `firstTrade.step` to `INTRODUCTION`, `firstTrade.started` true, `startedAt` (ISO 8601). Preserve existing fields in `state.json`.

Wait for user confirmation before proceeding.

---

### Step 2: Discovery

Use MCP **`discovery_get_top_traders`** to fetch top traders. Optionally use **`discovery_get_trader_state`** or **`discovery_get_trader_history`** for extra detail. Show a short table of top traders (e.g. by PnL, win rate) and **recommend one trader** to mirror for the first trade.

See [references/discovery-guide.md](references/discovery-guide.md) for display template and state update (`firstTrade.step: "DISCOVERY"`, `recommendedTraderId`, `recommendedTraderName`).

---

### Step 3: Strategy Sizing

Before creating the strategy, explain: chosen trader, budget (**$100 minimum**), and that the strategy will mirror that trader's positions. Warn about risk and liquidation. Ask user to say **"confirm"** to create the strategy.

See [references/strategy-management.md](references/strategy-management.md) for the sizing table and wording.

---

### Step 4: Create Strategy

On user confirmation, call MCP **`strategy_create`** with the chosen trader (from Step 2) and budget (**minimum $100**). On success, **show the celebration** (see [references/next-steps.md](references/next-steps.md) — "Celebrate (After First Strategy Created)"): congratulate the user for opening their first strategy, then offer "how's my strategy?", "close my strategy", or "show my positions". Do not show strategy status or raw IDs.

Update state per [references/strategy-management.md](references/strategy-management.md): set `firstTrade.step: "STRATEGY_CREATED"`, `tradeDetails` (strategyId, mirroredTraderId, etc.), **and** set `firstTrade.completed: true`, `firstTrade.step: "COMPLETE"`, `firstTrade.completedAt`. On failure, see [references/error-handling.md](references/error-handling.md).

---

### Step 5: Monitor Strategy

When user asks "how's my strategy?" or similar, fetch data via MCP: **`strategy_get`**, **`strategy_get_clearinghouse_state`**, or **`execution_get_open_position_details`** for open positions. Show strategy value, open positions (if any), unrealized PnL, ROE. Offer: Hold, Close strategy, or Add protection. Do **not** show a separate congratulations here — that was already shown when they created their first strategy (Step 4).

---

### Step 6: Close Strategy

When user says "close", "exit", "close my strategy", "take profit", etc., call MCP **`strategy_close`** with the strategy ID from state. Tell the user the strategy is closed and show **realized PnL, duration, and fees** in plain language. Show the "After Close" result and next steps from [references/next-steps.md](references/next-steps.md) (no separate congratulations — already shown when they created the strategy). Do not mention strategy status or internal codes. Update state (STRATEGY_CLOSE, tradeDetails with closedAt, pnl, etc.). See [references/strategy-management.md](references/strategy-management.md).

---

### Step 7: After Close — Result & Next Steps

When the user has closed their strategy (Step 6), the result and next steps are shown there. No separate celebration step — state was already set to `READY` and `firstTrade.completed` when they created their first strategy (Step 4). Full "After Close" copy: [references/next-steps.md](references/next-steps.md). State shape: [references/strategy-management.md](references/strategy-management.md).

---

## Interrupted Tutorial / Resume

If the user returns mid-tutorial, read firstTrade.step from state and resume from the matching step. See [references/next-steps.md](references/next-steps.md) for resume logic. **Resume message must be user-friendly only** — e.g. "You were in the middle of your first trade. Here’s where we left off…" Do not mention step names (INTRODUCTION, DISCOVERY, STRATEGY_CREATED, etc.) or state.

---

## Reference Files

- **[references/error-handling.md](references/error-handling.md)** — Insufficient balance, strategy_create failed, strategy_close failed, recovery
- **[references/discovery-guide.md](references/discovery-guide.md)** — discovery_get_top_traders, recommend a trader to mirror, display template
- **[references/strategy-management.md](references/strategy-management.md)** — Strategy sizing, strategy_create/strategy_close flow, state updates for firstTrade
- **[references/next-steps.md](references/next-steps.md)** — Celebration (after first strategy created), after close, skip tutorial, resume handling

---

## Installation

```bash
npx skills add Senpi-ai/senpi-skills/senpi-getting-started-guide
```

Or manually:

```bash
mkdir -p ~/.senpi/skills/senpi-getting-started-guide
curl -sL "https://raw.githubusercontent.com/Senpi-ai/senpi-skills/main/senpi-getting-started-guide/SKILL.md" \
  -o ~/.senpi/skills/senpi-getting-started-guide/SKILL.md
# Copy references/ into the same skill directory
```
