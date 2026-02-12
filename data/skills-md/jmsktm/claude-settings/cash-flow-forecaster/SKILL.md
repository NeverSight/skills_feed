---
name: Cash Flow Forecaster
slug: cash-flow-forecaster
description: Forecast cash inflows, outflows, and liquidity needs with scenario modeling and working capital optimization
category: finance
complexity: complex
version: "1.0.0"
author: "ID8Labs"
triggers:
  - "cash flow forecast"
  - "cash projection"
  - "liquidity planning"
  - "working capital"
  - "cash runway"
  - "13-week cash flow"
tags:
  - cash-flow
  - liquidity
  - treasury
  - working-capital
  - forecasting
---

# Cash Flow Forecaster

Expert cash flow modeling agent that builds detailed cash projections, stress tests liquidity, optimizes working capital, and manages cash position. Specializes in 13-week forecasts, rolling liquidity models, and scenario-based cash planning.

This skill applies rigorous treasury management principles to predict cash needs, prevent shortfalls, and optimize cash utilization. Perfect for startup runway planning, treasury operations, working capital management, and financial crisis planning.

## Core Workflows

### Workflow 1: 13-Week Cash Flow Forecast

**Objective:** Create detailed weekly cash forecast for near-term liquidity management

**Steps:**
1. **Opening Cash Position**
   - Bank balances by account
   - Cash in transit
   - Restricted cash
   - Available credit lines
   - Total available liquidity

2. **Cash Inflows by Week**
   - **Accounts Receivable Collections:**
     - Aged AR schedule
     - Customer payment patterns (DSO)
     - Expected collections by week
     - Bad debt assumptions

   - **Other Inflows:**
     - Recurring revenue (subscriptions, contracts)
     - Expected new sales
     - Investment income
     - Asset sales
     - Other receipts

3. **Cash Outflows by Week**
   - **Payroll (typically bi-weekly):**
     - Gross wages
     - Payroll taxes (same day or next day)
     - Benefits withholdings
     - 401k contributions

   - **Accounts Payable:**
     - Vendor payment schedule
     - Rent and lease payments
     - Utility payments
     - Contract payments

   - **Operating Expenses:**
     - Software subscriptions (monthly)
     - Insurance premiums
     - Professional services
     - Marketing spend

   - **Debt Service:**
     - Loan principal payments
     - Interest payments
     - Line of credit draws/payments

   - **Capital Expenditures:**
     - Equipment purchases
     - Facility improvements

4. **Weekly Cash Flow Calculation**
   - Beginning cash + Inflows - Outflows = Ending cash
   - Calculate for each of 13 weeks
   - Identify weekly cash surplus/deficit
   - Flag weeks with potential shortfalls

5. **Minimum Cash Requirements**
   - Operating buffer (2-4 weeks of expenses)
   - Debt covenant requirements
   - Seasonal requirements
   - Strategic reserves

6. **Variance Analysis**
   - Compare to prior forecast
   - Actual vs forecast for completed weeks
   - Identify forecast accuracy issues
   - Refine collection/payment assumptions

**Deliverable:** 13-week rolling cash forecast with daily/weekly precision

### Workflow 2: Monthly/Annual Cash Flow Projection

**Objective:** Long-term cash flow modeling for planning purposes

**Steps:**
1. **P&L to Cash Flow Bridge**
   - Start with projected net income
   - Add back non-cash items:
     - Depreciation and amortization
     - Stock-based compensation
     - Deferred revenue changes
     - Bad debt expense

2. **Working Capital Changes**
   - **Accounts Receivable:**
     - DSO assumption (Days Sales Outstanding)
     - AR = (Revenue / 365) x DSO
     - Change in AR = Cash impact

   - **Inventory:**
     - DIO assumption (Days Inventory Outstanding)
     - Inventory = (COGS / 365) x DIO
     - Change in Inventory = Cash impact

   - **Accounts Payable:**
     - DPO assumption (Days Payable Outstanding)
     - AP = (Expenses / 365) x DPO
     - Change in AP = Cash impact

   - **Other Working Capital:**
     - Prepaid expenses
     - Accrued liabilities
     - Deferred revenue

3. **Cash from Operating Activities**
   - Net Income
   - + Non-cash adjustments
   - - Working capital changes
   - = Operating Cash Flow

4. **Cash from Investing Activities**
   - Capital expenditures (CapEx)
   - Acquisitions
   - Asset sales
   - Investment purchases/sales

5. **Cash from Financing Activities**
   - Debt proceeds/repayments
   - Equity raises
   - Dividend payments
   - Stock buybacks

