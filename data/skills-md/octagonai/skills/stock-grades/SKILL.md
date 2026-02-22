---
name: stock-grades
description: Retrieve the latest stock grades and ratings from top analysts and financial institutions using Octagon MCP. Use when tracking analyst upgrades, downgrades, rating changes, and institutional sentiment over time.
---

# Stock Grades

Retrieve analyst grades, ratings, and rating changes from top financial institutions using the Octagon MCP server.

## Prerequisites

Ensure Octagon MCP is configured in your AI agent (Cursor, Claude Desktop, Windsurf, etc.). See [references/mcp-setup.md](references/mcp-setup.md) for installation instructions.

## Workflow

### 1. Identify the Stock

Determine the ticker symbol for the company you want to analyze (e.g., AAPL, MSFT, GOOGL).

### 2. Execute Query via Octagon MCP

Use the `octagon-agent` tool with a natural language prompt:

```
Get the latest stock grades for the symbol <TICKER> from top analysts and financial institutions.
```

**MCP Call Format:**

```json
{
  "server": "octagon-mcp",
  "toolName": "octagon-agent",
  "arguments": {
    "prompt": "Get the latest stock grades for the symbol AAPL from top analysts and financial institutions."
  }
}
```

### 3. Expected Output

The agent returns analyst rating history including:

- **Rating Actions**: Upgrades, downgrades, maintains
- **Analyst/Institution**: Source of the rating
- **Previous Rating**: Prior grade
- **New Rating**: Current grade
- **Date**: When the rating was issued

**Example**: Maxim Group upgraded from Hold to Buy on 2026-01-30

**Data Sources**: octagon-stock-data-agent

### 4. Interpret Results

See [references/interpreting-results.md](references/interpreting-results.md) for guidance on:
- Understanding rating scales
- Analyzing upgrade/downgrade trends
- Evaluating analyst credibility
- Tracking sentiment changes

## Example Queries

**Basic Query:**
```
Get the latest stock grades for the symbol AAPL from top analysts and financial institutions.
```

**Recent Changes:**
```
What are the most recent analyst rating changes for TSLA?
```

**Upgrade Focus:**
```
Show me recent upgrades for NVDA from major investment banks.
```

**Historical View:**
```
What is the history of analyst ratings for MSFT over the past year?
```

**Specific Institution:**
```
What is Goldman Sachs' current rating on AMZN?
```

## Understanding Rating Scales

### Common Rating Systems

| Rating Level | Common Terms |
|--------------|--------------|
| Strong Buy | Buy, Overweight, Outperform |
| Buy | Accumulate, Add, Positive |
| Hold | Neutral, Market Perform, Equal-Weight |
| Sell | Underweight, Underperform, Reduce |
| Strong Sell | Sell, Avoid |

### Rating Equivalencies

| Bank A | Bank B | Bank C | Meaning |
|--------|--------|--------|---------|
| Overweight | Buy | Outperform | Bullish |
| Equal-Weight | Hold | Market Perform | Neutral |
| Underweight | Sell | Underperform | Bearish |

## Rating Actions

### Action Types

| Action | Description |
|--------|-------------|
| Upgrade | Rating improved (e.g., Hold → Buy) |
| Downgrade | Rating lowered (e.g., Buy → Hold) |
| Maintain | Rating unchanged (reaffirmed) |
| Initiate | New coverage started |
| Reiterate | Rating repeated with emphasis |
| Resume | Coverage restarted |
| Suspend | Coverage temporarily halted |

### Significance Ranking

| Action | Impact |
|--------|--------|
| Upgrade from Sell | Highest positive |
| Upgrade from Hold | Significant positive |
| Initiate at Buy | Positive |
| Maintain at Buy | Stable positive |
| Downgrade to Hold | Negative signal |
| Downgrade to Sell | Highest negative |

## Analyst Credibility

### Factors to Consider

| Factor | Description |
|--------|-------------|
| Track Record | Historical accuracy |
| Institution Tier | Major bank vs. boutique |
| Sector Expertise | Specialization |
| Coverage Length | Experience with stock |
| Independence | Conflicts of interest |

### Institution Tiers

| Tier | Examples |
|------|----------|
| Bulge Bracket | Goldman Sachs, Morgan Stanley, JPMorgan |
| Major Banks | Bank of America, Citi, UBS |
| Boutiques | Wedbush, Piper Sandler, Needham |
| Independent | Morningstar, CFRA |

## Trend Analysis

### Sentiment Indicators

| Pattern | Interpretation |
|---------|----------------|
| Multiple upgrades | Improving sentiment |
| Multiple downgrades | Deteriorating outlook |
| Mixed actions | Uncertainty/debate |
| All maintains | Stable consensus |

### Momentum Signals

| Signal | Meaning |
|--------|---------|
| Upgrade cluster | Catalyst or breakout |
| Downgrade cluster | Concerns emerging |
| Initiation wave | Growing interest |
| Coverage drops | Reduced attention |

## Rating Distribution

### Consensus Rating

| Distribution | Interpretation |
|--------------|----------------|
| Mostly Buy | Strong bullish consensus |
| Mostly Hold | Neutral/wait-and-see |
| Mostly Sell | Bearish consensus |
| Mixed | Divergent views |

### Rating Counts

| Metric | What It Shows |
|--------|---------------|
| Buy % | Bullish proportion |
| Hold % | Neutral proportion |
| Sell % | Bearish proportion |
| Total Analysts | Coverage level |

## Timing Considerations

### When Ratings Change

| Catalyst | Typical Timing |
|----------|----------------|
| Earnings | Day of or day after |
| Guidance | Within 24-48 hours |
| Product News | Same day |
| Macro Events | As needed |
| Sector Rotation | Periodic |

### Staleness

| Age | Reliability |
|-----|-------------|
| <1 month | Current view |
| 1-3 months | Reasonably current |
| 3-6 months | May be outdated |
| >6 months | Likely stale |

## Common Use Cases

### Sentiment Check
```
What is the current analyst sentiment on AAPL?
```

### Change Monitoring
```
Have any analysts upgraded or downgraded TSLA recently?
```

### Catalyst Research
```
Why did analysts upgrade NVDA last week?
```

### Consensus View
```
What percentage of analysts rate MSFT as a buy?
```

### Historical Tracking
```
How has analyst sentiment on META changed over the past year?
```

## Analysis Tips

1. **Weight by institution**: Major banks carry more weight.

2. **Track changes, not just ratings**: Upgrades/downgrades signal shifts.

3. **Consider timing**: Post-earnings ratings are most current.

4. **Look for clusters**: Multiple changes = significant.

5. **Check track record**: Some analysts are more accurate.

6. **Combine with targets**: Rating + price target = complete view.

## Integration with Other Skills

| Skill | Combined Use |
|-------|--------------|
| price-target-consensus | Ratings + price targets |
| analyst-estimates | Ratings + earnings expectations |
| stock-quote | Rating changes + price reaction |
| stock-performance | Historical ratings vs. performance |
