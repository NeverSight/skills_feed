---
name: sec-cash-flow-review
description: Extract and analyze cash flow trends and working capital changes from SEC filings using Octagon MCP. Use when researching operating cash flow, investing activities, financing activities, free cash flow, liquidity, and working capital dynamics from 10-K and 10-Q filings.
---

# SEC Cash Flow Review

Extract and analyze cash flow trends and working capital changes from SEC filings for public companies using the Octagon MCP server.

## Prerequisites

Ensure Octagon MCP is configured in your AI agent (Cursor, Claude Desktop, Windsurf, etc.). See [references/mcp-setup.md](references/mcp-setup.md) for installation instructions.

## Workflow

### 1. Identify Analysis Parameters

Determine the following before querying:
- **Ticker**: Stock symbol (e.g., AAPL, MSFT, GOOGL)
- **Filing Type** (optional): 10-K (annual) or 10-Q (quarterly)
- **Focus Area** (optional): Operating, investing, financing, working capital

### 2. Execute Query via Octagon MCP

Use the `octagon-agent` tool with a natural language prompt:

```
Extract and analyze cash flow trends and working capital changes from <TICKER>'s latest 10-Q.
```

**MCP Call Format:**

```json
{
  "server": "octagon-mcp",
  "toolName": "octagon-agent",
  "arguments": {
    "prompt": "Extract and analyze cash flow trends and working capital changes from NFLX's latest 10-Q."
  }
}
```

### 3. Expected Output

The agent returns structured cash flow analysis including:

**Cash Flow Trends:**
- Operating Cash Flow: Increased 37.87% YoY
- Investing Cash Flow: -$2.08B (CapEx, investments)
- Financing Cash Flow: Mixed ($1.04B inflow, -$2.18B outflow)

**Working Capital Changes:**
- Change in Working Capital: -$456M
- Cash and Equivalents: Decreased $1.193B in 6 months

**Key Observations:**
- Operating cash flow growth outpaces investing/financing
- Working capital contraction from content investments
- Liquidity sufficient for 12+ months

**Data Sources**: octagon-financials-agent, octagon-sec-agent, octagon-web-search-agent

### 4. Interpret Results

See [references/interpreting-results.md](references/interpreting-results.md) for guidance on:
- Understanding cash flow components
- Evaluating cash flow quality
- Analyzing working capital trends
- Assessing liquidity position

## Example Queries

**Full Cash Flow Analysis:**
```
Extract and analyze cash flow trends and working capital changes from NFLX's latest 10-Q.
```

**Free Cash Flow Focus:**
```
Calculate and analyze free cash flow trends for AAPL over the last 4 quarters.
```

**Working Capital Deep Dive:**
```
Analyze working capital changes and cash conversion cycle for AMZN from the latest 10-K.
```

**Liquidity Assessment:**
```
Evaluate TSLA's liquidity position and cash runway from the latest quarterly filing.
```

**CapEx Analysis:**
```
Extract capital expenditure trends and investment priorities from GOOGL's cash flow statement.
```

**Financing Activities:**
```
Analyze debt repayments, share buybacks, and dividend payments from MSFT's latest 10-K cash flow.
```

## Cash Flow Statement Components

### Operating Activities

| Component | Description |
|-----------|-------------|
| Net Income | Starting point |
| Depreciation/Amortization | Non-cash add-back |
| Stock Compensation | Non-cash expense |
| Deferred Taxes | Timing differences |
| Working Capital Changes | Current asset/liability changes |
| Other Adjustments | Non-cash items |

### Investing Activities

| Component | Description |
|-----------|-------------|
| Capital Expenditures | Property, equipment purchases |
| Acquisitions | Business combinations |
| Investment Purchases | Securities bought |
| Investment Sales | Securities sold |
| Asset Dispositions | Property, equipment sales |

### Financing Activities

| Component | Description |
|-----------|-------------|
| Debt Issuance | Borrowings |
| Debt Repayment | Principal payments |
| Share Issuance | Stock offerings |
| Share Repurchases | Buybacks |
| Dividends | Shareholder distributions |

## Key Cash Flow Metrics

### Profitability vs. Cash

| Metric | Calculation | What It Shows |
|--------|-------------|---------------|
| Operating Cash Flow | From statement | Cash from operations |
| Free Cash Flow | OCF - CapEx | Cash after investment |
| FCF Margin | FCF / Revenue | Cash generation rate |
| Cash Conversion | OCF / Net Income | Earnings quality |

### Liquidity Metrics

| Metric | Calculation | What It Shows |
|--------|-------------|---------------|
| Cash Position | Cash + equivalents | Available liquidity |
| Cash Runway | Cash / Monthly Burn | Months of runway |
| Quick Ratio | (Cash + Receivables) / Current Liabilities | Short-term coverage |
| Current Ratio | Current Assets / Current Liabilities | Working capital |

