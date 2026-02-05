---
name: improve-trading-strategies
description: "Iterative refinement, parameter optimization, and ML enhancement of existing trading strategies. Provides 3 tools: refine_strategy (targeted code changes, $0.50-$3.00), optimize_strategy (parameter tuning, $2-$4), enhance_with_allora (ML integration, $1-$2.50). More cost-effective than regenerating from scratch. Use when you have working strategies that need improvement. Always test improvements with test-trading-strategies before deploying."
persona: ["developer"]
risk_level: "low"
cost_profile: "$0.50 to $4.00 per operation"
tools:
  - mcp__workbench__refine_strategy
  - mcp__workbench__optimize_strategy
  - mcp__workbench__enhance_with_allora
related_skills:
  prerequisites:
    - browse-robonet-data
    - build-trading-strategies
  next_step: test-trading-strategies
  alternative: build-trading-strategies
---

# Improve Trading Strategies

## Quick Start

This skill provides tools to improve existing strategies through refinement, optimization, and ML enhancement.

**Load the tools first**:
```
Use MCPSearch to select: mcp__workbench__refine_strategy
Use MCPSearch to select: mcp__workbench__optimize_strategy
Use MCPSearch to select: mcp__workbench__enhance_with_allora
```

**Quick improvement pattern**:
```
1. Get existing code:
   (use browse-robonet-data) get_strategy_code(strategy_name="MyStrategy")

2. Make targeted changes:
   refine_strategy(
       strategy_name="MyStrategy",
       changes_description="Add trailing stop at 1% below peak profit",
       mode="new"
   )

3. Test improvement:
   (use test-trading-strategies) run_backtest(strategy_name="MyStrategy_refined")
```

**When to use this skill**:
- Have existing strategy that needs improvement
- Want to add features without rewriting from scratch
- Need to tune parameters for better performance
- Want to integrate ML predictions (Allora Network)
- Cheaper than regenerating with `build-trading-strategies`

## Available Tools (3)

### refine_strategy

**Purpose**: Make targeted code changes with AI editing

**Parameters**:
- `strategy_name` (required): Strategy to refine (any version)
- `changes_description` (required): Specific changes you want
- `mode` (required): "new" (create new version, safe) or "replace" (overwrite existing)

**Returns**: Refined strategy code with automatic validation and safety checks

**Pricing**: Real LLM cost + margin (max $3.00)
- Typical: $0.50-$1.50 depending on change complexity

**Execution Time**: ~20-30 seconds

**Use when**:
- Making specific code changes (add indicator, change threshold, fix bug)
- Adding features (trailing stop, new exit condition)
- Cheaper than regenerating with create_strategy ($0.50-$3.00 vs $1-$4.50)

**Best practice**: Always use `mode="new"` to preserve original (can compare before/after)

### optimize_strategy

**Purpose**: Tune numeric parameters using backtesting data and AI

**Parameters**:
- `strategy_name` (required): Strategy to optimize
- `start_date` (required): Start date (YYYY-MM-DD)
- `end_date` (required): End date (YYYY-MM-DD)
- `symbol` (required): Trading pair (e.g., "BTC-USDT")
- `timeframe` (required): Timeframe (1m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d)

**Returns**: Optimized strategy version with improved parameters + performance comparison (before vs after)

**Pricing**: Real LLM cost + margin (max $4.00)
- Typical: $2.00-$3.50 (most expensive improvement tool)

**Execution Time**: ~30-60 seconds

**Use when**:
- Strategy logic is good but parameters need tuning
- Want AI to search parameter space
- Have sufficient backtest data (6+ months recommended)

**Warning**: Can lead to overfitting. Use walk-forward validation.

### enhance_with_allora

**Purpose**: Add Allora Network ML price predictions to strategy logic

**Parameters**:
- `strategy_name` (required): Strategy to enhance
- `symbol` (required): Trading pair
- `timeframe` (required): Timeframe
- `start_date` (required): Start date for comparison backtest
- `end_date` (required): End date for comparison backtest

**Returns**: Enhanced strategy version with ML signals integrated + before/after performance comparison

**Pricing**: Real LLM cost + margin (max $2.50)
- Typical: $1.00-$2.00

**Execution Time**: ~30-60 seconds

