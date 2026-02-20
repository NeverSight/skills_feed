---
name: polymarket
description: >
  Polymarket is a decentralized prediction market platform built on Polygon.
  Use this skill to interact with the Polymarket APIs for market discovery,
  price data, order placement, portfolio management, WebSocket streaming,
  and bridging/withdrawals.

metadata:
  author: Outsharp Inc.
  version: 0.1.0

compatibility:
  requirements:
    - Internet access
    - Node.js 16+ (for TypeScript SDK) or Python 3.7+ (for Python SDK) or Rust (for Rust SDK)
    - An Ethereum private key (for authenticated/trading operations)
  notes:
    - All read endpoints (markets, events, prices, orderbooks) are public and require no authentication.
    - Trading endpoints require two-level authentication (L1 wallet signature → L2 API credentials via HMAC-SHA256).
    - Polymarket operates on Polygon (Chain ID 137). Collateral is USDCe (Bridged USDC).
    - Prices range from 0.00 to 1.00 and represent implied probabilities. Winning tokens redeem for $1 USDCe.
    - All orders are limit orders (can be marketable). Order types include GTC, GTD, FOK, and FAK.

allowed-tools:
  - Bash(curl:*)
  - Bash(jq:*)
  - Bash(python*:*)
  - Bash(pip*:*)
  - Bash(npm*:*)
  - Bash(npx*:*)
  - Bash(cargo*:*)

---

# Polymarket API

