---
name: company-market-cap
description: Retrieve market capitalization data for a single company using Octagon MCP. Use when you need the current market value, valuation context, or size classification for any publicly traded stock.
---

# Company Market Cap

Retrieve the current market capitalization for a single company using the Octagon MCP server.

## Prerequisites

Ensure Octagon MCP is configured in your AI agent (Cursor, Claude Desktop, Windsurf, etc.). See [references/mcp-setup.md](references/mcp-setup.md) for installation instructions.

## Workflow

### 1. Identify the Stock

Determine the ticker symbol for the company you want to analyze (e.g., AAPL, MSFT, GOOGL).

### 2. Execute Query via Octagon MCP

Use the `octagon-agent` tool with a natural language prompt:

```
Get market capitalization data for the symbol <TICKER>.
```

**MCP Call Format:**

```json
{
  "server": "octagon-mcp",
  "toolName": "octagon-agent",
  "arguments": {
    "prompt": "Get market capitalization data for the symbol AAPL."
  }
}
```

### 3. Expected Output

The agent returns precise market cap data:

| Date | Market Capitalization (USD) |
|------|----------------------------|
| 2026-02-02 | $3,968,586,877,215.00 |

Additional context provided:
- Rounded value (e.g., $3.97 trillion)
- As-of date for the data
- Data source

**Data Sources**: octagon-stock-data-agent

### 4. Interpret Results

See [references/interpreting-results.md](references/interpreting-results.md) for guidance on:
- Understanding market cap magnitude
- Size classification
- Valuation context
- Historical comparison

## Example Queries

**Basic Query:**
```
Get market capitalization data for the symbol AAPL.
```

**With Context:**
```
What is the current market cap for Tesla?
```

**Historical Reference:**
```
What is Microsoft's market capitalization and how has it changed recently?
```

**Valuation Context:**
```
What is NVDA's market cap and how does it compare to other chipmakers?
```

**Size Classification:**
```
What size category is AMD based on its market cap?
```

## Understanding Market Cap

### Definition

```
Market Cap = Current Share Price × Shares Outstanding
```

### What It Represents

| Aspect | Description |
|--------|-------------|
| Total Value | Market's valuation of all shares |
| Size Indicator | Company scale and influence |
| Index Weight | Determines index composition |
| Acquisition Cost | Theoretical buyout price |

### What It Doesn't Represent

| Misconception | Reality |
|---------------|---------|
| Intrinsic Value | Market perception, not fundamental worth |
| Book Value | Different from accounting value |
| Enterprise Value | Excludes debt and cash |
| Sale Price | Acquisitions often have premiums |

## Size Classifications

### Standard Categories

| Category | Range | Characteristics |
|----------|-------|-----------------|
| Mega-cap | >$200B | Global leaders, household names |
| Large-cap | $10B-$200B | Established, stable companies |
| Mid-cap | $2B-$10B | Growth potential, moderate risk |
| Small-cap | $300M-$2B | Higher growth, higher volatility |
| Micro-cap | $50M-$300M | Speculative, limited coverage |
| Nano-cap | <$50M | Highest risk, low liquidity |

### Trillion-Dollar Club

| Threshold | Significance |
|-----------|--------------|
| >$1T | Elite status, massive scale |
| >$2T | Global economic influence |
| >$3T | Among world's most valuable |

## Market Cap Analysis

### Valuation Ratios

| Ratio | Formula | Purpose |
|-------|---------|---------|
| P/E | Market Cap / Net Income | Earnings valuation |
| P/S | Market Cap / Revenue | Revenue valuation |
| P/B | Market Cap / Book Value | Asset valuation |
| PEG | P/E / Growth Rate | Growth-adjusted value |

### Enterprise Value Comparison

| Metric | Calculation |
|--------|-------------|
| Enterprise Value | Market Cap + Debt - Cash |
| EV/EBITDA | EV / Operating earnings |
| EV/Revenue | EV / Total revenue |

## Contextual Analysis

### Industry Comparison

| Question | Purpose |
|----------|---------|
| Largest in sector? | Market leadership |
| Above/below median? | Relative positioning |
| Gap to leader? | Distance from top |

### Historical Perspective

| Timeframe | Analysis |
|-----------|----------|
| 1 Year | Recent performance |
| 5 Years | Medium-term trend |
| 10 Years | Long-term growth |
| All-time High | Peak valuation |

### Global Context

| Comparison | Purpose |
|------------|---------|
| vs. Global Leaders | Scale perspective |
| vs. Country GDP | Economic significance |
| vs. Index Total | Market weight |

## Factors Affecting Market Cap

### Price Drivers

| Factor | Impact |
|--------|--------|
| Earnings | Fundamental driver |
| Growth | Future expectations |
| Sentiment | Market psychology |
| Macro | Economic conditions |

### Share Count Changes

| Event | Effect |
|-------|--------|
| Buybacks | Reduces shares, concentrates value |
| Issuance | Increases shares, dilutes |
| Stock Split | No effect (price adjusts) |
| Spin-offs | Separates value |

## Common Use Cases

### Investment Analysis
```
What is the market cap for XYZ and how does it compare to peers?
```

### Portfolio Context
```
What is the market capitalization of my largest holding, AAPL?
```

### News Context
```
Apple's market cap after today's earnings announcement?
```

### Valuation Check
```
Is TSLA's market cap justified relative to its revenue?
```

## Analysis Tips

1. **Use precise values**: Full number for calculations, rounded for communication.

2. **Note the date**: Market cap changes constantly with price.

3. **Consider float**: Some shares may not be tradeable.

4. **Compare appropriately**: Same industry, similar business models.

5. **Understand drivers**: Price appreciation vs. share changes.

6. **Enterprise value**: Add debt consideration for M&A context.

## Integration with Other Skills

| Skill | Combined Use |
|-------|--------------|
| stock-quote | Market cap + current price details |
| batch-market-cap | Single company vs. peer group |
| income-statement | Market cap vs. earnings |
| balance-sheet | Market cap vs. book value |
| financial-metrics-analysis | Full valuation analysis |
