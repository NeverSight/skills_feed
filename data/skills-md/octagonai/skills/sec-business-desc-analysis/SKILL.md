---
name: sec-business-desc-analysis
description: Extract and analyze business descriptions and competitive landscape from SEC filings using Octagon MCP. Use when researching company business models, market positioning, competitive advantages, industry dynamics, and strategic focus areas from Item 1 disclosures.
---

# SEC Business Description Analysis

Extract and summarize business descriptions and competitive landscape from SEC filings for public companies using the Octagon MCP server.

## Prerequisites

Ensure Octagon MCP is configured in your AI agent (Cursor, Claude Desktop, Windsurf, etc.). See [references/mcp-setup.md](references/mcp-setup.md) for installation instructions.

## Workflow

### 1. Identify Analysis Parameters

Determine the following before querying:
- **Ticker**: Stock symbol (e.g., AAPL, MSFT, GOOGL)
- **Focus Area** (optional): Business model, competition, strategy
- **Comparison** (optional): Prior years, competitors

### 2. Execute Query via Octagon MCP

Use the `octagon-agent` tool with a natural language prompt:

```
Extract and summarize the business description and competitive landscape from <TICKER>'s latest 10-K filing.
```

**MCP Call Format:**

```json
{
  "server": "octagon-mcp",
  "toolName": "octagon-agent",
  "arguments": {
    "prompt": "Extract and summarize the business description and competitive landscape from GOOGL's latest 10-K filing."
  }
}
```

### 3. Expected Output

The agent returns structured business analysis including:

**Business Structure:**
- Primary segments: Google Services, Google Cloud
- Other Bets: Early-stage ventures
- Core mission and strategic focus

**Competitive Landscape:**
- Key competitive sectors
- Competitive strengths (innovation, brand, AI investments)
- Market positioning

**Data Sources**: octagon-sec-agent

### 4. Interpret Results

See [references/interpreting-results.md](references/interpreting-results.md) for guidance on:
- Understanding business model components
- Evaluating competitive positioning
- Analyzing strategic priorities
- Comparing across competitors

## Example Queries

**Full Business Analysis:**
```
Extract and summarize the business description and competitive landscape from GOOGL's latest 10-K filing.
```

**Segment Focus:**
```
Describe the business segments and their revenue contribution for AMZN from the latest 10-K.
```

**Competitive Analysis:**
```
What does MSFT identify as its key competitive advantages in the cloud computing market?
```

**Strategic Priorities:**
```
Extract the strategic priorities and growth initiatives from AAPL's latest 10-K business description.
```

**Market Position:**
```
How does META describe its competitive position in the social media and advertising markets?
```

**Year-over-Year Comparison:**
```
Compare the business description section between TSLA's 2024 and 2023 10-K filings.
```

## Item 1 Components

### Business Overview

| Section | Content |
|---------|---------|
| General | Company history, structure, mission |
| Products & Services | Offerings, features, capabilities |
| Segments | Business unit descriptions |
| Revenue Model | How the company generates revenue |
| Customers | Target markets, key customers |

### Industry & Competition

| Section | Content |
|---------|---------|
| Industry Background | Market size, trends, dynamics |
| Competitive Landscape | Key competitors, market position |
| Competitive Factors | Basis of competition |
| Barriers to Entry | Moats and advantages |
| Market Share | Position in key markets |

### Operations

| Section | Content |
|---------|---------|
| Manufacturing | Production capabilities, facilities |
| Supply Chain | Sourcing, distribution, logistics |
| Intellectual Property | Patents, trademarks, trade secrets |
| R&D | Research focus, innovation pipeline |
| Employees | Workforce composition, culture |

### Regulatory Environment

| Section | Content |
|---------|---------|
| Regulations | Industry-specific requirements |
| Compliance | Regulatory obligations |
| Licenses | Required permits, approvals |
| Environmental | Sustainability, emissions |

## Competitive Analysis Framework

### Porter's Five Forces

