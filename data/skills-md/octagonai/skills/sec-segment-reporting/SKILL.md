---
name: sec-segment-reporting
description: Analyze business segment performance and reporting from SEC filings using Octagon MCP. Use when researching segment revenue, operating income, margins, geographic breakdown, and segment restructuring from 10-K and 10-Q filings.
---

# SEC Segment Reporting

Analyze business segment performance and reporting from SEC filings for public companies using the Octagon MCP server.

## Prerequisites

Ensure Octagon MCP is configured in your AI agent (Cursor, Claude Desktop, Windsurf, etc.). See [references/mcp-setup.md](references/mcp-setup.md) for installation instructions.

## Workflow

### 1. Identify Analysis Parameters

Determine the following before querying:
- **Ticker**: Stock symbol (e.g., AAPL, MSFT, GOOGL)
- **Filing Type** (optional): 10-K (annual) or 10-Q (quarterly)
- **Focus Area** (optional): Revenue, profitability, geographic, trends

### 2. Execute Query via Octagon MCP

Use the `octagon-agent` tool with a natural language prompt:

```
Analyze business segment performance and reporting from <TICKER>'s latest quarterly filing.
```

**MCP Call Format:**

```json
{
  "server": "octagon-mcp",
  "toolName": "octagon-agent",
  "arguments": {
    "prompt": "Analyze business segment performance and reporting from IBM's latest quarterly filing."
  }
}
```

### 3. Expected Output

The agent returns structured segment analysis including:

| Segment | Revenue | YoY Growth | Operating Income | Margin |
|---------|---------|------------|------------------|--------|
| Software | $7,209M | 10.5% | $2,374M | 32.9% |
| Consulting | $5,324M | 3.3% | $686M | 12.9% |
| Infrastructure | $3,559M | 17.0% | $644M | 18.1% |
| Financing | $200M | 10.4% | $123M | 61.6% |

**Key Trends:**
- Infrastructure fastest-growing at 17.0%
- Software maintains highest margin at 32.9%
- Consulting stable revenue driver

**Data Sources**: octagon-financials-agent, octagon-sec-agent

### 4. Interpret Results

See [references/interpreting-results.md](references/interpreting-results.md) for guidance on:
- Understanding segment composition
- Evaluating segment profitability
- Tracking segment restructuring
- Analyzing geographic segments

## Example Queries

**Full Segment Analysis:**
```
Analyze business segment performance and reporting from IBM's latest quarterly filing.
```

**Segment Profitability:**
```
Compare operating margins across MSFT's business segments in the latest 10-K.
```

**Geographic Segments:**
```
Analyze AAPL's revenue breakdown by geographic region from the latest 10-K.
```

**Segment Growth Trends:**
```
Track revenue growth trends by segment for GOOGL over the last 4 quarters.
```

**Segment Restructuring:**
```
Has AMZN restructured its segment reporting in recent filings and how?
```

**Inter-Segment Comparison:**
```
Compare segment performance between META and GOOGL in their latest annual filings.
```

## Segment Reporting Framework

### Operating Segments (ASC 280)

| Element | Description |
|---------|-------------|
| Revenue | Segment sales, external and intersegment |
| Operating Income | Segment profit/loss |
| Assets | Segment assets allocated |
| CapEx | Capital expenditures by segment |
| Depreciation | D&A by segment |

### Geographic Segments

| Element | Description |
|---------|-------------|
| Revenue by Region | Sales by geography |
| Long-Lived Assets | Property, equipment by location |
| Country Disclosure | Material country breakouts |

### Common Segment Structures

| Industry | Typical Segments |
|----------|------------------|
| Technology | Products, Services, Cloud, Licensing |
| Retail | Stores, Online, Wholesale |
| Financial | Banking, Wealth, Insurance |
| Healthcare | Pharmaceuticals, Devices, Services |
| Industrial | Products, Services, Financing |

## Key Metrics by Segment

### Revenue Metrics

| Metric | Calculation | What It Shows |
|--------|-------------|---------------|
| Segment Revenue | Reported amount | Size of segment |
| Revenue Mix | Segment / Total | Business composition |
| Growth Rate | (Current - Prior) / Prior | Momentum |
| Intersegment | Internal sales | Vertical integration |

