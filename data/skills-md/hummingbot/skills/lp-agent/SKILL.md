---
name: lp-agent
description: Manage concentrated liquidity (CLMM) positions on DEXs like Meteora and Raydium. Create, monitor, and rebalance LP positions automatically.
metadata:
  author: hummingbot
---

# lp-agent

This skill manages **concentrated liquidity (CLMM) positions** on decentralized exchanges like Meteora (Solana) and Raydium. It provides automated LP position management with rebalancing capabilities similar to the LP Manager controller.

## Prerequisites

Before using this skill, ensure hummingbot-api and MCP are running:

```bash
bash <(curl -s https://raw.githubusercontent.com/hummingbot/skills/main/skills/lp-agent/scripts/check_prerequisites.sh)
```

If not installed, use the `hummingbot-deploy` skill first.

## Quick Start

### 1. Find a Pool

Use the `manage_gateway_clmm` MCP tool:

```
# List popular pools on Meteora
manage_gateway_clmm(action="list_pools", connector="meteora")

# Search for specific pools
manage_gateway_clmm(action="list_pools", connector="meteora", search_term="SOL")

# Get detailed pool info
manage_gateway_clmm(action="get_pool_info", connector="meteora", network="solana-mainnet-beta", pool_address="<address>")
```

### 2. Create LP Position

```
# First, see the LP executor config schema
manage_executors(executor_type="lp_executor")

# Create position with quote only (buy base as price drops)
manage_executors(
    action="create",
    executor_config={
        "type": "lp_executor",
        "connector_name": "meteora/clmm",
        "pool_address": "<pool_address>",
        "trading_pair": "SOL-USDC",
        "base_token": "SOL",
        "quote_token": "USDC",
        "base_amount": 0,
        "quote_amount": 100,
        "lower_price": 180,
        "upper_price": 200,
        "side": 1
    }
)
```

**Side values:**
- `0` = Both-sided (base + quote)
- `1` = Buy (quote-only, range below current price)
- `2` = Sell (base-only, range above current price)

**IMPORTANT - Verify Position Creation:**

After creating an executor, you MUST verify the position was actually created on-chain. Follow these steps:

**Step 1: Get the executor ID from the creation response**
The `manage_executors(action="create")` call returns the executor_id. Use this ID for verification.

**Step 2: Poll executor state until it changes from OPENING**
```
manage_executors(action="get", executor_id="<executor_id>")
```

Check `custom_info.state`:
- `OPENING` → Transaction in progress, **wait 5-10 seconds and check again**
- `IN_RANGE` or `OUT_OF_RANGE` → Position created successfully ✓
- `FAILED` or `RETRIES_EXCEEDED` → Transaction failed ✗

**Step 3: Confirm position exists on-chain**
Even if state shows success, verify the position actually exists:
```
manage_gateway_clmm(
    action="get_positions",
    connector="meteora",
    network="solana-mainnet-beta",
    pool_address="<pool_address>"
)
```

The response should contain a position with matching `lower_price` and `upper_price`.

**If verification fails:**
1. Stop the failed executor: `manage_executors(action="stop", executor_id="<id>", keep_position=false)`
2. Check the error in `custom_info.error` if available
3. Common issues: range too wide (reduce width), insufficient balance, network congestion

**IMPORTANT - Range Width Limits (check BEFORE opening position):**

Meteora DLMM pools have bin limits. Each bin represents a small price increment based on `bin_step`:
- `bin_step=1` → Each bin is 0.01% apart
- `bin_step=10` → Each bin is 0.1% apart
- `bin_step=100` → Each bin is 1% apart

**Maximum bins per position is ~69 due to Solana account size limits.**

Calculate maximum range width:
```
max_width_pct = bin_step * 69 / 100
user_width_pct = (upper_price - lower_price) / lower_price * 100
```

**Before creating any position, the agent MUST:**
1. Get pool info: `manage_gateway_clmm(action="get_pool_info", connector="meteora", network="solana-mainnet-beta", pool_address="<address>")`
2. Extract `bin_step` from response
3. Calculate `max_width_pct = bin_step * 69 / 100`
4. If user's range exceeds max, **warn user and suggest narrower range**
5. Check wallet balance: user needs token amounts + **at least 0.06 SOL for position rent**
   - Use `get_portfolio_overview` to check balances
   - Warn if insufficient SOL or token balance

Examples:
- `bin_step=1`: max ~0.69% width
- `bin_step=10`: max ~6.9% width
- `bin_step=100`: max ~69% width

### 3. Set Default Preferences (Optional)

Save commonly-used settings to avoid repeating them. Ask user which values they want to default:

