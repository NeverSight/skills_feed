---
name: design-trading-strategies
description: "AI-powered strategy ideation and concept exploration. Generate 1-10 creative trading strategy concepts based on current market data using the generate_ideas tool. Cheapest AI operation ($0.05-$1.00 vs $1-$4.50 for full strategy creation). Use this skill to explore creative concepts before committing to expensive development. Best for: exploring new markets, brainstorming approaches, validating ideas before building."
persona: ["researcher", "developer"]
risk_level: "low"
cost_profile: "$0.05 to $1.00 per idea generation"
tools:
  - mcp__workbench__generate_ideas
related_skills:
  prerequisite: browse-robonet-data
  next_steps:
    - build-trading-strategies
    - test-trading-strategies
---

# Design Trading Strategies

## Quick Start

This skill generates AI-powered trading strategy concepts before you commit to expensive development. It's the cheapest AI tool in Robonet ($0.05-$1.00 vs $1-$4.50 for full strategy creation).

**Load the tool first**:
```
Use MCPSearch to select: mcp__workbench__generate_ideas
```

**Basic usage**:
```
generate_ideas(strategy_count=3)
```

Returns 3 creative strategy concepts with descriptions of market conditions, entry/exit logic, and rationale.

**When to use this skill**:
- Exploring new markets or timeframes
- Stuck for strategy ideas
- Want to validate approach before expensive development
- Need inspiration from current market data
- Brainstorming session before building

**When to skip this skill**:
- You already know exactly what you want to build → Go directly to `build-trading-strategies`
- Iterating on existing strategy → Use `improve-trading-strategies`

## The generate_ideas Tool

**Purpose**: Creates innovative strategy concepts based on current Hyperliquid market data

**Parameters**:
- `strategy_count` (optional, integer, 1-10): Number of ideas to generate (default: 1)

**Returns**: List of strategy concepts including:
- **Strategy name**: Descriptive name for the concept
- **Market conditions**: What market regime it's designed for (trending, ranging, volatile, etc.)
- **Entry logic**: When to enter positions
- **Exit logic**: When to exit positions
- **Risk management**: Stop loss and position sizing approach
- **Indicators**: Which technical indicators to use
- **Rationale**: Why this strategy might work

**Pricing**: Real LLM cost + margin (max $1.00)
- Typical cost: $0.05-$0.50 depending on number of ideas
- Significantly cheaper than `create_strategy` ($1-$4.50)

**Execution Time**: ~20-40 seconds

**Example output**:
```
Strategy 1: "Bollinger Band Mean Reversion"
Market conditions: Ranging market with clear support/resistance
Entry logic: Enter long when price touches lower band and RSI <30
Exit logic: Exit at middle band or when RSI >70
Risk management: 2% position size, stop loss at 1.5× ATR below entry
Indicators: Bollinger Bands (20, 2), RSI (14), ATR (14)
Rationale: Markets tend to revert to the mean in ranging conditions.
           Bollinger Bands identify extremes, RSI confirms oversold/overbought.
```

## Core Concepts

### Strategy Archetypes

**Understanding common patterns helps evaluate AI-generated ideas**:

**1. Trend Following**
- **Market**: Trending markets (strong directional movement)
- **Logic**: Enter in direction of trend, ride momentum
- **Indicators**: Moving averages (EMA, SMA), ADX, MACD
- **Risk**: False breakouts, whipsaws in ranging markets
- **Example**: "Buy when price crosses above 50 EMA and ADX >25"

**2. Mean Reversion**
- **Market**: Ranging markets (price oscillates around mean)
- **Logic**: Buy oversold, sell overbought, profit from reversion
- **Indicators**: RSI, Bollinger Bands, Stochastic
- **Risk**: Trending markets (price may not revert)
- **Example**: "Buy when RSI <30 and at lower Bollinger Band"

**3. Breakout**
- **Market**: Consolidation followed by expansion
- **Logic**: Enter when price breaks support/resistance with volume
- **Indicators**: Bollinger Bands, ATR, Volume, Donchian Channels
- **Risk**: False breakouts, low win rate (requires large profit factor)
- **Example**: "Buy on breakout above 20-day high with volume >1.5× average"

**4. Momentum**
- **Market**: Strong directional moves
- **Logic**: Enter when momentum accelerates, exit when it fades
- **Indicators**: MACD, Stochastic, Rate of Change (ROC), Williams %R
- **Risk**: Late entries, momentum reversals
- **Example**: "Buy when MACD crosses above signal line and price makes new high"

