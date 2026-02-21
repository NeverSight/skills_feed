---
name: sec-amendments-review
description: Review amendments to SEC filings using Octagon MCP. Use when tracking material changes, corrections, restatements, and updates to previously filed documents including 10-K/A, 10-Q/A, 8-K/A, S-1/A, and Form 144/A filings.
---

# SEC Amendments Review

Review amendments to SEC filings and identify material changes or corrections for public companies using the Octagon MCP server.

## Prerequisites

Ensure Octagon MCP is configured in your AI agent (Cursor, Claude Desktop, Windsurf, etc.). See [references/mcp-setup.md](references/mcp-setup.md) for installation instructions.

## Workflow

### 1. Identify Analysis Parameters

Determine the following before querying:
- **Ticker**: Stock symbol (e.g., AAPL, MSFT, GOOGL)
- **Time Period** (optional): Recent amendments, specific date range
- **Filing Type** (optional): Specific amendment types of interest

### 2. Execute Query via Octagon MCP

Use the `octagon-agent` tool with a natural language prompt:

```
Review recent amendments to SEC filings for <TICKER> and identify material changes or corrections.
```

**MCP Call Format:**

```json
{
  "server": "octagon-mcp",
  "toolName": "octagon-agent",
  "arguments": {
    "prompt": "Review recent amendments to SEC filings for AMZN and identify material changes or corrections."
  }
}
```

### 3. Expected Output

The agent returns structured amendment analysis including:

**Recent Amendments:**
- Form 144/A: Amended report of proposed securities sales
- Filing date and description
- Material changes identified

**Related Filings:**
- Original filings being amended
- Subsequent transactions (e.g., bond offerings)

**Data Sources**: octagon-sec-agent, octagon-web-search-agent

### 4. Interpret Results

See [references/interpreting-results.md](references/interpreting-results.md) for guidance on:
- Understanding amendment types
- Assessing materiality of changes
- Tracking restatement patterns
- Evaluating correction significance

## Example Queries

**General Amendment Review:**
```
Review recent amendments to SEC filings for AMZN and identify material changes or corrections.
```

**10-K Amendments:**
```
Has TSLA filed any 10-K/A amendments in the past year and what changes were made?
```

**Restatement Search:**
```
Identify any financial restatements or 10-Q/A amendments filed by META in 2025.
```

**S-1 Amendment Tracking:**
```
Track the S-1/A amendments filed by Reddit during their IPO process.
```

**8-K Corrections:**
```
Find any 8-K/A amendments for NVDA that corrected prior disclosures.
```

**Proxy Amendments:**
```
Review DEF 14A amendments for AAPL and identify changes to compensation disclosures.
```

## Amendment Types

### Periodic Report Amendments

| Form | Original | Amendment |
|------|----------|-----------|
| Annual Report | 10-K | 10-K/A |
| Quarterly Report | 10-Q | 10-Q/A |
| Current Report | 8-K | 8-K/A |
| Transition Report | 10-KT | 10-KT/A |

### Registration Statement Amendments

| Form | Original | Amendment |
|------|----------|-----------|
| IPO Registration | S-1 | S-1/A |
| Shelf Registration | S-3 | S-3/A |
| M&A Registration | S-4 | S-4/A |
| Employee Plans | S-8 | S-8/A |

### Proxy Statement Amendments

| Form | Original | Amendment |
|------|----------|-----------|
| Definitive Proxy | DEF 14A | DEFA14A |
| Preliminary Proxy | PRE 14A | PREA14A |
| Contested Proxy | DEFC14A | N/A |

### Other Amendments

| Form | Description |
|------|-------------|
| Form 144/A | Amended proposed securities sale |
| Schedule 13D/A | Amended beneficial ownership (>5%) |
| Schedule 13G/A | Amended passive investor disclosure |
| Form 3/A, 4/A, 5/A | Amended insider ownership |

## Reasons for Amendments

### Financial Restatements

| Reason | Severity |
|--------|----------|
| Accounting Error | High |
| Revenue Recognition | High |
| Expense Timing | Medium |
| Classification Error | Medium |
| Rounding/Typo | Low |

### Disclosure Updates

