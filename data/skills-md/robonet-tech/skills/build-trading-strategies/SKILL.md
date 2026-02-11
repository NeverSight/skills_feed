---
name: build-trading-strategies
description: "AI-powered generation of complete trading strategy code. Uses create_strategy and create_prediction_market_strategy to transform requirements into production-ready Python code. Most expensive AI tool ($1.00-$4.50 per generation). Generates complete Jesse framework strategies with entry/exit logic, position sizing, and risk management. Use after exploring data and optionally generating ideas. ALWAYS test with test-trading-strategies before deploying."
persona: ["developer"]
risk_level: "low"
cost_profile: "$1.00 to $4.50 per generation"
tools:
  - mcp__workbench__create_strategy
  - mcp__workbench__create_prediction_market_strategy
related_skills:
  prerequisite: browse-robonet-data
  recommended: design-trading-strategies
  next_step: test-trading-strategies
  alternative: improve-trading-strategies
---

# Build Trading Strategies

## Quick Start

This skill generates complete, production-ready strategy code using AI. This is the **most expensive tool** in Robonet ($1-$4.50 per generation).

**Load the tools first**:
```
Use MCPSearch to select: mcp__workbench__create_strategy
Use MCPSearch to select: mcp__workbench__create_prediction_market_strategy
```

**Basic usage**:
```
create_strategy(
    strategy_name="RSIMeanReversion_M",
    description="Buy when RSI(14) < 30 and price at lower Bollinger Band (20,2).
                 Sell when RSI > 70 or price at middle Bollinger Band.
                 Stop loss at 2% below entry. Position size 90% of available margin."
)
```

Returns complete Python strategy code ready for backtesting.

**When to use this skill**:
- You have a clear strategy concept and want working code
- You've explored data and know what indicators/symbols to use
- You're ready to commit to expensive development ($1-$4.50)

**When NOT to use this skill**:
- You're still exploring ideas → Use `design-trading-strategies` first ($0.05-$1.00)
- You have existing code to improve → Use `improve-trading-strategies` ($0.50-$3.00)
- You haven't checked data availability → Use `browse-robonet-data` first (free-$0.001)

## Available Tools (2)

### create_strategy

**Purpose**: Generate complete crypto trading strategy code with AI

**Parameters**:
- `strategy_name` (required, string): Name following pattern `{Name}_{RiskLevel}[_suffix]`
  - Risk levels: H (high), M (medium), L (low)
  - Examples: "RSIMeanReversion_M", "MomentumBreakout_H_v2"
- `description` (required, string): Detailed requirements including:
  - Entry conditions (specific indicator values and thresholds)
  - Exit conditions (stop loss, take profit, trailing stops)
  - Position sizing (percentage of margin to use)
  - Risk management (max loss per trade)
  - Indicators to use (exact names from browse-robonet-data)
  - Timeframe context (5m scalping vs 1h swing trading)

**Returns**: Complete Python strategy code with:
- `should_long()` - Check if conditions met for long entry
- `should_short()` - Check if conditions met for short entry
- `go_long()` - Execute long entry with position sizing
- `go_short()` - Execute short entry with position sizing
- Optional methods: `on_open_position()`, `update_position()`, `should_cancel_entry()`

**Pricing**: Real LLM cost + margin (max $4.50)
- Typical cost: $1.00-$3.00 depending on complexity
- Most expensive tool in Robonet

**Execution Time**: ~30-60 seconds

**Use when**:
- Building new crypto perpetual trading strategy
- You have clear, detailed requirements
- You've verified indicators/symbols available (browse-robonet-data)
- Ready to commit to expensive operation

### create_prediction_market_strategy

**Purpose**: Generate Polymarket strategy code with YES/NO token trading logic

**Parameters**:
- `strategy_name` (required, string): Name following same pattern as create_strategy
- `description` (required, string): Detailed requirements for YES/NO token logic:
  - Conditions for buying YES tokens (probability thresholds)
  - Conditions for buying NO tokens
  - Exit criteria (profit targets, time-based exits)
  - Position sizing (percentage per market)
  - Market selection criteria (categories, liquidity requirements)

**Returns**: Complete Python strategy code with:
- `should_buy_yes()` - Check if conditions met for YES token entry
- `should_buy_no()` - Check if conditions met for NO token entry
- `go_yes()` - Execute YES token purchase with sizing
- `go_no()` - Execute NO token purchase with sizing
- Optional methods: `should_sell_yes()`, `should_sell_no()`, `on_market_resolution()`

