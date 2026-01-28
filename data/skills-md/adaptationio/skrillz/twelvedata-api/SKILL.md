---
name: twelvedata-api
description: Twelve Data financial API for stocks, forex, crypto, ETFs, and 100+ technical indicators. Use when fetching time series data, technical analysis, fundamentals, or real-time streaming quotes.
version: 1.0.0
---

# Twelve Data API Integration

Comprehensive financial data API providing stocks, forex, crypto, ETFs, indices, and 100+ technical indicators with excellent Python SDK support.

## Quick Start

### Authentication
```bash
# Environment variable (recommended)
export TWELVEDATA_API_KEY="your_api_key"

# Or in .env file
TWELVEDATA_API_KEY=your_api_key
```

### Basic Usage (Python)
```python
import requests
import os

API_KEY = os.getenv("TWELVEDATA_API_KEY")
BASE_URL = "https://api.twelvedata.com"

def get_quote(symbol: str) -> dict:
    """Get real-time quote for a symbol."""
    response = requests.get(
        f"{BASE_URL}/quote",
        params={"symbol": symbol, "apikey": API_KEY}
    )
    return response.json()

# Example
quote = get_quote("AAPL")
print(f"AAPL: ${quote['close']} ({quote['percent_change']}%)")
```

### Using Official SDK
```python
from twelvedata import TDClient

td = TDClient(apikey="your_api_key")

# Get time series
ts = td.time_series(
    symbol="AAPL",
    interval="1day",
    outputsize=30
).as_pandas()

# Get quote
quote = td.quote(symbol="AAPL").as_json()

# Get with technical indicators
ts_with_indicators = td.time_series(
    symbol="AAPL",
    interval="1day",
    outputsize=50
).with_sma(time_period=20).with_rsi().as_pandas()
```

## API Endpoints Reference

### Core Data

| Endpoint | Description | Credits |
|----------|-------------|---------|
| `/quote` | Real-time quote | 1 |
| `/price` | Current price only | 1 |
| `/eod` | End of day price | 1 |
| `/time_series` | Historical OHLCV | 1 |
| `/exchange_rate` | Currency conversion | 1 |

### Reference Data

| Endpoint | Description | Credits |
|----------|-------------|---------|
| `/symbol_search` | Search symbols | 1 |
| `/instruments` | List all instruments | Free |
| `/exchanges` | List exchanges | Free |
| `/instrument_type` | List types | Free |
| `/earliest_timestamp` | Data start date | Free |

### Fundamental Data

| Endpoint | Description | Credits |
|----------|-------------|---------|
| `/income_statement` | Income statement | 100 |
| `/balance_sheet` | Balance sheet | 100 |
| `/cash_flow` | Cash flow | 100 |
| `/earnings` | Earnings history | 100 |
| `/earnings_calendar` | Upcoming earnings | 100 |
| `/dividends` | Dividend history | 1 |
| `/splits` | Split history | 1 |
| `/statistics` | Key statistics | 100 |
| `/profile` | Company profile | 100 |

### Technical Indicators (100+)

All indicators cost 1 credit and are included with time_series:

**Trend:** SMA, EMA, WMA, DEMA, TEMA, KAMA, MAMA, T3, TRIMA, VWMA
**Momentum:** RSI, MACD, Stochastic, Williams %R, ADX, CCI, MFI, ROC, AROON
**Volatility:** Bollinger Bands, ATR, Keltner Channels, Donchian
**Volume:** OBV, AD, ADOSC, VWAP

## Rate Limits

| Tier | Calls/Min | Daily | WebSocket |
|------|-----------|-------|-----------|
| Free | 8 | 800 | Trial only |
| Grow ($29) | 55-377 | Unlimited | ❌ |
| Pro ($99) | 610-1597 | Unlimited | ✅ |
| Enterprise ($329) | 2584+ | Unlimited | ✅ |

**Credit System:**
- Standard endpoints: 1 credit per symbol
- Fundamental data: 100 credits per symbol
- Batch requests: Same cost as individual

## Common Tasks

### Task: Get Time Series with Pandas
```python
from twelvedata import TDClient
import pandas as pd

td = TDClient(apikey=API_KEY)

def get_historical_data(symbol: str, days: int = 100) -> pd.DataFrame:
    """Get historical OHLCV data as DataFrame."""
    ts = td.time_series(
        symbol=symbol,
        interval="1day",
        outputsize=days
    )
    return ts.as_pandas()

# Example
df = get_historical_data("AAPL", 100)
print(df.head())
```

### Task: Technical Analysis with Multiple Indicators
```python
def get_technical_analysis(symbol: str) -> pd.DataFrame:
    """Get price data with technical indicators."""
    ts = td.time_series(
        symbol=symbol,
        interval="1day",
        outputsize=100
    )

    # Chain indicators
    df = (ts
        .with_sma(time_period=20)
        .with_sma(time_period=50)
        .with_rsi(time_period=14)
        .with_macd()
        .with_bbands()
        .as_pandas()
    )

    return df

# Example
analysis = get_technical_analysis("AAPL")
```

