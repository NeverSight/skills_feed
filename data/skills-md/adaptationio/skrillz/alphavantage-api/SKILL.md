---
name: alphavantage-api
description: Alpha Vantage financial API for stocks, forex, crypto, and 50+ technical indicators. Use when fetching time series data, technical analysis, fundamentals, economic indicators, or news sentiment.
version: 1.0.0
---

# Alpha Vantage API Integration

Financial data API providing stocks, forex, crypto, technical indicators, fundamental data, economic indicators, and AI-powered news sentiment analysis.

## Quick Start

### Authentication
```bash
# Environment variable (recommended)
export ALPHAVANTAGE_API_KEY="your_api_key"

# Or in .env file
ALPHAVANTAGE_API_KEY=your_api_key
```

### Basic Usage (Python)
```python
import requests
import os

API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")
BASE_URL = "https://www.alphavantage.co/query"

def get_quote(symbol: str) -> dict:
    """Get real-time quote for a symbol."""
    response = requests.get(BASE_URL, params={
        "function": "GLOBAL_QUOTE",
        "symbol": symbol,
        "apikey": API_KEY
    })
    return response.json().get("Global Quote", {})

# Example
quote = get_quote("AAPL")
print(f"AAPL: ${quote['05. price']} ({quote['10. change percent']})")
```

### Using Python Package
```python
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators

# Time series data
ts = TimeSeries(key=API_KEY, output_format='pandas')
data, meta = ts.get_daily(symbol='AAPL', outputsize='compact')

# Technical indicators
ti = TechIndicators(key=API_KEY, output_format='pandas')
rsi, meta = ti.get_rsi(symbol='AAPL', interval='daily', time_period=14)
```

## API Functions Reference

### Stock Time Series

| Function | Description | Free |
|----------|-------------|------|
| `TIME_SERIES_INTRADAY` | 1-60min intervals | ✅ |
| `TIME_SERIES_DAILY` | Daily OHLCV | ✅ |
| `TIME_SERIES_DAILY_ADJUSTED` | With splits/dividends | ⚠️ Premium |
| `TIME_SERIES_WEEKLY` | Weekly OHLCV | ✅ |
| `TIME_SERIES_MONTHLY` | Monthly OHLCV | ✅ |
| `GLOBAL_QUOTE` | Latest quote | ✅ |
| `SYMBOL_SEARCH` | Search symbols | ✅ |

### Fundamental Data

| Function | Description | Free |
|----------|-------------|------|
| `OVERVIEW` | Company overview | ✅ |
| `INCOME_STATEMENT` | Income statements | ✅ |
| `BALANCE_SHEET` | Balance sheets | ✅ |
| `CASH_FLOW` | Cash flow statements | ✅ |
| `EARNINGS` | Earnings history | ✅ |
| `EARNINGS_CALENDAR` | Upcoming earnings | ✅ |
| `IPO_CALENDAR` | Upcoming IPOs | ✅ |

### Forex

| Function | Description | Free |
|----------|-------------|------|
| `CURRENCY_EXCHANGE_RATE` | Real-time rate | ✅ |
| `FX_INTRADAY` | Intraday forex | ✅ |
| `FX_DAILY` | Daily forex | ✅ |
| `FX_WEEKLY` | Weekly forex | ✅ |
| `FX_MONTHLY` | Monthly forex | ✅ |

### Cryptocurrency

| Function | Description | Free |
|----------|-------------|------|
| `CURRENCY_EXCHANGE_RATE` | Crypto rate | ✅ |
| `DIGITAL_CURRENCY_DAILY` | Daily crypto | ✅ |
| `DIGITAL_CURRENCY_WEEKLY` | Weekly crypto | ✅ |
| `DIGITAL_CURRENCY_MONTHLY` | Monthly crypto | ✅ |

### Technical Indicators (50+)

| Category | Indicators |
|----------|------------|
| **Trend** | SMA, EMA, WMA, DEMA, TEMA, KAMA, MAMA, T3, TRIMA |
| **Momentum** | RSI, MACD, STOCH, WILLR, ADX, CCI, MFI, ROC, AROON, MOM |
| **Volatility** | BBANDS, ATR, NATR, TRANGE |
| **Volume** | OBV, AD, ADOSC |
| **Hilbert** | HT_TRENDLINE, HT_SINE, HT_PHASOR, etc. |

