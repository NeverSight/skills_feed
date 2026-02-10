---
name: connectors-available
description: Check which exchanges work from your location and search for tokens with trading rules (min order size, price increment, order types).
metadata:
  author: hummingbot
---

# connectors-available

Test which exchange connectors are accessible from your location and search for tokens across all available exchanges. Shows trading rules including minimum order sizes, price increments, and supported order types.

## Workflow

### Step 1: Test Connectors

Ask user which connectors to test:
- All connectors
- Spot only
- Perpetual only
- Specific exchanges

### Step 2: Run Tests & Save Rules

```bash
./scripts/test_all.sh --timeout 10
```

Fetches trading rules from each connector. If data returns, it's accessible. Results saved to `data/trading_rules.json`.

### Step 3: Search for Tokens

When user asks about a token, search and display the trading rules table:

```bash
./scripts/search_token.sh --token BTC
```

**Always show the full table to the user:**

```
| Exchange | Pair | Min Order | Min Price Inc | Order Types |
|----------|------|-----------|---------------|-------------|
| hyperliquid_perpetual | BTC-USD | 0.00001 | 0.1 | Limit, Market |
| okx_perpetual | BTC-USDT | 0.0001 | 0.1 | Limit, Market |
| kraken | BTC-USD | 0.0001 | 0.1 | Limit, Market |
| coinbase_advanced_trade | BTC-USD | 0.0001 | 0.01 | Limit, Market |
| kucoin | BTC-USDT | 0.00001 | 0.1 | Limit, Market |
| gate_io | BTC-USDT | 0.0001 | 0.01 | Limit, Market |

Found 488 pairs containing BTC
```

## Trading Rules Explained

- **Min Order**: Minimum order size in base currency
- **Min Price Inc**: Minimum price increment (tick size)
- **Order Types**: Supported order types (Limit, Market)

## Scripts

**Test all connectors:**
```bash
./scripts/test_all.sh --timeout 10
```

**Test specific connectors:**
```bash
./scripts/test_all.sh --connectors "kraken,okx,hyperliquid" --timeout 10
```

**Search for a token:**
```bash
./scripts/search_token.sh --token BTC
./scripts/search_token.sh --token SOL
./scripts/search_token.sh --token HBOT
```

## Output Files

- `data/trading_rules.json` - All trading pairs and rules from available exchanges

## Requirements

- Hummingbot API running (default: localhost:8000)
- API credentials (default: admin/admin)

## Environment Variables

```bash
export API_URL=localhost:8000
export API_USER=admin
export API_PASS=admin
```
