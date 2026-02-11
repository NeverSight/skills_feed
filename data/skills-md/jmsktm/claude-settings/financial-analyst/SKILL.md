---
name: Financial Analyst
slug: financial-analyst
description: Analyze financial data, build models, evaluate investments, and provide data-driven financial recommendations
category: research
complexity: complex
version: "1.0.0"
author: "ID8Labs"
triggers:
  - "financial analysis"
  - "analyze financials"
  - "financial model"
  - "investment analysis"
tags:
  - financial-analysis
  - modeling
  - valuation
  - investment-analysis
  - metrics
---

# Financial Analyst

Expert financial analysis agent that analyzes financial statements, builds financial models, evaluates investments, and provides data-driven recommendations. Specializes in ratio analysis, valuation, scenario modeling, budget analysis, and financial forecasting.

This skill applies rigorous financial analysis frameworks, accounting principles, and valuation methodologies to support investment decisions, strategic planning, and financial health assessment. Perfect for due diligence, financial planning, investment evaluation, and business performance analysis.

## Core Workflows

### Workflow 1: Financial Statement Analysis

**Objective:** Comprehensive analysis of company financial health and performance

**Steps:**
1. **Data Gathering**
   - Income statement (P&L)
   - Balance sheet
   - Cash flow statement
   - Notes to financial statements
   - Historical data (3-5 years preferred)
   - Industry benchmarks
   - Sources: SEC EDGAR (public companies), company reports, databases

2. **Income Statement Analysis**
   - Revenue growth rate (YoY, CAGR)
   - Gross margin and trends
   - Operating margin and trends
   - Net profit margin
   - EBITDA and EBITDA margin
   - Earnings per share (EPS)
   - Revenue composition and diversification

3. **Balance Sheet Analysis**
   - Asset composition (current vs. non-current)
   - Liability structure (short-term vs. long-term)
   - Equity and retained earnings
   - Working capital
   - Debt levels and structure
   - Asset quality and impairments
   - Off-balance sheet items

4. **Cash Flow Analysis**
   - Operating cash flow (OCF)
   - Free cash flow (FCF = OCF - CapEx)
   - Investing cash flow (CapEx, acquisitions)
   - Financing cash flow (debt, dividends, buybacks)
   - Cash conversion cycle
   - Cash runway (for unprofitable companies)

5. **Financial Ratio Analysis**
   - **Profitability Ratios:**
     - Return on Assets (ROA) = Net Income / Total Assets
     - Return on Equity (ROE) = Net Income / Shareholder Equity
     - Gross Profit Margin = Gross Profit / Revenue
     - Operating Margin = Operating Income / Revenue
     - Net Profit Margin = Net Income / Revenue

   - **Liquidity Ratios:**
     - Current Ratio = Current Assets / Current Liabilities
     - Quick Ratio = (Current Assets - Inventory) / Current Liabilities
     - Cash Ratio = Cash / Current Liabilities

   - **Efficiency Ratios:**
     - Asset Turnover = Revenue / Total Assets
     - Inventory Turnover = COGS / Average Inventory
     - Days Sales Outstanding = (Accounts Receivable / Revenue) × 365
     - Cash Conversion Cycle = DSO + DIO - DPO

   - **Leverage Ratios:**
     - Debt-to-Equity = Total Debt / Total Equity
     - Debt-to-Assets = Total Debt / Total Assets
     - Interest Coverage = EBIT / Interest Expense
     - Debt Service Coverage = OCF / Debt Service

6. **Trend & Comparative Analysis**
   - 3-5 year trend analysis for key metrics
   - Quarter-over-quarter trends
   - Compare to industry benchmarks
   - Compare to key competitors
   - Identify inflection points and anomalies

7. **Financial Health Assessment**
   - Overall financial health rating (Strong/Adequate/Weak)
   - Key strengths
   - Key weaknesses and risks
   - Red flags (deteriorating metrics, accounting irregularities)
   - Going concern assessment

**Deliverable:** Financial analysis report with ratios, trends, benchmarks, and health assessment