### Economic Indicators

| Function | Description | Free |
|----------|-------------|------|
| `REAL_GDP` | US GDP | ✅ |
| `CPI` | Consumer Price Index | ✅ |
| `INFLATION` | Inflation rate | ✅ |
| `UNEMPLOYMENT` | Unemployment rate | ✅ |
| `FEDERAL_FUNDS_RATE` | Fed funds rate | ✅ |
| `TREASURY_YIELD` | Treasury yields | ✅ |

### Alpha Intelligence

| Function | Description | Free |
|----------|-------------|------|
| `NEWS_SENTIMENT` | AI sentiment analysis | ✅ |
| `TOP_GAINERS_LOSERS` | Market movers | ✅ |
| `INSIDER_TRANSACTIONS` | Insider trades | ⚠️ Premium |
| `ANALYTICS_FIXED_WINDOW` | Analytics | ⚠️ Premium |

## Rate Limits

| Tier | Daily | Per Minute | Price |
|------|-------|------------|-------|
| Free | 25 | 5 | $0 |
| Premium | Unlimited | 75-1,200 | $49.99-$249.99/mo |

**Important:** Rate limits are IP-based, not key-based.

## Common Tasks

### Task: Get Daily Stock Data
```python
def get_daily_data(symbol: str, full: bool = False) -> dict:
    """Get daily OHLCV data."""
    response = requests.get(BASE_URL, params={
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "outputsize": "full" if full else "compact",
        "apikey": API_KEY
    })
    return response.json().get("Time Series (Daily)", {})

# Example
data = get_daily_data("AAPL")
latest = list(data.items())[0]
print(f"{latest[0]}: Close ${latest[1]['4. close']}")
```

### Task: Get Technical Indicator
```python
def get_rsi(symbol: str, period: int = 14) -> dict:
    """Get RSI indicator values."""
    response = requests.get(BASE_URL, params={
        "function": "RSI",
        "symbol": symbol,
        "interval": "daily",
        "time_period": period,
        "series_type": "close",
        "apikey": API_KEY
    })
    return response.json().get("Technical Analysis: RSI", {})

# Example
rsi = get_rsi("AAPL")
latest_rsi = list(rsi.values())[0]["RSI"]
print(f"AAPL RSI(14): {latest_rsi}")
```

### Task: Get Company Overview
```python
def get_company_overview(symbol: str) -> dict:
    """Get comprehensive company information."""
    response = requests.get(BASE_URL, params={
        "function": "OVERVIEW",
        "symbol": symbol,
        "apikey": API_KEY
    })
    data = response.json()

    return {
        "name": data.get("Name"),
        "description": data.get("Description"),
        "sector": data.get("Sector"),
        "industry": data.get("Industry"),
        "market_cap": data.get("MarketCapitalization"),
        "pe_ratio": data.get("PERatio"),
        "dividend_yield": data.get("DividendYield"),
        "eps": data.get("EPS"),
        "52_week_high": data.get("52WeekHigh"),
        "52_week_low": data.get("52WeekLow"),
        "beta": data.get("Beta")
    }
```

### Task: Get Forex Rate
```python
def get_forex_rate(from_currency: str, to_currency: str) -> dict:
    """Get currency exchange rate."""
    response = requests.get(BASE_URL, params={
        "function": "CURRENCY_EXCHANGE_RATE",
        "from_currency": from_currency,
        "to_currency": to_currency,
        "apikey": API_KEY
    })
    return response.json().get("Realtime Currency Exchange Rate", {})

# Example
rate = get_forex_rate("USD", "EUR")
print(f"USD/EUR: {rate['5. Exchange Rate']}")
```

### Task: Get Crypto Price
```python
def get_crypto_price(symbol: str, market: str = "USD") -> dict:
    """Get cryptocurrency price."""
    response = requests.get(BASE_URL, params={
        "function": "CURRENCY_EXCHANGE_RATE",
        "from_currency": symbol,
        "to_currency": market,
        "apikey": API_KEY
    })
    data = response.json().get("Realtime Currency Exchange Rate", {})
    return {
        "symbol": symbol,
        "price": data.get("5. Exchange Rate"),
        "last_updated": data.get("6. Last Refreshed")
    }

# Example
btc = get_crypto_price("BTC")
print(f"BTC: ${float(btc['price']):,.2f}")
```

