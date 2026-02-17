---
name: polymarket
description: |
  Polymarket sports prediction markets — live odds, prices, order books, events, series, and market search. No auth required. Covers NFL, NBA, MLB, soccer, tennis, cricket, MMA, esports. Supports moneyline, spreads, totals, and player props.

  Use when: user asks about sports betting odds, prediction markets, win probabilities, market sentiment, or "who is favored to win" questions.
  Don't use when: user asks about actual match results, scores, or statistics — use football-data or fastf1 instead. Don't use for historical match data. Don't use for news — use sports-news instead. Don't confuse with Kalshi — Polymarket focuses on crypto-native prediction markets with deeper sports coverage; Kalshi is a US-regulated exchange with different market structure.
license: MIT
metadata:
  author: machina-sports
  version: "0.1.0"
---

# Polymarket — Sports Prediction Markets

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
sports-skills polymarket get_sports_markets --limit=20
sports-skills polymarket search_markets --query="NBA Finals"
```

Python SDK (alternative):
```python
from sports_skills import polymarket

markets = polymarket.get_sports_markets(limit=20)
prices = polymarket.get_market_prices(token_id="abc123")
```

## Commands

### get_sports_markets
Get active sports prediction markets.
- `limit` (int, optional): Max results (default: 50, max: 100)
- `offset` (int, optional): Pagination offset
- `sports_market_types` (str, optional): Filter by type ("moneyline", "spreads", "totals")
- `game_id` (str, optional): Filter by game
- `active` (bool, optional): Only active markets (default: true)
- `closed` (bool, optional): Include closed markets (default: false)
- `order` (str, optional): Sort field (default: "volume")
- `ascending` (bool, optional): Sort ascending (default: false)

### get_sports_events
Get sports events (each groups related markets).
- `limit`, `offset`, `active`, `closed`, `order`, `ascending` (same as above)
- `series_id` (str, optional): Filter by series (league) ID

### get_series
Get all series (leagues, recurring event groups).
- `limit` (int, optional): Max results (default: 100)
- `offset` (int, optional): Pagination offset

### get_market_details
Get detailed info for a specific market.
- `market_id` (str): Market ID
- `slug` (str): Market slug (alternative to ID)

### get_event_details
Get detailed info for a specific event.
- `event_id` (str): Event ID
- `slug` (str): Event slug (alternative to ID)

### get_market_prices
Get current prices from the CLOB API.
- `token_id` (str): Single CLOB token ID
- `token_ids` (list): Multiple CLOB token IDs (batch)

### get_order_book
Get full order book for a market.
- `token_id` (str, required): CLOB token ID

### get_sports_market_types
Get all valid sports market types. No params.

### search_markets
Find markets by keyword and filters. **Search matches event titles, not sport categories.** Use specific league/competition names, not generic terms like "soccer" or "football".
- `query` (str, optional): Keyword to search — use league names (e.g., "Premier League", "Champions League", "La Liga", "NBA Finals")
- `sports_market_types` (str, optional): Filter by type
- `tag_id` (int, optional): Tag ID (default: 1 = Sports)
- `limit` (int, optional): Max results (default: 20)

### get_price_history
Get historical price data.
- `token_id` (str, required): CLOB token ID
- `interval` (str, optional): Time range ("1d", "1w", "1m", "max"). Default: "max"
- `fidelity` (int, optional): Seconds between data points. Default: 120

### get_last_trade_price
Get the most recent trade price.
- `token_id` (str, required): CLOB token ID

## Examples

User: "Who's favored to win the NBA Finals?"
1. Call `search_markets(query="NBA Finals", sports_market_types="moneyline")`
2. Get `token_id` from the market details
3. Call `get_market_prices(token_id="...")` for current odds
4. Present teams with implied probabilities (price = probability)

User: "Who will win the Premier League?"
1. Call `search_markets(query="English Premier League")` — use full league name
2. Sort results by Yes outcome price descending
3. Present teams with implied probabilities (price = probability)

User: "Show me Champions League odds"
1. Call `search_markets(query="Champions League")`
2. Present top contenders with prices, volume, and liquidity

User: "What's the order book depth on this market?"
1. Call `get_order_book(token_id="...")` for full book
2. Present bids, asks, spread, and implied probabilities

## Error Handling

When a command fails (invalid token_id, no active markets, network error, etc.), **do not surface the raw error to the user**. Instead:

1. **Catch it silently** — treat the failure as an exploratory miss, not a fatal error.
2. **Try alternatives** — if a `token_id` is invalid, use `search_markets(query="...")` to find the correct market, then `get_market_details` to get the CLOB token_id. If a search returns empty, try broader or alternative keywords (e.g., "English Premier League" instead of "EPL").
3. **Only report failure after exhausting alternatives** — and when you do, give a clean human-readable message (e.g., "I couldn't find any active markets for that on Polymarket"), not a traceback or raw CLI output.

This is especially important when the agent is responding through messaging platforms (Telegram, Slack, etc.) where raw exec failures look broken.

## Common Mistakes

**These are the ONLY valid commands.** Do not invent or guess command names:
- `get_sports_markets`
- `get_sports_events`
- `get_series`
- `get_market_details`
- `get_event_details`
- `get_market_prices`
- `get_order_book`
- `get_sports_market_types`
- `search_markets`
- `get_price_history`
- `get_last_trade_price`

**Commands that DO NOT exist** (commonly hallucinated):
- ~~`get_market_odds`~~ / ~~`get_odds`~~ — market prices ARE the implied probability. Use `get_market_prices(token_id="...")` where price = probability.
- ~~`get_implied_probability`~~ — the price IS the implied probability. No conversion needed.
- ~~`get_current_odds`~~ — use `get_last_trade_price(token_id="...")` for the most recent price.
- ~~`get_markets`~~ — the correct command is `get_sports_markets` (for browsing) or `search_markets` (for searching by keyword).

**Other common mistakes:**
- Using `market_id` where `token_id` is needed — price and orderbook endpoints require the CLOB `token_id`, not the Gamma `market_id`. Always call `get_market_details` first to get `clobTokenIds`.
- Searching generic terms like "soccer" or "football" — `search_markets` matches event titles. Use specific league names: "Premier League", "Champions League", "La Liga", etc.
- Forgetting to get the `token_id` before calling price/orderbook endpoints — always fetch market details first.

If you're unsure whether a command exists, check this list. Do not try commands that aren't listed above.

## Troubleshooting

- **`sports-skills` command not found**: Package not installed. Run `pip install sports-skills`. If pip fails with a Python version error, you need Python 3.10+ — see Setup section.
- **`ModuleNotFoundError: No module named 'sports_skills'`**: Same as above — install the package. Prefer the CLI over Python imports to avoid path issues.
- **token_id vs market_id**: Price/orderbook endpoints need the CLOB `token_id` (found in market details under `clobTokenIds`), not the Gamma `market_id`. Always fetch market details first to get the token_id.
- **Search returns 0 results**: `search_markets` matches event titles, not sport categories. Don't search "soccer" or "football" — search by league name: "Premier League", "Champions League", "La Liga", "Bundesliga", "Serie A", "NBA Finals", etc.
- **Market not found by ID**: Use `search_markets(query="...")` with keywords instead of guessing IDs. Or use `get_market_details(slug="...")` with the URL slug.
- **Stale or wide prices**: Low-liquidity markets may have wide bid-ask spreads. The `mid` price from `get_market_prices` is the midpoint — check `spread` to assess reliability.
- **Pagination**: Use `offset` parameter for paging. Default `limit` varies by endpoint (20-100). Increment offset by limit for each page.

## APIs

- **Gamma API** (gamma-api.polymarket.com): Market metadata, events, series. Public, no auth.
- **CLOB API** (clob.polymarket.com): Prices, order books, trades. Public reads, no auth.
