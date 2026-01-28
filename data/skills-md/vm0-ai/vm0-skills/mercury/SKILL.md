---
name: mercury
description: Mercury Banking API via curl. Use this skill to manage bank accounts, transactions, transfers, and financial operations.
vm0_secrets:
  - MERCURY_API_TOKEN
---

# Mercury Banking API

Manage business bank accounts, transactions, transfers, and financial operations via Mercury's REST API.

> Official docs: https://docs.mercury.com/reference/getaccount

---

## When to Use

Use this skill when you need to:

- View account balances and details
- List and search transactions
- Create internal transfers between accounts
- Manage recipients for external transfers
- Download account statements
- Access treasury account information

---

## Prerequisites

1. Sign up for a Mercury business bank account at https://mercury.com
2. Go to Settings > Developers > API Tokens
3. Create a new API token with appropriate permissions

Set environment variable:

```bash
export MERCURY_API_TOKEN="your-api-token"
```

> **Important:** When using `$VAR` in a command that pipes to another command, wrap the command containing `$VAR` in `bash -c '...'`. Due to a Claude Code bug, environment variables are silently cleared when pipes are used directly.
> ```bash
> bash -c 'curl -s "https://api.example.com" --header "Authorization: Bearer $API_KEY"'
> ```

---

## Accounts

### List All Accounts

```bash
bash -c 'curl -s "https://api.mercury.com/api/v1/accounts" --header "Authorization: Bearer $MERCURY_API_TOKEN"'
```

### Get Account by ID

Replace `<your-account-id>` with the actual account ID:

```bash
bash -c 'curl -s "https://api.mercury.com/api/v1/account/<your-account-id>" --header "Authorization: Bearer $MERCURY_API_TOKEN"'
```

### Get Account Cards

Replace `<your-account-id>` with the actual account ID:

```bash
bash -c 'curl -s "https://api.mercury.com/api/v1/account/<your-account-id>/cards" --header "Authorization: Bearer $MERCURY_API_TOKEN"'
```

---

## Transactions

### List Account Transactions

Replace `<your-account-id>` with the actual account ID:

```bash
bash -c 'curl -s "https://api.mercury.com/api/v1/account/<your-account-id>/transactions" --header "Authorization: Bearer $MERCURY_API_TOKEN"'
```

### List Transactions with Filters

Filter by date range, status, or limit. Replace `<your-account-id>` with the actual account ID:

```bash
bash -c 'curl -s "https://api.mercury.com/api/v1/account/<your-account-id>/transactions?limit=50&start=2024-01-01&end=2024-12-31" --header "Authorization: Bearer $MERCURY_API_TOKEN"'
```

### Get Transaction by ID

Replace `<your-account-id>` and `<your-transaction-id>` with the actual IDs:

```bash
bash -c 'curl -s "https://api.mercury.com/api/v1/account/<your-account-id>/transaction/<your-transaction-id>" --header "Authorization: Bearer $MERCURY_API_TOKEN"'
```

---

## Transfers

### Create Internal Transfer

Transfer funds between your Mercury accounts.

Write to `/tmp/mercury_request.json`:

```json
{
  "toAccountId": "target-account-id",
  "amount": 100.00,
  "note": "Internal transfer"
}
```

Then run. Replace `<your-account-id>` with the actual account ID:

```bash
bash -c 'curl -s -X POST "https://api.mercury.com/api/v1/account/<your-account-id>/internal-transfer" --header "Authorization: Bearer $MERCURY_API_TOKEN" --header "Content-Type: application/json" -d @/tmp/mercury_request.json'
```

### Send Money Request

Initiate a money transfer request.

Write to `/tmp/mercury_request.json`:

```json
{
  "recipientId": "recipient-id",
  "amount": 100.00,
  "paymentMethod": "ach",
  "idempotencyKey": "unique-key-123"
}
```

Then run. Replace `<your-account-id>` with the actual account ID:

```bash
bash -c 'curl -s -X POST "https://api.mercury.com/api/v1/account/<your-account-id>/send-money" --header "Authorization: Bearer $MERCURY_API_TOKEN" --header "Content-Type: application/json" -d @/tmp/mercury_request.json'
```

### Get Send Money Request Status

Replace `<your-request-id>` with the actual request ID:

```bash
bash -c 'curl -s "https://api.mercury.com/api/v1/request-send-money/<your-request-id>" --header "Authorization: Bearer $MERCURY_API_TOKEN"'
```

---

## Recipients

### List All Recipients

```bash
bash -c 'curl -s "https://api.mercury.com/api/v1/recipients" --header "Authorization: Bearer $MERCURY_API_TOKEN"'
```

### Get Recipient by ID

Replace `<your-recipient-id>` with the actual recipient ID:

```bash
bash -c 'curl -s "https://api.mercury.com/api/v1/recipient/<your-recipient-id>" --header "Authorization: Bearer $MERCURY_API_TOKEN"'
```

### Create Recipient

Write to `/tmp/mercury_request.json`:

```json
{
  "name": "Vendor Name",
  "emails": ["vendor@example.com"],
  "paymentMethod": "ach",
  "electronicRoutingInfo": {
    "accountNumber": "123456789",
    "routingNumber": "021000021",
    "bankName": "Example Bank",
    "electronicAccountType": "businessChecking"
  }
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.mercury.com/api/v1/recipients" --header "Authorization: Bearer $MERCURY_API_TOKEN" --header "Content-Type: application/json" -d @/tmp/mercury_request.json'
```

---

## Statements

### List Account Statements

Replace `<your-account-id>` with the actual account ID:

```bash
bash -c 'curl -s "https://api.mercury.com/api/v1/account/<your-account-id>/statements" --header "Authorization: Bearer $MERCURY_API_TOKEN"'
```

### Download Statement PDF

Replace `<your-account-id>` and `<your-statement-id>` with the actual IDs:

```bash
bash -c 'curl -s "https://api.mercury.com/api/v1/account/<your-account-id>/statement/<your-statement-id>/pdf" --header "Authorization: Bearer $MERCURY_API_TOKEN"' > statement.pdf
```

---

## Organization

### Get Organization Info

```bash
bash -c 'curl -s "https://api.mercury.com/api/v1/organization" --header "Authorization: Bearer $MERCURY_API_TOKEN"'
```

---

## Treasury

### List Treasury Accounts

```bash
bash -c 'curl -s "https://api.mercury.com/api/v1/treasury" --header "Authorization: Bearer $MERCURY_API_TOKEN"'
```

### Get Treasury Account by ID

Replace `<your-treasury-id>` with the actual treasury ID:

```bash
bash -c 'curl -s "https://api.mercury.com/api/v1/treasury/<your-treasury-id>" --header "Authorization: Bearer $MERCURY_API_TOKEN"'
```

### List Treasury Transactions

Replace `<your-treasury-id>` with the actual treasury ID:

```bash
bash -c 'curl -s "https://api.mercury.com/api/v1/treasury/<your-treasury-id>/transactions" --header "Authorization: Bearer $MERCURY_API_TOKEN"'
```

---

## Users

### List Users

```bash
bash -c 'curl -s "https://api.mercury.com/api/v1/users" --header "Authorization: Bearer $MERCURY_API_TOKEN"'
```

---

## Credit

### List Credit Accounts

```bash
bash -c 'curl -s "https://api.mercury.com/api/v1/credit" --header "Authorization: Bearer $MERCURY_API_TOKEN"'
```

---

## Accounts Receivable

### List Customers

```bash
bash -c 'curl -s "https://api.mercury.com/api/v1/accounts-receivable/customers" --header "Authorization: Bearer $MERCURY_API_TOKEN"'
```

### Create Customer

Write to `/tmp/mercury_request.json`:

```json
{
  "name": "Customer Name",
  "email": "customer@example.com"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.mercury.com/api/v1/accounts-receivable/customers" --header "Authorization: Bearer $MERCURY_API_TOKEN" --header "Content-Type: application/json" -d @/tmp/mercury_request.json'
```

### List Invoices

```bash
bash -c 'curl -s "https://api.mercury.com/api/v1/accounts-receivable/invoices" --header "Authorization: Bearer $MERCURY_API_TOKEN"'
```

### Create Invoice

Write to `/tmp/mercury_request.json`:

```json
{
  "customerId": "customer-id",
  "lineItems": [{"description": "Service", "amount": 500.00}],
  "dueDate": "2024-12-31"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.mercury.com/api/v1/accounts-receivable/invoices" --header "Authorization: Bearer $MERCURY_API_TOKEN" --header "Content-Type: application/json" -d @/tmp/mercury_request.json'
```

### Download Invoice PDF

Replace `<your-invoice-id>` with the actual invoice ID:

```bash
bash -c 'curl -s "https://api.mercury.com/api/v1/accounts-receivable/invoice/<your-invoice-id>/pdf" --header "Authorization: Bearer $MERCURY_API_TOKEN"' > invoice.pdf
```

---

## Guidelines

1. **Rate Limits**: Mercury may enforce rate limits; implement appropriate backoff strategies for high-volume operations
2. **Idempotency**: Use `idempotencyKey` for transfer operations to prevent duplicate transactions
3. **Security**: Never expose API tokens in logs or client-side code
4. **Amounts**: All monetary amounts are typically in USD and represented as decimal numbers
5. **Pagination**: For large result sets, use `limit` and `offset` parameters where supported

---

## API Reference

- Documentation: https://docs.mercury.com/reference/getaccount
- Dashboard: https://dashboard.mercury.com
