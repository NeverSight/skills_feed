---
name: sec-10k-analysis
description: Analyze 10-K annual filings for public companies using Octagon MCP. Use when extracting key financial metrics, risk factors, business overview, management discussion, and regulatory disclosures from SEC 10-K filings.
---

# SEC 10-K Analysis

Analyze annual 10-K filings for public companies to extract key financial metrics, risk factors, and business insights using the Octagon MCP server.

## Prerequisites

Ensure Octagon MCP is configured in your AI agent (Cursor, Claude Desktop, Windsurf, etc.). See [references/mcp-setup.md](references/mcp-setup.md) for installation instructions.

## Workflow

### 1. Identify Analysis Parameters

Determine the following before querying:
- **Ticker**: Stock symbol (e.g., AAPL, MSFT, GOOGL)
- **Filing Year** (optional): Specific fiscal year if not latest
- **Focus Areas** (optional): Financial metrics, risk factors, business segments, etc.

### 2. Execute Query via Octagon MCP

Use the `octagon-agent` tool with a natural language prompt:

```
Analyze the latest 10-K filing for <TICKER> and extract key financial metrics and risk factors.
```

**MCP Call Format:**

```json
{
  "server": "octagon-mcp",
  "toolName": "octagon-agent",
  "arguments": {
    "prompt": "Analyze the latest 10-K filing for AAPL and extract key financial metrics and risk factors."
  }
}
```

### 3. Expected Output

The agent returns comprehensive 10-K analysis including:

**Financial Metrics:**
- Total Revenues
- Net Income
- Total Assets
- Total Liabilities
- Cash Flows (Operating, Investing, Financing)

**Risk Factors:**
- Macroeconomic risks
- Operational risks
- Regulatory risks
- Cybersecurity threats
- Supply chain dependencies

**Source Citations:**
- Specific page references from the 10-K filing

**Data Sources**: octagon-financials-agent, octagon-sec-agent

### 4. Interpret Results

See [references/interpreting-results.md](references/interpreting-results.md) for guidance on:
- Understanding 10-K structure and sections
- Analyzing risk factor disclosures
- Comparing YoY changes in filings
- Identifying material changes

## Example Queries

**Standard 10-K Analysis:**
```
Analyze the latest 10-K filing for AAPL and extract key financial metrics and risk factors.
```

**Risk Factor Focus:**
```
Extract and summarize all risk factors from TSLA's latest 10-K filing.
```

**Business Segment Analysis:**
```
Analyze the business segment disclosures in MSFT's latest 10-K filing.
```

**Management Discussion:**
```
Extract the Management Discussion and Analysis (MD&A) section from AMZN's latest 10-K.
```

**Historical Comparison:**
```
Compare key financial metrics between GOOGL's 2024 and 2023 10-K filings.
```

**Specific Section Extraction:**
```
Extract the legal proceedings section from META's latest 10-K filing.
```

## 10-K Filing Structure

| Section | Content |
|---------|---------|
| Part I, Item 1 | Business Overview |
| Part I, Item 1A | Risk Factors |
| Part I, Item 1B | Unresolved Staff Comments |
| Part I, Item 2 | Properties |
| Part I, Item 3 | Legal Proceedings |
| Part II, Item 5 | Market Information |
| Part II, Item 6 | Selected Financial Data |
| Part II, Item 7 | MD&A (Management Discussion & Analysis) |
| Part II, Item 7A | Quantitative & Qualitative Disclosures |
| Part II, Item 8 | Financial Statements |
| Part II, Item 9A | Controls and Procedures |

## Key Metrics to Extract

| Metric | Location | Importance |
|--------|----------|------------|
| Total Revenue | Income Statement | Top-line performance |
| Net Income | Income Statement | Bottom-line profitability |
| Total Assets | Balance Sheet | Company size/resources |
| Total Liabilities | Balance Sheet | Debt obligations |
| Operating Cash Flow | Cash Flow Statement | Cash generation |
| Free Cash Flow | Cash Flow Statement | Available cash |
| Segment Revenue | Notes | Business mix |

## Risk Factor Categories

Common risk categories disclosed in 10-K filings:

| Category | Examples |
|----------|----------|
| Macroeconomic | Economic downturns, inflation, interest rates |
| Operational | Supply chain, manufacturing, quality control |
| Regulatory | Government regulation, compliance, legal |
| Competitive | Market competition, pricing pressure |
| Technology | Cybersecurity, IP protection, obsolescence |
| Financial | Foreign exchange, credit, liquidity |
| Strategic | M&A integration, market expansion |

## Analysis Tips

1. **Compare to prior year**: Look for new risk factors or removed ones - changes signal shifting concerns.

2. **Read MD&A carefully**: Management's discussion often provides context not in the numbers.

3. **Check auditor opinion**: Located in Item 8, indicates any concerns about financial statements.

4. **Review legal proceedings**: Item 3 discloses ongoing litigation that could impact financials.

5. **Segment analysis**: Breakdown by segment reveals which businesses drive growth or drag performance.

6. **Cross-reference with 10-Q**: Quarterly filings may have more recent updates.

## Use Cases

- **Due diligence**: Comprehensive review before investment decisions
- **Risk assessment**: Identify company-specific and industry risks
- **Competitive analysis**: Compare disclosures across industry peers
- **Earnings prep**: Understand company context before earnings calls
- **Compliance review**: Verify disclosure completeness