```
# View current preferences
manage_executors(action="get_preferences")

# Save connector/pair defaults when creating
manage_executors(
    action="create",
    executor_config={
        "type": "lp_executor",
        "connector_name": "meteora/clmm",
        "trading_pair": "SOL-USDC",
        ...
    },
    save_as_default=true
)
```

**What can be defaulted:**
- `connector_name` - e.g., `meteora/clmm` (must include `/clmm` suffix)
- `trading_pair` - e.g., `SOL-USDC`
- `extra_params.strategyType` - Meteora only: 0=Spot, 1=Curve, 2=Bid-Ask

**What should NOT be defaulted:**
- `side` - Determined by amounts at creation time
- `base_token`/`quote_token` - Inferred from trading_pair
- `lower_price`/`upper_price` - Market-dependent

Defaults stored at `~/.hummingbot_mcp/executor_preferences.md`.

### 4. Monitor Positions

```
# List all LP positions
manage_executors(action="search", executor_types=["lp_executor"])

# Get specific position details
manage_executors(action="get", executor_id="<executor_id>")

# Get positions summary
manage_executors(action="get_summary")
```

### 5. Manage Positions

```
# Collect fees (via Gateway CLMM)
manage_gateway_clmm(
    action="collect_fees",
    connector="meteora",
    network="solana-mainnet-beta",
    position_address="<position_nft_address>"
)

# Close position
manage_executors(action="stop", executor_id="<executor_id>", keep_position=false)
```

## Position Types

### Double-Sided (Both Tokens)

Provide liquidity with both base and quote tokens. Best when you expect price to stay within range.

```
     Lower          Current         Upper
       |---------------|---------------|
       |<-- Quote zone | Base zone -->|
```

- Price goes UP: You sell base, accumulate quote
- Price goes DOWN: You buy base with quote

### Single-Sided: Quote Only (side=1)

Position entire range BELOW current price. You're buying base as price drops.

```
     Lower          Upper    Current
       |---------------|--------|
       |<---- Buy zone ---->|
```

### Single-Sided: Base Only (side=2)

Position entire range ABOVE current price. You're selling base as price rises.

```
                   Current    Lower          Upper
                      |--------|---------------|
                               |<-- Sell zone -->|
```

## Rebalancing Strategy (Agent-Driven)

When price moves out of your position range, the agent handles rebalancing automatically.

### Step 1: Monitor Position State

```
manage_executors(action="get", executor_id="<id>")
```

Check `custom_info.state`:
- `IN_RANGE` → No action needed
- `OUT_OF_RANGE` → Wait for rebalance delay, then rebalance

**Rebalance delay:** Wait for position to be out of range for a set time (default: 60 seconds). Ask user to confirm delay before starting.

### Step 2: Determine Rebalance Direction

Compare `custom_info.current_price` with `custom_info.lower_price` and `custom_info.upper_price`:

**If current_price < lower_price (price dropped below range):**
- You're now holding mostly BASE tokens
- Strategy: Create BASE-ONLY position ABOVE current price
- This lets you sell base as price recovers

**If current_price > upper_price (price rose above range):**
- You're now holding mostly QUOTE tokens
- Strategy: Create QUOTE-ONLY position BELOW current price
- This lets you buy base if price drops

### Step 3: Close Old Position

```
manage_executors(action="stop", executor_id="<old_id>", keep_position=false)
```

This returns tokens to wallet. Use the returned amounts for the new position.

### Step 4: Create New Single-Sided Position

Use tokens received from close. For position width W% (ask user, check bin_step limits):

**Price below range → base-only position ABOVE current price (side=2):**
```
new_lower_price = current_price
new_upper_price = current_price * (1 + W/100)
base_amount = <amount received from close>
quote_amount = 0
side = 2
```

**Price above range → quote-only position BELOW current price (side=1):**
```
new_lower_price = current_price * (1 - W/100)
new_upper_price = current_price
base_amount = 0
quote_amount = <amount received from close>
side = 1
```

```
manage_executors(action="create", executor_config={
    "type": "lp_executor",
    "connector_name": "<same_connector>",
    "pool_address": "<same_pool>",
    "trading_pair": "<same_pair>",
    "base_amount": <base_amount>,
    "quote_amount": <quote_amount>,
    "lower_price": <new_lower_price>,
    "upper_price": <new_upper_price>,
    "side": <side>
})
```

### Step 5: Verify New Position

```
manage_executors(action="get", executor_id="<new_id>")
```

Confirm `custom_info.state` is `IN_RANGE` or `OUT_OF_RANGE` (not `OPENING` or `FAILED`).

## MCP Tools Reference

### manage_gateway_clmm