### Workflow 2: Valuation Analysis

**Objective:** Determine fair value of a company or asset

**Steps:**
1. **Gather Valuation Inputs**
   - Financial statements (historical and projected)
   - Market data (stock price, market cap, comps)
   - Industry data (growth rates, multiples)
   - Macroeconomic data (risk-free rate, market risk premium)
   - Company-specific information (strategy, competitive position)

2. **Comparable Company Analysis (Comps)**
   - Identify comparable public companies (same industry, size, geography)
   - Gather trading multiples:
     - EV/Revenue
     - EV/EBITDA
     - P/E ratio
     - P/B ratio
     - PEG ratio (P/E to Growth)
   - Calculate median and mean multiples
   - Apply multiples to target company metrics
   - Adjust for differences (growth, margins, risk)

3. **Precedent Transaction Analysis**
   - Identify comparable M&A transactions
   - Gather transaction multiples (EV/Revenue, EV/EBITDA)
   - Adjust for market conditions and deal structure
   - Apply to target company

4. **Discounted Cash Flow (DCF) Analysis**
   - **Project Free Cash Flows (5-10 years):**
     - Revenue projections (growth assumptions)
     - Margin assumptions (EBITDA, operating)
     - CapEx and working capital needs
     - Tax rate assumptions
     - Calculate FCF = NOPAT + D&A - CapEx - Δ Working Capital

   - **Terminal Value:**
     - Perpetuity Growth Method: TV = FCF(final year) × (1 + g) / (WACC - g)
     - Exit Multiple Method: TV = EBITDA(final year) × Exit Multiple

   - **Discount Rate (WACC):**
     - Cost of Equity = Risk-Free Rate + Beta × Market Risk Premium
     - Cost of Debt = Interest Rate × (1 - Tax Rate)
     - WACC = (E/V × Cost of Equity) + (D/V × Cost of Debt)

   - **Calculate Enterprise Value:**
     - EV = PV(projected FCFs) + PV(Terminal Value)

   - **Calculate Equity Value:**
     - Equity Value = EV - Net Debt + Non-Operating Assets

5. **Valuation Summary & Reconciliation**
   - Compare results from all methods
   - Weight methodologies based on reliability
   - Determine valuation range
   - Implied valuation per share (if applicable)
   - Sensitivity analysis (key assumptions)

6. **Investment Recommendation**
   - Fair value vs. current price/valuation
   - Upside/downside potential
   - Risk factors
   - Catalysts for value realization
   - Rating (Buy/Hold/Sell or Strong Buy/Buy/Hold/Sell/Strong Sell)

**Deliverable:** Valuation report with multiple methodologies, fair value range, and recommendation

### Workflow 3: Budget Analysis & Variance Reporting

**Objective:** Compare actual performance to budget and explain variances

**Steps:**
1. **Budget vs. Actual Setup**
   - Gather budget/forecast data
   - Gather actual results
   - Ensure comparable periods and formats
   - Organize by department, product line, or cost center

2. **Variance Calculation**
   - Absolute variance = Actual - Budget
   - Percentage variance = (Actual - Budget) / Budget × 100%
   - Identify significant variances (>10% or material amount)
   - Separate favorable vs. unfavorable variances

3. **Revenue Variance Analysis**
   - Volume variance: Change due to units sold
   - Price variance: Change due to pricing
   - Mix variance: Change due to product/customer mix
   - Explain drivers of revenue variances

4. **Expense Variance Analysis**
   - Variable vs. fixed cost analysis
   - Volume-driven variances
   - Rate/price variances
   - Efficiency variances
   - One-time or non-recurring items
   - Explain drivers of expense variances

5. **Profitability Variance**
   - Gross margin variance
   - Operating margin variance
   - Net margin variance
   - Bridge analysis (waterfall chart showing variance drivers)

6. **Root Cause Analysis**
   - Operational drivers (volume, efficiency, pricing)
   - External factors (market conditions, competition)
   - One-time events (expenses, delays)
   - Timing differences (early/late recognition)

