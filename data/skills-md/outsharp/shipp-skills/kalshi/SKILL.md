---
name: kalshi
description: >
  Kalshi is a regulated prediction market exchange. Use this skill to interact
  with the Kalshi API for market data, trading, portfolio management,
  WebSocket streaming, and historical data retrieval.

metadata:
  author: Outsharp Inc.
  version: 0.1.0

compatibility:
  requirements:
    - Internet access
    - Python 3.7+ (for SDK or direct API usage)
    - cryptography library (for RSA-PSS request signing)
  notes:
    - Most read endpoints are public and require no authentication.
    - All write endpoints and WebSocket connections require RSA-PSS signed requests.
    - Requests and responses are JSON.
    - Prices are in cents (1–99). Monetary values in some WebSocket channels are in centi-cents (1/10,000th of a dollar).

allowed-tools:
  - Bash(curl:*)
  - Bash(jq:*)
  - Bash(python*:*)
  - Bash(pip*:*)
  - Bash(npm*:*)
  - Bash(npx*:*)

---

# Kalshi API

[Kalshi](https://kalshi.com) is a CFTC-regulated prediction market exchange where users trade on the outcomes of real-world events.

Check this skill and the [official documentation](https://docs.kalshi.com) _FREQUENTLY_. The canonical machine-readable index of all docs lives at:

> **<https://docs.kalshi.com/llms.txt>**

Always consult `llms.txt` to discover every available page before building. It is the single source of truth for endpoint references, SDK docs, WebSocket channels, FIX protocol details, and getting-started guides.

---

## Key Concepts (Glossary)

| Term | Definition |
|---|---|
| **Market** | A single binary outcome contract (Yes / No) with prices in cents (1–99¢). |
| **Event** | A collection of related markets representing a real-world occurrence (e.g., an election, a weather reading). |
| **Series** | A template for recurring events that share the same structure and rules (e.g., "Daily Highest Temp in NYC"). |
| **Orderbook** | Bids only — in binary markets a YES bid at X¢ is equivalent to a NO ask at (100−X)¢. |
| **Fill** | A matched trade on one of your orders. |
| **Settlement** | The final resolution of a market (Yes or No) after determination. |
| **Multivariate Event** | A combo event created dynamically from a multivariate event collection. |

Full glossary: <https://docs.kalshi.com/getting_started/terms.md>

---

## Base URLs

| Environment | REST API | WebSocket |
|---|---|---|
| **Production** | `https://api.elections.kalshi.com/trade-api/v2` | `wss://api.elections.kalshi.com/trade-api/ws/v2` |
| **Demo** | `https://demo-api.kalshi.co/trade-api/v2` | `wss://demo-api.kalshi.co/trade-api/ws/v2` |

> **Note:** Despite the `elections` subdomain, the production URL serves ALL Kalshi markets — economics, weather, tech, entertainment, etc.

Demo environment info: <https://docs.kalshi.com/getting_started/demo_env.md>

---

## Documentation & References

All detailed examples, request/response schemas, and walkthroughs live in the official docs. Always consult these before building:

| Resource | URL |
|---|---|
| **Full documentation index (llms.txt)** | <https://docs.kalshi.com/llms.txt> |
| Introduction | <https://docs.kalshi.com/welcome/index.md> |
| Making your first request | <https://docs.kalshi.com/getting_started/making_your_first_request.md> |
| Quick Start: Market Data | <https://docs.kalshi.com/getting_started/quick_start_market_data.md> |
| Quick Start: Authenticated Requests | <https://docs.kalshi.com/getting_started/quick_start_authenticated_requests.md> |
| Quick Start: Create Your First Order | <https://docs.kalshi.com/getting_started/quick_start_create_order.md> |
| Quick Start: WebSockets | <https://docs.kalshi.com/getting_started/quick_start_websockets.md> |
| API Keys guide | <https://docs.kalshi.com/getting_started/api_keys.md> |
| Rate Limits & Tiers | <https://docs.kalshi.com/getting_started/rate_limits.md> |
| Pagination | <https://docs.kalshi.com/getting_started/pagination.md> |
| Orderbook Responses | <https://docs.kalshi.com/getting_started/orderbook_responses.md> |
| Historical Data | <https://docs.kalshi.com/getting_started/historical_data.md> |
| Subpenny Pricing | <https://docs.kalshi.com/getting_started/subpenny_pricing.md> |
| Fixed-Point Contracts | <https://docs.kalshi.com/getting_started/fixed_point_contracts.md> |
| OpenAPI Spec (YAML) | <https://docs.kalshi.com/openapi.yaml> |
| API Changelog | <https://docs.kalshi.com/changelog/index.md> |
| Kalshi Platform | <https://kalshi.com> |
| Demo Platform | <https://demo.kalshi.co> |

---

## Authentication

Kalshi uses **RSA-PSS signed requests** (not Bearer tokens). Every authenticated request requires three headers:

| Header | Value |
|---|---|
| `KALSHI-ACCESS-KEY` | Your API Key ID |
| `KALSHI-ACCESS-TIMESTAMP` | Current Unix timestamp in **milliseconds** |
| `KALSHI-ACCESS-SIGNATURE` | Base64-encoded RSA-PSS signature of `{timestamp}{METHOD}{path}` |

**Important:** When signing, use the path **without** query parameters. For example, sign `/trade-api/v2/portfolio/orders` even if the request URL is `/trade-api/v2/portfolio/orders?limit=5`.

### Generating API Keys

1. Log in → Account Settings → API Keys section.
2. Click "Create New API Key" to generate an RSA key pair.
3. **Store the private key immediately** — it cannot be retrieved again.

Full guide: <https://docs.kalshi.com/getting_started/api_keys.md>

### Python Signing Example

```python
import base64, datetime, requests
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

def load_private_key(file_path):
    with open(file_path, "rb") as f:
        return serialization.load_pem_private_key(f.read(), password=None)

def sign_pss(private_key, text: str) -> str:
    sig = private_key.sign(
        text.encode("utf-8"),
        padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.DIGEST_LENGTH),
        hashes.SHA256(),
    )
    return base64.b64encode(sig).decode("utf-8")

def kalshi_headers(key_id, private_key, method, path):
    ts = str(int(datetime.datetime.now().timestamp() * 1000))
    path_no_qs = path.split("?")[0]
    sig = sign_pss(private_key, ts + method + path_no_qs)
    return {
        "KALSHI-ACCESS-KEY": key_id,
        "KALSHI-ACCESS-SIGNATURE": sig,
        "KALSHI-ACCESS-TIMESTAMP": ts,
    }
```

### JavaScript Signing Example

```javascript
const crypto = require("crypto");
const fs = require("fs");

function signPss(privateKeyPem, text) {
  const sign = crypto.createSign("RSA-SHA256");
  sign.update(text);
  sign.end();
  return sign.sign({
    key: privateKeyPem,
    padding: crypto.constants.RSA_PKCS1_PSS_PADDING,
    saltLength: crypto.constants.RSA_PSS_SALTLEN_DIGEST,
  }).toString("base64");
}

function kalshiHeaders(keyId, privateKeyPem, method, path) {
  const ts = Date.now().toString();
  const pathNoQs = path.split("?")[0];
  const sig = signPss(privateKeyPem, ts + method + pathNoQs);
  return {
    "KALSHI-ACCESS-KEY": keyId,
    "KALSHI-ACCESS-SIGNATURE": sig,
    "KALSHI-ACCESS-TIMESTAMP": ts,
  };
}
```

---

## SDKs

Kalshi provides official SDKs. Prefer these for production integrations:

| SDK | Install | Docs |
|---|---|---|
| Python (sync) | `pip install kalshi_python_sync` | <https://docs.kalshi.com/sdks/python/quickstart.md> |
| Python (async) | `pip install kalshi_python_async` | <https://docs.kalshi.com/sdks/python/quickstart.md> |
| TypeScript | `npm install kalshi-typescript` | <https://docs.kalshi.com/sdks/typescript/quickstart.md> |

> The old `kalshi-python` package is **deprecated**. Migrate to `kalshi_python_sync` or `kalshi_python_async`.

SDK overview: <https://docs.kalshi.com/sdks/overview.md>

For production applications, consider generating your own client from the [OpenAPI spec](https://docs.kalshi.com/openapi.yaml).

---

## Rate Limits

| Tier | Read | Write |
|---|---|---|
| Basic | 20/s | 10/s |
| Advanced | 30/s | 30/s |
| Premier | 100/s | 100/s |
| Prime | 400/s | 400/s |

Write-limited endpoints: `CreateOrder`, `CancelOrder`, `AmendOrder`, `DecreaseOrder`, `BatchCreateOrders`, `BatchCancelOrders`. In batch APIs each item counts as 1 transaction (except `BatchCancelOrders` where each cancel = 0.2 transactions).

Full details: <https://docs.kalshi.com/getting_started/rate_limits.md>

---

## Pagination

The API uses **cursor-based pagination**. Responses include a `cursor` field; pass it as `?cursor={value}` on the next request. An empty/null cursor means no more pages. Default page size is 100 (max typically 1000).

Full guide: <https://docs.kalshi.com/getting_started/pagination.md>

---

## REST API Endpoints Overview

Below is a summary organized by domain. For full request/response schemas, see the linked docs or browse <https://docs.kalshi.com/llms.txt>.

### Markets

| Endpoint | Method | Auth | Description |
|---|---|---|---|
| `/markets` | GET | No | List markets with filters (status, series, timestamps). Docs: [Get Markets](https://docs.kalshi.com/api-reference/market/get-markets.md) |
| `/markets/{ticker}` | GET | No | Get a single market by ticker. Docs: [Get Market](https://docs.kalshi.com/api-reference/market/get-market.md) |
| `/markets/{ticker}/orderbook` | GET | No | Get current orderbook (yes bids + no bids). Docs: [Get Market Orderbook](https://docs.kalshi.com/api-reference/market/get-market-orderbook.md) |
| `/markets/{ticker}/candlesticks` | GET | No | Candlestick data (1m, 1h, 1d). Docs: [Get Market Candlesticks](https://docs.kalshi.com/api-reference/market/get-market-candlesticks.md) |
| `/markets/candlesticks` | POST | No | Batch candlesticks for up to 100 tickers. Docs: [Batch Get Market Candlesticks](https://docs.kalshi.com/api-reference/market/batch-get-market-candlesticks.md) |
| `/markets/trades` | GET | No | All public trades. Docs: [Get Trades](https://docs.kalshi.com/api-reference/market/get-trades.md) |
| `/series/{ticker}` | GET | No | Get a series. Docs: [Get Series](https://docs.kalshi.com/api-reference/market/get-series.md) |
| `/series` | GET | No | List series. Docs: [Get Series List](https://docs.kalshi.com/api-reference/market/get-series-list.md) |

### Events

| Endpoint | Method | Auth | Description |
|---|---|---|---|
| `/events` | GET | No | List events (excludes multivariate). Docs: [Get Events](https://docs.kalshi.com/api-reference/events/get-events.md) |
| `/events/{ticker}` | GET | No | Get a single event. Docs: [Get Event](https://docs.kalshi.com/api-reference/events/get-event.md) |
| `/events/{ticker}/metadata` | GET | No | Event metadata only. Docs: [Get Event Metadata](https://docs.kalshi.com/api-reference/events/get-event-metadata.md) |
| `/events/{ticker}/candlesticks` | GET | No | Aggregated event candlesticks. Docs: [Get Event Candlesticks](https://docs.kalshi.com/api-reference/events/get-event-candlesticks.md) |
| `/events/{ticker}/forecast/percentile_history` | GET | No | Forecast percentile history. Docs: [Get Event Forecast Percentile History](https://docs.kalshi.com/api-reference/events/get-event-forecast-percentile-history.md) |
| `/events/multivariate` | GET | No | List multivariate events. Docs: [Get Multivariate Events](https://docs.kalshi.com/api-reference/events/get-multivariate-events.md) |

### Orders (Authenticated)

| Endpoint | Method | Auth | Description |
|---|---|---|---|
| `/portfolio/orders` | POST | Yes | Create an order. Docs: [Create Order](https://docs.kalshi.com/api-reference/orders/create-order.md) |
| `/portfolio/orders` | GET | Yes | List your orders (resting/canceled/executed). Docs: [Get Orders](https://docs.kalshi.com/api-reference/orders/get-orders.md) |
| `/portfolio/orders/{order_id}` | GET | Yes | Get a single order. Docs: [Get Order](https://docs.kalshi.com/api-reference/orders/get-order.md) |
| `/portfolio/orders/{order_id}` | DELETE | Yes | Cancel an order. Docs: [Cancel Order](https://docs.kalshi.com/api-reference/orders/cancel-order.md) |
| `/portfolio/orders/{order_id}/amend` | POST | Yes | Amend price/count. Docs: [Amend Order](https://docs.kalshi.com/api-reference/orders/amend-order.md) |
| `/portfolio/orders/{order_id}/decrease` | POST | Yes | Decrease contract count. Docs: [Decrease Order](https://docs.kalshi.com/api-reference/orders/decrease-order.md) |
| `/portfolio/orders/{order_id}/queue_position` | GET | Yes | Queue position. Docs: [Get Order Queue Position](https://docs.kalshi.com/api-reference/orders/get-order-queue-position.md) |
| `/portfolio/orders/queue_positions` | GET | Yes | Queue positions for all resting orders. Docs: [Get Queue Positions for Orders](https://docs.kalshi.com/api-reference/orders/get-queue-positions-for-orders.md) |
| `/portfolio/orders/batched` | POST | Yes | Batch create (up to 20). Docs: [Batch Create Orders](https://docs.kalshi.com/api-reference/orders/batch-create-orders.md) |
| `/portfolio/orders/batched` | DELETE | Yes | Batch cancel (up to 20). Docs: [Batch Cancel Orders](https://docs.kalshi.com/api-reference/orders/batch-cancel-orders.md) |

### Portfolio (Authenticated)

| Endpoint | Method | Auth | Description |
|---|---|---|---|
| `/portfolio/balance` | GET | Yes | Account balance (cents). Docs: [Get Balance](https://docs.kalshi.com/api-reference/portfolio/get-balance.md) |
| `/portfolio/positions` | GET | Yes | Market positions. Docs: [Get Positions](https://docs.kalshi.com/api-reference/portfolio/get-positions.md) |
| `/portfolio/fills` | GET | Yes | Your fills. Docs: [Get Fills](https://docs.kalshi.com/api-reference/portfolio/get-fills.md) |
| `/portfolio/settlements` | GET | Yes | Settlement history. Docs: [Get Settlements](https://docs.kalshi.com/api-reference/portfolio/get-settlements.md) |
| `/portfolio/resting_order_value` | GET | Yes | Total resting order value (FCM). Docs: [Get Total Resting Order Value](https://docs.kalshi.com/api-reference/portfolio/get-total-resting-order-value.md) |

### Subaccounts (Authenticated)

| Endpoint | Method | Auth | Description |
|---|---|---|---|
| `/portfolio/subaccounts` | POST | Yes | Create subaccount (max 32). Docs: [Create Subaccount](https://docs.kalshi.com/api-reference/portfolio/create-subaccount.md) |
| `/portfolio/subaccounts/balances` | GET | Yes | All subaccount balances. Docs: [Get All Subaccount Balances](https://docs.kalshi.com/api-reference/portfolio/get-all-subaccount-balances.md) |
| `/portfolio/subaccounts/transfers` | GET | Yes | Subaccount transfer history. Docs: [Get Subaccount Transfers](https://docs.kalshi.com/api-reference/portfolio/get-subaccount-transfers.md) |
| `/portfolio/subaccounts/transfer` | POST | Yes | Transfer between subaccounts. Docs: [Transfer Between Subaccounts](https://docs.kalshi.com/api-reference/portfolio/transfer-between-subaccounts.md) |

### Order Groups (Authenticated)

Order groups apply a rolling 15-second contracts limit; when hit, all orders in the group are auto-cancelled.

| Endpoint | Method | Auth | Description |
|---|---|---|---|
| `/portfolio/order_groups` | POST | Yes | Create group. Docs: [Create Order Group](https://docs.kalshi.com/api-reference/order-groups/create-order-group.md) |
| `/portfolio/order_groups` | GET | Yes | List groups. Docs: [Get Order Groups](https://docs.kalshi.com/api-reference/order-groups/get-order-groups.md) |
| `/portfolio/order_groups/{id}` | GET | Yes | Get group. Docs: [Get Order Group](https://docs.kalshi.com/api-reference/order-groups/get-order-group.md) |
| `/portfolio/order_groups/{id}` | DELETE | Yes | Delete group. Docs: [Delete Order Group](https://docs.kalshi.com/api-reference/order-groups/delete-order-group.md) |
| `/portfolio/order_groups/{id}/reset` | POST | Yes | Reset counter. Docs: [Reset Order Group](https://docs.kalshi.com/api-reference/order-groups/reset-order-group.md) |
| `/portfolio/order_groups/{id}/trigger` | POST | Yes | Manually trigger. Docs: [Trigger Order Group](https://docs.kalshi.com/api-reference/order-groups/trigger-order-group.md) |
| `/portfolio/order_groups/{id}/limit` | PUT | Yes | Update limit. Docs: [Update Order Group Limit](https://docs.kalshi.com/api-reference/order-groups/update-order-group-limit.md) |

### Communications / RFQ (Authenticated)

| Endpoint | Method | Auth | Description |
|---|---|---|---|
| `/communications/id` | GET | Yes | Get your comms ID. Docs: [Get Communications ID](https://docs.kalshi.com/api-reference/communications/get-communications-id.md) |
| `/rfqs` | POST | Yes | Create RFQ (max 100 open). Docs: [Create RFQ](https://docs.kalshi.com/api-reference/communications/create-rfq.md) |
| `/rfqs` | GET | Yes | List RFQs. Docs: [Get RFQs](https://docs.kalshi.com/api-reference/communications/get-rfqs.md) |
| `/rfqs/{id}` | GET | Yes | Get RFQ. Docs: [Get RFQ](https://docs.kalshi.com/api-reference/communications/get-rfq.md) |
| `/rfqs/{id}` | DELETE | Yes | Delete RFQ. Docs: [Delete RFQ](https://docs.kalshi.com/api-reference/communications/delete-rfq.md) |
| `/quotes` | POST | Yes | Create quote. Docs: [Create Quote](https://docs.kalshi.com/api-reference/communications/create-quote.md) |
| `/quotes` | GET | Yes | List quotes. Docs: [Get Quotes](https://docs.kalshi.com/api-reference/communications/get-quotes.md) |
| `/quotes/{id}` | GET | Yes | Get quote. Docs: [Get Quote](https://docs.kalshi.com/api-reference/communications/get-quote.md) |
| `/quotes/{id}` | DELETE | Yes | Delete quote. Docs: [Delete Quote](https://docs.kalshi.com/api-reference/communications/delete-quote.md) |
| `/quotes/{id}/accept` | POST | Yes | Accept quote. Docs: [Accept Quote](https://docs.kalshi.com/api-reference/communications/accept-quote.md) |
| `/quotes/{id}/confirm` | POST | Yes | Confirm quote. Docs: [Confirm Quote](https://docs.kalshi.com/api-reference/communications/confirm-quote.md) |

### Historical Data (Authenticated)

Historical data is for archived markets, orders, and fills that have moved past cutoff timestamps.

| Endpoint | Method | Auth | Description |
|---|---|---|---|
| `/historical/cutoff_timestamps` | GET | Yes | Cutoff boundaries. Docs: [Get Historical Cutoff Timestamps](https://docs.kalshi.com/api-reference/historical/get-historical-cutoff-timestamps.md) |
| `/historical/markets` | GET | Yes | Archived markets. Docs: [Get Historical Markets](https://docs.kalshi.com/api-reference/historical/get-historical-markets.md) |
| `/historical/markets/{ticker}` | GET | Yes | Single archived market. Docs: [Get Historical Market](https://docs.kalshi.com/api-reference/historical/get-historical-market.md) |
| `/historical/markets/{ticker}/candlesticks` | GET | Yes | Archived candlesticks. Docs: [Get Historical Market Candlesticks](https://docs.kalshi.com/api-reference/historical/get-historical-market-candlesticks.md) |
| `/historical/fills` | GET | Yes | Archived fills. Docs: [Get Historical Fills](https://docs.kalshi.com/api-reference/historical/get-historical-fills.md) |
| `/historical/orders` | GET | Yes | Archived orders. Docs: [Get Historical Orders](https://docs.kalshi.com/api-reference/historical/get-historical-orders.md) |

Historical data guide: <https://docs.kalshi.com/getting_started/historical_data.md>

### Multivariate Collections

| Endpoint | Method | Auth | Description |
|---|---|---|---|
| `/multivariate/collections` | GET | No | List collections. Docs: [Get Multivariate Event Collections](https://docs.kalshi.com/api-reference/multivariate/get-multivariate-event-collections.md) |
| `/multivariate/collections/{ticker}` | GET | No | Get collection. Docs: [Get Multivariate Event Collection](https://docs.kalshi.com/api-reference/multivariate/get-multivariate-event-collection.md) |
| `/multivariate/collections/{ticker}/markets` | POST | Yes | Create market in collection. Docs: [Create Market In Multivariate Event Collection](https://docs.kalshi.com/api-reference/multivariate/create-market-in-multivariate-event-collection.md) |
| `/multivariate/collections/{ticker}/lookup` | GET | No | Lookup tickers. Docs: [Lookup Tickers For Market In Multivariate Event Collection](https://docs.kalshi.com/api-reference/multivariate/lookup-tickers-for-market-in-multivariate-event-collection.md) |
| `/multivariate/collections/{ticker}/lookup_history` | GET | No | Recent lookups. Docs: [Get Multivariate Event Collection Lookup History](https://docs.kalshi.com/api-reference/multivariate/get-multivariate-event-collection-lookup-history.md) |

### Milestones & Structured Targets

| Endpoint | Method | Auth | Description |
|---|---|---|---|
| `/milestones` | GET | No | List milestones. Docs: [Get Milestones](https://docs.kalshi.com/api-reference/milestone/get-milestones.md) |
| `/milestones/{id}` | GET | No | Get milestone. Docs: [Get Milestone](https://docs.kalshi.com/api-reference/milestone/get-milestone.md) |
| `/structured_targets` | GET | No | List structured targets. Docs: [Get Structured Targets](https://docs.kalshi.com/api-reference/structured-targets/get-structured-targets.md) |
| `/structured_targets/{id}` | GET | No | Get structured target. Docs: [Get Structured Target](https://docs.kalshi.com/api-reference/structured-targets/get-structured-target.md) |

### Live Data

| Endpoint | Method | Auth | Description |
|---|---|---|---|
| `/live_data/{milestone_id}` | GET | No | Live data for milestone. Docs: [Get Live Data](https://docs.kalshi.com/api-reference/live-data/get-live-data.md) |
| `/live_data` | GET | No | Multiple milestones. Docs: [Get Multiple Live Data](https://docs.kalshi.com/api-reference/live-data/get-multiple-live-data.md) |

### Search & Discovery

| Endpoint | Method | Auth | Description |
|---|---|---|---|
| `/search/sports/filters` | GET | No | Sport filters. Docs: [Get Filters for Sports](https://docs.kalshi.com/api-reference/search/get-filters-for-sports.md) |
| `/search/tags` | GET | No | Tags by category. Docs: [Get Tags for Series Categories](https://docs.kalshi.com/api-reference/search/get-tags-for-series-categories.md) |

### Exchange & Account

| Endpoint | Method | Auth | Description |
|---|---|---|---|
| `/exchange/status` | GET | No | Exchange status. Docs: [Get Exchange Status](https://docs.kalshi.com/api-reference/exchange/get-exchange-status.md) |
| `/exchange/schedule` | GET | No | Exchange schedule. Docs: [Get Exchange Schedule](https://docs.kalshi.com/api-reference/exchange/get-exchange-schedule.md) |
| `/exchange/announcements` | GET | No | Announcements. Docs: [Get Exchange Announcements](https://docs.kalshi.com/api-reference/exchange/get-exchange-announcements.md) |
| `/exchange/data_timestamp` | GET | Yes | Data freshness timestamp. Docs: [Get User Data Timestamp](https://docs.kalshi.com/api-reference/exchange/get-user-data-timestamp.md) |
| `/exchange/series_fee_changes` | GET | No | Fee changes. Docs: [Get Series Fee Changes](https://docs.kalshi.com/api-reference/exchange/get-series-fee-changes.md) |
| `/account/api_limits` | GET | Yes | Your rate limit tier. Docs: [Get Account API Limits](https://docs.kalshi.com/api-reference/account/get-account-api-limits.md) |
| `/account/api_keys` | GET | Yes | List API keys. Docs: [Get API Keys](https://docs.kalshi.com/api-reference/api-keys/get-api-keys.md) |
| `/account/api_keys` | POST | Yes | Create API key. Docs: [Create API Key](https://docs.kalshi.com/api-reference/api-keys/create-api-key.md) |
| `/account/api_keys/generate` | POST | Yes | Generate key pair. Docs: [Get API Keys](https://docs.kalshi.com/api-reference/api-keys/generate-api-key.md) |
| `/account/api_keys/{id}` | DELETE | Yes | Delete API key. Docs: [Delete API Key](https://docs.kalshi.com/api-reference/api-keys/delete-api-key.md) |

### Incentive Programs

| Endpoint | Method | Auth | Description |
|---|---|---|---|
| `/incentives` | GET | No | List incentives. Docs: [Get Incentives](https://docs.kalshi.com/api-reference/incentive-programs/get-incentives.md) |

---

## WebSocket API

A single authenticated WebSocket connection provides real-time streaming. Subscribe to channels by sending JSON commands.

### Connection

```
wss://api.elections.kalshi.com/trade-api/ws/v2      (production)
wss://demo-api.kalshi.co/trade-api/ws/v2            (demo)
```

Authentication headers (`KALSHI-ACCESS-KEY`, `KALSHI-ACCESS-SIGNATURE`, `KALSHI-ACCESS-TIMESTAMP`) must be included during the handshake. Sign the string `{timestamp}GET/trade-api/ws/v2`.

### Available Channels

| Channel | Auth Required | Description | Docs |
|---|---|---|---|
| `ticker` | No* | Market price/volume/OI updates | [Market Ticker](https://docs.kalshi.com/websockets/market-ticker.md) |
| `trade` | No* | Public trade notifications | [Public Trades](https://docs.kalshi.com/websockets/public-trades.md) |
| `market_lifecycle_v2` | No* | Market/event state changes | [Market & Event Lifecycle](https://docs.kalshi.com/websockets/market-&-event-lifecycle.md) |
| `multivariate` | No* | Multivariate lookup notifications | [Multivariate Lookups](https://docs.kalshi.com/websockets/multivariate-lookups.md) |
| `orderbook_delta` | Yes | Real-time orderbook updates | [Orderbook Updates](https://docs.kalshi.com/websockets/orderbook-updates.md) |
| `fill` | Yes | Your fill notifications | [User Fills](https://docs.kalshi.com/websockets/user-fills.md) |
| `order` | Yes | Your order updates | [User Orders](https://docs.kalshi.com/websockets/user-orders.md) |
| `market_positions` | Yes | Your position updates | [Market Positions](https://docs.kalshi.com/websockets/market-positions.md) |
| `communications` | Yes | RFQ/quote notifications | [Communications](https://docs.kalshi.com/websockets/communications.md) |
| `order_group_updates` | Yes | Order group lifecycle | [Order Group Updates](https://docs.kalshi.com/websockets/order-group-updates.md) |

*The connection itself always requires authentication, even for public channels.

### Subscribe Command

```json
{
  "id": 1,
  "cmd": "subscribe",
  "params": {
    "channels": ["ticker", "orderbook_delta"],
    "market_tickers": ["KXHIGHNY-24JAN01-T60"]
  }
}
```

### Keep-Alive

Kalshi sends Ping frames every 10 seconds with body `heartbeat`. Clients must respond with Pong frames. Docs: [Connection Keep-Alive](https://docs.kalshi.com/websockets/connection-keep-alive.md)

Full WebSocket guide: <https://docs.kalshi.com/getting_started/quick_start_websockets.md>

---

## Orderbook Structure

Kalshi orderbooks return **bids only** (no asks). In binary markets:

- A **YES bid at X¢** = a **NO ask at (100−X)¢**
- A **NO bid at Y¢** = a **YES ask at (100−Y)¢**

Each entry is `[price, quantity]` sorted ascending. The best bid is the **last** element.

**Spread calculation:**
- Best YES ask = `100 - best_no_bid`
- Spread = Best YES ask − Best YES bid

Full guide: <https://docs.kalshi.com/getting_started/orderbook_responses.md>

---

## FIX Protocol

Kalshi also supports the Financial Information eXchange (FIX) protocol for low-latency trading:

| Topic | Docs |
|---|---|
| Overview | <https://docs.kalshi.com/fix/index.md> |
| Connectivity | <https://docs.kalshi.com/fix/connectivity.md> |
| Session Management | <https://docs.kalshi.com/fix/session-management.md> |
| Order Entry | <https://docs.kalshi.com/fix/order-entry.md> |
| Order Groups | <https://docs.kalshi.com/fix/order-groups.md> |
| Drop Copy | <https://docs.kalshi.com/fix/drop-copy.md> |
| Market Settlement | <https://docs.kalshi.com/fix/market-settlement.md> |
| RFQ Messages | <https://docs.kalshi.com/fix/rfq-messages.md> |
| Error Handling | <https://docs.kalshi.com/fix/error-handling.md> |
| Subpenny Pricing | <https://docs.kalshi.com/fix/subpenny-pricing.md> |

---

## Common Patterns

### Fetch All Open Markets for a Series

```bash
curl -s "https://api.elections.kalshi.com/trade-api/v2/markets?series_ticker=KXHIGHNY&status=open" | jq '.markets[] | {ticker, title, yes_price, volume}'
```

### Get Orderbook for a Market

```bash
curl -s "https://api.elections.kalshi.com/trade-api/v2/markets/KXHIGHNY-24JAN01-T60/orderbook" | jq '.orderbook'
```

### Paginate Through All Results

```bash
# First page
curl -s "https://api.elections.kalshi.com/trade-api/v2/markets?limit=100" > page1.json
# Extract cursor for next page
CURSOR=$(jq -r '.cursor' page1.json)
# Next page
curl -s "https://api.elections.kalshi.com/trade-api/v2/markets?limit=100&cursor=$CURSOR" > page2.json
```

---

## Usage Tips

- **Always check `llms.txt` first:** <https://docs.kalshi.com/llms.txt> has every endpoint and guide.
- **Use the demo environment** for testing — credentials are separate from production.
- **Never hardcode API keys** — use environment variables or secure key storage.
- **Prices are in cents** (1–99). Monetary values in WebSocket position channels are in **centi-cents** (divide by 10,000 for dollars).
- **Sign paths without query parameters.** Strip everything after `?` before signing.
- **Handle pagination** — always check for a non-null `cursor` and loop until exhausted.
- **Respect rate limits** — implement exponential backoff on 429 responses.
- **Combine REST + WebSocket** for the most accurate state: use REST for initial snapshots and WebSocket for real-time deltas.
- **Orderbook is bids-only** — derive asks via the 100−price complement.
- **Historical vs. Live data:** Check cutoff timestamps to know whether to query live or historical endpoints.
- For market status values, use: `unopened`, `open`, `closed`, `settled`.
- **Batch operations** count against per-second write limits per item.

---

## Error Handling

Standard HTTP error codes apply. The API returns JSON error bodies with descriptive messages. Implement retry with backoff for 429 (rate limited) and 5xx (server errors).

### WebSocket Error Codes

| Code | Meaning |
|---|---|
| 1 | Unable to process message |
| 2 | Params required |
| 3 | Channels required |
| 5 | Unknown command |
| 8 | Unknown channel name |
| 9 | Authentication required |
| 14 | Market ticker required |
| 16 | Market not found |
| 17 | Internal error |
| 18 | Command timeout |

Full error code table: <https://docs.kalshi.com/getting_started/quick_start_websockets.md>

---

## Example Project: Alph Bot

[**Alph Bot**](https://gitlab.com/outsharp/shipp/alph-bot) is an open-source automated trading bot that demonstrates a production-quality integration of the Kalshi API alongside [Shipp](https://shipp.ai) for real-time sports data and Claude AI for probability estimation.

### How Alph Bot Uses Kalshi

1. **Market discovery** — Searches for Kalshi event contracts related to a live sports game (e.g., NBA point spreads, totals).
2. **Orderbook reading** — Fetches orderbook data to determine current market-implied probabilities (prices in cents map directly to implied %).
3. **Edge detection** — Compares Kalshi market prices against AI-estimated probabilities powered by Claude + Shipp real-time game data.
4. **Order execution** — Places limit orders when sufficient edge is found, using Kelly Criterion for position sizing.
5. **Risk management** — Enforces circuit breakers (max daily loss), position size limits, single-market exposure caps, and minimum account balance thresholds.

### Alph Bot's Kalshi Configuration

From its `.env.example`:

```
ALPH_BOT_KALSHI_API_KEY_ID=abc123
ALPH_BOT_KALSHI_PRIVATE_KEY_PATH=./keys/kalshi-private.pem

# Strategy
ALPH_BOT_MIN_EDGE_PCT=5
ALPH_BOT_MIN_CONFIDENCE=medium
ALPH_BOT_KELLY_FRACTION=0.25

# Risk controls
ALPH_BOT_MAX_TOTAL_EXPOSURE_USD=10000
ALPH_BOT_MAX_POSITION_SIZE_USD=1000
ALPH_BOT_MAX_SINGLE_MARKET_PERCENT=20
ALPH_BOT_MAX_DAILY_LOSS_USD=500
ALPH_BOT_MAX_DAILY_TRADES=50
ALPH_BOT_MIN_ACCOUNT_BALANCE_USD=100
```

### Try It

```bash
git clone https://gitlab.com/outsharp/shipp/alph-bot.git
cd alph-bot
cp .env.example .env
# Add your Kalshi, Shipp, and Anthropic API keys

yarn migrate

# Find a game to trade on
./index.ts available-games --sport NBA

# Run value betting in demo mode (uses Kalshi demo environment)
./index.ts value-bet -d --game <GAME_ID>

# Run in paper mode (no real orders executed)
./index.ts value-bet --paper --game <GAME_ID>
```

> **Warning:** Trading on Kalshi involves real money when not in demo/paper mode. Always start with a [demo account](https://help.kalshi.com/account/demo-account).

See the [Alph Bot README](https://gitlab.com/outsharp/shipp/alph-bot) for full setup instructions.

---

## Versioning

The current API version is **v2** under `/trade-api/v2`. Monitor the [API Changelog](https://docs.kalshi.com/changelog/index.md) for updates. SDK versions align with the [OpenAPI spec](https://docs.kalshi.com/openapi.yaml) and are generally published weekly.