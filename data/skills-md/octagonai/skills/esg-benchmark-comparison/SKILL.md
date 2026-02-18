---
name: esg-benchmark-comparison
description: Retrieve ESG benchmark comparison metrics by sector using Octagon MCP. Use when comparing ESG performance across industries, analyzing sector-level sustainability benchmarks, identifying ESG leaders and laggards by industry, or referencing frameworks like MSCI, S&P Global, CDP, and CSRD.
---

# ESG Benchmark Comparison

Retrieve and analyze ESG benchmark comparison metrics across sectors and industries using the Octagon MCP server.

## Prerequisites

Ensure Octagon MCP is configured in your AI agent (Cursor, Claude Desktop, Windsurf, etc.). See [references/mcp-setup.md](references/mcp-setup.md) for installation instructions.

## Workflow

### 1. Identify Analysis Parameters

Determine the following before querying:
- **Fiscal Year**: Target year for benchmark data (e.g., 2024, 2023)
- **Sector** (optional): Specific sector to focus on (e.g., Technology, Energy, Healthcare)
- **Framework** (optional): ESG framework reference (MSCI, S&P Global, CDP, CSRD)

### 2. Execute Query via Octagon MCP

Use the `octagon-agent` tool with a natural language prompt:

```
Retrieve ESG benchmark comparison metrics by sector for the fiscal year <YEAR>.
```

**MCP Call Format:**

```json
{
  "server": "octagon-mcp",
  "toolName": "octagon-agent",
  "arguments": {
    "prompt": "Retrieve ESG benchmark comparison metrics by sector for the fiscal year 2024."
  }
}
```

### 3. Expected Output

The agent returns sector-level ESG benchmark data including:

**Sector-Level Metrics:**
- Industry ESG averages and ranges
- Top performers by sector
- Benchmark sources (MSCI, S&P, CDP)
- Regional variations (EU, US, APAC)

**Example Response:**

| Sector | Avg ESG Score | Top Quartile | Bottom Quartile | Key Metrics |
|--------|---------------|--------------|-----------------|-------------|
| Technology | 72.5 | 85+ | <55 | Carbon, Data Privacy |
| Energy | 48.3 | 65+ | <35 | Emissions, Transition |
| Healthcare | 68.2 | 80+ | <50 | Access, Governance |
| Financials | 65.8 | 78+ | <48 | Ethics, Climate Risk |

**Data Sources**: octagon-companies-agent, octagon-web-search-agent

### 4. Interpret Results

See [references/interpreting-results.md](references/interpreting-results.md) for guidance on:
- Understanding sector benchmark ranges
- Identifying industry leaders and laggards
- Comparing against ESG frameworks
- Regional benchmark variations

## Example Queries

**Standard Sector Benchmarks:**
```
Retrieve ESG benchmark comparison metrics by sector for the fiscal year 2024.
```

**Technology Sector Focus:**
```
Retrieve ESG benchmark comparison metrics for the Technology sector for FY2024, including MSCI and S&P benchmarks.
```

**Energy Transition Benchmarks:**
```
Retrieve ESG benchmark comparison for Energy sector companies with focus on climate transition metrics for 2024.
```

**Regional Comparison:**
```
Retrieve ESG benchmark comparison metrics by sector for EU companies in fiscal year 2024.
```

**Framework-Specific:**
```
Retrieve CDP climate benchmark scores by sector for 2024.
```

## Key Benchmark Sources

| Source | Coverage | Focus Areas |
|--------|----------|-------------|
| MSCI ESG | Global | Overall ESG, Industry Materiality |
| S&P Global | Global | ESG Scores, Sustainability |
| CDP | Global | Climate, Water, Forests |
| Sustainalytics | Global | ESG Risk Ratings |
| ISS ESG | Global | Governance, Climate |
| CSRD | EU | Comprehensive Disclosure |

## Sector Benchmark Ranges

Typical ESG score ranges by sector (0-100 scale):

| Sector | Low | Average | High | Key Materiality |
|--------|-----|---------|------|-----------------|
| Technology | 45 | 70 | 90 | Data privacy, supply chain |
| Financials | 40 | 65 | 85 | Governance, climate risk |
| Healthcare | 45 | 68 | 88 | Access, ethics, governance |
| Consumer Staples | 50 | 72 | 90 | Supply chain, packaging |
| Energy | 25 | 48 | 75 | Emissions, transition |
| Utilities | 35 | 55 | 80 | Renewable mix, emissions |
| Industrials | 35 | 58 | 82 | Safety, emissions |
| Materials | 30 | 52 | 78 | Pollution, resources |

## Analysis Tips

1. **Sector context matters**: A score of 60 may be excellent in Energy but average in Technology.

2. **Materiality focus**: Each sector has different material ESG issues—compare on relevant metrics.

3. **Benchmark evolution**: ESG benchmarks shift over time as standards tighten; use same-year comparisons.

4. **Regional differences**: EU companies often score higher due to stricter disclosure requirements.

5. **Multiple frameworks**: Cross-reference MSCI, S&P, and CDP for robust benchmarking.

## Use Cases

- **Sector allocation**: Identify ESG-leading sectors for portfolio tilts
- **Peer benchmarking**: Compare company ESG vs sector average
- **Gap analysis**: Identify areas where companies underperform sector benchmarks
- **Investment screening**: Set sector-relative ESG thresholds
- **Regulatory compliance**: Align with CSRD and other framework requirements
