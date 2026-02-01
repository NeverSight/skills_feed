---
name: mcp-payment-pix
description: Guide for paying Pix charges using the kobana-mcp-payment MCP server. Use when the user wants to pay Pix invoices, decode QR codes, or manage Pix payments using MCP tools instead of direct API calls.
license: Complete terms in LICENSE.txt
metadata:
  author: Kobana
  version: "1.0"
compatibility: Requires kobana-mcp-payment MCP server configured
---

# Kobana Pix Payment via MCP

Pay Pix charges and decode QR codes using the `kobana-mcp-payment` MCP server tools.

## Prerequisites

The `kobana-mcp-payment` MCP server must be configured. See [MCP Server Setup](#mcp-server-setup) below.

## Available MCP Tools

### Pix Payments
| Tool | Description |
|------|-------------|
| `list_payment_pix` | List all Pix payments |
| `create_payment_pix` | Create a new Pix payment |
| `get_payment_pix` | Get a specific Pix payment |
| `cancel_payment_pix` | Cancel a pending Pix payment |

### Pix Decoding
| Tool | Description |
|------|-------------|
| `decode_pix_emv` | Decode a Pix EMV (QR code/copy-paste) |

### Payment Batches
| Tool | Description |
|------|-------------|
| `list_payment_batches` | List all payment batches |
| `create_payment_pix_batch` | Create a Pix payment batch |
| `get_payment_batch` | Get a specific batch |
| `approve_payment_batch` | Approve a batch |
| `reprove_payment_batch` | Reprove (cancel) a batch |

### Financial Accounts
| Tool | Description |
|------|-------------|
| `list_financial_accounts` | List all financial accounts |
| `get_financial_account` | Get a specific financial account |

## Paying a Pix Charge

### Step 1: Get the Financial Account UID

First, list available financial accounts to get the source `financial_account_uid`:

```
Use tool: list_financial_accounts
```

### Step 2: Decode the Pix EMV (Optional)

Before paying, decode the QR code to validate the charge data:

```
Use tool: decode_pix_emv
Parameters: {
  "emv": "00020126580014br.gov.bcb.pix0136123e4567-e89b-12d3-a456-426614174000..."
}
```

This returns the charge details: amount, merchant name, key, description, etc.

### Step 3: Create the Payment

Use the `create_payment_pix` tool with the required parameters:

**Payment by EMV (Dynamic Pix):**
```json
{
  "financial_account_uid": "018df180-7208-727b-...",
  "emv": "00020126580014br.gov.bcb.pix0136123e4567-e89b-12d3-a456-426614174000...",
  "amount": 150.00,
  "external_id": "payment_001"
}
```

**Payment by Pix Key (Static Pix):**
```json
{
  "financial_account_uid": "018df180-7208-727b-...",
  "type": "key",
  "key_type": "email",
  "key": "recipient@example.com",
  "amount": 150.00,
  "beneficiary": {
    "document_number": "12.345.678/0001-90",
    "name": "Company LTDA"
  },
  "external_id": "payment_002"
}
```

### Step 4: Create a Batch to Send

After creating payments, create a batch to send them to the bank:

```
Use tool: create_payment_pix_batch
Parameters: {
  "financial_account_uid": "018df180-7208-727b-...",
  "payments": [
    { "uid": "019c0cbe-f018-717e-..." }
  ]
}
```

Or create new payments directly in the batch:
```json
{
  "financial_account_uid": "018df180-7208-727b-...",
  "payments": [
    {
      "emv": "00020126580014br.gov.bcb.pix...",
      "amount": 150.00
    }
  ]
}
```

### Step 5: Check Batch Status

```
Use tool: get_payment_batch
Parameters: { "uid": "019c0cbe-f018-717e-..." }
```

If the batch is `awaiting_approval`, approve it:
```
Use tool: approve_payment_batch
Parameters: { "uid": "019c0cbe-f018-717e-..." }
```

## Common Parameters

### Required
| Parameter | Type | Description |
|-----------|------|-------------|
| `financial_account_uid` | string | UUID of source financial account |
| `amount` | decimal | Payment amount in BRL |

### For EMV Payment (Dynamic Pix)
| Parameter | Type | Description |
|-----------|------|-------------|
| `emv` | string | Pix EMV string (from QR code) |

### For Key Payment (Static Pix)
| Parameter | Type | Description |
|-----------|------|-------------|
| `type` | string | Must be `key` |
| `key_type` | string | `cpf`, `cnpj`, `email`, `phone`, `random` |
| `key` | string | The Pix key value |

### Beneficiary
| Parameter | Type | Description |
|-----------|------|-------------|
| `beneficiary.document_number` | string | CPF or CNPJ |
| `beneficiary.name` | string | Full name or company name |

### Optional
| Parameter | Type | Description |
|-----------|------|-------------|
| `scheduled_to` | date | Schedule date (YYYY-MM-DD) |
| `description` | string | Payment description |
| `external_id` | string | External ID for tracking |
| `custom_data` | object | Custom metadata (JSON) |
| `tags` | array | Tags for organization |

## Payment Types

### By EMV (Dynamic Pix)
- Use when you have a QR code or copy-paste string
- Amount may be fixed by the charge
- Most common for invoices and bills

### By Pix Key (Static Pix)
- Use when paying directly to a Pix key
- You define the amount
- Use for donations, tips, or manual payments

## Status Reference

### Payment Status
- `pending` - Pending (initial)
- `awaiting_approval` - Awaiting batch approval
- `approved` - Approved, processing
- `confirmed` - Confirmed by bank
- `rejected` - Rejected by bank
- `reproved` - Reproved (canceled)

### Registration Status
- `pending` - Waiting for registration
- `requested` - Sent to bank
- `confirmed` - Confirmed at bank
- `rejected` / `failed` - Error

## MCP Server Setup

### Claude Desktop Configuration

Add to `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "kobana-payment": {
      "command": "npx",
      "args": ["-y", "kobana-mcp-payment"],
      "env": {
        "KOBANA_ACCESS_TOKEN": "your_access_token"
      }
    }
  }
}
```

### Sandbox Environment

```json
{
  "mcpServers": {
    "kobana-payment": {
      "command": "npx",
      "args": ["-y", "kobana-mcp-payment"],
      "env": {
        "KOBANA_ACCESS_TOKEN": "your_sandbox_token",
        "KOBANA_API_URL": "https://api-sandbox.kobana.com.br"
      }
    }
  }
}
```

### Claude Code Configuration

Add to `.mcp.json` in your project root:

```json
{
  "mcpServers": {
    "kobana-payment": {
      "command": "npx",
      "args": ["-y", "kobana-mcp-payment"],
      "env": {
        "KOBANA_ACCESS_TOKEN": "your_access_token"
      }
    }
  }
}
```

### Remote MCP (Hosted)

```json
{
  "mcpServers": {
    "kobana-payment": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://mcp.kobana.com.br/payment/mcp",
        "--header",
        "Authorization: Bearer your_access_token"
      ]
    }
  }
}
```

## Best Practices

1. **Get financial account first** - Use `list_financial_accounts` to get available accounts
2. **Decode before paying** - Use `decode_pix_emv` to validate the charge data
3. **Use batches for efficiency** - Create multiple payments in a single batch
4. **Check batch status** - Poll `get_payment_batch` or use webhooks
5. **Approve when needed** - Some accounts require manual approval
6. **Use external_id** - Track payments in your system
7. **Test in sandbox** - Configure sandbox environment first

## Reference Documentation

See [references/REFERENCE.md](references/REFERENCE.md) for complete MCP server documentation and all available tools.
