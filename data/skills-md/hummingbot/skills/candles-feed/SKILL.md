---
name: candles-feed
description: Fetch market data (OHLCV candles) and calculate technical indicators (RSI, EMA, MACD, Bollinger Bands) from exchanges via Hummingbot API. Use this skill when the user needs price data, candlestick charts, or technical analysis.
metadata:
  author: fengtality
---

# candles-feed

This skill fetches candlestick (OHLCV) data from exchanges and calculates technical indicators. It provides the data foundation for strategy development and market analysis.

## Prerequisites

- Hummingbot API server must be running (use the setup skill)
- Exchange connector must support candle data

## Capabilities

### 1. Get Available Connectors

List exchanges that support candle data:

```bash
./scripts/list_candle_connectors.sh
```

### 2. Fetch Candles

Get OHLCV data for a trading pair:

```bash
./scripts/get_candles.sh \
    --connector binance \
    --pair BTC-USDT \
    --interval 1h \
    --days 30
```

Supported intervals: `1m`, `5m`, `15m`, `30m`, `1h`, `4h`, `1d`, `1w`

### 3. Calculate Indicators

Calculate technical indicators on candle data:

```bash
# RSI (Relative Strength Index)
./scripts/calculate_indicator.sh \
    --connector binance \
    --pair BTC-USDT \
    --indicator rsi \
    --period 14

# EMA (Exponential Moving Average)
./scripts/calculate_indicator.sh \
    --connector binance \
    --pair BTC-USDT \
    --indicator ema \
    --period 20

# MACD (Moving Average Convergence Divergence)
./scripts/calculate_indicator.sh \
    --connector binance \
    --pair BTC-USDT \
    --indicator macd \
    --fast 12 \
    --slow 26 \
    --signal 9

# Bollinger Bands
./scripts/calculate_indicator.sh \
    --connector binance \
    --pair BTC-USDT \
    --indicator bb \
    --period 20 \
    --std 2
```

### 4. Get Current Price

Get the latest price for trading pairs:

```bash
./scripts/get_price.sh \
    --connector binance \
    --pairs "BTC-USDT,ETH-USDT"
```

### 5. Get Funding Rate (Perpetuals)

Get funding rate for perpetual contracts:

```bash
./scripts/get_funding_rate.sh \
    --connector binance_perpetual \
    --pair BTC-USDT
```

## Supported Indicators

| Indicator | Code | Parameters | Description |
|-----------|------|------------|-------------|
| RSI | `rsi` | period | Relative Strength Index |
| EMA | `ema` | period | Exponential Moving Average |
| SMA | `sma` | period | Simple Moving Average |
| MACD | `macd` | fast, slow, signal | Moving Average Convergence Divergence |
| Bollinger Bands | `bb` | period, std | Volatility bands |
| ATR | `atr` | period | Average True Range |
| VWAP | `vwap` | - | Volume Weighted Average Price |
| Stochastic | `stoch` | k_period, d_period | Stochastic Oscillator |

## Candle Data Format

Returned candle data includes:

| Field | Type | Description |
|-------|------|-------------|
| `timestamp` | int | Unix timestamp (ms) |
| `open` | float | Opening price |
| `high` | float | Highest price |
| `low` | float | Lowest price |
| `close` | float | Closing price |
| `volume` | float | Trading volume |

Example output:
```json
{
    "candles": [
        {
            "timestamp": 1706400000000,
            "open": 42150.5,
            "high": 42300.0,
            "low": 42100.0,
            "close": 42250.0,
            "volume": 1250.5
        }
    ],
    "interval": "1h",
    "total_candles": 720
}
```

## Indicator Output

### RSI Output
```json
{
    "indicator": "rsi",
    "period": 14,
    "current_value": 65.5,
    "signal": "neutral",
    "interpretation": {
        "overbought": 70,
        "oversold": 30,
        "description": "RSI at 65.5 indicates slightly bullish momentum"
    }
}
```

### MACD Output
```json
{
    "indicator": "macd",
    "current_values": {
        "macd_line": 125.5,
        "signal_line": 110.2,
        "histogram": 15.3
    },
    "signal": "bullish",
    "interpretation": "MACD above signal line, positive momentum"
}
```

### Bollinger Bands Output
```json
{
    "indicator": "bb",
    "period": 20,
    "std": 2,
    "current_values": {
        "upper": 43500.0,
        "middle": 42000.0,
        "lower": 40500.0,
        "current_price": 42250.0
    },
    "position": "middle",
    "bandwidth": 0.071
}
```

## Workflow: Market Analysis

1. **Check available connectors**
   ```bash
   ./scripts/list_candle_connectors.sh
   ```

2. **Fetch candle data**
   ```bash
   ./scripts/get_candles.sh --connector binance --pair BTC-USDT --interval 4h --days 30
   ```

3. **Calculate indicators**
   ```bash
   # Get RSI
   ./scripts/calculate_indicator.sh --connector binance --pair BTC-USDT --indicator rsi --period 14

   # Get EMA crossover
   ./scripts/calculate_indicator.sh --connector binance --pair BTC-USDT --indicator ema --period 20
   ./scripts/calculate_indicator.sh --connector binance --pair BTC-USDT --indicator ema --period 50
   ```

4. **Interpret signals**
   - RSI > 70: Overbought, potential sell signal
   - RSI < 30: Oversold, potential buy signal
   - EMA(20) > EMA(50): Bullish trend
   - EMA(20) < EMA(50): Bearish trend

## API Endpoints Used

All requests go to `http://localhost:8000` with Basic Auth (`admin:admin`):

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/market-data/available-candle-connectors` | GET | List connectors with candle support |
| `/market-data/historical-candles` | POST | Fetch bulk historical OHLCV data |
| `/market-data/candles` | POST | Fetch real-time OHLCV data |
| `/market-data/prices` | POST | Get current prices |
| `/market-data/funding-info` | POST | Get funding rates |

## Data Fetching Strategy

Scripts use a dual-fetch approach for comprehensive data:
1. **Historical candles** - Bulk data from `/market-data/historical-candles`
2. **Real-time candles** - Latest data from `/market-data/candles`
3. **Merge** - Deduplicate by timestamp, real-time overrides historical

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `API_URL` | `http://localhost:8000` | API base URL |
| `API_USER` | `admin` | API username |
| `API_PASS` | `admin` | API password |

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| "Connector not supported" | Exchange doesn't support candles | Use list_candle_connectors |
| "Invalid interval" | Unsupported interval format | Use 1m, 5m, 15m, 30m, 1h, 4h, 1d, 1w |
| "Rate limited" | Too many requests | Wait and retry |
| "Invalid trading pair" | Pair not available | Check exchange for valid pairs |

## Notes

- Candle data is fetched directly from exchanges via the Hummingbot API
- Indicators are calculated locally using the fetched candle data
- Historical data availability varies by exchange (typically 30-90 days)
- For real-time data, consider shorter intervals (1m, 5m)
- For trend analysis, use longer intervals (4h, 1d)
