---
name: Competitive Analysis
description: This skill should be used when the user asks to "analyze competitors", "map competitive landscape", "Porter's 5 Forces analysis", "competitor comparison", "competitive positioning", "identify competitors", "competitive intelligence", or needs guidance on competitor research methodology, market positioning analysis, or competitive strategy frameworks.
version: 0.1.0
---

# Competitive Analysis

## Overview

Competitive analysis systematically evaluates competitors to understand market positioning, identify gaps, and inform strategic decisions. This skill provides frameworks and methodologies for thorough competitive intelligence gathering.

## When to Use

- Entering a new market or segment
- Evaluating product positioning
- Identifying feature gaps
- Understanding pricing dynamics
- Assessing competitive threats
- Planning differentiation strategy

## Core Frameworks

### Porter's 5 Forces

Analyze industry structure through five competitive forces:

**1. Competitive Rivalry**
- Number and size of competitors
- Industry growth rate
- Product differentiation level
- Exit barriers
- **Indicator**: High rivalry = challenging margins

**2. Supplier Power**
- Supplier concentration
- Switching costs
- Unique inputs
- Forward integration threat
- **Indicator**: High power = cost pressure

**3. Buyer Power**
- Buyer concentration
- Purchase volume
- Switching costs
- Price sensitivity
- **Indicator**: High power = pricing pressure

**4. Threat of Substitution**
- Alternative solutions
- Price-performance trade-off
- Switching costs
- Buyer propensity to substitute
- **Indicator**: High threat = innovation pressure

**5. Threat of New Entry**
- Capital requirements
- Economies of scale
- Brand loyalty
- Regulatory barriers
- **Indicator**: High threat = margin pressure

### Competitor Matrix

Create comparison table with:
| Dimension | Competitor A | Competitor B | Your Position |
|-----------|--------------|--------------|---------------|
| Market Share | % | % | % |
| Pricing | $-$$$ | $-$$$ | $-$$$ |
| Key Features | List | List | List |
| Strengths | List | List | List |
| Weaknesses | List | List | List |
| Trend | INC/DEC/CONST | INC/DEC/CONST | - |

### Positioning Map

Visualize competitive positioning on two key dimensions:
- X-axis: Feature richness (or price)
- Y-axis: Quality/premium positioning (or another differentiator)

Generate as Mermaid quadrant chart showing relative positions.

## Research Process

### Step 1: Identify Competitors
- Direct competitors (same product/market)
- Indirect competitors (different product, same need)
- Potential entrants (adjacent markets)
- Substitutes (alternative solutions)

### Step 2: Gather Intelligence
**Public Sources:**
- Company websites and blogs
- Press releases and news
- Financial reports (if public)
- Job postings (reveals priorities)
- Social media presence
- Customer reviews
- Industry analyst reports

**Search Patterns:**
- "[competitor] pricing"
- "[competitor] vs [alternative]"
- "[competitor] review"
- "[competitor] funding" / "[competitor] revenue"
- "site:[competitor.com] features"

### Step 3: Analyze Findings
- Map to Porter's 5 Forces
- Build competitor matrix
- Create positioning map
- Identify trend directions (INC/DEC/CONST)

### Step 4: Synthesize Insights
- Competitive advantages/disadvantages
- Market gaps and opportunities
- Threat assessment
- Strategic recommendations

## Output Structure

```markdown
## Competitive Landscape Overview
[Summary of competitive environment]

## Porter's 5 Forces Analysis
[Force-by-force assessment with ratings]

## Competitor Profiles
[Detailed profiles of top 3-5 competitors]

## Competitive Matrix
[Comparison table]

## Positioning Map
[Mermaid quadrant chart]

## Key Insights
1. [Insight with implication]
2. [Insight with implication]

## Strategic Recommendations
- [Recommendation based on analysis]
```

## Trend Indicators

Apply three-valued logic to competitor trajectories:
- **INC**: Growing market share, expanding features, positive momentum
- **DEC**: Losing share, reducing investment, negative signals
- **CONST**: Stable position, maintaining but not growing

## Best Practices

- Update analysis quarterly at minimum
- Cross-validate from multiple sources
- Note source reliability and dates
- Distinguish facts from speculation
- Consider regional variations
- Track competitor job postings for strategy hints

## Additional Resources

For detailed frameworks and templates, see:
- `references/porters-five-forces.md` - Complete Porter's framework
- `references/competitive-matrix-template.md` - Matrix templates
- `examples/competitive-analysis-report.md` - Sample report