### Task: Get Multiple Symbols (Batch)
```python
def get_batch_quotes(symbols: list) -> dict:
    """Get quotes for multiple symbols efficiently."""
    symbol_str = ",".join(symbols)

    response = requests.get(
        f"{BASE_URL}/quote",
        params={
            "symbol": symbol_str,
            "apikey": API_KEY
        }
    )
    return response.json()

# Example: Up to 120 symbols per request
quotes = get_batch_quotes(["AAPL", "MSFT", "GOOGL", "AMZN"])
```

### Task: Get Fundamental Data
```python
def get_fundamentals(symbol: str) -> dict:
    """Get comprehensive fundamental data."""
    # Note: Each call costs 100 credits

    profile = requests.get(
        f"{BASE_URL}/profile",
        params={"symbol": symbol, "apikey": API_KEY}
    ).json()

    stats = requests.get(
        f"{BASE_URL}/statistics",
        params={"symbol": symbol, "apikey": API_KEY}
    ).json()

    return {
        "name": profile.get("name"),
        "sector": profile.get("sector"),
        "industry": profile.get("industry"),
        "market_cap": stats.get("statistics", {}).get("valuations_metrics", {}).get("market_capitalization"),
        "pe_ratio": stats.get("statistics", {}).get("valuations_metrics", {}).get("trailing_pe"),
        "dividend_yield": stats.get("statistics", {}).get("dividends_and_splits", {}).get("dividend_yield")
    }
```

### Task: Get Forex Rates
```python
def get_forex_rate(from_currency: str, to_currency: str) -> dict:
    """Get currency exchange rate."""
    response = requests.get(
        f"{BASE_URL}/exchange_rate",
        params={
            "symbol": f"{from_currency}/{to_currency}",
            "apikey": API_KEY
        }
    )
    return response.json()

# Example
rate = get_forex_rate("USD", "EUR")
print(f"USD/EUR: {rate['rate']}")
```

### Task: Get Crypto Data
```python
def get_crypto_price(symbol: str, exchange: str = "Binance") -> dict:
    """Get cryptocurrency price."""
    response = requests.get(
        f"{BASE_URL}/quote",
        params={
            "symbol": f"{symbol}/USD",
            "exchange": exchange,
            "apikey": API_KEY
        }
    )
    return response.json()

# Example
btc = get_crypto_price("BTC")
print(f"BTC: ${btc['close']}")
```

### Task: Search for Symbols
```python
def search_symbols(query: str, show_plan: bool = False) -> list:
    """Search for stock/crypto symbols."""
    params = {
        "symbol": query,
        "apikey": API_KEY
    }
    if show_plan:
        params["show_plan"] = "true"

    response = requests.get(f"{BASE_URL}/symbol_search", params=params)
    return response.json().get("data", [])

# Example
results = search_symbols("Apple")
for r in results[:5]:
    print(f"{r['symbol']}: {r['instrument_name']}")
```

## WebSocket Real-Time Streaming

```python
from twelvedata import TDClient

td = TDClient(apikey=API_KEY)

def on_event(event):
    """Handle real-time price updates."""
    print(f"{event['symbol']}: ${event['price']}")

# Create WebSocket (requires Pro plan)
ws = td.websocket(
    symbols=["AAPL", "MSFT", "GOOGL"],
    on_event=on_event
)

ws.connect()
ws.keep_alive()
```

## Error Handling

```python
def safe_api_call(endpoint: str, params: dict) -> dict:
    """Make API call with error handling."""
    params["apikey"] = API_KEY

    try:
        response = requests.get(f"{BASE_URL}/{endpoint}", params=params)
        data = response.json()

        # Check for API errors
        if "status" in data and data["status"] == "error":
            print(f"API Error: {data.get('message', 'Unknown error')}")
            return {}

        # Check remaining credits
        credits_used = response.headers.get("api-credits-used")
        credits_left = response.headers.get("api-credits-left")
        if credits_left:
            print(f"Credits remaining: {credits_left}")

        return data

    except Exception as e:
        print(f"Request error: {e}")
        return {}
```

## Free vs Premium Features

### Free Tier Includes
- 8 API calls/minute, 800/day
- US stocks, forex, crypto
- Time series data (end of day)
- All technical indicators
- Basic reference data
- 1-2 years intraday history
- 30+ years daily history

### Premium Required
- Higher rate limits
- International stocks (Grow+)
- WebSocket streaming (Pro+)
- Pre/post market data (Pro+)
- Extended hours trading
- Mutual funds & ETF breakdown (Enterprise)
- No daily limits

## Best Practices

1. **Use batch requests** - Up to 120 symbols per call
2. **Cache reference data** - Exchanges, instruments rarely change
3. **Use SDK pandas output** - Easier data manipulation
4. **Chain indicators** - Include with time_series (1 credit total)
5. **Monitor credits** - Check response headers
6. **Use appropriate intervals** - 1day for analysis, 1min for trading

## Installation

```bash
# Python SDK with all features
pip install twelvedata[matplotlib,plotly]

# Basic installation
pip install twelvedata

# For WebSocket
pip install websocket-client
```

## Related Skills
- `finnhub-api` - Real-time news focus
- `alphavantage-api` - Alternative indicator source
- `fmp-api` - Fundamental analysis focus

## References
- [Official Documentation](https://twelvedata.com/docs)
- [Python SDK](https://github.com/twelvedata/twelvedata-python)
- [Technical Indicators](https://twelvedata.com/docs#technical-indicators)
- [Pricing](https://twelvedata.com/pricing)