[Polymarket](https://polymarket.com) is a decentralized prediction market where users trade on the outcomes of real-world events. It uses a hybrid-decentralized Central Limit Order Book (CLOB) with off-chain matching and on-chain settlement on Polygon.

Check this skill and the [official documentation](https://docs.polymarket.com) _FREQUENTLY_. The canonical machine-readable index of all docs lives at:

> **<https://docs.polymarket.com/llms.txt>**

Always consult `llms.txt` to discover every available page before building. It is the single source of truth for endpoint references, SDK docs, WebSocket channels, builder program details, and getting-started guides.

---

## Key Concepts (Glossary)

| Term | Definition |
|---|---|
| **Event** | A collection of related markets grouped under a common topic (e.g., "2024 US Presidential Election"). |
| **Market** | A single tradeable binary outcome within an event. Each market has Yes and No sides, a condition ID, question ID, and pair of token IDs. |
| **Token** | Represents a position in a specific outcome (Yes or No). Prices range from 0.00 to 1.00. Winning tokens redeem for $1 USDCe. Also called *outcome token*. |
| **Token ID** | The unique identifier for a specific outcome token. Required when placing orders or querying prices. |
| **Condition ID** | On-chain identifier for a market's resolution condition. Used in CTF operations and as the market identifier in the CLOB. |
| **Question ID** | Identifier linking a market to its resolution oracle (UMA). |
| **Slug** | Human-readable URL identifier for a market or event (e.g., `polymarket.com/event/[slug]`). |
| **CLOB** | Central Limit Order Book — Polymarket's off-chain order matching system. Orders are matched here before on-chain settlement. |
| **Tick Size** | Minimum price increment for a market. Usually `0.01` (1 cent) or `0.001` (0.1 cent). |
| **Fill** | When an order is matched and executed. Orders can be partially or fully filled. |
| **Negative Risk (NegRisk)** | A multi-outcome event where only one outcome can resolve Yes. Requires `negRisk: true` in order parameters. |
| **CTF** | Conditional Token Framework — the on-chain smart contracts that manage outcome tokens. |
| **Split** | Convert USDCe into a complete set of outcome tokens (one Yes + one No). |
| **Merge** | Convert a complete set of outcome tokens back into USDCe. |
| **Redeem** | After resolution, exchange winning tokens for $1 USDCe each. |
| **USDCe** | Bridged USDC on Polygon — the stablecoin used as collateral on Polymarket. |
| **Funder Address** | The wallet address that holds funds and tokens for trading. |
| **Signature Type** | Identifies wallet type: `0` = EOA, `1` = Magic Link proxy (POLY_PROXY), `2` = Gnosis Safe proxy. |

Full glossary: <https://docs.polymarket.com/quickstart/reference/glossary.md>

---

## Order Types

| Type | Name | Description |
|---|---|---|
| **GTC** | Good-Til-Cancelled | Remains open until filled or manually cancelled. |
| **GTD** | Good-Til-Date | Expires at a specified time if not filled. |
| **FOK** | Fill-Or-Kill | Must be filled entirely and immediately, or cancelled. No partial fills. |
| **FAK** | Fill-And-Kill | Fills as much as possible immediately, then cancels any remaining unfilled portion. |

---

## Base URLs

| API | Base URL | Description |
|---|---|---|
| **CLOB API** | `https://clob.polymarket.com` | Order management, prices, orderbooks, trading |
| **Gamma API** | `https://gamma-api.polymarket.com` | Market discovery, metadata, events, tags |
| **Data API** | `https://data-api.polymarket.com` | User positions, activity, trade history |
| **CLOB WebSocket** | `wss://ws-subscriptions-clob.polymarket.com/ws/` | Orderbook updates, order status |
| **RTDS WebSocket** | `wss://ws-live-data.polymarket.com` | Low-latency crypto prices, comments |

Endpoints reference: <https://docs.polymarket.com/quickstart/reference/endpoints.md>

---

## Documentation & References

All detailed examples, request/response schemas, and walkthroughs live in the official docs. Always consult these before building:

| Resource | URL |
|---|---|
| **Full documentation index (llms.txt)** | <https://docs.polymarket.com/llms.txt> |
| Developer Quickstart | <https://docs.polymarket.com/quickstart/overview.md> |
| Fetching Market Data | <https://docs.polymarket.com/quickstart/fetching-data.md> |
| Placing Your First Order | <https://docs.polymarket.com/quickstart/first-order.md> |
| API Rate Limits | <https://docs.polymarket.com/quickstart/introduction/rate-limits.md> |
| Endpoints Reference | <https://docs.polymarket.com/quickstart/reference/endpoints.md> |
| Glossary | <https://docs.polymarket.com/quickstart/reference/glossary.md> |
| CLOB Introduction | <https://docs.polymarket.com/developers/CLOB/introduction.md> |
| Authentication | <https://docs.polymarket.com/developers/CLOB/authentication.md> |
| Client Methods Overview | <https://docs.polymarket.com/developers/CLOB/clients/methods-overview.md> |
| Public Methods | <https://docs.polymarket.com/developers/CLOB/clients/methods-public.md> |
| L1 Methods | <https://docs.polymarket.com/developers/CLOB/clients/methods-l1.md> |
| L2 Methods | <https://docs.polymarket.com/developers/CLOB/clients/methods-l2.md> |
| Orders Overview | <https://docs.polymarket.com/developers/CLOB/orders/orders.md> |
| Place Single Order | <https://docs.polymarket.com/developers/CLOB/orders/create-order.md> |
| Place Multiple Orders | <https://docs.polymarket.com/developers/CLOB/orders/create-order-batch.md> |
| Cancel Orders | <https://docs.polymarket.com/developers/CLOB/orders/cancel-orders.md> |
| WebSocket Overview | <https://docs.polymarket.com/developers/CLOB/websocket/wss-overview.md> |
| Market Channel | <https://docs.polymarket.com/developers/CLOB/websocket/market-channel.md> |
| User Channel | <https://docs.polymarket.com/developers/CLOB/websocket/user-channel.md> |
| Gamma Structure | <https://docs.polymarket.com/developers/gamma-markets-api/gamma-structure.md> |
| How to Fetch Markets | <https://docs.polymarket.com/developers/gamma-markets-api/fetch-markets-guide.md> |
| Negative Risk Overview | <https://docs.polymarket.com/developers/neg-risk/overview.md> |
| CTF Overview | <https://docs.polymarket.com/developers/CTF/overview.md> |
| Builder Program | <https://docs.polymarket.com/developers/builders/builder-intro.md> |
| Market Makers Introduction | <https://docs.polymarket.com/developers/market-makers/introduction.md> |
| Bridge Overview | <https://docs.polymarket.com/developers/misc-endpoints/bridge-overview.md> |
| Polymarket Platform | <https://polymarket.com> |

---

## Authentication

Polymarket uses a **two-level authentication** system. Public endpoints (market data, prices, orderbooks) require no authentication.

### L1 Authentication (Private Key)

L1 uses the wallet's private key to sign an EIP-712 message. It proves ownership of the wallet and is used to **create or derive L2 API credentials**.

**L1 Headers (for direct REST calls):**

| Header | Description |
|---|---|
| `POLY_ADDRESS` | Polygon signer address |
| `POLY_SIGNATURE` | EIP-712 signature |
| `POLY_TIMESTAMP` | Current UNIX timestamp |
| `POLY_NONCE` | Nonce (default 0) |

The `POLY_SIGNATURE` is generated by signing an EIP-712 struct with domain `ClobAuthDomain` (version `1`, chainId `137`).

**TypeScript example:**

```typescript
import { ClobClient } from "@polymarket/clob-client";
import { Wallet } from "ethers"; // v5.8.0

const HOST = "https://clob.polymarket.com";
const CHAIN_ID = 137; // Polygon mainnet
const signer = new Wallet(process.env.PRIVATE_KEY);

const client = new ClobClient(HOST, CHAIN_ID, signer);
const apiCreds = await client.createOrDeriveApiKey();
// Returns: { apiKey, secret, passphrase }
```

**Python example:**

```python
from py_clob_client.client import ClobClient
import os

client = ClobClient(
    host="https://clob.polymarket.com",
    chain_id=137,
    key=os.getenv("PRIVATE_KEY"),
)
api_creds = client.create_or_derive_api_creds()
# Returns: { "apiKey": "...", "secret": "...", "passphrase": "..." }
```

Full L1 auth details: <https://docs.polymarket.com/developers/CLOB/authentication.md>

### L2 Authentication (API Credentials)

L2 uses the API credentials (apiKey, secret, passphrase) derived from L1. Requests are signed with **HMAC-SHA256** using the `secret`.

**L2 Headers (for direct REST calls):**

| Header | Description |
|---|---|
| `POLY_ADDRESS` | Polygon signer address |
| `POLY_SIGNATURE` | HMAC-SHA256 signature |
| `POLY_TIMESTAMP` | Current UNIX timestamp |
| `POLY_API_KEY` | User's API `apiKey` value |
| `POLY_PASSPHRASE` | User's API `passphrase` value |

**TypeScript example (full L2 client):**

```typescript
import { ClobClient } from "@polymarket/clob-client";
import { Wallet } from "ethers"; // v5.8.0

const signer = new Wallet(process.env.PRIVATE_KEY);
const apiCreds = {
  apiKey: process.env.API_KEY,
  secret: process.env.SECRET,
  passphrase: process.env.PASSPHRASE,
};

const client = new ClobClient(
  "https://clob.polymarket.com",
  137,
  signer,
  apiCreds,
  2,  // Signature type: 0=EOA, 1=POLY_PROXY, 2=GNOSIS_SAFE
  process.env.FUNDER_ADDRESS, // proxy wallet address
);
```

**Python example (full L2 client):**

```python
from py_clob_client.client import ClobClient
from py_clob_client.clob_types import ApiCreds
import os

api_creds = ApiCreds(
    api_key=os.getenv("API_KEY"),
    api_secret=os.getenv("SECRET"),
    api_passphrase=os.getenv("PASSPHRASE"),
)

client = ClobClient(
    host="https://clob.polymarket.com",
    chain_id=137,
    key=os.getenv("PRIVATE_KEY"),
    creds=api_creds,
    signature_type=2,  # 0=EOA, 1=POLY_PROXY, 2=GNOSIS_SAFE
    funder=os.getenv("FUNDER_ADDRESS"),
)
```

### Signature Types

| Type | Value | Description |
|---|---|---|
| EOA | 0 | Standard Ethereum wallet. Funder is the EOA address. Needs POL for gas. |
| POLY_PROXY | 1 | Magic Link email/Google login proxy wallet. User must export PK from Polymarket.com. |
| GNOSIS_SAFE | 2 | Gnosis Safe multisig proxy wallet. Most common for Polymarket.com users. |

Full auth guide: <https://docs.polymarket.com/developers/CLOB/authentication.md>

---

## SDKs

Polymarket provides official SDKs. Prefer these for production integrations:

| SDK | Install | Source |
|---|---|---|
| TypeScript | `npm install @polymarket/clob-client` | [GitHub](https://github.com/Polymarket/clob-client) |
| Python | `pip install py-clob-client` | [GitHub](https://github.com/Polymarket/py-clob-client) |
| Rust | `cargo add polymarket-client-sdk` | — |

For builders routing orders for users, also install:

| Package | Install | Purpose |
|---|---|---|
| Builder Signing SDK | `npm install @polymarket/builder-signing-sdk` | Builder order attribution |

---

## Rate Limits

Polymarket uses Cloudflare-based throttling (requests are delayed, not immediately rejected). Key limits:

### General

| Endpoint | Limit |
|---|---|
| General Rate Limiting | 15,000 requests / 10s |

### Gamma API

| Endpoint | Limit |
|---|---|
| Gamma (General) | 4,000 / 10s |
| `/events` | 500 / 10s |
| `/markets` | 300 / 10s |
| `/markets` & `/events` listing | 900 / 10s |
| Search | 350 / 10s |
| Tags | 200 / 10s |
| Comments | 200 / 10s |

### CLOB API

| Endpoint | Limit |
|---|---|
| CLOB (General) | 9,000 / 10s |
| `/book` | 1,500 / 10s |
| `/price` | 1,500 / 10s |
| `/midprice` | 1,500 / 10s |
| `/books`, `/prices`, `/midprices` | 500 / 10s |
| Price History | 1,000 / 10s |

### CLOB Trading

| Endpoint | Burst Limit | Sustained Limit |
|---|---|---|
| POST `/order` | 3,500 / 10s (500/s) | 36,000 / 10min (60/s) |
| DELETE `/order` | 3,000 / 10s (300/s) | 30,000 / 10min (50/s) |
| POST `/orders` (batch) | 1,000 / 10s (100/s) | 15,000 / 10min (25/s) |
| DELETE `/orders` (batch) | 1,000 / 10s (100/s) | 15,000 / 10min (25/s) |
| DELETE `/cancel-all` | 250 / 10s (25/s) | 6,000 / 10min (10/s) |

### Data API

| Endpoint | Limit |
|---|---|
| Data API (General) | 1,000 / 10s |
| `/trades` | 200 / 10s |
| `/positions` | 150 / 10s |
| `/closed-positions` | 150 / 10s |

Full rate limits: <https://docs.polymarket.com/quickstart/introduction/rate-limits.md>

---

## REST API Endpoints Overview

Below is a summary organized by API. For full request/response schemas, see the linked docs or browse <https://docs.polymarket.com/llms.txt>.

### Gamma API — Market Discovery & Metadata

Base: `https://gamma-api.polymarket.com`

| Endpoint | Method | Description | Docs |
|---|---|---|---|
| `/events` | GET | List events (filter by `active`, `closed`, `tag_id`, `series_id`, etc.) | [List Events](https://docs.polymarket.com/api-reference/events/list-events.md) |
| `/events/{id}` | GET | Get event by ID | [Get Event by ID](https://docs.polymarket.com/api-reference/events/get-event-by-id.md) |
| `/events/{slug}` | GET | Get event by slug | [Get Event by Slug](https://docs.polymarket.com/api-reference/events/get-event-by-slug.md) |
| `/events/tags` | GET | Get event tags | [Get Event Tags](https://docs.polymarket.com/api-reference/events/get-event-tags.md) |
| `/markets` | GET | List markets (filter by various criteria) | [List Markets](https://docs.polymarket.com/api-reference/markets/list-markets.md) |
| `/markets/{id}` | GET | Get market by ID | [Get Market by ID](https://docs.polymarket.com/api-reference/markets/get-market-by-id.md) |
| `/markets/{slug}` | GET | Get market by slug | [Get Market by Slug](https://docs.polymarket.com/api-reference/markets/get-market-by-slug.md) |
| `/tags` | GET | List tags | [List Tags](https://docs.polymarket.com/api-reference/tags/list-tags.md) |
| `/tags/{id}` | GET | Get tag by ID | [Get Tag by ID](https://docs.polymarket.com/api-reference/tags/get-tag-by-id.md) |
| `/tags/{slug}` | GET | Get tag by slug | [Get Tag by Slug](https://docs.polymarket.com/api-reference/tags/get-tag-by-slug.md) |
| `/series` | GET | List series | [List Series](https://docs.polymarket.com/api-reference/series/list-series.md) |
| `/series/{id}` | GET | Get series by ID | [Get Series by ID](https://docs.polymarket.com/api-reference/series/get-series-by-id.md) |
| `/sports` | GET | Get sports metadata | [Get Sports Metadata](https://docs.polymarket.com/api-reference/sports/get-sports-metadata-information.md) |
| `/sports/market-types` | GET | Get valid sports market types | [Get Valid Sports Market Types](https://docs.polymarket.com/api-reference/sports/get-valid-sports-market-types.md) |
| `/teams` | GET | List teams | [List Teams](https://docs.polymarket.com/api-reference/sports/list-teams.md) |
| `/search` | GET | Search markets, events, and profiles | [Search](https://docs.polymarket.com/api-reference/search/search-markets-events-and-profiles.md) |
| `/comments` | GET | List comments | [List Comments](https://docs.polymarket.com/api-reference/comments/list-comments.md) |
| `/profiles/{address}` | GET | Get public profile by wallet address | [Get Profile](https://docs.polymarket.com/api-reference/profiles/get-public-profile-by-wallet-address.md) |

Gamma structure guide: <https://docs.polymarket.com/developers/gamma-markets-api/gamma-structure.md>

### CLOB API — Pricing & Orderbooks (Public)

Base: `https://clob.polymarket.com`

| Endpoint | Method | Auth | Description | Docs |
|---|---|---|---|---|
| `/price` | GET | No | Get current price for a token and side | [Get Market Price](https://docs.polymarket.com/api-reference/pricing/get-market-price.md) |
| `/prices` | POST | No | Get prices for multiple tokens and sides | [Get Multiple Market Prices](https://docs.polymarket.com/api-reference/pricing/get-multiple-market-prices-by-request.md) |
| `/midpoint` | GET | No | Get midpoint price for a token | [Get Midpoint Price](https://docs.polymarket.com/api-reference/pricing/get-midpoint-price.md) |
| `/book` | GET | No | Get order book for a token | [Get Order Book Summary](https://docs.polymarket.com/api-reference/orderbook/get-order-book-summary.md) |
| `/books` | POST | No | Get order books for multiple tokens | [Get Multiple Order Books](https://docs.polymarket.com/api-reference/orderbook/get-multiple-order-books-summaries-by-request.md) |
| `/prices-history` | GET | No | Get historical price data for a token | [Get Price History](https://docs.polymarket.com/api-reference/pricing/get-price-history-for-a-traded-token.md) |
| `/spreads` | GET | No | Get bid-ask spreads for multiple tokens | [Get Bid-Ask Spreads](https://docs.polymarket.com/api-reference/spreads/get-bid-ask-spreads.md) |

### CLOB API — Trading (Authenticated)

Base: `https://clob.polymarket.com`

| Endpoint | Method | Auth | Description | Docs |
|---|---|---|---|---|
| `/order` | POST | L2 | Place a single order | [Place Single Order](https://docs.polymarket.com/developers/CLOB/orders/create-order.md) |
| `/order` | DELETE | L2 | Cancel a single order | [Cancel Orders](https://docs.polymarket.com/developers/CLOB/orders/cancel-orders.md) |
| `/orders` | POST | L2 | Place multiple orders (batch, up to 15) | [Place Multiple Orders](https://docs.polymarket.com/developers/CLOB/orders/create-order-batch.md) |
| `/orders` | DELETE | L2 | Cancel multiple orders | [Cancel Orders](https://docs.polymarket.com/developers/CLOB/orders/cancel-orders.md) |
| `/cancel-all` | DELETE | L2 | Cancel all open orders | [Cancel Orders](https://docs.polymarket.com/developers/CLOB/orders/cancel-orders.md) |
| `/cancel-market-orders` | DELETE | L2 | Cancel all orders for a specific market | [Cancel Orders](https://docs.polymarket.com/developers/CLOB/orders/cancel-orders.md) |

### CLOB API — Orders & Trades (Authenticated)

| Endpoint | Method | Auth | Description | Docs |
|---|---|---|---|---|
| `/data/order/{orderId}` | GET | L2 | Get a specific order | [Get Order](https://docs.polymarket.com/developers/CLOB/orders/get-order.md) |
| `/data/orders` | GET | L2 | Get active/open orders | [Get Active Orders](https://docs.polymarket.com/developers/CLOB/orders/get-active-order.md) |
| `/data/trades` | GET | L2 | Get user's trades | [Get Trades](https://docs.polymarket.com/developers/CLOB/trades/trades.md) |
| `/order/scoring` | GET | L2 | Check order reward scoring eligibility | [Check Scoring](https://docs.polymarket.com/developers/CLOB/orders/check-scoring.md) |

### CLOB API — Auth Endpoints

| Endpoint | Method | Auth | Description |
|---|---|---|---|
| `/auth/api-key` | POST | L1 | Create new API credentials |
| `/auth/derive-api-key` | GET | L1 | Derive existing API credentials |
| `/auth/api-keys` | GET | L2 | List API keys |
| `/auth/api-key` | DELETE | L2 | Delete/revoke an API key |

### Data API — Positions & Activity

Base: `https://data-api.polymarket.com`

| Endpoint | Method | Description | Docs |
|---|---|---|---|
| `/positions` | GET | Get current positions for a user | [Get Current Positions](https://docs.polymarket.com/api-reference/core/get-current-positions-for-a-user.md) |
| `/closed-positions` | GET | Get closed positions for a user | [Get Closed Positions](https://docs.polymarket.com/api-reference/core/get-closed-positions-for-a-user.md) |
| `/positions/market` | GET | Get positions for a market | [Get Positions for Market](https://docs.polymarket.com/api-reference/core/get-positions-for-a-market.md) |
| `/positions/value` | GET | Get total value of a user's positions | [Get Total Value](https://docs.polymarket.com/api-reference/core/get-total-value-of-a-users-positions.md) |
| `/top-holders` | GET | Get top holders for markets | [Get Top Holders](https://docs.polymarket.com/api-reference/core/get-top-holders-for-markets.md) |
| `/trades` | GET | Get trades for a user or markets | [Get Trades](https://docs.polymarket.com/api-reference/core/get-trades-for-a-user-or-markets.md) |
| `/activity` | GET | Get user on-chain activity | [Get User Activity](https://docs.polymarket.com/api-reference/core/get-user-activity.md) |
| `/leaderboard` | GET | Get trader leaderboard rankings | [Get Leaderboard](https://docs.polymarket.com/api-reference/core/get-trader-leaderboard-rankings.md) |
| `/open-interest` | GET | Get open interest | [Get Open Interest](https://docs.polymarket.com/api-reference/misc/get-open-interest.md) |
| `/volume` | GET | Get live volume for an event | [Get Live Volume](https://docs.polymarket.com/api-reference/misc/get-live-volume-for-an-event.md) |

### Bridge API — Deposits & Withdrawals

| Endpoint | Method | Description | Docs |
|---|---|---|---|
| `/deposit` | POST | Create deposit addresses | [Create Deposit Addresses](https://docs.polymarket.com/api-reference/bridge/create-deposit-addresses.md) |
| `/withdraw` | POST | Create withdrawal addresses | [Create Withdrawal Addresses](https://docs.polymarket.com/api-reference/bridge/create-withdrawal-addresses.md) |
| `/supported-assets` | GET | Get supported chains & tokens | [Get Supported Assets](https://docs.polymarket.com/api-reference/bridge/get-supported-assets.md) |
| `/quote` | GET | Get deposit/withdrawal quote | [Get a Quote](https://docs.polymarket.com/api-reference/bridge/get-a-quote.md) |
| `/status` | GET | Get transaction status | [Get Transaction Status](https://docs.polymarket.com/api-reference/bridge/get-transaction-status.md) |

Bridge overview: <https://docs.polymarket.com/developers/misc-endpoints/bridge-overview.md>

### Builder Program Endpoints

| Endpoint | Method | Description | Docs |
|---|---|---|---|
| `/builders/leaderboard` | GET | Get aggregated builder leaderboard | [Builder Leaderboard](https://docs.polymarket.com/api-reference/builders/get-aggregated-builder-leaderboard.md) |
| `/builders/volume` | GET | Get daily builder volume time-series | [Builder Volume](https://docs.polymarket.com/api-reference/builders/get-daily-builder-volume-time-series.md) |

Builder program: <https://docs.polymarket.com/developers/builders/builder-intro.md>

---

## Fees

Current fee schedule (subject to change):

| Volume Level | Maker Fee (bps) | Taker Fee (bps) |
|---|---|---|
| >0 USDC | 0 | 0 |

Fee calculation depends on buying vs. selling:

- **Selling** outcome tokens: `feeQuote = baseRate × min(price, 1 - price) × size`
- **Buying** outcome tokens: `feeBase = baseRate × min(price, 1 - price) × (size / price)`

Fees details: <https://docs.polymarket.com/developers/CLOB/introduction.md>

Maker rebates program: <https://docs.polymarket.com/developers/market-makers/maker-rebates-program.md>

---

## WebSocket API

Polymarket provides two WebSocket services for real-time data.

### CLOB WebSocket

```
wss://ws-subscriptions-clob.polymarket.com/ws/
```

Two channels are available:

| Channel | Auth Required | Description | Docs |
|---|---|---|---|
| `market` | No | Orderbook and price updates (public) | [Market Channel](https://docs.polymarket.com/developers/CLOB/websocket/market-channel.md) |
| `user` | Yes | Order status and trade updates | [User Channel](https://docs.polymarket.com/developers/CLOB/websocket/user-channel.md) |

#### Market Channel Events

| Event Type | Trigger | Description |
|---|---|---|
| `book` | First subscribe / trade | Full orderbook snapshot with bids and asks |
| `price_change` | New order / cancellation | Incremental price level changes with best bid/ask |
| `tick_size_change` | Price > 0.96 or < 0.04 | Minimum tick size update |
| `last_trade_price` | Trade match | Last trade price, side, and size |
| `best_bid_ask` | Best price change | Best bid, ask, and spread (requires `custom_feature_enabled`) |
| `new_market` | Market created | New market details (requires `custom_feature_enabled`) |
| `market_resolved` | Market resolved | Resolution details with winning outcome (requires `custom_feature_enabled`) |

#### User Channel Events

| Event Type | Trigger | Description |
|---|---|---|
| `trade` | Order matched / status change | Trade details with maker orders, status (`MATCHED`, `MINED`, `CONFIRMED`, `RETRYING`, `FAILED`) |
| `order` | Order placed / updated / cancelled | Order details with type (`PLACEMENT`, `UPDATE`, `CANCELLATION`) |

#### Subscription

Send a JSON message upon connection:

```json
{
  "auth": { /* L2 auth for user channel */ },
  "markets": ["0x...conditionId"],
  "assets_ids": ["tokenId1", "tokenId2"],
  "type": "market",
  "custom_feature_enabled": true
}
```

Subscribe/unsubscribe to additional assets after connecting:

```json
{
  "assets_ids": ["tokenId3"],
  "markets": [],
  "operation": "subscribe",
  "custom_feature_enabled": true
}
```

Full WebSocket guide: <https://docs.polymarket.com/developers/CLOB/websocket/wss-overview.md>
WSS Authentication: <https://docs.polymarket.com/developers/CLOB/websocket/wss-auth.md>

### RTDS (Real-Time Data Stream)

```
wss://ws-live-data.polymarket.com
```

Low-latency streaming for crypto prices and comment feeds. Optimized for market makers.

- RTDS Overview: <https://docs.polymarket.com/developers/RTDS/RTDS-overview.md>
- RTDS Crypto Prices: <https://docs.polymarket.com/developers/RTDS/RTDS-crypto-prices.md>
- RTDS Comments: <https://docs.polymarket.com/developers/RTDS/RTDS-comments.md>

### Sports WebSocket

Real-time sports results via WebSocket:

- Overview: <https://docs.polymarket.com/developers/sports-websocket/overview.md>
- Quickstart: <https://docs.polymarket.com/developers/sports-websocket/quickstart.md>
- Message Format: <https://docs.polymarket.com/developers/sports-websocket/message-format.md>

---

## Data Model

### Event → Market → Token Hierarchy

```
Event (e.g., "Who will win the 2024 election?")
├── Market 1 (e.g., "Will Candidate A win?")
│   ├── Token: Yes (token_id: "abc...")  price: 0.65
│   └── Token: No  (token_id: "def...")  price: 0.35
├── Market 2 (e.g., "Will Candidate B win?")
│   ├── Token: Yes (token_id: "ghi...")  price: 0.30
│   └── Token: No  (token_id: "jkl...")  price: 0.70
└── ...
```

- **Prices** are implied probabilities (0.00–1.00). Yes + No prices sum to ≈ $1.
- **`clobTokenIds`** from the Gamma API map to CLOB token IDs needed for trading.
- **`outcomes`** and **`outcomePrices`** arrays are 1:1 mapped.

### Negative Risk Events

Multi-outcome events where only one outcome can resolve "Yes" use the negative risk architecture. A NO share in any market can be converted into 1 YES share in all other markets, enabling capital efficiency.

- `negRisk: true` on the event indicates negative risk.
- `negRiskAugmented: true` means placeholder outcomes can be clarified later.

Full NegRisk docs: <https://docs.polymarket.com/developers/neg-risk/overview.md>

---

## Common Patterns

### Fetch Active Events

```bash
curl -s "https://gamma-api.polymarket.com/events?active=true&closed=false&limit=10" | jq '.[].title'
```

### Get Event Details with Markets

```bash
curl -s "https://gamma-api.polymarket.com/events?slug=will-bitcoin-reach-100k-by-2025" | jq '.[0] | {title, markets: [.markets[] | {question, outcomePrices, clobTokenIds}]}'
```

### Get Current Price for a Token

```bash
curl -s "https://clob.polymarket.com/price?token_id=YOUR_TOKEN_ID&side=buy"
# Returns: { "price": "0.65" }
```

### Get Orderbook Depth

```bash
curl -s "https://clob.polymarket.com/book?token_id=YOUR_TOKEN_ID" | jq '{bids: .bids[:3], asks: .asks[:3]}'
```

### Get Midpoint Price

```bash
curl -s "https://clob.polymarket.com/midpoint?token_id=YOUR_TOKEN_ID"
# Returns: { "mid": "0.655" }
```

### Search for Markets

```bash
curl -s "https://gamma-api.polymarket.com/search?query=bitcoin&limit=5" | jq '.markets[] | {question, slug}'
```

### Discover Sports Markets

```bash
# Get all supported sports leagues
curl -s "https://gamma-api.polymarket.com/sports" | jq '.'

# Get NBA events
curl -s "https://gamma-api.polymarket.com/events?series_id=10345&active=true&closed=false" | jq '.[].title'
```

### Get User Positions (Data API)

```bash
curl -s "https://data-api.polymarket.com/positions?user=0xYOUR_ADDRESS" | jq '.'
```

### Place an Order (TypeScript)

```typescript
import { ClobClient, Side, OrderType } from "@polymarket/clob-client";
import { Wallet } from "ethers";

const client = new ClobClient(
  "https://clob.polymarket.com", 137, signer, apiCreds, 2, funderAddress
);

const market = await client.getMarket("CONDITION_ID");
const response = await client.createAndPostOrder(
  { tokenID: "TOKEN_ID", price: 0.50, size: 10, side: Side.BUY },
  { tickSize: market.tickSize, negRisk: market.negRisk },
  OrderType.GTC
);
console.log("Order ID:", response.orderID);
```

### Place an Order (Python)

```python
from py_clob_client.client import ClobClient
from py_clob_client.clob_types import OrderArgs, OrderType
from py_clob_client.order_builder.constants import BUY

market = client.get_market("CONDITION_ID")
response = client.create_and_post_order(
    OrderArgs(token_id="TOKEN_ID", price=0.50, size=10, side=BUY),
    options={"tick_size": market["tickSize"], "neg_risk": market["negRisk"]},
    order_type=OrderType.GTC,
)
print("Order ID:", response["orderID"])
```

---

## CTF Operations (Split / Merge / Redeem)

The Conditional Token Framework enables conversion between USDCe and outcome tokens:

| Operation | Description | When to Use |
|---|---|---|
| **Split** | USDCe → 1 Yes token + 1 No token | Create inventory for market making |
| **Merge** | 1 Yes token + 1 No token → USDCe | Exit positions, reclaim collateral |
| **Redeem** | Winning token → $1 USDCe | After market resolution |

- Split: <https://docs.polymarket.com/developers/CTF/split.md>
- Merge: <https://docs.polymarket.com/developers/CTF/merge.md>
- Redeem: <https://docs.polymarket.com/developers/CTF/redeem.md>
- Deployment & addresses: <https://docs.polymarket.com/developers/CTF/deployment-resources.md>

---

## Builder Program

Builders are third-party developers who integrate Polymarket into their apps. The program offers permissionless integration with tiered rate limits, rewards, and revenue opportunities.

| Resource | URL |
|---|---|
| Builder Introduction | <https://docs.polymarket.com/developers/builders/builder-intro.md> |
| Builder Profile & Keys | <https://docs.polymarket.com/developers/builders/builder-profile.md> |
| Builder Tiers | <https://docs.polymarket.com/developers/builders/builder-tiers.md> |
| Order Attribution | <https://docs.polymarket.com/developers/builders/order-attribution.md> |
| Builder Methods | <https://docs.polymarket.com/developers/CLOB/clients/methods-builder.md> |
| Relayer Client (gasless txns) | <https://docs.polymarket.com/developers/builders/relayer-client.md> |
| Examples (Next.js) | <https://docs.polymarket.com/developers/builders/examples.md> |

Builder credentials are **separate** from user credentials. You use builder credentials to tag/attribute orders, but each user still needs their own L2 credentials to trade.

---

## Market Making

| Resource | URL |
|---|---|
| Introduction | <https://docs.polymarket.com/developers/market-makers/introduction.md> |
| Setup | <https://docs.polymarket.com/developers/market-makers/setup.md> |
| Trading | <https://docs.polymarket.com/developers/market-makers/trading.md> |
| Inventory Management | <https://docs.polymarket.com/developers/market-makers/inventory.md> |
| Data Feeds | <https://docs.polymarket.com/developers/market-makers/data-feeds.md> |
| Liquidity Rewards | <https://docs.polymarket.com/developers/market-makers/liquidity-rewards.md> |
| Maker Rebates | <https://docs.polymarket.com/developers/market-makers/maker-rebates-program.md> |

---

## Usage Tips

- **Always check `llms.txt` first:** <https://docs.polymarket.com/llms.txt> has every endpoint and guide.
- **Never hardcode private keys** — use environment variables or secure key storage.
- **Prices are probabilities** (0.00–1.00). Winning tokens redeem at $1 USDCe.
- **Use `active=true&closed=false`** when querying events to get only live, tradable markets.
- **Token IDs come from Gamma** — fetch events/markets from Gamma API, then use `clobTokenIds` for CLOB queries and trading.
- **Set `negRisk` correctly** — multi-outcome events use negative risk. Check the event's `negRisk` field and pass it when creating orders.
- **Use the SDK** instead of signing manually — L1/L2 signing is complex (EIP-712 + HMAC-SHA256). The TypeScript and Python clients handle this.
- **Allowances must be set** — before placing orders, the funder address must have USDCe allowance set for the Exchange contract (buying) or conditional token allowance (selling).
- **Combine REST + WebSocket** — use REST for initial state and WebSocket for real-time deltas.
- **Respect rate limits** — implement backoff when throttled. Use batch endpoints (`/books`, `/prices`) to reduce request count.
- **Signature type matters** — type `0` (EOA) for standalone wallets, type `2` (Gnosis Safe) for most Polymarket.com accounts. Incorrect type will cause auth failures.
- **Funder ≠ Signer** for proxy wallets — the funder is the proxy wallet address (visible at polymarket.com/settings), not the private key's EOA address.
- **Geographic restrictions apply** — check <https://docs.polymarket.com/developers/CLOB/geoblock.md> before trading.
- **Order validity is continuously monitored** — balances, allowances, and on-chain cancellations are checked in real time. Abuse leads to blacklisting.

---

## Error Handling

Standard HTTP error codes apply. The API returns JSON error bodies with descriptive messages.

- **Throttled requests** (rate limited): Requests are delayed/queued, not immediately rejected. Implement backoff.
- **Authentication errors**: Verify private key, signature type, funder address, and API credentials match.
- **Insufficient balance**: Check funder address has enough USDCe or conditional tokens, including existing open order commitments.
- **Order rejected**: Max order size = `balance - sum(openOrderSize - fillAmount)` per market.
- **Geographic restriction**: Trading blocked from restricted regions.

---

## Resolution

Markets are resolved by the **UMA Optimistic Oracle**, a smart-contract-based optimistic oracle. Resolution can be disputed via the UMA protocol.

- Resolution overview: <https://docs.polymarket.com/developers/resolution/UMA.md>
- How markets are resolved: <https://docs.polymarket.com/polymarket-learn/markets/how-are-markets-resolved.md>
- How markets are disputed: <https://docs.polymarket.com/polymarket-learn/markets/dispute.md>

---

## On-Chain Resources

| Resource | URL |
|---|---|
| Exchange contract source | [GitHub](https://github.com/Polymarket/ctf-exchange/tree/main/src) |
| Exchange contract docs | [GitHub](https://github.com/Polymarket/ctf-exchange/blob/main/docs/Overview.md) |
| Security audit (Chainsecurity) | [Audit PDF](https://github.com/Polymarket/ctf-exchange/blob/main/audit/ChainSecurity_Polymarket_Exchange_audit.pdf) |
| Negative Risk Adapter | [Polygonscan](https://polygonscan.com/address/0xd91E80cF2E7be2e162c6513ceD06f1dD0dA35296) |
| Subgraph overview | <https://docs.polymarket.com/developers/subgraph/overview.md> |
| Blockchain data resources | <https://docs.polymarket.com/developers/builders/blockchain-data-resources.md> |
| USDC on Polygon | `0x2791bca1f2de4661ed88a30c99a7a9449aa84174` |

---

## Changelog

Monitor the [Polymarket Changelog](https://docs.polymarket.com/changelog/changelog.md) for updates to the CLOB, API, UI, and mobile applications.