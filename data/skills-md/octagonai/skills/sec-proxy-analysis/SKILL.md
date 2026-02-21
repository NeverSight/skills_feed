---
name: sec-proxy-analysis
description: Analyze proxy statements (DEF 14A) to extract executive compensation, governance information, and shareholder voting matters using Octagon MCP. Use when researching CEO pay, board composition, say-on-pay votes, and corporate governance practices.
---

# SEC Proxy Analysis

Analyze proxy statements (DEF 14A) to extract executive compensation and governance information for public companies using the Octagon MCP server.

## Prerequisites

Ensure Octagon MCP is configured in your AI agent (Cursor, Claude Desktop, Windsurf, etc.). See [references/mcp-setup.md](references/mcp-setup.md) for installation instructions.

## Workflow

### 1. Identify Analysis Parameters

Determine the following before querying:
- **Ticker**: Stock symbol (e.g., AAPL, MSFT, GOOGL)
- **Focus Area** (optional): Compensation, governance, proposals
- **Comparison** (optional): Peer companies, prior years

### 2. Execute Query via Octagon MCP

Use the `octagon-agent` tool with a natural language prompt:

```
Extract executive compensation details and governance information from <TICKER>'s latest proxy statement.
```

**MCP Call Format:**

```json
{
  "server": "octagon-mcp",
  "toolName": "octagon-agent",
  "arguments": {
    "prompt": "Extract executive compensation details and governance information from TSLA's latest proxy statement."
  }
}
```

### 3. Expected Output

The agent returns structured proxy analysis including:

**Director Compensation:**
- Stock awards valued at over $3 billion collectively
- Comparison to peer compensation levels

**Governance Framework:**
- Board standards for employees, officers, and directors
- Governance policies and oversight

**Voting Matters:**
- Non-binding votes on executive compensation frequency
- Director compensation disclosures

**Data Sources**: octagon-companies-agent, octagon-sec-agent, octagon-web-search-agent

### 4. Interpret Results

See [references/interpreting-results.md](references/interpreting-results.md) for guidance on:
- Understanding compensation structures
- Evaluating governance practices
- Analyzing shareholder proposals
- Comparing to peer companies

## Example Queries

**Full Proxy Analysis:**
```
Extract executive compensation details and governance information from TSLA's latest proxy statement.
```

**CEO Compensation Focus:**
```
What is the total compensation for AAPL's CEO in the latest proxy statement?
```

**Board Composition:**
```
Analyze the board of directors composition and independence from MSFT's latest DEF 14A.
```

**Say-on-Pay Results:**
```
What were the say-on-pay voting results for AMZN in their latest proxy?
```

**Peer Comparison:**
```
Compare executive compensation between GOOGL and META based on their latest proxy statements.
```

**Shareholder Proposals:**
```
What shareholder proposals were included in JPM's latest proxy statement and how did they fare?
```

## Proxy Statement Components

### Executive Compensation (Item 402)

| Component | Description |
|-----------|-------------|
| Summary Compensation Table | Total pay for Named Executive Officers (NEOs) |
| Salary | Base salary amounts |
| Bonus | Cash bonus payments |
| Stock Awards | Equity grants at grant date fair value |
| Option Awards | Stock options at grant date fair value |
| Non-Equity Incentive | Performance-based cash compensation |
| Pension Value | Change in pension/deferred compensation |
| All Other Compensation | Perks, 401(k) match, insurance |

### CEO Pay Ratio

| Element | Description |
|---------|-------------|
| CEO Total Compensation | All-in CEO pay |
| Median Employee Pay | Median worker compensation |
| Pay Ratio | CEO pay / median employee pay |

### Compensation Discussion & Analysis (CD&A)

| Section | Content |
|---------|---------|
| Philosophy | Compensation objectives and strategy |
| Pay Mix | Balance of fixed vs. variable pay |
| Performance Metrics | Goals used for incentive pay |
| Peer Group | Companies used for benchmarking |
| Decisions | Rationale for pay decisions |

### Corporate Governance

