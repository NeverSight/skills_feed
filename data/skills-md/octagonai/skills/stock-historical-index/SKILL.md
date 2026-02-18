---
name: stock-historical-index
description: Retrieve full historical end-of-day price data for market indices using Octagon MCP. Use when analyzing index performance over time, tracking market trends, calculating returns, and understanding market context for individual stock analysis.
---

# Stock Historical Index

Retrieve full historical end-of-day price data for market indices using the Octagon MCP server.

## Prerequisites

Ensure Octagon MCP is configured in your AI agent (Cursor, Claude Desktop, Windsurf, etc.). See [references/mcp-setup.md](references/mcp-setup.md) for installation instructions.

## Workflow

### 1. Identify Parameters

Determine your query parameters:
- **Index Symbol**: ^GSPC (S&P 500), ^DJI (Dow), ^IXIC (NASDAQ), etc.
- **Start Date**: Beginning of date range
- **End Date**: End of date range

### 2. Execute Query via Octagon MCP

Use the `octagon-agent` tool with a natural language prompt:

```
Retrieve full historical end-of-day price data for the <INDEX> index from <START_DATE> to <END_DATE>.
```

**MCP Call Format:**

```json
{
  "server": "octagon-mcp",
  "toolName": "octagon-agent",
  "arguments": {
    "prompt": "Retrieve full historical end-of-day price data for the ^GSPC index from 2025-01-01 to 2025-04-30."
  }
}
```

### 3. Expected Output

The agent returns comprehensive daily index data:

| Date | Open | High | Low | Close | Volume | Change | Change % | VWAP |
|------|------|------|-----|-------|--------|--------|----------|------|
| 2025-04-30 | 5,499.44 | 5,581.84 | 5,433.24 | 5,569.07 | 5.45B | +69.63 | +1.27% | 5,520.90 |
| 2025-04-29 | 5,508.87 | 5,571.95 | 5,505.70 | 5,560.82 | 4.75B | +51.95 | +0.94% | 5,536.84 |
| ... | ... | ... | ... | ... | ... | ... | ... | ... |

**Key Statistics**:
- Highest single-day volume: 9.49B on 2025-04-09
- Largest daily gain: +9.90% on 2025-04-09
- Largest daily loss: -4.12% on 2025-04-04
- Trading days covered: 79

**Data Sources**: octagon-stock-data-agent

### 4. Interpret Results

See [references/interpreting-results.md](references/interpreting-results.md) for guidance on:
- Analyzing index price trends
- Calculating period returns
- Understanding volume patterns
- Identifying significant market moves

## Example Queries

**S&P 500 History:**
```
Retrieve full historical end-of-day price data for the ^GSPC index from 2025-01-01 to 2025-04-30.
```

**NASDAQ Composite:**
```
Get historical data for ^IXIC from 2024-01-01 to 2024-12-31.
```

**Dow Jones:**
```
Show ^DJI historical prices for Q1 2025.
```

**Russell 2000:**
```
Retrieve historical data for ^RUT from 2024-06-01 to 2025-06-01.
```

**Multiple Indices:**
```
Compare ^GSPC and ^IXIC performance from 2025-01-01 to 2025-03-31.
```

## Common Index Symbols

### US Major Indices

| Symbol | Index | Description |
|--------|-------|-------------|
| ^GSPC | S&P 500 | 500 large-cap US stocks |
| ^DJI | Dow Jones | 30 blue-chip stocks |
| ^IXIC | NASDAQ Composite | All NASDAQ stocks |
| ^NDX | NASDAQ 100 | 100 largest NASDAQ |
| ^RUT | Russell 2000 | 2000 small-cap stocks |

### Sector Indices

| Symbol | Index | Description |
|--------|-------|-------------|
| ^XLK | Technology | Tech sector |
| ^XLF | Financials | Financial sector |
| ^XLV | Healthcare | Healthcare sector |
| ^XLE | Energy | Energy sector |
| ^XLI | Industrials | Industrial sector |

### Volatility Indices

| Symbol | Index | Description |
|--------|-------|-------------|
| ^VIX | VIX | Market volatility |
| ^VXN | VXN | NASDAQ volatility |

## Understanding Index Data

### Price Components

| Field | Description |
|-------|-------------|
| Open | First trade price of day |
| High | Highest price of day |
| Low | Lowest price of day |
| Close | Last trade price of day |
| Volume | Total shares traded |
| Change | Point change from prior close |
| Change % | Percentage change |
| VWAP | Volume-weighted average price |