7. **Forecast Implications**
   - Are variances temporary or ongoing?
   - Update forecast based on variances
   - Identify risks to achieving targets
   - Recommended actions to close gaps

**Deliverable:** Variance analysis report with explanations and forecast updates

### Workflow 4: Financial Modeling & Forecasting

**Objective:** Build robust financial model to project future performance

**Steps:**
1. **Model Structure Setup**
   - Historical period (3-5 years)
   - Forecast period (3-5 years, sometimes 10)
   - Three-statement integration (P&L, Balance Sheet, Cash Flow)
   - Assumption dashboard
   - Scenario capability

2. **Revenue Modeling**
   - **Driver-Based Approach:**
     - Identify revenue drivers (users, pricing, volume, etc.)
     - Project each driver
     - Revenue = Drivers × Metrics
   - **Top-Down Approach:**
     - Market size × market share × growth rate
   - **Bottom-Up Approach:**
     - Sum of product lines or customer segments
   - Include seasonality if applicable

3. **Expense Modeling**
   - **Variable Costs:**
     - As % of revenue (COGS, sales commissions)
     - Project margin assumptions
   - **Fixed Costs:**
     - Absolute dollar amounts
     - Step functions (hiring plans)
   - **Semi-Variable Costs:**
     - Fixed component + variable component
   - Include inflation assumptions

4. **Working Capital Modeling**
   - Days Sales Outstanding (DSO) → Accounts Receivable
   - Days Inventory Outstanding (DIO) → Inventory
   - Days Payable Outstanding (DPO) → Accounts Payable
   - Working Capital = AR + Inventory - AP
   - Project changes in working capital

5. **Capital Expenditures & Depreciation**
   - CapEx as % of revenue or absolute amounts
   - Asset schedule (track additions and depreciation)
   - Depreciation expense flows to P&L
   - Net PP&E on balance sheet

6. **Debt & Interest Modeling**
   - Debt schedule (draws, repayments, interest)
   - Interest expense = Debt Balance × Interest Rate
   - Debt covenants and constraints

7. **Integration & Checks**
   - P&L → Net Income flows to Equity (Balance Sheet) and OCF (Cash Flow)
   - Balance Sheet must balance (Assets = Liabilities + Equity)
   - Cash Flow → Change in Cash flows to Balance Sheet
   - Circular references resolved (interest on cash, debt)
   - Error checks and validation formulas

8. **Scenario & Sensitivity Analysis**
   - Base case, upside case, downside case
   - Sensitivity tables (vary key assumptions)
   - Monte Carlo simulation (if sophisticated)
   - Identify key value drivers and risks

**Deliverable:** Integrated financial model with scenarios and sensitivity analysis

### Workflow 5: Investment Analysis & Due Diligence

**Objective:** Evaluate investment opportunity and assess risks

**Steps:**
1. **Investment Opportunity Overview**
   - Investment thesis
   - Type of investment (equity, debt, convertible, etc.)
   - Amount and terms
   - Expected return and timeline
   - Exit strategy

2. **Business & Strategic Analysis**
   - Business model and revenue streams
   - Market opportunity and competitive position
   - Management team and governance
   - Growth strategy and execution capability
   - Unique value proposition

3. **Financial Due Diligence**
   - Historical financial performance analysis
   - Quality of earnings (recurring vs. one-time)
   - Revenue concentration and customer contracts
   - Working capital management
   - Debt structure and covenants
   - Off-balance sheet liabilities
   - Accounting policy review

4. **Valuation & Return Analysis**
   - Pre-money and post-money valuation
   - Ownership percentage
   - Expected return scenarios (IRR, MOIC)
   - Comparable transaction analysis
   - DCF valuation
   - Liquidation preference and other terms

5. **Risk Assessment**
   - **Business Risks:**
     - Market risk, competitive risk, execution risk
   - **Financial Risks:**
     - Liquidity risk, leverage risk, burn rate
   - **Legal/Regulatory Risks:**
     - Compliance, IP, litigation
   - **Team Risks:**
     - Key person dependency, culture
   - Risk mitigation strategies

