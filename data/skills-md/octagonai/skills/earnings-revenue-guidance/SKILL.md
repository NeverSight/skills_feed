---
name: earnings-revenue-guidance
description: Extract specific revenue guidance and growth projections from earnings call transcripts, including segment breakdown, constant currency adjustments, and M&A contributions.
---

# Earnings Revenue Guidance

Extract specific revenue guidance and growth projections from earnings call transcripts with detailed breakdowns by segment, currency impact, and M&A contributions.

## Prerequisites

Ensure Octagon MCP is configured. See [references/mcp-setup.md](references/mcp-setup.md) for installation instructions.

## Workflow

### Step 1: Extract Revenue Guidance

Use the Octagon MCP to extract revenue guidance:

```
Extract specific revenue guidance and growth projections from <TICKER>'s latest earnings call transcript.
```

### Step 2: Targeted Revenue Analysis

Focus on specific aspects of revenue guidance:

```
# Total Revenue
Extract total revenue guidance from <TICKER>'s latest earnings call.

# Segment Revenue
Extract segment-level revenue guidance from <TICKER>'s earnings transcript.

# Organic vs. M&A
Separate organic revenue guidance from M&A contribution in <TICKER>'s earnings call.

# Currency Impact
What is the FX impact on <TICKER>'s revenue guidance?

# Subscription Revenue
Extract recurring revenue guidance from <TICKER>'s earnings call.

# Growth Rates
Extract revenue growth rate guidance from <TICKER>'s earnings transcript.
```

## Expected Output

The skill returns structured revenue guidance including:

| Component | Description |
|-----------|-------------|
| Revenue Range | Dollar guidance (low-high) |
| Growth Rate | Nominal YoY growth percentage |
| Constant Currency | FX-adjusted growth rate |
| Segment Breakdown | Revenue by business unit |
| M&A Contribution | Acquisition impact on growth |
| Source Citations | Transcript page references |

## Example Query

```
Extract specific revenue guidance and growth projections from CRM's latest earnings call transcript.
```

## Example Response

Salesforce (CRM) provided the following revenue guidance and growth projections in its Q3 2026 earnings call transcript:

**Revenue Guidance**

| Metric | Range | Growth Rate (Nominal) | Growth Rate (Constant Currency) |
|--------|-------|----------------------|--------------------------------|
| Total Revenue | $41.15B - $41.25B | 9.00% | 8.00% |
| Total Revenue (with Informatica) | $41.545B - $41.55B | 9.00% - 10.00% | 9.00% |

**Subscription & Support Revenue**
- Anticipated growth: Slightly under 10.00% year-over-year in constant currency
- Informatica contribution: +0.80 percentage points to growth

**Source**: CRM_Q32026, Page: 6

## Revenue Guidance Components

### Total Revenue
| Component | Description |
|-----------|-------------|
| Range Low | Conservative estimate |
| Range High | Optimistic estimate |
| Midpoint | Implied expectation |
| Growth Rate | YoY percentage change |

### Segment Revenue
| Segment Type | Examples |
|--------------|----------|
| Product Lines | Cloud, Hardware, Services |
| Business Units | Enterprise, SMB, Consumer |
| Revenue Type | Subscription, Perpetual, Services |
| Geography | Americas, EMEA, APAC |

### Growth Rate Types
| Type | Description |
|------|-------------|
| Reported (Nominal) | As-reported in local currency |
| Constant Currency | FX-adjusted growth |
| Organic | Excluding M&A |
| Pro Forma | As if M&A included in prior period |

## Currency Impact Analysis

### Understanding FX Effects

| FX Scenario | Revenue Impact | Growth Rate |
|-------------|----------------|-------------|
| USD Strong | Lower reported | Reported < CC |
| USD Weak | Higher reported | Reported > CC |
| Neutral | No impact | Reported = CC |

### Calculating Currency Impact

```
Example:
- Reported Growth: 9.00%
- Constant Currency Growth: 8.00%
- FX Tailwind: 9.00% - 8.00% = +1.00pp

Interpretation: Currency added 1 percentage point to reported growth
```

## M&A Contribution Analysis

### Separating Organic from Inorganic

| Component | Calculation |
|-----------|-------------|
| Total Growth | Reported YoY change |
| M&A Contribution | Acquired revenue / prior base |
| Organic Growth | Total Growth - M&A Contribution |

### Example Breakdown

```
Total Growth: 10.00%
M&A Contribution: +0.80pp (Informatica)
Organic Growth: 10.00% - 0.80% = 9.20%

Key Insight: Underlying business growing at 9.2%
```

## Segment Guidance Framework

### Segment Revenue Table

| Segment | Guidance | Growth | Mix |
|---------|----------|--------|-----|
| Cloud | $25B | +15% | 60% |
| Services | $10B | +5% | 25% |
| Other | $6B | +2% | 15% |
| **Total** | **$41B** | **+10%** | **100%** |

### Mix Shift Analysis

| Trend | Implication |
|-------|-------------|
| High-growth segment gaining share | Positive for overall growth |
| High-margin segment gaining share | Positive for profitability |
| Declining segment shrinking | Healthy portfolio management |
| All segments growing | Broad-based strength |

## Guidance Range Analysis

### Range Width Interpretation

| Range Width | Confidence Level |
|-------------|------------------|
| < 1% of midpoint | Very high confidence |
| 1-2% of midpoint | High confidence |
| 2-3% of midpoint | Moderate confidence |
| > 3% of midpoint | Low confidence, high variability |

### Midpoint Calculation

```
Example:
Range: $41.15B - $41.25B
Midpoint: ($41.15B + $41.25B) / 2 = $41.20B
Range Width: $41.25B - $41.15B = $0.10B
% of Midpoint: $0.10B / $41.20B = 0.24%

Interpretation: Very tight range, high confidence
```

## Tracking Revenue Guidance

### Quarter-over-Quarter Changes

| Period | Guidance | Change | Signal |
|--------|----------|--------|--------|
| Q1 FY26 | $40.5B | Initial | Baseline |
| Q2 FY26 | $40.8B | +$0.3B | Raised |
| Q3 FY26 | $41.2B | +$0.4B | Raised |
| Full Year | $165B | | Annual |

### Guidance Revision Analysis

| Revision | Interpretation |
|----------|----------------|
| Raised | Positive momentum |
| Maintained | On track |
| Narrowed | Increased visibility |
| Lowered | Challenges |
| Widened | Decreased visibility |

## Use Cases

1. **Model Updates**: Feed revenue guidance into financial models
2. **Consensus Comparison**: Compare to Street estimates
3. **Organic Growth Tracking**: Separate core growth from M&A
4. **FX Impact Analysis**: Understand currency effects
5. **Segment Trends**: Track business unit performance
6. **Beat/Miss Prediction**: Anticipate earnings outcomes

## Combining with Other Skills

| Skill | Combined Analysis |
|-------|-------------------|
| analyst-estimates | Guidance vs. consensus |
| income-statement | Historical revenue trends |
| earnings-financial-guidance | Full guidance context |
| revenue-product-segmentation | Segment validation |
| stock-price-change | Guidance impact on price |

## Analysis Tips

1. **Track Organic Growth**: Strip out M&A and FX for true trends

2. **Compare to Consensus**: Is guidance above or below Street?

3. **Watch Range Width**: Narrow = confident, wide = uncertain

4. **Note Revisions**: Raising or lowering tells you direction

5. **Segment Focus**: Which segments driving growth?

6. **Historical Accuracy**: Does management typically beat guidance?

## Interpreting Results

See [references/interpreting-results.md](references/interpreting-results.md) for detailed guidance on analyzing revenue guidance.
