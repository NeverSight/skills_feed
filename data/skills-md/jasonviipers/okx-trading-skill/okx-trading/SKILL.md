---
name: okx-trading
description: Implement and maintain the OKX broker/provider integration for this workspace using okx-api SDK best practices, including auth/signing, spot/margin/futures/options trading, market/account endpoints, rate limiting, websocket subscriptions, and OKX error handling. Use when adding or changing any code under src/providers/okx or when an LLM needs canonical SDK usage patterns derived from .trae/okx-api-llm.txt.
---

# OKX Provider Broker Skill

Use this workflow when editing `src/providers/okx/*`.

## 1. Load only needed references

- For SDK usage patterns and method names, read `references/okx-sdk-usage.md`.
- For error-to-action mapping, read `references/okx-error-map.md`.
- For full source context, consult `.trae/okx-api-llm.txt` only for missing details.

## 2. Keep architecture compatibility

- Preserve compatibility with `src/providers/types.ts` (`BrokerProvider`, `MarketDataProvider`, `OptionsProvider`).
- Put OKX-specific expanded APIs behind OKX provider interfaces (for example `OkxTradingProvider`) while keeping generic provider methods working.
- Ensure `src/providers/broker-factory.ts` can return OKX providers without adapter breakage.

## 3. Enforce auth and signing rules

- Require all three credentials: API key, secret, passphrase.
- Use OKX signing prehash: `timestamp + UPPERCASE_METHOD + requestPathWithQuery + rawBody`.
- Use HMAC SHA256 base64 signing for both REST and private websocket auth via `customSignMessageFn`.
- Pass `demoTrading: true` for simulated trading.

## 4. Trading and market coverage minimums

- Trading: spot, margin, swap/futures, options order placement + cancel/query + list.
- Account: balances, positions, bills/transactions, fills.
- Market data: ticker(s), order book, trades, candles, instruments.
- Websocket: ticker, orderbook, trades, candles, account/orders/positions subscriptions.

## 5. Error and rate-limit behavior

- Parse and map OKX `code` + `msg` errors into internal error categories.
- Handle known auth/order/risk/rate-limit codes explicitly.
- Apply request throttling + retry with exponential backoff and jitter for retryable failures.
- Avoid retrying invalid input/auth failures.

## 6. Documentation requirements for code changes

- Update `src/providers/okx/README.md` with examples that match current method names.
- Include one example each for: spot order, futures order, option order, account history, websocket subscription.
- Keep examples SDK-realistic and aligned with `references/okx-sdk-usage.md`.
