---
name: batch-market-cap
description: Retrieve market capitalization data for multiple companies at once using Octagon MCP. Use when comparing valuations across peers, screening by market cap, or analyzing a portfolio's composition by company size.
---

# Batch Market Cap

Retrieve market capitalization data for multiple companies in a single query using the Octagon MCP server.

## Prerequisites

Ensure Octagon MCP is configured in your AI agent (Cursor, Claude Desktop, Windsurf, etc.). See [references/mcp-setup.md](references/mcp-setup.md) for installation instructions.

## Workflow

### 1. Prepare Company List

Compile the list of ticker symbols you want to analyze (e.g., AAPL, MSFT, GOOGL).

### 2. Execute Query via Octagon MCP

Use the `octagon-agent` tool with a natural language prompt:

```
Retrieve market capitalization data for the following companies: <TICKER1>, <TICKER2>, <TICKER3>.
```

**MCP Call Format:**

```json
{
  "server": "octagon-mcp",
  "toolName": "octagon-agent",
  "arguments": {
    "prompt": "Retrieve market capitalization data for the following companies: AAPL, MSFT, GOOG."
  }
}
```

### 3. Expected Output

The agent returns a structured table with market cap data:

| Company | Ticker | Market Cap (USD) | Source |
|---------|--------|------------------|--------|
| Apple | AAPL | $2.99986 trillion | Octagon Companies Agent |
| Microsoft | MSFT | $3.143 trillion | Companies Market Cap |
| Alphabet | GOOGL | $2.00018 trillion | Octagon Companies Agent |

**Data Sources**: octagon-companies-agent, octagon-financials-agent, octagon-web-search-agent

### 4. Interpret Results

See [references/interpreting-results.md](references/interpreting-results.md) for guidance on:
- Comparing market caps across companies
- Understanding size categories
- Analyzing relative valuations
- Tracking market cap changes

## Example Queries

**Basic Batch Query:**
```
Retrieve market capitalization data for the following companies: AAPL, MSFT, GOOG.
```

**Sector Comparison:**
```
Get market caps for tech giants: AAPL, MSFT, GOOGL, AMZN, META, NVDA.
```

**Portfolio Analysis:**
```
What are the market capitalizations of TSLA, F, GM, and RIVN?
```

**Industry Comparison:**
```
Compare market caps of major banks: JPM, BAC, WFC, C, GS.
```

**Index Components:**
```
Get market caps for the top 10 S&P 500 companies by weight.
```

**International Comparison:**
```
Compare market caps of AAPL, SMSN.IL (Samsung), TSM, and ASML.
```

## Market Cap Categories

### Size Classifications

| Category | Market Cap Range |
|----------|------------------|
| Mega-cap | >$200 billion |
| Large-cap | $10B - $200B |
| Mid-cap | $2B - $10B |
| Small-cap | $300M - $2B |
| Micro-cap | $50M - $300M |
| Nano-cap | <$50M |

### Category Characteristics

| Category | Typical Traits |
|----------|----------------|
| Mega-cap | Market leaders, global reach, stable |
| Large-cap | Established, diversified, moderate growth |
| Mid-cap | Growth potential, less coverage |
| Small-cap | Higher growth, higher volatility |
| Micro-cap | Speculative, limited liquidity |

## Comparative Analysis Framework

### Peer Comparison

| Analysis | Purpose |
|----------|---------|
| Absolute Size | Rank by market cap |
| Relative Size | Ratio to peers |
| Size Distribution | Concentration analysis |
| Historical Rank | Position changes |

### Industry Context

| Comparison | What It Shows |
|------------|---------------|
| vs. Industry Leader | Distance from top |
| vs. Industry Median | Above/below average |
| vs. Sector Total | Market share proxy |

### Valuation Implications

| Scenario | Interpretation |
|----------|----------------|
| Higher market cap, lower revenue | Premium valuation |
| Lower market cap, higher revenue | Discount valuation |
| Similar market cap, different earnings | P/E differential |

## Use Cases

### Portfolio Allocation

| Use | Description |
|-----|-------------|
| Concentration Analysis | Largest holdings by cap |
| Diversification Check | Size mix across holdings |
| Rebalancing | Adjust for cap changes |

### Competitive Analysis

| Use | Description |
|-----|-------------|
| Market Leadership | Largest in industry |
| Relative Positioning | Size vs. competitors |
| Growth Comparison | Cap changes over time |

### Screening

| Use | Description |
|-----|-------------|
| Size Filter | Include/exclude by cap |
| Category Selection | Target specific sizes |
| Index Eligibility | Meets cap requirements |

## Market Cap Calculations

### Basic Formula

```
Market Cap = Share Price × Shares Outstanding
```

### Factors Affecting Market Cap

| Factor | Impact |
|--------|--------|
| Price Change | Direct proportional effect |
| Share Buybacks | Reduces shares, concentrates value |
| New Issuance | Dilutes if price doesn't rise |
| Stock Splits | No effect (price adjusts) |

### Fully Diluted Market Cap

| Component | Description |
|-----------|-------------|
| Basic Shares | Currently outstanding |
| Options | Employee stock options |
| Warrants | Convertible instruments |
| Convertibles | Convertible debt/preferred |

## Data Considerations

### Source Variations

| Factor | Consideration |
|--------|---------------|
| Timing | Real-time vs. delayed data |
| Currency | USD conversion rates |
| Share Count | Basic vs. diluted |
| Updates | Frequency of refresh |

### Handling Discrepancies

| Issue | Approach |
|-------|----------|
| Different sources | Note the variance |
| Different dates | Use consistent timing |
| Currency mix | Convert to single currency |
| Missing data | Flag unavailable items |

## Analysis Tips

1. **Use consistent data**: Same source/date for fair comparison.

2. **Consider context**: Industry norms for market cap.

3. **Track changes**: Market cap shifts over time.

4. **Combine with fundamentals**: P/E, P/S for valuation context.

5. **Watch for outliers**: Investigate unusual sizes.

6. **Global perspective**: Different markets, different scales.

## Integration with Other Skills

| Skill | Combined Use |
|-------|--------------|
| stock-quote | Market cap + current price |
| income-statement | Market cap vs. revenue/earnings |
| financial-metrics-analysis | Valuation multiples |
| analyst-estimates | Market cap vs. price targets |
