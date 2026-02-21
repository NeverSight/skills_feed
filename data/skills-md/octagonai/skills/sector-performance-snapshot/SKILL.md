---
name: sector-performance-snapshot
description: Retrieve a snapshot of market sector performance using Octagon MCP. Use when analyzing sector-wide metrics including revenue, EBITDA, net income, market cap, and enterprise value for companies within a specific sector and exchange.
---

# Sector Performance Snapshot

Retrieve comprehensive sector performance metrics by exchange using the Octagon MCP server.

## Prerequisites

Ensure Octagon MCP is configured in your AI agent (Cursor, Claude Desktop, Windsurf, etc.). See [references/mcp-setup.md](references/mcp-setup.md) for installation instructions.

## Workflow

### 1. Identify Parameters

Determine your query parameters:
- **Date**: Specific date for the snapshot
- **Exchange**: NYSE, NASDAQ, etc.
- **Sector**: Technology, Healthcare, Financials, etc.

### 2. Execute Query via Octagon MCP

Use the `octagon-agent` tool with a natural language prompt:

```
Retrieve a snapshot of market sector performance for <DATE>, filtered by exchange <EXCHANGE> and sector <SECTOR>.
```

**MCP Call Format:**

```json
{
  "server": "octagon-mcp",
  "toolName": "octagon-agent",
  "arguments": {
    "prompt": "Retrieve a snapshot of market sector performance for 2025-02-03, filtered by exchange NASDAQ and sector Technology."
  }
}
```

### 3. Expected Output

The agent returns comprehensive sector performance data:

| Metric | Value |
|--------|-------|
| Revenue | $29,094.00 million |
| EBITDA | $12,486.00 million |
| Net Income | $3,882.00 million |
| Market Cap | $113,333.57 million |
| Enterprise Value | $115,021.51 million |
| Employees | 48,000 |
| Recent Debt | $2.68 billion raised |

Additional information:
- Representative companies
- Competitors
- Growth rates (e.g., 71.05% revenue growth YoY)
- Capital structure changes

**Data Sources**: octagon-companies-agent

### 4. Interpret Results

See [references/interpreting-results.md](references/interpreting-results.md) for guidance on:
- Analyzing sector financial health
- Comparing companies within sector
- Understanding valuation metrics
- Evaluating growth trends

## Example Queries

**Specific Sector and Exchange:**
```
Retrieve a snapshot of market sector performance for 2025-02-03, filtered by exchange NASDAQ and sector Technology.
```

**Broad Sector View:**
```
Get performance metrics for all Healthcare companies on NYSE.
```

**Growth Focus:**
```
What are the fastest growing companies in the Technology sector?
```

**Valuation Analysis:**
```
Show market cap and enterprise value for Financial sector on NYSE.
```

**Sector Comparison:**
```
Compare performance metrics of Technology vs. Healthcare sectors.
```

## Key Performance Metrics

### Revenue Metrics

| Metric | Description |
|--------|-------------|
| Revenue | Total sales/income |
| Revenue Growth | YoY change |
| Revenue per Employee | Efficiency |
| Revenue Distribution | Concentration |

### Profitability Metrics

| Metric | Description |
|--------|-------------|
| EBITDA | Operating profitability |
| EBITDA Margin | EBITDA / Revenue |
| Net Income | Bottom line profit |
| Net Margin | Net Income / Revenue |

### Valuation Metrics

| Metric | Description |
|--------|-------------|
| Market Cap | Equity value |
| Enterprise Value | Total firm value |
| EV/Revenue | Revenue multiple |
| EV/EBITDA | Earnings multiple |

### Operational Metrics

| Metric | Description |
|--------|-------------|
| Employees | Workforce size |
| Revenue/Employee | Productivity |
| Market Cap/Employee | Value per employee |

## Understanding Sector Metrics

### Aggregate vs. Average

| Type | Description |
|------|-------------|
| Aggregate | Sum of all companies |
| Average | Mean per company |
| Median | Middle company |
| Weighted | Market-cap weighted |