**5. Arbitrage/Market Making**
- **Market**: Any (exploits inefficiencies or spreads)
- **Logic**: Profit from price discrepancies or spread capture
- **Indicators**: Spread analysis, correlation, volume
- **Risk**: Low margins, requires high frequency, execution risk
- **Example**: "Capture spread between related assets or maker/taker fees"

### Realistic Performance Expectations

**Set realistic expectations to evaluate generated ideas**:

**Sharpe Ratio** (risk-adjusted return):
- **>2.0**: Exceptional (rare for algorithmic strategies)
- **1.0-2.0**: Good (achievable with solid strategy)
- **0.5-1.0**: Acceptable (worth testing)
- **<0.5**: Poor (likely not profitable after costs)

**Max Drawdown** (largest peak-to-trough decline):
- **<10%**: Conservative (lower returns, safer)
- **10-20%**: Moderate (balanced risk/reward)
- **20-40%**: Aggressive (higher returns, higher risk)
- **>40%**: Very risky (difficult to recover from)

**Win Rate** (percentage of profitable trades):
- **45-65%**: Realistic for most strategies
- **>70%**: Suspicious (likely overfitting or unrealistic assumptions)
- **<40%**: Needs improvement or higher profit factor

**Typical characteristics of good strategies**:
- Clear entry and exit rules (not ambiguous)
- Realistic indicator parameters (not over-optimized)
- Appropriate for market regime (trend-following in trending markets)
- Risk management included (stop loss, position sizing)
- Based on sound trading principles (not curve-fitted)

### Market Regime Awareness

**Different strategies work in different market conditions**:

**Trending Markets** (strong directional movement):
- **Best**: Trend following, momentum strategies
- **Worst**: Mean reversion (buys dips that keep dipping)
- **Current state**: Check BTC/ETH price action (making new highs/lows?)

**Ranging Markets** (sideways price action):
- **Best**: Mean reversion, oscillator-based strategies
- **Worst**: Trend following (whipsawed by false signals)
- **Current state**: Price oscillating between clear support/resistance?

**Volatile Markets** (large price swings):
- **Best**: Breakout strategies, volatility-based position sizing
- **Worst**: Tight stop losses (get stopped out frequently)
- **Current state**: ATR elevated? Wide intraday ranges?

**Low Volatility Markets** (compressed ranges):
- **Best**: Range trading, spread capture
- **Worst**: Momentum strategies (insufficient movement)
- **Current state**: ATR compressed? Narrow ranges?

**How generate_ideas uses market data**:
- Analyzes current Hyperliquid market data
- Considers recent volatility, trends, and patterns
- Generates ideas appropriate for current conditions
- You should still validate ideas against your own market view

## Best Practices

### Cost Optimization

**Why use generate_ideas before create_strategy**:

```
Without generate_ideas:
1. create_strategy("vague idea") → $2.50
2. Code doesn't match expectations → Wasted
3. create_strategy("try again") → $2.50
4. Still not quite right → Wasted
Total cost: $5.00, no strategy yet

With generate_ideas:
1. generate_ideas(strategy_count=3) → $0.30
2. Review 3 concepts, pick best
3. create_strategy("refined concept from idea #2") → $2.50
4. Code matches expectations → Success
Total cost: $2.80, working strategy
```

**Savings: $2.20 (44% reduction) + better outcome**

### Effective Idea Generation

**Request multiple ideas to compare approaches**:
```
generate_ideas(strategy_count=3-5)
```

**Why 3-5 ideas**:
- See multiple approaches to same problem
- Compare trade-offs (risk vs return, complexity vs simplicity)
- Identify common themes (e.g., all ideas use RSI → probably important)
- Cost is still minimal ($0.15-$0.50 total)

**Avoid**:
- `strategy_count=1`: Limited perspective, may miss better approaches
- `strategy_count=10`: Diminishing returns, most ideas will be variations

### Critical Evaluation of AI Ideas

**Not all AI-generated ideas are good. Evaluate critically**:

**Red flags** (be skeptical of these):
- **Unrealistic parameters**: "Buy when RSI exactly equals 27.6" (over-optimized)
- **Too many indicators**: Uses 8+ indicators (overfitting risk)
- **Vague logic**: "Enter when conditions are favorable" (not actionable)
- **No risk management**: Doesn't mention stop loss or position sizing
- **Ignores market regime**: Mean reversion strategy for strongly trending market
- **Contradictory logic**: "Buy when RSI <30 AND RSI >70" (impossible)

