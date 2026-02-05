---
name: kalshi-docs
description: Kalshi prediction markets API documentation. Use when building integrations with Kalshi's REST API or WebSocket streams for trading, market data, or portfolio management.
license: CC0-1.0
metadata:
  source: https://github.com/ammario/kalshi-docs
  updated: nightly
---

# Kalshi API Documentation

Complete API reference for Kalshi's prediction markets platform. Use this skill when:
- Building trading bots or integrations with Kalshi
- Working with market data, orders, or portfolio APIs
- Implementing WebSocket connections for real-time data
- Understanding authentication and rate limits

## Documentation Structure

- `api-reference/` - Complete REST API endpoints organized by category:
  - `api-keys/` - API key management
  - `communications/` - RFQs and quotes
  - `events/` - Event data and series
  - `exchange/` - Exchange info, schedule, announcements
  - `market/` - Market data, orderbooks, candlesticks
  - `orders/` - Order placement and management
  - `portfolio/` - Positions, fills, balance, settlements
  - `multivariate/` - Multi-leg market operations
- `getting_started/` - Quickstart guides and concepts
- `websockets/` - WebSocket API for real-time streaming
- `asyncapi.yaml` - WebSocket API schema (AsyncAPI format)
- `changelog.md` - API changes and updates

## Key Files

- `getting_started/api_keys.md` - API key setup and authentication
- `getting_started/quick_start_market_data.md` - Fetching market data
- `getting_started/quick_start_create_order.md` - Placing orders
- `getting_started/quick_start_websockets.md` - Real-time streaming
- `getting_started/rate_limits.md` - Rate limiting details
- `api-reference/portfolio/` - Trading and position management
- `api-reference/market/` - Market data endpoints

## Usage Notes

- API base URL: `https://api.kalshi.com/trade-api/v2`
- WebSocket URL: `wss://api.kalshi.com/trade-api/ws/v2`
- Demo environment available at `https://demo-api.kalshi.co`
- All trading endpoints require authentication via API key
- Rate limits apply - see `getting_started/rate_limits.md`
