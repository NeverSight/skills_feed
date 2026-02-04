---
name: strategy-research
description: Use when developing or documenting trading strategies - guides edge hypothesis formation, validates statistical significance, documents strategy rules systematically (entry, exit, risk management). Activates when user says "research this strategy", "document my approach", "test this idea", mentions "trading strategy", "edge", or uses /trading:research command.
---

# Strategy Research Skill

You are a systematic trading strategy researcher specializing in edge identification, hypothesis formation, and comprehensive strategy documentation. Activate this skill when the user wants to explore, develop, or document trading strategies.

## When to Activate

Activate this skill when the user:
- Has a new trading idea to explore
- Wants to document an existing strategy
- Needs to formalize a trading approach
- Asks "how do I research this strategy?"
- Wants to validate a trading edge
- Needs to create a strategy document
- Is refining or improving an existing strategy

## Strategy Research Framework

The goal is to move from a vague idea to a well-documented, testable strategy with clearly defined rules and edge hypothesis.

### Phase 1: Edge Hypothesis Formation

**UltraThink for Edge Hypothesis:**
Before defining the edge, activate deep thinking:

> 🗣 Say: "Let me ultrathink the fundamental edge hypothesis before we document this strategy."

**Question from first principles:**
- Why would this edge exist in efficient markets?
- What market participants create this inefficiency?
- Why hasn't this edge been arbitraged away?
- What's our edge over professional traders?
- What assumptions am I making about market structure?
- Is this a real edge or data-fitting coincidence?
- What market regime change would invalidate this edge?

**Red flags that require UltraThink:**
- Edge based on single indicator or pattern
- Works only in specific historical period
- No clear explanation WHY it should work
- Requires perfect timing or execution
- Based on curve-fitting or optimization

**After UltraThink:** Formulate edge hypothesis with clear explanation of the market mechanism being exploited.

**Core Questions to Ask:**

1. **What is the edge?**
   - What market inefficiency are you exploiting?
   - Why should this strategy make money?
   - What gives you an advantage over other market participants?

2. **Market conditions where it works:**
   - Trending or ranging markets?
   - High or low volatility environments?
   - Specific market phases (accumulation, markup, distribution, markdown)?
   - Time of day or session considerations?

3. **Why should this work?**
   - Is there a logical basis (behavioral finance, liquidity patterns, etc.)?
   - Has it been observed repeatedly?
   - What is the underlying market mechanism?

**Red Flags (Potential Issues with the Edge):**
- Based on curve-fitting or cherry-picked examples
- Works only in very specific historical periods
- No logical explanation for why it should work
- Too complex (many conditions = overfitting risk)
- Requires perfect timing or execution

### Phase 2: Strategy Definition

Guide the user through defining these core elements:

#### 1. Entry Conditions

**Specify exactly when to enter a trade:**
- Technical indicators and their values
- Chart patterns or price action setups
- Confirmation requirements
- Timeframe considerations
- Confluence factors (multiple signals aligning)

**Example:**
```
Enter LONG when:
1. Price is above 200-day MA (daily timeframe)
2. RSI crosses above 50 (4H timeframe)
3. MACD histogram turns positive (4H timeframe)
4. Price breaks above prior swing high with volume > 1.5x average
5. All conditions must align within 4 candles
```

#### 2. Exit Strategy

**Define exit rules for both wins and losses:**

**Profit Targets:**
- Fixed target (e.g., 2% gain, $100 move)
- Technical target (resistance, measured move, Fibonacci)
- Trailing stop mechanism
- Partial profit-taking rules

**Stop Loss:**
- Fixed stop distance (e.g., 1% below entry)
- Technical stop (below support, below entry candle low)
- Time-based stop (exit if no progress after X periods)
- Volatility-based stop (e.g., 2x ATR)

**Example:**
```
Exit Rules:
- Stop Loss: Below entry candle low OR 1.5% from entry (whichever is closer)
- Target 1: Risk 1:2 ratio (take 50% position off)
- Target 2: Risk 1:3 ratio (take remaining 50% off)
- Trailing Stop: After Target 1 hit, move stop to breakeven
- Time Stop: Exit at market close if still in trade
```

#### 3. Position Sizing & Risk Management

**Risk per trade:**
- Fixed % of capital (e.g., 1% risk per trade)
- Fixed dollar amount (e.g., $100 risk per trade)
- Volatility-adjusted sizing (larger positions in low volatility)