**Green flags** (good ideas have these):
- **Clear entry conditions**: Specific, measurable criteria
- **Clear exit conditions**: Defined profit target and stop loss
- **Appropriate indicators**: 2-4 indicators that complement each other
- **Market regime awareness**: Strategy matches current conditions
- **Risk management**: Position sizing and stop loss defined
- **Sound rationale**: Based on trading principles, not curve-fitting

**Example evaluation**:
```
Idea: "Buy when price is above 200 EMA, RSI crosses above 50, and MACD crosses bullish"
✓ Clear entry conditions (3 specific criteria)
✓ Indicators complement each other (trend + momentum + momentum confirmation)
✓ Appropriate for trending markets
? Missing exit logic (need to ask for refinement)
? No position sizing mentioned (need to specify)

Verdict: Good foundation, needs exit logic and risk management details
```

### Iterative Refinement

**Use ideas as starting points, not final solutions**:

```
1. generate_ideas(strategy_count=3) → Get initial concepts

2. Evaluate ideas:
   - Idea #1: Too complex (8 indicators)
   - Idea #2: Good concept, but missing exit logic
   - Idea #3: Too risky (no stop loss)

3. Pick best idea (#2) and refine:
   - Use browse-robonet-data to verify indicators available
   - Add missing details (exit logic, risk management)
   - Create refined concept description

4. Proceed to build-trading-strategies:
   - Use refined concept as input
   - Get working code on first try
```

### Exploring Different Markets

**Generate ideas for specific symbols or timeframes**:

```
# First, check available symbols
(Use browse-robonet-data skill)
get_all_symbols()
get_data_availability(symbols=["BTC-USDT", "ETH-USDT"], only_with_data=true)

# Generate ideas (generate_ideas pulls current market data automatically)
generate_ideas(strategy_count=3)

# AI will analyze current market conditions and propose strategies
```

**Note**: `generate_ideas` automatically analyzes current Hyperliquid market data. You don't need to specify symbol or timeframe—it considers the current market environment.

## Common Workflows

### Workflow 1: Exploring New Market

**Goal**: Generate ideas for trading a new asset

```
1. Browse available assets (use browse-robonet-data skill):
   get_all_symbols() → See what's available
   get_data_availability(symbols=["SOL-USDT"]) → Check history

2. Generate ideas:
   generate_ideas(strategy_count=3) → Get 3 concepts

3. Evaluate ideas:
   - Which idea fits current market regime?
   - Which idea has clearest logic?
   - Which idea has best risk/reward?

4. Select best idea:
   - Pick idea with clearest logic and appropriate risk

5. Build strategy (use build-trading-strategies skill):
   - Use selected idea as description input
   - Get working code in one attempt
```

**Cost**: ~$0.20-$0.50

### Workflow 2: Brainstorming Session

**Goal**: Explore multiple approaches before committing to development

```
1. Generate initial batch:
   generate_ideas(strategy_count=5) → Get 5 diverse concepts

2. Group ideas by type:
   - Trend following: Ideas #1, #3
   - Mean reversion: Ideas #2, #4
   - Breakout: Idea #5

3. Compare approaches:
   - Trend following: Higher win rate but slower trades
   - Mean reversion: More trades but lower win rate
   - Breakout: Highest risk/reward but lowest frequency

4. Choose based on goals:
   - Want frequent trades? → Mean reversion
   - Want high win rate? → Trend following
   - Want big winners? → Breakout

5. Proceed to development:
   - Build chosen strategy type
   - Test thoroughly before deployment
```

**Cost**: ~$0.30-$0.70

### Workflow 3: Validating Your Own Idea

**Goal**: See if your strategy concept is viable before building

```
1. You have an idea:
   "I want to trade BTC mean reversion using RSI"

2. Generate AI ideas:
   generate_ideas(strategy_count=3) → See what AI suggests

3. Compare:
   - Do any AI ideas match your concept?
   - What do AI ideas do differently?
   - Are there obvious flaws in your idea that AI avoids?

4. Refine your idea:
   - Incorporate AI insights
   - Add missing details (exit logic, risk management)
   - Validate indicator selection

5. Build refined strategy:
   - Use your idea + AI insights as input
   - Proceed to build-trading-strategies skill
```

**Cost**: ~$0.15-$0.40

### Workflow 4: Market Regime Analysis

**Goal**: Understand what strategies work in current market

