---
name: massive-api
description: Access Massive(Polygon) stock, crypto, forex, options, indices, futures, market data, and news APIs via CLI.
metadata:
  openclaw:
    requires:
      bins: ["npx"]
      env: ["MASSIVE_API_KEY"]
    primaryEnv: "MASSIVE_API_KEY"
---

# Massive(Polygon) Market Data Skill

A CLI tool and JS client wrapper for the [Massive(Polygon)](https://massive.com) financial data APIs. Covers stocks, crypto, forex, options, indices, futures, market status, news, and reference data.

## CLI Usage

```bash
npx -y massive-cli <command> [options]
```

All commands output JSON to stdout. Use `--help` for a list of commands or `<command> --help` for command-specific options.

## Command Structure

Commands are organized by asset class with subcommands:

### Stocks

```bash
npx -y massive-cli stocks <subcommand> [options]
```

Available subcommands:
- `aggs` - Stock aggregate bars (OHLCV)
- `trades` - Stock trades
- `quotes` - Stock quotes (NBBO)
- `snapshot` - Stock ticker snapshot
- `open-close` - Stock daily open/close
- `previous` - Stock previous day aggregates
- `grouped` - Stock grouped daily aggregates
- `sma` - Simple Moving Average
- `ema` - Exponential Moving Average
- `rsi` - Relative Strength Index
- `macd` - Moving Average Convergence/Divergence
- `last-trade` - Last stock trade
- `last-quote` - Last stock quote

See [Stocks Commands Reference](references/stocks_commands.md) for full details.

### Crypto

```bash
npx -y massive-cli crypto <subcommand> [options]
```

Available subcommands:
- `aggs` - Crypto aggregate bars
- `trades` - Crypto trades
- `snapshot` - Crypto ticker snapshot
- `snapshot-direction` - Crypto snapshot by direction (gainers/losers)
- `snapshot-tickers` - Crypto snapshot for multiple tickers
- `open-close` - Crypto daily open/close
- `previous` - Crypto previous day aggregates
- `grouped` - Crypto grouped daily aggregates
- `sma` - Simple Moving Average
- `ema` - Exponential Moving Average
- `rsi` - Relative Strength Index
- `macd` - Moving Average Convergence/Divergence
- `last-trade` - Last crypto trade

See [Crypto Commands Reference](references/crypto_commands.md) for full details.

### Forex

```bash
npx -y massive-cli forex <subcommand> [options]
```

Available subcommands:
- `aggs` - Forex aggregate bars
- `quotes` - Forex quotes
- `snapshot` - Forex ticker snapshot
- `previous` - Forex previous day aggregates
- `grouped` - Forex grouped daily aggregates
- `sma` - Simple Moving Average
- `ema` - Exponential Moving Average
- `rsi` - Relative Strength Index
- `macd` - Moving Average Convergence/Divergence
- `last-quote` - Last forex quote

Standalone commands:
- `currency-conversion` - Currency conversion

See [Forex Commands Reference](references/forex_commands.md) for full details.

### Options

```bash
npx -y massive-cli options <subcommand> [options]
```

Available subcommands:
- `aggs` - Options aggregate bars
- `trades` - Options trades
- `quotes` - Options quotes
- `open-close` - Options daily open/close
- `chain` - Options chain
- `contract` - Options contract details
- `previous` - Options previous day aggregates
- `sma` - Simple Moving Average
- `ema` - Exponential Moving Average
- `rsi` - Relative Strength Index
- `macd` - Moving Average Convergence/Divergence
- `last-trade` - Last options trade

See [Options Commands Reference](references/options_commands.md) for full details.

### Indices

```bash
npx -y massive-cli indices <subcommand> [options]
```

Available subcommands:
- `aggs` - Indices aggregate bars
- `open-close` - Indices daily open/close
- `snapshot` - Indices ticker snapshot
- `previous` - Indices previous day aggregates
- `sma` - Simple Moving Average
- `ema` - Exponential Moving Average
- `rsi` - Relative Strength Index
- `macd` - Moving Average Convergence/Divergence

See [Indices Commands Reference](references/indices_commands.md) for full details.

### Reference Data

Standalone commands for reference data:
- `tickers` - Query all ticker symbols
- `ticker-details` - Get ticker details
- `ticker-types` - Get ticker types mapping
- `exchanges` - List all exchanges
- `conditions` - List all conditions
- `dividends` - Get dividend data
- `stock-splits` - Get stock splits data
- `financials` - Get financial data
- `ipos` - Get IPO data
- `related-companies` - Get related companies

See [Reference Data Commands Reference](references/reference_commands.md) for full details.

### Market

Standalone commands for market data:
- `market-status` - Get market status
- `market-holidays` - Get market holidays

See [Market Commands Reference](references/market_commands.md) for full details.

### News

Standalone command for news:
- `news` - Get news articles

See [News Commands Reference](references/news_commands.md) for full details.
