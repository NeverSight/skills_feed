---
name: Financial Analysis
description: This skill should be used when the user asks to "analyze financials", "revenue model", "unit economics", "pricing analysis", "cost structure", "profitability analysis", "financial projections", "business model economics", or needs guidance on financial metrics, revenue analysis, or economic viability assessment.
version: 0.1.0
---

# Financial Analysis

## Overview

Financial analysis evaluates economic viability and business model health through metrics, projections, and benchmarking. This skill covers key financial frameworks for market and business analysis.

## Core Metrics

### Unit Economics

**Customer Acquisition Cost (CAC)**
- Total sales & marketing spend ÷ new customers acquired
- Benchmark: Varies by industry ($50-$500+ for SaaS)

**Lifetime Value (LTV)**
- Average revenue per customer × gross margin × customer lifetime
- Simplified: ARPU ÷ churn rate × gross margin

**LTV:CAC Ratio**
- Target: 3:1 or higher
- <1:1 = unsustainable
- >5:1 = may be under-investing

**Payback Period**
- CAC ÷ (ARPU × gross margin)
- Target: <12 months for SaaS

### Revenue Metrics

**Monthly Recurring Revenue (MRR)**
- Sum of all recurring subscription revenue

**Annual Recurring Revenue (ARR)**
- MRR × 12

**Average Revenue Per User (ARPU)**
- Total revenue ÷ number of customers

**Net Revenue Retention (NRR)**
- (Starting MRR + expansion - contraction - churn) ÷ Starting MRR
- Target: >100% (expansion exceeds churn)

### Growth Metrics

**Month-over-Month Growth**
- (Current MRR - Previous MRR) ÷ Previous MRR

**Year-over-Year Growth**
- (Current ARR - Previous Year ARR) ÷ Previous Year ARR

**Compound Annual Growth Rate (CAGR)**
- ((End Value ÷ Start Value)^(1/years)) - 1

## Revenue Models

### Subscription (SaaS)
- Recurring monthly/annual payments
- Metrics: MRR, ARR, churn, NRR
- Trend: INC (dominant model)

### Usage-Based
- Pay per consumption
- Metrics: Usage growth, ARPU, expansion rate
- Trend: INC (growing adoption)

### Transactional
- Per-transaction fees
- Metrics: Transaction volume, take rate, AOV
- Trend: CONST

### Marketplace
- Commission on GMV
- Metrics: GMV, take rate, liquidity
- Trend: CONST

### Enterprise Licensing
- Large upfront + maintenance
- Metrics: Deal size, renewal rate, services %
- Trend: DEC (shifting to SaaS)

## Pricing Analysis

### Pricing Strategies

| Strategy | Description | Best For |
|----------|-------------|----------|
| Cost-plus | Cost + margin | Commodities |
| Value-based | % of customer value | Differentiated products |
| Competitive | Relative to alternatives | Crowded markets |
| Penetration | Low to gain share | New entrants |
| Premium | High for positioning | Luxury/enterprise |

### Pricing Power Indicators

- **Strong**: Price increases stick, low churn
- **Moderate**: Some price sensitivity, competitive pressure
- **Weak**: Commodity, price-driven decisions

## Cost Structure Analysis

### Fixed vs. Variable Costs

| Cost Type | Examples | Trend Implication |
|-----------|----------|-------------------|
| Fixed | Rent, salaries, infrastructure | High fixed = operating leverage |
| Variable | COGS, commissions, hosting | Scales with revenue |
| Semi-variable | Support staff, marketing | Partially scales |

### Gross Margin Analysis

**Software/SaaS**: 70-85% typical
**Services**: 30-50% typical
**Marketplace**: Depends on take rate

### Operating Leverage

High fixed costs + low variable = High operating leverage
- Good when growing (profits scale faster)
- Risky when declining (losses amplify)

## Profitability Analysis

### Income Statement Ratios

| Metric | Formula | Benchmark |
|--------|---------|-----------|
| Gross Margin | (Rev - COGS) / Rev | 70%+ for SaaS |
| Operating Margin | Operating Income / Rev | 20%+ mature |
| Net Margin | Net Income / Rev | 10%+ profitable |

### Rule of 40 (SaaS)

Growth Rate % + Profit Margin % ≥ 40%

- Growing 50%? Can be -10% margin
- Growing 20%? Need 20% margin
- Below 40 = concern for investors

## Financial Projections

### Projection Components

1. **Revenue Forecast**
   - Customer growth × ARPU
   - Include expansion/contraction
   - Apply trend indicators (INC/DEC/CONST)

2. **Cost Forecast**
   - Fixed costs + (variable rate × revenue)
   - Step functions for scaling costs

3. **Cash Flow**
   - Operating cash generation
   - Capital requirements
   - Runway calculation

### Scenario Modeling

| Scenario | Revenue Growth | Margin | Cash Position |
|----------|----------------|--------|---------------|
| Bear | X% | Y% | $Z |
| Base | X% | Y% | $Z |
| Bull | X% | Y% | $Z |

## Benchmarking

### SaaS Benchmarks by Stage

| Metric | Early | Growth | Scale |
|--------|-------|--------|-------|
| Growth Rate | >100% | 50-100% | 20-50% |
| Gross Margin | 60%+ | 70%+ | 75%+ |
| NRR | >100% | >110% | >120% |
| LTV:CAC | >3:1 | >3:1 | >4:1 |
| Payback | <18mo | <12mo | <12mo |

## Output Structure

```markdown
## Financial Analysis Summary

### Business Model
- **Type**: [Subscription/Usage/etc.]
- **Revenue Streams**: [List]
- **Pricing Strategy**: [Type]

### Key Metrics
| Metric | Value | Benchmark | Assessment |
|--------|-------|-----------|------------|
| Gross Margin | X% | Y% | Above/Below |
| LTV:CAC | X:1 | 3:1 | Healthy/Concerning |
| NRR | X% | 100% | Strong/Weak |

### Unit Economics
- CAC: $X
- LTV: $X
- Payback: X months
- LTV:CAC: X:1

### Trend Indicators
- Revenue Growth: INC/DEC/CONST
- Margin Trajectory: INC/DEC/CONST
- Unit Economics: INC/DEC/CONST

### Financial Health Assessment
[Overall assessment with key findings]

### Projections
[3-year scenario projections]

### Recommendations
1. [Financial recommendation]
2. [Financial recommendation]
```

## Best Practices

- Use multiple data sources for validation
- Note data recency and reliability
- Distinguish reported vs. estimated figures
- Consider industry-specific benchmarks
- Apply appropriate trend indicators

## Additional Resources

For detailed templates, see:
- `references/unit-economics.md` - Deep dive on LTV/CAC
- `references/saas-metrics.md` - SaaS-specific metrics
- `examples/financial-analysis.md` - Sample analysis
