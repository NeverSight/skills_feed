---
name: test-trading-strategies
description: "Backtest trading strategies on historical data and interpret performance metrics. Provides run_backtest (crypto strategies) and run_prediction_market_backtest (Polymarket strategies). Fast execution (20-60s), minimal cost ($0.001). Returns Sharpe ratio, max drawdown, win rate, profit factor, and trade statistics. Use this skill after building or improving strategies to validate performance before deploying. NEVER deploy without thorough backtesting (6+ months recommended)."
persona: ["developer", "trader"]
risk_level: "none"
cost_profile: "$0.001 per backtest"
tools:
  - mcp__workbench__run_backtest
  - mcp__workbench__run_prediction_market_backtest
  - mcp__workbench__get_latest_backtest_results
related_skills:
  prerequisites:
    - browse-robonet-data
    - build-trading-strategies
  next_steps:
    - improve-trading-strategies
    - deploy-live-trading
---

# Test Trading Strategies

## Quick Start

This skill validates strategy performance on historical data before risking real capital. Testing is fast (20-60s), cheap ($0.001), and essential for safe trading.

**Load the tools first**:
```
Use MCPSearch to select: mcp__workbench__run_backtest
Use MCPSearch to select: mcp__workbench__get_latest_backtest_results
```

**Basic backtest**:
```
run_backtest(
    strategy_name="MyStrategy",
    start_date="2024-01-01",
    end_date="2024-12-31",
    symbol="BTC-USDT",
    timeframe="1h"
)
```

Returns performance metrics in 20-40 seconds:
- Sharpe ratio: 1.4 (good risk-adjusted return)
- Max drawdown: 12% (moderate risk)
- Win rate: 52% (realistic)
- Profit factor: 1.8 (profitable)

**When to use this skill**:
- After building new strategy (validate it works)
- After improving strategy (confirm improvement)
- Before deploying to live trading (ALWAYS)
- Comparing multiple strategy versions
- Testing parameter variations

**Critical rule**: NEVER deploy without backtesting 6+ months of data

## Available Tools (3)

### run_backtest

**Purpose**: Test crypto trading strategy performance on historical data

**Parameters**:
- `strategy_name` (required): Strategy to test
- `start_date` (required): Start date (YYYY-MM-DD)
- `end_date` (required): End date (YYYY-MM-DD)
- `symbol` (required): Trading pair (e.g., "BTC-USDT")
- `timeframe` (required): Timeframe (1m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d)
- `config` (optional): Backtest configuration object:
  - `fee`: Trading fee per side (default: 0.0005 = 0.05%)
  - `slippage`: Slippage per trade (default: 0.0005 = 0.05%)
  - `leverage`: Position multiplier (default: 1, max: 5)

**Returns**: Performance metrics:
- **Net profit**: Total profit/loss in USDC
- **Total return**: Percentage return
- **Annual return**: Annualized return percentage
- **Sharpe ratio**: Risk-adjusted return (industry standard metric)
- **Max drawdown**: Largest peak-to-trough decline
- **Win rate**: Percentage of profitable trades
- **Profit factor**: Gross profit / gross loss
- **Trade statistics**: Total trades, average trade duration, consecutive losses
- **Equity curve**: Balance over time (for visualization)

**Pricing**: $0.001 (essentially free)

**Execution Time**: ~20-40 seconds

**Use when**: Testing crypto perpetual strategies on Hyperliquid

### run_prediction_market_backtest

**Purpose**: Test Polymarket prediction market strategy on historical data

**Parameters**:
- `strategy_name` (required): PolymarketStrategy to test
- `start_date` (required): Start date (YYYY-MM-DD)
- `end_date` (required): End date (YYYY-MM-DD)
- `condition_id` (for single market): Specific Polymarket condition ID
- `asset` (for rolling markets): Asset symbol ("BTC", "ETH")
- `interval` (for rolling markets): Market interval ("15m", "1h")
- `initial_balance` (optional): Starting USDC (default: 10000)
- `timeframe` (optional): Execution timeframe (default: 1m)

**Returns**: Backtest metrics:
- Profit/loss
- Win rate
- Position history for YES/NO tokens
- Market resolution outcomes

**Pricing**: $0.001

**Execution Time**: ~20-60 seconds

**Use when**: Testing Polymarket prediction market strategies

### get_latest_backtest_results

**Purpose**: View recent backtest results without re-running

**Parameters**:
- `strategy_name` (optional): Filter by strategy name
- `limit` (optional, 1-100): Number of results (default: 10)
- `include_equity_curve` (optional): Include equity curve data
- `equity_curve_max_points` (optional, 50-1000): Curve resolution