### Task: Get News Sentiment
```python
def get_news_sentiment(tickers: str = None, topics: str = None) -> list:
    """Get AI-powered news sentiment analysis."""
    params = {
        "function": "NEWS_SENTIMENT",
        "apikey": API_KEY
    }
    if tickers:
        params["tickers"] = tickers
    if topics:
        params["topics"] = topics

    response = requests.get(BASE_URL, params=params)
    return response.json().get("feed", [])

# Example
news = get_news_sentiment(tickers="AAPL")
for article in news[:3]:
    sentiment = article.get("overall_sentiment_label", "N/A")
    print(f"{article['title'][:50]}... [{sentiment}]")
```

### Task: Get Economic Indicators
```python
def get_economic_indicator(indicator: str) -> dict:
    """Get US economic indicator data."""
    response = requests.get(BASE_URL, params={
        "function": indicator,
        "apikey": API_KEY
    })
    return response.json()

# Examples
gdp = get_economic_indicator("REAL_GDP")
cpi = get_economic_indicator("CPI")
unemployment = get_economic_indicator("UNEMPLOYMENT")
fed_rate = get_economic_indicator("FEDERAL_FUNDS_RATE")
```

### Task: Get Earnings Calendar
```python
def get_earnings_calendar(horizon: str = "3month") -> list:
    """Get upcoming earnings releases."""
    import csv
    from io import StringIO

    response = requests.get(BASE_URL, params={
        "function": "EARNINGS_CALENDAR",
        "horizon": horizon,  # 3month, 6month, 12month
        "apikey": API_KEY
    })

    # Returns CSV format
    reader = csv.DictReader(StringIO(response.text))
    return list(reader)

# Example
earnings = get_earnings_calendar()
for e in earnings[:5]:
    print(f"{e['symbol']}: {e['reportDate']}")
```

## Error Handling

```python
def safe_api_call(params: dict) -> dict:
    """Make API call with error handling."""
    params["apikey"] = API_KEY

    try:
        response = requests.get(BASE_URL, params=params)
        data = response.json()

        # Check for rate limit
        if "Note" in data:
            print(f"Rate limit: {data['Note']}")
            return {}

        # Check for error message
        if "Error Message" in data:
            print(f"API Error: {data['Error Message']}")
            return {}

        # Check for information message (often rate limit)
        if "Information" in data:
            print(f"Info: {data['Information']}")
            return {}

        return data

    except Exception as e:
        print(f"Request error: {e}")
        return {}
```

## Free vs Premium Features

### Free Tier Includes
- 25 requests per day
- 5 requests per minute
- Historical time series (20+ years)
- 50+ technical indicators
- Fundamental data
- Forex and crypto
- Economic indicators
- News sentiment

### Premium Required
- Unlimited daily requests
- Adjusted time series
- Realtime US market data
- 15-minute delayed data
- Insider transactions
- Advanced analytics
- Priority support

## Best Practices

1. **Cache responses** - Data doesn't change frequently
2. **Use compact outputsize** - Unless you need full history
3. **Batch requests wisely** - 25/day limit is strict
4. **Handle rate limits** - Check for "Note" key in response
5. **Use pandas output** - With alpha_vantage package
6. **Store historical data** - Avoid re-fetching same data

## Installation

```bash
# Official Python wrapper
pip install alpha_vantage pandas

# For async support
pip install aiohttp
```

## Usage with Pandas

```python
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
import pandas as pd

# Initialize with pandas output
ts = TimeSeries(key=API_KEY, output_format='pandas')
ti = TechIndicators(key=API_KEY, output_format='pandas')

# Get daily data
data, meta = ts.get_daily(symbol='AAPL', outputsize='compact')

# Get indicators
sma, _ = ti.get_sma(symbol='AAPL', interval='daily', time_period=20)
rsi, _ = ti.get_rsi(symbol='AAPL', interval='daily', time_period=14)

# Combine
analysis = data.join([sma, rsi])
```

## Related Skills
- `finnhub-api` - Real-time quotes and news
- `twelvedata-api` - More indicators, better rate limits
- `fmp-api` - Fundamental analysis focus

## References
- [Official Documentation](https://www.alphavantage.co/documentation/)
- [Python Package](https://github.com/RomelTorres/alpha_vantage)
- [API Support](https://www.alphavantage.co/support/)