6. **Monthly Cash Position**
   - Beginning cash
   - + Operating cash flow
   - + Investing cash flow
   - + Financing cash flow
   - = Ending cash

7. **Scenario Modeling**
   - Base case projection
   - Stress case (revenue -20%, slower collections)
   - Best case (accelerated collections, growth)

**Deliverable:** Monthly cash flow projection with scenarios

### Workflow 3: Working Capital Optimization

**Objective:** Improve cash flow by optimizing working capital components

**Steps:**
1. **Current State Analysis**
   - Calculate Cash Conversion Cycle:
     - CCC = DSO + DIO - DPO
     - Industry benchmarks
     - Historical trends

2. **Accounts Receivable Optimization**
   - **Current DSO Analysis:**
     - DSO by customer segment
     - Aging bucket analysis
     - Collection effectiveness

   - **Improvement Opportunities:**
     - Invoice timing (bill sooner)
     - Payment terms (shorten from Net 60 to Net 30)
     - Early payment discounts (2/10 Net 30)
     - Automated payment reminders
     - Credit policy tightening
     - Electronic payment options

   - **Target DSO and Cash Impact:**
     - Current DSO: X days
     - Target DSO: Y days
     - Cash freed = (Revenue / 365) x (X - Y)

3. **Accounts Payable Optimization**
   - **Current DPO Analysis:**
     - DPO by vendor category
     - Payment term utilization

   - **Optimization Opportunities:**
     - Negotiate extended terms
     - Optimize payment timing
     - Take early pay discounts when NPV positive
     - Centralize AP for better control

   - **Target DPO and Cash Impact:**
     - Current DPO: X days
     - Target DPO: Y days
     - Cash freed = (Expenses / 365) x (Y - X)

4. **Inventory Optimization** (if applicable)
   - Current DIO analysis
   - Excess and obsolete inventory
   - Safety stock optimization
   - Supplier lead time reduction
   - Cash impact of inventory reduction

5. **Working Capital Improvement Plan**
   - Prioritized initiatives
   - Expected cash impact
   - Implementation timeline
   - Responsible owners
   - Tracking metrics

**Deliverable:** Working capital improvement plan with cash flow impact

### Workflow 4: Liquidity Stress Testing

**Objective:** Model cash position under adverse scenarios

**Steps:**
1. **Define Stress Scenarios**
   - **Revenue Shock:**
     - Revenue decline 20%, 40%, 60%
     - Customer concentration loss
     - Market downturn

   - **Collection Stress:**
     - DSO increase 30-60 days
     - Customer bankruptcies
     - Increased bad debt

   - **Cost Increases:**
     - Key supplier price increases
     - Wage inflation
     - Unexpected expenses

   - **Credit Facility Loss:**
     - Line of credit revoked
     - Covenant violations
     - Credit downgrade

2. **Model Each Scenario**
   - Apply stress assumptions to base forecast
   - Calculate impact on cash flows
   - Determine time to cash exhaustion
   - Identify cash floor breaches

3. **Identify Trigger Points**
   - Weeks of cash remaining
   - Minimum cash threshold breaches
   - Covenant violation points
   - Point of no return

4. **Develop Contingency Plans**
   - **Tier 1 (Cash tight):**
     - Defer discretionary spending
     - Accelerate collections
     - Negotiate payment extensions

   - **Tier 2 (Cash crisis):**
     - Hiring freeze
     - Marketing cuts
     - Vendor renegotiations
     - Draw credit facilities

   - **Tier 3 (Survival mode):**
     - Layoffs
     - Asset sales
     - Emergency fundraising
     - Strategic alternatives

5. **Quantify Contingency Impact**
   - Cash preserved by each action
   - Implementation speed
   - Business impact
   - Recovery implications

**Deliverable:** Stress test results with contingency action plans

### Workflow 5: Startup Runway Modeling

**Objective:** Model cash runway and funding needs for startups

**Steps:**
1. **Current Burn Analysis**
   - Monthly gross burn (total expenses)
   - Monthly net burn (gross burn - revenue)
   - Burn trend (increasing/decreasing)
   - Cash on hand

2. **Runway Calculation**
   - Simple runway = Cash / Net Burn
   - Account for burn rate changes
   - Factor in revenue growth
   - Calculate zero-cash date

3. **Path to Profitability Analysis**
   - Monthly revenue required for breakeven
   - Unit economics at scale
   - Timeline to profitability
   - Cash required to reach profitability

4. **Funding Scenarios**
   - No additional funding (how long?)
   - Bridge round (12-18 months runway)
   - Full round (24+ months runway)
   - Strategic investment

5. **Milestone-Based Planning**
   - Key milestones for next round
   - Cost to achieve each milestone
   - Timeline requirements
   - Risk-adjusted funding needs

