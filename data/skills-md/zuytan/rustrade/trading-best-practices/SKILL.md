---
name: Trading Best Practices
description: Critical analysis of trading techniques and financial innovation
---

# Skill: Trading Best Practices

## When to use this skill

- Before implementing a new trading strategy
- When modifying risk management logic
- Quarterly review of existing strategies
- Before going live with real capital
- When performance degrades unexpectedly

## Purpose

This skill ensures that trading implementations follow current best practices and avoid common pitfalls in algorithmic trading. It includes mechanisms to stay updated with the latest financial research and market structure changes.

## Critical Trading Principles

### 1. Risk Management (Non-negotiable)

**Position Sizing:**
- Never risk more than 1-2% of capital per trade
- Use Kelly Criterion or fixed fractional sizing
- Account for correlation between positions

**Stop Losses:**
- ALWAYS use stop losses (no exceptions)
- Place stops based on volatility (ATR) not arbitrary percentages
- Never move stops against your position

**Drawdown Protection:**
- Maximum drawdown threshold: 20% (conservative) to 30% (aggressive)
- Implement circuit breakers for daily loss limits
- Use high-water mark tracking

### 2. Strategy Development

**Avoid Overfitting:**
- ❌ Don't optimize on the same data you test on
- ✅ Use walk-forward analysis
- ✅ Test on out-of-sample data
- ✅ Prefer simple strategies with fewer parameters

**Backtesting Integrity:**
- Account for transaction costs (commissions + slippage)
- Use realistic fill assumptions (no perfect fills at close)
- Avoid look-ahead bias (only use data available at decision time)
- Include survivorship bias (test on delisted stocks too)

**Statistical Validation:**
- Minimum 100+ trades for statistical significance
- Sharpe Ratio > 1.0 (preferably > 1.5)
- Profit Factor > 1.5
- Win rate should match strategy type (trend: 40-50%, mean reversion: 55-65%)

### 3. Market Microstructure Awareness

**Execution Quality:**
- Use limit orders to control slippage
- Avoid market orders on illiquid assets
- Be aware of bid-ask spread costs
- Consider market impact for larger positions

**Regime Awareness:**
- Strategies perform differently in bull/bear/sideways markets
- Adapt position sizing to market volatility (VIX)
- Reduce exposure during high uncertainty events

### 4. Common Pitfalls to Avoid

| Pitfall | Why it's bad | Solution |
|---------|--------------|----------|
| **Curve fitting** | Strategy works on past but fails live | Walk-forward testing, simplicity |
| **Ignoring costs** | Profitable backtest becomes losing live | Include realistic commissions + slippage |
| **Revenge trading** | Emotional decisions after losses | Automated rules, circuit breakers |
| **Over-leveraging** | One bad trade wipes account | Fixed fractional position sizing |
| **No stop loss** | Small loss becomes catastrophic | Always use stops based on volatility |
| **Ignoring correlation** | Diversification illusion | Monitor sector/asset correlation |

## Research Workflow

To stay current with financial innovation, perform quarterly reviews:

### Step 1: Research Latest Practices

```bash
# Use web search to find recent research
# Topics to research:
# - "algorithmic trading best practices 2026"
# - "quantitative finance risk management"
# - "market microstructure changes"
# - "regulatory changes algorithmic trading"
```

### Step 2: Review Current Implementation

Compare findings against:
- `src/domain/risk/` - Risk management logic
- `src/application/strategies/` - Strategy implementations
- `docs/STRATEGIES.md` - Strategy documentation

### Step 3: Identify Gaps

Document any practices we're missing or doing incorrectly.

### Step 4: Update Implementation

If gaps found:
1. Create issue/task for improvement
2. Follow `/implement` workflow
3. Backtest changes thoroughly
4. Update this skill with new learnings

## Checklist: Strategy Implementation

Before implementing ANY new strategy:

- [ ] Strategy has clear entry/exit rules
- [ ] Risk per trade is defined (max 2%)
- [ ] Stop loss logic is implemented
- [ ] Position sizing accounts for volatility
- [ ] Backtested on 2+ years of data
- [ ] Tested on out-of-sample data
- [ ] Transaction costs included in backtest
- [ ] Sharpe Ratio > 1.0
- [ ] Max Drawdown < 20%
- [ ] No look-ahead bias
- [ ] Strategy logic is simple (fewer parameters = better)
- [ ] Correlation with existing strategies checked

## Red Flags in Strategy Design

```rust
// ❌ RED FLAG: No stop loss
if signal == Signal::Buy {
    execute_order(symbol, quantity); // Where's the stop?
}

// ❌ RED FLAG: Fixed position size (ignores risk)
let quantity = 100; // Always 100 shares?

// ❌ RED FLAG: No transaction costs
let profit = exit_price - entry_price; // Ignores commissions/slippage

// ❌ RED FLAG: Too many parameters
struct Strategy {
    sma_period_1: usize,
    sma_period_2: usize,
    rsi_period: usize,
    rsi_oversold: f64,
    rsi_overbought: f64,
    macd_fast: usize,
    macd_slow: usize,
    // ... 20 more parameters = overfitting
}

// ✅ GOOD: Risk-based position sizing with stop
let risk_amount = capital * risk_per_trade;
let stop_distance = entry_price * atr_multiplier;
let quantity = risk_amount / stop_distance;
let stop_loss = entry_price - stop_distance;
```

## Resources to Monitor

**Academic Research:**
- SSRN (Social Science Research Network)
- arXiv quantitative finance section
- Journal of Portfolio Management

**Industry Standards:**
- CFA Institute guidelines
- FIX Protocol updates (market structure)
- SEC/FINRA regulatory changes

**Market Data:**
- VIX (volatility regime)
- Sector rotation trends
- Correlation matrices

## Update Frequency

- **Monthly**: Check VIX and market regime
- **Quarterly**: Research latest academic papers
- **Annually**: Full strategy review and revalidation
- **Ad-hoc**: When performance degrades or market structure changes

## Integration with Other Skills

- Use `benchmarking` skill to validate strategies
- Use `critical-review` skill for code quality
- Use `rust-trading` skill for implementation rules
- Update `documentation` skill when best practices change