| Action | Parameters | Description |
|--------|------------|-------------|
| `list_pools` | connector, search_term, sort_key, limit | Browse available pools |
| `get_pool_info` | connector, network, pool_address | Get pool details |
| `get_positions` | connector, network, pool_address | Get positions in a pool |
| `open_position` | connector, network, pool_address, lower_price, upper_price, base_token_amount, quote_token_amount | Open position directly |
| `close_position` | connector, network, position_address | Close position |
| `collect_fees` | connector, network, position_address | Collect accumulated fees |

### manage_executors

| Action | Parameters | Description |
|--------|------------|-------------|
| (none) | executor_type="lp_executor" | Show config schema with your defaults |
| `create` | executor_config, save_as_default | Create LP executor (optionally save as default) |
| `search` | executor_types=["lp_executor"] | List LP executors |
| `get` | executor_id | Get executor details |
| `stop` | executor_id, keep_position | Stop executor |
| `get_summary` | - | Get overall summary |
| `get_preferences` | - | View preferences file |
| `save_preferences` | preferences_content | Save edited preferences |
| `reset_preferences` | - | Reset to default template |

## Scripts

| Script | Purpose |
|--------|---------|
| `check_prerequisites.sh` | Verify API, Gateway, wallet setup |

## LP Executor Config Schema

```json
{
    "type": "lp_executor",
    "connector_name": "meteora/clmm",
    "pool_address": "2sfXxxxx...",
    "trading_pair": "SOL-USDC",
    "base_token": "SOL",
    "quote_token": "USDC",
    "base_amount": 0,
    "quote_amount": 100,
    "lower_price": 70,
    "upper_price": 90,
    "side": 1,
    "extra_params": {
        "strategyType": 0
    }
}
```

**Fields:**
- `connector_name`: CLMM connector - append `/clmm` to connector name (e.g., `meteora/clmm`)
- `pool_address`: Pool contract address
- `trading_pair`: Format "BASE-QUOTE"
- `base_amount` / `quote_amount`: Token amounts (set one to 0 for single-sided)
- `lower_price` / `upper_price`: Position price bounds
- `side`: 0=both, 1=buy (quote-only), 2=sell (base-only)
- `extra_params`: Connector-specific (Meteora strategyType: 0=Spot, 1=Curve, 2=Bid-Ask)

**Supported Connectors:**
- `meteora/clmm` - Tested and fully supported
- Other Gateway CLMM connectors - Should work but not yet tested

To list available CLMM connectors:
```
manage_gateway_config(resource_type="connectors", action="list")
```
Append `/clmm` to any CLMM connector name when creating executors.

## Example: Full LP Management Flow

```
# 1. Check prerequisites
bash <(curl -s https://raw.githubusercontent.com/hummingbot/skills/main/skills/lp-agent/scripts/check_prerequisites.sh)

# 2. Find a pool
manage_gateway_clmm(action="list_pools", connector="meteora", search_term="SOL", sort_key="volume")

# 3. Get pool details (note the bin_step for range calculation)
manage_gateway_clmm(action="get_pool_info", connector="meteora", network="solana-mainnet-beta", pool_address="2sfXxxxx")
# Example response shows: bin_step=10, current_price=190
# Max range width = 10 * 69 / 100 = 6.9%
# Use conservative 5% width: lower=185.5, upper=194.5

# 4. Create position
manage_executors(action="create", executor_config={
    "type": "lp_executor",
    "connector_name": "meteora/clmm",
    "pool_address": "2sfXxxxx",
    "trading_pair": "SOL-USDC",
    "base_token": "SOL",
    "quote_token": "USDC",
    "base_amount": 0,
    "quote_amount": 100,
    "lower_price": 185.5,
    "upper_price": 194.5,
    "side": 1
})

# 5. VERIFY position was created (critical step!)
manage_executors(action="get", executor_id="<id>")
# Check custom_info.state:
# - "OPENING" → wait and check again
# - "IN_RANGE" or "OUT_OF_RANGE" → success!
# - "FAILED" → check error, possibly reduce range width

# 6. Monitor position
manage_executors(action="get", executor_id="<id>")

# 7. If out of range for 60+ seconds, rebalance (see Rebalancing Strategy)
# - Close: manage_executors(action="stop", executor_id="<id>", keep_position=false)
# - Reopen with tokens received as single-sided position

# 8. When done, close
manage_executors(action="stop", executor_id="<id>", keep_position=false)
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| "Prerequisites not met" | API or MCP not running | Run `hummingbot-deploy` skill |
| "Pool not found" | Invalid pool address | Use list_pools to find valid pools |
| "Insufficient balance" | Not enough tokens | Check wallet balance, reduce amounts |
| "Position not in range" | Price outside bounds | Wait or rebalance |
| "InvalidRealloc" | Position range spans too many bins | Reduce range width (see bin_step limits above) |
| State stuck at "OPENING" | Transaction failed silently | Stop executor and retry with narrower range |

