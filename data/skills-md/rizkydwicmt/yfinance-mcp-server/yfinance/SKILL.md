---
name: yfinance
description: Access Yahoo Finance data — stock prices, history, financials, options, dividends, news, and market screeners
---

# YFinance MCP Server

Access real-time and historical financial data from Yahoo Finance. This MCP server provides 12 tools covering stock prices, company fundamentals, analyst recommendations, options chains, dividends, market movers, and news.

## Available Tools

### Stock Data (7 tools)

#### `tool_get_stock_price` — Current Price & Trading Metrics
```
tool_get_stock_price(symbol: "AAPL")
tool_get_stock_price(symbol: "BBCA.JK")
```
Returns: current price, change %, open, day high/low, volume, 52-week range, market cap, P/E, dividend yield, direction (▲/▼).

#### `tool_get_stock_info` — Company Details
```
tool_get_stock_info(symbol: "MSFT")
```
Returns: sector, industry, full name, market cap, P/E, P/B, profit margins, revenue growth, analyst price targets, business description.

#### `tool_get_history` — Historical OHLCV Data
```
tool_get_history(symbol: "AAPL", period: "1mo", interval: "1d")
tool_get_history(symbol: "BBCA.JK", period: "1y", interval: "1wk")
tool_get_history(symbol: "BTC-USD", period: "5y", interval: "1mo")
```
- **period**: `1d`, `5d`, `1mo`, `3mo`, `6mo`, `1y`, `2y`, `5y`, `10y`, `ytd`, `max`
- **interval**: `1m`, `2m`, `5m`, `15m`, `30m`, `60m`, `90m`, `1h`, `1d`, `5d`, `1wk`, `1mo`, `3mo`

#### `tool_get_financials` — Financial Statements
```
tool_get_financials(symbol: "AAPL", statement_type: "income", quarterly: false)
tool_get_financials(symbol: "MSFT", statement_type: "balance_sheet", quarterly: true)
tool_get_financials(symbol: "GOOG", statement_type: "all")
```
- **statement_type**: `income`, `balance_sheet`, `cash_flow`, `all`

#### `tool_get_recommendations` — Analyst Ratings
```
tool_get_recommendations(symbol: "TSLA")
```
Returns: recommendation trends (strongBuy, buy, hold, sell, strongSell), price targets (low, mean, median, high), and recent upgrades/downgrades.

#### `tool_get_options` — Options Chain
```
tool_get_options(symbol: "AAPL")
tool_get_options(symbol: "TSLA", expiration: "2025-03-21")
```
Returns: calls and puts with strike, last price, bid, ask, volume, open interest, implied volatility. Lists available expiration dates.

#### `tool_get_dividends` — Dividend History
```
tool_get_dividends(symbol: "JNJ")
tool_get_dividends(symbol: "BBCA.JK")
```
Returns: current yield, ex-date, payment rate, and historical dividend payments.

---

### Market Analysis (3 tools)

#### `tool_compare_stocks` — Side-by-Side Comparison
```
tool_compare_stocks(symbols: "AAPL,MSFT,GOOG")
tool_compare_stocks(symbols: "BBCA.JK BBRI.JK BMRI.JK")
```
Compares up to 10 stocks on: price, change %, market cap, P/E, dividend yield, margins, revenue growth, analyst rating. Symbols can be comma or space separated.

#### `tool_get_market_movers` — Top Movers
```
tool_get_market_movers(mover_type: "gainers")
tool_get_market_movers(mover_type: "losers")
tool_get_market_movers(mover_type: "most_active")
```

#### `tool_screen_stocks` — Stock Screener
```
tool_screen_stocks(sector: "Technology", min_market_cap: 1000000000)
tool_screen_stocks(max_pe_ratio: 15, min_dividend_yield: 0.03)
tool_screen_stocks(sector: "Healthcare", exchange: "NMS")
```
All filters are optional and combinable:
- **sector**: `Technology`, `Healthcare`, `Financial Services`, `Energy`, etc.
- **min_market_cap**: in USD (e.g., `1000000000` = $1B)
- **max_pe_ratio**: max trailing P/E (e.g., `25`)
- **min_dividend_yield**: as decimal (e.g., `0.03` = 3%)
- **exchange**: `NMS` (NASDAQ), `NYQ` (NYSE), etc.

---

### Search & News (2 tools)