### Daily Range Analysis

| Metric | Calculation |
|--------|-------------|
| Daily Range | High - Low |
| Range % | (High - Low) / Open |
| Position in Range | (Close - Low) / (High - Low) |

## Return Calculations

### Period Returns

| Period | Formula |
|--------|---------|
| Daily | (Close - Prior Close) / Prior Close |
| Weekly | (Friday Close - Monday Open) / Monday Open |
| Monthly | (Month End - Month Start) / Month Start |
| YTD | (Current - Year Start) / Year Start |

### Example

From the data:
- Start (Jan 2): 5,868.56
- End (Apr 30): 5,569.07
- Return: (5,569.07 - 5,868.56) / 5,868.56 = -5.10%

### Cumulative Returns

```
Cumulative = (1 + r1) × (1 + r2) × ... × (1 + rn) - 1
```

## Volume Analysis

### Volume Patterns

| Pattern | Interpretation |
|---------|----------------|
| High volume + up | Strong buying |
| High volume + down | Strong selling |
| Low volume + up | Weak rally |
| Low volume + down | Lack of sellers |

### Volume Metrics

| Metric | Purpose |
|--------|---------|
| Average daily volume | Baseline |
| Volume spike | Unusual activity |
| Volume trend | Participation changes |

### Example

From the data:
- Highest volume: 9.49B on 2025-04-09
- This coincided with +9.90% gain (major rally)

## Trend Analysis

### Trend Identification

| Pattern | Characteristics |
|---------|-----------------|
| Uptrend | Higher highs, higher lows |
| Downtrend | Lower highs, lower lows |
| Consolidation | Range-bound |
| Reversal | Trend change |

### Moving Averages

| MA | Use |
|----|-----|
| 50-day | Short-term trend |
| 200-day | Long-term trend |
| Golden Cross | 50 > 200 (bullish) |
| Death Cross | 50 < 200 (bearish) |

## Volatility Analysis

### Measuring Volatility

| Metric | Calculation |
|--------|-------------|
| Daily Range % | (High - Low) / Close |
| Daily Change | Absolute daily change |
| Std Deviation | Dispersion of returns |

### Volatility Context

| Daily Change % | Market Condition |
|----------------|------------------|
| <0.5% | Low volatility |
| 0.5-1% | Normal |
| 1-2% | Elevated |
| >2% | High volatility |
| >4% | Extreme |

### Example

From the data:
- Largest gain: +9.90%
- Largest loss: -4.12%
- Range: 14.02%
- **Interpretation**: Period of elevated volatility

## Key Market Events

### Identifying Significant Days

| Criteria | Threshold |
|----------|-----------|
| Big up day | >2% gain |
| Big down day | >2% loss |
| Volume spike | >2x average |
| Range expansion | >2x normal range |

### Event Analysis

| From Data | Event |
|-----------|-------|
| +9.90% on Apr 9 | Major rally |
| -4.12% on Apr 4 | Significant selloff |
| 9.49B volume | Highest participation |

## Benchmarking Use

### Stock vs. Index

| Comparison | Formula |
|------------|---------|
| Alpha | Stock Return - Index Return |
| Beta | Stock Vol / Index Vol × Correlation |
| Relative Strength | Stock / Index |

### Example Use

- Your stock returned +15%
- S&P 500 returned -5.10%
- Alpha: +20.10% outperformance

## Common Use Cases

### Market Context
```
What was the overall market doing when my stock fell?
```

### Return Comparison
```
How did the S&P 500 perform in Q1 2025?
```

### Volatility Assessment
```
What were the biggest up and down days for the market in 2024?
```

### Trend Analysis
```
Is the market in an uptrend or downtrend?
```

### Volume Analysis
```
What were the highest volume days for the S&P 500?
```

## Analysis Tips

1. **Use for context**: Index performance explains stock moves.

2. **Calculate alpha**: Your returns vs. market.

3. **Watch volume**: High volume days are significant.

4. **Track extremes**: Big up/down days signal sentiment.

5. **Compare indices**: Different indices, different signals.

6. **Consider VIX**: Volatility index for fear gauge.

## Integration with Other Skills

| Skill | Combined Use |
|-------|--------------|
| stock-performance | Stock vs. index comparison |
| sector-performance-snapshot | Sector vs. index |
| stock-quote | Current vs. historical |
| historical-market-cap | Market cap vs. index |
