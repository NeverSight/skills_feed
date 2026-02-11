---
name: financial-metrics-analysis
description: Analyze year-over-year growth in income statement items and financial metrics using Octagon MCP. Use when retrieving YoY Revenue Growth, Cost of Revenue Growth, Gross Profit Growth, Operating Income Growth, Net Income Growth, or comparing financial performance across fiscal periods for any public company.
---

# Financial Metrics Analysis

Retrieve and analyze year-over-year growth in key income statement items for public companies using the Octagon MCP server.

## Prerequisites

Ensure Octagon MCP is configured in your AI agent (Cursor, Claude Desktop, Windsurf, etc.). See [references/mcp-setup.md](references/mcp-setup.md) for installation instructions.

## Workflow

### 1. Identify Analysis Parameters

Determine the following before querying:
- **Ticker**: Stock symbol (e.g., AAPL, MSFT, GOOGL)
- **Records**: Number of periods to retrieve (e.g., 5 years)
- **Period**: FY (fiscal year) or Q (quarterly)

### 2. Execute Query via Octagon MCP

Use the `octagon-agent` tool with a natural language prompt:

```
Retrieve year-over-year growth in key income-statement items for <TICKER>, limited to <N> records and filtered by period <FY|Q>.
```

**MCP Call Format:**

```json
{
  "server": "octagon-mcp",
  "toolName": "octagon-agent",
  "arguments": {
    "prompt": "Retrieve year-over-year growth in key income-statement items for AAPL, limited to 5 records and filtered by period FY"
  }
}
```

### 3. Expected Output

The agent returns a tabular response with YoY growth percentages:

| Year | Revenue Growth | Cost of Revenue Growth | Gross Profit Growth | Operating Income Growth | Net Income Growth |
|------|----------------|------------------------|---------------------|-------------------------|-------------------|
| 2024 | 2.0%           | 1.5%                   | 3.1%                | 5.2%                    | 4.8%              |
| 2023 | -2.8%          | -1.2%                  | -4.5%               | -8.1%                   | -10.2%            |
| ...  | ...            | ...                    | ...                 | ...                     | ...               |

**Data Sources**: octagon-companies-agent, octagon-financials-agent

### 4. Interpret Results

See [references/interpreting-results.md](references/interpreting-results.md) for guidance on:
- Reading growth percentages
- Identifying trends and inflection points
- Spotting operating leverage signals
- Comparing to industry benchmarks

## Example Queries

**Basic YoY Analysis:**
```
Retrieve year-over-year growth in key income-statement items for AAPL, limited to 5 records and filtered by period FY.
```

**Quarterly Analysis:**
```
Retrieve year-over-year growth in key income-statement items for TSLA, limited to 8 records and filtered by period Q.
```

**Extended Historical View:**
```
Retrieve year-over-year growth in key income-statement items for MSFT, limited to 10 records and filtered by period FY.
```

## Key Metrics Explained

| Metric | Definition |
|--------|------------|
| Revenue Growth | YoY change in total revenue/sales |
| Cost of Revenue Growth | YoY change in direct costs (COGS) |
| Gross Profit Growth | YoY change in Revenue minus COGS |
| Operating Income Growth | YoY change in income from operations |
| Net Income Growth | YoY change in bottom-line profit |

## Analysis Tips

1. **Revenue vs Net Income divergence**: If Net Income grows faster than Revenue, the company is improving margins or reducing costs.

2. **Operating leverage**: When Operating Income grows faster than Revenue, fixed costs are being spread over more sales.

3. **Margin compression**: If Cost of Revenue grows faster than Revenue, margins are declining.

4. **Consistency**: Look for companies with consistent positive growth across all metrics.

5. **Trend reversals**: A switch from negative to positive growth often signals a turnaround.
