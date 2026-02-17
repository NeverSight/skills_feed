---
name: kalshi
description: |
  Kalshi prediction markets — events, series, markets, trades, and candlestick data. Public API, no auth required for reads. US-regulated exchange (CFTC). Covers soccer, basketball, baseball, tennis, NFL, hockey event contracts.

  Use when: user asks about Kalshi-specific markets, event contracts, CFTC-regulated prediction markets, or candlestick/OHLC price history on sports outcomes.
  Don't use when: user asks about actual match results, scores, or statistics — use football-data or fastf1 instead. Don't use for general "who will win" questions unless Kalshi is specifically mentioned — try polymarket first (broader sports coverage). Don't use for news — use sports-news instead.
license: MIT
metadata:
  author: machina-sports
  version: "0.1.0"
---

# Kalshi — Prediction Markets

## Setup

Before first use, check if the CLI is available:
```bash
which sports-skills || pip install sports-skills
```
If `pip install` fails with a Python version error, the package requires Python 3.10+. Find a compatible Python:
```bash
python3 --version  # check version
# If < 3.10, try: python3.12 -m pip install sports-skills
# On macOS with Homebrew: /opt/homebrew/bin/python3.12 -m pip install sports-skills
```
No API keys required.

## Quick Start

Prefer the CLI — it avoids Python import path issues:
```bash
sports-skills kalshi get_markets --series_ticker=KXNBA
sports-skills kalshi get_events --series_ticker=KXNBA --status=open
```

Python SDK (alternative):
```python
from sports_skills import kalshi

markets = kalshi.get_markets(series_ticker="KXNBA")
event = kalshi.get_event(event_ticker="KXNBA-26FEB14")
```

## Commands

### get_exchange_status
Get exchange status (trading active, maintenance). No params.

### get_exchange_schedule
Get exchange operating schedule. No params.

### get_series_list
Get all available series.
- `category` (str, optional): Filter by category
- `tags` (str, optional): Filter by tags

### get_series
Get details for a specific series.
- `series_ticker` (str, required): Series ticker (see table below)

### get_events
Get events with optional filtering.
- `limit` (int, optional): Max results (default: 100, max: 200)
- `cursor` (str, optional): Pagination cursor
- `status` (str, optional): Filter by status ("open", "closed", "settled")
- `series_ticker` (str, optional): Filter by series ticker
- `with_nested_markets` (bool, optional): Include nested markets

### get_event
Get details for a specific event.
- `event_ticker` (str, required): Event ticker
- `with_nested_markets` (bool, optional): Include nested markets

### get_markets
Get markets with optional filtering.
- `limit` (int, optional): Max results (default: 100)
- `cursor` (str, optional): Pagination cursor
- `event_ticker` (str, optional): Filter by event
- `series_ticker` (str, optional): Filter by series
- `status` (str, optional): Filter ("unopened", "open", "closed", "settled")
- `tickers` (str, optional): Comma-separated market tickers

### get_market
Get details for a specific market.
- `ticker` (str, required): Market ticker

### get_trades
Get recent trades.
- `limit` (int, optional): Max results (default: 100, max: 1000)
- `cursor` (str, optional): Pagination cursor
- `ticker` (str, optional): Filter by market ticker
- `min_ts` (int, optional): After Unix timestamp
- `max_ts` (int, optional): Before Unix timestamp

### get_market_candlesticks
Get OHLC candlestick data.
- `series_ticker` (str, required): Series ticker
- `ticker` (str, required): Market ticker
- `start_ts` (int, required): Start Unix timestamp
- `end_ts` (int, required): End Unix timestamp
- `period_interval` (int, required): Interval in minutes (1, 60, or 1440)

### get_sports_filters
Get available sports filter categories. No params.

## Common Series Tickers

**IMPORTANT:** On Kalshi, "Football" = American Football (NFL). Soccer is under "Soccer".

| Sport | Series Ticker | Notes |
|-------|--------------|-------|
| NBA | `KXNBA` | Games + futures |
| NFL | `KXNFL` | Games + futures |
| MLB | `KXMLB` | Games + futures |
| Champions League | `KXUCL` | Futures (winner) |
| La Liga | `KXLALIGA` | Futures (winner) |
| Bundesliga | `KXBUNDESLIGA` | Futures (winner) |
| Serie A | `KXSERIEA` | Futures (winner) |
| Ligue 1 | `KXLIGUE1` | Futures (winner) |
| FA Cup | `KXFACUP` | Futures |
| Europa League | `KXUEL` | Futures |
| Conference League | `KXUECL` | Futures |

