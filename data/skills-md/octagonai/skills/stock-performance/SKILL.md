---
name: stock-performance
description: Retrieve stock price data and performance metrics using Octagon MCP. Use when analyzing daily closing prices, trading volume, price trends, historical performance, and comparing stock movements over specific time periods.
---

# Stock Performance

Retrieve daily closing prices, trading volume, and performance metrics for public companies using the Octagon MCP server.

## Prerequisites

Ensure Octagon MCP is configured in your AI agent (Cursor, Claude Desktop, Windsurf, etc.). See [references/mcp-setup.md](references/mcp-setup.md) for installation instructions.

## Workflow

### 1. Identify Analysis Parameters

Determine the following before querying:
- **Ticker**: Stock symbol (e.g., AAPL, MSFT, GOOGL)
- **Time Period**: Number of days or date range
- **Metrics** (optional): Price, volume, returns

### 2. Execute Query via Octagon MCP

Use the `octagon-agent` tool with a natural language prompt:

```
Retrieve the daily closing prices for <TICKER> over the last <N> days.
```

**MCP Call Format:**

```json
{
  "server": "octagon-mcp",
  "toolName": "octagon-agent",
  "arguments": {
    "prompt": "Retrieve the daily closing prices for AAPL over the last 30 days."
  }
}
```

### 3. Expected Output

The agent returns structured price data including:

| Date | Closing Price | Volume |
|------|---------------|--------|
| 2026-02-02 | $270.01 | 73,677,607 |
| 2026-01-30 | $259.48 | 92,443,408 |
| 2026-01-29 | $258.28 | 67,253,009 |
| ... | ... | ... |

**Data Sources**: octagon-stock-data-agent, octagon-web-search-agent

### 4. Interpret Results

See [references/interpreting-results.md](references/interpreting-results.md) for guidance on:
- Analyzing price trends
- Evaluating volume patterns
- Calculating returns
- Identifying support/resistance levels

## Example Queries

**Daily Closing Prices:**
```
Retrieve the daily closing prices for AAPL over the last 30 days.
```

**Extended Historical Data:**
```
Get historical stock prices for MSFT for the past 90 days.
```

**Volume Analysis:**
```
Retrieve daily trading volume for TSLA over the last 2 weeks.
```

**Price Range:**
```
What are the high and low prices for NVDA over the past month?
```

**Multi-Stock Comparison:**
```
Compare the stock performance of AAPL, MSFT, and GOOGL over the last 30 days.
```

**52-Week Analysis:**
```
What is the 52-week high and low for AMZN?
```

## Key Metrics

### Price Metrics

| Metric | Description |
|--------|-------------|
| Closing Price | End-of-day price |
| Opening Price | Start-of-day price |
| High | Intraday high |
| Low | Intraday low |
| Adjusted Close | Dividend/split adjusted |

### Volume Metrics

| Metric | Description |
|--------|-------------|
| Daily Volume | Shares traded per day |
| Average Volume | Typical daily volume |
| Relative Volume | Current vs. average |
| Volume Trend | Direction over time |

### Return Metrics

| Metric | Calculation |
|--------|-------------|
| Daily Return | (Close - Prior Close) / Prior Close |
| Period Return | (End - Start) / Start |
| Cumulative Return | Running return over period |
| Annualized Return | Period return scaled to 1 year |

## Price Analysis Framework

### Trend Analysis

| Pattern | Characteristics |
|---------|-----------------|
| Uptrend | Higher highs, higher lows |
| Downtrend | Lower highs, lower lows |
| Sideways | Range-bound movement |
| Breakout | Move beyond range |

### Volatility Assessment

| Measure | Description |
|---------|-------------|
| Price Range | High - Low over period |
| Daily Range | Average daily high-low |
| Standard Deviation | Price dispersion |
| Beta | Relative to market |

### Support/Resistance

| Level | Description |
|-------|-------------|
| Support | Price floor, buying interest |
| Resistance | Price ceiling, selling pressure |
| Moving Averages | Dynamic support/resistance |
| Round Numbers | Psychological levels |

## Volume Analysis

### Volume Patterns

| Pattern | Interpretation |
|---------|----------------|
| High Volume + Price Up | Strong buying conviction |
| High Volume + Price Down | Strong selling pressure |
| Low Volume + Price Up | Weak rally, may reverse |
| Low Volume + Price Down | Lack of selling interest |

### Volume Indicators

| Indicator | Usage |
|-----------|-------|
| Volume Spike | Unusual activity, potential catalyst |
| Volume Dry-up | Consolidation, waiting mode |
| Volume Trend | Confirms price trend |
| On-Balance Volume | Cumulative volume direction |

## Time Period Analysis

### Short-Term (1-30 Days)

| Focus | Use Case |
|-------|----------|
| Recent Performance | Current momentum |
| Trading Signals | Entry/exit timing |
| News Impact | Event analysis |
| Volatility | Risk assessment |

### Medium-Term (1-6 Months)

| Focus | Use Case |
|-------|----------|
| Trend Identification | Direction confirmation |
| Seasonality | Cyclical patterns |
| Earnings Impact | Quarterly effects |
| Sector Rotation | Relative performance |

### Long-Term (1+ Years)

| Focus | Use Case |
|-------|----------|
| Major Trends | Secular moves |
| 52-Week Range | Valuation context |
| Recovery/Decline | Major shifts |
| Dividend Yield | Income analysis |

## Comparative Analysis

### Peer Comparison

| Metric | What to Compare |
|--------|-----------------|
| Return | Relative performance |
| Volatility | Risk comparison |
| Correlation | Movement similarity |
| Volume | Liquidity comparison |

### Benchmark Comparison

| Benchmark | Usage |
|-----------|-------|
| S&P 500 | Large cap reference |
| Sector ETF | Industry context |
| Nasdaq | Tech comparison |
| Russell 2000 | Small cap reference |

## Analysis Tips

1. **Consider context**: Market conditions affect individual stocks.

2. **Adjust for events**: Earnings, dividends, splits affect prices.

3. **Use volume confirmation**: Price moves need volume support.

4. **Multiple timeframes**: Longer and shorter perspectives.

5. **Compare to peers**: Relative performance matters.

6. **Watch key levels**: Round numbers, 52-week highs/lows.

## Use Cases

- **Trading analysis**: Entry and exit timing
- **Performance tracking**: Portfolio monitoring
- **Event analysis**: Earnings, news impact
- **Volatility assessment**: Risk evaluation
- **Peer comparison**: Relative performance
