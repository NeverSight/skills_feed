---
name: sec-risk-factors
description: Extract and summarize risk factors from SEC filings using Octagon MCP. Use when analyzing Item 1A risk disclosures, categorizing business risks, identifying new or material risks, and comparing risk profiles across companies or time periods.
---

# SEC Risk Factors Analysis

Extract and summarize risk factors from SEC filings (10-K and 10-Q) for public companies using the Octagon MCP server.

## Prerequisites

Ensure Octagon MCP is configured in your AI agent (Cursor, Claude Desktop, Windsurf, etc.). See [references/mcp-setup.md](references/mcp-setup.md) for installation instructions.

## Workflow

### 1. Identify Analysis Parameters

Determine the following before querying:
- **Ticker**: Stock symbol (e.g., AAPL, MSFT, GOOGL)
- **Filing Type** (optional): 10-K (annual) or 10-Q (quarterly updates)
- **Focus Areas** (optional): Specific risk categories of interest

### 2. Execute Query via Octagon MCP

Use the `octagon-agent` tool with a natural language prompt:

```
Extract and summarize the risk factors section from <TICKER>'s latest annual report.
```

**MCP Call Format:**

```json
{
  "server": "octagon-mcp",
  "toolName": "octagon-agent",
  "arguments": {
    "prompt": "Extract and summarize the risk factors section from AAPL's latest annual report."
  }
}
```

### 3. Expected Output

The agent returns categorized risk factors including:

| Risk Category | Description | Source Pages |
|---------------|-------------|--------------|
| Macroeconomic & Industry Risks | Economic downturns, inflation, currency | 10-K, p.8 |
| Legal & Regulatory Compliance | Legal proceedings, regulatory challenges | 10-K, p.15-16 |
| Financial Risks | Pricing pressures, competition, FX volatility | 10-K, p.18-31 |
| Business Risks | Product transitions, competitiveness | 10-K, p.11 |
| Operational Risks | Manufacturing, logistics, outsourcing | 10-K, p.11 |
| Data Security & Privacy | Cybersecurity, data protection | 10-K, p.18 |
| Supply Chain Risks | Geopolitical tensions, natural disasters | 10-K, p.9 |

**Data Sources**: octagon-sec-agent

### 4. Interpret Results

See [references/interpreting-results.md](references/interpreting-results.md) for guidance on:
- Understanding risk factor categories
- Assessing risk materiality
- Comparing risks across filings
- Identifying new or emerging risks

## Example Queries

**Standard Risk Factor Extraction:**
```
Extract and summarize the risk factors section from AAPL's latest annual report.
```

**Quarterly Risk Updates:**
```
Extract any new or updated risk factors from TSLA's latest 10-Q filing.
```

**Specific Risk Category:**
```
Extract cybersecurity and data privacy risk factors from META's latest 10-K.
```

**Comparative Analysis:**
```
Compare the risk factors between GOOGL's 2024 and 2023 10-K filings.
```

**Industry Comparison:**
```
Extract and compare supply chain risk factors from AAPL and MSFT's latest 10-K filings.
```

**Regulatory Focus:**
```
Extract all regulatory and legal compliance risk factors from JPM's latest annual report.
```

## Risk Factor Categories

### Macroeconomic Risks

| Risk Type | Examples |
|-----------|----------|
| Economic Cycles | Recessions, GDP decline, consumer spending |
| Inflation | Input costs, pricing power, margin pressure |
| Interest Rates | Borrowing costs, valuation impacts |
| Currency | FX volatility, translation effects |
| Geopolitical | Trade wars, sanctions, political instability |

### Operational Risks

| Risk Type | Examples |
|-----------|----------|
| Supply Chain | Supplier concentration, logistics disruptions |
| Manufacturing | Production issues, quality control |
| Technology | System failures, IT infrastructure |
| Human Capital | Key personnel, labor relations |
| Business Continuity | Natural disasters, pandemics |

### Financial Risks

| Risk Type | Examples |
|-----------|----------|
| Liquidity | Cash flow, access to capital |
| Credit | Counterparty risk, receivables |
| Market | Stock price volatility, valuation |
| Tax | Rate changes, audit exposure |
| Pension | Funding obligations, assumptions |

### Regulatory & Legal Risks

| Risk Type | Examples |
|-----------|----------|
| Compliance | Industry regulations, licensing |
| Litigation | Lawsuits, class actions |
| Antitrust | Competition law, market dominance |
| Data Privacy | GDPR, CCPA, data breaches |
| Environmental | ESG regulations, climate policies |

### Strategic Risks

| Risk Type | Examples |
|-----------|----------|
| Competition | Market share, pricing pressure |
| Disruption | Technology shifts, new entrants |
| M&A | Integration risks, deal failure |
| Innovation | R&D success, product pipeline |
| Reputation | Brand damage, public perception |

## Analyzing Risk Changes

### New Risks (High Priority)

Risks added since prior filing:
- Indicates emerging concerns
- Often reflects recent events
- May signal strategic shifts

### Removed Risks (Monitor)

Risks no longer disclosed:
- Issue may be resolved
- Or consolidated into other risks
- Verify resolution in MD&A

### Modified Language (Important)

Risks with changed wording:
- Expanded = increased concern
- Reduced = diminished concern
- More specific = crystallizing risk

## Analysis Tips

1. **Order matters**: Risks are typically ordered by perceived materiality - first risks are often most significant.

2. **Length signals importance**: More detailed risk descriptions often indicate greater management concern.

3. **Specificity is key**: Specific examples suggest real concerns vs. boilerplate language.

4. **Cross-reference MD&A**: Management discussion often provides context for risk factors.

5. **Track changes YoY**: New, removed, or modified risks reveal evolving concerns.

6. **Compare to peers**: Unique risks vs. industry-standard disclosures indicate company-specific issues.

## Use Cases

- **Investment due diligence**: Comprehensive risk assessment before investing
- **Portfolio risk monitoring**: Track risk evolution for holdings
- **Competitive analysis**: Compare risk profiles across competitors
- **Sector research**: Identify common vs. unique risks in an industry
- **Compliance review**: Ensure adequate risk disclosure