Not all soccer leagues have futures/winner markets. EPL has match-day games but **no title winner** market. Use `get_sports_filters()` to discover all available competitions.

## Examples

User: "What NBA markets are on Kalshi?"
1. Call `get_events(series_ticker="KXNBA", status="open", with_nested_markets=True)`
2. Present events with their nested markets, yes/no prices, and volume

User: "Who will win the Champions League?"
1. Call `get_markets(series_ticker="KXUCL", status="open")`
2. Sort by `last_price` descending — price = implied probability (e.g., 20 = 20%)
3. Present top teams with `yes_sub_title`, `last_price`, and `volume`

User: "Show me the price history for this NBA game"
1. Get the market ticker from `get_markets(series_ticker="KXNBA")`
2. Call `get_market_candlesticks(series_ticker="KXNBA", ticker="...", start_ts=..., end_ts=..., period_interval=60)`
3. Present OHLC data with volume

## Error Handling

When a command fails (invalid ticker, no open markets, network error, etc.), **do not surface the raw error to the user**. Instead:

1. **Catch it silently** — treat the failure as an exploratory miss, not a fatal error.
2. **Try alternatives** — if a series ticker returns no results, call `get_series_list()` to discover available tickers. If an event ticker is invalid, use `get_events(series_ticker="...")` to find valid events. If markets are empty for a sport, check `get_sports_filters()` for available categories.
3. **Only report failure after exhausting alternatives** — and when you do, give a clean human-readable message (e.g., "No open markets found for that sport on Kalshi right now"), not a traceback or raw CLI output.

This is especially important when the agent is responding through messaging platforms (Telegram, Slack, etc.) where raw exec failures look broken.

## Common Mistakes

**These are the ONLY valid commands.** Do not invent or guess command names:
- `get_exchange_status`
- `get_exchange_schedule`
- `get_series_list`
- `get_series`
- `get_events`
- `get_event`
- `get_markets`
- `get_market`
- `get_trades`
- `get_market_candlesticks`
- `get_sports_filters`

**Commands that DO NOT exist** (commonly hallucinated):
- ~~`get_odds`~~ / ~~`get_probability`~~ — market prices ARE the implied probability. Use `get_market(ticker="...")` and read the `last_price` field (e.g., 20 = 20% implied probability).
- ~~`get_market_odds`~~ — use `get_market` or `get_markets` and interpret `last_price` as probability.
- ~~`search_markets`~~ — Kalshi has no search endpoint. Use `get_events(series_ticker="...")` or `get_markets(series_ticker="...")` to filter by sport.
- ~~`get_series_by_sport`~~ — use `get_series_list()` and filter, or check the Common Series Tickers table.

**Other common mistakes:**
- Confusing "Football" (NFL) with "Soccer" on Kalshi — see the Common Series Tickers table.
- Guessing series or event tickers instead of discovering them via `get_series_list()` or `get_events()`.
- Forgetting `status="open"` when querying markets — without it, results include settled/closed markets mixed with active ones.

If you're unsure whether a command exists, check this list. Do not try commands that aren't listed above.

## Troubleshooting

- **`sports-skills` command not found**: Package not installed. Run `pip install sports-skills`. If pip fails with a Python version error, you need Python 3.10+ — see Setup section.
- **`ModuleNotFoundError: No module named 'sports_skills'`**: Same as above — install the package. Prefer the CLI over Python imports to avoid path issues.
- **Empty market results**: Use `status="open"` to filter for active markets. Default returns all statuses including settled/closed.
- **Series ticker unknown**: Check the Common Series Tickers table above. Use `get_sports_filters()` to discover categories, but note: "Football" = NFL, "Soccer" = football/soccer. Not all soccer leagues have futures markets.
- **"Football" returned NFL, not soccer**: Kalshi categorizes American Football as "Football" and soccer as "Soccer". Use `KXUCL`, `KXLALIGA`, etc. for soccer — see tickers table.
- **Pagination**: Default limit is 100. If results are truncated, use the `cursor` value from the response to fetch the next page.
- **Candlestick timestamps**: `start_ts` and `end_ts` must be Unix timestamps (seconds). `period_interval` is in minutes: 1 (1-min), 60 (1-hour), or 1440 (1-day).

## API

- **Base URL:** `https://api.elections.kalshi.com/trade-api/v2`
- All endpoints are public, read-only. No authentication required.
