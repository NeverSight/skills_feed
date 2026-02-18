---
name: stock-price-change
description: Retrieve stock price change statistics across multiple time periods using Octagon MCP. Use when analyzing short-term and long-term returns, comparing performance across timeframes, and evaluating momentum and historical growth.
---

# Stock Price Change

Retrieve comprehensive price change statistics across multiple time periods using the Octagon MCP server.

## Prerequisites

Ensure Octagon MCP is configured in your AI agent (Cursor, Claude Desktop, Windsurf, etc.). See [references/mcp-setup.md](references/mcp-setup.md) for installation instructions.

## Workflow

### 1. Identify the Stock

Determine the ticker symbol for the company you want to analyze (e.g., AAPL, MSFT, GOOGL).

### 2. Execute Query via Octagon MCP

Use the `octagon-agent` tool with a natural language prompt:

```
Get stock price change statistics for the symbol <TICKER>.
```

**MCP Call Format:**

```json
{
  "server": "octagon-mcp",
  "toolName": "octagon-agent",
  "arguments": {
    "prompt": "Get stock price change statistics for the symbol AAPL."
  }
}
```

### 3. Expected Output

The agent returns price change data across multiple timeframes:

| Time Period | Percentage Change |
|-------------|-------------------|
| 1 Day | 4.06% |
| 5 Days | 4.80% |
| 1 Month | -0.37% |
| 3 Months | -0.13% |
| 6 Months | 33.42% |
| Year-to-Date (YTD) | -0.37% |
| 1 Year | 18.42% |
| 3 Years | 79.03% |
| 5 Years | 100.02% |
| 10 Years | 1,043.14% |
| All-Time High | 210,270.08% |

**Key Insight**: Strong long-term growth with 10-year return of 1,043.14%, but recent short-term performance slightly negative.

**Data Sources**: octagon-stock-data-agent

### 4. Interpret Results

See [references/interpreting-results.md](references/interpreting-results.md) for guidance on:
- Evaluating short-term vs. long-term performance
- Understanding momentum signals
- Comparing to benchmarks
- Assessing trend consistency

## Example Queries

**Basic Query:**
```
Get stock price change statistics for the symbol AAPL.
```

**Multiple Stocks:**
```
Compare price change statistics for AAPL, MSFT, and GOOGL.
```

**Specific Focus:**
```
What is the 1-year and 5-year return for TSLA?
```

**YTD Performance:**
```
What is the year-to-date performance of NVDA?
```

**Long-Term Growth:**
```
What is the 10-year cumulative return for AMZN?
```

## Understanding Time Periods

### Short-Term Periods

| Period | Use Case |
|--------|----------|
| 1 Day | Daily momentum |
| 5 Days | Weekly trend |
| 1 Month | Recent performance |
| 3 Months | Quarterly trend |

### Medium-Term Periods

| Period | Use Case |
|--------|----------|
| 6 Months | Half-year momentum |
| YTD | Calendar year performance |
| 1 Year | Annual return |

### Long-Term Periods

| Period | Use Case |
|--------|----------|
| 3 Years | Business cycle |
| 5 Years | Market cycle |
| 10 Years | Secular trend |
| All-Time | Total return since inception |

## Return Interpretation

### Performance Classification

| Return (1 Year) | Classification |
|-----------------|----------------|
| >50% | Exceptional |
| 25-50% | Very strong |
| 10-25% | Strong |
| 0-10% | Moderate |
| -10 to 0% | Weak |
| <-10% | Poor |

### Long-Term Standards

| Return (10 Year) | Classification |
|------------------|----------------|
| >500% | Exceptional |
| 200-500% | Very strong |
| 100-200% | Strong |
| 50-100% | Moderate |
| 0-50% | Below average |
| <0% | Poor |

## Momentum Analysis

### Trend Consistency

| Pattern | Interpretation |
|---------|----------------|
| All periods positive | Strong consistent uptrend |
| Short negative, long positive | Pullback in uptrend |
| Short positive, long negative | Bounce in downtrend |
| All periods negative | Consistent downtrend |

### Momentum Signals

| Signal | Pattern |
|--------|---------|
| Accelerating | Returns increasing across periods |
| Decelerating | Returns decreasing across periods |
| Stable | Consistent returns across periods |
| Reversal | Sign change between periods |

### Example Analysis

From AAPL data:
- 1 Day: +4.06% (strong daily)
- 1 Month: -0.37% (slight pullback)
- 1 Year: +18.42% (solid annual)
- 10 Year: +1,043.14% (exceptional long-term)

**Interpretation**: Long-term compounder with recent consolidation.

## Annualized Returns

### Calculation

```
Annualized Return = (1 + Total Return)^(1/Years) - 1
```

### Example

From AAPL data:
- 10-Year Return: 1,043.14%
- Annualized: (1 + 10.4314)^(1/10) - 1 = 27.3% per year

### Annualized Benchmarks

| Annual Return | Rating |
|---------------|--------|
| >25% | Exceptional |
| 15-25% | Very strong |
| 10-15% | Strong |
| 7-10% | Market-like |
| <7% | Below market |

## Comparison Analysis

### vs. Benchmarks

| Benchmark | What to Compare |
|-----------|-----------------|
| S&P 500 | Market performance |
| Sector ETF | Industry performance |
| Peers | Competitive position |

### Alpha Calculation

```
Alpha = Stock Return - Benchmark Return
```

### Example

If AAPL 1-year return is +18.42% and S&P 500 is +10%:
- Alpha: +8.42% outperformance

## Time Period Relationships

### Healthy Patterns

| Pattern | Interpretation |
|---------|----------------|
| Long > Short | Healthy uptrend |
| Positive all periods | Consistent strength |
| Improving short-term | Momentum building |

### Warning Patterns

| Pattern | Interpretation |
|---------|----------------|
| Long << Short | Mean reversion risk |
| Long > 0, Short < 0 | Trend weakening |
| All negative | Fundamental issues |

## All-Time High Analysis

### Distance from ATH

```
Distance = (ATH - Current) / ATH × 100%
```

### ATH Context

| Position | Interpretation |
|----------|----------------|
| At ATH | Maximum strength |
| 0-10% below | Near highs |
| 10-20% below | Correction |
| 20-40% below | Bear market |
| >40% below | Severe decline |

## Common Use Cases

### Performance Summary
```
What are the returns for AAPL across all time periods?
```

### Trend Analysis
```
Is MSFT in an uptrend or downtrend based on recent returns?
```

### Long-Term Growth
```
What is the 10-year cumulative return for the FAANG stocks?
```

### Momentum Check
```
Is NVDA showing positive momentum in the short-term?
```

### Comparison
```
Compare 1-year returns for major tech stocks.
```

## Analysis Tips

1. **Don't rely on one period**: Use multiple timeframes.

2. **Compare to benchmarks**: Returns mean more in context.

3. **Consider consistency**: Smooth vs. volatile returns.

4. **Annualize long-term**: For fair comparison.

5. **Watch for divergence**: Short vs. long-term signals.

6. **Factor in dividends**: Total return vs. price return.

## Integration with Other Skills

| Skill | Combined Use |
|-------|--------------|
| stock-quote | Current price context |
| stock-performance | Daily price data |
| stock-historical-index | vs. market returns |
| financial-metrics-analysis | Fundamentals behind returns |
