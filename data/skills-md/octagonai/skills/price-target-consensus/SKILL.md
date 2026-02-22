---
name: price-target-consensus
description: Retrieve consensus price targets for any stock using Octagon MCP. Use when you need the average, median, high, and low analyst price targets to evaluate upside/downside potential and analyst agreement.
---

# Price Target Consensus

Retrieve consensus price target metrics including average, median, high, and low targets using the Octagon MCP server.

## Prerequisites

Ensure Octagon MCP is configured in your AI agent (Cursor, Claude Desktop, Windsurf, etc.). See [references/mcp-setup.md](references/mcp-setup.md) for installation instructions.

## Workflow

### 1. Identify the Stock

Determine the ticker symbol for the company you want to analyze (e.g., AAPL, MSFT, GOOGL).

### 2. Execute Query via Octagon MCP

Use the `octagon-agent` tool with a natural language prompt:

```
Retrieve consensus price targets for the stock symbol <TICKER>.
```

**MCP Call Format:**

```json
{
  "server": "octagon-mcp",
  "toolName": "octagon-agent",
  "arguments": {
    "prompt": "Retrieve consensus price targets for the stock symbol AAPL."
  }
}
```

### 3. Expected Output

The agent returns consensus price target data:

| Metric | Value |
|--------|-------|
| Consensus Target | $303.11 |
| Median Target | $315.00 |
| Target High | $350.00 |
| Target Low | $220.00 |

**Data Sources**: octagon-stock-data-agent

### 4. Interpret Results

See [references/interpreting-results.md](references/interpreting-results.md) for guidance on:
- Understanding consensus vs. median
- Analyzing the target range
- Calculating upside/downside
- Evaluating analyst agreement

## Example Queries

**Basic Query:**
```
Retrieve consensus price targets for the stock symbol AAPL.
```

**With Price Context:**
```
What is the consensus price target for TSLA and how does it compare to current price?
```

**Range Focus:**
```
What are the highest and lowest analyst price targets for NVDA?
```

**Comparison:**
```
Compare consensus price targets for AAPL, MSFT, and GOOGL.
```

**Upside Analysis:**
```
What upside does the consensus target imply for AMZN?
```

## Understanding the Metrics

### Consensus Target

| Aspect | Description |
|--------|-------------|
| Definition | Average of all analyst targets |
| Calculation | Sum of targets / Number of analysts |
| Use | General market expectation |
| Limitation | Skewed by outliers |

### Median Target

| Aspect | Description |
|--------|-------------|
| Definition | Middle value of all targets |
| Calculation | 50th percentile |
| Use | Central tendency, outlier-resistant |
| Advantage | Less affected by extremes |

### Target High

| Aspect | Description |
|--------|-------------|
| Definition | Most bullish analyst target |
| Represents | Best-case scenario |
| Use | Maximum upside potential |
| Caution | May be overly optimistic |

### Target Low

| Aspect | Description |
|--------|-------------|
| Definition | Most bearish analyst target |
| Represents | Worst-case scenario |
| Use | Downside risk assessment |
| Caution | May be overly pessimistic |

## Calculating Potential

### Upside/Downside Formulas

```
Consensus Upside = (Consensus Target - Current Price) / Current Price × 100%
Maximum Upside = (Target High - Current Price) / Current Price × 100%
Downside Risk = (Target Low - Current Price) / Current Price × 100%
```

### Example Calculations

If AAPL trades at $270.01:

| Metric | Target | Potential |
|--------|--------|-----------|
| Consensus | $303.11 | +12.3% upside |
| Median | $315.00 | +16.7% upside |
| High | $350.00 | +29.6% upside |
| Low | $220.00 | -18.5% downside |

## Range Analysis

### Spread Calculation

```
Range = Target High - Target Low
Spread % = Range / Consensus Target × 100%
```

### Interpreting Spread

| Spread % | Interpretation |
|----------|----------------|
| <20% | Strong consensus |
| 20-40% | Normal range |
| 40-60% | Moderate disagreement |
| >60% | High uncertainty |

### Example Range Analysis

From AAPL data:
- High: $350.00
- Low: $220.00
- Range: $130.00
- Consensus: $303.11
- Spread: 42.9%

**Interpretation**: Moderate disagreement among analysts, with significant difference between bulls and bears.

## Consensus vs. Median

### When to Use Each

| Scenario | Prefer |
|----------|--------|
| Normal distribution | Consensus (average) |
| Outliers present | Median |
| Skewed targets | Median |
| General expectation | Consensus |

### Identifying Skew

| Condition | Indicates |
|-----------|-----------|
| Consensus > Median | Right skew (bullish outliers) |
| Consensus < Median | Left skew (bearish outliers) |
| Consensus ≈ Median | Symmetric distribution |

### Example

From AAPL data:
- Consensus: $303.11
- Median: $315.00
- Consensus < Median → Left skew (some bearish outliers pulling average down)

## Bull vs. Bear Cases

### Understanding Extremes

| Target | Represents |
|--------|------------|
| High | Bull case assumptions |
| Low | Bear case assumptions |
| Gap | Range of outcomes |

### Scenario Analysis

| Scenario | Assumptions |
|----------|-------------|
| Bull Case | Strong growth, expanding margins, favorable macro |
| Base Case | Consensus expectations |
| Bear Case | Challenges, competition, risks materialize |

## Practical Applications

### Investment Decision

| Finding | Consideration |
|---------|---------------|
| Price < Low Target | Potential deep value or concerns |
| Price near Consensus | Fairly valued |
| Price > High Target | Potentially overvalued |

### Risk Assessment

| Metric | Use For |
|--------|---------|
| Downside to Low | Worst-case loss |
| Upside to High | Best-case gain |
| Risk/Reward | Low upside / High downside |

### Position Sizing

| Consensus View | Position Approach |
|----------------|-------------------|
| Strong upside, tight range | Larger position |
| Moderate upside, wide range | Standard position |
| Limited upside, wide range | Smaller position |

## Common Use Cases

### Quick Valuation Check
```
Is AAPL fairly valued based on analyst targets?
```

### Upside Screening
```
Which tech stocks have the highest consensus upside?
```

### Risk Assessment
```
What's the downside risk to the lowest analyst target for TSLA?
```

### Sentiment Check
```
How wide is the range between bull and bear cases for NVDA?
```

## Analysis Tips

1. **Compare to current price**: Calculate actual upside/downside.

2. **Use median when skewed**: More reliable central tendency.

3. **Analyze the range**: Wide = uncertainty, tight = agreement.

4. **Consider timing**: Targets are typically 12-month forward.

5. **Track changes**: Rising consensus = improving sentiment.

6. **Combine with fundamentals**: Targets are opinions, verify with data.

## Integration with Other Skills

| Skill | Combined Use |
|-------|--------------|
| stock-quote | Current price for potential calculation |
| price-target-summary | Historical target trends |
| analyst-estimates | Earnings behind the targets |
| financial-metrics-analysis | Fundamental validation |
