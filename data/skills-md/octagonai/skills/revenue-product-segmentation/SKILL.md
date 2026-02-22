---
name: revenue-product-segmentation
description: Retrieve detailed revenue breakdown by product segment for public companies. Use when analyzing product mix, revenue concentration, segment contribution, or business line performance.
---

# Revenue Product Segmentation

Retrieve detailed revenue breakdown by product segment for public companies using Octagon MCP.

## Prerequisites

Ensure Octagon MCP is configured in your AI agent (Cursor, Claude Desktop, Windsurf, etc.). See [references/mcp-setup.md](references/mcp-setup.md) for installation instructions.

## Query Format

```
Retrieve detailed revenue by product segment for <TICKER>, for the annual period with a flat response structure.
```

**MCP Call:**

```json
{
  "server": "octagon-mcp",
  "toolName": "octagon-agent",
  "arguments": {
    "prompt": "Retrieve detailed revenue by product segment for AAPL, for the annual period with a flat response structure"
  }
}
```

## Output Format

The agent returns a table with revenue by product segment:

| Product Segment | Revenue (USD Billion) |
|-----------------|----------------------|
| iPhone | $209.59 |
| Services | $109.16 |
| Wearables, Home and Accessories | $35.69 |
| Mac | $33.71 |
| iPad | $28.02 |
| **Total** | **$416.17** |

**Data Source:** octagon-financials-agent

## Key Insights Pattern

After receiving data, generate insights:

1. **Revenue concentration**: Calculate each segment as % of total
2. **Core business identification**: Identify largest revenue driver
3. **Growth segments**: Note high-growth or emerging segments
4. **Diversification assessment**: Evaluate revenue balance across segments
5. **Strategic positioning**: Understand product portfolio mix

## Analysis Tips

### Revenue Concentration
Calculate segment share:
```
Segment Share = Segment Revenue / Total Revenue × 100
```
Example: $209.59B / $416.17B = 50.36%

### Concentration Risk
- Single segment >50% = high concentration
- Top 2 segments >80% = moderate concentration
- No segment >30% = well diversified

### Segment Dynamics
Compare to prior periods:
- Which segments are growing share?
- Which are declining?
- Any new segments emerging?

### Margin Implications
Different segments often have different margins:
- Services typically higher margin than hardware
- Premium products vs commodity segments
- Recurring vs one-time revenue

### Strategic Questions
Based on segmentation:
- Is the company transitioning its business model?
- Are growth investments in high-margin segments?
- How does mix compare to competitors?

## Segment Analysis Framework

### Hardware vs Services
For tech companies:
- Hardware: One-time, capital intensive
- Services: Recurring, higher margin, scalable

### Geographic Implications
Segments may have geographic skew:
- Some products stronger in certain regions
- Currency exposure by segment
- Regulatory considerations

### Lifecycle Positioning
Segment maturity assessment:
- Growth phase: High growth, lower margins
- Mature: Stable, optimized margins
- Decline: Shrinking, harvesting

## Follow-up Queries

Based on results, suggest deeper analysis:

- "What are the year-over-year growth rates for each product segment?"
- "How do these revenue figures compare to [COMPANY]'s guidance?"
- "What are the regional breakdowns for [SEGMENT1] and [SEGMENT2] revenue?"
- "Compare [COMPANY]'s product segment mix to [PEER1] and [PEER2]"
