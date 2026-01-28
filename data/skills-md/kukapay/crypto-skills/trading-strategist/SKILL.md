---
name: trading-strategist
description: Provides trading strategies for cryptocurrencies based on Binance market data, calculated technical analysis indicators, and aggregated market sentiment from crypto RSS news feeds. Use when users ask for trading advice, strategy recommendations, or analysis combining price data, TA, and sentiment for crypto assets like ETH, BTC, or altcoins.
---

# Trading Strategies Skill

This skill generates data-driven trading strategies for cryptocurrencies by integrating multiple data sources and analytical tools.

## Core Components

1. **Binance Market Data**: Real-time price, volume, and historical klines from Binance API
2. **Technical Analysis (TA)**: Calculated indicators including SMA, RSI, MACD, Bollinger Bands, Stochastic, and more
3. **Market Sentiment**: Aggregated sentiment scores from popular crypto RSS feeds

## Workflow

### Step 1: Data Collection
- Fetch current ticker data from Binance API (`/api/v3/ticker/price` and `/api/v3/ticker/24hr`)
- Retrieve historical klines (`/api/v3/klines` with 30-100 days of data)
- Aggregate sentiment using the market-sentiment skill

### Step 2: TA Calculation
Use the `scripts/calculate_ta.py` script to compute indicators from historical data.

### Step 3: Strategy Generation
Combine TA signals, price action, and sentiment score to recommend:
- Buy/Sell/Hold signals
- Entry/exit points
- Risk management (stop-loss, position sizing)
- Timeframes (swing, day trading)

## Usage Examples

### Basic Strategy Request
```
For ETH, generate a trading strategy based on current market data.
```
→ Fetch ETH data, calculate TA, get sentiment, output strategy.

### Advanced Analysis
```
Analyze BTC with 50-day history, include sentiment, recommend swing trade.
```
→ Use longer history, focus on swing signals.

## Risk Management
- Always include stop-loss recommendations
- Suggest position sizes (1-5% of capital)
- Warn about volatility and leverage risks
- Note: Not financial advice

## References
- TA formulas: See [references/ta_formulas.md](references/ta_formulas.md)
- Sentiment interpretation: See [references/sentiment_guide.md](references/sentiment_guide.md)

## Scripts
- `scripts/calculate_ta.py`: Python script for TA indicator calculations
- `scripts/fetch_binance.py`: Helper for Binance API calls</content>
<parameter name="filePath">./skills/trading-strategies/SKILL.md
