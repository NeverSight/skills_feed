---
name: Market Sizing
description: This skill should be used when the user asks to "calculate market size", "TAM SAM SOM analysis", "estimate market opportunity", "market sizing", "total addressable market", "serviceable market", "market potential", or needs guidance on market size estimation methodologies, market opportunity calculations, or growth projections.
version: 0.1.0
---

# Market Sizing (TAM/SAM/SOM)

## Overview

Market sizing quantifies the revenue opportunity in a market. The TAM/SAM/SOM framework provides progressively refined estimates from total market to realistically achievable share.

## Key Definitions

**TAM (Total Addressable Market)**
- Total global market demand for a product/service
- Assumes 100% market share (theoretical maximum)
- Useful for understanding ceiling and investor conversations

**SAM (Serviceable Addressable Market)**
- Portion of TAM targetable with current business model
- Considers geographic, demographic, or segment constraints
- More realistic than TAM

**SOM (Serviceable Obtainable Market)**
- Realistic market share achievable in near term (1-3 years)
- Considers competition, resources, and go-to-market capability
- Most relevant for planning

## Calculation Methodologies

### Top-Down Approach

Start with large market data, narrow down:

1. **Find industry market size** from analyst reports
2. **Apply relevant percentage** for target segment
3. **Adjust for geography** if not global
4. **Factor growth rates** for projections

**Example:**
- Global SaaS market: $200B (TAM)
- HR SaaS segment: 15% → $30B (TAM refined)
- North America: 40% → $12B (SAM)
- Achievable share 2%: $240M (SOM)

**Pros:** Fast, uses existing research
**Cons:** May miss nuances, depends on source quality

### Bottom-Up Approach

Build from unit economics upward:

1. **Identify target customer count**
2. **Estimate price per customer**
3. **Calculate total revenue potential**

**Example:**
- Target customers: 50,000 SMBs
- Average contract value: $5,000/year
- Total: $250M (SOM)
- Expand to all SMBs (500,000): $2.5B (SAM)
- Include enterprise: $10B (TAM)

**Pros:** More defensible, validates assumptions
**Cons:** Slower, requires customer data

### Value Theory Approach

Estimate based on value delivered:

1. **Calculate customer pain point cost**
2. **Estimate value of solution**
3. **Apply capture rate** (typically 10-30% of value)

**Example:**
- Customer loses $100K/year to problem
- Solution captures 20%: $20K willingness to pay
- 100,000 potential customers: $2B market

## Trend Indicators

Apply three-valued logic to growth projections:

- **INC (Increasing)**: Market growing >10% annually
- **CONST (Constant)**: Market growth 0-10% annually
- **DEC (Decreasing)**: Market contracting

Document evidence for each indicator:
- INC: "Analyst projects 25% CAGR through 2027"
- CONST: "Mature market with 3% annual growth"
- DEC: "Legacy technology being displaced"

## Data Sources

**Primary Sources (Most Reliable):**
- Industry analyst reports (Gartner, Forrester, IDC)
- Government statistics (Census, BLS)
- Trade association data
- Company financials (public companies)

**Secondary Sources:**
- Market research firms (Statista, IBISWorld)
- News articles citing research
- Industry publications
- Competitor disclosures

**Estimation Sources (Use Carefully):**
- LinkedIn job counts × average salary
- Google Trends relative volume
- App store downloads × price
- Website traffic estimates

## Output Structure

```markdown
## Market Sizing Summary

| Metric | Value | Growth | Trend |
|--------|-------|--------|-------|
| TAM | $X.XB | X% CAGR | INC/DEC/CONST |
| SAM | $X.XB | X% CAGR | INC/DEC/CONST |
| SOM | $XXM | - | - |

## Methodology
[Top-down / Bottom-up / Hybrid]

## TAM Calculation
[Step-by-step with sources]

## SAM Derivation
[How SAM was narrowed from TAM]

## SOM Justification
[Realistic share rationale]

## Key Assumptions
1. [Assumption and sensitivity]
2. [Assumption and sensitivity]

## Data Sources
- [Source 1]: [What it provided]
- [Source 2]: [What it provided]

## Confidence Level
[High/Medium/Low with explanation]
```

## Common Pitfalls

- **Double-counting**: Ensure segments don't overlap
- **Currency confusion**: Specify USD/EUR and year
- **Stale data**: Note data age, adjust for growth
- **Over-optimism**: SOM should be conservative
- **Missing context**: Include methodology for credibility

## Scenario Modeling

For uncertain markets, provide range:

| Scenario | TAM | SAM | SOM |
|----------|-----|-----|-----|
| Bear | $5B | $500M | $10M |
| Base | $8B | $800M | $25M |
| Bull | $12B | $1.2B | $50M |

Use transitional scenario graphs to show how market might evolve between scenarios.

## Additional Resources

For detailed templates and examples, see:
- `references/sizing-methodologies.md` - Complete methodology guide
- `references/data-sources.md` - Source reliability ratings
- `examples/market-sizing-report.md` - Sample sizing report