### Investment Metrics

| Metric | Calculation | What It Shows |
|--------|-------------|---------------|
| CapEx Intensity | CapEx / Revenue | Investment level |
| CapEx / D&A | CapEx / Depreciation | Maintenance vs. growth |
| Acquisition Spend | From investing | M&A activity |
| Investment Returns | Sales / Purchases | Portfolio activity |

## Working Capital Analysis

### Components

| Component | Increase Means | Decrease Means |
|-----------|----------------|----------------|
| Accounts Receivable | Cash used | Cash provided |
| Inventory | Cash used | Cash provided |
| Prepaid Expenses | Cash used | Cash provided |
| Accounts Payable | Cash provided | Cash used |
| Accrued Liabilities | Cash provided | Cash used |
| Deferred Revenue | Cash provided | Cash used |

### Cash Conversion Cycle

| Metric | Calculation |
|--------|-------------|
| Days Sales Outstanding | (AR / Revenue) × 365 |
| Days Inventory Outstanding | (Inventory / COGS) × 365 |
| Days Payables Outstanding | (AP / COGS) × 365 |
| Cash Conversion Cycle | DSO + DIO - DPO |

### Working Capital Trends

| Trend | Interpretation |
|-------|----------------|
| Declining CCC | Improved efficiency |
| Rising CCC | Cash tied up longer |
| Negative CCC | Customer-funded model |
| Stable CCC | Consistent operations |

## Cash Flow Quality Assessment

### Quality Indicators

| Factor | High Quality | Low Quality |
|--------|-------------|-------------|
| OCF vs. Net Income | OCF > NI | OCF < NI |
| Sustainability | Recurring sources | One-time items |
| Working Capital | Stable trends | Erratic changes |
| Non-Cash Charges | Reasonable D&A | Excessive add-backs |

### Red Flags

1. **OCF < Net Income persistently** - Earnings quality concern
2. **Negative FCF** - Cash consumption
3. **Rising receivables** - Collection issues
4. **Inventory buildup** - Demand weakness
5. **Declining payables** - Supplier pressure
6. **Heavy stock compensation** - Dilution concern

## Trend Analysis

### Period-over-Period

| Metric | Prior Period | Current | Change |
|--------|--------------|---------|--------|
| Operating CF | | | |
| Investing CF | | | |
| Financing CF | | | |
| Free Cash Flow | | | |
| Working Capital | | | |

### Multi-Year Trends

Track over time:
- OCF growth trajectory
- FCF conversion rate
- Working capital efficiency
- CapEx patterns
- Capital return trends

## Liquidity Assessment

### Cash Position Analysis

| Factor | Assessment |
|--------|------------|
| Absolute Level | Adequate for operations |
| Trend | Growing or declining |
| vs. Obligations | Coverage of debt, commitments |
| vs. Investment | Ability to fund growth |

### Runway Calculation

| Scenario | Calculation |
|----------|-------------|
| Conservative | Cash / Average Monthly Burn |
| Including Revolver | (Cash + Available Credit) / Burn |
| Stress | Cash / Peak Monthly Burn |

### Covenant Considerations

| Factor | What to Check |
|--------|---------------|
| Debt/EBITDA | Leverage limits |
| Interest Coverage | Payment ability |
| Minimum Cash | Required balances |
| CapEx Limits | Investment constraints |

## Financing Activity Analysis

### Capital Structure Changes

| Activity | Implication |
|----------|-------------|
| Debt Issuance | Leverage increase |
| Debt Repayment | Deleveraging |
| Equity Issuance | Dilution, capital raise |
| Buybacks | Return to shareholders |
| Dividends | Cash distribution |

### Capital Allocation Assessment

| Priority | What It Signals |
|----------|-----------------|
| Heavy CapEx | Growth investment |
| Heavy Buybacks | Mature, returning cash |
| Debt Focus | Deleveraging priority |
| M&A | External growth |
| Balanced | Diversified approach |

## Analysis Tips

1. **Compare OCF to earnings**: Divergence signals quality issues.

2. **Track FCF trends**: More important than net income.

3. **Analyze working capital drivers**: Understand component changes.

4. **Consider seasonality**: Quarterly patterns affect cash flow.

5. **Read footnotes**: Capital commitments disclosed there.

6. **Check management discussion**: Cash flow commentary in MD&A.

## Use Cases

- **Investment analysis**: Assess cash generation quality
- **Credit analysis**: Evaluate debt service capability
- **Valuation**: FCF-based models
- **Liquidity monitoring**: Track cash position
- **Working capital efficiency**: Operational assessment
