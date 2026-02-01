---
name: portfolio
description: View portfolio balances, positions, and history across all connected exchanges. Use this skill when the user wants to check their balance, see positions, view portfolio distribution, or track portfolio history.
metadata:
  author: fengtality
---

# portfolio

This skill provides portfolio visibility across all connected exchanges and accounts.

## Prerequisites

- Hummingbot API server must be running
- Exchange credentials configured via keys-manager skill

## Quick Start

### Get Current Portfolio State

```bash
./scripts/get_state.sh
```

Filter by specific connectors:
```bash
./scripts/get_state.sh --connector hyperliquid_perpetual
```

Force refresh balances from exchange:
```bash
./scripts/get_state.sh --refresh
```

### Get Portfolio Distribution

See token allocation across accounts:
```bash
./scripts/get_distribution.sh
```

### Get Portfolio History

View historical portfolio values:
```bash
./scripts/get_history.sh --days 7
```

With interval sampling:
```bash
./scripts/get_history.sh --days 30 --interval 1d
```

### Get Full Portfolio Overview

Combined view with balances, positions, and orders:
```bash
./scripts/get_overview.sh
```

## Scripts

### get_state.sh

Fetches current portfolio state with token balances.

```bash
./scripts/get_state.sh [OPTIONS]

Options:
  --account ACCOUNT      Filter by account name (default: all)
  --connector CONNECTOR  Filter by connector name
  --refresh              Force refresh from exchange (slower but accurate)
  --skip-gateway         Skip Gateway wallets (faster for CEX-only)
```

### get_distribution.sh

Shows portfolio distribution by token with percentages.

```bash
./scripts/get_distribution.sh [OPTIONS]

Options:
  --account ACCOUNT      Filter by account name
  --connector CONNECTOR  Filter by connector name
```

### get_history.sh

Retrieves historical portfolio data with pagination.

```bash
./scripts/get_history.sh [OPTIONS]

Options:
  --days DAYS           Number of days of history (default: 7)
  --interval INTERVAL   Data granularity: 5m, 15m, 30m, 1h, 4h, 12h, 1d (default: 1h)
  --account ACCOUNT     Filter by account name
  --connector CONNECTOR Filter by connector name
  --limit LIMIT         Max records to return (default: 100)
```

### get_overview.sh

Comprehensive portfolio view including:
- Token balances
- Perpetual positions
- Active orders

```bash
./scripts/get_overview.sh [OPTIONS]

Options:
  --account ACCOUNT      Filter by account name
  --connector CONNECTOR  Filter by connector name
  --no-balances          Skip token balances
  --no-positions         Skip perpetual positions
  --no-orders            Skip active orders
```

## Output Examples

### Portfolio State
```json
{
  "accounts": {
    "master_account": {
      "hyperliquid_perpetual": {
        "balances": {
          "USDC": {"total": 1000.0, "available": 850.0}
        }
      }
    }
  },
  "total_value_usd": 1000.0
}
```

### Portfolio Distribution
```json
{
  "tokens": {
    "USDC": {
      "total_value": 1000.0,
      "percentage": 100.0,
      "accounts": ["master_account"]
    }
  }
}
```

### Portfolio History
```json
{
  "data": [
    {"timestamp": 1706400000, "total_value": 1000.0},
    {"timestamp": 1706486400, "total_value": 1050.0}
  ],
  "interval": "1d",
  "period": "7d"
}
```

## API Endpoints Used

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/portfolio/state` | POST | Get current portfolio state |
| `/portfolio/distribution` | POST | Get token distribution |
| `/portfolio/history` | POST | Get historical data |
| `/trading/{account}/{connector}/orders` | GET | Get active orders |
| `/trading/{account}/{connector}/positions` | GET | Get perpetual positions |

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `API_URL` | `http://localhost:8000` | API base URL |
| `API_USER` | `admin` | API username |
| `API_PASS` | `admin` | API password |
