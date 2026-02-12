---
name: analyst-estimates
description: Retrieve analyst financial estimates including Revenue and EPS projections with low/high ranges and analyst coverage. Use when analyzing forward expectations, consensus estimates, valuation inputs, or comparing projections to historical performance.
---

# Analyst Estimates

Retrieve analyst financial estimates for public companies using Octagon MCP.

## Prerequisites

Ensure Octagon MCP is configured in your AI agent (Cursor, Claude Desktop, Windsurf, etc.). See [references/mcp-setup.md](references/mcp-setup.md) for installation instructions.

## Query Format

```
Retrieve analyst financial estimates for <TICKER> for the annual period, limited to <N> records on page 0.
```

**MCP Call:**

```json
{
  "server": "octagon-mcp",
  "toolName": "octagon-agent",
  "arguments": {
    "prompt": "Retrieve analyst financial estimates for AAPL for the annual period, limited to 10 records on page 0"
  }
}
```

## Output Format

The agent returns a table with analyst estimates across future periods:

| Fiscal Year Ending | Revenue Estimate (Low to High) | Revenue Avg | EPS Estimate (Low to High) | EPS Avg | # Revenue Analysts | # EPS Analysts |
|-------------------|-------------------------------|-------------|---------------------------|---------|-------------------|----------------|
| 2030-09-27 | $540.64B - $600.88B | $566.24B | $12.01 - $13.78 | $12.77 | 9 | 6 |
| 2029-09-27 | $520.95B - $578.99B | $545.62B | $10.62 - $12.17 | $11.28 | 13 | 6 |
| 2028-09-27 | $515.19B - $520.48B | $517.84B | $8.96 - $11.18 | $10.20 | 18 | 15 |
| 2027-09-27 | $474.27B - $531.94B | $490.97B | $8.41 - $9.77 | $9.23 | 31 | 30 |
| 2026-09-27 | $445.03B - $483.54B | $460.35B | $7.84 - $8.92 | $8.42 | 24 | 29 |

**Data Source:** octagon-financials-agent

## Key Observations Pattern

After receiving data, generate observations:

1. **Growth trajectory**: Calculate implied revenue and EPS CAGR
2. **Estimate dispersion**: Analyze spread between low and high estimates
3. **Analyst coverage**: Note number of analysts covering each period
4. **Near vs far-term**: Compare confidence in near-term vs long-term estimates
5. **Historical comparison**: Compare estimates to actual historical performance

## Metrics Reference

| Metric | Definition |
|--------|------------|
| Revenue Estimate (Low to High) | Range of analyst revenue projections |
| Revenue Avg | Consensus average revenue estimate |
| EPS Estimate (Low to High) | Range of analyst EPS projections |
| EPS Avg | Consensus average EPS estimate |
| # Revenue Analysts | Number of analysts providing revenue estimates |
| # EPS Analysts | Number of analysts providing EPS estimates |

## Analysis Tips

### Implied Growth Rate
```
Implied CAGR = (Future Estimate / Current)^(1/Years) - 1
```
Example: ($566B / $416B)^(1/5) - 1 = 6.4% revenue CAGR

### Estimate Dispersion
```
Dispersion = (High - Low) / Average × 100
```
- Narrow dispersion (<10%) = High consensus
- Wide dispersion (>20%) = Significant uncertainty

### Analyst Coverage Quality
- More analysts = more reliable consensus
- Declining coverage = less institutional interest
- <5 analysts = thin coverage, use caution

### Forward P/E Calculation
```
Forward P/E = Current Price / EPS Estimate
```
Use for valuation relative to growth expectations.

### Estimate Revisions (with follow-up)
Track changes over time:
- Upward revisions = positive momentum
- Downward revisions = negative momentum
- Frequency of revisions matters

## Valuation Applications

### DCF Inputs
Use estimates for:
- Revenue projections
- Margin assumptions (with historical data)
- Terminal growth rate guidance

### Relative Valuation
Compare:
- Forward P/E to historical average
- Forward P/E to peers
- PEG ratio (P/E / Growth rate)

### Earnings Surprise Potential
Compare estimates to:
- Management guidance
- Historical beat/miss rate
- Recent operating trends

## Confidence Assessment

### High Confidence Estimates
- Near-term (1-2 years out)
- Many analysts covering
- Narrow dispersion
- Stable business model

### Low Confidence Estimates
- Long-term (5+ years out)
- Few analysts covering
- Wide dispersion
- Rapidly changing industry

## Follow-up Queries

Based on results, suggest deeper analysis:

- "What factors are driving the projected revenue growth from [YEAR1] to [YEAR2]?"
- "How do these estimates compare to [COMPANY]'s historical financial performance?"
- "What are the key risks to achieving the upper end of these revenue estimates?"
- "Retrieve analyst price targets and ratings for [TICKER]"
