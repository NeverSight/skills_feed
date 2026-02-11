---
name: income-statement
description: Retrieve real-time income statement data including Revenue, Net Income, and EPS Diluted for public companies. Use when analyzing absolute financial figures, historical earnings, or comparing company scale across fiscal periods.
---

# Income Statement

Retrieve real-time income statement data for public companies using Octagon MCP.

## Prerequisites

Ensure Octagon MCP is configured in your AI agent (Cursor, Claude Desktop, Windsurf, etc.). See [references/mcp-setup.md](references/mcp-setup.md) for installation instructions.

## Query Format

```
Retrieve real-time income statement data for <TICKER>, limited to <N> records and filtered by period <FY|Q>.
```

**MCP Call:**

```json
{
  "server": "octagon-mcp",
  "toolName": "octagon-agent",
  "arguments": {
    "prompt": "Retrieve real-time income statement data for AAPL, limited to 5 records and filtered by period FY"
  }
}
```

## Output Format

The agent returns a table with absolute financial figures:

| Fiscal Year | Revenue (USD) | Net Income (USD) | EPS (Diluted) |
|-------------|---------------|------------------|---------------|
| 2025 | $416,161,000,000 | $112,010,000,000 | 7.46 |
| 2024 | $391,035,000,000 | $93,736,000,000 | 6.08 |
| 2023 | $383,285,000,000 | $96,995,000,000 | 6.13 |
| 2022 | $394,328,000,000 | $99,803,000,000 | 6.11 |
| 2021 | $365,817,000,000 | $94,680,000,000 | 5.61 |

**Data Source:** octagon-financials-agent

## Key Observations Pattern

After receiving data, generate observations:

1. **Revenue trajectory**: Calculate dollar and percentage changes year-over-year
2. **Net income trends**: Track profitability in absolute terms
3. **EPS progression**: Note earnings per share expansion or contraction
4. **Margin calculation**: Compute Net Income / Revenue for net margin
5. **Scale context**: Compare figures to industry peers

## Metrics Reference

| Metric | Definition |
|--------|------------|
| Revenue | Total sales/top-line income for the period |
| Net Income | Bottom-line profit after all expenses and taxes |
| EPS (Diluted) | Earnings per share assuming all dilutive securities converted |

## Analysis Tips

### Revenue Scale
- Use to compare company size across industry
- Track absolute dollar growth, not just percentages
- Larger base requires more absolute growth to maintain % growth

### Net Income Quality
- Compare Net Income to Operating Income for non-operating items
- Check for one-time gains/losses distorting figures
- Look for consistent growth trajectory

### EPS Analysis
- EPS can grow faster than Net Income due to buybacks
- Compare to analyst estimates and guidance
- Check shares outstanding for context

### Margin Calculation
Calculate from the data:
```
Net Margin = Net Income / Revenue × 100
```

Example: $112B / $416B = 26.9% net margin

### Period Comparisons
- FY for annual strategic view
- Q for seasonal patterns and recent trends
- Compare same periods (Q1 vs Q1) for seasonality

## Follow-up Queries

Based on results, suggest deeper analysis:

- "What factors contributed to the revenue growth in [YEAR]?"
- "How does [COMPANY]'s [YEAR] net margin compare to industry peers?"
- "What are the key drivers of the EPS expansion over the [N]-year period?"
- "Retrieve quarterly income statement data for [TICKER] to see seasonal patterns"
