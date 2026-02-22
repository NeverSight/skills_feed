---
name: sec-corp-governance
description: Review corporate governance practices and board composition from SEC filings using Octagon MCP. Use when researching board structure, director qualifications, committee composition, governance policies, shareholder rights, and related party transactions from proxy statements.
---

# SEC Corporate Governance

Review corporate governance practices and board composition from SEC filings for public companies using the Octagon MCP server.

## Prerequisites

Ensure Octagon MCP is configured in your AI agent (Cursor, Claude Desktop, Windsurf, etc.). See [references/mcp-setup.md](references/mcp-setup.md) for installation instructions.

## Workflow

### 1. Identify Analysis Parameters

Determine the following before querying:
- **Ticker**: Stock symbol (e.g., AAPL, MSFT, GOOGL)
- **Focus Area** (optional): Board, committees, policies, proposals
- **Comparison** (optional): Prior year, peers

### 2. Execute Query via Octagon MCP

Use the `octagon-agent` tool with a natural language prompt:

```
Review corporate governance practices and board composition from <TICKER>'s latest proxy statement.
```

**MCP Call Format:**

```json
{
  "server": "octagon-mcp",
  "toolName": "octagon-agent",
  "arguments": {
    "prompt": "Review corporate governance practices and board composition from ORCL's latest proxy statement."
  }
}
```

### 3. Expected Output

The agent returns structured governance analysis including:

**Proxy Statement Information:**
- Filing date and annual meeting details
- CEO and key contacts

**Key Governance Areas:**
- Director election proposals
- Shareholder voting policies
- Governance disclosures

**Data Sources**: octagon-companies-agent, octagon-sec-agent, octagon-web-search-agent

### 4. Interpret Results

See [references/interpreting-results.md](references/interpreting-results.md) for guidance on:
- Evaluating board quality
- Assessing governance practices
- Understanding shareholder rights
- Identifying governance concerns

## Example Queries

**Full Governance Review:**
```
Review corporate governance practices and board composition from ORCL's latest proxy statement.
```

**Board Composition:**
```
Analyze board of directors composition, independence, and diversity for AAPL.
```

**Committee Structure:**
```
Extract audit, compensation, and nominating committee details from MSFT's proxy statement.
```

**Director Qualifications:**
```
What qualifications and experience do GOOGL's board nominees bring?
```

**Governance Policies:**
```
Review corporate governance guidelines and policies from JPM's latest proxy.
```

**Shareholder Proposals:**
```
What shareholder proposals are included in AMZN's latest proxy statement?
```

## Board Composition Analysis

### Independence Assessment

| Category | Best Practice |
|----------|---------------|
| Board Independence | >75% independent |
| Lead Director | If CEO is Chair |
| Committee Independence | 100% for key committees |
| Audit Financial Expert | At least one required |

### Director Demographics

| Dimension | What to Track |
|-----------|---------------|
| Gender Diversity | Representation percentages |
| Ethnic Diversity | Background representation |
| Age Distribution | Balanced tenure |
| Geographic | International perspective |
| Industry | Relevant experience |

### Director Qualifications

| Qualification | Relevance |
|---------------|-----------|
| Industry Experience | Sector knowledge |
| CEO/C-Suite Experience | Leadership perspective |
| Financial Expertise | Audit oversight |
| Technology | Digital transformation |
| Risk Management | Enterprise risk |
| International | Global operations |

## Committee Structure

### Audit Committee

| Requirement | Best Practice |
|-------------|---------------|
| Independence | 100% independent |
| Financial Expert | At least one designated |
| Meetings | Quarterly minimum |
| Responsibilities | Financial oversight, internal controls |

### Compensation Committee

| Requirement | Best Practice |
|-------------|---------------|
| Independence | 100% independent |
| Expertise | Executive compensation experience |
| Advisor | Independent consultant |
| Responsibilities | Executive pay, equity plans |

### Nominating/Governance Committee

| Requirement | Best Practice |
|-------------|---------------|
| Independence | Majority independent |
| Responsibilities | Director selection, governance policies |
| Process | Transparent nomination criteria |

### Other Committees

