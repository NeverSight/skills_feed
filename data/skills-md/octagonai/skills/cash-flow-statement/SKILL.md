---
name: cash-flow-statement
description: Retrieve real-time or historical cash flow statement data including Net Income, Operating Cash Flow, Investing Cash Flow, Financing Cash Flow, Free Cash Flow, and Cash Position for public companies. Use when analyzing cash generation, capital allocation, or liquidity trends.
---

# Cash Flow Statement

Retrieve real-time or historical cash flow statement data for public companies using Octagon MCP.

## Prerequisites

Ensure Octagon MCP is configured in your AI agent (Cursor, Claude Desktop, Windsurf, etc.). See [references/mcp-setup.md](references/mcp-setup.md) for installation instructions.

## Query Format

```
Retrieve real-time or historical cash flow statement data for <TICKER>, limited to <N> records and filtered by period <FY|Q>.
```

**MCP Call:**

```json
{
  "server": "octagon-mcp",
  "toolName": "octagon-agent",
  "arguments": {
    "prompt": "Retrieve real-time or historical cash flow statement data for AAPL, limited to 5 records and filtered by period FY"
  }
}
```

## Output Format

The agent returns a table with absolute cash flow figures:

| Fiscal Year | Net Income (USD) | Operating Cash Flow (USD) | Investing Cash Flow (USD) | Financing Cash Flow (USD) | Free Cash Flow (USD) | Net Change in Cash (USD) | Cash at End of Period (USD) |
|-------------|-----------------|--------------------------|--------------------------|--------------------------|---------------------|-------------------------|----------------------------|
| 2025 | $112.01B | $111.48B | $15.19B | -$120.69B | $98.77B | $5.99B | $35.93B |
| 2024 | $93.74B | $118.25B | $2.94B | -$121.98B | $108.81B | -$794.00M | $29.94B |
| 2023 | $96.99B | $110.54B | $3.71B | -$108.49B | $99.58B | $5.76B | $30.74B |
| 2022 | $99.80B | $122.15B | -$2.24B | -$110.75B | $111.44B | -$1.09B | $24.98B |
| 2021 | $94.68B | $104.04B | -$1.45B | -$93.35B | $92.95B | -$386.00M | $35.93B |

**Data Source:** octagon-financials-agent

## Key Observations Pattern

After receiving data, generate observations:

1. **Operating cash flow consistency**: Track OCF relative to Net Income
2. **Financing outflows**: Analyze buybacks and dividends
3. **Free cash flow capacity**: Assess cash generation strength
4. **Capital expenditure trends**: Derive from OCF minus FCF
5. **Cash position trajectory**: Monitor ending cash balance

## Metrics Reference

| Metric | Definition |
|--------|------------|
| Net Income | Bottom-line profit (starting point for OCF) |
| Operating Cash Flow | Cash from core business operations |
| Investing Cash Flow | Cash for/from investments and capex |
| Financing Cash Flow | Cash from/to debt and equity activities |
| Free Cash Flow | OCF minus capital expenditures |
| Net Change in Cash | Total cash change for the period |
| Cash at End of Period | Ending cash and equivalents balance |

## Analysis Tips

### Cash Conversion Quality
```
Cash Conversion = Operating Cash Flow / Net Income
```
- Above 1.0 = high quality earnings
- Consistently below 1.0 = potential concerns

### Capex Calculation
```
Capital Expenditures = Operating Cash Flow - Free Cash Flow
```
Example: $111.48B - $98.77B = $12.71B capex

### Shareholder Returns
Financing outflows typically include:
- Share repurchases (buybacks)
- Dividend payments
- Debt repayments

### Three-Statement Linkage
- Net Income flows from Income Statement
- Cash at End links to Balance Sheet
- Changes explain Balance Sheet movements

### Cash Flow Sustainability
Strong indicators:
- OCF consistently > Net Income
- FCF covers dividends and buybacks
- Positive ending cash trend

Warning signs:
- OCF declining while income grows
- FCF negative with continued buybacks
- Cash position eroding

## Follow-up Queries

Based on results, suggest deeper analysis:

- "Break down [COMPANY]'s financing cash flow between buybacks, dividends, and debt activity"
- "What is [COMPANY]'s capital expenditure trend and guidance for next year?"
- "Compare [COMPANY]'s free cash flow yield to [PEER1] and [PEER2]"
- "Analyze [COMPANY]'s working capital changes driving operating cash flow"
