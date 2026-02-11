---
name: financial-health-scores
description: Retrieve financial health scores including Altman Z-Score and Piotroski Score for public companies. Use when assessing bankruptcy risk, financial strength, value investing screening, or credit quality analysis.
---

# Financial Health Scores

Retrieve financial health scores including Altman Z-Score and Piotroski Score for public companies using Octagon MCP.

## Prerequisites

Ensure Octagon MCP is configured in your AI agent (Cursor, Claude Desktop, Windsurf, etc.). See [references/mcp-setup.md](references/mcp-setup.md) for installation instructions.

## Query Format

```
Retrieve financial health scores for <TICKER>, including the Altman Z-Score and Piotroski Score.
```

**MCP Call:**

```json
{
  "server": "octagon-mcp",
  "toolName": "octagon-agent",
  "arguments": {
    "prompt": "Retrieve financial health scores for TSLA, including the Altman Z-Score and Piotroski Score"
  }
}
```

## Output Format

The agent returns health scores with supporting metrics:

**Altman Z-Score:** 16.84 (calculated using working capital, total assets, retained earnings, EBIT, and market cap). A score above 3.0 indicates low bankruptcy risk.

**Piotroski Score:** 6 (out of a maximum 9). This score assesses profitability, leverage, liquidity, and operating efficiency.

**Supporting Financial Metrics:**

| Metric | Value (USD) |
|--------|-------------|
| Working Capital | 36,928,000,000 |
| Total Assets | 137,806,000,000 |
| Retained Earnings | 39,003,000,000 |
| EBIT | 5,616,000,000 |
| Market Cap | 1,400,635,834,800 |
| Total Liabilities | 54,941,000,000 |
| Revenue | 94,827,000,000 |

**Data Source:** octagon-financials-agent

## Altman Z-Score Interpretation

The Altman Z-Score predicts bankruptcy probability:

| Z-Score Range | Interpretation |
|---------------|----------------|
| > 3.0 | Safe Zone - Low bankruptcy risk |
| 1.8 - 3.0 | Grey Zone - Moderate risk, needs monitoring |
| < 1.8 | Distress Zone - High bankruptcy risk |

### Z-Score Formula
```
Z = 1.2(WC/TA) + 1.4(RE/TA) + 3.3(EBIT/TA) + 0.6(MC/TL) + 1.0(Rev/TA)
```
Where:
- WC = Working Capital
- TA = Total Assets
- RE = Retained Earnings
- EBIT = Earnings Before Interest and Taxes
- MC = Market Cap
- TL = Total Liabilities
- Rev = Revenue

## Piotroski Score Interpretation

The Piotroski F-Score (0-9) assesses financial strength:

| Score Range | Interpretation |
|-------------|----------------|
| 8-9 | Strong - High quality value stock |
| 5-7 | Moderate - Average financial health |
| 0-4 | Weak - Poor financial health |

### Piotroski Components (9 criteria)

**Profitability (4 points):**
1. Positive Net Income
2. Positive Operating Cash Flow
3. Return on Assets improvement
4. OCF > Net Income (accruals quality)

**Leverage/Liquidity (3 points):**
5. Lower long-term debt ratio
6. Higher current ratio
7. No new share issuance

**Operating Efficiency (2 points):**
8. Higher gross margin
9. Higher asset turnover

## Analysis Tips

### Combined Assessment
Use both scores together:
- High Z-Score + High Piotroski = Financially healthy
- High Z-Score + Low Piotroski = Watch operating trends
- Low Z-Score + High Piotroski = Leverage concern
- Low Z-Score + Low Piotroski = Avoid or deep value

### Value Investing Application
Piotroski Score designed for:
- Screening high book-to-market stocks
- Identifying quality within value
- Avoiding value traps

### Credit Analysis
Z-Score useful for:
- Bond investment decisions
- Supplier credit assessment
- Counterparty risk evaluation

### Sector Considerations
Scores work best for:
- Manufacturing companies (Z-Score original use)
- Mature businesses with stable operations
- Less reliable for: financials, early-stage, asset-light

## Follow-up Queries

Based on results, suggest deeper analysis:

- "What factors contributed to [COMPANY]'s Piotroski Score versus industry peers?"
- "How does [COMPANY]'s Altman Z-Score compare to its historical averages?"
- "Break down the individual components of [COMPANY]'s Piotroski Score"
- "Compare [COMPANY]'s financial health scores to [PEER1] and [PEER2]"
