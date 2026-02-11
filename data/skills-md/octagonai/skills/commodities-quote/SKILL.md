---
name: commodities-quote
description: Retrieve real-time commodity price quotes using Octagon MCP. Use when checking current commodity prices, analyzing day ranges, comparing to moving averages, and tracking precious metals, energy, and agricultural commodity prices.
---

# Commodities Quote

Retrieve real-time price quotes for commodities including precious metals, energy, and agricultural products using the Octagon MCP server.

## Prerequisites

Ensure Octagon MCP is configured in your AI agent (Cursor, Claude Desktop, Windsurf, etc.). See [references/mcp-setup.md](references/mcp-setup.md) for installation instructions.

## Workflow

### 1. Identify the Commodity

Determine the commodity symbol you want to quote:
- **GCUSD**: Gold
- **SIUSD**: Silver
- **CLUSD**: Crude Oil
- **NGUSD**: Natural Gas
- etc.

### 2. Execute Query via Octagon MCP

Use the `octagon-agent` tool with a natural language prompt:

```
Retrieve the real-time price quote for <SYMBOL>.
```

**MCP Call Format:**

```json
{
  "server": "octagon-mcp",
  "toolName": "octagon-agent",
  "arguments": {
    "prompt": "Retrieve the real-time price quote for GCUSD."
  }
}
```

### 3. Expected Output

The agent returns comprehensive quote data:

| Metric | Value |
|--------|-------|
| Current Price | $4,864.20 |
| Change | +$211.60 (+4.55%) |
| Day Low | $4,690.20 |
| Day High | $4,871.00 |
| 50-Day Avg | $4,559.45 |
| 200-Day Avg | $3,888.90 |
| Year Low | $2,837.40 |
| Year High | $5,626.80 |
| Trading Volume | 18,846 |
| Previous Close | $4,652.60 |

**Data Sources**: octagon-stock-data-agent

### 4. Interpret Results

See [references/interpreting-results.md](references/interpreting-results.md) for guidance on:
- Analyzing price movements
- Understanding range positions
- Using moving averages
- Evaluating volume

## Example Queries

**Gold Quote:**
```
Retrieve the real-time price quote for GCUSD.
```

**Silver Quote:**
```
Get the current price for silver (SIUSD).
```

**Crude Oil:**
```
What is the current price of crude oil (CLUSD)?
```

**Natural Gas:**
```
Get the real-time quote for natural gas (NGUSD).
```

**Multiple Commodities:**
```
Compare current prices for gold, silver, and platinum.
```

## Common Commodity Symbols

### Precious Metals

| Symbol | Commodity |
|--------|-----------|
| GCUSD | Gold |
| SIUSD | Silver |
| PLUSD | Platinum |
| PAUSD | Palladium |

### Energy

| Symbol | Commodity |
|--------|-----------|
| CLUSD | Crude Oil (WTI) |
| BZUSD | Brent Crude |
| NGUSD | Natural Gas |
| HOUSD | Heating Oil |
| RBUSD | Gasoline (RBOB) |

### Base Metals

| Symbol | Commodity |
|--------|-----------|
| HGUSD | Copper |
| ALUSD | Aluminum |
| ZNUSD | Zinc |
| NIUSD | Nickel |

### Agricultural

| Symbol | Commodity |
|--------|-----------|
| ZCUSD | Corn |
| ZSUSD | Soybeans |
| ZWUSD | Wheat |
| KCUSD | Coffee |
| SBUSD | Sugar |
| CTUSD | Cotton |

## Understanding Quote Data

### Price Components

| Field | Description |
|-------|-------------|
| Current Price | Latest traded price |
| Change | Dollar change from prior close |
| Change % | Percentage change |
| Previous Close | Prior session close |

### Range Data

| Field | Description |
|-------|-------------|
| Day Low | Lowest price today |
| Day High | Highest price today |
| Year Low | 52-week low |
| Year High | 52-week high |

### Technical Indicators