| Force | What to Look For |
|-------|------------------|
| Rivalry | Number/strength of competitors, industry growth |
| New Entrants | Barriers to entry, capital requirements |
| Substitutes | Alternative products/services |
| Buyer Power | Customer concentration, switching costs |
| Supplier Power | Input dependencies, alternatives |

### Competitive Advantages

| Type | Examples |
|------|----------|
| Cost Leadership | Scale economies, operational efficiency |
| Differentiation | Brand, technology, quality |
| Network Effects | Platform value increases with users |
| Switching Costs | Customer lock-in, integration depth |
| Intangibles | Patents, regulatory licenses, data |

### Competitive Dynamics

| Factor | Strong Position | Weak Position |
|--------|-----------------|---------------|
| Market Share | Leading or growing | Small or declining |
| Brand | Recognized, trusted | Unknown, weak |
| Technology | Leading edge | Lagging |
| Scale | Significant | Limited |
| Pricing Power | Premium pricing | Commodity |

## Business Model Analysis

### Revenue Streams

| Type | Characteristics |
|------|-----------------|
| Product Sales | One-time, inventory-based |
| Services | Recurring, labor-intensive |
| Subscription | Recurring, predictable |
| Advertising | Volume-dependent, cyclical |
| Licensing | High-margin, IP-based |
| Transaction Fees | Volume-driven, platform-based |

### Customer Analysis

| Factor | What to Assess |
|--------|----------------|
| Concentration | Top customer exposure |
| Diversity | Geographic, industry mix |
| Retention | Churn rates, loyalty |
| Acquisition | Cost, channels, efficiency |
| Lifetime Value | Revenue per customer over time |

### Value Chain Position

| Position | Characteristics |
|----------|-----------------|
| Upstream | Raw materials, components |
| Midstream | Manufacturing, processing |
| Downstream | Distribution, retail |
| Platform | Connecting multiple parties |
| Integrated | Multiple value chain positions |

## Strategic Analysis

### Growth Strategies

| Strategy | What to Look For |
|----------|------------------|
| Organic Growth | New products, market expansion |
| M&A | Acquisitions, partnerships |
| Geographic | International expansion |
| Diversification | New markets, verticals |
| Innovation | R&D investment, patents |

### Strategic Priorities

Track management emphasis on:
1. **Core business** - Defending/growing base
2. **New initiatives** - Emerging opportunities
3. **Efficiency** - Cost reduction, optimization
4. **Capital allocation** - Investment priorities
5. **Talent** - Workforce development

### Inflection Points

| Signal | Interpretation |
|--------|----------------|
| New segment created | Major strategic shift |
| Segment eliminated | Exit or consolidation |
| Acquisition integration | Growth through M&A |
| Geographic emphasis | Expansion priorities |
| Technology investment | Innovation focus |

## Comparing Business Descriptions

### Year-over-Year Changes

Track evolution in:
1. **Segment descriptions** - Expanding/contracting focus
2. **Product emphasis** - Shifting priorities
3. **Competitive language** - Changing market view
4. **Strategic messaging** - Evolving priorities
5. **Risk awareness** - Emerging concerns

### Peer Comparisons

Compare across competitors:

| Dimension | Your Company | Peer A | Peer B |
|-----------|--------------|--------|--------|
| Primary Focus | | | |
| Key Differentiator | | | |
| Growth Strategy | | | |
| Competitive Claim | | | |

## Analysis Tips

1. **Read between the lines**: What's emphasized and what's minimized reveals priorities.

2. **Track changes**: Year-over-year differences show strategic evolution.

3. **Compare to peers**: Industry context reveals differentiation claims.

4. **Verify claims**: Cross-reference with financials and external data.

5. **Note specificity**: Concrete details vs. vague language indicates confidence.

6. **Watch for omissions**: Missing topics may signal concerns.

## Use Cases

- **Investment research**: Understand business model and competitive position
- **Due diligence**: Comprehensive company assessment
- **Competitive intelligence**: Compare positioning across industry
- **Strategy analysis**: Evaluate management's strategic direction
- **Industry research**: Map competitive landscape
