---
name: ratings-snapshot
description: Retrieve ratings snapshot with overall rating and key metric scores including DCF, ROE, ROA, Debt-to-Equity, P/E, and P/B for public companies. Use when screening stocks, comparing quality metrics, or quick fundamental assessment.
---

# Ratings Snapshot

Retrieve ratings snapshot with overall rating and key metric scores for public companies using Octagon MCP.

## Prerequisites

Ensure Octagon MCP is configured in your AI agent (Cursor, Claude Desktop, Windsurf, etc.). See [references/mcp-setup.md](references/mcp-setup.md) for installation instructions.

## Query Format

```
Retrieve a ratings snapshot with overall rating and key metric scores (DCF, ROE, ROA, Debt-to-Equity, P/E, P/B) for <TICKER(S)>, limited to <N> records.
```

**MCP Call:**

```json
{
  "server": "octagon-mcp",
  "toolName": "octagon-agent",
  "arguments": {
    "prompt": "Retrieve a ratings snapshot with overall rating and key metric scores (DCF, ROE, ROA, Debt-to-Equity, P/E, P/B) for AAPL, MSFT, GOOGL, limited to 10 records"
  }
}
```

## Output Format

The agent returns a table with rating scores:

| Metric | Score |
|--------|-------|
| Overall Rating | B |
| Discounted Cash Flow (DCF) | 3 |
| Return on Equity (ROE) | 5 |
| Return on Assets (ROA) | 5 |
| Debt-to-Equity | 1 |
| Price-to-Earnings (P/E) | 2 |
| Price-to-Book (P/B) | 1 |

**Data Sources:** octagon-financials-agent, octagon-stock-data-agent

## Metrics Reference

| Metric | What It Measures | Higher Score Means |
|--------|------------------|-------------------|
| Overall Rating | Composite assessment (A-F or similar) | Better overall quality |
| DCF Score | Intrinsic value vs market price | More undervalued |
| ROE Score | Return on shareholder equity | Better profitability |
| ROA Score | Return on total assets | Better asset efficiency |
| Debt-to-Equity | Leverage assessment | Lower leverage (better) |
| P/E Score | Earnings valuation | More attractive valuation |
| P/B Score | Book value valuation | More attractive valuation |

## Score Interpretation

### Overall Rating Scale
| Rating | Interpretation |
|--------|----------------|
| A | Excellent - Top quality |
| B | Good - Above average |
| C | Average - Moderate quality |
| D | Below Average - Concerns present |
| F | Poor - Significant issues |

### Component Scores (typically 1-5)
| Score | Interpretation |
|-------|----------------|
| 5 | Excellent - Top quintile |
| 4 | Good - Above average |
| 3 | Average - Middle of pack |
| 2 | Below Average - Bottom half |
| 1 | Poor - Bottom quintile |

## Analysis Tips

### Quick Screening
Use ratings for initial filtering:
- Focus on A/B overall ratings
- Look for multiple high component scores
- Flag low scores for investigation

### Identify Strengths and Weaknesses
Component analysis reveals:
- High ROE + High ROA = Efficient operator
- Low D/E = Conservative financing
- Low P/E + Low P/B = Value candidate
- High DCF = Potentially undervalued

### Peer Comparison
Compare ratings across competitors:
- Same industry normalization important
- Relative ranking within sector
- Identify best-in-class

### Value vs Quality Trade-off
Different profiles:
- High profitability + High valuation = Quality premium
- Low profitability + Low valuation = Value trap risk
- High profitability + Low valuation = Potential opportunity

## Component Deep Dives

### DCF (Discounted Cash Flow)
- Compares intrinsic value to market price
- High score = stock appears undervalued
- Based on cash flow projections

### ROE (Return on Equity)
- Net Income / Shareholders' Equity
- Measures profit per dollar of equity
- Industry-relative comparison important

### ROA (Return on Assets)
- Net Income / Total Assets
- Measures profit per dollar of assets
- Lower for asset-heavy industries

### Debt-to-Equity
- Total Debt / Shareholders' Equity
- Lower = less financial risk
- Industry norms vary significantly

### P/E (Price-to-Earnings)
- Stock Price / Earnings Per Share
- Lower may indicate value
- Compare to growth rate (PEG)

### P/B (Price-to-Book)
- Market Cap / Book Value
- Lower may indicate value
- Less relevant for asset-light companies

## Follow-up Queries

Based on results, suggest deeper analysis:

- "What specific ratings criteria are used to calculate these scores?"
- "Are there historical trends in these metrics for [COMPANY]?"
- "What is the methodology for calculating the overall rating from component scores?"
- "Compare detailed financial metrics for [TICKER1] vs [TICKER2]"
