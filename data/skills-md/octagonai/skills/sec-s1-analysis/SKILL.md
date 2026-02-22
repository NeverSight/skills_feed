---
name: sec-s1-analysis
description: Analyze S-1 registration statements for IPOs using Octagon MCP. Use when researching pre-IPO companies, extracting business models, risk factors, use of proceeds, capitalization, principal shareholders, and growth opportunities from IPO filings.
---

# SEC S-1 Analysis

Analyze S-1 registration statements (IPO filings) for companies going public using the Octagon MCP server.

## Prerequisites

Ensure Octagon MCP is configured in your AI agent (Cursor, Claude Desktop, Windsurf, etc.). See [references/mcp-setup.md](references/mcp-setup.md) for installation instructions.

## Workflow

### 1. Identify Analysis Parameters

Determine the following before querying:
- **Company Name**: Name of the company filing for IPO
- **Focus Area** (optional): Risks, opportunities, financials, capitalization
- **Specific Topics** (optional): Use of proceeds, shareholders, governance

### 2. Execute Query via Octagon MCP

Use the `octagon-agent` tool with a natural language prompt:

```
Analyze the S-1 registration statement for <COMPANY> and extract key business risks and opportunities.
```

**MCP Call Format:**

```json
{
  "server": "octagon-mcp",
  "toolName": "octagon-agent",
  "arguments": {
    "prompt": "Analyze the S-1 registration statement for Figma and extract key business risks and opportunities."
  }
}
```

### 3. Expected Output

The agent returns structured S-1 analysis including:

**Key Business Risks:**
- Customer retention and growth challenges
- Technological and market competition
- Regulatory and operational risks
- Internal management and control concerns

**Key Opportunities:**
- Product innovation and platform enhancements
- Customer expansion and conversion
- International growth
- Strategic acquisitions

**Data Sources**: octagon-sec-agent

### 4. Interpret Results

See [references/interpreting-results.md](references/interpreting-results.md) for guidance on:
- Understanding S-1 structure
- Evaluating IPO risks
- Assessing business model viability
- Analyzing capitalization and ownership

## Example Queries

**Full S-1 Analysis:**
```
Analyze the S-1 registration statement for Figma and extract key business risks and opportunities.
```

**Business Model:**
```
Extract the business model and revenue streams from Stripe's S-1 filing.
```

**Use of Proceeds:**
```
What are the planned use of proceeds from the IPO in Reddit's S-1?
```

**Capitalization:**
```
Analyze the capitalization table and share structure from Instacart's S-1.
```

**Principal Shareholders:**
```
Who are the principal shareholders and what are their ownership stakes in Arm's S-1?
```

**Financial Performance:**
```
Extract the historical financial performance and growth metrics from Klaviyo's S-1.
```

## S-1 Key Sections

### Prospectus Summary

| Section | Content |
|---------|---------|
| Business Overview | What the company does |
| The Offering | Shares offered, price range |
| Risk Factor Summary | Key risks highlighted |
| Use of Proceeds | How IPO funds will be used |

### Risk Factors

| Category | Common Risks |
|----------|--------------|
| Business | Competition, customer concentration |
| Financial | Losses, cash burn, liquidity |
| Operational | Scaling, key personnel |
| Regulatory | Compliance, legal proceedings |
| Market | Economic conditions, industry trends |
| Offering | Dilution, stock volatility |

### Business Description

| Section | Content |
|---------|---------|
| Company History | Founding, milestones |
| Products/Services | Offerings, technology |
| Market Opportunity | TAM, SAM, SOM |
| Growth Strategy | Expansion plans |
| Competition | Competitive landscape |

### Management's Discussion (MD&A)

| Section | Content |
|---------|---------|
| Results of Operations | Historical performance |
| Key Metrics | Operating KPIs |
| Liquidity | Cash position, burn rate |
| Critical Policies | Accounting judgments |

### Financial Statements

| Statement | Key Metrics |
|-----------|-------------|
| Income Statement | Revenue, losses, margins |
| Balance Sheet | Assets, liabilities, equity |
| Cash Flow | Operating, investing, financing |
| Notes | Accounting policies, details |

### Capitalization

