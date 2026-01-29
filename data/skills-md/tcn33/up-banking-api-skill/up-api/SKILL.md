---
name: up-api
description: |
  Interact with the Up Banking API to query accounts, transactions, categories, and tags. Use when the user wants to:
  - Check account balances or list accounts
  - Search or filter transactions (by date, category, tag, status)
  - Analyze spending patterns or generate summaries
  - Categorize transactions or manage tags
  - Set up or manage webhooks for real-time notifications
  Requires UP_API_TOKEN environment variable.
---

# Up Banking API

## Setup

Requires `UP_API_TOKEN` environment variable. Get your token at [api.up.com.au](https://api.up.com.au) by scanning the QR code with your Up app.

Verify setup: `python3 scripts/up_api.py ping`

## CLI Usage

All commands support `--json` flag for raw output.

### Accounts

```bash
# List all accounts
python3 scripts/up_api.py accounts

# Filter by type
python3 scripts/up_api.py accounts --type saver

# Get specific account
python3 scripts/up_api.py account <account_id>
```

### Transactions

```bash
# Recent transactions (default 30)
python3 scripts/up_api.py transactions

# Filter by date range (RFC-3339 format required)
python3 scripts/up_api.py transactions --since 2024-01-01T00:00:00Z --until 2024-02-01T00:00:00Z

# Filter by category or tag
python3 scripts/up_api.py transactions --category groceries
python3 scripts/up_api.py transactions --tag "holiday"

# All transactions (paginated)
python3 scripts/up_api.py transactions --all --since 2024-01-01T00:00:00Z
```

### Categories and Tags

```bash
# List categories
python3 scripts/up_api.py categories

# List subcategories
python3 scripts/up_api.py categories --parent good-life

# Categorize a transaction
python3 scripts/up_api.py categorize <tx_id> <category_id>

# List tags
python3 scripts/up_api.py tags

# Add/remove tags
python3 scripts/up_api.py tag <tx_id> "trip" "business"
python3 scripts/up_api.py untag <tx_id> "trip"
```

### Webhooks

```bash
python3 scripts/up_api.py webhooks
python3 scripts/up_api.py webhook-create https://example.com/hook "My webhook"
python3 scripts/up_api.py webhook-ping <webhook_id>
python3 scripts/up_api.py webhook-logs <webhook_id>
python3 scripts/up_api.py webhook-delete <webhook_id>
```

## Spending Analysis

For spending summaries, fetch transactions with `--json --all` and process the output:

```bash
# Get all transactions for a month as JSON
python3 scripts/up_api.py transactions --json --all --since 2024-01-01T00:00:00Z --until 2024-02-01T00:00:00Z
```

Parse the JSON to aggregate by category, calculate totals, or identify patterns.

## Reference

For endpoint details, filters, and response schemas, see [api-reference.md](references/api-reference.md).
