---
name: sec-annual-comparison
description: Compare key metrics and disclosures between annual 10-K filings using Octagon MCP. Use when analyzing year-over-year changes in financials, risk factors, business descriptions, and strategic priorities across fiscal years.
---

# SEC Annual Comparison

Compare key metrics and risk factors between current and previous year 10-K filings for public companies using the Octagon MCP server.

## Prerequisites

Ensure Octagon MCP is configured in your AI agent (Cursor, Claude Desktop, Windsurf, etc.). See [references/mcp-setup.md](references/mcp-setup.md) for installation instructions.

## Workflow

### 1. Identify Analysis Parameters

Determine the following before querying:
- **Ticker**: Stock symbol (e.g., AAPL, MSFT, GOOGL)
- **Years** (optional): Specific fiscal years to compare
- **Focus Areas** (optional): Financials, risks, segments, strategy

### 2. Execute Query via Octagon MCP

Use the `octagon-agent` tool with a natural language prompt:

```
Compare key metrics and risk factors between <TICKER>'s current and previous year 10-K filings.
```

**MCP Call Format:**

```json
{
  "server": "octagon-mcp",
  "toolName": "octagon-agent",
  "arguments": {
    "prompt": "Compare key metrics and risk factors between CRM's current and previous year 10-K filings."
  }
}
```

### 3. Expected Output

The agent returns structured year-over-year comparison including:

**Financial Metrics:**
- Revenue: $31.353B (FY2023) vs $26.492B (FY2022) - 18.59% growth
- Net Income: $208M (FY2023) vs $1.444B (FY2022) - significant decline
- Total Assets: $98.849B vs $95.209B
- Total Liabilities: $41.755B vs $37.076B

**Key Changes:**
- $1.2B impairment of customer relationships and acquisition assets
- Increased goodwill from acquisitions (Slack, Acumen, Vlocity)
- Debt at $10.682B, covenant compliant

**Risk Factors:**
- Operational, regulatory, financial, market volatility risks
- Industry competition risks

**Data Sources**: octagon-financials-agent, octagon-sec-agent

### 4. Interpret Results

See [references/interpreting-results.md](references/interpreting-results.md) for guidance on:
- Understanding year-over-year trends
- Identifying significant changes
- Evaluating risk factor evolution
- Assessing strategic shifts

## Example Queries

**Full Annual Comparison:**
```
Compare key metrics and risk factors between CRM's current and previous year 10-K filings.
```

**Multi-Year Trend:**
```
Compare AAPL's financial performance across the last 3 fiscal years from 10-K filings.
```

**Risk Factor Evolution:**
```
How have TSLA's risk factors changed between FY2024 and FY2023 10-K filings?
```

**Segment Comparison:**
```
Compare revenue segment breakdown between GOOGL's FY2024 and FY2023 10-K filings.
```

**Strategic Changes:**
```
Compare the business description and strategy sections between MSFT's current and prior year 10-K.
```

**Margin Analysis:**
```
Compare gross margin and operating margin trends between NVDA's FY2024 and FY2023 10-K filings.
```

## Comparison Framework

### Financial Metrics

| Category | Key Metrics |
|----------|-------------|
| Revenue | Total revenue, growth rate, segment breakdown |
| Profitability | Gross profit, operating income, net income |
| Margins | Gross margin, operating margin, net margin |
| Balance Sheet | Assets, liabilities, equity, cash, debt |
| Cash Flow | Operating, investing, financing, free cash flow |
| Per Share | EPS, book value, dividends |

### Operational Metrics

| Category | Key Metrics |
|----------|-------------|
| Customers | Count, retention, concentration |
| Employees | Headcount, productivity |
| Geographic | Revenue by region, asset location |
| Segments | Business unit performance |

### Risk Factors

| Category | What to Compare |
|----------|-----------------|
| Business | Competitive, operational, strategic |
| Financial | Liquidity, debt, currency |
| Regulatory | Compliance, legal |
| Market | Economic, industry |
| Technology | Innovation, disruption |

### Strategic Elements

| Category | What to Compare |
|----------|-----------------|
| Mission | Corporate purpose |
| Strategy | Growth initiatives |
| Investments | R&D, CapEx, M&A |
| Markets | Geographic, product expansion |

