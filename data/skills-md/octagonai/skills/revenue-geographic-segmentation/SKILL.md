---
name: revenue-geographic-segmentation
description: Retrieve detailed revenue breakdown by geographic segment for public companies. Use when analyzing regional exposure, geographic concentration, international expansion, or currency risk assessment.
---

# Revenue Geographic Segmentation

Retrieve detailed revenue breakdown by geographic segment for public companies using Octagon MCP.

## Prerequisites

Ensure Octagon MCP is configured in your AI agent (Cursor, Claude Desktop, Windsurf, etc.). See [references/mcp-setup.md](references/mcp-setup.md) for installation instructions.

## Query Format

```
Retrieve detailed revenue by geographic segment for <TICKER>, for the annual period with a flat response structure.
```

**MCP Call:**

```json
{
  "server": "octagon-mcp",
  "toolName": "octagon-agent",
  "arguments": {
    "prompt": "Retrieve detailed revenue by geographic segment for AAPL, for the annual period with a flat response structure"
  }
}
```

## Output Format

The agent returns a table with revenue by geographic segment across years:

| Fiscal Year | Americas Segment | Europe Segment | Greater China Segment | Japan Segment | Rest of Asia Pacific Segment |
|-------------|-----------------|----------------|----------------------|---------------|------------------------------|
| 2025 | $178,353.00M | $111,032.00M | $64,377.00M | $28,703.00M | $33,696.00M |
| 2024 | $167,045.00M | $101,328.00M | $66,952.00M | $25,052.00M | $30,658.00M |
| 2023 | $162,560.00M | $94,294.00M | $72,559.00M | $24,257.00M | $29,615.00M |
| 2022 | $169,658.00M | $95,118.00M | $74,200.00M | $25,977.00M | $29,375.00M |
| 2021 | $153,306.00M | $89,307.00M | $68,366.00M | $28,482.00M | $26,356.00M |

**Data Source:** octagon-financials-agent

## Key Observations Pattern

After receiving data, generate observations:

1. **Regional concentration**: Identify largest revenue regions
2. **Growth trends**: Track which regions are growing fastest
3. **Currency exposure**: Assess FX risk by region
4. **Emerging markets**: Monitor developing region growth
5. **Historical evolution**: Track geographic mix changes over time

## Analysis Tips

### Regional Share Calculation
```
Region Share = Region Revenue / Total Revenue × 100
```
Calculate for each region to understand geographic mix.

### Geographic Concentration
- Americas >50% = US-centric
- Single region >60% = high concentration
- Well balanced = no region >40%

### Growth Rate by Region
```
Region Growth = (Current Year - Prior Year) / Prior Year × 100
```
Identify fastest and slowest growing regions.

### Currency Implications
Regional exposure implies currency risk:
- Americas: USD (base currency typically)
- Europe: EUR, GBP exposure
- Greater China: CNY exposure
- Japan: JPY exposure
- Rest of Asia Pacific: Mixed currencies

### Geopolitical Risk
Consider regional risks:
- Trade tensions (US-China)
- Regulatory environment
- Economic cycles
- Political stability

## Strategic Analysis

### International Expansion
Track over time:
- Is international share growing?
- Which regions showing momentum?
- New market entries?

### Market Penetration
Compare to:
- Regional GDP or population
- Addressable market size
- Competitor regional presence

### Diversification Benefits
Balanced geographic mix provides:
- Currency hedging (natural)
- Economic cycle diversification
- Regulatory risk distribution

## Segment Evolution

### Long-term Trends
Observe over 10+ years:
- Americas: Typically stable, large base
- Europe: Steady growth
- Greater China: Rapid expansion then maturation
- Emerging Asia: High growth potential

### Inflection Points
Note significant changes:
- New market entries
- Trade policy impacts
- Pandemic effects
- Currency devaluations

## Follow-up Queries

Based on results, suggest deeper analysis:

- "What factors drove the Americas Segment's revenue growth from [YEAR1] to [YEAR2]?"
- "How has [COMPANY]'s product mix evolved across geographic segments?"
- "What percentage of total revenue does each geographic segment represent in [YEAR]?"
- "Compare [COMPANY]'s geographic revenue mix to [PEER1] and [PEER2]"
