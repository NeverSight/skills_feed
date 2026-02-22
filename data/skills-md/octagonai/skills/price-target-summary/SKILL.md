---
name: price-target-summary
description: Retrieve analysts' price target summary for any stock using Octagon MCP. Use when evaluating analyst sentiment, upside/downside potential, consensus expectations, and tracking target trends over time.
---

# Price Target Summary

Retrieve aggregated analyst price target data across multiple timeframes using the Octagon MCP server.

## Prerequisites

Ensure Octagon MCP is configured in your AI agent (Cursor, Claude Desktop, Windsurf, etc.). See [references/mcp-setup.md](references/mcp-setup.md) for installation instructions.

## Workflow

### 1. Identify the Stock

Determine the ticker symbol for the company you want to analyze (e.g., AAPL, MSFT, GOOGL).

### 2. Execute Query via Octagon MCP

Use the `octagon-agent` tool with a natural language prompt:

```
Retrieve the analysts' price-target summary for the stock symbol <TICKER>.
```

**MCP Call Format:**

```json
{
  "server": "octagon-mcp",
  "toolName": "octagon-agent",
  "arguments": {
    "prompt": "Retrieve the analysts' price-target summary for the stock symbol AAPL."
  }
}
```

### 3. Expected Output

The agent returns price target data across timeframes:

| Timeframe | Number of Analysts | Average Price Target |
|-----------|-------------------|---------------------|
| Last Month | 9 | $305.72 |
| Last Quarter | 16 | $312.80 |
| Last Year | 48 | $282.91 |
| All Time | 229 | $219.71 |

**Key Insights**: Trend analysis comparing timeframes

**Data Sources**: octagon-stock-data-agent (aggregating StreetInsider, TheFly, Benzinga, etc.)

### 4. Interpret Results

See [references/interpreting-results.md](references/interpreting-results.md) for guidance on:
- Analyzing target trends
- Calculating upside/downside potential
- Understanding analyst coverage
- Evaluating consensus strength

## Example Queries

**Basic Query:**
```
Retrieve the analysts' price-target summary for the stock symbol AAPL.
```

**With Current Price Context:**
```
What are the analyst price targets for TSLA compared to its current price?
```

**Trend Focus:**
```
How have analyst price targets for NVDA changed over the past year?
```

**Coverage Analysis:**
```
How many analysts cover Microsoft and what are their price targets?
```

**Range Request:**
```
What are the highest and lowest analyst price targets for AMZN?
```

## Understanding Price Targets

### What Price Targets Represent

| Aspect | Description |
|--------|-------------|
| Definition | Analyst's expected stock price |
| Timeframe | Typically 12 months forward |
| Basis | Fundamental and technical analysis |
| Purpose | Guide for fair value |

### Types of Price Targets

| Type | Description |
|------|-------------|
| Average | Mean of all targets |
| Median | Middle value |
| High | Most bullish target |
| Low | Most bearish target |
| Consensus | Weighted average |

## Timeframe Analysis

### Understanding Timeframes

| Timeframe | What It Shows |
|-----------|---------------|
| Last Month | Most recent sentiment |
| Last Quarter | Near-term trend |
| Last Year | Annual evolution |
| All Time | Historical context |

### Trend Interpretation

| Pattern | Interpretation |
|---------|----------------|
| Rising targets | Growing optimism |
| Falling targets | Increasing concern |
| Stable targets | Consensus maintained |
| Diverging targets | Uncertainty/debate |

## Calculating Potential

### Upside/Downside

```
Upside = (Target Price - Current Price) / Current Price × 100%
```

### Example Calculation

- Current Price: $270.01
- Average Target: $312.80
- Upside: ($312.80 - $270.01) / $270.01 = 15.8%

### Interpreting Potential

| Upside | Interpretation |
|--------|----------------|
| >20% | Significant upside expected |
| 10-20% | Moderate upside |
| 0-10% | Near fair value |
| <0% | Downside risk |

## Analyst Coverage

### Coverage Levels

| Analysts | Coverage Level |
|----------|----------------|
| 30+ | Heavily covered |
| 15-30 | Well covered |
| 5-15 | Moderate coverage |
| <5 | Limited coverage |

### Coverage Implications

| Level | Characteristics |
|-------|-----------------|
| Heavy | More consensus reliability |
| Moderate | Good perspective diversity |
| Light | Less reliable consensus |
| Minimal | Limited institutional interest |

## Consensus Strength

### Evaluating Consensus

| Factor | Strong Consensus | Weak Consensus |
|--------|------------------|----------------|
| Range | Tight (low to high) | Wide spread |
| Recent Changes | Aligned direction | Mixed revisions |
| Analyst Count | Many participants | Few analysts |

### Standard Deviation

| Spread | Interpretation |
|--------|----------------|
| Narrow | High agreement |
| Moderate | Normal debate |
| Wide | Significant disagreement |

## Target Revisions

### Revision Trends

| Pattern | Signal |
|---------|--------|
| Upgrades increasing | Improving outlook |
| Downgrades increasing | Deteriorating outlook |
| Mixed revisions | Uncertainty |
| No changes | Status quo |

### Revision Triggers

| Catalyst | Common Result |
|----------|---------------|
| Strong earnings | Target increases |
| Weak earnings | Target decreases |
| Guidance change | Aligned revision |
| Sector news | Coordinated moves |

## Data Sources

### Common Publishers

| Source | Description |
|--------|-------------|
| StreetInsider | Financial news aggregator |
| TheFly | Real-time news |
| Benzinga | Market intelligence |
| Sell-side Firms | Investment bank research |

### Source Considerations

| Factor | Note |
|--------|------|
| Timeliness | Recent targets more relevant |
| Reputation | Weight by analyst track record |
| Conflicts | Consider investment banking ties |
| Methodology | Different valuation approaches |

## Common Use Cases

### Investment Decision
```
Should I buy AAPL based on analyst targets?
```

### Valuation Check
```
Is MSFT overvalued relative to analyst expectations?
```

### Sentiment Tracking
```
How has analyst sentiment on GOOGL changed this year?
```

### Peer Comparison
```
Compare analyst targets for major cloud stocks.
```

## Analysis Tips

1. **Compare to current price**: Calculate upside/downside potential.

2. **Track trend direction**: Rising or falling targets over time.

3. **Consider coverage**: More analysts = more reliable consensus.

4. **Check range**: Tight = agreement, wide = uncertainty.

5. **Time weight**: Recent targets more relevant.

6. **Use with fundamentals**: Targets are opinions, not facts.

## Integration with Other Skills

| Skill | Combined Use |
|-------|--------------|
| stock-quote | Current price vs. target |
| analyst-estimates | Targets + earnings expectations |
| income-statement | Fundamentals behind targets |
| stock-performance | Price trend vs. target evolution |