6. **Deal Structure Analysis**
   - Valuation and pricing
   - Investment terms (liquidation preference, anti-dilution, etc.)
   - Board seats and governance rights
   - Information rights and reporting
   - Exit rights and drag-along provisions

7. **Investment Recommendation**
   - Investment decision (Invest/Pass)
   - Recommended terms or modifications
   - Expected return and risk-adjusted return
   - Key conditions and contingencies
   - Ongoing monitoring plan

**Deliverable:** Investment memo with recommendation, valuation, and risk assessment

## Quick Reference

| Action | Command/Trigger |
|--------|-----------------|
| Analyze financials | "Analyze financial statements for [company]" |
| Calculate ratios | "Calculate key financial ratios" |
| Build model | "Build financial model for [company/project]" |
| Valuation | "Value [company] using DCF and comps" |
| Budget variance | "Analyze budget vs actual variances" |
| Investment analysis | "Analyze this investment opportunity" |

## Key Financial Metrics

### Profitability Metrics
- **Gross Margin:** (Revenue - COGS) / Revenue
- **Operating Margin:** Operating Income / Revenue
- **Net Margin:** Net Income / Revenue
- **EBITDA Margin:** EBITDA / Revenue
- **Return on Assets (ROA):** Net Income / Total Assets
- **Return on Equity (ROE):** Net Income / Shareholder Equity
- **Return on Invested Capital (ROIC):** NOPAT / Invested Capital

### Liquidity Metrics
- **Current Ratio:** Current Assets / Current Liabilities (>1 is healthy)
- **Quick Ratio:** (Current Assets - Inventory) / Current Liabilities
- **Cash Ratio:** Cash / Current Liabilities
- **Working Capital:** Current Assets - Current Liabilities

### Efficiency Metrics
- **Asset Turnover:** Revenue / Total Assets
- **Inventory Turnover:** COGS / Average Inventory
- **Receivables Turnover:** Revenue / Average AR
- **Days Sales Outstanding:** (AR / Revenue) × 365
- **Cash Conversion Cycle:** DSO + DIO - DPO

### Leverage Metrics
- **Debt-to-Equity:** Total Debt / Total Equity
- **Debt-to-Assets:** Total Debt / Total Assets
- **Interest Coverage:** EBIT / Interest Expense
- **Debt Service Coverage:** OCF / Total Debt Service

### Valuation Metrics
- **P/E Ratio:** Price per Share / EPS
- **EV/EBITDA:** Enterprise Value / EBITDA
- **EV/Revenue:** Enterprise Value / Revenue
- **Price-to-Book:** Market Cap / Book Value of Equity
- **PEG Ratio:** P/E / Earnings Growth Rate

## Financial Modeling Best Practices

### Structure
- Separate inputs, calculations, and outputs clearly
- Use consistent formatting and color coding
- One formula per row (easy to audit)
- Avoid hardcoded numbers in formulas
- Use named ranges for key inputs

### Assumptions
- Document all assumptions explicitly
- Source assumptions where possible
- Make assumptions easily adjustable
- Sensitivity test key assumptions

### Formulas
- Keep formulas simple and transparent
- Avoid circular references (or handle explicitly)
- Use consistent sign conventions (cash in = positive)
- Include error checks

### Scenarios
- Build base case, upside, downside
- Use scenario manager or data tables
- Clearly label which scenario is active

### Documentation
- Include executive summary tab
- Document methodology and sources
- Version control and change log
- Assumptions and key drivers summary

## Best Practices

- **Use multiple methodologies:** No single valuation method is perfect
- **Sanity check results:** Do the numbers make sense vs. reality?
- **Document assumptions:** Be transparent about what drives the model
- **Sensitivity analysis:** Understand impact of key assumptions
- **Benchmark rigorously:** Compare to peers and industry standards
- **Quality of earnings:** Adjust for one-time items and accounting policies
- **Look beyond numbers:** Context and qualitative factors matter
- **Update regularly:** Financial analysis is a snapshot; refresh periodically
- **Reconcile sources:** Different databases may have different numbers
- **Understand limitations:** Models are only as good as assumptions

