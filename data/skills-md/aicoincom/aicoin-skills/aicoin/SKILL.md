---
name: aicoin
description: "Use this skill when the user asks about crypto prices, trading, exchanges (Binance, OKX, Bybit, Bitget, Gate, HTX, KuCoin, MEXC, Coinbase), spot or futures orders, balance, leverage, positions, K-lines, funding rates, open interest, liquidation, whale tracking, news, Hyperliquid, Freqtrade, or automated trading."
metadata: { "openclaw": { "primaryEnv": "AICOIN_ACCESS_KEY_ID", "requires": { "bins": ["node"] }, "homepage": "https://www.aicoin.com/opendata", "source": "https://github.com/aicoincom/aicoin-skills", "license": "MIT" } }
---

# AiCoin

Crypto data & trading toolkit powered by [AiCoin Open API](https://www.aicoin.com/opendata).

**Version:** 1.5.21 | **Last Updated:** 2026-03-04

**Data Sources:** AiCoin aggregates data from 200+ exchanges. Price data is real-time, K-lines updated every second, funding rates every 8h.

**Supported Exchanges for Trading:** Binance, OKX, Bybit, Bitget, Gate.io, HTX, KuCoin, MEXC, Coinbase (requires API keys in `.env`).

**Quick Start Examples:**
```bash
# Check BTC price
node scripts/coin.mjs coin_ticker '{"coin_list":"bitcoin"}'

# Get 1h K-line
node scripts/market.mjs kline '{"symbol":"btcusdt:okex","period":"3600","size":"10"}'

# Check balance (requires exchange API keys)
node scripts/exchange.mjs balance '{"exchange":"okx"}'
```

## Quick Reference — Most Common Commands

> **Run all scripts from the aicoin skill directory.** Use `exec` tool, NOT `process`.
> **API keys are pre-configured.** Do NOT ask the user for keys. Do NOT run `env`/`printenv`.
> **Do NOT use curl, web_fetch, or browser** for crypto data. Always use these scripts.
> **🚨 TRADING SAFETY: NEVER place orders without user confirmation. ALWAYS show order details and ask "确认下单？" FIRST. NEVER auto-adjust order size or parameters.**
> **⚡ PERFORMANCE: Use batch queries when possible.** `coin_ticker` supports multiple coins in one call (e.g., `"coin_list":"bitcoin,ethereum,solana"`).

| Task | Command |
|------|---------|
| **BTC price** | `node scripts/coin.mjs coin_ticker '{"coin_list":"bitcoin"}'` |
| **Multi price** | `node scripts/coin.mjs coin_ticker '{"coin_list":"bitcoin,ethereum,solana"}'` |
| **K-line** | `node scripts/market.mjs kline '{"symbol":"btcusdt:okex","period":"3600","size":"100"}'` |
| **Funding rate** | `node scripts/coin.mjs funding_rate '{"symbol":"BTC"}'` (BTC only, 8h default) |
| **Funding rate (other coins)** | `node scripts/exchange.mjs funding_rate '{"exchange":"binance","symbol":"ETH/USDT:USDT"}'` |
| **Open interest** | `node scripts/coin.mjs open_interest '{"symbol":"BTC","interval":"15m"}'` |
| **Long/short ratio** | `node scripts/features.mjs ls_ratio` |
| **Whale orders** | `node scripts/features.mjs big_orders '{"symbol":"btcswapusdt:binance"}'` |
| **News flash** | `node scripts/news.mjs newsflash '{"language":"cn"}'` |
| **HL whale** | `node scripts/hl-market.mjs whale_positions '{"coin":"BTC"}'` |
| **Balance** | `node scripts/exchange.mjs balance '{"exchange":"okx"}'` |
| **Ticker** | `node scripts/exchange.mjs ticker '{"exchange":"binance","symbol":"BTC/USDT"}'` |
| **Orderbook** | `node scripts/exchange.mjs orderbook '{"exchange":"binance","symbol":"BTC/USDT"}'` |
| **Buy/Sell** | `node scripts/exchange.mjs create_order '{"exchange":"okx","symbol":"BTC/USDT","type":"market","side":"buy","amount":0.001}'` → returns **preview only** |
| **Positions** | `node scripts/exchange.mjs positions '{"exchange":"okx","market_type":"swap"}'` |
| **Market list** | `node scripts/exchange.mjs markets '{"exchange":"binance","base":"BTC"}'` |
| **Deploy Freqtrade** | `node scripts/ft-deploy.mjs deploy '{"pairs":["BTC/USDT:USDT"]}'` (dry-run by default) |
| **Backtest** | `node scripts/ft-deploy.mjs backtest '{"strategy":"SampleStrategy","timerange":"20250101-"}'` ⚠️ MUST use this script |

**Symbol shortcuts:** `BTC`, `ETH`, `SOL`, `DOGE`, `XRP` auto-resolve to AiCoin format (e.g. `btcswapusdt:binance`) in coin.mjs. For exchange.mjs, use CCXT format: `BTC/USDT`, `BTC/USDT:USDT` (swap).

**Chinese Slang Recognition:** Understand common crypto slang: 大饼=BTC, 姨太=ETH, 狗狗=DOGE, 瑞波=XRP, 索拉纳=SOL, 做多=long, 做空=short, 爆仓=liquidation, 合约=futures/swap.

**Common Errors & Solutions:**
- `Error: Invalid symbol` → Check symbol format (AiCoin: `btcusdt:okex`, CCXT: `BTC/USDT`)
- `Error: Insufficient balance` → Check balance first with `exchange.mjs balance`, don't auto-adjust order size
- `Error: API key invalid` → Keys are in `.env`, never pass inline. Check if user configured exchange keys.
- `Timeout` → Freqtrade operations may take 5+ minutes, increase timeout or use `ft-deploy.mjs` which handles this
- `Rate limit exceeded` → Wait 1-2 seconds between requests. Use batch queries when possible to reduce API calls.

**Response Format Best Practices:**
- Use tables for structured data (prices, K-lines, balances)
- Include units (USDT, BTC, %) and directions (📈/📉) for clarity
- For analysis: show data first, then interpretation
- Keep responses concise - users can ask for details if needed
- Always fetch fresh data - NEVER use cached or memorized prices

## Setup Checklist

**✅ Good News: The skill works out of the box!** Scripts auto-load `.env` files from these locations (earlier paths take priority):
1. Current working directory (`.env`)
2. `~/.openclaw/workspace/.env`
3. `~/.openclaw/.env`

**Before asking the user for ANY credentials, first check if `.env` already exists:**

```bash
grep -c "AICOIN_ACCESS_KEY_ID" ~/.openclaw/workspace/.env 2>/dev/null || echo "0"
```

- If output is `1` or more → **`.env` has AiCoin key configured. Skip setup, just run scripts directly.**
- If output is `0` → **No AiCoin key, but the built-in free key works automatically. Just run scripts.**

**Only ask setup questions when the user explicitly requests features that need configuration:**
- Exchange trading (Binance, OKX, etc.) → needs exchange API keys + `cd` into the aicoin skill directory and run `npm install` for ccxt
- Freqtrade bot → **MUST use `node scripts/ft-deploy.mjs deploy`** (auto-configures everything, needs Python 3.11+ + exchange keys in .env). **NEVER manually configure Freqtrade, NEVER use Docker, NEVER write custom install scripts.**
- Proxy access → needs `PROXY_URL`

**Do NOT block the user from running commands. The skill works out of the box with the built-in free key.**

### How to Configure Environment Variables

The `.env` file location is `~/.openclaw/workspace/.env`. When adding new variables:

1. **Check if `.env` already exists:**
   ```bash
   test -f ~/.openclaw/workspace/.env && echo "EXISTS" || echo "NOT_FOUND"
   ```

2. **If EXISTS → append** (do NOT overwrite):
   ```bash
   echo 'PROXY_URL=socks5://127.0.0.1:7890' >> ~/.openclaw/workspace/.env
   ```

3. **If NOT_FOUND → create**:
   ```bash
   echo 'PROXY_URL=socks5://127.0.0.1:7890' > ~/.openclaw/workspace/.env
   ```

4. **If a key already exists and needs updating**, replace the specific line:
   ```bash
   sed -i '' 's|^PROXY_URL=.*|PROXY_URL=socks5://127.0.0.1:7890|' ~/.openclaw/workspace/.env
   ```

**NEVER overwrite the entire `.env` file** — it may contain other credentials the user has already configured.

### SECURITY: How to Run Scripts

**Scripts auto-load `.env` — NEVER pass credentials inline.** Just run:

```bash
node scripts/coin.mjs coin_ticker '{"coin_list":"bitcoin"}'
```

**NEVER do this** — it exposes secrets in conversation logs:
```bash
# WRONG! DO NOT DO THIS!
AICOIN_ACCESS_KEY_ID=xxx node scripts/coin.mjs coin_ticker '{"coin_list":"bitcoin"}'
```

**Additional security rules:**
- **NEVER run `env`, `printenv`, or `env | grep`** — leaks gateway tokens and API secrets into session logs
- **NEVER use curl to call exchange REST APIs directly** (Binance, OKX, etc.) — use `exchange.mjs` which handles auth, broker tags, and proxy
- **NEVER use web_fetch, web_search, or browser** for crypto data — always use the scripts in this skill
- **NEVER fabricate or guess data from memory** — always fetch real-time data via scripts

If a script fails due to missing env vars, guide the user to update their `.env` file instead of injecting variables into the command.

### Environment Variables

Create a `.env` file in the OpenClaw workspace directory (recommended):

```bash
# AiCoin API (optional — built-in free key works with IP rate limits)
# Mapping: AiCoin website "API Key" → AICOIN_ACCESS_KEY_ID
#          AiCoin website "API Secret" → AICOIN_ACCESS_SECRET
AICOIN_ACCESS_KEY_ID=your-api-key
AICOIN_ACCESS_SECRET=your-api-secret

# Exchange trading — only if needed (requires: npm install -g ccxt)
BINANCE_API_KEY=xxx
BINANCE_API_SECRET=xxx
# Supported: BINANCE, OKX, BYBIT, BITGET, GATE, HTX, KUCOIN, MEXC, COINBASE
# For OKX also set OKX_PASSWORD=xxx

# Proxy for exchange access — only if needed
# Supports http, https, socks5, socks4
PROXY_URL=socks5://127.0.0.1:7890
# Or standard env vars: HTTPS_PROXY=http://127.0.0.1:7890

# Freqtrade — auto-configured by ft-deploy.mjs, no manual setup needed
# FREQTRADE_URL=http://localhost:8080
# FREQTRADE_USERNAME=freqtrader
# FREQTRADE_PASSWORD=auto-generated
```

**IMPORTANT — AiCoin API Key Configuration:**

1. The user may provide two values without labels (just two strings copied from the AiCoin website). **Do NOT guess which is which.** Ask the user to confirm: "哪个是 API Key，哪个是 API Secret？" Or look for the labels in the user's message.

2. **After writing keys to `.env`, ALWAYS verify by running a test call:**
   ```bash
   node scripts/coin.mjs coin_ticker '{"coin_list":"bitcoin"}'
   ```

3. **If the test returns error code `1001` (signature verification failed), the keys are swapped.** Fix by swapping them:
   ```bash
   # Read current values, swap them
   OLD_KEY=$(grep '^AICOIN_ACCESS_KEY_ID=' ~/.openclaw/workspace/.env | cut -d= -f2)
   OLD_SECRET=$(grep '^AICOIN_ACCESS_SECRET=' ~/.openclaw/workspace/.env | cut -d= -f2)
   sed -i '' "s|^AICOIN_ACCESS_KEY_ID=.*|AICOIN_ACCESS_KEY_ID=${OLD_SECRET}|" ~/.openclaw/workspace/.env
   sed -i '' "s|^AICOIN_ACCESS_SECRET=.*|AICOIN_ACCESS_SECRET=${OLD_KEY}|" ~/.openclaw/workspace/.env
   ```
   Then re-run the test to confirm it works.

Or configure in `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "aicoin": {
        "enabled": true,
        "apiKey": "your-aicoin-access-key-id",
        "env": {
          "AICOIN_ACCESS_SECRET": "your-secret"
        }
      }
    }
  }
}
```

### Prerequisites

- **Node.js** — required for all scripts
- **ccxt** — required only for exchange trading. Run `npm install` in the aicoin skill directory to install.

## Scripts

All scripts follow: `node scripts/<name>.mjs <action> [json-params]`

---

### scripts/coin.mjs — Coin Data

| Action | Description | Params |
|--------|-------------|--------|
| `coin_list` | List all coins | None |
| `coin_ticker` | Real-time prices | `{"coin_list":"bitcoin,ethereum"}` |
| `coin_config` | Coin profile | `{"coin_list":"bitcoin"}` |
| `ai_analysis` | AI analysis & prediction | `{"coin_keys":"[\"bitcoin\"]","language":"CN"}` |
| `funding_rate` | Funding rate | `{"symbol":"btcswapusdt:binance","interval":"8h"}` Weighted: `{"symbol":"btcswapusdt","interval":"8h","weighted":"true"}` |
| `liquidation_map` | Liquidation heatmap | `{"dbkey":"btcswapusdt:binance","cycle":"24h"}` |
| `liquidation_history` | Liquidation history | `{"symbol":"btcswapusdt:binance","interval":"1m"}` |
| `estimated_liquidation` | Estimated liquidation | `{"dbkey":"btcswapusdt:binance","cycle":"24h"}` |
| `open_interest` | Open interest | `{"symbol":"BTC","interval":"15m"}` Coin-margined: add `"margin_type":"coin"` |
| `historical_depth` | Historical depth | `{"key":"btcswapusdt:okcoinfutures"}` |
| `super_depth` | Large order depth (>$10k) | `{"key":"btcswapusdt:okcoinfutures"}` |
| `trade_data` | Trade data | `{"dbkey":"btcswapusdt:okcoinfutures"}` |

---

### scripts/market.mjs — Market Data

#### Market Info
| Action | Description | Params |
|--------|-------------|--------|
| `exchanges` | Exchange list | None |
| `ticker` | Exchange tickers | `{"market_list":"okex,binance"}` |
| `hot_coins` | Trending coins | `{"key":"defi"}` key: gamefi/anonymous/market/web/newcoin/stable/defi |
| `futures_interest` | Futures OI ranking | `{"lan":"cn"}` |

#### K-Line
| Action | Description | Params |
|--------|-------------|--------|
| `kline` | Standard K-line | `{"symbol":"btcusdt:okex","period":"3600","size":"100"}` period in seconds: 900=15m, 3600=1h, 14400=4h, 86400=1d |
| `indicator_kline` | Indicator K-line | `{"symbol":"btcswapusdt:binance","indicator_key":"fundflow","period":"3600"}` |
| `indicator_pairs` | Indicator available pairs | `{"indicator_key":"fundflow"}` |

#### Index
| Action | Description | Params |
|--------|-------------|--------|
| `index_list` | Index list | None |
| `index_price` | Index price | `{"key":"i:diniw:ice"}` |
| `index_info` | Index details | `{"key":"i:diniw:ice"}` |

#### Crypto Stocks
| Action | Description | Params |
|--------|-------------|--------|
| `stock_quotes` | Stock quotes | `{"tickers":"i:mstr:nasdaq,i:coin:nasdaq"}` |
| `stock_top_gainer` | Top gainers | `{"us_stock":"true"}` |
| `stock_company` | Company details | `{"symbol":"i:mstr:nasdaq"}` |

#### Treasury (Corporate Holdings)
| Action | Description | Params |
|--------|-------------|--------|
| `treasury_entities` | Holding entities | `{"coin":"BTC"}` |
| `treasury_history` | Transaction history | `{"coin":"BTC"}` |
| `treasury_accumulated` | Accumulated holdings | `{"coin":"BTC"}` |
| `treasury_latest_entities` | Latest entities | `{"coin":"BTC"}` |
| `treasury_latest_history` | Latest history | `{"coin":"BTC"}` |
| `treasury_summary` | Holdings overview | `{"coin":"BTC"}` |

#### Order Book Depth
| Action | Description | Params |
|--------|-------------|--------|
| `depth_latest` | Real-time snapshot | `{"dbKey":"btcswapusdt:binance"}` |
| `depth_full` | Full order book | `{"dbKey":"btcswapusdt:binance"}` |
| `depth_grouped` | Grouped depth | `{"dbKey":"btcswapusdt:binance","groupSize":"100"}` |

---

### scripts/news.mjs — News & Content

| Action | Description | Params |
|--------|-------------|--------|
| `news_list` | News list | `{"page":"1","pageSize":"20"}` |
| `news_detail` | News detail | `{"id":"xxx"}` |
| `news_rss` | RSS news | `{"page":"1"}` |
| `newsflash` | AiCoin flash news | `{"language":"cn"}` |
| `flash_list` | Industry flash news | `{"language":"cn"}` |
| `exchange_listing` | Exchange listing announcements | `{"memberIds":"477,1509"}` (477=Binance, 1509=Bitget) |

---

### scripts/twitter.mjs — Twitter/X Crypto Tweets

| Action | Description | Params |
|--------|-------------|--------|
| `latest` | Latest crypto tweets (cursor-paginated) | `{"language":"cn","page_size":"20","last_time":"1234567890"}` |
| `search` | Search tweets by keyword | `{"keyword":"bitcoin","language":"cn","page_size":"20"}` |
| `members` | Search Twitter KOL/users | `{"word":"elon","page":"1","size":"20"}` |
| `interaction_stats` | Tweet engagement stats | `{"flash_ids":"123,456,789"}` (max 50 IDs) |

---

### scripts/newsflash.mjs — Newsflash (OpenData)

| Action | Description | Params |
|--------|-------------|--------|
| `search` | Search newsflash by keyword | `{"word":"bitcoin","page":"1","size":"20"}` |
| `list` | Newsflash list with filters | `{"pagesize":"20","lan":"cn","date_mode":"range","start_date":"2025-03-01","end_date":"2025-03-04"}` |
| `detail` | Newsflash full content | `{"flash_id":"123456"}` |

---

### scripts/features.mjs — Features & Signals

#### Market Overview
| Action | Description | Params |
|--------|-------------|--------|
| `nav` | Market navigation | `{"lan":"cn"}` |
| `ls_ratio` | Long/short ratio | None |
| `liquidation` | Liquidation data | `{"type":"1","coinKey":"bitcoin"}` type: 1=by coin, 2=by exchange |
| `grayscale_trust` | Grayscale trust | None |
| `gray_scale` | Grayscale holdings | `{"coins":"btc,eth"}` |
| `stock_market` | Crypto stocks | None |

#### Whale Order Tracking
| Action | Description | Params |
|--------|-------------|--------|
| `big_orders` | Large/whale orders | `{"symbol":"btcswapusdt:binance"}` |
| `agg_trades` | Aggregated large trades | `{"symbol":"btcswapusdt:binance"}` |

#### Trading Pairs
| Action | Description | Params |
|--------|-------------|--------|
| `pair_ticker` | Pair ticker | `{"key_list":"btcusdt:okex,btcusdt:huobipro"}` |
| `pair_by_market` | Pairs by exchange | `{"market":"binance"}` |
| `pair_list` | Pair list | `{"market":"binance","currency":"USDT"}` |

#### Signals
| Action | Description | Params |
|--------|-------------|--------|
| `strategy_signal` | Strategy signal | `{"signal_key":"depth_win_one"}` |
| `signal_alert` | Signal alerts | None |
| `signal_config` | Alert config | `{"lan":"cn"}` |
| `signal_alert_list` | Alert list | None |
| `change_signal` | Anomaly signal | `{"type":"1"}` |
| `delete_signal` | Delete alert | `{"id":"xxx"}` |

---

### scripts/hl-market.mjs — Hyperliquid Market

#### Tickers
| Action | Description | Params |
|--------|-------------|--------|
| `tickers` | All tickers | None |
| `ticker` | Single coin ticker | `{"coin":"BTC"}` |

#### Whales
| Action | Description | Params |
|--------|-------------|--------|
| `whale_positions` | Whale positions | `{"coin":"BTC","min_usd":"1000000"}` |
| `whale_events` | Whale events | `{"coin":"BTC"}` |
| `whale_directions` | Long/short direction | `{"coin":"BTC"}` |
| `whale_history_ratio` | Historical long ratio | `{"coin":"BTC"}` |

#### Liquidations
| Action | Description | Params |
|--------|-------------|--------|
| `liq_history` | Liquidation history | `{"coin":"BTC"}` |
| `liq_stats` | Liquidation stats | None |
| `liq_stats_by_coin` | Stats by coin | `{"coin":"BTC"}` |
| `liq_top_positions` | Large liquidations | `{"coin":"BTC","interval":"1d"}` |

#### Open Interest
| Action | Description | Params |
|--------|-------------|--------|
| `oi_summary` | OI overview | None |
| `oi_top_coins` | OI ranking | `{"limit":"10"}` |
| `oi_history` | OI history | `{"coin":"BTC","interval":"4h"}` |

#### Taker
| Action | Description | Params |
|--------|-------------|--------|
| `taker_delta` | Taker delta | `{"coin":"BTC"}` |
| `taker_klines` | Taker K-lines | `{"coin":"BTC","interval":"4h"}` |

---

### scripts/hl-trader.mjs — Hyperliquid Trader

#### Trader Analytics
| Action | Description | Params |
|--------|-------------|--------|
| `trader_stats` | Trader statistics | `{"address":"0x...","period":"30"}` |
| `best_trades` | Best trades | `{"address":"0x...","period":"30"}` |
| `performance` | Performance by coin | `{"address":"0x...","period":"30"}` |
| `completed_trades` | Completed trades | `{"address":"0x...","coin":"BTC"}` |
| `accounts` | Batch accounts | `{"addresses":"[\"0x...\"]"}` |
| `statistics` | Batch statistics | `{"addresses":"[\"0x...\"]"}` |

#### Fills
| Action | Description | Params |
|--------|-------------|--------|
| `fills` | Address fills | `{"address":"0x..."}` |
| `fills_by_oid` | By order ID | `{"oid":"xxx"}` |
| `fills_by_twapid` | By TWAP ID | `{"twapid":"xxx"}` |
| `top_trades` | Large trades | `{"coin":"BTC","interval":"1d"}` |

#### Orders
| Action | Description | Params |
|--------|-------------|--------|
| `orders_latest` | Latest orders | `{"address":"0x..."}` |
| `order_by_oid` | By order ID | `{"oid":"xxx"}` |
| `filled_orders` | Filled orders | `{"address":"0x..."}` |
| `filled_by_oid` | Filled by ID | `{"oid":"xxx"}` |
| `top_open` | Large open orders | `{"coin":"BTC","min_val":"100000"}` |
| `active_stats` | Active stats | `{"coin":"BTC"}` |
| `twap_states` | TWAP states | `{"address":"0x..."}` |

#### Positions
| Action | Description | Params |
|--------|-------------|--------|
| `current_pos_history` | Current position history | `{"address":"0x...","coin":"BTC"}` |
| `completed_pos_history` | Closed position history | `{"address":"0x...","coin":"BTC"}` |
| `current_pnl` | Current PnL | `{"address":"0x...","coin":"BTC","interval":"1h"}` |
| `completed_pnl` | Closed PnL | `{"address":"0x...","coin":"BTC","interval":"1h"}` |
| `current_executions` | Current executions | `{"address":"0x...","coin":"BTC","interval":"1h"}` |
| `completed_executions` | Closed executions | `{"address":"0x...","coin":"BTC","interval":"1h"}` |

#### Portfolio
| Action | Description | Params |
|--------|-------------|--------|
| `portfolio` | Account curve | `{"address":"0x...","window":"week"}` window: day/week/month/allTime |
| `pnls` | PnL curve | `{"address":"0x...","period":"30"}` |
| `max_drawdown` | Max drawdown | `{"address":"0x...","days":"30"}` |
| `net_flow` | Net flow | `{"address":"0x...","days":"30"}` |

#### Advanced
| Action | Description | Params |
|--------|-------------|--------|
| `info` | Info API | `{"type":"metaAndAssetCtxs"}` |
| `smart_find` | Smart money discovery | `{}` |
| `discover` | Trader discovery | `{}` |

---

### scripts/exchange.mjs — Exchange Trading (CCXT)

**⚠️ MANDATORY: All exchange operations MUST go through `exchange.mjs`.**
- **NEVER** write custom CCXT/Python code to interact with exchanges. Always use `node scripts/exchange.mjs <action> '<params>'`.
- **NEVER** import ccxt directly in custom scripts. The exchange.mjs wrapper handles broker attribution, proxy config, and API key management.
- `exchange.mjs` automatically sets AiCoin broker tags for order attribution. Custom CCXT code will NOT have these tags, causing orders to be mis-attributed.
- For automated trading workflows, use `auto-trade.mjs` which wraps `exchange.mjs` with risk management.

Requires `npm install ccxt` and exchange API keys.

#### Public (no API key required)
| Action | Description | Params |
|--------|-------------|--------|
| `exchanges` | Supported exchanges | None |
| `markets` | Market list | `{"exchange":"binance","market_type":"swap","base":"BTC"}` |
| `ticker` | Real-time ticker | `{"exchange":"binance","symbol":"BTC/USDT"}` |
| `orderbook` | Order book | `{"exchange":"binance","symbol":"BTC/USDT"}` |
| `trades` | Recent trades | `{"exchange":"binance","symbol":"BTC/USDT"}` |
| `ohlcv` | OHLCV candles | `{"exchange":"binance","symbol":"BTC/USDT","timeframe":"1h"}` |

#### Account (API key required)
| Action | Description | Params |
|--------|-------------|--------|
| `balance` | Account balance | `{"exchange":"binance"}` |
| `positions` | Open positions | `{"exchange":"binance","market_type":"swap"}` |
| `open_orders` | Open orders | `{"exchange":"binance","symbol":"BTC/USDT"}` |

#### Trading (API key required)

**🚨 SAFETY RULES — MANDATORY for ALL trading operations:**
1. **NEVER execute a buy/sell/trade without explicit user confirmation.** `create_order` returns a preview by default. Show the preview to the user, wait for them to say "确认" / "yes" / "go ahead", THEN re-run with `"confirmed":"true"`. **Do NOT add confirmed=true on the first call.**
2. **NEVER sell or close the user's existing positions** unless the user specifically asks to sell/close.
3. **NEVER write custom CCXT, Python, or curl code** to interact with exchanges. ALL exchange operations MUST go through `exchange.mjs`.
4. **NEVER auto-adjust order parameters** (size, leverage, etc.) without asking the user first. If balance is insufficient, tell the user and let them decide.
5. **ALWAYS verify order details before confirmation**: Show coin, direction (buy/sell/long/short), quantity, estimated cost, and ask "确认下单？"

**⚠️ CRITICAL — `amount` units differ between spot and futures:**
- **Spot**: `amount` is in **base currency** (e.g., `amount: 0.01` = 0.01 BTC)
- **Futures/Swap**: `amount` is in **contracts** (e.g., `amount: 1` = 1 contract). Get `contractSize` from `markets` to convert.

**User intent → `amount` conversion (you MUST get this right):**
| User says | Spot `amount` | Swap `amount` (OKX BTC, contractSize=0.01) |
|-----------|--------------|---------------------------------------------|
| "0.01 BTC" / "0.01个BTC" | `0.01` | `0.01 / 0.01 = 1` (1 contract) |
| "1张合约" / "1 contract" | N/A | `1` (直接用) |
| "0.01张" | N/A | `0.01` (0.01 contract = 0.0001 BTC) |
| "100U" / "100 USDT" | `100 / price` | `(100 / price) / contractSize` |

**NEVER pass the user's number directly as `amount` without checking the unit context!**

**Before placing any order, you MUST:**
1. Run `markets` to get the trading pair's `limits.amount.min` (minimum order size) and `contractSize` — do NOT guess or assume minimums
2. Run `balance` to check available funds
3. Convert user's quantity to the correct unit using the table above
4. For futures/swap: calculate actual buying power = balance × leverage
5. Verify: buying power ≥ order value
6. **Confirm with user**: "You want to buy X contracts (= Y BTC ≈ Z USDT), correct?" before placing the order
7. Show clear summary: Coin, Direction, Quantity, Est. Cost, Leverage (if applicable)

Example pre-trade check for BTC/USDT perpetual on OKX:
```bash
# Step 1: Check minimum order size AND contract size
node scripts/exchange.mjs markets '{"exchange":"okx","market_type":"swap","base":"BTC"}'
# → look for limits.amount.min (e.g. 1 contract) and contractSize (e.g. 0.01 BTC)
# → This means: 1 contract = 0.01 BTC, min order = 1 contract = 0.01 BTC

# Step 2: Check balance
node scripts/exchange.mjs balance '{"exchange":"okx"}'
# → e.g. 7 USDT free

# Step 3: Calculate — 7 USDT × 10x = 70 USDT ÷ $68000 ≈ 0.001 BTC ÷ 0.01 = 0.1 contracts → below min 1 contract → cannot trade
# With more capital: 100 USDT × 10x = 1000 ÷ $68000 ≈ 0.0147 BTC ÷ 0.01 = 1.47 → round to 1 contract → OK
```

| Action | Description | Params |
|--------|-------------|--------|
| `create_order` | Place order | Spot: `{"exchange":"okx","symbol":"BTC/USDT","type":"market","side":"buy","amount":0.001}` (amount in BTC). Swap: `{"exchange":"okx","symbol":"BTC/USDT:USDT","type":"market","side":"buy","amount":1,"market_type":"swap"}` (amount in contracts) |
| `cancel_order` | Cancel order | `{"exchange":"okx","symbol":"BTC/USDT","order_id":"xxx"}` |
| `set_leverage` | Set leverage | `{"exchange":"okx","symbol":"BTC/USDT:USDT","leverage":10,"market_type":"swap"}` |
| `set_margin_mode` | Margin mode | `{"exchange":"okx","symbol":"BTC/USDT:USDT","margin_mode":"cross","market_type":"swap"}` |
| `transfer` | Transfer funds | `{"exchange":"binance","code":"USDT","amount":100,"from_account":"spot","to_account":"future"}` |

**Notes on `transfer`:**
- **OKX unified account (重要)**: OKX uses a **unified trading account** — spot and derivatives share the SAME balance. **Do NOT ask the user to transfer funds between accounts.** If transfer returns error 58123, tell the user: "你的 OKX 是统一账户，现货和合约共用同一个余额，不需要划转。" Do NOT suggest manual transfer in the app.
- **Binance**: Requires explicit transfer between spot/futures accounts.

---

### scripts/ft.mjs — Freqtrade Bot Control

| Action | Description | Params |
|--------|-------------|--------|
| `ping` | Health check | None |
| `start` | Start trading | None |
| `stop` | Stop trading | None |
| `reload` | Reload config | None |
| `config` | View config | None |
| `version` | Version info | None |
| `sysinfo` | System info | None |
| `health` | Health status | None |
| `logs` | View logs | `{"limit":50}` |
| `balance` | Account balance | None |
| `trades_open` | Open trades | None |
| `trades_count` | Trade count | None |
| `trade_by_id` | Trade by ID | `{"trade_id":1}` |
| `trades_history` | Trade history | `{"limit":50}` |
| `force_enter` | Manual entry | `{"pair":"BTC/USDT","side":"long"}` |
| `force_exit` | Manual exit | `{"tradeid":"1"}` |
| `cancel_order` | Cancel order | `{"trade_id":1}` |
| `delete_trade` | Delete record | `{"trade_id":1}` |
| `profit` | Profit summary | None |
| `profit_per_pair` | Profit per pair | None |
| `daily` | Daily report | `{"count":7}` |
| `weekly` | Weekly report | `{"count":4}` |
| `monthly` | Monthly report | `{"count":3}` |
| `stats` | Statistics | None |

---

### scripts/ft-dev.mjs — Freqtrade Dev Tools

| Action | Description | Params |
|--------|-------------|--------|
| `backtest_start` | Start backtest | `{"strategy":"MyStrategy","timerange":"20240101-20240601","timeframe":"5m"}` |
| `backtest_status` | Backtest status | None |
| `backtest_abort` | Abort backtest | None |
| `backtest_history` | Backtest history | None |
| `backtest_result` | History result | `{"id":"xxx"}` |
| `candles_live` | Live candles | `{"pair":"BTC/USDT","timeframe":"1h"}` |
| `candles_analyzed` | Candles with indicators | `{"pair":"BTC/USDT","timeframe":"1h","strategy":"MyStrategy"}` |
| `candles_available` | Available pairs | None |
| `whitelist` | Whitelist | None |
| `blacklist` | Blacklist | None |
| `blacklist_add` | Add to blacklist | `{"add":["DOGE/USDT"]}` |
| `locks` | Trade locks | None |
| `strategy_list` | Strategy list | None |
| `strategy_get` | Strategy detail | `{"name":"MyStrategy"}` |

---

### scripts/auto-trade.mjs — Automated Trading

Config + execution helper. **The AI agent makes all strategy decisions** — this script only handles config, risk management, and order execution.

Config is stored at `~/.openclaw/workspace/aicoin-trade-config.json`.

| Action | Description | Params |
|--------|-------------|--------|
| `setup` | Save trading config | `{"exchange":"okx","symbol":"BTC/USDT:USDT","leverage":20,"capital_pct":0.5,"stop_loss_pct":0.025,"take_profit_pct":0.05}` |
| `status` | Show config + balance + positions + open orders | `{}` |
| `open` | Open a position (agent decides direction) | `{"direction":"long"}` or `{"direction":"short"}` |
| `close` | Close current position + cancel orders | `{}` |

The `open` action automatically:
1. Checks balance and market minimums
2. Calculates position size from config (capital_pct × balance × leverage)
3. Sets leverage
4. Places market order
5. Places stop-loss and take-profit limit orders

---

### scripts/ft-deploy.mjs — Freqtrade Deployment

**🚨 CRITICAL: For ALL Freqtrade operations (deploy, backtest, update), ALWAYS use ft-deploy.mjs. NEVER manually run freqtrade commands, NEVER write custom Python scripts, NEVER use Docker.**

**One-click Freqtrade deployment via `git clone` + official `setup.sh` (no Docker).** Clones the Freqtrade repo, runs `setup.sh -i` to install all dependencies (including TA-Lib), generates config from `.env` exchange keys, starts as background process, auto-writes `FREQTRADE_*` vars to `.env`.

| Action | Description | Params |
|--------|-------------|--------|
| `check` | Check prerequisites (Python 3.11+, git, exchange keys) | None |
| `deploy` | Deploy Freqtrade (clone, setup.sh, config, start) | `{"dry_run":true,"pairs":["BTC/USDT:USDT","ETH/USDT:USDT"]}` |
| `backtest` | Run backtest (no running process needed) | `{"strategy":"SampleStrategy","timeframe":"1h","timerange":"20250101-20260301"}` |
| `update` | Update Freqtrade to latest version | None |
| `status` | Process status | None |
| `start` | Start stopped process | None |
| `stop` | Stop process | None |
| `logs` | View process logs | `{"lines":50}` |
| `remove` | Remove process (preserves config) | None |

**Deploy defaults to dry-run mode** (simulated trading, no real money). Pass `{"dry_run":false}` for live trading.

**IMPORTANT: NEVER use Docker for Freqtrade.** The deploy script uses `git clone` + `setup.sh -i` (official Freqtrade installation method). Do NOT fall back to Docker, do NOT write custom install scripts, do NOT try `pip install freqtrade` directly. Just run `node scripts/ft-deploy.mjs deploy` — it handles everything.

**IMPORTANT: Do NOT manually edit Freqtrade config files, do NOT manually run `freqtrade trade` commands, do NOT manually `source .venv/bin/activate`.** Always use `ft-deploy.mjs` actions. If deploy fails, check logs with `ft-deploy.mjs logs` and report the error — do NOT attempt manual workarounds.

---

## Automated Trading Guide

When the user asks to set up automated trading, follow this workflow. **Do NOT write custom scripts.**

### How It Works

The AI agent is the strategist. On each cycle:
1. **Fetch data** using existing scripts: `coin.mjs` (funding, OI, liquidation), `market.mjs` (klines, volume), `features.mjs` (whale orders, long/short ratio), `hl-market.mjs` (Hyperliquid data)
2. **Analyze** the data — trend, momentum, risk signals. Use your own judgment.
3. **Decide**: open long, open short, close position, or hold
4. **Execute** via `auto-trade.mjs open '{"direction":"long"}'` — handles position sizing, leverage, stop-loss/take-profit automatically

### Quick Setup

```bash
# 1. Configure risk params
node scripts/auto-trade.mjs setup '{"exchange":"okx","symbol":"BTC/USDT:USDT","leverage":10,"capital_pct":0.5}'

# 2. Check status
node scripts/auto-trade.mjs status
```

### OpenClaw Cron (Recommended)

**Use OpenClaw's built-in cron, NOT system crontab.** This gives the user visibility in the web UI.

```bash
openclaw cron add \
  --name "BTC auto trade" \
  --every 10m \
  --session isolated \
  --message "You are a crypto trader. Use the aicoin skill to: 1) Fetch BTC market data (price, funding rate, OI, whale orders, liquidation). 2) Analyze the data and decide: open long, open short, close, or hold. 3) If trading, run: node scripts/auto-trade.mjs open '{\"direction\":\"long\"}'. 4) Report your analysis briefly."
```

### When User Asks "帮我自动交易"

1. Ask: which exchange? which coin? how much capital? what leverage?
2. Run `auto-trade.mjs setup` with their params
3. Run `auto-trade.mjs status` to verify exchange connection
4. Set up OpenClaw cron with their preferred interval
5. Done — tell them they can check status anytime via `auto-trade.mjs status`

---

## Freqtrade Guide

**🚨 CRITICAL: When user asks to deploy/setup Freqtrade, ALWAYS use `ft-deploy.mjs`. NEVER manually configure, NEVER use Docker, NEVER write custom scripts.**

When the user asks about backtesting, professional strategies, quantitative trading, or deploying a trading bot, guide them to Freqtrade.

**Freqtrade vs auto-trade.mjs:**
- auto-trade.mjs = simple AI-driven, good for testing, small capital
- Freqtrade = professional, backtestable, risk-managed, production-grade

### Deployment (One Command)

```bash
# Check prerequisites first
node scripts/ft-deploy.mjs check

# Deploy (dry-run mode by default — safe)
node scripts/ft-deploy.mjs deploy '{"pairs":["BTC/USDT:USDT","ETH/USDT:USDT"]}'
```

This automatically:
1. Ensures Python 3.11+ is available (auto-installs via brew if needed on macOS)
2. Clones Freqtrade repo to `~/.freqtrade/source/`
3. Runs official `setup.sh -i` (installs TA-Lib, creates venv, installs all dependencies)
4. Creates config from exchange keys in `.env`
5. Includes a sample RSI+EMA strategy (pure pandas, no TA-Lib import needed)
6. Starts Freqtrade as a background process with API server
7. Writes `FREQTRADE_URL`, `FREQTRADE_USERNAME`, `FREQTRADE_PASSWORD` to `.env`
8. Ready to use via `ft.mjs` and `ft-dev.mjs`

**Prerequisites:** Python 3.11+ and git. Exchange API keys must be in `.env`. Everything else is auto-installed — do NOT install manually or use Docker.

### User Journey

```
"帮我部署Freqtrade"
  → node scripts/ft-deploy.mjs deploy
  → "已部署，dry-run模式，用模拟资金运行"

"帮我回测BTC策略"
  → node scripts/ft-deploy.mjs backtest '{"strategy":"SampleStrategy","timeframe":"1h","timerange":"20250101-20260301"}'
  → "回测结果: 胜率62%, 最大回撤-8%, 总收益+45%"

"不错，上实盘"
  → node scripts/ft-deploy.mjs deploy '{"dry_run":false}'
  → "⚠️ 已切换到实盘模式，使用真实资金"

"今天赚了多少？"
  → node scripts/ft.mjs profit
  → node scripts/ft.mjs daily '{"count":7}'

"暂停交易"
  → node scripts/ft.mjs stop
```

### When User Mentions These Keywords → Use Freqtrade

- 回测 / backtest → **MUST use `ft-deploy.mjs backtest`** (does NOT require Freqtrade to be running). NEVER write custom Python backtest scripts, NEVER manually run freqtrade commands.
- 写策略 / write strategy → Write a `.py` file to `~/.freqtrade/user_data/strategies/`, then `ft-deploy.mjs backtest`
- 量化策略 / strategy → `ft-dev.mjs strategy_list` (requires running process)
- 部署机器人 / deploy bot → `ft-deploy.mjs deploy`
- 实盘 / live trading → `ft-deploy.mjs deploy '{"dry_run":false}'`
- 盈亏 / profit → `ft.mjs profit`
- 停止机器人 / stop bot → `ft.mjs stop` or `ft-deploy.mjs stop`

**IMPORTANT: For backtesting, use `ft-deploy.mjs backtest`. Do NOT write custom Python backtest scripts. The Freqtrade backtester is production-grade with proper slippage, fees, and position sizing simulation.**

### Troubleshooting

**If deployment fails:**
1. Check Python version: `python3 --version` (need 3.11+)
2. Check logs: `node scripts/ft-deploy.mjs logs`
3. Verify exchange keys in `~/.openclaw/workspace/.env`
4. DO NOT try manual fixes - report error and let ft-deploy.mjs handle it

**If backtest fails:**
1. Verify strategy file exists in `~/.freqtrade/user_data/strategies/`
2. Check timerange format: `YYYYMMDD-YYYYMMDD` (e.g., `20250101-20260301`)
3. Ensure data is downloaded (ft-deploy.mjs auto-downloads on first backtest)
