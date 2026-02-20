---
name: cash-flow-growth
description: Retrieve year-over-year growth in cash flow metrics including Operating Cash Flow, Free Cash Flow, and Net Cash Flow. Use when analyzing company cash generation trends, capital allocation efficiency, or liquidity trajectory.
---

# Cash Flow Growth

Retrieve and analyze year-over-year growth in cash flow metrics for public companies using Octagon MCP.

## Prerequisites

Ensure Octagon MCP is configured in your AI agent (Cursor, Claude Desktop, Windsurf, etc.). See [references/mcp-setup.md](references/mcp-setup.md) for installation instructions.

## Query Format

```
Retrieve cash-flow growth metrics for <TICKER>, limited to <N> records and filtered by period <FY|Q>.
```

**MCP Call:**

```json
{
  "server": "octagon-mcp",
  "toolName": "octagon-agent",
  "arguments": {
    "prompt": "Retrieve cash-flow growth metrics for AAPL, limited to 5 records and filtered by period FY"
  }
}
```

## Output Format

The agent returns a table with YoY growth percentages:

| Fiscal Year | Operating Cash Flow Growth (%) | Free Cash Flow Growth (%) | Net Cash Flow Growth (%) |
|-------------|-------------------------------|--------------------------|-------------------------|
| 2025 | -5.73 | -9.23 | 8.55 |
| 2024 | 6.98 | 9.26 | -1.14 |
| 2023 | -9.50 | -10.64 | 1.53 |
| 2022 | 17.41 | 19.89 | -1.84 |
| 2021 | 28.96 | 26.70 | 0.63 |

**Data Source:** octagon-financials-agent

## Key Observations Pattern

After receiving data, generate observations:

1. **Operating cash flow trends**: Core business cash generation ability
2. **Free cash flow health**: Capital available for dividends, buybacks, M&A
3. **Net cash flow direction**: Overall liquidity position changes
4. **Volatility assessment**: Consistency of cash generation
5. **Historical context**: Multi-year patterns and inflection points

## Metrics Reference

| Metric | Definition |
|--------|------------|
| Operating Cash Flow Growth | YoY change in cash from core business operations |
| Free Cash Flow Growth | YoY change in OCF minus Capital Expenditures |
| Net Cash Flow Growth | YoY change in total cash position (OCF + Investing + Financing) |

## Analysis Tips

### Strong Cash Generation
When Operating Cash Flow Growth > Revenue Growth:
- Efficient working capital management
- Strong collections and payables optimization
- Quality earnings (cash backing profits)

### Free Cash Flow Divergence
When FCF Growth differs significantly from OCF Growth:
- Capex changes driving the difference
- Growth investments (negative) or harvesting (positive)
- Check capex as % of revenue trend

### Net Cash Flow Volatility
Net Cash Flow often volatile due to:
- Large debt issuances or repayments
- Share buyback programs
- Dividend policy changes
- M&A activity

### Working Capital Impact
Significant OCF swings often driven by:
- Inventory build/drawdown
- Receivables collection timing
- Payables management
- Deferred revenue changes

### Quality of Earnings Check
Compare to income statement:
- OCF should track or exceed Net Income over time
- Persistent OCF < Net Income signals earnings quality concerns

## Follow-up Queries

Based on results, suggest deeper analysis:

- "What drove the operating cash flow decline in [YEAR]?"
- "Break down [COMPANY]'s working capital changes for the last 3 years"
- "Compare [COMPANY]'s free cash flow yield to industry peers"
- "Analyze [COMPANY]'s capital expenditure trends and guidance"
