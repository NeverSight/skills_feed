---
name: industry-pe-ratios
description: Retrieve industry-specific P/E ratios using Octagon MCP. Use when comparing company valuations to specific industry peers, analyzing sub-sector valuations, and understanding niche market valuations beyond broad sector averages.
---

# Industry P/E Ratios

Retrieve price-to-earnings ratios by specific industry and exchange using the Octagon MCP server.

## Prerequisites

Ensure Octagon MCP is configured in your AI agent (Cursor, Claude Desktop, Windsurf, etc.). See [references/mcp-setup.md](references/mcp-setup.md) for installation instructions.

## Workflow

### 1. Identify Parameters

Determine your query parameters:
- **Date**: Specific date for the data
- **Exchange**: NYSE, NASDAQ, etc.
- **Industry**: Semiconductors, Software, Biotechnology, etc.

### 2. Execute Query via Octagon MCP

Use the `octagon-agent` tool with a natural language prompt:

```
Retrieve the latest industry P/E ratios for <DATE>, filtered by exchange <EXCHANGE> and industry <INDUSTRY>.
```

**MCP Call Format:**

```json
{
  "server": "octagon-mcp",
  "toolName": "octagon-agent",
  "arguments": {
    "prompt": "Retrieve the latest industry P/E ratios for 2025-02-03, filtered by exchange NYSE and industry Semiconductors."
  }
}
```

### 3. Expected Output

The agent returns industry P/E data:

| Metric | Value |
|--------|-------|
| Industry | Semiconductors |
| Exchange | NYSE |
| P/E Ratio | 12.47 |
| Date | 2025-02-03 |
| Example Company | ON Semiconductor (ON) |

**Data Sources**: octagon-companies-agent, octagon-financials-agent, octagon-sec-agent, octagon-web-search-agent

### 4. Interpret Results

See [references/interpreting-results.md](references/interpreting-results.md) for guidance on:
- Comparing company P/E to industry P/E
- Industry vs. sector differences
- Cross-industry analysis
- Peer group valuation

## Example Queries

**Specific Industry and Exchange:**
```
Retrieve the latest industry P/E ratios for 2025-02-03, filtered by exchange NYSE and industry Semiconductors.
```

**NASDAQ Industry:**
```
Get P/E ratios for the Software industry on NASDAQ.
```

**Industry Comparison:**
```
Compare P/E ratios for Semiconductors, Software, and Internet industries.
```

**Historical Trend:**
```
What is the historical P/E trend for the Biotechnology industry?
```

**Peer Analysis:**
```
What are the P/E ratios for companies in the Electric Vehicles industry?
```

## Industry vs. Sector

### Hierarchy

```
Sector (Broad) → Industry (Specific) → Sub-Industry (Niche)
```

### Example

| Level | Example |
|-------|---------|
| Sector | Technology |
| Industry | Semiconductors |
| Sub-Industry | Memory Chips |

### Why Industry Matters

| Comparison | Purpose |
|------------|---------|
| Sector P/E | Broad market context |
| Industry P/E | Peer group benchmark |
| Company P/E | Specific valuation |

## Common Industries

### Technology Sector Industries

| Industry | Typical P/E Range |
|----------|-------------------|
| Semiconductors | 15-35 |
| Software | 25-50 |
| IT Services | 18-30 |
| Hardware | 15-25 |
| Internet | 30-60 |

### Healthcare Sector Industries

| Industry | Typical P/E Range |
|----------|-------------------|
| Biotechnology | 20-40 (or N/A) |
| Pharmaceuticals | 15-25 |
| Medical Devices | 25-40 |
| Healthcare Services | 18-28 |
| Health Insurance | 12-20 |

### Financial Sector Industries

| Industry | Typical P/E Range |
|----------|-------------------|
| Banks | 10-15 |
| Insurance | 10-18 |
| Asset Management | 12-20 |
| REITs | 15-25 |
| Fintech | 25-50 |

### Consumer Sector Industries

| Industry | Typical P/E Range |
|----------|-------------------|
| Retail | 15-25 |
| Restaurants | 20-35 |
| Apparel | 15-25 |
| Automotive | 8-15 |
| E-commerce | 30-60 |

### Industrial Sector Industries

| Industry | Typical P/E Range |
|----------|-------------------|
| Aerospace & Defense | 18-25 |
| Machinery | 15-22 |
| Transportation | 12-20 |
| Construction | 12-18 |
| Electrical Equipment | 18-28 |

## Using Industry P/E for Analysis

### Company Valuation Context

| Comparison | Interpretation |
|------------|----------------|
| Company P/E < Industry P/E | Potential value or concerns |
| Company P/E = Industry P/E | Fairly valued vs. peers |
| Company P/E > Industry P/E | Premium for quality/growth |

### Premium/Discount Calculation

```
Premium/Discount = (Company P/E - Industry P/E) / Industry P/E × 100%
```

### Example

- Company P/E: 18
- Industry P/E (Semiconductors): 12.47
- Premium: (18 - 12.47) / 12.47 = +44.3% (trading at premium)

## Peer Group Analysis

### Defining Peer Groups

| Approach | Method |
|----------|--------|
| Same Industry | Direct competitors |
| Similar Size | Market cap range |
| Similar Growth | Growth rate bands |
| Similar Model | Business model match |

### Peer Comparison Framework

| Metric | Compare |
|--------|---------|
| P/E vs. Industry | Relative value |
| Growth vs. Industry | Growth premium |
| Margins vs. Industry | Quality premium |
| Size vs. Industry | Scale premium |

## Industry Characteristics

### High P/E Industries

| Industry | Why Higher P/E |
|----------|----------------|
| Software | Recurring revenue, scalability |
| Biotech | Pipeline optionality |
| E-commerce | Growth potential |
| Cloud | Secular growth trend |

### Low P/E Industries

| Industry | Why Lower P/E |
|----------|----------------|
| Banks | Cyclical, regulated |
| Insurance | Mature, capital-intensive |
| Utilities | Slow growth, stable |
| Commodities | Cyclical, price-takers |

## Exchange Considerations

### NYSE vs. NASDAQ

| Exchange | Industry Mix |
|----------|--------------|
| NYSE | More diversified, traditional |
| NASDAQ | Tech-heavy, growth-oriented |

### Same Industry, Different Exchange

| Consideration | Impact |
|---------------|--------|
| Different companies | Different P/E averages |
| Liquidity differences | Valuation premiums |
| Listing requirements | Company quality |

## Common Use Cases

### Stock Valuation
```
Is AMD's P/E reasonable compared to the Semiconductor industry?
```

### Industry Selection
```
Which industries have the most attractive valuations?
```

### Peer Benchmarking
```
How does NVDA's valuation compare to semiconductor peers?
```

### M&A Analysis
```
What P/E is typical for Software industry acquisitions?
```

## Analysis Tips

1. **Use industry, not just sector**: More precise comparison.

2. **Consider growth rates**: Higher growth justifies higher P/E.

3. **Check profitability mix**: Loss-making companies distort averages.

4. **Compare apples to apples**: Same business model.

5. **Adjust for size**: Large-caps often command premiums.

6. **Look at sub-industries**: Even more precise comparisons.

## Integration with Other Skills

| Skill | Combined Use |
|-------|--------------|
| sector-pe-ratios | Industry vs. sector context |
| financial-metrics-analysis | Company P/E details |
| income-statement | Earnings driving P/E |
| stock-performance | Price trends within industry |
