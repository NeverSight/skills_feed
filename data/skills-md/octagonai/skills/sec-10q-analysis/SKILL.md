---
name: sec-10q-analysis
description: Analyze 10-Q quarterly filings for public companies using Octagon MCP. Use when extracting quarterly performance metrics, revenue breakdown, operating margins, segment performance, and interim financial updates from SEC 10-Q filings.
---

# SEC 10-Q Analysis

Analyze quarterly 10-Q filings for public companies to extract quarterly performance metrics, segment breakdown, and interim financial updates using the Octagon MCP server.

## Prerequisites

Ensure Octagon MCP is configured in your AI agent (Cursor, Claude Desktop, Windsurf, etc.). See [references/mcp-setup.md](references/mcp-setup.md) for installation instructions.

## Workflow

### 1. Identify Analysis Parameters

Determine the following before querying:
- **Ticker**: Stock symbol (e.g., AAPL, MSFT, GOOGL)
- **Quarter** (optional): Specific quarter if not latest (Q1, Q2, Q3)
- **Focus Areas** (optional): Revenue, margins, segment performance, etc.

### 2. Execute Query via Octagon MCP

Use the `octagon-agent` tool with a natural language prompt:

```
Analyze the latest 10-Q filing for <TICKER> and extract quarterly performance metrics.
```

**MCP Call Format:**

```json
{
  "server": "octagon-mcp",
  "toolName": "octagon-agent",
  "arguments": {
    "prompt": "Analyze the latest 10-Q filing for AAPL and extract quarterly performance metrics."
  }
}
```

### 3. Expected Output

The agent returns comprehensive 10-Q analysis including:

**Quarterly Metrics:**
- Total Revenue (with YoY comparison)
- Net Income
- Basic and Diluted EPS
- Operating Income and Margin
- Segment Revenue Breakdown

**Balance Sheet Updates:**
- Cash and Equivalents
- Long-term Debt
- Liquidity Position

**Source Citations:**
- Specific page references from the 10-Q filing

**Data Sources**: octagon-financials-agent, octagon-sec-agent

### 4. Interpret Results

See [references/interpreting-results.md](references/interpreting-results.md) for guidance on:
- Understanding quarterly vs annual comparisons
- Analyzing segment performance
- Identifying sequential trends
- Comparing to analyst expectations

## Example Queries

**Standard 10-Q Analysis:**
```
Analyze the latest 10-Q filing for AAPL and extract quarterly performance metrics.
```

**Segment Performance:**
```
Extract product segment revenue breakdown from AAPL's latest 10-Q filing.
```

**Margin Analysis:**
```
Analyze operating and gross margins from MSFT's Q2 2024 10-Q filing.
```

**YoY Comparison:**
```
Compare GOOGL's Q3 2024 quarterly metrics to Q3 2023 from 10-Q filings.
```

**Cash Flow Focus:**
```
Extract quarterly cash flow metrics from AMZN's latest 10-Q filing.
```

**Guidance Updates:**
```
Extract any updated guidance or outlook from META's latest 10-Q filing.
```

## 10-Q Filing Structure

| Section | Content |
|---------|---------|
| Part I, Item 1 | Financial Statements (Unaudited) |
| Part I, Item 2 | MD&A (Management Discussion & Analysis) |
| Part I, Item 3 | Quantitative & Qualitative Disclosures |
| Part I, Item 4 | Controls and Procedures |
| Part II, Item 1 | Legal Proceedings |
| Part II, Item 1A | Risk Factors (Updates) |
| Part II, Item 2 | Unregistered Sales of Equity |
| Part II, Item 6 | Exhibits |

## Key Quarterly Metrics

| Metric | Description | Comparison |
|--------|-------------|------------|
| Revenue | Quarterly sales | YoY and QoQ |
| Net Income | Quarterly profit | YoY and QoQ |
| EPS (Basic) | Earnings per share | vs Estimates |
| EPS (Diluted) | Diluted EPS | vs Estimates |
| Operating Income | Income from operations | Margin trend |
| Gross Margin | Gross profit / Revenue | vs Prior quarter |
| Operating Margin | Operating income / Revenue | vs Prior quarter |

## Segment Analysis

Common segment breakdowns in 10-Q filings:

| Company | Typical Segments |
|---------|------------------|
| AAPL | iPhone, Mac, iPad, Services, Wearables |
| MSFT | Productivity, Intelligent Cloud, Personal Computing |
| GOOGL | Google Services, Google Cloud, Other Bets |
| AMZN | North America, International, AWS |
| META | Family of Apps, Reality Labs |

## 10-Q vs 10-K Differences

| Aspect | 10-Q | 10-K |
|--------|------|------|
| Frequency | Quarterly (Q1, Q2, Q3) | Annual |
| Financials | Unaudited | Audited |
| Detail Level | Summary | Comprehensive |
| Risk Factors | Updates only | Full disclosure |
| MD&A | Quarterly focus | Annual review |

## Analysis Tips

1. **Sequential comparison**: Compare Q2 to Q1 (QoQ) not just YoY for trend insights.

2. **Seasonality awareness**: Some businesses have strong seasonal patterns - compare to same quarter prior year.

3. **Guidance updates**: Check MD&A for any updated full-year guidance.

4. **Risk factor changes**: Part II Item 1A only includes changes - review for new concerns.

5. **Segment mix shifts**: Watch for changes in segment contribution to total revenue.

6. **Margin trends**: Operating margin changes can signal pricing or cost pressures.

## Use Cases

- **Earnings analysis**: Detailed breakdown after quarterly earnings
- **Trend tracking**: Monitor sequential quarter performance
- **Estimate validation**: Compare actual results to analyst estimates
- **Guidance monitoring**: Track any guidance updates or revisions
- **Competitive tracking**: Compare quarterly performance across peers
