---
name: mcp-charge-pix
description: Guide for creating Pix charges using the kobana-mcp-charge MCP server. Use when the user wants to create instant Pix payments or billing Pix using MCP tools instead of direct API calls.
license: Complete terms in LICENSE.txt
metadata:
  author: Kobana
  version: "1.0"
compatibility: Requires kobana-mcp-charge MCP server configured
---

# Kobana Pix Creation via MCP

Create Pix charges using the `kobana-mcp-charge` MCP server tools.

## Prerequisites

The `kobana-mcp-charge` MCP server must be configured. See [MCP Server Setup](#mcp-server-setup) below.

## Available MCP Tools

### Pix Accounts
| Tool | Description |
|------|-------------|
| `list_charge_pix_accounts` | List all Pix accounts |
| `create_charge_pix_account` | Create a new Pix account |
| `get_charge_pix_account` | Get a specific Pix account |

### Pix Charges
| Tool | Description |
|------|-------------|
| `list_charge_pix` | List all Pix charges with filters |
| `create_charge_pix` | Create a new Pix charge |
| `get_charge_pix` | Get a specific Pix charge |
| `update_charge_pix` | Update a Pix charge |
| `cancel_charge_pix` | Cancel a Pix charge |

## Creating a Pix Charge

### Step 1: Get the Pix Account UID

First, list available Pix accounts to get the `pix_account_uid`:

```
Use tool: list_charge_pix_accounts
```

### Step 2: Create the Pix Charge

Use the `create_charge_pix` tool with the required parameters:

**Instant Pix (e-commerce, delivery):**
```json
{
  "amount": 150.00,
  "pix_account_uid": "018df180-7208-727b-...",
  "expire_at": "2026-01-31T12:30:00-03:00",
  "registration_kind": "instant",
  "payer": {
    "document_number": "111.321.322-09",
    "name": "João da Silva"
  },
  "external_id": "order_12345"
}
```

**Billing Pix (invoices, subscriptions):**
```json
{
  "amount": 500.00,
  "pix_account_uid": "018df180-7208-727b-...",
  "expire_at": "2026-02-10T23:59:59-03:00",
  "registration_kind": "billing",
  "payer": {
    "document_number": "12.345.678/0001-90",
    "name": "Company LTDA"
  },
  "fine_type": "percentage",
  "fine_percentage": 2.0,
  "interest_type": "monthly_percentage_calendar",
  "interest_percentage": 1.0,
  "revoke_days": 30
}
```

### Step 3: Get the QR Code

The initial response may not contain the QR Code (asynchronous registration). To get it:

1. **Poll the charge** using `get_charge_pix` with the returned UID
2. **Check `registration_status`**: When it's `confirmed`, the `qrcode` field will be populated

```
Use tool: get_charge_pix
Parameters: { "uid": "019c0cbe-f018-717e-..." }
```

## Common Parameters

### Required
| Parameter | Type | Description |
|-----------|------|-------------|
| `amount` | decimal | Value in BRL (minimum 0.01) |
| `pix_account_uid` | string | UUID of the Pix Account |
| `expire_at` | string | Expiration date (ISO 8601) |

### Payer Data
| Parameter | Type | Description |
|-----------|------|-------------|
| `payer.document_number` | string | CPF or CNPJ |
| `payer.name` | string | Full name or company name |
| `payer.email` | string | Email (optional) |

### Fine and Interest (Billing Pix only)
| Parameter | Type | Description |
|-----------|------|-------------|
| `fine_type` | string | `percentage` or `amount` |
| `fine_percentage` | decimal | Fine percentage |
| `interest_type` | string | See interest types in reference |
| `interest_percentage` | decimal | Interest percentage |
| `revoke_days` | integer | Days active after due date (required with fine/interest) |

### Tracking
| Parameter | Type | Description |
|-----------|------|-------------|
| `external_id` | string | External ID for tracking |
| `custom_data` | object | Custom metadata (JSON) |
| `tags` | array | Tags for organization |
| `message` | string | Message to payer (max 140 chars) |

## Pix Types

### Instant Pix (`registration_kind: "instant"`)
- Short expiration (minutes to hours)
- No interest, fines, or discounts
- Use for: e-commerce, delivery, point-of-sale

### Billing Pix (`registration_kind: "billing"`)
- Formal due date
- Supports interest, fines, discounts
- Stays active after due date (if `revoke_days` set)
- Use for: monthly invoices, subscriptions

## Status Reference

### Charge Status
- `opened` - Open (initial)
- `paid` - Paid
- `overdue` - Overdue
- `canceled` - Canceled

### Registration Status
- `pending` - Waiting for registration
- `confirmed` - Ready (has QR Code)
- `rejected` / `failed` - Error

## MCP Server Setup

### Claude Desktop Configuration

Add to `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "kobana-charge": {
      "command": "npx",
      "args": ["-y", "kobana-mcp-charge"],
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
    "kobana-charge": {
      "command": "npx",
      "args": ["-y", "kobana-mcp-charge"],
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
    "kobana-charge": {
      "command": "npx",
      "args": ["-y", "kobana-mcp-charge"],
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
    "kobana-charge": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://mcp.kobana.com.br/charge/mcp",
        "--header",
        "Authorization: Bearer your_access_token"
      ]
    }
  }
}
```

## Best Practices

1. **Always get the Pix Account first** - Use `list_charge_pix_accounts` to get available accounts
2. **Poll for QR Code** - Use `get_charge_pix` to check registration status
3. **Use external_id** - Track charges in your system
4. **Set revoke_days** - Required for interest/fines on Billing Pix
5. **Validate CPF/CNPJ** - Before creating the charge
6. **Test in sandbox** - Configure sandbox environment first

## Reference Documentation

See [references/REFERENCE.md](references/REFERENCE.md) for complete MCP server documentation and all available tools.
