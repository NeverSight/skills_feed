---
name: industry-performance-snapshot
description: Retrieve a daily overview of industry performance using Octagon MCP. Use when analyzing daily price movements, average changes, and performance trends for specific industries within an exchange.
---

# Industry Performance Snapshot

Retrieve daily industry performance data by exchange using the Octagon MCP server.

## Prerequisites

Ensure Octagon MCP is configured in your AI agent (Cursor, Claude Desktop, Windsurf, etc.). See [references/mcp-setup.md](references/mcp-setup.md) for installation instructions.

## Workflow

### 1. Identify Parameters

Determine your query parameters:
- **Date**: Specific trading date
- **Exchange**: NYSE, NASDAQ, etc.
- **Industry**: Biotechnology, Semiconductors, Software, etc.

### 2. Execute Query via Octagon MCP

Use the `octagon-agent` tool with a natural language prompt:

```
Retrieve a daily overview of industry performance for <DATE>, filtered by exchange <EXCHANGE> and industry <INDUSTRY>.
```

**MCP Call Format:**

```json
{
  "server": "octagon-mcp",
  "toolName": "octagon-agent",
  "arguments": {
    "prompt": "Retrieve a daily overview of industry performance for 2025-01-09, filtered by exchange NASDAQ and industry Biotechnology."
  }
}
```

### 3. Expected Output

The agent returns daily industry performance metrics:

| Metric | Value |
|--------|-------|
| Industry | Biotechnology |
| Exchange | NASDAQ |
| Date | 2025-01-09 |
| Average Change | +7.89% |

**Interpretation**: Strong positive movement in biotechnology stocks on NASDAQ for the specified date.

**Data Sources**: octagon-stock-data-agent

### 4. Interpret Results

See [references/interpreting-results.md](references/interpreting-results.md) for guidance on:
- Evaluating daily performance magnitude
- Comparing industry vs. market moves
- Identifying sector rotation signals
- Tracking momentum trends

## Example Queries

**Specific Industry and Date:**
```
Retrieve a daily overview of industry performance for 2025-01-09, filtered by exchange NASDAQ and industry Biotechnology.
```

**Technology Industry:**
```
Get today's performance for the Semiconductor industry on NASDAQ.
```

**Multiple Industries:**
```
Compare daily performance of Software, Hardware, and Semiconductors on NASDAQ.
```

**Historical Date:**
```
What was the Biotechnology industry performance on the last FDA approval day?
```

**Trend Analysis:**
```
Show industry performance for Healthcare on NYSE over the past week.
```

## Understanding Daily Performance

### What Average Change Represents

| Aspect | Description |
|--------|-------------|
| Definition | Average price change of stocks in industry |
| Calculation | Mean of individual stock returns |
| Weighting | Equal or market-cap weighted |
| Timeframe | Single trading day |

### Performance Levels

| Change | Interpretation |
|--------|----------------|
| >5% | Exceptional (major catalyst) |
| 2-5% | Strong move |
| 0.5-2% | Moderate move |
| -0.5% to +0.5% | Flat |
| -2 to -0.5% | Moderate decline |
| <-5% | Significant decline |

## Industry Categories

### Technology Industries

| Industry | Typical Volatility |
|----------|-------------------|
| Biotechnology | High (clinical trials, FDA) |
| Semiconductors | Moderate-High (cyclical) |
| Software | Moderate |
| IT Services | Low-Moderate |
| Hardware | Moderate |

### Healthcare Industries

| Industry | Typical Volatility |
|----------|-------------------|
| Biotechnology | High |
| Pharmaceuticals | Moderate |
| Medical Devices | Low-Moderate |
| Healthcare Services | Low |

### Financial Industries

| Industry | Typical Volatility |
|----------|-------------------|
| Banks | Moderate (rate-sensitive) |
| Insurance | Low-Moderate |
| Asset Management | Moderate |
| Fintech | Moderate-High |

## Analyzing Performance

### Context Matters

| Factor | Consideration |
|--------|---------------|
| Market direction | Industry vs. S&P 500 |
| Sector performance | Industry vs. sector |
| Historical range | Normal vs. unusual |
| Catalyst presence | News-driven vs. rotation |

### Relative Performance

| Comparison | Insight |
|------------|---------|
| Industry > Market | Outperforming |
| Industry = Market | In-line |
| Industry < Market | Underperforming |

### Alpha Calculation

```
Alpha = Industry Return - Market Return
```

Example:
- Industry: +7.89%
- Market: +0.5%
- Alpha: +7.39% (significant outperformance)

## Catalyst Analysis

### Common Industry Catalysts

| Catalyst | Expected Impact |
|----------|-----------------|
| FDA approval | Biotech +3-10% |
| Earnings season | Varies |
| Rate decision | Financials ±2-5% |
| Product launch | Tech +1-3% |
| Regulatory news | Varies |

### Biotechnology Specifics

| Event | Typical Response |
|-------|------------------|
| Phase 3 success | +5-20% |
| FDA approval | +5-15% |
| Clinical setback | -5-30% |
| M&A announcement | +10-50% |

## Momentum Analysis

### Trend Signals

| Pattern | Interpretation |
|---------|----------------|
| Multiple up days | Positive momentum |
| Multiple down days | Negative momentum |
| Reversal | Potential trend change |
| Range-bound | Consolidation |

### Follow-Through

| Signal | Reliability |
|--------|-------------|
| High volume + strong move | Strong signal |
| Low volume + strong move | Weak signal |
| Continuation next day | Trend confirmation |
| Reversal next day | False move |

## Sector Rotation Signals

### Industry Leadership

| Pattern | Meaning |
|---------|---------|
| Cyclicals leading | Risk-on sentiment |
| Defensives leading | Risk-off sentiment |
| Growth leading | Optimistic outlook |
| Value leading | Cautious approach |

### Rotation Indicators

| Observation | Interpretation |
|-------------|----------------|
| Biotech surging | Speculative appetite |
| Utilities leading | Flight to safety |
| Banks rallying | Rate expectations |
| Tech selling off | Growth concerns |

## Exchange Considerations

### NASDAQ Characteristics

| Factor | Impact |
|--------|--------|
| Tech-heavy | More volatile |
| Growth-oriented | Bigger moves |
| Biotech concentration | FDA-sensitive |

### NYSE Characteristics

| Factor | Impact |
|--------|--------|
| More diversified | Moderate volatility |
| Large-cap focus | Steadier moves |
| Traditional industries | Less speculative |

## Common Use Cases

### Daily Monitoring
```
How did Biotechnology perform today?
```

### Catalyst Research
```
What was the industry reaction to the FDA announcement?
```

### Sector Rotation
```
Which industries are leading the market today?
```

### Historical Analysis
```
What was industry performance during last quarter's earnings season?
```

### Momentum Tracking
```
Is the Semiconductor industry showing positive momentum this week?
```

## Analysis Tips

1. **Compare to market**: Industry move vs. S&P 500/NASDAQ.

2. **Check for catalysts**: News explains unusual moves.

3. **Consider volatility**: Biotech ±5% is normal, utilities ±5% is not.

4. **Track trends**: One day is noise, multiple days is signal.

5. **Volume matters**: High volume confirms moves.

6. **Look at breadth**: How many stocks participated?

## Integration with Other Skills

| Skill | Combined Use |
|-------|--------------|
| sector-performance-snapshot | Broader sector context |
| industry-pe-ratios | Valuation with performance |
| stock-performance | Individual stock details |
| stock-quote | Current prices |
