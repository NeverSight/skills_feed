---
name: sec-footnotes-analysis
description: Analyze footnotes and accounting policies from SEC filings using Octagon MCP. Use when researching revenue recognition policies, critical estimates, lease obligations, pension assumptions, stock compensation, contingencies, and new accounting pronouncements.
---

# SEC Footnotes Analysis

Analyze footnotes and accounting policies from SEC filings for public companies using the Octagon MCP server.

## Prerequisites

Ensure Octagon MCP is configured in your AI agent (Cursor, Claude Desktop, Windsurf, etc.). See [references/mcp-setup.md](references/mcp-setup.md) for installation instructions.

## Workflow

### 1. Identify Analysis Parameters

Determine the following before querying:
- **Ticker**: Stock symbol (e.g., AAPL, MSFT, GOOGL)
- **Filing Type** (optional): 10-K (annual) or 10-Q (quarterly)
- **Focus Area** (optional): Specific footnote topics of interest

### 2. Execute Query via Octagon MCP

Use the `octagon-agent` tool with a natural language prompt:

```
Analyze the footnotes and accounting policies from <TICKER>'s latest quarterly filing.
```

**MCP Call Format:**

```json
{
  "server": "octagon-mcp",
  "toolName": "octagon-agent",
  "arguments": {
    "prompt": "Analyze the footnotes and accounting policies from NVDA's latest quarterly filing."
  }
}
```

### 3. Expected Output

The agent returns structured footnote analysis including:

**Accounting Consistency:**
- No material changes to significant accounting policies since annual report

**Fiscal Year Structure:**
- 52-week fiscal year ending last Sunday in January
- Q3 is a 13-week quarter

**Consolidation Principles:**
- Includes wholly owned subsidiaries
- Intercompany balances eliminated

**Estimates and Assumptions:**
- Management estimates that could differ from actual results

**New Accounting Pronouncements:**
- No recent adoptions materially impacting statements

**Data Sources**: octagon-sec-agent

### 4. Interpret Results

See [references/interpreting-results.md](references/interpreting-results.md) for guidance on:
- Understanding key footnote disclosures
- Evaluating accounting policy changes
- Assessing critical estimates
- Identifying hidden risks

## Example Queries

**Full Footnote Analysis:**
```
Analyze the footnotes and accounting policies from NVDA's latest quarterly filing.
```

**Revenue Recognition:**
```
Extract the revenue recognition policies and performance obligations from MSFT's latest 10-K footnotes.
```

**Lease Obligations:**
```
Analyze the lease footnotes and operating lease obligations from AMZN's latest 10-K.
```

**Debt Details:**
```
Extract debt maturity schedule and terms from AAPL's footnotes in the latest 10-K.
```

**Stock Compensation:**
```
Analyze the stock-based compensation footnotes for GOOGL including vesting schedules and expense.
```

**Contingencies:**
```
Extract litigation and contingency disclosures from META's latest 10-K footnotes.
```

## Key Footnote Categories

### Significant Accounting Policies (Note 1/2)

| Policy | What It Covers |
|--------|----------------|
| Revenue Recognition | When and how revenue is recognized |
| Consolidation | Subsidiaries, VIEs, eliminations |
| Cash Equivalents | Definition, components |
| Inventory | Valuation method (FIFO, LIFO, avg) |
| Property & Equipment | Depreciation methods, useful lives |
| Intangibles | Amortization, impairment testing |
| Leases | Classification, measurement |
| Income Taxes | Deferred taxes, uncertain positions |

### Revenue Recognition

| Element | Disclosure |
|---------|------------|
| Performance Obligations | Distinct goods/services |
| Transaction Price | Allocation methodology |
| Timing | Point in time vs. over time |
| Contract Assets/Liabilities | Deferred revenue, unbilled |
| Disaggregation | Revenue by type, geography |

### Fair Value Measurements

| Level | Description |
|-------|-------------|
| Level 1 | Quoted prices in active markets |
| Level 2 | Observable inputs other than Level 1 |
| Level 3 | Unobservable inputs |

### Debt and Financing

| Disclosure | Content |
|------------|---------|
| Terms | Interest rates, covenants |
| Maturities | Repayment schedule |
| Fair Value | Carrying vs. market value |
| Credit Facilities | Availability, usage |

### Leases

| Element | Disclosure |
|---------|------------|
| Classification | Operating vs. finance |
| ROU Assets | Right-of-use asset values |
| Lease Liabilities | Present value of payments |
| Maturity Schedule | Future payment obligations |
| Expense | Lease cost breakdown |

### Commitments and Contingencies

| Type | Disclosure |
|------|------------|
| Legal | Litigation status, reserves |
| Purchase | Contractual obligations |
| Guarantees | Indemnifications, warranties |
| Environmental | Remediation, compliance |

### Stock Compensation

| Element | Disclosure |
|---------|------------|
| Plan Description | Types of awards |
| Expense | Period cost recognized |
| Valuation | Assumptions (volatility, term) |
| Unvested Awards | Outstanding, expected vesting |

## Critical Accounting Estimates

### High Judgment Areas

| Estimate | Risk Factors |
|----------|--------------|
| Goodwill | Impairment testing assumptions |
| Revenue | Variable consideration, returns |
| Allowances | Bad debt, inventory obsolescence |
| Taxes | Uncertain positions, valuation allowance |
| Contingencies | Litigation outcomes, timing |
| Pensions | Discount rate, return assumptions |

### Red Flags in Estimates

1. **Aggressive assumptions** - Below-market discount rates
2. **Inconsistent changes** - Estimate revisions without explanation
3. **Concentrated judgment** - Single estimate driving results
4. **Lack of disclosure** - Vague sensitivity analysis
5. **Trend divergence** - Estimates moving opposite to peers

## New Accounting Standards

### Recently Adopted

Track impact of:
- Revenue recognition (ASC 606)
- Leases (ASC 842)
- Credit losses (ASC 326)
- Income taxes (various)

### Pending Adoption

Monitor upcoming:
- Segment reporting changes
- Crypto asset disclosure
- Climate-related disclosures
- Income tax transparency

## Comparing Footnotes

### Year-over-Year Changes

| Change Type | Significance |
|-------------|--------------|
| New policy | Significant event or standard |
| Policy modification | Changed circumstances |
| Removed disclosure | Issue resolved or consolidated |
| Expanded disclosure | Increased materiality |
| Reduced disclosure | Decreased significance |

### Peer Comparison

Compare across competitors:
- Revenue recognition approaches
- Estimate methodologies
- Disclosure quality
- Policy choices

## Analysis Tips

1. **Start with Note 1**: Summary of significant policies provides foundation.

2. **Track changes**: Compare footnotes year-over-year for policy shifts.

3. **Read related party**: Transactions with insiders reveal governance.

4. **Check subsequent events**: Post-period events may be material.

5. **Cross-reference MD&A**: Management discussion provides context.

6. **Note judgmental areas**: High-estimate disclosures signal risk.

## Use Cases

- **Accounting research**: Understand company's financial reporting
- **Risk assessment**: Identify hidden liabilities and contingencies
- **Valuation support**: Gather inputs for financial modeling
- **Due diligence**: Comprehensive policy review
- **Audit analysis**: Evaluate disclosure quality