**Pricing**: Real LLM cost + margin (max $4.50)
- Typical cost: $1.00-$3.00

**Execution Time**: ~30-60 seconds

**Use when**:
- Building Polymarket prediction market strategies
- Trading on real-world events (politics, economics, sports)
- Want YES/NO token exposure based on probability analysis

## Core Concepts

### Jesse Framework Structure

**All crypto strategies must implement these required methods**:

```python
class MyStrategy(Strategy):
    def should_long(self) -> bool:
        """Check if all conditions are met for long entry"""
        # Return True to signal long entry opportunity
        # Called every candle

    def should_short(self) -> bool:
        """Check if all conditions are met for short entry"""
        # Return True to signal short entry opportunity
        # Called every candle

    def go_long(self):
        """Execute long entry with position sizing"""
        # Calculate position size (qty)
        # Place buy order
        # Set stop loss and take profit in on_open_position()

    def go_short(self):
        """Execute short entry with position sizing"""
        # Calculate position size (qty)
        # Place sell order
        # Set stop loss and take profit in on_open_position()
```

**Optional but recommended methods**:

```python
    def on_open_position(self, order):
        """Set stop loss and take profit after entry"""
        # Called when position opens
        # Set self.stop_loss and self.take_profit

    def update_position(self):
        """Update position (trailing stops, etc.)"""
        # Called every candle while in position
        # Modify stop loss for trailing stops

    def should_cancel_entry(self) -> bool:
        """Cancel unfilled entry orders"""
        # Return True to cancel pending entry order
```

### Strategy Naming Convention

**Follow this pattern**: `{Name}_{RiskLevel}[_suffix]`

**Risk Levels**:
- **H** (High): Aggressive strategies, high leverage, tight stops, >20% drawdown acceptable
- **M** (Medium): Balanced strategies, moderate leverage, standard stops, 10-20% drawdown
- **L** (Low): Conservative strategies, low leverage, wide stops, <10% drawdown

**Examples**:
- `RSIMeanReversion_M` - Base strategy, medium risk
- `MomentumBreakout_H_optimized` - After optimization, high risk
- `TrendFollower_L_allora` - With Allora ML enhancement, low risk
- `BollingerBands_M_v2` - Version 2 of strategy

**Why naming matters**:
- Helps organize strategies by risk profile
- Clear versioning (_v2, _v3) tracks evolution
- Suffixes (_optimized, _allora) indicate enhancements
- Consistent naming enables easy filtering and comparison

### Position Sizing Patterns

**Recommended position sizing**: 85-95% of available margin

**Common approaches**:

**1. Fixed percentage** (simple, predictable):
```python
def go_long(self):
    qty = utils.size_to_qty(self.balance * 0.90, self.price)
    self.buy = qty, self.price
```

**2. Volatility-based** (adaptive to market conditions):
```python
def go_long(self):
    atr = ta.atr(self.candles, period=14)
    # Reduce size in high volatility
    size_multiplier = 0.90 if atr < self.price * 0.02 else 0.70
    qty = utils.size_to_qty(self.balance * size_multiplier, self.price)
    self.buy = qty, self.price
```

**3. Risk-based** (size based on stop loss distance):
```python
def go_long(self):
    atr = ta.atr(self.candles, period=14)
    stop_distance = atr * 2  # Stop at 2× ATR
    # Risk 2% of balance per trade
    risk_amount = self.balance * 0.02
    qty = risk_amount / stop_distance
    self.buy = qty, self.price
```

**Best practice**: Specify position sizing approach in description when creating strategy

### Risk Management Requirements

**Every strategy should include**:

**1. Stop Loss** (mandatory):
```python
def on_open_position(self, order):
    atr = ta.atr(self.candles, period=14)
    # Stop at 2× ATR below entry (long) or above entry (short)
    self.stop_loss = qty, self.price - (atr * 2)  # Long
    # or
    self.stop_loss = qty, self.price + (atr * 2)  # Short
```

**2. Take Profit** (recommended):
```python
def on_open_position(self, order):
    atr = ta.atr(self.candles, period=14)
    # Target at 3× ATR (risk/reward = 1.5)
    self.take_profit = qty, self.price + (atr * 3)  # Long
```

**3. Position sizing** (see above)

**Red flags** (avoid these):
- No stop loss (unlimited downside)
- Stop loss too tight (<0.5% from entry) - will be stopped out by noise
- Stop loss too wide (>5% from entry) - excessive risk per trade
- Position size >95% of margin - insufficient buffer for margin calls
- No take profit - positions may give back gains

