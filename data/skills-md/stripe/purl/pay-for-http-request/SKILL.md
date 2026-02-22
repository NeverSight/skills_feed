---
name: pay-for-http-request
description: Make HTTP requests with automatic x402 payment support using the purl command line interface.
---
# pay-for-http-request

Make HTTP requests with automatic x402 payment support using `purl`.

## Description

This skill enables making HTTP requests to payment-gated APIs using `purl`, a curl-like CLI tool that automatically handles x402-based payments on EVM and Solana networks.

## When to Use This Skill

When an API returns HTTP 402 (Payment Required) and supports the x402 payment protocol, purl can automatically negotiate and execute the payment to access the resource.

### Common Scenarios

| Scenario | Example |
|----------|---------|
| Tool calls | Paying per request to an API service |
| Premium data feeds | Accessing real-time market data, weather, or analytics |
| Content monetization | Paying to access paywalled articles or media |
| Compute resources | On-demand access to compute or storage services |

### When NOT to Use

- Regular HTTP requests that don't require payment (use `curl` instead)
- APIs using traditional payment methods (credit cards, API keys with billing)

## Usage

```bash
purl <URL> [OPTIONS]
purl <COMMAND>
```

## Commands

| Command | Description |
|---------|-------------|
| `wallet` | Manage wallets (keystores) |
| `config` | Manage configuration |
| `balance` | Check wallet balance |
| `inspect` | Inspect payment requirements without executing |
| `networks` | Manage and inspect supported networks |
| `version` | Show version information |
| `completions` | Generate shell completions script |
| `topics` | Display help topics (exit-codes, formatting, examples, environment) |

## Request Options

### Payment Options

| Option | Description |
|--------|-------------|
| `--max-amount <AMOUNT>` | Maximum amount willing to pay (in atomic units) |
| `--confirm` | Require confirmation before paying |
| `--network <NETWORKS>` | Filter to specific networks (comma-separated) |
| `--dry-run` | Preview payment without executing |

### Display Options

| Option | Description |
|--------|-------------|
| `-v, --verbosity` | Verbosity level (can be used multiple times: -v, -vv, -vvv) |
| `-q, --quiet` / `-s, --silent` | Do not print log messages |
| `-i, --include` | Include HTTP headers in output |
| `-I, --head` | Show only HTTP headers |
| `-o, --output <FILE>` | Write output to file |
| `--output-format <FORMAT>` | Output format: auto, text, json, yaml (auto detects: text for terminal, json for pipes) |
| `--color <MODE>` | Control color output: auto, always, never |

### HTTP Options

| Option | Description |
|--------|-------------|
| `-X, --request <METHOD>` | Custom request method |
| `-H, --header <HEADER>` | Add custom header |
| `-A, --user-agent <AGENT>` | Set user agent |
| `-L, --location` | Follow redirects |
| `--connect-timeout <SECONDS>` | Connection timeout in seconds |
| `-m, --max-time <SECONDS>` | Maximum time for the request |
| `-d, --data <DATA>` | POST data |
| `--json <JSON>` | Send JSON data with Content-Type header |

### Wallet Options

| Option | Description |
|--------|-------------|
| `--wallet <PATH>` | Path to wallet file |
| `--password <PASSWORD>` | Password for wallet decryption |
| `--private-key <KEY>` | Raw private key (hex, for EVM; use wallet for better security) |

### Global Options

| Option | Description |
|--------|-------------|
| `-C, --config <PATH>` | Configuration file path |

## Wallet Commands

```bash
purl wallet <COMMAND>
```

| Command | Description |
|---------|-------------|
| `list` | List available wallets |
| `add` | Create a new wallet (interactive) |
| `show <NAME>` | Show wallet details |
| `verify <NAME>` | Verify wallet integrity |
| `use <NAME>` | Set a wallet as the active payment method |
| `remove <NAME>` | Remove a wallet |

### Wallet Add Options

| Option | Description |
|--------|-------------|
| `-n, --name <NAME>` | Name for the wallet |
| `-t, --wallet-type <TYPE>` | Wallet type: evm or solana |
| `-k, --private-key <KEY>` | Private key to import (hex for EVM, base58 for Solana) |

## Config Commands

```bash
purl config [COMMAND]
```

| Command | Description |
|---------|-------------|
| (none) | Show current config |
| `get <KEY>` | Get a specific configuration value (supports dot notation) |
| `validate` | Validate configuration file |

## Examples

### Basic payment request
```bash
purl https://api.example.com/premium-data
```

### Preview payment without executing
```bash
purl --dry-run https://api.example.com/data
```

### Require confirmation before payment
```bash
purl --confirm https://api.example.com/data
```

### Set maximum payment amount
```bash
purl --max-amount 10000 https://api.example.com/data
```

### Filter to specific network
```bash
purl --network base-sepolia https://api.example.com/data
```

### Verbose output with headers
```bash
purl -vi https://api.example.com/data
```

### Save output to file as JSON
```bash
purl -o output.json --output-format json https://api.example.com/data
```

### POST request with JSON data
```bash
purl --json '{"key": "value"}' https://api.example.com/data
```

### Custom headers
```bash
purl -H "Authorization: Bearer token" https://api.example.com/data
```

### Follow redirects with custom method
```bash
purl -L -X POST https://api.example.com/data
```

### Check wallet balance
```bash
purl balance
purl balance --network base
```

### Inspect payment requirements
```bash
purl inspect https://api.example.com/endpoint
```

### Wallet management
```bash
purl wallet add                      # Interactive wallet creation
purl wallet add --type evm           # Skip type selection
purl wallet add --type solana -k KEY # Import existing key
purl wallet list                     # List all wallets
purl wallet use my-wallet            # Switch active wallet
```

### View supported networks
```bash
purl networks
purl networks info base
```

## Supported Networks

| Type | Networks |
|------|----------|
| EVM | ethereum, ethereum-sepolia, base, base-sepolia, avalanche, avalanche-fuji, polygon, arbitrum, optimism |
| SVM | solana, solana-devnet |

## Prerequisites

1. Create a wallet: `purl wallet add`
2. Set up a payment method (wallet) with funds on the desired network
3. Ensure the target API supports x402 payment protocol

## Environment Variables

| Variable | Description |
|----------|-------------|
| `PURL_MAX_AMOUNT` | Default maximum amount willing to pay |
| `PURL_NETWORK` | Default network filter |
| `PURL_CONFIRM` | Default confirmation behavior (true/false) |
| `PURL_KEYSTORE` | Default wallet/keystore path |
| `PURL_PASSWORD` | Wallet password (for non-interactive use) |
