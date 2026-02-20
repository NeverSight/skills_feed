---
name: balance-sheet-growth
description: Retrieve year-over-year growth in balance sheet items including Total Assets, Total Liabilities, Shareholders Equity, Cash, and Inventories. Use when analyzing company financial position trends, capital structure changes, or liquidity management.
---

# Balance Sheet Growth

Retrieve and analyze year-over-year growth in key balance sheet items for public companies using Octagon MCP.

## Prerequisites

Ensure Octagon MCP is configured in your AI agent (Cursor, Claude Desktop, Windsurf, etc.). See [references/mcp-setup.md](references/mcp-setup.md) for installation instructions.

## Query Format

```
Retrieve year-over-year growth in key balance-sheet items for <TICKER>, limited to <N> records and filtered by period <FY|Q>.
```

**MCP Call:**

```json
{
  "server": "octagon-mcp",
  "toolName": "octagon-agent",
  "arguments": {
    "prompt": "Retrieve year-over-year growth in key balance-sheet items for AAPL, limited to 5 records and filtered by period FY"
  }
}
```

## Output Format

The agent returns a table with YoY growth percentages:

| Fiscal Year | Total Assets Growth (%) | Total Liabilities Growth (%) | Shareholders' Equity Growth (%) | Cash & Cash Equivalents Growth (%) | Inventories Growth (%) |
|-------------|------------------------|-----------------------------|---------------------------------|-----------------------------------|------------------------|
| 2025 | -1.57 | -7.31 | 29.47 | 12.01 | -21.52 |
| 2024 | 3.51 | 6.05 | -8.36 | -0.07 | 15.08 |
| 2023 | -0.00 | -3.85 | 22.64 | 26.72 | 28.00 |
| 2022 | 0.49 | 4.92 | -19.68 | -32.32 | -24.83 |

**Data Sources:** octagon-companies-agent, octagon-financials-agent

## Key Observations Pattern

After receiving data, generate observations:

1. **Asset base changes**: Track total assets growth/decline and drivers
2. **Leverage trends**: Compare liabilities growth to equity growth
3. **Liquidity position**: Monitor cash and cash equivalents trajectory
4. **Working capital**: Assess inventory management efficiency
5. **Capital structure shifts**: Note significant equity vs liability changes

## Metrics Reference

| Metric | Definition |
|--------|------------|
| Total Assets Growth | YoY change in all company assets |
| Total Liabilities Growth | YoY change in all obligations and debts |
| Shareholders' Equity Growth | YoY change in net worth (Assets - Liabilities) |
| Cash & Cash Equivalents Growth | YoY change in liquid assets |
| Inventories Growth | YoY change in unsold goods and materials |

## Analysis Tips

### Deleveraging Signal
When Liabilities decline while Equity grows:
- Company paying down debt
- Strengthening balance sheet
- Example: Liabilities -7.31%, Equity +29.47%

### Asset-Light Trend
When Assets decline but Equity grows:
- Efficient capital deployment
- Possible divestitures or write-offs
- Focus on return on assets

### Cash Accumulation
When Cash grows faster than Assets:
- Building war chest for M&A or buybacks
- Conservative financial positioning
- May signal limited reinvestment opportunities

### Inventory Management
When Inventories decline while Revenue grows:
- Improved supply chain efficiency
- Just-in-time inventory practices
- Better demand forecasting

### Capital Structure Warning
When Liabilities grow faster than Assets:
- Increasing leverage
- Potential solvency concerns if sustained
- Review debt covenants and maturities

## Follow-up Queries

Based on results, suggest deeper analysis:

- "What drove the significant shareholders' equity growth in [YEAR]?"
- "Analyze [COMPANY]'s debt maturity schedule and refinancing risk"
- "Compare [COMPANY]'s leverage ratios to industry peers"
- "Extract cash flow statement data for [TICKER] to understand cash sources"
