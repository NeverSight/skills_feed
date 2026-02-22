---
name: sec-debt-covenant
description: Analyze debt covenants and credit agreement terms from SEC filings using Octagon MCP. Use when researching financial covenants, leverage ratios, interest coverage requirements, credit facilities, debt maturity schedules, and covenant compliance from 10-K, 10-Q, and 8-K filings.
---

# SEC Debt Covenant Analysis

Analyze debt covenants and credit agreement terms disclosed in SEC filings for public companies using the Octagon MCP server.

## Prerequisites

Ensure Octagon MCP is configured in your AI agent (Cursor, Claude Desktop, Windsurf, etc.). See [references/mcp-setup.md](references/mcp-setup.md) for installation instructions.

## Workflow

### 1. Identify Analysis Parameters

Determine the following before querying:
- **Ticker**: Stock symbol (e.g., AAPL, MSFT, GOOGL)
- **Filing Type** (optional): 10-K, 10-Q, 8-K
- **Focus Area** (optional): Covenants, facilities, maturities

### 2. Execute Query via Octagon MCP

Use the `octagon-agent` tool with a natural language prompt:

```
Analyze debt covenants and credit agreement terms disclosed in <TICKER>'s latest SEC filings.
```

**MCP Call Format:**

```json
{
  "server": "octagon-mcp",
  "toolName": "octagon-agent",
  "arguments": {
    "prompt": "Analyze debt covenants and credit agreement terms disclosed in F's latest SEC filings."
  }
}
```

### 3. Expected Output

The agent returns structured debt analysis including:

**Debt Overview:**
- Total debt excluding subsidiaries: $20.9B
- Short-term debt: $0.8B

**Covenant Information:**
- FCE Credit Agreement covenants
- Financial metric maintenance requirements

**Data Sources**: octagon-financials-agent, octagon-sec-agent, octagon-web-search-agent

### 4. Interpret Results

See [references/interpreting-results.md](references/interpreting-results.md) for guidance on:
- Understanding covenant types
- Assessing covenant cushion
- Evaluating credit facility terms
- Monitoring compliance risk

## Example Queries

**Full Debt Covenant Analysis:**
```
Analyze debt covenants and credit agreement terms disclosed in F's latest SEC filings.
```

**Covenant Compliance:**
```
Is T in compliance with all debt covenants based on latest 10-Q disclosures?
```

**Credit Facility Terms:**
```
Extract revolving credit facility terms and availability from BA's latest 10-K.
```

**Debt Maturity Schedule:**
```
Analyze the debt maturity schedule and near-term obligations for GE.
```

**Leverage Ratios:**
```
What are the maximum leverage ratio covenants in CCL's credit agreements?
```

**Interest Coverage:**
```
Extract interest coverage ratio requirements from NCLH's debt covenants.
```

## Debt Structure Overview

### Types of Debt

| Type | Characteristics |
|------|-----------------|
| Senior Secured | First lien, asset-backed |
| Senior Unsecured | No collateral, higher rate |
| Subordinated | Junior to senior debt |
| Convertible | Can convert to equity |
| Term Loans | Fixed maturity, amortizing |
| Revolving Credit | Drawable, flexible |

### Credit Facilities

| Facility | Purpose |
|----------|---------|
| Revolving Credit | Working capital, liquidity |
| Term Loan A | Bank loan, amortizing |
| Term Loan B | Institutional, bullet |
| Bridge Facility | Short-term, M&A |
| Letter of Credit | Guarantees, obligations |

## Covenant Types

### Financial Covenants

| Covenant | Typical Requirement |
|----------|---------------------|
| Leverage Ratio | Debt/EBITDA ≤ X.Xx |
| Interest Coverage | EBITDA/Interest ≥ X.Xx |
| Fixed Charge | (EBITDA-CapEx)/Fixed Charges ≥ X.Xx |
| Minimum EBITDA | EBITDA ≥ $X million |
| Maximum CapEx | CapEx ≤ $X million |
| Minimum Liquidity | Cash + Availability ≥ $X |

### Incurrence Covenants

| Covenant | Restriction |
|----------|-------------|
| Debt Incurrence | Limits new borrowing |
| Lien Incurrence | Limits secured debt |
| Restricted Payments | Limits dividends, buybacks |
| Asset Sales | Requires reinvestment |
| Affiliate Transactions | Arms-length requirement |

### Maintenance Covenants

| Covenant | Requirement |
|----------|-------------|
| Tested Periodically | Quarterly or annually |
| Must Maintain | Ongoing compliance |
| Cure Rights | Ability to remedy |
| Spring | Only tested when drawn |

## Key Covenant Metrics

### Leverage Metrics