```
1. Generate ideas (AI analyzes current market automatically):
   generate_ideas(strategy_count=5)

2. Identify patterns in generated ideas:
   - All ideas trend-following? → Market is trending
   - All ideas mean-reversion? → Market is ranging
   - Mix of approaches? → Mixed/transitional market

3. Use insights to guide strategy selection:
   - Build strategy aligned with current regime
   - Be aware of regime change risk
   - Consider multi-regime strategies

4. Proceed to development:
   - Build strategy appropriate for current market
```

**Cost**: ~$0.30-$0.70

## Advanced Usage

### Combining with Browse Data

**Optimal workflow for thorough exploration**:

```
1. Browse data first (use browse-robonet-data skill):
   get_all_symbols() → Available assets
   get_all_technical_indicators(category="momentum") → Indicators
   get_allora_topics() → ML predictions available

2. Generate ideas:
   generate_ideas(strategy_count=4) → AI concepts

3. Cross-reference:
   - Do generated ideas use available indicators?
   - Can I enhance with Allora ML (check topics)?
   - Do I have sufficient data history?

4. Select idea that aligns with:
   - Available data
   - Available indicators
   - ML prediction coverage

5. Build with confidence:
   - All resources verified
   - No surprises during development
```

### Extracting Patterns Across Ideas

**Learn from multiple idea generations**:

```
Generate ideas multiple times and track patterns:
- Session 1: generate_ideas(strategy_count=3) → Uses EMA, RSI, MACD
- Session 2: generate_ideas(strategy_count=3) → Uses EMA, ATR, Bollinger
- Session 3: generate_ideas(strategy_count=3) → Uses EMA, Volume, ADX

Pattern identified: EMA appears in 9/9 ideas → Fundamental indicator
→ Include EMA in your custom strategy design
```

## Troubleshooting

### "Generated Ideas Are Too Generic"

**Issue**: Ideas lack specific details or actionable logic

**Solutions**:
- This is expected—ideas are concepts, not complete strategies
- Use ideas as starting points, not final solutions
- Refine the best idea and use it as input to `build-trading-strategies`
- Ideas are meant to inspire, not to be implemented directly

### "Ideas Don't Match My Market View"

**Issue**: AI generates trend-following ideas but you think market is ranging

**Solutions**:
- AI analyzes current data, but markets change
- Use ideas for inspiration, not gospel
- Modify concept to match your view
- Generate new ideas and select one that aligns better
- Remember: You have final say, AI provides suggestions

### "All Ideas Look Similar"

**Issue**: 5 ideas generated but they're all variations of same approach

**Solutions**:
- This can happen if market regime is very clear (strong trend → all trend-following)
- Try generating another batch (different ideas each time)
- If pattern persists, market may strongly favor one approach
- Consider building the repeated strategy type (market is telegraphing opportunity)

### "Ideas Use Indicators I Don't Understand"

**Issue**: AI suggests indicators you're unfamiliar with

**Solutions**:
- Use `browse-robonet-data` skill: `get_all_technical_indicators()` to see all indicators
- Research indicator (Google "ADX indicator trading" for examples)
- Ask AI to explain indicator in strategy description when building
- Choose ideas with familiar indicators if uncomfortable

## Next Steps

After generating and evaluating ideas:

**Build the strategy**:
- Use `build-trading-strategies` skill to transform concept into code
- Cost: $1.00-$4.50 per strategy
- Provide refined idea description as input
- Get complete Python strategy code

**Test the strategy**:
- Use `test-trading-strategies` skill to backtest generated ideas
- Cost: $0.001 per backtest
- Validate performance before committing to expensive development

**Improve the strategy**:
- If you already have a strategy and want to refine it
- Use `improve-trading-strategies` skill
- Cost: $0.50-$4.00 per operation

**Deploy to production**:
- After thorough testing shows strong performance
- Use `deploy-live-trading` skill (HIGH RISK)
- Cost: $0.50 deployment fee
- NEVER deploy without extensive backtesting

## Summary

This skill provides **cheap AI-powered strategy ideation** before expensive development:

- **1 tool**: `generate_ideas` (1-10 concepts per call)
- **Cost**: $0.05-$1.00 (significantly cheaper than building $1-$4.50)
- **Execution**: 20-40 seconds
- **Purpose**: Explore concepts, validate ideas, get inspiration

**Core principle**: Spend $0.30 exploring 3 ideas before spending $3.00 building. This saves money and improves outcomes.

**Best practice**: Browse data first (browse-robonet-data), generate ideas (this skill), then build best idea (build-trading-strategies). This workflow minimizes waste and maximizes success rate.

**Remember**: AI-generated ideas are starting points, not final solutions. Evaluate critically, refine, and validate before building.
