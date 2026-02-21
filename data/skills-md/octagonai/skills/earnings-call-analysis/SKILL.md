---
name: earnings-call-analysis
description: Analyze earnings call transcripts to extract forward-looking guidance, strategic focus areas, supply chain insights, and generate follow-up questions for deeper analysis.
---

# Earnings Call Analysis

Analyze earnings call transcripts to extract comprehensive forward-looking guidance, strategic initiatives, operational challenges, and automatically generate follow-up questions for deeper research.

## Prerequisites

Ensure Octagon MCP is configured. See [references/mcp-setup.md](references/mcp-setup.md) for installation instructions.

## Workflow

### Step 1: Analyze Earnings Call Transcript

Use the Octagon MCP to analyze earnings call transcripts:

```
Analyze <TICKER>'s latest earnings call transcript and extract key insights about future guidance.
```

### Step 2: Targeted Analysis

Focus on specific aspects of the earnings call:

```
# Full Guidance Analysis
Analyze <TICKER>'s latest earnings call and extract all forward-looking guidance.

# Strategic Initiatives
What strategic initiatives did management highlight in <TICKER>'s earnings call?

# Operational Challenges
Summarize operational challenges and headwinds mentioned in <TICKER>'s earnings call.

# Investment Priorities
What are <TICKER>'s investment priorities based on the latest earnings call?

# Competitive Commentary
Extract competitive positioning comments from <TICKER>'s earnings call.
```

## Expected Output

The skill returns structured analysis including:

| Category | Information |
|----------|-------------|
| Revenue Growth | Expected growth rate and drivers |
| Segment Guidance | Business unit specific outlook |
| Margin Outlook | Gross margin and operating margin projections |
| Operating Expenses | OpEx guidance with investment priorities |
| Tax Rate | Effective tax rate forecast |
| Strategic Focus | Key initiatives and priorities |
| Risk Factors | Supply constraints, macro concerns |
| Follow-up Questions | AI-generated questions for deeper analysis |
| Source Citations | Specific transcript page references |

## Example Query

```
Analyze AAPL's latest earnings call transcript and extract key insights about future guidance.
```

## Example Response

Apple Inc. (AAPL) outlined the following forward-looking guidance during its Q1 2026 earnings call:

**Financial Guidance**
- **Revenue Growth**: Expects total revenue to increase by 13% to 16% year-over-year in the upcoming quarter, despite constrained iPhone supply
- **Services Revenue**: Anticipates growth at a similar rate to the previous quarter (Q4 2025)
- **Gross Margin**: Projects a margin range of 48.00% to 49.00%
- **Operating Expenses**: Estimates expenses between $18.4 billion and $18.7 billion, driven by higher R&D investments
- **Tax Rate**: Forecasts a tax rate of approximately 17.50%

**Strategic Focus**
- Highlighted growth opportunities in India and emphasized collaboration with Google in AI development

**Risk Factors**
- **Supply Constraints**: Remains cautious about advanced node capacity limitations, which could impact demand fulfillment

**Follow-up Questions**
- What was the exact growth rate for services revenue in Q4 2025?
- How much of the R&D investment is allocated to AI initiatives?
- What specific supply chain bottlenecks were identified in the call transcript?

**Sources**: AAPL_Q12026, Pages: 1, 4, 6

## Key Metrics to Extract

### Quantitative Guidance
| Metric | Description |
|--------|-------------|
| Revenue Growth | YoY or QoQ growth expectations |
| Gross Margin | Projected margin range |
| Operating Expenses | OpEx forecast with drivers |
| EPS | Earnings per share guidance |
| Tax Rate | Effective tax rate expectation |
| CapEx | Capital expenditure plans |
| Free Cash Flow | FCF expectations |

### Qualitative Insights
| Insight | Description |
|---------|-------------|
| Strategic Priorities | Key focus areas for management |
| Investment Areas | R&D, geographic expansion, M&A |
| Competitive Position | Market share, differentiation |
| Risk Factors | Headwinds, constraints, uncertainties |
| Geographic Trends | Regional performance outlook |

## Analysis Framework

### Guidance Interpretation

| Component | What to Analyze |
|-----------|-----------------|
| Range Width | Narrow = high confidence, Wide = uncertainty |
| YoY Comparison | Acceleration or deceleration |
| Beat/Miss Context | Factors driving performance |
| Segment Mix | Which units driving growth |

### Strategic Signal Analysis

| Signal Type | Examples |
|-------------|----------|
| Growth Drivers | New markets, products, partnerships |
| Investment Focus | R&D areas, geographic expansion |
| Competitive Response | Pricing, innovation, M&A |
| Risk Mitigation | Supply chain diversification, hedging |

### Follow-up Question Categories

The AI generates follow-up questions across these areas:

| Category | Purpose |
|----------|---------|
| Clarification | Specific numbers or metrics not disclosed |
| Deep Dive | Further detail on strategic initiatives |
| Risk Exploration | Understanding of headwinds and mitigations |
| Competitive | Comparison to peers or market |
| Historical | Comparison to prior guidance or performance |

## Use Cases

1. **Earnings Season Coverage**: Quickly analyze multiple earnings calls
2. **Due Diligence**: Extract guidance for investment decisions
3. **Competitive Analysis**: Compare guidance across peers
4. **Model Updates**: Feed guidance into financial models
5. **Research Reports**: Source material for analyst reports
6. **Risk Assessment**: Identify emerging risks and challenges

## Combining with Other Skills

| Skill | Combined Analysis |
|-------|-------------------|
| analyst-estimates | Compare guidance to consensus |
| income-statement | Validate trends vs. guidance |
| stock-price-change | Analyze market reaction to guidance |
| sec-10q-analysis | Cross-reference with official filings |
| price-target-consensus | Check if targets reflect new guidance |

## Source Citations

The skill provides specific source citations:

| Citation Format | Description |
|-----------------|-------------|
| TICKER_Q#YEAR | Transcript identifier |
| Page: # | Specific page in transcript |
| Multiple sources | Cross-referenced insights |

## Analysis Tips

1. **Track Guidance Changes**: Compare current guidance to prior quarter

2. **Evaluate Credibility**: Consider management's historical accuracy

3. **Use Follow-up Questions**: Dig deeper on AI-generated questions

4. **Cross-Reference**: Verify guidance against 10-Q filings

5. **Peer Comparison**: Compare guidance to industry peers

6. **Watch for Hedging**: Note cautious language or wide ranges

## Interpreting Results

See [references/interpreting-results.md](references/interpreting-results.md) for detailed guidance on analyzing earnings call transcripts.