| Section | Content |
|---------|---------|
| Pre-IPO Cap Table | Existing ownership |
| Post-IPO Structure | Dilution effects |
| Share Classes | Voting rights, preferences |
| Options/Warrants | Outstanding instruments |

### Principal Shareholders

| Disclosure | Content |
|------------|---------|
| 5%+ Owners | Major shareholders |
| Directors/Officers | Management ownership |
| Selling Shareholders | Who is selling |
| Lock-up | Restrictions on sales |

## IPO Analysis Framework

### Business Quality Assessment

| Factor | Strong | Weak |
|--------|--------|------|
| Revenue Growth | >30% YoY | <10% or declining |
| Gross Margin | >60% | <30% |
| Net Revenue Retention | >120% | <100% |
| Customer Concentration | Low (<10% top customer) | High (>25% top customer) |
| Unit Economics | CAC payback <18mo | Never payback |

### Market Opportunity

| Factor | Positive | Concern |
|--------|----------|---------|
| TAM Size | Large and growing | Small or saturated |
| Market Position | Leader or fast follower | Late entrant |
| Competitive Moat | Strong differentiation | Commoditized |
| Secular Trends | Tailwinds | Headwinds |

### Financial Health

| Metric | Healthy | Concerning |
|--------|---------|------------|
| Cash Runway | >24 months | <12 months |
| Path to Profitability | Clear, near-term | Unclear, distant |
| Burn Rate | Decreasing | Accelerating |
| Working Capital | Positive | Negative |

### Governance Structure

| Factor | Shareholder-Friendly | Concern |
|--------|---------------------|---------|
| Share Classes | Single class | Multi-class voting |
| Board Independence | Majority independent | Controlled |
| Founder Control | Reasonable | Perpetual control |
| Antitakeover | None/limited | Poison pill, staggered |

## Risk Factor Analysis

### Risk Prioritization

| Risk Type | Materiality Indicators |
|-----------|----------------------|
| Critical | First listed, extensive detail |
| Significant | Multiple paragraphs |
| Moderate | Standard disclosure |
| Boilerplate | Generic, brief |

### Red Flags in Risk Factors

1. **Going concern** - Questions about survival
2. **Material weakness** - Internal control issues
3. **Regulatory investigation** - Government scrutiny
4. **Key customer loss** - Revenue concentration
5. **Founder departure** - Leadership instability
6. **Litigation** - Significant legal exposure
7. **Related party** - Insider transactions

## Use of Proceeds Analysis

### Common Uses

| Use | Positive Sign | Concern |
|-----|---------------|---------|
| R&D Investment | Growth focus | Unclear allocation |
| Sales Expansion | Market capture | Unproven markets |
| Working Capital | Flexibility | Cash burn funding |
| Debt Repayment | Deleveraging | Refinancing distress |
| M&A | Strategic growth | Vague "opportunities" |
| General Corporate | Flexibility | Lack of specific plan |

### Shareholder Liquidity

Watch for:
- Proceeds to company vs. selling shareholders
- Insider selling proportions
- Lock-up terms and expiration

## Valuation Context

### Pre-IPO Metrics

| Metric | Calculation |
|--------|-------------|
| Revenue Multiple | Valuation / Revenue |
| Gross Profit Multiple | Valuation / Gross Profit |
| Price/Sales | Post-money / Revenue |
| Implied Growth | Embedded expectations |

### Comparable Analysis

Compare to:
- Recent IPOs in sector
- Public company peers
- Prior funding rounds

## Analysis Tips

1. **Read risk factors carefully**: Order and detail indicate materiality.

2. **Track insider participation**: Selling vs. holding signals confidence.

3. **Verify TAM claims**: Companies often overstate market size.

4. **Check customer metrics**: Retention, concentration, churn.

5. **Understand share structure**: Multi-class can limit shareholder rights.

6. **Review lock-up terms**: Post-IPO supply pressure.

## Use Cases

- **IPO investing**: Evaluate new public offerings
- **Private market research**: Understand pre-IPO companies
- **Competitive intelligence**: Analyze emerging competitors
- **Industry research**: Track sector trends through filings
- **Due diligence**: Comprehensive company assessment