| Field | Description |
|-------|-------------|
| 50-Day Avg | 50-day moving average |
| 200-Day Avg | 200-day moving average |
| Volume | Contracts/units traded |

## Price Analysis

### Day Range Position

```
Position = (Current - Day Low) / (Day High - Day Low) × 100%
```

### Example

From GCUSD data:
- Current: $4,864.20
- Day Low: $4,690.20
- Day High: $4,871.00
- Position: (4,864.20 - 4,690.20) / (4,871.00 - 4,690.20) = 96.2%

**Interpretation**: Trading near the high of the day (bullish).

### 52-Week Range Position

```
Position = (Current - Year Low) / (Year High - Year Low) × 100%
```

### Example

From GCUSD data:
- Current: $4,864.20
- Year Low: $2,837.40
- Year High: $5,626.80
- Position: (4,864.20 - 2,837.40) / (5,626.80 - 2,837.40) = 72.6%

**Interpretation**: Upper portion of 52-week range.

## Moving Average Analysis

### Price vs. Moving Averages

| Condition | Interpretation |
|-----------|----------------|
| Price > 50-day > 200-day | Strong uptrend |
| Price > 200-day > 50-day | Recovery mode |
| Price < 200-day < 50-day | Starting downtrend |
| Price < 50-day < 200-day | Strong downtrend |

### Example

From GCUSD data:
- Price: $4,864.20
- 50-Day: $4,559.45
- 200-Day: $3,888.90
- Pattern: Price > 50-Day > 200-Day

**Interpretation**: Strong uptrend confirmed by moving averages.

### Golden/Death Cross

| Signal | Condition | Meaning |
|--------|-----------|---------|
| Golden Cross | 50-day crosses above 200-day | Bullish |
| Death Cross | 50-day crosses below 200-day | Bearish |

## Volume Analysis

### Volume Context

| Volume Level | Interpretation |
|--------------|----------------|
| Above average | High interest |
| Average | Normal trading |
| Below average | Low interest |
| Spike | Significant event |

### Volume-Price Relationship

| Combination | Meaning |
|-------------|---------|
| High volume + price up | Strong buying |
| High volume + price down | Strong selling |
| Low volume + price up | Weak rally |
| Low volume + price down | Weak decline |

## Commodity-Specific Factors

### Gold (GCUSD)

| Driver | Impact |
|--------|--------|
| Dollar strength | Inverse relationship |
| Interest rates | Higher rates = lower gold |
| Inflation | Hedge demand |
| Geopolitics | Safe haven flows |

### Crude Oil (CLUSD)

| Driver | Impact |
|--------|--------|
| OPEC decisions | Supply impact |
| Economic growth | Demand driver |
| Inventory data | Weekly catalyst |
| Geopolitics | Supply risk |

### Natural Gas (NGUSD)

| Driver | Impact |
|--------|--------|
| Weather | Heating/cooling demand |
| Storage levels | Supply indicator |
| Production | Shale output |
| LNG exports | Demand shift |

## Common Use Cases

### Price Check
```
What is gold trading at right now?
```

### Trend Analysis
```
Is crude oil above or below its 200-day average?
```

### Range Analysis
```
Where is silver relative to its 52-week range?
```

### Momentum Check
```
Is natural gas showing strength today?
```

### Comparison
```
Compare precious metals prices today.
```

## Analysis Tips

1. **Check the trend**: Price vs. moving averages.

2. **Note the range**: Day range and 52-week range positions.

3. **Consider volume**: Confirms or contradicts price move.

4. **Watch the change %**: Context for daily move.

5. **Compare to peers**: Gold vs. silver, WTI vs. Brent.

6. **Know the drivers**: Fundamental factors for each commodity.

## Integration with Other Skills

| Skill | Combined Use |
|-------|--------------|
| commodities-list | Context on commodity markets |
| stock-historical-index | Broader market context |
| stock-price-change | Compare to equity performance |
| sector-performance-snapshot | Energy sector context |
