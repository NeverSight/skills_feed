---
name: stock-quote
description: Retrieve real-time stock quotes using Octagon MCP. Use when you need current price, day range, 52-week range, volume, market cap, and moving averages for any publicly traded stock.
---

# Stock Quote

Retrieve real-time stock quotes with current price, volume, day range, 52-week range, market cap, and moving averages using the Octagon MCP server.

## Prerequisites

Ensure Octagon MCP is configured in your AI agent (Cursor, Claude Desktop, Windsurf, etc.). See [references/mcp-setup.md](references/mcp-setup.md) for installation instructions.

## Workflow

### 1. Identify the Stock

Determine the ticker symbol for the stock you want to quote (e.g., AAPL, MSFT, GOOGL).

### 2. Execute Query via Octagon MCP

Use the `octagon-agent` tool with a natural language prompt:

```
Get real-time stock quote for the symbol <TICKER>.
```

**MCP Call Format:**

```json
{
  "server": "octagon-mcp",
  "toolName": "octagon-agent",
  "arguments": {
    "prompt": "Get real-time stock quote for the symbol AAPL."
  }
}
```

### 3. Expected Output

The agent returns a comprehensive quote including:

| Metric | Example Value |
|--------|---------------|
| Current Price | $270.01 |
| Change | +$10.53 (+4.06%) |
| Volume | 72,890,096 shares |
| Day Range | $259.21 - $270.48 |
| 52-Week Range | $169.21 - $288.62 |
| Market Cap | $3.97 trillion |
| Exchange | NASDAQ |
| Previous Close | $259.48 |
| 50-Day Average | $268.30 |
| 200-Day Average | $236.65 |

**Data Sources**: octagon-stock-data-agent

### 4. Interpret Results

See [references/interpreting-results.md](references/interpreting-results.md) for guidance on:
- Understanding price movements
- Evaluating volume significance
- Analyzing range positions
- Using moving averages

## Example Queries

**Basic Quote:**
```
Get real-time stock quote for the symbol AAPL.
```

**Multiple Stocks:**
```
Get stock quotes for AAPL, MSFT, and GOOGL.
```

**Specific Metrics:**
```
What is the current price and market cap for TSLA?
```

**Range Analysis:**
```
Where is NVDA trading relative to its 52-week range?
```

**Moving Averages:**
```
What are the 50-day and 200-day moving averages for AMZN?
```

## Key Quote Components

### Price Information

| Component | Description |
|-----------|-------------|
| Current Price | Last traded price |
| Change | Dollar change from previous close |
| Percent Change | Percentage change from previous close |
| Previous Close | Prior day's closing price |

### Volume Data

| Component | Description |
|-----------|-------------|
| Volume | Shares traded today |
| Average Volume | Typical daily volume |
| Relative Volume | Current vs. average |

### Range Data

| Component | Description |
|-----------|-------------|
| Day High | Highest price today |
| Day Low | Lowest price today |
| 52-Week High | Highest price in past year |
| 52-Week Low | Lowest price in past year |

### Market Data

| Component | Description |
|-----------|-------------|
| Market Cap | Total market value |
| Exchange | Trading venue (NASDAQ, NYSE, etc.) |
| Shares Outstanding | Total shares issued |

### Technical Indicators

| Component | Description |
|-----------|-------------|
| 50-Day MA | 50-day moving average |
| 200-Day MA | 200-day moving average |
| Golden Cross | 50-day crosses above 200-day |
| Death Cross | 50-day crosses below 200-day |

## Quote Analysis Framework

### Price Position Analysis

| Position | Interpretation |
|----------|----------------|
| Near 52-Week High | Strong momentum, potential resistance |
| Near 52-Week Low | Weakness, potential support |
| Mid-Range | Neutral, watch for direction |
| Above Moving Averages | Bullish trend |
| Below Moving Averages | Bearish trend |

### Volume Analysis

| Volume Level | Interpretation |
|--------------|----------------|
| Above Average | High interest, confirming move |
| Below Average | Low conviction |
| Spike | Unusual activity, catalyst likely |

### Moving Average Signals

| Signal | Condition | Interpretation |
|--------|-----------|----------------|
| Golden Cross | 50-day > 200-day | Bullish |
| Death Cross | 50-day < 200-day | Bearish |
| Price > Both MAs | Above both averages | Strong uptrend |
| Price < Both MAs | Below both averages | Strong downtrend |

## Market Context

### Trading Hours

| Session | Time (ET) |
|---------|-----------|
| Pre-Market | 4:00 AM - 9:30 AM |
| Regular | 9:30 AM - 4:00 PM |
| After-Hours | 4:00 PM - 8:00 PM |

### Quote Timing

| When | Data Reflects |
|------|---------------|
| Market Hours | Real-time or 15-min delay |
| Pre/After Hours | Extended hours trading |
| Closed Market | Previous close |

## Common Use Cases

### Quick Price Check
```
What is AAPL trading at right now?
```

### Portfolio Monitoring
```
Get quotes for my holdings: AAPL, MSFT, GOOGL, AMZN, META.
```

### Valuation Context
```
What is the market cap of NVDA?
```

### Technical Analysis
```
Is TSLA trading above or below its 200-day moving average?
```

### Range Analysis
```
How close is AMZN to its 52-week high?
```

## Analysis Tips

1. **Compare to averages**: Price vs. 50-day and 200-day MA shows trend.

2. **Check volume**: High volume confirms price moves.

3. **Range position**: Near highs = strength, near lows = weakness.

4. **Market cap context**: Larger caps typically less volatile.

5. **Time of day**: Opening and closing often most volatile.

6. **Pre/post market**: Less liquidity, wider spreads.

## Integration with Other Skills

| Skill | Combined Use |
|-------|--------------|
| stock-performance | Current quote + historical context |
| financial-metrics-analysis | Quote + fundamental valuation |
| income-statement | Price vs. earnings relationship |
| analyst-estimates | Quote vs. price targets |
