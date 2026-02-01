---
name: keys-manager
description: Manage exchange API keys and credentials for Hummingbot trading. Use this skill when the user wants to add, remove, or list API credentials for exchanges like Binance, Coinbase, Kraken, etc.
metadata:
  author: fengtality
---

# keys-manager

This skill manages exchange API keys and credentials for Hummingbot. It uses **progressive disclosure** to guide users through the setup process step by step.

## Prerequisites

- Hummingbot API server must be running (use the setup skill first)
- API server credentials (default: admin/admin)

## Quick Start: Setup Connector (Progressive Disclosure)

The `setup_connector.sh` script uses a 4-step progressive flow:

### Step 1: List Available Exchanges

```bash
./scripts/setup_connector.sh
```

Shows all available connectors and current account status.

### Step 2: Show Required Credentials

```bash
./scripts/setup_connector.sh --connector binance
```

Shows what credential fields are required for that exchange.

### Step 3: Select Account

```bash
./scripts/setup_connector.sh --connector binance \
    --credentials '{"binance_api_key":"YOUR_KEY","binance_api_secret":"YOUR_SECRET"}'
```

Shows available accounts and prompts you to select one.

### Step 4: Connect

```bash
./scripts/setup_connector.sh --connector binance \
    --credentials '{"binance_api_key":"YOUR_KEY","binance_api_secret":"YOUR_SECRET"}' \
    --account master_account
```

Completes the connection. Use `--force` to override existing credentials.

## Other Scripts

### List All Connectors

```bash
./scripts/list_connectors.sh
```

### Get Connector Requirements

```bash
./scripts/get_connector_config.sh --connector binance
```

### Add Credentials Directly

```bash
./scripts/add_credentials.sh \
    --connector binance \
    --account master_account \
    --credentials '{"binance_api_key": "KEY", "binance_api_secret": "SECRET"}'
```

### Remove Credentials

```bash
./scripts/remove_credentials.sh \
    --connector binance \
    --account master_account
```

### List Account Credentials

```bash
./scripts/list_account_credentials.sh --account master_account
```

## Supported Exchanges

### Centralized Exchanges (CEX)

| Exchange | Connector Name | Required Fields |
|----------|----------------|-----------------|
| Binance | `binance` | api_key, api_secret |
| Binance Perpetual | `binance_perpetual` | api_key, api_secret |
| Coinbase | `coinbase_advanced_trade` | api_key, api_secret |
| Kraken | `kraken` | api_key, api_secret |
| KuCoin | `kucoin` | api_key, api_secret, passphrase |
| Gate.io | `gate_io` | api_key, api_secret |
| OKX | `okx` | api_key, api_secret, passphrase |
| Bybit | `bybit` | api_key, api_secret |
| Hyperliquid | `hyperliquid_perpetual` | address, secret_key |

## Security Notes

- **Never log credentials** - credentials should only be passed to scripts, never echoed
- **Credentials are encrypted** - Hummingbot encrypts all stored credentials
- **API key permissions** - recommend users create keys with minimal required permissions

## API Endpoints Used

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/connectors/` | GET | List available connectors |
| `/connectors/{name}/config-map` | GET | Get required credential fields |
| `/accounts/` | GET | List accounts |
| `/accounts/{name}/credentials` | GET | List account credentials |
| `/accounts/{name}/credentials` | POST | Add credentials |
| `/accounts/{name}/credentials/{connector}` | DELETE | Remove credentials |

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| "Invalid credentials" | Wrong API key/secret | Verify credentials are correct |
| "Connector not found" | Typo in connector name | Use Step 1 to see valid names |
| "Account not found" | Account doesn't exist | Use default "master_account" |
| "Credentials already exist" | Connector already configured | Use --force to override |
