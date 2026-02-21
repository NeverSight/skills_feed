---
name: historical-market-cap
description: Retrieve historical market capitalization data for any stock using Octagon MCP. Use when tracking market cap changes over time, analyzing valuation trends, identifying peak and trough valuations, and comparing historical size classifications.
---

# Historical Market Cap

Retrieve historical market capitalization data over a specified date range using the Octagon MCP server.

## Prerequisites

Ensure Octagon MCP is configured in your AI agent (Cursor, Claude Desktop, Windsurf, etc.). See [references/mcp-setup.md](references/mcp-setup.md) for installation instructions.

## Workflow

### 1. Identify Parameters

Determine your query parameters:
- **Ticker**: Stock symbol (e.g., AAPL, MSFT)
- **Start Date**: Beginning of date range
- **End Date**: End of date range
- **Limit** (optional): Maximum records to return

### 2. Execute Query via Octagon MCP

Use the `octagon-agent` tool with a natural language prompt:

```
Retrieve historical market capitalization data for <TICKER> from <START_DATE> to <END_DATE>, limited to <LIMIT> records.
```

**MCP Call Format:**

```json
{
  "server": "octagon-mcp",
  "toolName": "octagon-agent",
  "arguments": {
    "prompt": "Retrieve historical market capitalization data for AAPL from 2025-01-01 to 2025-04-30, limited to 1000 records."
  }
}
```

### 3. Expected Output

The agent returns daily market cap values:

| Date | Market Cap (USD) |
|------|------------------|
| 2025-04-30 | $3.17 trillion |
| 2025-02-25 | $3.70 trillion (High) |
| 2025-04-08 | $2.57 trillion (Low) |
| ... | ... |

**Summary Statistics**:
- Highest: $3.70 trillion on 2025-02-25
- Lowest: $2.57 trillion on 2025-04-08
- Most Recent: $3.17 trillion on 2025-04-30

**Data Sources**: octagon-stock-data-agent

### 4. Interpret Results

See [references/interpreting-results.md](references/interpreting-results.md) for guidance on:
- Analyzing market cap trends
- Calculating growth rates
- Identifying peaks and troughs
- Understanding volatility

## Example Queries

**Standard Date Range:**
```
Retrieve historical market capitalization data for AAPL from 2025-01-01 to 2025-04-30, limited to 1000 records.
```

**Full Year:**
```
Get historical market cap for MSFT for the entire year 2024.
```

**Quarterly Analysis:**
```
Show TSLA's market cap history for Q1 2025.
```

**Multi-Year Trend:**
```
Retrieve market cap history for NVDA from 2020 to 2025.
```

**Peak Analysis:**
```
When did AAPL reach its highest market cap in 2024?
```

## Understanding Market Cap History

### What the Data Shows

| Metric | Description |
|--------|-------------|
| Daily Market Cap | End-of-day value |
| Date Series | Trading days only |
| Calculation | Price × Shares Outstanding |
| Adjustments | Split-adjusted shares |

### Key Statistics

| Statistic | Purpose |
|-----------|---------|
| Maximum | Peak valuation |
| Minimum | Trough valuation |
| Average | Typical valuation |
| Range | Volatility indicator |

## Trend Analysis

### Calculating Changes

| Metric | Formula |
|--------|---------|
| Absolute Change | End Cap - Start Cap |
| Percentage Change | (End - Start) / Start × 100% |
| CAGR | (End/Start)^(1/years) - 1 |

### Example Calculation

From the AAPL data:
- High: $3.70T (Feb 25)
- Low: $2.57T (Apr 8)
- Range: $1.13T
- Peak-to-Trough: -30.5%

### Trend Patterns

| Pattern | Characteristics |
|---------|-----------------|
| Uptrend | Higher highs, higher lows |
| Downtrend | Lower highs, lower lows |
| Consolidation | Range-bound |
| V-Recovery | Sharp decline, sharp recovery |
| Rounded Top | Gradual peak formation |

## Period Analysis

### Daily Analysis

| Use Case | Focus |
|----------|-------|
| Trading | Short-term moves |
| Volatility | Day-to-day changes |
| Events | Catalyst impact |

### Weekly/Monthly Analysis

| Use Case | Focus |
|----------|-------|
| Trends | Direction over time |
| Comparisons | Period-over-period |
| Smoothing | Reduce noise |

### Annual Analysis

| Use Case | Focus |
|----------|-------|
| Growth | Long-term trajectory |
| Milestones | Major achievements |
| CAGR | Compound growth |

## Volatility Assessment

### Measuring Volatility

| Metric | Calculation |
|--------|-------------|
| Range | High - Low |
| Range % | (High - Low) / Average |
| Daily Moves | Average daily change |
| Standard Deviation | Price dispersion |

### Volatility Interpretation

| Range % | Volatility |
|---------|------------|
| <20% | Low |
| 20-40% | Moderate |
| 40-60% | High |
| >60% | Very High |

### Example

From AAPL data:
- High: $3.70T
- Low: $2.57T
- Range: $1.13T
- Range %: ~35%
- **Interpretation**: Moderate-high volatility

## Peak and Trough Analysis

### Identifying Peaks

| Signal | Description |
|--------|-------------|
| All-time High | Highest ever |
| Period High | Highest in range |
| Local Peak | Temporary high |

### Identifying Troughs

| Signal | Description |
|--------|-------------|
| All-time Low | Lowest ever |
| Period Low | Lowest in range |
| Local Trough | Temporary low |

### Peak-to-Trough Metrics

| Metric | Purpose |
|--------|---------|
| Drawdown % | Decline from peak |
| Recovery Time | Days to recover |
| Drawdown Duration | Peak to trough time |

## Size Classification Over Time

### Tracking Category Changes

| If Market Cap... | Classification |
|------------------|----------------|
| >$200B | Mega-cap |
| $10B-$200B | Large-cap |
| $2B-$10B | Mid-cap |
| $300M-$2B | Small-cap |

### Milestone Analysis

| Milestone | Significance |
|-----------|--------------|
| First $1T | Historic achievement |
| Crossed $2T | Elite status |
| Crossed $3T | World's most valuable |

## Comparative Analysis

### Same Company Over Time

| Comparison | Purpose |
|------------|---------|
| YoY | Year-over-year growth |
| QoQ | Quarterly momentum |
| MoM | Monthly trends |

### Multiple Companies

| Comparison | Purpose |
|------------|---------|
| Relative Size | Market position |
| Relative Growth | Performance comparison |
| Correlation | Movement similarity |

## Common Use Cases

### Trend Analysis
```
How has AAPL's market cap changed over the past year?
```

### Peak Finding
```
When did TSLA reach its highest market cap?
```

### Drawdown Analysis
```
What was NVDA's biggest decline from peak in 2024?
```

### Milestone Tracking
```
When did MSFT first cross $3 trillion market cap?
```

### Comparison
```
Compare the market cap growth of AAPL and MSFT over 5 years.
```

## Analysis Tips

1. **Use appropriate timeframes**: Match analysis to investment horizon.

2. **Identify catalysts**: Major moves often have drivers.

3. **Consider splits**: Ensure data is split-adjusted.

4. **Watch for milestones**: Round numbers are psychologically important.

5. **Calculate drawdowns**: Understand downside risk.

6. **Compare to benchmarks**: Market cap vs. index performance.

## Integration with Other Skills

| Skill | Combined Use |
|-------|--------------|
| company-market-cap | Current vs. historical |
| stock-performance | Price driving cap changes |
| income-statement | Earnings supporting cap |
| financial-metrics-analysis | Valuation evolution |