### Available Indicators

**170+ technical indicators via `jesse.indicators`**:

Use exact names when describing strategy requirements:

**Momentum** (16 indicators):
- RSI, MACD, Stochastic, ADX, CCI, MFI, ROC, Williams %R, etc.

**Trend** (12 indicators):
- EMA, SMA, DEMA, TEMA, WMA, Supertrend, Parabolic SAR, VWAP, HMA, etc.

**Volatility** (8 indicators):
- Bollinger Bands, ATR, Keltner Channels, Donchian Channels, Standard Deviation, etc.

**Volume** (10 indicators):
- OBV, Volume Profile, Chaikin Money Flow, etc.

**How to find indicators**:
```
(Use browse-robonet-data skill)
get_all_technical_indicators(category="momentum")
```

**In strategy description, use exact names**:
✓ "Use RSI with period 14"
✓ "Use Bollinger Bands with period 20, std 2"
✗ "Use relative strength" (ambiguous)
✗ "Use BB" (unclear abbreviation)

## Best Practices

### Cost Management

**This is the most expensive tool ($1-$4.50). Minimize waste**:

**Before using create_strategy**:
1. ✅ Browse data with `browse-robonet-data` (verify symbols/indicators available)
2. ✅ Optionally generate ideas with `design-trading-strategies` ($0.05-$1.00 exploration)
3. ✅ Have detailed requirements written out
4. ✅ Understand Jesse framework basics

**Avoid these costly mistakes**:
- ❌ Creating strategy without checking indicator availability → Wasted $2.50
- ❌ Vague description ("build a good BTC strategy") → Poor results, need to regenerate
- ❌ Unclear requirements → Code doesn't match expectations, wasted generation
- ❌ Not specifying risk management → Need to regenerate with stops/sizing

**Cost-saving pattern**:
```
1. browse-robonet-data ($0.001) → Verify resources
2. design-trading-strategies ($0.30) → Explore 3 ideas
3. Pick best idea and refine description
4. create_strategy ($2.50) → Generate once, correctly
Total: $2.80 with high success rate

vs.

1. create_strategy ($2.50) → Vague requirements
2. Doesn't work, try again ($2.50)
3. Still not right ($2.50)
Total: $7.50 with frustration
```

### Writing Effective Descriptions

**Anatomy of a good description**:

```
Entry Conditions:
- Specific indicator with exact parameters
- Exact thresholds
- Multiple conditions with AND/OR logic

Exit Conditions:
- Stop loss method and distance
- Take profit method and target
- Trailing stop if applicable

Position Sizing:
- Percentage of margin to use
- Or risk-based sizing method

Risk Management:
- Maximum loss per trade
- Any position limits

Context:
- Timeframe (5m, 1h, 4h, 1d)
- Market regime (trending, ranging)
```

**Example of GOOD description**:

```
"RSI Mean Reversion strategy for BTC-USDT on 1h timeframe.

ENTRY (Long):
- RSI(14) < 30 (oversold)
- Price touches lower Bollinger Band (20-period, 2 std dev)
- Confirm with volume: current volume > 1.2× 20-period average

EXIT (Long):
- Take profit: Price reaches middle Bollinger Band
- Stop loss: 2% below entry price
- Trailing stop: Once profit >3%, trail stop at 1.5% below highest price

POSITION SIZING:
- Use 90% of available margin per trade
- Single position at a time (no pyramiding)

RISK MANAGEMENT:
- Maximum loss: 2% of account per trade
- No new trades if in drawdown >10%"
```

**Example of BAD description**:

```
"Build a profitable BTC strategy using RSI and Bollinger Bands"
```

Problems:
- No entry conditions specified (what RSI value?)
- No exit conditions (when to close?)
- No position sizing (how much to risk?)
- No timeframe (1m? 1d?)
- Too vague → Will require regeneration

### Validation Checklist

**After strategy is generated, verify code includes**:

- [ ] All required methods (should_long, should_short, go_long, go_short)
- [ ] Stop loss logic (in on_open_position or go_long/go_short)
- [ ] Take profit logic (recommended)
- [ ] Position sizing (qty calculation in go_long/go_short)
- [ ] Valid indicator calls (e.g., `ta.rsi(self.candles, period=14)`)
- [ ] Proper entry/exit conditions matching description
- [ ] No syntax errors (code is runnable)
- [ ] Indicator parameters are reasonable (not over-optimized)

**If validation fails**:
- Use `improve-trading-strategies` skill to fix issues ($0.50-$3.00)
- Cheaper than regenerating with `create_strategy` ($1-$4.50)

