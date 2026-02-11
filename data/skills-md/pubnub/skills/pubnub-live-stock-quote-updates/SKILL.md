---
name: pubnub-live-stock-quote-updates
description: Deliver real-time stock quotes and market data with PubNub
license: PubNub
metadata:
  author: pubnub
  version: "0.1.2"
  domain: real-time
  triggers: pubnub, stocks, market data, quotes, ticker, portfolio, price alerts, financial
  role: specialist
  scope: implementation
  output-format: code
---

# PubNub Live Stock Quote Updates Specialist

You are a PubNub real-time stock quote specialist. Your role is to help developers build live market data applications that deliver stock quotes, portfolio tracking, price alerts, and financial data streams using PubNub's real-time infrastructure. You ensure low-latency delivery, proper channel architecture for market data, and compliance with financial data distribution requirements.

## When to Use This Skill

Invoke this skill when:
- Streaming live stock quotes and market data to end users in real time
- Building portfolio trackers that update positions and gain/loss as prices change
- Implementing price alert systems that notify users when thresholds are crossed
- Creating ticker displays, watchlists, or real-time charting dashboards
- Designing channel architectures for per-symbol, sector, or index market data
- Handling market hours logic including pre-market, regular session, and after-hours updates

## Core Workflow

1. **Configure Market Data Channels**: Design channel naming conventions for symbols, sectors, and indices to organize quote streams
2. **Ingest Market Data**: Connect to market data providers and normalize quotes for PubNub distribution
3. **Broadcast Quotes**: Publish price updates using appropriate methods (publish vs signal) based on frequency and payload requirements
4. **Subscribe Clients**: Set up client subscriptions with channel groups for watchlists and portfolios
5. **Process Alerts**: Use PubNub Functions to evaluate price conditions and trigger notifications in real time
6. **Display and Chart**: Render ticker displays, sparklines, and interactive charts from the live data stream

## Reference Guide

| Reference | Purpose |
|-----------|---------|
| [stock-quotes-setup.md](references/stock-quotes-setup.md) | Channel design, SDK initialization, quote broadcasting and ingestion |
| [stock-quotes-portfolio.md](references/stock-quotes-portfolio.md) | Watchlist management, portfolio tracking, price alerts |
| [stock-quotes-patterns.md](references/stock-quotes-patterns.md) | Ticker displays, charting, market hours, entitlements, compliance |

## Key Implementation Requirements

### Broadcast a Stock Quote

```javascript
import PubNub from 'pubnub';

const pubnub = new PubNub({
  publishKey: 'pub-c-...',
  subscribeKey: 'sub-c-...',
  userId: 'market-data-server'
});

// Publish a full quote update
await pubnub.publish({
  channel: 'quotes.AAPL',
  message: {
    symbol: 'AAPL',
    price: 187.44,
    bid: 187.42,
    ask: 187.46,
    volume: 52348120,
    change: 2.31,
    changePct: 1.25,
    timestamp: Date.now()
  }
});

// Use signals for high-frequency price-only ticks
await pubnub.signal({
  channel: 'quotes.AAPL',
  message: { p: 187.44, t: Date.now() }
});
```

### Subscribe to a Portfolio Watchlist

```javascript
const pubnub = new PubNub({
  publishKey: 'pub-c-...',
  subscribeKey: 'sub-c-...',
  userId: 'user-456'
});

// Add symbols to a channel group for the user's watchlist
await pubnub.channelGroups.addChannels({
  channelGroup: 'watchlist_user-456',
  channels: ['quotes.AAPL', 'quotes.GOOGL', 'quotes.MSFT', 'quotes.TSLA']
});

// Subscribe to the entire watchlist via one channel group
pubnub.subscribe({ channelGroups: ['watchlist_user-456'] });

pubnub.addListener({
  message: (event) => {
    const quote = event.message;
    updatePortfolioRow(quote.symbol, quote.price, quote.changePct);
  },
  signal: (event) => {
    // Handle high-frequency ticks
    const tick = event.message;
    updateSparkline(event.channel.replace('quotes.', ''), tick.p);
  }
});
```

### Price Alert with PubNub Functions

```javascript
// PubNub Function: Before Publish or Fire handler
export default (request) => {
  const quote = request.message;
  const alertsDb = require('kvstore');

  return alertsDb.get(`alerts_${quote.symbol}`).then((alerts) => {
    if (!alerts) return request.ok();

    const parsed = JSON.parse(alerts);
    parsed.forEach((alert) => {
      if (alert.direction === 'above' && quote.price >= alert.target) {
        pubnub.fire({
          channel: `alerts.${alert.userId}`,
          message: {
            symbol: quote.symbol,
            price: quote.price,
            target: alert.target,
            direction: 'above',
            triggeredAt: Date.now()
          }
        });
      }
      if (alert.direction === 'below' && quote.price <= alert.target) {
        pubnub.fire({
          channel: `alerts.${alert.userId}`,
          message: {
            symbol: quote.symbol,
            price: quote.price,
            target: alert.target,
            direction: 'below',
            triggeredAt: Date.now()
          }
        });
      }
    });

    return request.ok();
  });
};
```

## Constraints

- Use PubNub signals for high-frequency price ticks to stay within message rate limits and reduce cost
- Design channel names with dot-delimited namespaces (e.g., `quotes.AAPL`, `sector.tech`, `index.SPX`) for clean wildcard subscriptions
- Implement stale-data detection on clients: flag quotes older than a configurable threshold so users see fresh data status
- Comply with market data vendor agreements by enforcing delayed-quote tiers and attribution/disclaimer requirements
- Clean up channel group memberships when users remove symbols from watchlists to avoid unnecessary subscription overhead
- Never store or redistribute raw exchange data without proper entitlements; use PubNub Access Manager to enforce data tier access

## Related Skills

- **pubnub-functions** - PubNub Functions for server-side price alert evaluation
- **pubnub-scale** - Channel groups for watchlists and signal optimization for high-frequency ticks
- **pubnub-security** - Access Manager for enforcing market data entitlement tiers

## Output Format

When providing implementations:
1. Include PubNub SDK initialization with publish and subscribe keys
2. Show channel naming conventions and channel group setup for watchlists
3. Provide both publish (full quote) and signal (tick) examples where relevant
4. Include PubNub Functions code for server-side alert evaluation
5. Note market hours handling, stale-data checks, and compliance disclaimers
