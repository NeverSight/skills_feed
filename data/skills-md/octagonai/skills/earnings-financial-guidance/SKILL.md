---
name: earnings-financial-guidance
description: Extract and analyze financial guidance and forward-looking statements from earnings transcripts, including segment guidance, risk factors, and guidance vs. actuals comparison.
---

# Earnings Financial Guidance

Extract and analyze financial guidance and forward-looking statements from earnings transcripts, with segment-level detail, risk factor identification, and comparison to actual results.

## Prerequisites

Ensure Octagon MCP is configured. See [references/mcp-setup.md](references/mcp-setup.md) for installation instructions.

## Workflow

### Step 1: Extract Financial Guidance

Use the Octagon MCP to extract guidance from earnings transcripts:

```
Extract and analyze financial guidance and forward-looking statements from <TICKER>'s latest earnings transcript.
```

### Step 2: Targeted Guidance Analysis

Focus on specific guidance components:

```
# Revenue Guidance
Extract revenue guidance from <TICKER>'s latest earnings call.

# Segment Guidance
Extract segment-level revenue guidance from <TICKER>'s earnings transcript.

# Margin Guidance
Extract gross margin and operating margin guidance from <TICKER>'s earnings call.

# EPS Guidance
Extract earnings per share guidance from <TICKER>'s latest earnings transcript.

# Risk Factors
Extract risk factors and forward-looking statement caveats from <TICKER>'s earnings call.

# Guidance vs. Actuals
Compare prior guidance to actual results in <TICKER>'s latest earnings call.
```

## Expected Output

The skill returns structured guidance analysis including:

| Component | Description |
|-----------|-------------|
| Company Guidance | Explicit forecasts and ranges |
| Segment Detail | Business unit specific outlook |
| Demand Outlook | Customer demand expectations |
| Risk Factors | Caveats and uncertainties |
| Guidance vs. Actuals | Prior guidance compared to results |
| Follow-up Questions | AI-generated questions for deeper analysis |
| Source Citations | Transcript and web search references |

## Example Query

```
Extract and analyze financial guidance and forward-looking statements from MSFT's latest earnings transcript.
```

## Example Response

**Financial Guidance and Forward-Looking Statements from MSFT's Q4 2023 Earnings Transcript**

Microsoft's latest earnings transcript (Q4 2023) outlines the following key guidance and forward-looking statements:

**Guidance Summary**
- **Demand Outlook**: The company expects consistent demand signals across commercial businesses, LinkedIn, gaming, and search advertising. However, results may vary if macroeconomic conditions change
- **Windows OEM Inventory**: Elevated inventory levels in the Windows OEM business from the prior quarter are anticipated to decrease, leading to a widened guidance range for the More Personal Computing segment
- **More Personal Computing Guidance**: The segment's revenue guidance was adjusted to $12.5–$12.9 billion, though actual Q4 2023 revenue reached $13.7 billion (3% year-over-year increase)

**Risk Factors**
- Results could be impacted by changes in the business environment, particularly in the Windows OEM segment

**Additional Context from Web Search**
- Refinitiv estimates projected a 5.7% year-on-year decline for the More Personal Computing segment in Q4 2023, contrasting with the actual 3% growth reported
- Cost of revenue for the segment increased $3.2 billion (5%) year-over-year, driven by growth in cloud and AI investments

**Follow-up Questions**
- What specific factors caused the discrepancy between the guidance range ($12.5–$12.9B) and actual revenue ($13.7B) for More Personal Computing?
- How does Microsoft plan to address potential inventory risks in the Windows OEM business moving forward?
- What portion of the $3.2 billion cost increase in More Personal Computing relates to AI/cloud investments versus other operational expenses?

**Sources**: MSFT_Q42023 [Page 1], Web Search Results

## Guidance Categories

### Revenue Guidance
| Type | Description |
|------|-------------|
| Total Revenue | Company-wide revenue forecast |
| Segment Revenue | Business unit breakdown |
| Geographic | Regional revenue outlook |
| Growth Rate | YoY or QoQ expectations |

### Profitability Guidance
| Type | Description |
|------|-------------|
| Gross Margin | Product/service margin outlook |
| Operating Margin | Operating profitability target |
| Net Margin | Bottom-line expectations |
| EPS | Earnings per share guidance |