### Sector Composition

| Factor | Impact on Metrics |
|--------|-------------------|
| Large-cap dominance | Skews aggregates |
| Diverse industries | Wide ranges |
| Cyclicality | Time-sensitive |
| Profitability mix | Margin variation |

## Sector Comparisons

### Technology Sector Benchmarks

| Metric | Typical Range |
|--------|---------------|
| Revenue Growth | 10-30% |
| EBITDA Margin | 20-40% |
| Net Margin | 10-25% |
| EV/Revenue | 3-10x |

### Healthcare Sector Benchmarks

| Metric | Typical Range |
|--------|---------------|
| Revenue Growth | 5-15% |
| EBITDA Margin | 15-30% |
| Net Margin | 5-15% |
| EV/Revenue | 2-6x |

### Financial Sector Benchmarks

| Metric | Typical Range |
|--------|---------------|
| Revenue Growth | 3-10% |
| Net Margin | 15-30% |
| ROE | 10-15% |
| P/E | 10-18x |

### Industrial Sector Benchmarks

| Metric | Typical Range |
|--------|---------------|
| Revenue Growth | 3-8% |
| EBITDA Margin | 12-22% |
| Net Margin | 5-12% |
| EV/EBITDA | 8-14x |

## Analysis Framework

### Sector Health Assessment

| Indicator | Healthy | Concerning |
|-----------|---------|------------|
| Revenue Growth | Positive, consistent | Declining |
| Margins | Stable/expanding | Contracting |
| Cash Generation | Strong | Weak |
| Debt Levels | Manageable | Excessive |

### Comparative Analysis

| Comparison | Purpose |
|------------|---------|
| vs. Prior Period | Trend direction |
| vs. Other Sectors | Relative performance |
| vs. Market | Alpha/beta analysis |
| vs. Expectations | Beat/miss assessment |

## Capital Structure Insights

### Debt Analysis

| Metric | Significance |
|--------|--------------|
| Recent Debt Raised | Capital needs |
| Debt/EBITDA | Leverage level |
| Interest Coverage | Debt service ability |
| Maturity Schedule | Refinancing risk |

### Equity Analysis

| Metric | Significance |
|--------|--------------|
| Market Cap | Equity valuation |
| Shares Outstanding | Dilution |
| Float | Tradeable shares |
| Insider Ownership | Alignment |

## Competitor Landscape

### Identifying Competitors

| Method | Approach |
|--------|----------|
| Same Industry | Direct peers |
| Similar Size | Market cap range |
| Similar Model | Business type |
| Similar Geography | Regional focus |

### Competitive Position

| Metric | What It Shows |
|--------|---------------|
| Market Share | Industry position |
| Relative Size | Scale vs. peers |
| Relative Growth | Momentum vs. peers |
| Relative Margins | Efficiency vs. peers |

## Common Use Cases

### Sector Screening
```
Which sectors have the strongest revenue growth?
```

### Company Context
```
How does AAPL compare to the Technology sector average?
```

### Investment Research
```
What are the key metrics for Healthcare sector on NYSE?
```

### Trend Analysis
```
How has Technology sector profitability changed over time?
```

### Competitive Analysis
```
Who are the main competitors to company X in this sector?
```

## Analysis Tips

1. **Use multiple metrics**: Don't rely on one indicator.

2. **Consider sector norms**: Different sectors have different benchmarks.

3. **Track trends**: Point-in-time vs. direction.

4. **Weight by size**: Large companies dominate aggregates.

5. **Look for outliers**: May indicate opportunities or risks.

6. **Combine with macro**: Sector performance reflects economy.

## Integration with Other Skills

| Skill | Combined Use |
|-------|--------------|
| sector-pe-ratios | Valuation context |
| industry-pe-ratios | Industry drill-down |
| income-statement | Company-specific financials |
| financial-metrics-analysis | Detailed company metrics |
| stock-performance | Price performance overlay |
