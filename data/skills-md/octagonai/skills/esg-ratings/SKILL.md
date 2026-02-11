---
name: esg-ratings
description: Retrieve ESG ratings and scores using Octagon MCP. Use when analyzing Environmental, Social, and Governance ratings, MSCI ESG ratings, Sustainalytics risk ratings, industry ESG rankings, and sustainability metrics for any public company.
---

# ESG Ratings

Retrieve and analyze Environmental, Social, and Governance (ESG) ratings and scores for public companies using the Octagon MCP server.

## Prerequisites

Ensure Octagon MCP is configured in your AI agent (Cursor, Claude Desktop, Windsurf, etc.). See [references/mcp-setup.md](references/mcp-setup.md) for installation instructions.

## Workflow

### 1. Identify Analysis Parameters

Determine the following before querying:
- **Ticker**: Stock symbol (e.g., MSFT, AAPL, TSLA)
- **Specific metrics** (optional): ESG score, environmental score, social score, governance score, industry rank

### 2. Execute Query via Octagon MCP

Use the `octagon-agent` tool with a natural language prompt:

```
Retrieve ESG ratings and scores, including risk rating and industry rank, for <TICKER>.
```

**MCP Call Format:**

```json
{
  "server": "octagon-mcp",
  "toolName": "octagon-agent",
  "arguments": {
    "prompt": "Retrieve ESG ratings and scores, including risk rating and industry rank, for MSFT."
  }
}
```

### 3. Expected Output

The agent returns comprehensive ESG data including:

**Key ESG Metrics:**
- MSCI ESG Rating (AAA to CCC scale)
- Sustainalytics ESG Risk Rating
- Composite ESG Score
- Environmental Score
- Social Score
- Governance Score
- S&P Global ESG Score
- Industry rank and categorization

**Example Response:**

| Metric | Value |
|--------|-------|
| MSCI ESG Rating | AAA |
| ESG Score | 65.19 |
| Environmental | 74.57 |
| Social | 58.08 |
| Governance | 62.93 |
| Industry | Enterprise and Infrastructure Software |

**Data Sources**: octagon-companies-agent, octagon-financials-agent, octagon-web-search-agent

### 4. Interpret Results

See [references/interpreting-results.md](references/interpreting-results.md) for guidance on:
- Understanding MSCI rating scale
- Interpreting Sustainalytics risk ratings
- Comparing E, S, and G component scores
- Industry ranking context

## Example Queries

**Standard ESG Analysis:**
```
Retrieve ESG ratings and scores, including risk rating and industry rank, for MSFT.
```

**Environmental Focus:**
```
Retrieve ESG ratings with focus on environmental scores and carbon emissions for AAPL.
```

**Comparative Analysis:**
```
Retrieve ESG ratings and scores for TSLA and compare to automotive industry peers.
```

**Governance Deep Dive:**
```
Retrieve ESG ratings with detailed governance scores and board diversity metrics for JPM.
```

## Key Metrics Explained

| Metric | Definition | Scale |
|--------|------------|-------|
| MSCI ESG Rating | Overall ESG assessment by MSCI | AAA (best) to CCC (worst) |
| Sustainalytics Risk Rating | Unmanaged ESG risk level | 0-100 (lower = less risk) |
| ESG Score | Composite sustainability score | 0-100 (higher = better) |
| Environmental Score | Climate, pollution, resource use | 0-100 |
| Social Score | Labor, community, human rights | 0-100 |
| Governance Score | Board, ethics, transparency | 0-100 |
| Industry Rank | Position vs sector peers | Percentile or rank |

## MSCI Rating Scale

| Rating | Category | Meaning |
|--------|----------|---------|
| AAA, AA | Leader | Best-in-class ESG performance |
| A, BBB, BB | Average | Mixed or average ESG performance |
| B, CCC | Laggard | Below-average ESG, higher risk |

## Analysis Tips

1. **Component imbalance**: A company may score high on Environmental but low on Governance—assess each dimension.

2. **Industry context**: ESG scores vary significantly by sector. Compare to industry peers, not cross-sector.

3. **Trend over time**: Request historical ESG data to see if ratings are improving or declining.

4. **Materiality**: Different ESG factors matter more in different industries (e.g., Environmental for energy, Social for retail).

5. **Multiple sources**: MSCI, Sustainalytics, and S&P may give different ratings—consider the consensus view.

## Use Cases

- **ESG screening**: Filter investments based on minimum ESG thresholds
- **Risk assessment**: Identify companies with high unmanaged ESG risks
- **Portfolio alignment**: Ensure holdings meet sustainability mandates
- **Engagement targeting**: Identify areas for shareholder engagement
- **Regulatory compliance**: Meet ESG disclosure requirements