#### `tool_search_stocks` — Find Tickers
```
tool_search_stocks(query: "Apple", max_results: 5)
tool_search_stocks(query: "semiconductor ETF")
tool_search_stocks(query: "bank indonesia")
```
Searches stocks, ETFs, mutual funds, indices by name, ticker, or keyword.

#### `tool_get_news` — Latest News
```
tool_get_news(symbol: "AAPL", max_items: 5)
tool_get_news(symbol: "TSLA")
```
Returns: title, publisher, link, publish time, and thumbnail for each article.

---

## Supported Markets

This server works with **any ticker supported by Yahoo Finance**:

| Market | Examples |
|--------|----------|
| US Stocks | AAPL, MSFT, GOOG, TSLA, AMZN |
| Indonesia (IDX) | BBCA.JK, BBRI.JK, TLKM.JK, BMRI.JK |
| Japan (TSE) | 7203.T (Toyota), 6758.T (Sony) |
| UK (LSE) | SHEL.L, AZN.L, HSBA.L |
| Hong Kong (HKEX) | 0700.HK (Tencent), 9988.HK (Alibaba) |
| ETFs | SPY, QQQ, VTI, VOO, ARKK |
| Crypto | BTC-USD, ETH-USD, SOL-USD |
| Indices | ^GSPC (S&P 500), ^IXIC (NASDAQ), ^JKSE (IDX) |
| Forex | USDIDR=X, EURUSD=X, GBPUSD=X |

## Common Usage Patterns

### Investment Research
1. `tool_search_stocks` → find the ticker
2. `tool_get_stock_info` → understand the company
3. `tool_get_financials` → analyze fundamentals
4. `tool_get_recommendations` → check analyst sentiment
5. `tool_get_history` → review price trends

### Portfolio Monitoring
1. `tool_compare_stocks` → compare your holdings
2. `tool_get_stock_price` → check current prices
3. `tool_get_news` → stay updated on each position

### Market Discovery
1. `tool_get_market_movers` → find trending stocks
2. `tool_screen_stocks` → filter by criteria
3. `tool_get_stock_info` → deep dive on candidates

---

## Installation

### Quick Install (install.sh)

The included `install.sh` automates everything — uv setup, Python 3.12 venv, package install, mcporter config, and OpenClaw skill registration:

```bash
# Clone the repository on your server
git clone https://github.com/rizkydwicmt/yfinance-mcp-server.git
cd yfinance-mcp-server

# Run the installer
chmod +x install.sh
./install.sh
```

The installer will:
1. ✅ Check for `pyproject.toml` in the project directory
2. ✅ Install `uv` if not already present
3. ✅ Create a Python 3.12 virtual environment
4. ✅ Install `yfinance-mcp-server` + all dependencies
5. ✅ Verify all 12 tools load correctly
6. ✅ Add `yfinance` to your mcporter config (auto-detected)
7. ✅ Install `SKILL.md` to OpenClaw skills directory

### Environment Variables

Customize the installer behavior with environment variables:

```bash
# Change project location
YFINANCE_PROJECT_DIR=/opt/mcp/yfinance ./install.sh

# Use a different Python version
YFINANCE_PYTHON_VERSION=3.11 ./install.sh

# Custom venv location
YFINANCE_VENV_DIR=/opt/venvs/yfinance ./install.sh

# Specify mcporter config path
MCPORTER_CONFIG=/etc/clawd/mcporter.json ./install.sh

# Custom OpenClaw directory
CLAWD_DIR=/opt/clawd ./install.sh

# Skip mcporter / skill steps
SKIP_MCPORTER=true ./install.sh
SKIP_SKILL=true ./install.sh
```

### Manual Install

```bash
# 1. Clone repository
git clone https://github.com/rizkydwicmt/yfinance-mcp-server.git
cd yfinance-mcp-server

# 2. Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# 3. Create venv + install
uv venv .venv --python 3.12
uv pip install -e . --python .venv/bin/python

# 4. Add to mcporter.json
# {"mcpServers": {"yfinance": {"command": "/path/to/.venv/bin/yfin-mcp"}}}

# 5. Install skill
mkdir -p ${CLAWD_DIR}/skills/yfinance
cp SKILL.md ${CLAWD_DIR}/skills/yfinance/SKILL.md
```

### Verify

```bash
# Check tools load
mcporter --config ${CLAWD_DIR}/config/mcporter.json list yfinance --schema

# Live test
mcporter --config ${CLAWD_DIR}/config/mcporter.json call yfinance.tool_get_stock_price symbol=AAPL
```