## Year-over-Year Analysis

### Financial Trend Assessment

| Metric | Positive Trend | Negative Trend |
|--------|----------------|----------------|
| Revenue | Growing, accelerating | Declining, slowing |
| Margins | Expanding | Contracting |
| Earnings | Increasing | Decreasing |
| Cash Flow | Strengthening | Weakening |
| Debt | Declining | Increasing |

### Key Ratios to Track

| Ratio | Calculation | What It Shows |
|-------|-------------|---------------|
| Revenue Growth | (Current - Prior) / Prior | Top-line momentum |
| Gross Margin | Gross Profit / Revenue | Pricing power, costs |
| Operating Margin | Operating Income / Revenue | Operational efficiency |
| Net Margin | Net Income / Revenue | Bottom-line profitability |
| ROE | Net Income / Equity | Shareholder returns |
| Debt/Equity | Total Debt / Equity | Financial leverage |

### Change Analysis

| Change Type | Significance |
|-------------|--------------|
| >20% improvement | Major positive development |
| 5-20% improvement | Solid progress |
| ±5% | Stable/flat |
| 5-20% decline | Concerning deterioration |
| >20% decline | Material negative change |

## Risk Factor Comparison

### Types of Changes

| Change | What It Means |
|--------|---------------|
| New risk added | Emerging concern |
| Risk removed | Issue resolved or de-emphasized |
| Language expanded | Increased concern |
| Language reduced | Diminished concern |
| Position changed | Priority shift |
| Specificity added | Crystallizing risk |

### Priority Assessment

| Position | Prior Year | Current Year | Interpretation |
|----------|------------|--------------|----------------|
| Top 5 | Top 5 | Top 5 | Persistent priority |
| Lower | Lower | Top 5 | Elevated concern |
| Top 5 | Top 5 | Lower | Reduced priority |
| None | None | Added | New risk |
| Present | Present | Removed | Resolved |

## Business Description Changes

### What to Track

| Section | Changes to Note |
|---------|-----------------|
| Products | New offerings, discontinued products |
| Markets | Geographic expansion, exits |
| Customers | Target market shifts |
| Competition | New competitors, changed positioning |
| Strategy | New initiatives, changed priorities |
| Technology | Platform changes, R&D focus |

### Strategic Shifts

| Indicator | Examples |
|-----------|----------|
| New emphasis | Repeated new terms |
| Removed emphasis | Topics no longer discussed |
| Changed language | Different framing |
| Quantification | New metrics disclosed |
| Commitment | Specific targets stated |

## Segment Performance Comparison

### Revenue Analysis

| Segment | Prior Year | Current Year | Growth | Mix Change |
|---------|------------|--------------|--------|------------|
| Segment A | $X | $Y | Z% | +/- pp |
| Segment B | $X | $Y | Z% | +/- pp |

### Segment Health Indicators

| Indicator | Positive | Negative |
|-----------|----------|----------|
| Growth | Accelerating | Decelerating |
| Margin | Improving | Declining |
| Share of Total | Increasing (if healthy) | Declining |
| Investment | Increasing | Divesting |

## Multi-Year Trend Analysis

### 3-5 Year Comparison

Track over extended periods:
- Revenue CAGR
- Margin trajectories
- Balance sheet evolution
- Risk factor patterns
- Strategic consistency

### Inflection Points

| Signal | What Changed |
|--------|--------------|
| Growth acceleration | New product, market |
| Margin expansion | Scale, efficiency |
| Cash flow improvement | Working capital, CapEx |
| Risk emergence | New competitive threat |
| Strategic pivot | Changed direction |

## Analysis Tips

1. **Start with financials**: Numbers provide objective comparison base.

2. **Read both MD&As**: Management commentary reveals context.

3. **Track risk factor order**: Position indicates priority.

4. **Note new disclosures**: First-time mentions often significant.

5. **Compare segment detail**: Business unit changes reveal strategy.

6. **Check footnote changes**: Accounting policy shifts matter.

## Use Cases

- **Investment research**: Understand company trajectory
- **Due diligence**: Track performance evolution
- **Competitive analysis**: Compare across competitors
- **Risk monitoring**: Identify emerging concerns
- **Earnings analysis**: Context for quarterly results