| Area | Details |
|------|---------|
| Board Composition | Directors, independence, diversity |
| Committees | Audit, Compensation, Nominating |
| Leadership Structure | Chair/CEO separation, lead director |
| Risk Oversight | Board role in risk management |
| Shareholder Rights | Voting standards, proxy access |

### Shareholder Proposals

| Type | Common Topics |
|------|---------------|
| Governance | Board declassification, majority voting |
| Environmental | Climate disclosure, emissions targets |
| Social | Human rights, DEI reporting |
| Compensation | Pay for performance, clawbacks |

## Compensation Analysis

### Pay Components Breakdown

| Component | Typical Range | What to Look For |
|-----------|---------------|------------------|
| Base Salary | 10-20% | Stability, changes |
| Cash Bonus | 15-25% | Metrics, achievement |
| Stock Awards | 40-60% | Vesting, performance |
| Options | 5-15% | Strike price, term |
| Other | 1-5% | Perks, benefits |

### Pay-for-Performance Alignment

| Metric | Strong Alignment | Weak Alignment |
|--------|------------------|----------------|
| TSR Correlation | Pay tracks returns | Pay disconnected |
| Metric Rigor | Challenging targets | Easy thresholds |
| Vesting | Performance-based | Time-based only |
| Peer Rank | Median position | Outlier high |

### Red Flags in Compensation

1. **Excessive perks** - Private jets, security, housing
2. **Guaranteed bonuses** - No performance link
3. **Option repricing** - Underwater options reset
4. **Pension spiking** - Inflated pension values
5. **Golden parachutes** - Excessive change-in-control pay
6. **Tax gross-ups** - Company pays executive taxes

## Governance Assessment

### Board Quality Indicators

| Factor | Strong Governance | Weak Governance |
|--------|-------------------|-----------------|
| Independence | >75% independent | <50% independent |
| Diversity | Diverse backgrounds | Homogeneous |
| Tenure | Balanced mix | All long-tenured |
| Overboarding | Limited seats | Directors overcommitted |
| Attendance | >90% average | Low attendance |

### Committee Structure

| Committee | Key Oversight | Best Practices |
|-----------|---------------|----------------|
| Audit | Financials, controls | All independent, financial experts |
| Compensation | Executive pay | All independent, no interlocks |
| Nominating | Board composition | Independent, clear criteria |
| Risk | Enterprise risk | Defined charter, regular meetings |

### Shareholder Rights

| Right | Shareholder-Friendly | Concern |
|-------|---------------------|---------|
| Voting Standard | Majority voting | Plurality only |
| Proxy Access | Available | Not available |
| Special Meetings | Low threshold | High/no threshold |
| Written Consent | Allowed | Prohibited |
| Dual Class | Single class | Multi-class voting |

## Voting Analysis

### Say-on-Pay Voting

| Support Level | Interpretation |
|---------------|----------------|
| >90% | Strong approval |
| 70-90% | Acceptable |
| 50-70% | Concerns raised |
| <50% | Failed - action required |

### Director Elections

| Support Level | Interpretation |
|---------------|----------------|
| >95% | Strong support |
| 80-95% | Normal range |
| <80% | Significant opposition |
| <50% | Failed (if majority vote) |

### Shareholder Proposals

| Support Level | Interpretation |
|---------------|----------------|
| >50% | Passed - expect action |
| 30-50% | Significant support |
| 20-30% | Moderate interest |
| <20% | Limited support |

## Analysis Tips

1. **Track trends**: Compare compensation over 3-5 years, not just one year.

2. **Read the CD&A**: Narrative explains rationale behind numbers.

3. **Check peer group**: Ensure peers are truly comparable.

4. **Note changes**: New compensation elements or governance provisions.

5. **Follow the votes**: Declining support signals concerns.

6. **Review related transactions**: Conflicts of interest disclosed.

## Use Cases

- **Investment analysis**: Assess management alignment with shareholders
- **Governance screening**: Evaluate board quality and practices
- **Activist research**: Identify governance improvement opportunities
- **Compensation benchmarking**: Compare pay across companies
- **ESG analysis**: Evaluate social and governance factors