**Returns**: List of recent backtest records with metrics

**Pricing**: Free

**Use when**: Checking if backtest already exists, comparing strategies, avoiding redundant backtests

## Core Concepts

### Performance Metrics Interpretation

**Sharpe Ratio** (risk-adjusted return):
```
Formula: (Mean Return - Risk-Free Rate) / Standard Deviation of Returns

Interpretation:
>2.0  → Excellent (very rare for algo strategies)
1.0-2.0 → Good (achievable with solid strategy)
0.5-1.0 → Acceptable (worth testing further)
<0.5  → Poor (likely not profitable after costs)

Why it matters:
- Accounts for volatility (high return with high volatility = lower Sharpe)
- Industry standard for comparing strategies
- More useful than total return alone
```

**Max Drawdown** (largest peak-to-trough decline):
```
Example: Strategy grows from $10k → $15k → $12k
Drawdown: ($15k - $12k) / $15k = 20%

Interpretation:
<10%  → Conservative (lower returns, safer)
10-20% → Moderate (balanced risk/reward)
20-40% → Aggressive (higher returns, higher risk)
>40%  → Very risky (difficult to recover from)

Why it matters:
- Measures worst-case scenario
- Predicts emotional difficulty of holding strategy
- 50% drawdown requires 100% return to recover
```

**Win Rate** (percentage of profitable trades):
```
Formula: (Winning Trades / Total Trades) × 100%

Interpretation:
45-65% → Realistic for most strategies
>70%  → Suspicious (possible overfitting or unrealistic fills)
<40%  → Needs improvement (unless very high profit factor)

Why it matters:
- High win rate doesn't guarantee profitability
- Can have 40% win rate but profitable (if winners > losers)
- Very high win rate (>75%) often indicates overfitting

Common misconception: Higher is always better
Reality: 40% win rate with 3:1 reward:risk is better than 60% win rate with 1:1
```

**Profit Factor** (gross profit / gross loss):
```
Formula: Sum of All Winning Trades / Sum of All Losing Trades

Interpretation:
>2.0  → Excellent
1.5-2.0 → Good
1.2-1.5 → Acceptable
<1.2  → Marginal (risky to deploy)
<1.0  → Unprofitable (losses exceed profits)

Why it matters:
- Simple profitability measure
- <1.5 means small edge, vulnerable to slippage/fees
- Combines win rate and win size into single metric

Example:
10 trades: 6 winners ($100 each), 4 losers ($50 each)
Gross profit: $600, Gross loss: $200
Profit factor: $600 / $200 = 3.0 (excellent)
```

**Total Return vs Annual Return**:
```
Total Return: 50% over 6 months
Annual Return: ~100% (extrapolated to 12 months)

Why both matter:
- Total return: Actual profit over test period
- Annual return: Standardized for comparison across time periods
- Longer test periods more reliable (6-12 months minimum)
```

### Testing Methodology

**Minimum data requirements**:
```
Quick test: 1-3 months
- Limited validation
- Use for initial screening only
- High risk of luck/overfitting

Standard test: 6-12 months (RECOMMENDED MINIMUM)
- Captures multiple market regimes
- Sufficient trades for statistical significance
- Industry standard for strategy validation

Robust test: 12-24 months
- Ideal for high-confidence validation
- Includes bull, bear, and ranging markets
- Best for strategies before live deployment
```

**Multi-period testing** (essential for robustness):
```
1. Train period: 2024-01-01 to 2024-08-31
   run_backtest(..., start_date="2024-01-01", end_date="2024-08-31")
   → Sharpe: 1.5

2. Validation period: 2024-09-01 to 2024-12-31
   run_backtest(..., start_date="2024-09-01", end_date="2024-12-31")
   → Sharpe: 1.3

3. Compare:
   Performance similar → Robust strategy ✓
   Performance degraded significantly → Overfit to train period ✗
```

**Market regime testing**:
```
Test strategy across different market conditions:

1. Trending up (bull market): 2023-10 to 2024-03
   → Sharpe: 1.8

2. Trending down (bear market): 2024-04 to 2024-07
   → Sharpe: 0.9

3. Ranging (sideways): 2024-08 to 2024-12
   → Sharpe: 1.1

Analysis:
- Works well in all regimes ✓
- Or works in specific regime (trend-following good in trends)
- Fails in all regimes → Fundamentally broken ✗
```

### Red Flags (Overfitting Indicators)

**Warning signs that backtest results may not persist**:

**1. Unrealistically high win rate (>70%)**:
```
Win rate: 82%
Problem: Markets are noisy; >70% suggests strategy memorized past data
Solution: Test on out-of-sample data; expect performance degradation
```