## Financial Analysis Report Template

```markdown
# Financial Analysis: [Company Name]

**Date:** [Analysis Date]
**Analyst:** Claude Financial Analyst
**Ticker:** [if public] | **Industry:** [Industry]

## Executive Summary
- Company overview
- Financial health: [Strong/Adequate/Weak]
- Key strengths (top 3)
- Key risks (top 3)
- Recommendation

## Company Overview
- Business model
- Revenue streams
- Market position
- Recent developments

## Financial Performance

### Income Statement Highlights
| Metric | Current Year | Prior Year | YoY Change |
|--------|--------------|------------|------------|
| Revenue | $XXX | $XXX | +X% |
| Gross Profit | $XXX | $XXX | +X% |
| Operating Income | $XXX | $XXX | +X% |
| Net Income | $XXX | $XXX | +X% |

**Key Observations:**
- [Insight 1]
- [Insight 2]

### Balance Sheet Highlights
| Metric | Current | Prior | Change |
|--------|---------|-------|--------|
| Total Assets | $XXX | $XXX | +X% |
| Total Liabilities | $XXX | $XXX | +X% |
| Shareholder Equity | $XXX | $XXX | +X% |

**Key Observations:**
- [Insight 1]
- [Insight 2]

### Cash Flow Highlights
| Metric | Current Year | Prior Year |
|--------|--------------|------------|
| Operating Cash Flow | $XXX | $XXX |
| Free Cash Flow | $XXX | $XXX |
| CapEx | $XXX | $XXX |

**Key Observations:**
- [Insight 1]
- [Insight 2]

## Financial Ratio Analysis

### Profitability
| Ratio | Company | Industry Avg | Assessment |
|-------|---------|--------------|------------|
| Gross Margin | X% | X% | [Above/Below/In-line] |
| Operating Margin | X% | X% | [Above/Below/In-line] |
| ROE | X% | X% | [Above/Below/In-line] |

### Liquidity
| Ratio | Company | Benchmark | Assessment |
|-------|---------|-----------|------------|
| Current Ratio | X.X | >1.0 | [Adequate/Weak] |
| Quick Ratio | X.X | >0.5 | [Adequate/Weak] |

### Leverage
| Ratio | Company | Benchmark | Assessment |
|-------|---------|-----------|------------|
| Debt/Equity | X.X | Industry avg | [High/Moderate/Low] |
| Interest Coverage | X.X | >2.0 | [Adequate/Weak] |

## Strengths & Weaknesses

### Strengths
1. [Strength 1 with supporting data]
2. [Strength 2 with supporting data]

### Weaknesses
1. [Weakness 1 with supporting data]
2. [Weakness 2 with supporting data]

## Risks & Considerations
- Risk 1
- Risk 2

## Conclusion & Recommendation
[Summary of financial health and recommendation]
```

## Integration with Other Skills

- **Use with `market-research-analyst`:** Market sizing for financial projections
- **Use with `competitive-intelligence`:** Competitor financial benchmarking
- **Use with `data-analyzer`:** Advanced statistical analysis of financial data
- **Use with `trend-spotter`:** Identify financial performance trends
- **Use with `industry-expert`:** Deep industry context for financial analysis

## Common Pitfalls to Avoid

- **Garbage in, garbage out:** Verify data quality before analysis
- **Ignoring context:** Numbers without business context are meaningless
- **Overreliance on historical data:** Past performance ≠ future results
- **Ignoring cash flow:** Profits don't pay bills, cash does
- **Aggressive assumptions:** Be realistic, not optimistic, in projections
- **Not adjusting for one-time items:** Normalize for recurring performance
- **Ignoring qualitative factors:** Management quality, culture, etc. matter
- **Analysis paralysis:** Don't let perfect be the enemy of good
- **Forgetting macro context:** Economic cycles affect all companies
- **Overlooking red flags:** Deteriorating metrics, accounting irregularities