### Operational Guidance
| Type | Description |
|------|-------------|
| Operating Expenses | OpEx forecast and drivers |
| CapEx | Capital expenditure plans |
| Tax Rate | Effective tax rate expectation |
| Share Count | Diluted shares outstanding |

## Guidance Analysis Framework

### Guidance Quality Assessment

| Quality | Indicators |
|---------|------------|
| High | Specific ranges, clear assumptions |
| Medium | Directional guidance, qualitative |
| Low | Vague statements, many caveats |

### Range Interpretation

```
Narrow Range (e.g., $12.5B - $12.7B):
- High confidence in forecast
- Limited variability expected
- Typical for mature, predictable businesses

Wide Range (e.g., $12.0B - $13.5B):
- Lower confidence or visibility
- Multiple scenarios possible
- Common in volatile environments
```

### Guidance vs. Consensus

| Scenario | Interpretation |
|----------|----------------|
| Guidance > Consensus | Company more optimistic than Street |
| Guidance = Consensus | Aligned expectations |
| Guidance < Consensus | Street may need to revise down |

## Forward-Looking Statement Analysis

### Common Caveats
| Caveat | Meaning |
|--------|---------|
| "Subject to market conditions" | Macro-dependent |
| "Excluding one-time items" | Adjusted basis |
| "If demand trends continue" | Assumes steady state |
| "Barring unforeseen events" | Base case only |

### Risk Factor Categories
| Category | Examples |
|----------|----------|
| Macroeconomic | Recession, inflation, rates |
| Competitive | Market share, pricing pressure |
| Operational | Supply chain, capacity |
| Regulatory | Policy changes, compliance |
| Foreign Exchange | Currency headwinds/tailwinds |

## Segment-Level Analysis

### Segment Guidance Components

| Component | What to Extract |
|-----------|-----------------|
| Revenue Range | Dollar or growth guidance |
| Margin Outlook | Profitability expectations |
| Key Drivers | Factors influencing performance |
| Risk Factors | Segment-specific headwinds |

### Cross-Segment Comparison

| Segment | Growth | Margin | Risk |
|---------|--------|--------|------|
| Segment A | High | Stable | Low |
| Segment B | Low | Improving | Medium |
| Segment C | Moderate | Declining | High |

## Guidance vs. Actuals Tracking

### Building a Tracking Table

| Metric | Guidance | Actual | Variance | Beat/Miss |
|--------|----------|--------|----------|-----------|
| Revenue | $12.5-12.9B | $13.7B | +$0.8B | Beat |
| EPS | $2.50-2.60 | $2.69 | +$0.09 | Beat |
| Gross Margin | 68-69% | 69.8% | +80bps | Beat |

### Variance Analysis

| Variance | Interpretation |
|----------|----------------|
| Significant beat | Conservative guidance or tailwinds |
| Modest beat | Good execution |
| In-line | Accurate forecasting |
| Modest miss | Minor headwinds |
| Significant miss | Major challenges |

## Use Cases

1. **Model Updates**: Feed guidance into financial models
2. **Consensus Comparison**: Check Street alignment
3. **Risk Assessment**: Identify disclosed uncertainties
4. **Segment Analysis**: Understand business unit outlook
5. **Trend Tracking**: Monitor guidance changes over time
6. **Beat/Miss Prediction**: Anticipate earnings outcomes

## Combining with Other Skills

| Skill | Combined Analysis |
|-------|-------------------|
| analyst-estimates | Guidance vs. consensus |
| income-statement | Validate historical trends |
| earnings-call-analysis | Full context + guidance detail |
| sec-10q-analysis | Cross-reference with filings |
| stock-price-change | Market reaction to guidance |

## Analysis Tips

1. **Track Guidance History**: Build a multi-quarter tracker

2. **Note Assumption Changes**: What's different from last quarter?

3. **Compare to Peers**: How does guidance compare to competitors?

4. **Watch for Revisions**: Mid-quarter updates signal importance

5. **Read the Caveats**: Understand limitations of guidance

6. **Cross-Reference Sources**: Verify with SEC filings

## Interpreting Results

See [references/interpreting-results.md](references/interpreting-results.md) for detailed guidance on analyzing financial guidance.