**2. Very few trades (<20 in 6 months)**:
```
Total trades: 8 over 6 months
Problem: Not enough data for statistical significance; could be luck
Solution: Test longer period or adjust strategy to generate more trades
```

**3. Excellent backtest, terrible out-of-sample**:
```
Train period (Jan-Aug): Sharpe 2.5
Test period (Sep-Dec): Sharpe 0.3
Problem: Overfitted to training data
Solution: Simplify strategy, reduce parameters, test on more data
```

**4. Performance concentrated in short period**:
```
6-month test: 50% return
- Month 1-5: -5% return
- Month 6: 55% return (one lucky trade)
Problem: Performance driven by single event, not consistent edge
Solution: Analyze equity curve; look for consistent growth, not spikes
```

**5. Strategy complexity doesn't match performance**:
```
Strategy uses 12 indicators, 20+ parameters
Sharpe ratio: 1.3 (only modest improvement)
Problem: Complex strategies should dramatically outperform simple ones
Solution: Simplify; complexity without performance = overfitting
```

**6. Backtest perfect, live trading fails**:
```
Backtest: Win rate 75%, Sharpe 2.3
Live: Win rate 45%, Sharpe 0.6
Problem: Backtest didn't account for slippage, fees, execution delays
Solution: Use realistic fees (0.05-0.1%), slippage (0.05-0.1%), and test on higher timeframes
```

### Pre-Deployment Validation Checklist

**Before deploying to live trading, verify**:

- [ ] **Backtest duration**: Tested on 6+ months minimum (12+ preferred)
- [ ] **Sharpe ratio**: >1.0 (preferably >1.5)
- [ ] **Max drawdown**: <20% (acceptable risk level)
- [ ] **Win rate**: 45-65% (realistic range)
- [ ] **Profit factor**: >1.5 (sufficient edge)
- [ ] **Trade count**: 50+ trades in test period (statistical significance)
- [ ] **Multi-period validation**: Tested on multiple time ranges with consistent results
- [ ] **Out-of-sample test**: Performed well on data not used for development
- [ ] **Regime testing**: Works in different market conditions (or you understand when it fails)
- [ ] **Realistic fees**: Configured with actual trading fees (0.05-0.1%)
- [ ] **Realistic slippage**: Configured with expected slippage (0.05-0.1%)
- [ ] **No red flags**: Win rate not >70%, sufficient trades, consistent performance
- [ ] **Equity curve review**: Growth is steady, not driven by single lucky trade
- [ ] **Risk management verified**: Stop loss and position sizing are reasonable

**If any item fails, DO NOT DEPLOY. Improve strategy first.**

## Best Practices

### Configuration Best Practices

**Realistic fees and slippage**:
```
config = {
    "fee": 0.0005,      # 0.05% per trade (Hyperliquid taker fee)
    "slippage": 0.0005,  # 0.05% slippage (liquid markets)
    "leverage": 1        # Start with 1x (no leverage)
}

run_backtest(
    ...,
    config=config
)
```

**Why realistic configuration matters**:
```
Without fees/slippage:
- Backtest: 50% return, Sharpe 2.0
- Reality: Fees eat 5-10% of profit → 40% return, Sharpe 1.5

With realistic fees/slippage:
- Backtest: 40% return, Sharpe 1.5
- Reality: Matches expectation → 38-42% return
```

**Leverage testing**:
```
# Test without leverage first
run_backtest(..., config={"leverage": 1})
→ Sharpe: 1.5, Drawdown: 12%

# Then test with leverage (if deploying with leverage)
run_backtest(..., config={"leverage": 2})
→ Sharpe: 1.4, Drawdown: 24% (doubled)

Risk assessment:
- Leverage amplifies returns AND drawdowns
- 2x leverage doesn't mean 2x Sharpe (risk increases faster)
- Start deployment at 1x, increase cautiously
```

### Comparing Strategy Versions

**Systematic comparison**:
```
1. Backtest all versions on SAME date range:
   run_backtest(strategy_name="Strategy_v1", start_date="2024-01-01", end_date="2024-12-31", ...)
   run_backtest(strategy_name="Strategy_v2", start_date="2024-01-01", end_date="2024-12-31", ...)
   run_backtest(strategy_name="Strategy_v3", start_date="2024-01-01", end_date="2024-12-31", ...)

2. Compare all metrics (not just one):
   | Version | Sharpe | Drawdown | Win Rate | Profit Factor |
   |---------|--------|----------|----------|---------------|
   | v1      | 1.2    | 15%      | 50%      | 1.6           |
   | v2      | 1.5    | 12%      | 52%      | 1.8           |
   | v3      | 1.8    | 25%      | 48%      | 2.2           |

3. Analyze trade-offs:
   v1: Baseline (acceptable)
   v2: Better across all metrics ✓ (clear winner)
   v3: Higher Sharpe but excessive drawdown ✗ (too risky)

4. Decision:
   Deploy v2 (balanced improvement without excessive risk)
```

