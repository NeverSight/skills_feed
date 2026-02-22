---
name: sec-8k-analysis
description: Analyze 8-K filings to extract material events and corporate changes using Octagon MCP. Use when tracking real-time corporate disclosures, M&A announcements, leadership changes, earnings releases, and other material events requiring immediate investor attention.
---

# SEC 8-K Analysis

Analyze 8-K filings to extract material events and corporate changes for public companies using the Octagon MCP server.

## Prerequisites

Ensure Octagon MCP is configured in your AI agent (Cursor, Claude Desktop, Windsurf, etc.). See [references/mcp-setup.md](references/mcp-setup.md) for installation instructions.

## Workflow

### 1. Identify Analysis Parameters

Determine the following before querying:
- **Ticker**: Stock symbol (e.g., AAPL, MSFT, GOOGL)
- **Time Period** (optional): Recent filings, specific date range
- **Event Type** (optional): Specific 8-K items of interest

### 2. Execute Query via Octagon MCP

Use the `octagon-agent` tool with a natural language prompt:

```
Analyze recent 8-K filings for <TICKER> and extract material events and corporate changes.
```

**MCP Call Format:**

```json
{
  "server": "octagon-mcp",
  "toolName": "octagon-agent",
  "arguments": {
    "prompt": "Analyze recent 8-K filings for AAPL and extract material events and corporate changes."
  }
}
```

### 3. Expected Output

The agent returns structured 8-K analysis including:

**Filing Summary:**
- Filing date: January 29, 2026
- Event category: Item 2.02 (Results of Operations and Financial Condition)

**Material Events:**
- No material corporate changes in this filing
- Financial focus: Q1 2026 results disclosure

**Corporate Changes:**
- No acquisitions, dispositions, or management changes

**Data Sources**: octagon-sec-agent

### 4. Interpret Results

See [references/interpreting-results.md](references/interpreting-results.md) for guidance on:
- Understanding 8-K item categories
- Assessing event materiality
- Tracking corporate changes over time

## Example Queries

**Recent 8-K Analysis:**
```
Analyze recent 8-K filings for AAPL and extract material events and corporate changes.
```

**Leadership Changes:**
```
Find any 8-K filings for TSLA in 2025 that disclose executive departures or appointments.
```

**M&A Activity:**
```
Extract 8-K filings related to acquisitions or mergers for MSFT in the past 6 months.
```

**Earnings Announcements:**
```
Summarize the most recent 8-K earnings release filing for GOOGL.
```

**Material Agreements:**
```
Find 8-K filings disclosing material definitive agreements for AMZN.
```

**Auditor Changes:**
```
Has NVDA filed any 8-K filings regarding auditor changes in the past year?
```

## 8-K Item Categories

### Section 1 - Registrant's Business and Operations

| Item | Description | Materiality |
|------|-------------|-------------|
| 1.01 | Entry into Material Definitive Agreement | High |
| 1.02 | Termination of Material Definitive Agreement | High |
| 1.03 | Bankruptcy or Receivership | Critical |
| 1.04 | Mine Safety Reporting | Industry-specific |
| 1.05 | Material Cybersecurity Incidents | High |

### Section 2 - Financial Information

| Item | Description | Materiality |
|------|-------------|-------------|
| 2.01 | Completion of Acquisition or Disposition | High |
| 2.02 | Results of Operations and Financial Condition | Medium |
| 2.03 | Creation of Direct Financial Obligation | High |
| 2.04 | Triggering Events (Acceleration) | High |
| 2.05 | Costs for Exit or Disposal Activities | Medium |
| 2.06 | Material Impairments | High |

### Section 3 - Securities and Trading Markets

| Item | Description | Materiality |
|------|-------------|-------------|
| 3.01 | Notice of Delisting or Transfer | Critical |
| 3.02 | Unregistered Sales of Equity | Medium |
| 3.03 | Material Modification to Rights | High |

### Section 4 - Matters Related to Accountants and Financial Statements

| Item | Description | Materiality |
|------|-------------|-------------|
| 4.01 | Changes in Certifying Accountant | High |
| 4.02 | Non-Reliance on Previously Issued Financials | Critical |

### Section 5 - Corporate Governance and Management

| Item | Description | Materiality |
|------|-------------|-------------|
| 5.01 | Changes in Control | Critical |
| 5.02 | Departure/Appointment of Directors/Officers | High |
| 5.03 | Amendments to Articles/Bylaws | Medium |
| 5.04 | Temporary Suspension of Trading | High |
| 5.05 | Amendments to Code of Ethics | Medium |
| 5.06 | Change in Shell Company Status | High |
| 5.07 | Shareholder Vote Results | Medium |
| 5.08 | Shareholder Nominations | Low |

### Section 6 - Asset-Backed Securities

| Item | Description | Materiality |
|------|-------------|-------------|
| 6.01-6.05 | ABS-specific disclosures | Industry-specific |

### Section 7 - Regulation FD

| Item | Description | Materiality |
|------|-------------|-------------|
| 7.01 | Regulation FD Disclosure | Varies |

### Section 8 - Other Events

| Item | Description | Materiality |
|------|-------------|-------------|
| 8.01 | Other Events (Voluntary) | Varies |

### Section 9 - Financial Statements and Exhibits

| Item | Description | Materiality |
|------|-------------|-------------|
| 9.01 | Financial Statements and Exhibits | Supporting |

## Event Materiality Assessment

### Critical Events (Immediate Action)

| Event Type | Examples |
|------------|----------|
| Bankruptcy | Chapter 11 filing, receivership |
| Restatement | Non-reliance on financials |
| Delisting | Exchange notice received |
| Control Change | Acquisition, tender offer |
| Cyber Incident | Material breach disclosed |

### High Priority Events

| Event Type | Examples |
|------------|----------|
| M&A | Acquisition completion, divestitures |
| Leadership | CEO/CFO departure, board changes |
| Agreements | Major contracts, partnerships |
| Financial | Impairments, debt obligations |
| Auditor | Auditor change, disagreements |

### Medium Priority Events

| Event Type | Examples |
|------------|----------|
| Earnings | Quarterly results (Item 2.02) |
| Restructuring | Cost reduction programs |
| Governance | Bylaw amendments, vote results |
| Securities | Stock issuances, modifications |

## Tracking 8-K Patterns

### Frequency Analysis

| Pattern | What It May Indicate |
|---------|---------------------|
| High frequency | Active M&A, restructuring, volatility |
| Low frequency | Stable operations, mature company |
| Clustered | Major corporate event unfolding |
| Regular | Routine quarterly disclosures |

### Content Evolution

Track over time:
1. **Recurring themes** - Ongoing issues or strategies
2. **New item types** - Emerging concerns or opportunities
3. **Tone changes** - Shifting management sentiment
4. **Exhibit quality** - Detail and transparency level

## Analysis Tips

1. **Check all items**: 8-Ks often contain multiple items - don't focus only on headlines.

2. **Read exhibits**: Press releases and agreements in exhibits contain critical details.

3. **Note timing**: Friday afternoon or holiday filings may attempt to minimize attention.

4. **Track patterns**: Frequent 8-Ks may signal ongoing corporate activity.

5. **Cross-reference**: Compare 8-K disclosures with subsequent 10-Q/10-K filings.

6. **Monitor amendments**: 8-K/A filings update or correct prior disclosures.

## Use Cases

- **Event-driven investing**: Track material events for trading signals
- **M&A monitoring**: Follow acquisition announcements and completions
- **Governance oversight**: Monitor leadership and board changes
- **Risk management**: Identify material risks as they emerge
- **Compliance tracking**: Ensure timely disclosure monitoring