### Profitability Metrics

| Metric | Calculation | What It Shows |
|--------|-------------|---------------|
| Operating Income | Segment profit | Profitability |
| Operating Margin | Op Income / Revenue | Efficiency |
| Contribution | Segment / Total Op Income | Profit mix |
| Margin Trend | Current vs. Prior | Direction |

### Asset Metrics

| Metric | Calculation | What It Shows |
|--------|-------------|---------------|
| Segment Assets | Reported amount | Capital deployed |
| Asset Turnover | Revenue / Assets | Efficiency |
| CapEx Intensity | CapEx / Revenue | Investment level |
| ROA | Op Income / Assets | Return on assets |

## Segment Performance Analysis

### Growth Assessment

| Growth Rate | Assessment |
|-------------|------------|
| >20% | High growth, investment phase |
| 10-20% | Solid growth |
| 5-10% | Moderate growth |
| 0-5% | Mature, stable |
| Negative | Declining, concern |

### Margin Assessment

| Margin Level | Assessment |
|--------------|------------|
| >30% | High margin, premium |
| 20-30% | Strong margin |
| 10-20% | Moderate margin |
| 5-10% | Low margin |
| <5% | Thin margin, scale needed |

### Segment Health Matrix

| | High Margin | Low Margin |
|---|-------------|------------|
| **High Growth** | Star segment | Investment needed |
| **Low Growth** | Cash cow | Turnaround/exit |

## Geographic Segment Analysis

### Revenue Distribution

| Region | Typical Disclosure |
|--------|-------------------|
| Americas | US, Canada, Latin America |
| EMEA | Europe, Middle East, Africa |
| APAC | Asia Pacific, Japan |
| Other | Emerging markets |

### Geographic Considerations

| Factor | What to Assess |
|--------|----------------|
| Concentration | Over-reliance on one region |
| Growth Rates | Regional momentum |
| Currency | FX exposure |
| Regulatory | Region-specific risks |

## Segment Restructuring

### Types of Changes

| Change | What It Means |
|--------|---------------|
| Segment Added | New business, acquisition |
| Segment Removed | Divestiture, consolidation |
| Segments Combined | Simplified reporting |
| Segments Split | More granular disclosure |
| Renamed | Strategic repositioning |

### Restructuring Red Flags

1. **Frequent changes** - May obscure performance
2. **Combining declining segments** - Hiding weakness
3. **Timing around issues** - Coincides with problems
4. **Reduced disclosure** - Less transparency
5. **Changed metrics** - Different KPIs reported

## Tracking Segment Trends

### Quarterly Progression

| Metric | Q1 | Q2 | Q3 | Q4 | Trend |
|--------|----|----|----|----|-------|
| Revenue | | | | | |
| Growth | | | | | |
| Margin | | | | | |

### Year-over-Year Comparison

| Segment | Prior Year | Current | Change |
|---------|------------|---------|--------|
| Segment A | $X | $Y | Z% |
| Segment B | $X | $Y | Z% |

## Inter-Company Comparison

### Peer Benchmarking

Compare across competitors:
- Segment mix composition
- Relative growth rates
- Margin comparison
- Asset efficiency

### Apples-to-Apples Considerations

| Factor | Adjustment Needed |
|--------|-------------------|
| Segment Definition | May differ by company |
| Cost Allocation | Different methodologies |
| Transfer Pricing | Intersegment policies |
| Consolidation | Elimination methods |

## Analysis Tips

1. **Read segment footnotes**: Detailed policies and changes disclosed.

2. **Track restructuring**: Segment changes may signal strategy shifts.

3. **Calculate margins yourself**: Verify reported figures.

4. **Watch mix shifts**: Revenue composition reveals priorities.

5. **Consider seasonality**: Quarterly patterns affect segments differently.

6. **Compare to guidance**: Management targets by segment.

## Use Cases

- **Investment analysis**: Understand business composition
- **Valuation**: Sum-of-parts analysis
- **Due diligence**: Segment-level performance
- **Competitive intelligence**: Compare segment positions
- **Strategic analysis**: Identify growth drivers