### Avoiding Redundant Backtests

**Check if backtest already exists**:
```
1. Before running backtest:
   get_latest_backtest_results(strategy_name="MyStrategy")

2. Review results:
   - If recent backtest exists with same parameters → Use cached result
   - If parameters differ (date range, symbol, timeframe) → Run new backtest

3. Saves time and clutter:
   - Backtests are fast (20-40s) but avoiding duplicates is cleaner
   - Easier to find specific backtest results later
```

## Common Workflows

### Workflow 1: Initial Strategy Validation

**Goal**: Test newly created strategy for first time

```
1. Check data availability (use browse-robonet-data):
   get_data_availability(symbols=["BTC-USDT"], only_with_data=true)
   → Verify 6+ months of history available

2. Run initial backtest (6 months):
   run_backtest(
       strategy_name="NewStrategy",
       start_date="2024-06-01",
       end_date="2024-12-31",
       symbol="BTC-USDT",
       timeframe="1h",
       config={"fee": 0.0005, "slippage": 0.0005, "leverage": 1}
   )

3. Evaluate results:
   Sharpe: 1.3 ✓ (good)
   Drawdown: 14% ✓ (moderate)
   Win rate: 51% ✓ (realistic)
   Profit factor: 1.7 ✓ (profitable)
   Total trades: 87 ✓ (sufficient)

4. Decision:
   → Strong initial results
   → Proceed to multi-period validation (Workflow 2)
```

**Cost**: $0.001 (~free)

### Workflow 2: Multi-Period Validation

**Goal**: Verify strategy robustness across different time periods

```
1. Test Period 1 (Train):
   run_backtest(..., start_date="2024-01-01", end_date="2024-06-30")
   → Sharpe: 1.5, Drawdown: 12%

2. Test Period 2 (Validation):
   run_backtest(..., start_date="2024-07-01", end_date="2024-12-31")
   → Sharpe: 1.3, Drawdown: 15%

3. Compare:
   Period 2 slightly worse but consistent ✓
   Sharpe drop: 13% (acceptable variation)
   Drawdown increase: 3% (acceptable)

4. Test Period 3 (Recent):
   run_backtest(..., start_date="2024-10-01", end_date="2024-12-31")
   → Sharpe: 1.4, Drawdown: 11%

5. Analysis:
   Consistent performance across all periods ✓
   No significant degradation ✓
   Strategy is robust ✓

6. Decision:
   → Ready for deployment consideration
   → Review pre-deployment checklist
```

**Cost**: $0.003 (3 backtests)

### Workflow 3: Before/After Improvement Testing

**Goal**: Validate that improvements actually helped

```
1. Baseline (before improvement):
   run_backtest(
       strategy_name="Strategy_original",
       start_date="2024-01-01",
       end_date="2024-12-31",
       ...
   )
   → Sharpe: 1.0, Drawdown: 18%, Win rate: 48%

2. Improve strategy (use improve-trading-strategies):
   refine_strategy(strategy_name="Strategy_original", changes="Add trailing stop", mode="new")

3. Test improvement:
   run_backtest(
       strategy_name="Strategy_original_refined",
       start_date="2024-01-01",  # SAME date range!
       end_date="2024-12-31",
       ...
   )
   → Sharpe: 1.3, Drawdown: 14%, Win rate: 52%

4. Compare (apples-to-apples on same data):
   Sharpe: +0.3 (+30%) ✓
   Drawdown: -4% (-22%) ✓
   Win rate: +4% (+8%) ✓
   → Clear improvement across all metrics

5. Validate on different period (avoid overfitting to test data):
   run_backtest(
       strategy_name="Strategy_original_refined",
       start_date="2023-07-01",  # Different period
       end_date="2023-12-31",
       ...
   )
   → Sharpe: 1.2 (still better than original's 1.0)
   → Improvement is real, not overfitted

6. Decision:
   → Keep improved version
   → Consider further optimization or deployment
```

**Cost**: $0.003 (3 backtests)

### Workflow 4: Parameter Sensitivity Testing

**Goal**: Understand how sensitive strategy is to parameters