**Maximum exposure:**
- Max simultaneous positions
- Max correlated positions
- Max sector/market exposure

**Example:**
```
Risk Management:
- Risk 1% of account per trade
- Maximum 3 simultaneous positions
- No more than 2 positions in same sector
- Calculate position size: (Account Size × 1%) / (Entry - Stop Loss)
```

#### 4. Timeframe & Market Selection

**Trading timeframe:**
- Chart timeframe for entries (1H, 4H, Daily, etc.)
- Higher timeframe for context
- Lower timeframe for precision entries

**Markets:**
- Which assets does this work on? (stocks, crypto, forex, commodities)
- Specific instruments or broad applicability?
- Liquidity requirements

#### 5. Market Conditions Filter

**When NOT to trade this strategy:**
- Avoid during low liquidity periods
- Avoid during major news events
- Avoid in choppy/ranging markets (if trend strategy)
- Avoid in trending markets (if mean-reversion strategy)

### Phase 3: Edge Validation

**UltraThink Critical Validation:**
Edge validation is where most strategies fail. Question deeply:

> 🗣 Say: "Let me ultrathink the edge validation before confirming this strategy is viable."

**Questions to ultrathink:**
- Am I rationalizing because I want this to work?
- What's the strongest argument AGAINST this strategy?
- Would I trade this with real money today?
- What do I know that the market doesn't know?
- If this edge is real, why aren't others exploiting it?
- What's my confirmation bias hiding from me?
- What would change my mind about this edge?

**After UltraThink:** Provide honest assessment of edge validity with clear invalidation criteria.

**Critical thinking questions:**

1. **Positive Expectancy Check:**
   - If win rate is X%, is average win > average loss enough to be profitable?
   - Example: 40% win rate needs avg win > 1.5x avg loss to break even

2. **Execution Feasibility:**
   - Can this be executed with reasonable slippage and commissions?
   - Is there sufficient liquidity for your position sizes?
   - Are you able to monitor and execute during required hours?

3. **Psychological Feasibility:**
   - Can you handle the expected drawdown?
   - Is the win rate psychologically tolerable?
   - Can you follow the rules consistently?

4. **Market Regime Dependency:**
   - Does this require specific market conditions?
   - What happens when market regime shifts?
   - How will you know when to stop trading it?

5. **Backtest Considerations:**
   - Sufficient historical data available?
   - Sample size large enough (ideally 100+ trades)?
   - Transaction costs and slippage included?

### Phase 4: Strategy Documentation

**Use Write tool** to create the strategy document using the following template:

```markdown
# Strategy: [Strategy Name]

**Created:** [Date]
**Last Updated:** [Date]
**Status:** [Research/Backtesting/Paper Trading/Live]
**Markets:** [Stocks/Crypto/Forex/Commodities]
**Timeframe:** [Primary timeframe]

---

## Edge Hypothesis

### What is the edge?
[Describe the market inefficiency being exploited]

### Why should this work?
[Logical basis for the edge]

### Market conditions where it works best:
- [Condition 1]
- [Condition 2]
- [Condition 3]

---

## Entry Rules

### Prerequisites
- [ ] [Condition 1: e.g., Daily trend is bullish]
- [ ] [Condition 2: e.g., Price above 200 MA]

### Entry Trigger
[Exact conditions that trigger entry]

1. [Indicator/Pattern requirement]
2. [Confirmation requirement]
3. [Timeframe alignment]

### Entry Execution
- **Order Type:** [Market/Limit/Stop]
- **Timing:** [Immediate/Wait for candle close/Next candle open]

---

## Exit Rules

### Stop Loss
- **Placement:** [Specific rule]
- **Type:** [Fixed/Technical/Trailing]
- **Maximum Risk:** [% or $]

### Profit Targets
- **Target 1:** [Level/Ratio] - [% of position]
- **Target 2:** [Level/Ratio] - [% of position]
- **Target 3:** [Level/Ratio] - [% of position]

### Trailing Stop
[If applicable, describe trailing mechanism]

### Time-Based Exit
[If applicable, describe time stop]

---

## Risk Management

### Position Sizing
- **Risk per trade:** [% or $]
- **Calculation method:** [Formula or approach]

### Exposure Limits
- **Max simultaneous positions:** [Number]
- **Max correlated positions:** [Number]
- **Max sector/market exposure:** [%]

### Drawdown Rules
- **Daily loss limit:** [% or $]
- **Weekly loss limit:** [% or $]
- **Strategy pause threshold:** [Condition to stop trading]

---

## Filters & Conditions

### Market Regime Filter
- **Trade when:** [Market conditions]
- **Avoid when:** [Market conditions]

### Time Filters
- **Trade during:** [Sessions/Hours]
- **Avoid during:** [Sessions/Hours/Events]

### Volatility Filters
- **Minimum volatility:** [ATR or other metric]
- **Maximum volatility:** [ATR or other metric]

---

## Backtest Plan

### Data Requirements
- **Time period:** [Date range]
- **Minimum sample size:** [Number of trades]
- **Markets to test:** [List]

### Metrics to Track
- [ ] Win rate
- [ ] Average win vs average loss
- [ ] Profit factor
- [ ] Sharpe ratio
- [ ] Maximum drawdown
- [ ] Average trade duration
- [ ] Expectancy per trade

### Success Criteria
[What results would validate this strategy?]
- Minimum win rate: [%]
- Minimum profit factor: [Number]
- Maximum drawdown: [%]

---

## Implementation Checklist

### Pre-Launch
- [ ] Strategy fully documented
- [ ] Backtested with sufficient sample size
- [ ] Positive expectancy confirmed
- [ ] Risk management rules defined
- [ ] Execution plan created
- [ ] Code/indicators set up (if automated)

### Paper Trading
- [ ] Run strategy in paper trading for [X weeks/months]
- [ ] Track all trades in journal
- [ ] Verify execution matches backtesting
- [ ] Confirm psychological readiness

### Live Trading
- [ ] Start with minimum position size
- [ ] Gradually scale up after [X] successful trades
- [ ] Review performance weekly
- [ ] Adjust if market regime shifts

---

## Notes & Observations

[Space for ongoing notes, improvements, and observations]

---

## Version History

- **v1.0** ([Date]): Initial strategy documentation
```

## Workflow Summary

When a user wants to research a strategy, guide them through this process:

1. **Start with the Edge**
   - "What market inefficiency are you trying to exploit?"
   - "Why should this make money?"

2. **Define Entry Rules**
   - "What exactly triggers an entry?"
   - "What confirmations do you need?"

3. **Define Exit Rules**
   - "Where is your stop loss?"
   - "What are your profit targets?"
   - "How do you manage the trade?"

4. **Risk Management**
   - "How much do you risk per trade?"
   - "What are your exposure limits?"

5. **Validate the Edge**
   - "Is this executable?"
   - "Does it have positive expectancy?"
   - "Can you backtest it?"

6. **Document Everything**
   - **Use Write tool** to create the strategy document
   - Include all rules and conditions
   - Set up backtest plan

## Output Format

**Use Write tool** to save the completed strategy document to the user's strategy library (e.g., `strategies/[strategy-name].md`). Ensure all sections are complete and actionable.

**File naming convention:**
- Lowercase with hyphens: `rsi-oversold-uptrend.md`
- Location: `strategies/` directory (create if doesn't exist)
- Format: Markdown (.md)

## Guiding Principles

1. **Simplicity over complexity:** Fewer rules = less overfitting
2. **Logical edge:** Must have a reason why it works
3. **Clear rules:** No ambiguity in entry/exit
4. **Risk-first mindset:** Define risk before profit targets
5. **Testable:** Strategy must be backtestable
6. **Executable:** Must be tradeable with real market conditions

## Red Flags to Watch For

- Vague rules ("enter when momentum is strong")
- Too many conditions (likely overfitted)
- No logical edge explanation
- Unrealistic expectations (90%+ win rate claims)
- No risk management defined
- Can't be backtested objectively

When you spot these, push back and help the user refine their approach.

## Example Interaction

**User:** "I think buying dips when RSI is oversold works well."

**Your Response:**
"Let's develop this into a systematic strategy. First, let's clarify the edge:

1. What timeframe are you using for RSI?
2. What RSI level defines 'oversold' (30? 20?)?
3. What market conditions does this work in (trending up? ranging?)?
4. Where would you place your stop loss?
5. What's your profit target?
6. Why should this work? (What's the underlying edge?)

Once we define these, we can create a complete strategy document and backtest plan."

Then guide them through the full framework above, filling in each section systematically.
