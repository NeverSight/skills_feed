---
name: plaid-integration
description: Integrate Plaid API for bank account connections and transaction syncing. Use when implementing financial data access, bank linking, or transaction imports in TypeScript/Bun applications.
---

# Plaid API Integration

Integrate Plaid for connecting bank accounts and syncing transactions in TypeScript applications using Bun.

## Quick Start

```bash
bun add plaid
```

```typescript
import { Configuration, PlaidApi, PlaidEnvironments } from 'plaid';

const plaidClient = new PlaidApi(new Configuration({
  basePath: PlaidEnvironments[process.env.PLAID_ENV || 'sandbox'],
  baseOptions: {
    headers: {
      'PLAID-CLIENT-ID': process.env.PLAID_CLIENT_ID,
      'PLAID-SECRET': process.env.PLAID_SECRET,
    }
  }
}));
```

## Environment Setup

| Environment | Use Case | HTTPS Required | Real Data |
|-------------|----------|----------------|-----------|
| `sandbox` | Development/testing | No | No (test accounts) |
| `development` | Limited Production | Yes for redirect, No for popup | Yes (with limits) |
| `production` | Full production | Yes | Yes |

**Critical**: Use popup mode (no `redirect_uri`) for local development to avoid HTTPS requirements:

```typescript
// Popup mode - works with HTTP localhost
const linkConfig = {
  user: { client_user_id: `user-${Date.now()}` },
  client_name: 'My App',
  products: ['transactions'],
  country_codes: ['US'],
  language: 'en',
  // NO redirect_uri = popup mode
};
```

## Authentication Flow

The Plaid Link flow has 3 steps:

1. **Create Link Token** (backend) → Returns temporary token for Link UI
2. **User Authenticates** (frontend) → Opens Plaid Link, user logs into bank
3. **Exchange Tokens** (backend) → Trade public_token for permanent access_token

See `references/code-examples.md` for complete implementation.

## Key Concepts

- **Item**: A bank connection (one per institution per user)
- **Access Token**: Permanent credential for API calls (store securely)
- **Public Token**: Temporary token from Link (exchange immediately)
- **Link Token**: Short-lived token to initialize Link UI

## Products

Common products to request:

| Product | Description |
|---------|-------------|
| `transactions` | Transaction history and real-time updates |
| `auth` | Account and routing numbers |
| `identity` | Account holder information |
| `investments` | Investment account data |
| `liabilities` | Loan and credit card data |

## Database Schema

For multi-account support, use SQLite with Bun's built-in driver:

```typescript
import { Database } from "bun:sqlite";

db.run(`
  CREATE TABLE IF NOT EXISTS items (
    id TEXT PRIMARY KEY,
    access_token TEXT NOT NULL,
    institution_id TEXT,
    institution_name TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
  )
`);

db.run(`
  CREATE TABLE IF NOT EXISTS accounts (
    id TEXT PRIMARY KEY,
    item_id TEXT NOT NULL,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    subtype TEXT,
    current_balance REAL,
    FOREIGN KEY (item_id) REFERENCES items(id) ON DELETE CASCADE
  )
`);

db.run(`
  CREATE TABLE IF NOT EXISTS transactions (
    id TEXT PRIMARY KEY,
    account_id TEXT NOT NULL,
    amount REAL NOT NULL,
    date TEXT NOT NULL,
    name TEXT NOT NULL,
    merchant_name TEXT,
    category TEXT,
    FOREIGN KEY (account_id) REFERENCES accounts(id) ON DELETE CASCADE
  )
`);
```

## Transaction Pagination

Plaid returns max 500 transactions per request. Always paginate:

```typescript
let offset = 0;
const count = 500;
let hasMore = true;

while (hasMore) {
  const response = await plaidClient.transactionsGet({
    access_token,
    start_date: '2023-01-01',
    end_date: '2024-12-31',
    options: { count, offset },
  });

  // Process response.data.transactions
  offset += response.data.transactions.length;
  hasMore = offset < response.data.total_transactions;
}
```

## Common Errors

| Error Code | Cause | Solution |
|------------|-------|----------|
| `INVALID_ACCESS_TOKEN` | Token expired or invalid | Re-link the account |
| `ITEM_LOGIN_REQUIRED` | Bank requires re-authentication | Use update mode Link |
| `INVALID_FIELD` + "redirect_uri must use HTTPS" | Using redirect in dev/prod | Use popup mode or HTTPS |
| `PRODUCTS_NOT_SUPPORTED` | Institution doesn't support product | Check institution capabilities |

## Documentation Links

- [Plaid Quickstart](https://plaid.com/docs/quickstart/)
- [Link Token API](https://plaid.com/docs/api/tokens/#linktokencreate)
- [Transactions API](https://plaid.com/docs/api/products/transactions/)
- [Error Reference](https://plaid.com/docs/errors/)
- [Sandbox Test Credentials](https://plaid.com/docs/sandbox/test-credentials/)

## Reference Files

- `references/code-examples.md` - Complete implementation patterns
- `references/api-reference.md` - API endpoints and responses