```
1. Baseline (default parameters):
   Strategy uses RSI(14) threshold of 30
   run_backtest(...) → Sharpe: 1.3

2. Test parameter variations:
   Create variants: RSI threshold 25, 30, 35

   run_backtest(strategy_name="Strategy_RSI25", ...) → Sharpe: 1.1
   run_backtest(strategy_name="Strategy_RSI30", ...) → Sharpe: 1.3
   run_backtest(strategy_name="Strategy_RSI35", ...) → Sharpe: 1.2

3. Analysis:
   Performance varies only slightly (1.1 to 1.3)
   → Strategy is robust (not overly sensitive to exact parameters) ✓

   vs. High sensitivity:
   RSI25: Sharpe 2.5
   RSI30: Sharpe 1.3
   RSI35: Sharpe 0.4
   → Overfitted to specific parameter value ✗

4. Decision:
   Robust strategy (small variation) → Safe to deploy
   Sensitive strategy (large variation) → Likely overfit, risky to deploy
```

**Cost**: $0.003 (3 backtests)

## Troubleshooting

### "No Data Available"

**Issue**: Backtest fails with "insufficient data"

**Solutions**:
```
1. Check data availability first (use browse-robonet-data):
   get_data_availability(symbols=["YOUR-SYMBOL"], only_with_data=true)

2. Adjust date range:
   - BTC-USDT, ETH-USDT: Available from 2020-present
   - Altcoins: Typically 6-24 months
   - Use date range within available data

3. Try different symbol:
   - BTC-USDT and ETH-USDT have longest history
   - Start testing on these, then expand to altcoins
```

### "No Trades Generated"

**Issue**: Backtest completes but zero trades executed

**Solutions**:
```
1. Entry conditions too restrictive:
   - Review strategy code (use browse-robonet-data: get_strategy_code)
   - Conditions may never be met simultaneously
   - Example: "RSI < 20 AND price > 200 EMA" (RSI rarely gets to 20)

2. Test on longer period:
   - 6 months may not have ideal conditions
   - Try 12-24 months

3. Adjust thresholds (use improve-trading-strategies):
   - Loosen entry conditions slightly
   - Example: Change "RSI < 25" to "RSI < 30"
```

### "Backtest Takes >2 Minutes"

**Issue**: Backtest runs for a long time

**Solutions**:
```
1. Long date range + high-frequency timeframe:
   - 2+ years on 1m timeframe = slow
   - Solution: Test shorter range or use 5m/15m timeframe

2. Complex strategy with many indicators:
   - Some indicators are computationally expensive
   - Solution: Simplify strategy if possible

3. Normal for prediction markets:
   - run_prediction_market_backtest can take 30-60s
   - This is expected
```

### "Results Look Too Good"

**Issue**: Sharpe >3.0, win rate >75%, profit factor >5.0

**Solutions**:
```
1. Likely overfitted to historical data
2. Test on out-of-sample period (different dates)
3. Check for look-ahead bias (using future data)
4. Verify realistic fees and slippage configured
5. If too-good-to-be-true persists, be very skeptical
6. Start with tiny deployment size to validate in live market
```

## Next Steps

After backtesting strategies:

**Improve underperforming strategies**:
- Use `improve-trading-strategies` skill to refine
- Cost: $0.50-$4.00 per operation
- Test improvements with this skill again

**Deploy passing strategies** (HIGH RISK):
- Use `deploy-live-trading` skill ONLY after thorough testing
- Cost: $0.50 deployment fee
- Verify all pre-deployment checklist items passed
- Start with small capital, monitor closely

**Browse other strategies**:
- Use `browse-robonet-data` skill to see existing strategies
- Compare your results to others
- Learn from high-performing strategies

## Summary

This skill provides **strategy validation through backtesting**:

- **3 tools**: run_backtest (crypto), run_prediction_market_backtest (Polymarket), get_latest_backtest_results (cached)
- **Cost**: $0.001 per backtest (essentially free)
- **Execution**: 20-60 seconds
- **Purpose**: Validate strategy performance before risking capital

**Core principle**: Thorough backtesting (6+ months, multiple periods) is the only way to validate strategies. Past performance doesn't guarantee future results, but lack of past performance guarantees future losses.

**Critical warning**: NEVER deploy strategies without backtesting. Backtesting is cheap ($0.001) and fast (20-60s). Deploying untested strategies risks real capital and will almost certainly result in losses.

**Pre-deployment checklist**: Verify Sharpe >1.0, drawdown <20%, win rate 45-65%, profit factor >1.5, 50+ trades, tested on 6+ months, multi-period validation, realistic fees/slippage, no red flags. If ANY item fails, improve strategy before deploying.

**Best practice**: Test → Improve → Test → Improve (iterate). Each improvement should be validated with new backtest on same data to confirm actual improvement vs. noise.
