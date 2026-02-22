---
name: solana-trader
description: Autonomous Solana token trading. Use when setting up a wallet, checking balances, scanning for opportunities, executing swaps, or running a trading monitor on Solana.
---

# Solana Trader Skill

This skill provides autonomous trading capabilities on the Solana blockchain using Jupiter for swaps and multiple data sources for opportunity scanning.

## Quick Start

### 1. Create & Fund Wallet
```
Use the solana_wallet tool with action="create" to generate a new wallet.
Fund it with SOL at the provided address (minimum 0.1 SOL recommended).
```

### 2. Check Balance
```
Use solana_wallet with action="balance" to see SOL and token holdings.
```

### 3. Start Trading
```
Use solana_scan to find opportunities, then solana_swap to execute trades.
```

## Available Tools

### `solana_wallet`
**Parameters:** `action` (create | balance | address)

- **create**: Generates a new Solana keypair and saves it
- **balance**: Returns SOL balance and all token holdings  
- **address**: Returns the wallet's public key

**Example:**
```json
{
  "action": "balance"
}
```

### `solana_swap`
**Parameters:** `inputToken`, `outputToken`, `amountUsd`

Executes a token swap via Jupiter aggregator.

**Supported tokens:** SOL, USDC, USDT, RAY, SRM, or any valid mint address

**Example:**
```json
{
  "inputToken": "USDC",
  "outputToken": "SOL", 
  "amountUsd": 10
}
```

### `solana_scan`
**Parameters:** `chain` (optional), `maxResults` (optional, default 5)

Scans multiple sources for trading opportunities:
- DexScreener boosted tokens (paid promotion = attention)
- GeckoTerminal trending pools (momentum)
- GeckoTerminal new pools (early discovery)

Returns scored opportunities with momentum, liquidity, and volume metrics.

**Example:**
```json
{
  "chain": "solana",
  "maxResults": 10
}
```

## Automated Trading

### Running the Monitor
The trading monitor (`scripts/monitor.js`) can run autonomously via cron:

```bash
# Every 15 minutes during market hours
*/15 6-23 * * * cd ~/.openclaw/workspace && node skills/solana-trader/scripts/monitor.js
```

### Configuration (Environment Variables)
```bash
export SOLANA_RPC_URL="https://api.mainnet-beta.solana.com"
export SOLANA_WALLET_PATH="~/.openclaw/workspace/solana-wallet.json"
export POSITION_SIZE_USD=10          # Max $ per trade
export MAX_POSITIONS=4               # Max concurrent positions
export MIN_SCORE=25                  # Minimum opportunity score
export TAKE_PROFIT_PCT=50            # Take profit at 50% gain
export STOP_LOSS_PCT=-25             # Stop loss at -25%
export TRAILING_STOP_PCT=15          # Trailing stop from peak
```

## Trading Strategy

### Entry Criteria
The system scores opportunities based on:

1. **Early Stage Bonus** (30 pts max)
   - Micro cap FDV < $500k: +30 pts
   - Small cap FDV < $2M: +20 pts
   - Mid cap FDV < $10M: +10 pts

2. **Momentum** (45 pts max)
   - Steady 5m rise (0-15%): +3 pts per %
   - Hourly momentum (0-30%): +2 pts per %
   - Acceleration bonus: +15 pts

3. **Volume/Liquidity Ratio** (35 pts max)
   - High ratio (>2): +20 pts
   - Very high ratio (>5): +15 pts additional

4. **Buy Pressure** (25 pts max)
   - Buy/sell ratio >1.3: +15 pts
   - Buy/sell ratio >2.0: +10 pts additional

### Entry Penalties
- Already pumped (5m >30%): -25 pts
- Dumping (1h <-15%): -20 pts
- Dead token (24h <-40%): -20 pts
- Low liquidity (<$15k): -10 pts
- Sell pressure (buy/sell <0.5): -15 pts

### Exit Logic
1. **Take Profit**: +50% gain
2. **Trailing Stop**: If up >30%, exit if drops 15% from peak
3. **Stop Loss**: -25% loss
4. **Momentum Death**: 5m <-8% AND 1h <-15%

### Risk Management
- Maximum 4 concurrent positions
- $3-10 position sizes (25% of available USDC)
- Always keep $5+ liquid for gas/exits
- Never risk more than you can afford to lose

## Data Sources

### DexScreener
- Boosted tokens (paid promotion = attention)
- Rich metadata (price, volume, liquidity, txns)
- Rate limit: ~5 calls/second

### GeckoTerminal  
- Trending pools (momentum plays)
- New pools (early opportunities)
- Rate limit: ~2 calls/second

### Jupiter
- Best execution routing
- Ultra-light API for fast swaps
- Handles slippage automatically

## Files & State

### State Management
- `trades.json` - Trade history log
- `state.json` - Portfolio state, positions, balances
- `solana-wallet.json` - Encrypted wallet keypair

### Monitoring
- `monitor.js` - Main trading loop
- `scan.js` - Standalone opportunity scanner
- Strategy stats tracking (win/loss ratios, PnL by strategy)

## Safety Notes

- Start small ($5-20 positions) to test the system
- Monitor for 24-48h before increasing size
- Never commit more than you can afford to lose
- Keep some SOL for transaction fees
- Regularly backup your wallet file

The Solana trading ecosystem is fast-moving and high-risk. This system is designed for momentum plays on trending tokens, not long-term holding.

## Advanced Features

### SOL Swing Trading
- Auto-buy SOL on >-7% daily drops
- Auto-sell SOL on >+6% daily pumps
- Maintains 0.2+ SOL base position

### Portfolio Balancing
- Automatically rebalances between SOL and USDC
- Maintains minimum liquidity for new opportunities
- Tracks total portfolio value vs starting point

Use responsibly and understand that token trading involves significant risk of loss.