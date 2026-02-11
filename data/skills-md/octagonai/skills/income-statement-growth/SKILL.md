---
name: income-statement-growth
description: Retrieve year-over-year growth in income statement items including Revenue, Gross Profit, Operating Income, Net Income, and EPS Diluted. Use when analyzing company financial growth trends, comparing fiscal year performance, or identifying profitability inflection points.
---

# Income Statement Growth

Retrieve and analyze year-over-year growth in key income statement items for public companies using Octagon MCP.

## Prerequisites

Ensure Octagon MCP is configured in your AI agent (Cursor, Claude Desktop, Windsurf, etc.). See [references/mcp-setup.md](references/mcp-setup.md) for installation instructions.

## Query Format

```
Retrieve year-over-year growth in key income-statement items for <TICKER>, limited to <N> records and filtered by period <FY|Q>.
```

**MCP Call:**

```json
{
  "server": "octagon-mcp",
  "toolName": "octagon-agent",
  "arguments": {
    "prompt": "Retrieve year-over-year growth in key income-statement items for AAPL, limited to 5 records and filtered by period FY"
  }
}
```

## Output Format

The agent returns a table with YoY growth percentages:

| Fiscal Year | Revenue Growth (%) | Gross Profit Growth (%) | Operating Income Growth (%) | Net Income Growth (%) | EPS Diluted Growth (%) |
|-------------|-------------------|------------------------|----------------------------|----------------------|------------------------|
| 2025 | 6.43 | 8.04 | 7.98 | 19.50 | 22.70 |
| 2024 | 2.02 | 6.82 | 7.80 | -3.36 | -0.82 |
| 2023 | -2.80 | -0.96 | -4.30 | -2.81 | 0.33 |
| 2022 | 7.79 | 11.74 | 9.63 | 5.41 | 8.91 |

**Data Source:** octagon-financials-agent

## Key Observations Pattern

After receiving data, generate observations:

1. **Growth acceleration**: Identify years with strong growth across all metrics
2. **Margin divergence**: Note when Net Income growth differs significantly from Revenue growth
3. **EPS vs Net Income**: Compare EPS growth to Net Income growth (share buybacks impact)
4. **Contraction periods**: Flag years with negative growth and potential causes

## Follow-up Queries

Based on results, suggest deeper analysis:

- "What factors contributed to the significant net income growth in [YEAR] despite moderate revenue growth?"
- "Why did net income decline in [YEAR] despite positive operating income growth?"
- "How did [COMPANY]'s cost management strategies impact gross profit trends?"

## Metrics Reference

| Metric | Definition |
|--------|------------|
| Revenue Growth | YoY change in total sales |
| Gross Profit Growth | YoY change in Revenue minus Cost of Goods Sold |
| Operating Income Growth | YoY change in income from core operations |
| Net Income Growth | YoY change in bottom-line profit after all expenses |
| EPS Diluted Growth | YoY change in earnings per share (fully diluted) |

## Analysis Tips

1. **EPS outpacing Net Income**: Indicates share buyback activity reducing share count
2. **Gross Profit > Revenue growth**: Margin expansion from pricing power or cost efficiency
3. **Operating Income > Gross Profit growth**: Operating leverage from fixed cost management
4. **Net Income volatility**: Often driven by one-time items, taxes, or interest expenses
