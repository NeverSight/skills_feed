---
name: historical-financial-ratings
description: Retrieve historical financial ratings and key metric scores over time using Octagon MCP. Use when analyzing overall ratings, return on assets, return on equity, discounted cash flow scores, debt-to-equity scores, and letter grades (A+, A, B, etc.) for any public company.
---

# Historical Financial Ratings

Retrieve and analyze historical financial ratings and key metric scores over time for public companies using the Octagon MCP server.

## Prerequisites

Ensure Octagon MCP is configured in your AI agent (Cursor, Claude Desktop, Windsurf, etc.). See [references/mcp-setup.md](references/mcp-setup.md) for installation instructions.

## Workflow

### 1. Identify Analysis Parameters

Determine the following before querying:
- **Ticker**: Stock symbol (e.g., NVDA, AAPL, MSFT)
- **Records**: Number of historical data points to retrieve (e.g., 100, 500, 2000)

### 2. Execute Query via Octagon MCP

Use the `octagon-agent` tool with a natural language prompt:

```
Retrieve historical financial ratings and key metric scores over time for <TICKER>, limited to <N> records.
```

**MCP Call Format:**

```json
{
  "server": "octagon-mcp",
  "toolName": "octagon-agent",
  "arguments": {
    "prompt": "Retrieve historical financial ratings and key metric scores over time for NVDA, limited to 2000 records."
  }
}
```

### 3. Expected Output

The agent returns historical ratings data including:

| Date | Overall Score | Overall Rating | ROA Score | ROE Score | DCF Score | D/E Score |
|------|---------------|----------------|-----------|-----------|-----------|-----------|
| 2024-01-15 | 5 | A+ | 4 | 4 | 3 | 3 |
| 2024-01-08 | 5 | A+ | 4 | 4 | 3 | 3 |
| 2023-12-29 | 5 | A | 4 | 3 | 3 | 3 |
| ... | ... | ... | ... | ... | ... | ... |

**Data Sources**: octagon-financials-agent

### 4. Interpret Results

See [references/interpreting-results.md](references/interpreting-results.md) for guidance on:
- Understanding overall scores and ratings
- Analyzing individual metric scores
- Identifying rating trends and changes
- Spotting financial health improvements or deterioration

## Example Queries

**Standard Historical Analysis:**
```
Retrieve historical financial ratings and key metric scores over time for NVDA, limited to 2000 records.
```

**Recent Ratings Focus:**
```
Retrieve historical financial ratings and key metric scores over time for AAPL, limited to 100 records.
```

**Extended Historical View:**
```
Retrieve historical financial ratings and key metric scores over time for MSFT, limited to 5000 records.
```

## Key Metrics Explained

| Metric | Definition | Score Range |
|--------|------------|-------------|
| Overall Score | Composite financial health rating | 1-5 (5 = best) |
| Overall Rating | Letter grade for financial health | A+ to F |
| ROA Score | Return on Assets efficiency | 1-5 (5 = best) |
| ROE Score | Return on Equity efficiency | 1-5 (5 = best) |
| DCF Score | Discounted Cash Flow valuation score | 1-5 (5 = best) |
| D/E Score | Debt-to-Equity health | 1-5 (5 = lowest debt) |

## Analysis Tips

1. **Consistent high scores**: Companies maintaining 5-star overall scores and A+ ratings over extended periods demonstrate stable financial excellence.

2. **Score improvements**: Watch for upward trends in individual metrics (ROA, ROE) as indicators of improving operational efficiency.

3. **Debt management**: A stable or improving D/E score suggests the company is managing leverage responsibly.

4. **Rating downgrades**: Sudden drops in overall rating (e.g., A+ to B) warrant deeper investigation into financials.

5. **Diverging metrics**: If ROE is high but ROA is low, the company may be using significant leverage to boost returns.

## Use Cases

- **Investment screening**: Filter for companies with consistently high ratings
- **Risk monitoring**: Track rating changes for portfolio holdings
- **Due diligence**: Review historical financial health before investment decisions
- **Peer comparison**: Compare rating trajectories across competitors