### Timeframe Considerations

**Match strategy logic to timeframe**:

**Scalping (1m-5m)**:
- Tight stops (0.2-0.5%)
- Quick exits (minutes to hours)
- High-frequency indicators (short periods)
- Focus on execution and fees

**Intraday (15m-1h)**:
- Moderate stops (0.5-2%)
- Hold hours to 1 day
- Standard indicator periods (14, 20, 50)
- Balance between frequency and noise

**Swing Trading (4h-1d)**:
- Wide stops (2-5%)
- Hold days to weeks
- Longer indicator periods (50, 100, 200)
- Focus on larger trends

**Specify timeframe in description**:
```
"For 1h timeframe..." (helps AI tune indicator parameters appropriately)
```

## Common Workflows

### Workflow 1: Build from Scratch

**Goal**: Create new strategy from concept

```
1. Explore data (use browse-robonet-data):
   get_all_symbols() → Choose BTC-USDT
   get_all_technical_indicators(category="momentum") → Pick RSI
   get_all_technical_indicators(category="volatility") → Pick Bollinger Bands

2. Optional: Generate ideas (use design-trading-strategies):
   generate_ideas(strategy_count=3) → Get concepts
   Pick best concept as starting point

3. Write detailed description:
   - Entry: RSI < 30 AND price at lower BB
   - Exit: Price at middle BB OR stop loss 2%
   - Sizing: 90% margin
   - Timeframe: 1h

4. Create strategy:
   create_strategy(
       strategy_name="RSIMeanReversion_M",
       description="[detailed description from step 3]"
   )

5. Validate generated code:
   - Check all required methods present
   - Verify indicators match description
   - Confirm risk management included

6. Test immediately (use test-trading-strategies):
   run_backtest(strategy_name="RSIMeanReversion_M", ...)
```

**Cost**: ~$2-4 total ($0.30 ideas + $2.50 creation + $0.001 test)

### Workflow 2: Build from Idea

**Goal**: Transform AI-generated concept into working code

```
1. Generate ideas (use design-trading-strategies):
   generate_ideas(strategy_count=3)

   Idea #2: "Bollinger Band Breakout"
   Entry: Price breaks above upper BB with high volume
   Exit: Price returns to middle BB
   Uses: Bollinger Bands, Volume

2. Refine idea into detailed description:
   "Bollinger Band Breakout strategy for ETH-USDT on 4h timeframe.

   ENTRY (Long):
   - Price closes above upper Bollinger Band (20, 2)
   - Current volume > 1.5× 20-period average volume
   - ADX(14) > 25 (confirm trend strength)

   EXIT (Long):
   - Price closes below middle Bollinger Band
   - Or stop loss 3% below entry
   - Or take profit at 9% above entry (3:1 reward:risk)

   POSITION SIZING: 85% of margin
   RISK: Max 3% loss per trade"

3. Create strategy:
   create_strategy(
       strategy_name="BollingerBreakout_H",
       description="[detailed description from step 2]"
   )

4. Test and validate:
   run_backtest(strategy_name="BollingerBreakout_H", ...)
```

**Cost**: ~$3 ($0.30 ideas + $2.50 creation + $0.001 test)

### Workflow 3: Build Prediction Market Strategy

**Goal**: Create Polymarket YES/NO token trading strategy

```
1. Browse prediction markets (use browse-robonet-data):
   get_data_availability(data_type="polymarket")
   → See available markets

2. Analyze market data:
   get_prediction_market_data(condition_id="...")
   → Study YES/NO token price history

3. Write detailed description:
   "Polymarket probability arbitrage strategy for crypto_rolling markets.

   BUY YES TOKEN when:
   - YES token price < 0.40 (implied 40% probability)
   - Market has >$10k volume (sufficient liquidity)
   - Time to resolution > 2 hours (avoid last-minute volatility)

   BUY NO TOKEN when:
   - NO token price < 0.40 (YES price > 0.60)
   - Same liquidity and time criteria

   EXIT:
   - Sell when price reaches 0.55 (15% profit target)
   - Or hold until market resolution
   - Stop loss: Sell if price drops to 0.25 (37.5% loss)

   POSITION SIZING: 5% of capital per market
   MAX POSITIONS: 10 simultaneous markets"

4. Create prediction market strategy:
   create_prediction_market_strategy(
       strategy_name="PolymarketArbitrage_M",
       description="[detailed description from step 3]"
   )

5. Test on historical markets:
   run_prediction_market_backtest(...)
```