| Metric | Calculation |
|--------|-------------|
| Total Leverage | Total Debt / EBITDA |
| Net Leverage | (Total Debt - Cash) / EBITDA |
| Senior Leverage | Senior Debt / EBITDA |
| Secured Leverage | Secured Debt / EBITDA |

### Coverage Metrics

| Metric | Calculation |
|--------|-------------|
| Interest Coverage | EBITDA / Interest Expense |
| Fixed Charge | (EBITDA - CapEx) / (Interest + Principal) |
| Debt Service | EBITDA / (Interest + Principal) |
| Cash Interest | EBITDA / Cash Interest |

### Liquidity Metrics

| Metric | Calculation |
|--------|-------------|
| Minimum Cash | Cash and equivalents |
| Minimum Liquidity | Cash + Revolver Availability |
| Current Ratio | Current Assets / Current Liabilities |

## Covenant Cushion Analysis

### Cushion Calculation

| Metric | Current | Covenant | Cushion |
|--------|---------|----------|---------|
| Leverage | X.Xx | ≤Y.Yx | Z.Zx |
| Coverage | X.Xx | ≥Y.Yx | Z.Zx |
| Liquidity | $XM | ≥$YM | $ZM |

### Cushion Assessment

| Cushion Level | Assessment |
|---------------|------------|
| >30% | Comfortable |
| 15-30% | Adequate |
| 5-15% | Tight |
| <5% | At risk |

## Credit Agreement Terms

### Key Terms to Extract

| Term | What It Specifies |
|------|-------------------|
| Facility Size | Total commitment |
| Maturity Date | When it expires |
| Interest Rate | Pricing terms |
| Commitment Fee | Unused fee |
| Amortization | Repayment schedule |
| Prepayment | Early repayment terms |

### Pricing Terms

| Component | Description |
|-----------|-------------|
| Base Rate | SOFR, Prime, LIBOR |
| Spread | Margin over base |
| Floor | Minimum rate |
| Grid Pricing | Spread varies with metrics |

## Maturity Schedule Analysis

### Debt Maturity Profile

| Year | Amount | % of Total |
|------|--------|------------|
| 2025 | $XM | Y% |
| 2026 | $XM | Y% |
| 2027 | $XM | Y% |
| 2028+ | $XM | Y% |

### Refinancing Risk

| Factor | High Risk | Low Risk |
|--------|-----------|----------|
| Near-Term Maturities | >25% in 1 year | <10% in 2 years |
| Market Access | Limited | Strong |
| Credit Rating | Downgrade risk | Stable/upgrading |
| Covenant Headroom | Tight | Comfortable |

## Covenant Violation Analysis

### Consequences of Violation

| Consequence | Description |
|-------------|-------------|
| Default | Triggers acceleration |
| Cross-Default | Affects other debt |
| Waiver Required | Lender approval needed |
| Amendment | Terms modification |
| Cure Period | Time to remedy |

### Cure Mechanisms

| Mechanism | How It Works |
|-----------|--------------|
| Equity Cure | Inject equity to improve ratios |
| Asset Sale | Reduce debt |
| Amendment | Modify covenant level |
| Waiver | Temporary relief |

## Red Flags

### Covenant Red Flags

1. **Tight cushion** - <10% headroom
2. **Covenant holiday** - Temporarily suspended
3. **Repeated amendments** - Ongoing issues
4. **Pro forma adjustments** - Aggressive EBITDA add-backs
5. **Springing covenants** - May become tested

### Liquidity Red Flags

1. **High revolver utilization** - >80% drawn
2. **Near-term maturities** - Large amounts due
3. **Limited refinancing options** - Market access concerns
4. **Declining EBITDA** - Coverage deterioration
5. **Downgrade risk** - Rating agency warnings

## Disclosure Locations

### Where to Find Covenants

| Filing | Location |
|--------|----------|
| 10-K/10-Q | Debt footnote |
| 10-K/10-Q | Liquidity discussion in MD&A |
| 8-K | Credit agreement announcement |
| Exhibits | Full credit agreement |
| S-1/424B | Debt description |

### Key Exhibits

| Exhibit | Content |
|---------|---------|
| Credit Agreement | Full terms |
| Indenture | Bond terms |
| Amendment | Modified terms |
| Compliance Certificate | Covenant calculations |

## Analysis Tips

1. **Read the footnotes**: Detailed covenant terms disclosed there.

2. **Check MD&A liquidity**: Management discusses compliance.

3. **Review exhibits**: Full credit agreements filed.

4. **Track amendments**: Changes signal issues or refinancing.

5. **Calculate cushion**: Don't rely solely on management claims.

6. **Monitor ratings**: Agency reports discuss covenants.

## Use Cases

- **Credit analysis**: Evaluate debt risk
- **Distressed investing**: Identify covenant stress
- **Equity research**: Assess financial flexibility
- **Due diligence**: Understand debt structure
- **Refinancing analysis**: Maturity and terms review