6. **Sensitivity Analysis**
   - Revenue growth scenarios
   - Burn rate scenarios
   - Combined scenarios
   - Probability-weighted runway

**Deliverable:** Runway model with funding recommendations

## Quick Reference

| Action | Command/Trigger |
|--------|-----------------|
| 13-week forecast | "Build 13-week cash flow forecast" |
| Monthly projection | "Project cash flow for next 12 months" |
| Working capital | "Analyze working capital optimization" |
| Stress test | "Stress test liquidity position" |
| Runway | "Calculate startup runway" |
| CCC analysis | "Analyze cash conversion cycle" |

## Cash Flow Formulas

### Key Metrics

| Metric | Formula | Healthy Range |
|--------|---------|---------------|
| Days Sales Outstanding (DSO) | (AR / Revenue) x 365 | 30-45 days |
| Days Inventory Outstanding (DIO) | (Inventory / COGS) x 365 | Industry varies |
| Days Payable Outstanding (DPO) | (AP / COGS) x 365 | 30-60 days |
| Cash Conversion Cycle (CCC) | DSO + DIO - DPO | Lower is better |
| Current Ratio | Current Assets / Current Liabilities | > 1.5 |
| Quick Ratio | (Current Assets - Inventory) / Current Liabilities | > 1.0 |
| Operating Cash Flow Ratio | OCF / Current Liabilities | > 1.0 |

### Cash Flow Calculations

```
Operating Cash Flow =
  Net Income
  + Depreciation & Amortization
  + Stock-Based Compensation
  - Increase in Accounts Receivable
  - Increase in Inventory
  + Increase in Accounts Payable
  + Other Non-Cash Adjustments

Free Cash Flow =
  Operating Cash Flow
  - Capital Expenditures

Net Burn Rate =
  Total Expenses - Total Revenue

Runway (months) =
  Cash on Hand / Net Burn Rate
```

## 13-Week Cash Flow Template

```markdown
| Week Ending | W1 | W2 | W3 | W4 | W5 | W6 | W7 | W8 | W9 | W10 | W11 | W12 | W13 |
|-------------|----|----|----|----|----|----|----|----|----|----|-----|-----|-----|
| **Beginning Cash** |
| |
| **Cash Inflows** |
| AR Collections | | | | | | | | | | | | | |
| New Sales | | | | | | | | | | | | | |
| Other Income | | | | | | | | | | | | | |
| **Total Inflows** | | | | | | | | | | | | | |
| |
| **Cash Outflows** |
| Payroll | | | | | | | | | | | | | |
| Vendor Payments | | | | | | | | | | | | | |
| Rent | | | | | | | | | | | | | |
| Utilities | | | | | | | | | | | | | |
| Debt Service | | | | | | | | | | | | | |
| Other | | | | | | | | | | | | | |
| **Total Outflows** | | | | | | | | | | | | | |
| |
| **Net Cash Flow** | | | | | | | | | | | | | |
| **Ending Cash** | | | | | | | | | | | | | |
| |
| **Minimum Required** |
| **Surplus/(Deficit)** |
```

## Best Practices

### Forecasting
- Update weekly (13-week) and monthly (annual)
- Track actual vs forecast to improve accuracy
- Bias toward conservative assumptions
- Document key assumptions
- Maintain version history

### Collections
- Age receivables weekly
- Follow up on overdue immediately
- Offer multiple payment methods
- Consider factoring for cash crunch

### Payments
- Maximize DPO within terms
- Take early pay discounts when > borrowing cost
- Centralize payment processing
- Negotiate extended terms with key vendors

### Monitoring
- Daily cash position tracking
- Weekly forecast updates
- Monthly variance analysis
- Quarterly stress testing

## Integration with Other Skills

- **Use with `budget-planner`:** Convert budget to cash flow
- **Use with `revenue-modeler`:** Model revenue collection timing
- **Use with `accounts-reconciler`:** Validate bank balances
- **Use with `billing-manager`:** Improve collection timing
- **Use with `financial-reporter`:** Create cash flow reports

## Common Pitfalls to Avoid

- **Confusing profit with cash:** Profitable companies can run out of cash
- **Ignoring timing:** When cash flows matters as much as amount
- **Optimistic collections:** Assume slower collections than promised
- **Forgetting lumpy payments:** Quarterly taxes, annual renewals
- **Static assumptions:** Update DSO/DPO based on actual performance
- **No buffer:** Always maintain operating cash cushion
- **Ignoring seasonality:** Model peak and trough periods
- **Incomplete coverage:** Capture all cash movements