**Cost**: ~$2.50 + $0.001 test = $2.501

## Advanced Usage

### Multi-Timeframe Strategies

**Describe higher timeframe context in strategy requirements**:

```
"ETH-USDT swing trading strategy on 1h timeframe with 4h trend filter.

HIGHER TIMEFRAME (4h):
- Only take long trades when 4h EMA(50) is rising
- Only take short trades when 4h EMA(50) is falling

ENTRY TIMEFRAME (1h):
- [standard entry conditions on 1h]
..."
```

AI will generate code that checks higher timeframe conditions.

### Complex Entry Logic

**Specify precise logic for multiple conditions**:

```
"Entry requires ALL of these conditions (AND logic):
1. RSI(14) < 30
2. Price < Lower Bollinger Band (20, 2)
3. MACD histogram positive (bullish divergence)
4. Volume > 1.3× average

OR entry if these alternative conditions met:
1. Price makes higher low
2. RSI makes higher low (bullish divergence)
3. Volume surge (>2× average)"
```

AI can handle complex multi-condition logic if clearly specified.

### Dynamic Position Sizing

**Specify adaptive sizing in description**:

```
"Position sizing based on volatility:
- When ATR(14) < 2% of price: Use 95% margin (low volatility)
- When ATR between 2-4%: Use 85% margin (normal)
- When ATR > 4%: Use 70% margin (high volatility)

This reduces risk during volatile periods."
```

## Troubleshooting

### "Generated Code Has Errors"

**Issue**: Strategy code doesn't run or has syntax errors

**Solutions**:
- Use `improve-trading-strategies` skill with `refine_strategy` to fix errors
- Cheaper than regenerating ($0.50-$3.00 vs $1-$4.50)
- Specify exact error message in refine description

### "Strategy Doesn't Match Description"

**Issue**: Generated logic differs from what you requested

**Solutions**:
- Description may have been ambiguous
- Use `improve-trading-strategies` skill to refine specific parts
- For major mismatch, may need to regenerate with clearer description

### "Indicators Not Available"

**Issue**: Strategy uses indicators that don't exist in Jesse

**Solutions**:
- Should have used `browse-robonet-data` first to verify indicators
- Use `refine_strategy` to replace with valid indicators
- Check indicator spelling (RSI not rsi, MACD not macd)

### "Strategy Too Complex"

**Issue**: Generated code is overly complicated with 8+ indicators

**Solutions**:
- Simplify description (request fewer indicators)
- Use `refine_strategy` to remove unnecessary complexity
- Complex strategies often overfit and perform poorly

### "No Risk Management Included"

**Issue**: Generated code lacks stop loss or position sizing

**Solutions**:
- Description must explicitly request risk management
- Use `refine_strategy` to add stop loss and sizing
- Always specify: "Include stop loss at X% and position size of Y%"

## Next Steps

After building a strategy:

**Test the strategy** (CRITICAL - do this next):
- Use `test-trading-strategies` skill to backtest
- Cost: $0.001 per backtest
- Validate performance before ANY further work
- Check: Sharpe >1.0, drawdown <20%, win rate 45-65%

**Improve the strategy** (if needed):
- Use `improve-trading-strategies` skill to refine code
- Cost: $0.50-$4.00 per operation
- Cheaper than regenerating from scratch
- Options: refine_strategy, optimize_strategy, enhance_with_allora

**Deploy to production** (only after thorough testing):
- Use `deploy-live-trading` skill (HIGH RISK)
- Cost: $0.50 deployment fee
- NEVER deploy without extensive backtesting (6+ months recommended)
- Start small, monitor closely

## Summary

This skill provides **AI-powered strategy code generation**:

- **2 tools**: create_strategy (crypto), create_prediction_market_strategy (Polymarket)
- **Cost**: $1.00-$4.50 per generation (MOST EXPENSIVE tool)
- **Execution**: 30-60 seconds
- **Output**: Production-ready Python code with Jesse framework structure

**Core principle**: This is expensive. Prepare thoroughly before using:
1. Browse data (verify resources available)
2. Optionally generate ideas (explore concepts cheaply)
3. Write detailed description (clear requirements)
4. Generate once, correctly
5. Test immediately

**Critical warning**: Generated code may have bugs or not match expectations. ALWAYS test with `test-trading-strategies` before deploying. NEVER deploy untested strategies to live trading.

**Cost optimization**: Spending 5 minutes preparing ($0-$0.30 exploration) saves dollars in wasted generations and improves success rate dramatically.