| Reason | Typical Content |
|--------|-----------------|
| Additional Information | Expanded details |
| Clarification | Improved explanation |
| Correction | Fixed errors |
| Subsequent Events | New developments |
| Exhibit Updates | New or corrected exhibits |

### Registration Statement Updates

| Reason | Purpose |
|--------|---------|
| SEC Comments | Response to staff review |
| Pricing Update | Final terms |
| Financial Update | More recent financials |
| Material Change | Business developments |
| Risk Factor Update | New risks identified |

## Materiality Assessment

### High Materiality Amendments

| Type | Indicators |
|------|------------|
| Restatement | Changed reported numbers |
| Control Weakness | Internal control issues |
| Regulatory | Government action response |
| Legal | Litigation developments |
| M&A | Deal term changes |

### Medium Materiality Amendments

| Type | Indicators |
|------|------------|
| Clarification | Expanded disclosure |
| Reclassification | Changed categories |
| Exhibit | New supporting documents |
| Officer | Management updates |

### Low Materiality Amendments

| Type | Indicators |
|------|------------|
| Typographical | Spelling, formatting |
| Administrative | Signatures, dates |
| Cross-reference | Citation fixes |
| Exhibit | Technical corrections |

## Amendment Analysis Framework

### Key Questions

1. **What changed?** - Specific sections modified
2. **Why?** - Stated reason for amendment
3. **When?** - Timing relative to original
4. **How material?** - Impact on financials/operations
5. **Pattern?** - History of amendments

### Red Flags

1. **Frequent restatements** - Recurring accuracy issues
2. **Delayed amendments** - Long gaps from original
3. **Material weakness** - Control deficiencies
4. **SEC comment response** - Regulatory concerns
5. **Multiple rounds** - Repeated amendments
6. **Downward revisions** - Reduced financials

## S-1/A Amendment Tracking

### IPO Amendment Progression

| Amendment | Typical Content |
|-----------|-----------------|
| S-1/A #1 | SEC comment responses |
| S-1/A #2 | Additional responses, updates |
| S-1/A #3+ | Further refinements |
| Final S-1/A | Pricing, final terms |

### Key Changes to Track

| Section | What Changes |
|---------|--------------|
| Risk Factors | New risks, updated language |
| Financials | More recent quarters |
| Valuation | Price range updates |
| Use of Proceeds | Refined allocation |
| Shares Offered | Final share count |

## 10-K/A and 10-Q/A Analysis

### Common Amendment Reasons

| Reason | Frequency |
|--------|-----------|
| Restatement | Uncommon, serious |
| Control Disclosure | Moderate |
| Exhibit Filing | Common |
| Signature | Common |
| XBRL Correction | Common |

### Financial Impact Assessment

| Change | How to Assess |
|--------|---------------|
| Revenue | Compare restated vs. original |
| Earnings | Impact on EPS, net income |
| Balance Sheet | Asset/liability changes |
| Cash Flow | Operating cash adjustments |
| Ratios | Covenant, metric impacts |

## 8-K/A Analysis

### Amendment Purposes

| Purpose | Content |
|---------|---------|
| Correction | Fix errors in original |
| Additional Info | Complete disclosure |
| Exhibit | Add omitted documents |
| Financial Statements | Required within 71 days |

### Timing Considerations

| Timing | Interpretation |
|--------|----------------|
| Same day | Quick correction |
| Within week | Discovered error |
| Within month | Deliberate update |
| Extended | Potential concern |

## Tracking Amendment Patterns

### Company History

Track over time:
- Frequency of amendments
- Types filed
- Reasons stated
- Time to amend

### Peer Comparison

Compare to industry:
- Amendment frequency
- Types of corrections
- Materiality levels
- Response times

## Analysis Tips

1. **Compare versions**: Use SEC compare tools to see exact changes.

2. **Read cover page**: Amendment reason often stated upfront.

3. **Check exhibits**: Often key documents added/corrected.

4. **Note timing**: Gaps between filings reveal issues.

5. **Track patterns**: Recurring amendments signal problems.

6. **Cross-reference 8-Ks**: Material amendments often disclosed.

## Use Cases

- **Due diligence**: Identify correction history
- **Risk assessment**: Track restatement patterns
- **IPO analysis**: Monitor S-1 amendment progression
- **Governance review**: Evaluate filing quality
- **Compliance monitoring**: Track regulatory responses