**Use when**:
- Strategy is profitable but could use ML signals
- Trading BTC, ETH, SOL, or NEAR (Allora coverage)
- Want to combine technical analysis with ML predictions

**Note**: Requires Allora topics available for your symbol/timeframe (check with browse-robonet-data)

## Core Concepts

### Iterative Improvement Pattern

**Recommended improvement sequence**:

```
1. START: Working strategy (tested, decent performance)
   Sharpe: 0.8, Drawdown: 15%, Win rate: 48%

2. REFINE: Fix obvious issues ($0.50-$1.50)
   - Add missing stop loss
   - Fix indicator parameter typo
   - Add position sizing limit
   → New Sharpe: 1.1, Drawdown: 12%

3. TEST: Validate improvement
   - Compare metrics before/after
   - Ensure improvement is real, not noise

4. OPTIMIZE: Tune parameters ($2-$4)
   - Search parameter space for RSI threshold
   - Find optimal Bollinger Band period
   → New Sharpe: 1.4, Drawdown: 10%

5. TEST: Validate optimization
   - Test on out-of-sample data
   - Check for overfitting

6. ENHANCE: Add ML predictions ($1-$2)
   - Integrate Allora Network signals
   - Use ML as confirmation filter
   → New Sharpe: 1.7, Drawdown: 9%

7. TEST: Final validation
   - Compare all metrics end-to-end
   - Decide if ready for deployment

TOTAL COST: ~$4-7 (much cheaper than regenerating 3-4 times at $2.50 each = $7.50-$10)
```

### Optimization Best Practices

**Avoiding overfitting**:

**What is overfitting?**
- Parameters tuned to past data perform poorly on new data
- Strategy "memorizes" historical noise instead of learning patterns
- Common with excessive optimization

**How to avoid**:

**1. Use sufficient data** (6+ months minimum):
```
optimize_strategy(
    strategy_name="MyStrategy",
    start_date="2024-01-01",
    end_date="2024-12-31",  # 12 months
    symbol="BTC-USDT",
    timeframe="1h"
)
```

**2. Walk-forward validation**:
```
# Train on first 8 months
optimize_strategy(..., start_date="2024-01-01", end_date="2024-08-31")

# Test on last 4 months (use test-trading-strategies)
run_backtest(..., start_date="2024-09-01", end_date="2024-12-31")

# Performance should be similar on test period
# If much worse → overfitted
```

**3. Limit optimization iterations**:
- 1st optimization: Often yields 20-30% improvement
- 2nd optimization: Yields 10-15% improvement
- 3rd optimization: Yields <5% improvement (diminishing returns)
- 4th+ optimization: Often makes performance worse (overfitting)

**Stop after 2-3 optimization rounds**

**4. Compare multiple metrics** (not just one):
```
Before optimization: Sharpe 1.0, Drawdown 15%, Win rate 52%
After optimization: Sharpe 1.3, Drawdown 14%, Win rate 54%

✓ Multiple metrics improved consistently → Good
✗ Sharpe jumped to 3.0 but drawdown 40% → Overfitted/risky
```

**5. Keep parameter ranges reasonable**:
- RSI: 10-20 (not 2-100)
- Moving average: 20-200 (not 1-1000)
- Stop loss: 1-5% (not 0.1-50%)

### Allora Network ML Integration

**What Allora provides**:
- ML-powered price predictions
- Multiple horizons: 5m, 8h, 24h, 1 week
- Assets: BTC, ETH, SOL, NEAR
- Networks: Mainnet (production) + Testnet (experimental)

**How to use ML predictions**:

**Pattern 1: ML as confirmation filter**
```
Original strategy: Buy when RSI < 30
Enhanced strategy: Buy when RSI < 30 AND Allora predicts price increase

→ Reduces false signals, improves win rate
```

**Pattern 2: ML as primary signal**
```
Original strategy: Trend following with EMA
Enhanced strategy: Buy when Allora predicts strong upward movement + EMA confirms

→ ML catches moves early, EMA confirms trend
```

**Pattern 3: ML for position sizing**
```
Original strategy: Fixed 90% margin position size
Enhanced strategy:
- 95% margin when Allora confidence high
- 85% margin when Allora confidence medium
- 70% margin when Allora confidence low

→ Adaptive sizing based on prediction confidence
```

**Before using enhance_with_allora**:

```
1. Check Allora topic availability (use browse-robonet-data):
   get_allora_topics()
   → Verify your symbol has predictions

2. Match prediction horizon to strategy timeframe:
   - 5m scalping strategy → Use 5m predictions
   - 1h swing strategy → Use 8h predictions
   - 4h daily strategy → Use 24h predictions

3. Test before/after:
   - enhance_with_allora automatically runs comparison backtest
   - Check improvement metrics
   - ML should improve Sharpe by 10-30% (not 200%—that's unrealistic)
```

**Realistic ML improvement expectations**:
- **10-30% Sharpe improvement**: Good, realistic
- **30-50% improvement**: Excellent (verify it's real, not overfitting)
- **>50% improvement**: Suspicious, likely overfit to historical data
- **Negative improvement**: ML doesn't help this strategy, remove it

### Refinement Modes

**mode="new"** (recommended):
```
refine_strategy(
    strategy_name="MyStrategy",
    changes_description="Add trailing stop",
    mode="new"
)
```

Creates: `MyStrategy_refined`

**Advantages**:
- Preserves original (safe)
- Can compare versions
- Easy to rollback if refinement makes things worse

**Use when**: Always (unless you're certain about replacement)

**mode="replace"** (destructive):
```
refine_strategy(
    strategy_name="MyStrategy",
    changes_description="Fix typo",
    mode="replace"
)
```

Overwrites: `MyStrategy` (original lost)

**Advantages**:
- No version clutter
- Direct update

**Use when**:
- Fixing obvious bugs
- Making trivial changes (typos, formatting)
- You're certain the change is correct
- You've backed up the original code

**Warning**: Original cannot be recovered. Use sparingly.

## Best Practices

### Cost Sequencing

**Optimize costs by ordering operations from cheap to expensive**:

```
RECOMMENDED ORDER:

1. Refine first ($0.50-$3.00):
   - Fix obvious issues
   - Add missing features
   - Make targeted improvements
   - Cheapest, often yields biggest gains

2. Optimize second ($2-$4):
   - Tune parameters after logic is solid
   - Most expensive improvement tool
   - Wait until refinement complete

3. ML enhance third ($1-$2.50):
   - Add after base strategy is strong
   - ML won't fix fundamentally broken strategy
   - Test thoroughly (ML can overfit too)

AVOID THIS ORDER:
1. Optimize first → Tuning parameters on broken logic
2. ML enhance → Adding ML to weak foundation
3. Refine → Should have fixed issues first

Cost difference: $3.50-9.50 (recommended) vs $3.50-9.50 (reversed order)
Outcome quality: Much better with recommended order
```

### Before/After Validation

**Always compare metrics after improvement**:

```
BEFORE improvement:
run_backtest(strategy_name="MyStrategy_original", ...)
→ Sharpe: 1.0, Drawdown: 15%, Win rate: 50%

IMPROVE:
refine_strategy(...) or optimize_strategy(...) or enhance_with_allora(...)

AFTER improvement:
run_backtest(strategy_name="MyStrategy_refined", ...)
→ Sharpe: 1.3, Drawdown: 12%, Win rate: 54%

COMPARE:
- Sharpe improved 30% ✓
- Drawdown reduced 20% ✓
- Win rate up 4% ✓
→ Real improvement, keep changes
```

**Red flags** (improvement might be overfitting):
- Sharpe improved >100% (doubled)
- Win rate >70% (unrealistic)
- Performance much better on recent data than older data
- Improvement disappears on out-of-sample test

**Validation checklist**:
- [ ] Test on multiple time periods (not just one)
- [ ] Compare all metrics (Sharpe, drawdown, win rate, profit factor)
- [ ] Check improvement is consistent (not just lucky period)
- [ ] Verify on out-of-sample data (walk-forward)
- [ ] Improvement is meaningful (>0.2 Sharpe increase)

### Specific vs Generic Refinements

**Specific refinements work best**:

✓ **GOOD** (specific):
```
"Add trailing stop: Once profit exceeds 3%, move stop loss to 1.5% below highest price since entry"
```

✗ **BAD** (generic):
```
"Make the strategy better"
```

**Specific refinement examples**:
- "Change RSI threshold from 30 to 25"
- "Add volume filter: only enter if volume > 1.5× 20-period average"
- "Modify stop loss from 2% to 1.5× ATR"
- "Add time-based exit: close position after 24 hours regardless of profit/loss"

**Generic refinements that don't work well**:
- "Improve performance"
- "Make it more profitable"
- "Optimize everything"
- "Fix all issues"

### Testing After Each Change

**Iterative test pattern**:

```
1. Baseline:
   run_backtest(strategy_name="Original") → Sharpe 1.0

2. Refine:
   refine_strategy(changes="Add feature X")

3. Test refinement:
   run_backtest(strategy_name="Original_refined") → Sharpe 1.2
   Improvement: +0.2 ✓

4. Optimize:
   optimize_strategy(strategy_name="Original_refined")

5. Test optimization:
   run_backtest(strategy_name="Original_refined_optimized") → Sharpe 1.5
   Improvement: +0.3 ✓

6. Enhance with ML:
   enhance_with_allora(strategy_name="Original_refined_optimized")

7. Test ML enhancement:
   run_backtest(strategy_name="Original_refined_optimized_allora") → Sharpe 1.8
   Improvement: +0.3 ✓

CUMULATIVE: 1.0 → 1.8 (80% improvement through iterative testing)
```

**Never skip testing between improvements**. Each change should be validated before moving to next.

## Common Workflows

### Workflow 1: Targeted Refinement

**Goal**: Fix specific issues or add targeted features

```
1. Get current code (use browse-robonet-data):
   get_strategy_code(strategy_name="MyStrategy")

2. Identify improvement:
   "Strategy needs trailing stop to lock in profits"

3. Refine with specific changes:
   refine_strategy(
       strategy_name="MyStrategy",
       changes_description="Add trailing stop: Once profit >3%,
                          trail stop at 1.5% below highest price",
       mode="new"
   )

4. Test before/after:
   run_backtest(strategy_name="MyStrategy") → Sharpe 1.1
   run_backtest(strategy_name="MyStrategy_refined") → Sharpe 1.4

5. Compare:
   Improvement: +0.3 Sharpe (27% better) ✓
   Keep refined version
```

**Cost**: ~$0.50-$1.50 (much cheaper than regenerating)

### Workflow 2: Parameter Optimization

**Goal**: Tune numeric parameters for better performance

```
1. Baseline test (use test-trading-strategies):
   run_backtest(
       strategy_name="RSIMeanReversion_M",
       start_date="2024-01-01",
       end_date="2024-08-31"
   )
   → Sharpe: 0.9, Drawdown: 18%

2. Optimize parameters:
   optimize_strategy(
       strategy_name="RSIMeanReversion_M",
       start_date="2024-01-01",
       end_date="2024-08-31",
       symbol="BTC-USDT",
       timeframe="1h"
   )
   → Creates: RSIMeanReversion_M_optimized

3. Test optimized version:
   run_backtest(
       strategy_name="RSIMeanReversion_M_optimized",
       start_date="2024-09-01",  # Out-of-sample!
       end_date="2024-12-31"
   )
   → Sharpe: 1.2, Drawdown: 14%

4. Validate improvement:
   - Sharpe improved 33% ✓
   - Drawdown reduced 22% ✓
   - Performed well on out-of-sample data ✓
   → Real improvement, not overfitting
```

**Cost**: ~$2-$4

### Workflow 3: ML Enhancement

**Goal**: Integrate Allora predictions to improve performance

```
1. Check ML availability (use browse-robonet-data):
   get_allora_topics()
   → Verify BTC has 8h predictions available

2. Baseline strategy performance:
   run_backtest(strategy_name="TrendFollower_M") → Sharpe 1.3

3. Enhance with ML:
   enhance_with_allora(
       strategy_name="TrendFollower_M",
       symbol="BTC-USDT",
       timeframe="1h",
       start_date="2024-01-01",
       end_date="2024-12-31"
   )
   → Automatically tests before/after
   → Returns comparison: Base Sharpe 1.3 → Enhanced Sharpe 1.6

4. Review improvement:
   +0.3 Sharpe (23% improvement) ✓
   ML is helping, keep enhancement

5. If needed, refine ML integration:
   refine_strategy(
       strategy_name="TrendFollower_M_allora",
       changes="Use ML only as confirmation, not primary signal",
       mode="new"
   )
```

**Cost**: ~$1-$2.50

### Workflow 4: Complete Overhaul

**Goal**: Comprehensive improvement of existing strategy

```
1. Baseline:
   get_latest_backtest_results(strategy_name="Old_Strategy")
   → Sharpe: 0.7, Drawdown: 22%, Win rate: 45%
   → Needs major improvement

2. Fix critical issues first (REFINE $0.50-$1.50):
   refine_strategy(
       strategy_name="Old_Strategy",
       changes="Fix: Add proper stop loss (missing),
                      improve position sizing (too aggressive),
                      add volume filter (too many false signals)",
       mode="new"
   )
   → Test: Sharpe 1.0 (+43% improvement)

3. Tune parameters (OPTIMIZE $2-$4):
   optimize_strategy(
       strategy_name="Old_Strategy_refined",
       ...
   )
   → Test: Sharpe 1.4 (+40% improvement from refined)

4. Add ML enhancement (ENHANCE $1-$2):
   enhance_with_allora(
       strategy_name="Old_Strategy_refined_optimized",
       ...
   )
   → Test: Sharpe 1.7 (+21% improvement from optimized)

5. Final validation:
   Compare: 0.7 → 1.7 Sharpe (143% total improvement)
   Test on multiple periods
   Test on out-of-sample data
   → Ready for deployment consideration

TOTAL COST: ~$4-7.50
ALTERNATIVE: Regenerate 3 times with build-trading-strategies → $7.50-$13.50
SAVINGS: $0.50-$6 + better iterative process
```

## Troubleshooting

### "Refinement Made Performance Worse"

**Issue**: Strategy performs worse after refinement

**Solutions**:
- Good thing you used `mode="new"` (original preserved!)
- Revert to original strategy
- Analyze what went wrong (was change too aggressive?)
- Try smaller, more targeted change

### "Optimization Yields Unrealistic Results"

**Issue**: Optimized strategy has Sharpe >3.0, win rate >80%

**Solutions**:
- Likely overfitted to historical data
- Test on out-of-sample period (different date range)
- If performance drops significantly → overfitted, discard
- Use less aggressive optimization (shorter period, fewer parameters)

### "ML Enhancement Doesn't Help"

**Issue**: Sharpe same or worse after enhance_with_allora

**Solutions**:
- ML doesn't help every strategy (technical analysis may be sufficient)
- Strategy timeframe may not match prediction horizon
- Check if Allora predictions align with strategy logic
- Remove ML enhancement, stick with base strategy

### "Successive Optimizations Making Things Worse"

**Issue**: 1st optimization helped, 2nd optimization helped, 3rd made performance worse

**Solutions**:
- **Diminishing returns**: You've hit optimization limits
- Stop optimizing (keep version before 3rd optimization)
- More optimization = more overfitting risk
- **General rule**: Stop after 2-3 optimization rounds

## Next Steps

After improving strategies:

**Test improvements** (CRITICAL):
- Use `test-trading-strategies` skill to validate
- Cost: $0.001 per backtest
- Test on multiple time periods
- Compare all metrics (not just Sharpe)

**Deploy improved strategies**:
- Use `deploy-live-trading` skill (HIGH RISK)
- Cost: $0.50 deployment fee
- Only after thorough testing shows consistent improvement
- Start small, monitor closely

**Further improvement**:
- Can iterate: refine → test → optimize → test → enhance → test
- Diminishing returns after 2-3 improvement cycles
- Know when to stop (don't over-optimize)

## Summary

This skill provides **iterative strategy improvement** tools:

- **3 tools**: refine ($0.50-$3), optimize ($2-$4), enhance with ML ($1-$2.50)
- **Cost**: $0.50-$4 per operation (cheaper than regenerating)
- **Execution**: 20-60 seconds depending on tool

**Core principle**: Improve iteratively with testing between each change. Small, targeted improvements compound better than big, sweeping changes.

**Recommended sequence**: Refine (cheap, fix issues) → Optimize (expensive, tune parameters) → Enhance with ML (add predictions). Test after each step.

**Critical warning**: Optimization can lead to overfitting. Use walk-forward validation, test on out-of-sample data, and stop after 2-3 optimization rounds. If improvement looks too good to be true (>100% Sharpe increase), it probably is.

**Best practice**: Always use `mode="new"` for refinements to preserve originals. Test before/after on multiple time periods. Stop optimizing when improvements become marginal or negative.
