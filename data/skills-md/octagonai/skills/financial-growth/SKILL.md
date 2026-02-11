---
name: financial-growth
description: Retrieve comprehensive year-over-year growth in key financial metrics including Revenue, Gross Profit, Operating Income, Net Income, EPS, and Free Cash Flow. Use when analyzing overall company financial performance trends across income statement and cash flow.
---

# Financial Growth

Retrieve and analyze comprehensive year-over-year growth in key financial metrics for public companies using Octagon MCP.

## Prerequisites

Ensure Octagon MCP is configured in your AI agent (Cursor, Claude Desktop, Windsurf, etc.). See [references/mcp-setup.md](references/mcp-setup.md) for installation instructions.

## Query Format

```
Retrieve year-over-year growth in key financial metrics for <TICKER>, limited to <N> records and filtered by period <FY|Q>.
```

**MCP Call:**

```json
{
  "server": "octagon-mcp",
  "toolName": "octagon-agent",
  "arguments": {
    "prompt": "Retrieve year-over-year growth in key financial metrics for AAPL, limited to 5 records and filtered by period FY"
  }
}
```

## Output Format

The agent returns a comprehensive table with YoY growth percentages:

| Fiscal Year | Revenue Growth (%) | Gross Profit Growth (%) | Operating Income Growth (%) | Net Income Growth (%) | EPS Growth (%) | Free Cash Flow Growth (%) |
|-------------|-------------------|------------------------|----------------------------|----------------------|----------------|--------------------------|
| 2025 | 6.43% | 8.04% | 7.98% | 19.50% | 22.59% | -5.73% |
| 2024 | 2.02% | 6.82% | 7.80% | -3.36% | -0.81% | 6.98% |
| 2023 | -2.80% | -0.96% | -4.30% | -2.81% | 0.16% | -10.64% |
| 2022 | 7.79% | 11.74% | 9.63% | 5.41% | 8.47% | 19.89% |
| 2021 | 33.26% | 45.62% | 64.36% | 64.92% | 71.30% | 26.70% |

**Data Source:** octagon-financials-agent

## Key Insights Pattern

After receiving data, generate insights:

1. **Peak performance years**: Identify years with highest growth across all metrics
2. **Earnings vs cash flow divergence**: Compare Net Income growth to FCF growth
3. **Margin trends**: Compare Gross Profit and Operating Income growth to Revenue
4. **EPS enhancement**: Note when EPS growth exceeds Net Income growth (buybacks)
5. **Challenging periods**: Flag years with broad-based declines

## Metrics Reference

| Metric | Definition |
|--------|------------|
| Revenue Growth | YoY change in total sales |
| Gross Profit Growth | YoY change in Revenue minus COGS |
| Operating Income Growth | YoY change in income from operations |
| Net Income Growth | YoY change in bottom-line profit |
| EPS Growth | YoY change in earnings per share |
| Free Cash Flow Growth | YoY change in operating cash flow minus capex |

## Analysis Tips

### Exceptional Growth Years
When all metrics show double-digit growth:
- Identify specific drivers (new products, markets, pricing)
- Assess sustainability of growth rate
- Compare to industry and competitors

### Earnings Quality Check
When Net Income Growth >> Free Cash Flow Growth:
- Potential working capital build
- Aggressive revenue recognition
- One-time items boosting earnings
- Investigate cash conversion

### Share Buyback Impact
When EPS Growth > Net Income Growth:
- Active share repurchase program
- Check shares outstanding trend
- Assess capital allocation priorities

### Margin Expansion
When Operating Income Growth > Revenue Growth:
- Operating leverage at work
- Cost discipline showing results
- Pricing power in action

### Contraction Periods
When multiple metrics decline:
- Identify root cause (demand, competition, costs)
- Check if industry-wide or company-specific
- Look for recovery signals in subsequent periods

## Follow-up Queries

Based on results, suggest deeper analysis:

- "What factors contributed to the significant [YEAR] growth spike?"
- "How did the [YEAR] downturn impact [COMPANY]'s long-term strategy?"
- "What explains the [YEAR] net income growth despite lower free cash flow?"
- "Compare [COMPANY]'s growth metrics to [PEER1] and [PEER2]"
