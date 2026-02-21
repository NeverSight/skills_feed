---
name: sector-pe-ratios
description: Retrieve sector P/E ratios using Octagon MCP. Use when comparing company valuations to sector benchmarks, analyzing sector valuations across exchanges, and understanding market-wide valuation trends.
---

# Sector P/E Ratios

Retrieve price-to-earnings ratios by sector and exchange using the Octagon MCP server.

## Prerequisites

Ensure Octagon MCP is configured in your AI agent (Cursor, Claude Desktop, Windsurf, etc.). See [references/mcp-setup.md](references/mcp-setup.md) for installation instructions.

## Workflow

### 1. Identify Parameters

Determine your query parameters:
- **Date**: Specific date for the data
- **Exchange**: NYSE, NASDAQ, etc.
- **Sector**: Technology, Healthcare, Financials, etc.

### 2. Execute Query via Octagon MCP

Use the `octagon-agent` tool with a natural language prompt:

```
Retrieve the latest sector P/E ratios for <DATE>, filtered by exchange <EXCHANGE> and sector <SECTOR>.
```

**MCP Call Format:**

```json
{
  "server": "octagon-mcp",
  "toolName": "octagon-agent",
  "arguments": {
    "prompt": "Retrieve the latest sector P/E ratios for 2025-02-03, filtered by exchange NASDAQ and sector Technology."
  }
}
```

### 3. Expected Output

The agent returns sector P/E data:

| Metric | Value |
|--------|-------|
| Sector | Technology |
| Exchange | NASDAQ |
| P/E Ratio | 58.77 |
| Date | 2025-02-03 |

**Data Sources**: octagon-stock-data-agent

### 4. Interpret Results

See [references/interpreting-results.md](references/interpreting-results.md) for guidance on:
- Comparing company P/E to sector P/E
- Historical sector valuation context
- Cross-sector comparisons
- Exchange-specific analysis

## Example Queries

**Specific Sector and Exchange:**
```
Retrieve the latest sector P/E ratios for 2025-02-03, filtered by exchange NASDAQ and sector Technology.
```

**All Sectors on Exchange:**
```
Get P/E ratios for all sectors on the NYSE.
```

**Sector Comparison:**
```
Compare P/E ratios for Technology, Healthcare, and Financials sectors.
```

**Historical Trend:**
```
What is the historical P/E trend for the Technology sector on NASDAQ?
```

**Cross-Exchange:**
```
Compare Technology sector P/E ratios on NYSE vs. NASDAQ.
```

## Understanding P/E Ratios

### Definition

```
P/E Ratio = Stock Price / Earnings Per Share
```

For sectors:
```
Sector P/E = Weighted Average P/E of all stocks in the sector
```

### Types of P/E

| Type | Description |
|------|-------------|
| Trailing P/E | Based on past 12 months earnings |
| Forward P/E | Based on estimated future earnings |
| GAAP P/E | Using GAAP earnings |
| Non-GAAP P/E | Using adjusted earnings |

## Sector Categories

### Major Sectors

| Sector | Typical P/E Range |
|--------|-------------------|
| Technology | 25-60 |
| Healthcare | 18-35 |
| Financials | 10-18 |
| Consumer Discretionary | 15-30 |
| Consumer Staples | 18-25 |
| Industrials | 15-25 |
| Energy | 8-20 |
| Utilities | 15-22 |
| Real Estate | 30-50 |
| Materials | 12-20 |
| Communications | 15-25 |

### P/E Characteristics by Sector

| Sector | P/E Tendency | Reason |
|--------|--------------|--------|
| Technology | Higher | Growth expectations |
| Financials | Lower | Mature, regulated |
| Utilities | Moderate | Stable, dividend-focused |
| Healthcare | Variable | Mix of growth/value |

## Major Exchanges

### Exchange Characteristics

| Exchange | Focus |
|----------|-------|
| NYSE | Large-cap, established |
| NASDAQ | Tech-heavy, growth |
| AMEX | Smaller companies, ETFs |

### Exchange P/E Differences

| Factor | NYSE | NASDAQ |
|--------|------|--------|
| Tech Weight | Lower | Higher |
| Average P/E | Generally lower | Generally higher |
| Growth vs. Value | More balanced | Growth-tilted |

## Using Sector P/E for Analysis

### Company Valuation Context

| Comparison | Interpretation |
|------------|----------------|
| Company P/E < Sector P/E | Potentially undervalued or issues |
| Company P/E = Sector P/E | Fairly valued relative to sector |
| Company P/E > Sector P/E | Premium valuation or overvalued |

### Premium/Discount Calculation

```
Premium/Discount = (Company P/E - Sector P/E) / Sector P/E × 100%
```

### Example

- Company P/E: 45
- Sector P/E: 58.77
- Discount: (45 - 58.77) / 58.77 = -23.4% (trading at discount)

## Historical Context

### Valuation Levels

| Sector P/E vs. History | Interpretation |
|------------------------|----------------|
| Above 10-year average | Potentially elevated |
| At 10-year average | Normal valuation |
| Below 10-year average | Potentially attractive |

### Cycle Considerations

| Phase | Typical Sector P/E Behavior |
|-------|----------------------------|
| Early Recovery | Rising from lows |
| Mid-Cycle | Moderate, stable |
| Late Cycle | Often elevated |
| Recession | Compressed or distorted |

## Cross-Sector Analysis

### Relative Value

| Comparison | Use |
|------------|-----|
| Tech vs. Financials | Growth vs. value |
| Cyclical vs. Defensive | Risk appetite |
| High vs. Low P/E | Market expectations |

### Rotation Signals

| Signal | Meaning |
|--------|---------|
| Tech P/E rising faster | Growth favored |
| Value sectors rising | Risk-off rotation |
| Convergence | Normalization |
| Divergence | Theme-driven market |

## Data Considerations

### Timing

| Factor | Consideration |
|--------|---------------|
| Earnings season | P/E updates with new earnings |
| Price movements | Daily fluctuation |
| Index rebalancing | Composition changes |

### Calculation Differences

| Source | May Differ On |
|--------|---------------|
| Weighting | Market-cap vs. equal |
| Earnings | Trailing vs. forward |
| Constituents | Index composition |

## Common Use Cases

### Stock Valuation
```
Is AAPL's P/E reasonable compared to the Technology sector?
```

### Sector Selection
```
Which sectors have the lowest P/E ratios currently?
```

### Market Timing
```
Are Technology sector valuations elevated compared to history?
```

### Portfolio Analysis
```
How do my holdings' P/E ratios compare to their sectors?
```

## Analysis Tips

1. **Compare apples to apples**: Same sector, similar companies.

2. **Consider growth**: High P/E may be justified by high growth.

3. **Check historical range**: Current vs. typical levels.

4. **Look at earnings quality**: P/E only as good as earnings.

5. **Cross-reference exchanges**: Same sector, different exchanges.

6. **Watch for outliers**: Negative earnings distort averages.

## Integration with Other Skills

| Skill | Combined Use |
|-------|--------------|
| financial-metrics-analysis | Company P/E vs. sector |
| income-statement | Earnings driving P/E |
| stock-quote | Current price context |
| analyst-estimates | Forward P/E calculation |
