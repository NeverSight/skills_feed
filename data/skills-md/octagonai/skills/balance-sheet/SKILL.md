---
name: balance-sheet
description: Retrieve detailed balance sheet statement data including Total Assets, Current Assets, Non-Current Assets, Liabilities, Equity, and Net Debt for public companies. Use when analyzing financial position, capital structure, or leverage metrics.
---

# Balance Sheet

Retrieve detailed balance sheet statement data for public companies using Octagon MCP.

## Prerequisites

Ensure Octagon MCP is configured in your AI agent (Cursor, Claude Desktop, Windsurf, etc.). See [references/mcp-setup.md](references/mcp-setup.md) for installation instructions.

## Query Format

```
Retrieve detailed balance sheet statement data for <TICKER>, limited to <N> records and filtered by period <FY|Q>.
```

**MCP Call:**

```json
{
  "server": "octagon-mcp",
  "toolName": "octagon-agent",
  "arguments": {
    "prompt": "Retrieve detailed balance sheet statement data for AAPL, limited to 5 records and filtered by period FY"
  }
}
```

## Output Format

The agent returns a table with absolute financial figures:

| Fiscal Year | Total Assets (USD) | Total Current Assets (USD) | Total Non-Current Assets (USD) | Total Liabilities (USD) | Total Equity (USD) | Net Debt (USD) |
|-------------|-------------------|---------------------------|-------------------------------|------------------------|-------------------|----------------|
| 2025 | 359,241.00 million | 147,957.00 million | 211,284.00 million | 285,508.00 million | 73,733.00 million | 89,749.00 million |
| 2024 | 364,980.00 million | 152,987.00 million | 211,993.00 million | 308,030.00 million | 56,950.00 million | 89,116.00 million |
| 2023 | 352,583.00 million | 143,566.00 million | 209,017.00 million | 290,437.00 million | 62,146.00 million | 93,965.00 million |
| 2022 | 352,755.00 million | 135,405.00 million | 217,350.00 million | 302,083.00 million | 50,672.00 million | 108,834.00 million |
| 2021 | 351,002.00 million | 134,836.00 million | 216,166.00 million | 287,912.00 million | 63,090.00 million | 101,582.00 million |

**Data Source:** octagon-financials-agent

## Key Observations Pattern

After receiving data, generate observations:

1. **Asset base changes**: Track total assets trajectory over time
2. **Asset composition**: Analyze current vs non-current asset mix
3. **Equity trends**: Monitor shareholders' equity changes
4. **Leverage position**: Track net debt levels and direction
5. **Capital structure**: Compare liabilities to equity ratios

## Metrics Reference

| Metric | Definition |
|--------|------------|
| Total Assets | All resources owned by the company |
| Total Current Assets | Assets convertible to cash within 1 year |
| Total Non-Current Assets | Long-term assets (PP&E, intangibles, investments) |
| Total Liabilities | All obligations and debts |
| Total Equity | Net worth (Assets - Liabilities) |
| Net Debt | Total debt minus cash and equivalents |

## Analysis Tips

### Asset Composition
- Current Assets: Liquidity and working capital
- Non-Current Assets: Long-term investments and capacity
- Shift toward current = more liquid
- Shift toward non-current = more invested

### Capital Structure Ratios
Calculate from the data:
```
Debt-to-Equity = Total Liabilities / Total Equity
Equity Ratio = Total Equity / Total Assets
```

### Net Debt Analysis
- Declining Net Debt = deleveraging
- Negative Net Debt = net cash position
- Compare to EBITDA for leverage context

### Equity Trends
Rising equity from:
- Retained earnings (profitable operations)
- Stock issuance
- Other comprehensive income

Declining equity from:
- Net losses
- Share buybacks
- Dividends exceeding earnings

### Working Capital
```
Working Capital = Current Assets - Current Liabilities
```
Positive = can meet short-term obligations

## Follow-up Queries

Based on results, suggest deeper analysis:

- "What factors contributed to the decline in total assets in [YEAR] compared to [PRIOR YEAR]?"
- "How has [COMPANY]'s capital allocation strategy evolved between [YEAR1] and [YEAR2]?"
- "What specific components of non-current assets grew between [YEAR1] and [YEAR2]?"
- "Compare [COMPANY]'s leverage ratios to [PEER1] and [PEER2]"
