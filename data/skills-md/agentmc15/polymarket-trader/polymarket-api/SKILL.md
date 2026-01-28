---
name: polymarket-api
description: Deep integration guide for Polymarket's CLOB API, Gamma API, and on-chain data. Use when building trading functionality, fetching market data, or implementing order execution.
---

# Polymarket API Integration Skill

## Overview

This skill provides comprehensive guidance for integrating with Polymarket's APIs and smart contracts.

## API Endpoints

### CLOB API (Central Limit Order Book)
Base URL: `https://clob.polymarket.com`

#### Authentication Levels
- **Level 0 (Public)**: Market data, orderbooks, prices
- **Level 1 (Signer)**: Create/derive API keys
- **Level 2 (Authenticated)**: Trading, orders, positions

#### Key Endpoints
```
GET  /markets              # List all markets
GET  /markets/{token_id}   # Get specific market
GET  /price?token_id=X     # Get current price
GET  /midpoint?token_id=X  # Get midpoint price
GET  /book?token_id=X      # Get orderbook
GET  /trades               # Get user trades
POST /order                # Place order
DELETE /order/{id}         # Cancel order
GET  /positions            # Get positions
```

### Gamma API (Market Metadata)
Base URL: `https://gamma-api.polymarket.com`

```
GET /events              # List events
GET /events/{slug}       # Get event details
GET /markets             # List markets
GET /markets/{id}        # Get market details
```

## Python Implementation Patterns

### Initialize Client
```python
from py_clob_client.client import ClobClient
from py_clob_client.clob_types import OrderArgs, OrderType
import os

class PolymarketService:
    def __init__(self):
        self.client = ClobClient(
            host="https://clob.polymarket.com",
            key=os.getenv("POLYMARKET_PRIVATE_KEY"),
            chain_id=137,
            signature_type=1,
            funder=os.getenv("POLYMARKET_FUNDER_ADDRESS")
        )
        self.client.set_api_creds(
            self.client.create_or_derive_api_creds()
        )
    
    async def get_market_data(self, token_id: str) -> dict:
        """Fetch comprehensive market data."""
        return {
            "price": self.client.get_price(token_id, "BUY"),
            "midpoint": self.client.get_midpoint(token_id),
            "book": self.client.get_order_book(token_id),
            "spread": self.client.get_spread(token_id),
        }
    
    async def place_order(
        self,
        token_id: str,
        side: str,
        price: float,
        size: float,
        order_type: str = "GTC"
    ) -> dict:
        """Place a limit order."""
        order = self.client.create_order(
            OrderArgs(
                token_id=token_id,
                price=price,
                size=size,
                side=side,
            )
        )
        return self.client.post_order(order, order_type)
```

### WebSocket Subscription
```python
import asyncio
import websockets
import json

async def subscribe_market_updates(token_ids: list[str]):
    """Subscribe to real-time market updates."""
    uri = "wss://ws-subscriptions-clob.polymarket.com/ws/market"
    
    async with websockets.connect(uri) as ws:
        await ws.send(json.dumps({
            "type": "subscribe",
            "markets": token_ids
        }))
        
        async for message in ws:
            data = json.loads(message)
            yield data
```

### Gamma API Client
```python
import httpx

class GammaClient:
    BASE_URL = "https://gamma-api.polymarket.com"
    
    def __init__(self):
        self.client = httpx.AsyncClient(base_url=self.BASE_URL)
    
    async def get_active_markets(self) -> list[dict]:
        """Fetch all active markets."""
        response = await self.client.get("/markets", params={"active": True})
        return response.json()
    
    async def get_event(self, slug: str) -> dict:
        """Fetch event with all markets."""
        response = await self.client.get(f"/events/{slug}")
        return response.json()
```

## Order Types

- **GTC** (Good Till Cancelled): Stays until filled or cancelled
- **GTD** (Good Till Date): Expires at specified time
- **FOK** (Fill or Kill): Must fill entirely or cancel
- **IOC** (Immediate or Cancel): Fill what's available, cancel rest

## Price Calculations

```python
def calculate_implied_probability(price: float) -> float:
    """Convert price to implied probability."""
    return price  # Prices ARE probabilities (0-1)

def calculate_cost(price: float, shares: float) -> float:
    """Calculate cost to buy shares."""
    return price * shares

def calculate_pnl(
    entry_price: float,
    current_price: float,
    shares: float,
    side: str
) -> float:
    """Calculate unrealized P&L."""
    if side == "BUY":
        return (current_price - entry_price) * shares
    return (entry_price - current_price) * shares
```

## Error Handling

```python
from py_clob_client.exceptions import PolymarketException

try:
    result = client.post_order(order)
except PolymarketException as e:
    if "INSUFFICIENT_BALANCE" in str(e):
        # Handle insufficient funds
        pass
    elif "INVALID_PRICE" in str(e):
        # Handle price out of range
        pass
    raise
```

## Rate Limits

- Public endpoints: ~100 requests/minute
- Authenticated endpoints: ~1000 requests/minute
- WebSocket: Varies by subscription type

Always implement exponential backoff and request queuing.

## Key Contract Addresses (Polygon)

```python
CONTRACTS = {
    "CTF_EXCHANGE": "0x4bFb41d5B3570DeFd03C39a9A4D8dE6Bd8B8982E",
    "NEG_RISK_CTF_EXCHANGE": "0xC5d563A36AE78145C45a50134d48A1215220f80a",
    "CONDITIONAL_TOKENS": "0x4D97DCd97eC945f40cF65F87097ACe5EA0476045",
    "USDC": "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174",
}
```
