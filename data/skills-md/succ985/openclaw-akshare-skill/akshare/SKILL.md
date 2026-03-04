---
name: akshare
description: Chinese financial data access using AkShare library. Fetch real-time and historical data for A-shares, Hong Kong stocks, US stocks, futures, funds, and macroeconomic indicators. Use when user requests Chinese market data, stock prices, market analysis, or financial information from Chinese exchanges. Supports stock quotes, historical data, futures market data, fund information, macroeconomic indicators, and real-time market updates.
---

# AkShare - Chinese Financial Data

## Overview

AkShare is a free, open-source Python library for accessing Chinese financial market data. This skill provides guidance for fetching data from Chinese exchanges including Shanghai Stock Exchange, Shenzhen Stock Exchange, Hong Kong Exchange, and more.

## Quick Start

Install AkShare:
```bash
pip install akshare
```

Basic stock quote:
```python
import akshare as ak
df = ak.stock_zh_a_spot_em()  # Real-time A-share data
```

## Stock Data

### A-Shares (A股)

**Real-time quotes:**
```python
# All A-shares real-time data
df = ak.stock_zh_a_spot_em()

# Single stock real-time quote
df = ak.stock_zh_a_spot()
```

**Historical data:**
```python
# Historical daily data
df = ak.stock_zh_a_hist(symbol="000001", period="daily", start_date="20240101", end_date="20241231", adjust="qfq")
```

**Stock list:**
```python
# Get all A-share stock list
df = ak.stock_info_a_code_name()
```

### Hong Kong Stocks (港股)

**Real-time quotes:**
```python
df = ak.stock_hk_spot_em()
```

**Historical data:**
```python
df = ak.stock_hk_hist(symbol="00700", period="daily", adjust="qfq")
```

### US Stocks (美股)

**Real-time data:**
```python
df = ak.stock_us_spot_em()
```

## Futures Data (期货)

**Real-time futures:**
```python
# Commodity futures
df = ak.futures_zh_spot()
```

**Historical futures:**
```python
df = ak.futures_zh_hist_sina(symbol="IF0")
```

## Fund Data (基金)

**Fund list:**
```python
df = ak.fund_open_fund_info_em()
```

**Fund historical data:**
```python
df = ak.fund_open_fund_info_em(fund="000001", indicator="单位净值走势")
```

## Macroeconomic Indicators (宏观)

**GDP data:**
```python
df = ak.macro_china_gdp()
```

**CPI data:**
```python
df = ak.macro_china_cpi()
```

**PMI data:**
```python
df = ak.macro_china_pmi()
```

## Common Parameters

**Period (周期):**
- `daily` - 日线
- `weekly` - 周线
- `monthly` - 月线

**Adjustment (复权):**
- `qfq` - 前复权
- `hfq` - 后复权
- `""` - 不复权

## Tips

1. **Data caching**: AkShare doesn't cache data, implement your own caching if needed
2. **Rate limiting**: Be mindful of request frequency to avoid being blocked
3. **Data format**: Returns pandas DataFrame, can be easily processed
4. **Error handling**: Network errors may occur, implement retry logic

## References

For complete API documentation and advanced usage, see:
- [references/akshare_api.md](references/akshare_api.md) - Detailed API reference
- [references/common_functions.md](references/common_functions.md) - Commonly used functions
- [https://akshare.akfamily.xyz/](https://akshare.akfamily.xyz/) - Official documentation