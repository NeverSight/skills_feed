---
name: kalshi-trading
description: Trade on Kalshi prediction markets. Use when user wants to check markets, analyze odds, view positions, place orders, or research prediction market opportunities. Kalshi is a regulated exchange for event contracts.
---

# Kalshi Trading

Trade on [Kalshi](https://kalshi.com), a CFTC-regulated prediction market exchange. This skill enables you to query markets, analyze probabilities, manage positions, and execute trades.

## Types

```typescript
interface Market {
  ticker: string;
  title: string;
  status: string;
  yes_bid?: number;
  yes_ask?: number;
  volume?: number;
  close_time?: string;
}

interface Orderbook {
  yes: [number, number][]; // [price_cents, quantity]
  no: [number, number][];
}

interface Balance {
  balance: number; // cents
  payout: number;  // pending settlement
}

interface Position {
  ticker: string;
  position: number; // positive = YES, negative = NO
  market_exposure: number;
}

interface Order {
  order_id: string;
  ticker: string;
  side: "yes" | "no";
  action: "buy" | "sell";
  count: number;
  status: string;
}
```

## Quick Start

```typescript
import * as crypto from "crypto";

const API_BASE = "https://api.elections.kalshi.com/trade-api/v2";

// See AUTHENTICATION.md for full setup
function getAuthHeaders(
  apiKey: string,
  privateKeyPem: string,
  method: string,
  path: string
): Record<string, string> {
  const timestamp = Date.now().toString();
  const message = `${timestamp}${method}${path}`;

  const sign = crypto.createSign("RSA-SHA256");
  sign.update(message);
  const signature = sign.sign(privateKeyPem, "base64");

  return {
    "KALSHI-ACCESS-KEY": apiKey,
    "KALSHI-ACCESS-SIGNATURE": signature,
    "KALSHI-ACCESS-TIMESTAMP": timestamp,
    "Content-Type": "application/json",
  };
}
```

## Common Operations

### Search Markets

```typescript
async function searchMarkets(query: string, limit = 10): Promise<Market[]> {
  const url = new URL(`${API_BASE}/markets`);
  url.searchParams.set("status", "open");
  url.searchParams.set("limit", String(limit));

  const response = await fetch(url.toString());
  const data = await response.json();

  // Filter by query in title
  return data.markets.filter((m: Market) =>
    m.title.toLowerCase().includes(query.toLowerCase())
  );
}
```

### Get Market Details

```typescript
async function getMarket(ticker: string): Promise<Market> {
  const response = await fetch(`${API_BASE}/markets/${ticker}`);
  const data = await response.json();
  return data.market;
}
```

### Get Orderbook

```typescript
async function getOrderbook(ticker: string): Promise<Orderbook> {
  const response = await fetch(`${API_BASE}/markets/${ticker}/orderbook`);
  const data = await response.json();
  return data.orderbook;
}
```

### Check Balance (Authenticated)

```typescript
async function getBalance(
  apiKey: string,
  privateKeyPem: string
): Promise<Balance> {
  const path = "/portfolio/balance";
  const headers = getAuthHeaders(apiKey, privateKeyPem, "GET", path);

  const response = await fetch(`${API_BASE}${path}`, { headers });
  return response.json();
}
```

### Get Positions (Authenticated)

```typescript
async function getPositions(
  apiKey: string,
  privateKeyPem: string
): Promise<Position[]> {
  const path = "/portfolio/positions";
  const headers = getAuthHeaders(apiKey, privateKeyPem, "GET", path);

  const response = await fetch(`${API_BASE}${path}`, { headers });
  const data = await response.json();
  return data.market_positions;
}
```

### Place Order (Authenticated)

```typescript
async function placeOrder(
  apiKey: string,
  privateKeyPem: string,
  ticker: string,
  side: "yes" | "no",
  action: "buy" | "sell",
  count: number,
  price: number // In cents (1-99)
): Promise<Order> {
  const path = "/portfolio/orders";
  const headers = getAuthHeaders(apiKey, privateKeyPem, "POST", path);

  const body = {
    ticker,
    side,
    action,
    count,
    type: "limit",
    ...(side === "yes" ? { yes_price: price } : { no_price: price }),
  };

  const response = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers,
    body: JSON.stringify(body),
  });
  const data = await response.json();
  return data.order;
}
```

## Key Concepts

- **Markets**: Event contracts with Yes/No outcomes (e.g., "Will X happen by Y date?")
- **Prices**: Quoted in cents (1-99), representing probability percentage
- **Positions**: Your holdings in Yes or No contracts
- **Settlement**: Markets resolve to $1.00 (Yes wins) or $0.00 (No wins)

## Additional Resources

- [AUTHENTICATION.md](AUTHENTICATION.md) - Detailed API key setup
- [API_REFERENCE.md](API_REFERENCE.md) - Full endpoint documentation
- [scripts/kalshi-client.ts](scripts/kalshi-client.ts) - Ready-to-use TypeScript client

## Tips

1. **Start with market research**: Use `searchMarkets()` to explore opportunities
2. **Check liquidity**: Review orderbook depth before placing large orders
3. **Use limit orders**: Avoid market orders to control execution price
4. **Monitor positions**: Regularly check your positions and P&L