| Committee | Purpose |
|-----------|---------|
| Risk | Enterprise risk oversight |
| Technology | Digital/cyber oversight |
| Sustainability | ESG oversight |
| Finance | Capital allocation |

## Governance Policies

### Key Policies

| Policy | Description |
|--------|-------------|
| Governance Guidelines | Board operating principles |
| Code of Ethics | Conduct standards |
| Stock Ownership | Director/executive requirements |
| Clawback | Compensation recovery |
| Anti-Hedging/Pledging | Stock restrictions |

### Shareholder Rights

| Right | Shareholder-Friendly |
|-------|---------------------|
| Majority Voting | For director elections |
| Proxy Access | Nomination rights |
| Special Meetings | Low threshold (10-25%) |
| Written Consent | Ability to act |
| No Poison Pill | Or with sunset |

### Antitakeover Provisions

| Provision | Effect |
|-----------|--------|
| Classified Board | Delays takeover |
| Supermajority | High approval threshold |
| Poison Pill | Deters acquirers |
| Dual-Class Stock | Concentrates control |
| Blank Check Preferred | Board authority |

## Leadership Structure

### Chair/CEO Separation

| Structure | Assessment |
|-----------|------------|
| Separate Chair | Best practice |
| Combined with Lead | Acceptable with strong lead |
| Combined, No Lead | Concern |

### Lead Director

| Responsibility | Description |
|----------------|-------------|
| Board Leadership | Independent voice |
| Executive Sessions | Leads non-management meetings |
| CEO Evaluation | Performance oversight |
| Shareholder Communication | Access point |

## Related Party Transactions

### Key Disclosures

| Type | What to Review |
|------|----------------|
| Family Transactions | Deals with relatives |
| Director Transactions | Business with directors |
| Major Shareholder | Controlling shareholder deals |
| Officer Transactions | Executive arrangements |

### Red Flags

1. **Material amounts** - Large related party business
2. **Recurring** - Ongoing dependency
3. **Below market** - Off-market terms
4. **Complexity** - Difficult to understand
5. **New relationships** - Recently established

## Director Elections

### Voting Standards

| Standard | Description |
|----------|-------------|
| Majority | Must receive >50% |
| Plurality | Most votes wins |
| Majority of Quorum | >50% of attending |

### Contested Elections

| Factor | What to Track |
|--------|---------------|
| Activist Proposals | Dissident nominees |
| Vote Results | Support levels |
| Settlement | Negotiated outcome |
| Proxy Fight | Full contest |

## Governance Benchmarking

### ISS/Glass Lewis Assessment

| Factor | What Matters |
|--------|--------------|
| Board Quality | Independence, diversity |
| Compensation | Pay for performance |
| Shareholder Rights | Voting, access |
| Audit | Financial oversight |

### Peer Comparison

Compare across competitors:
- Board size and composition
- Committee structure
- Governance policies
- Shareholder rights

## Governance Quality Indicators

### Strong Governance

| Indicator | Description |
|-----------|-------------|
| Independent Board | >80% independent |
| Diverse Board | Multiple dimensions |
| Separate Chair | Or strong lead director |
| Shareholder Rights | Proxy access, majority voting |
| Responsive | Addresses concerns |

### Weak Governance

| Indicator | Description |
|-----------|-------------|
| Low Independence | <50% independent |
| Homogeneous | Lack of diversity |
| Entrenched | Long tenure, classified |
| Limited Rights | Supermajority, no access |
| Unresponsive | Ignores proposals |

## Analysis Tips

1. **Check independence definitions**: Companies may define differently.

2. **Track tenure**: Long-serving directors may be less independent.

3. **Review overboarding**: Directors on too many boards.

4. **Assess attendance**: Low attendance signals disengagement.

5. **Compare to peers**: Industry context matters.

6. **Monitor changes**: Year-over-year governance evolution.

## Use Cases

- **Investment screening**: Governance quality filter
- **Proxy voting**: Inform voting decisions
- **Activist analysis**: Identify targets
- **Risk assessment**: Governance-related risks
- **ESG analysis**: Governance pillar evaluation
