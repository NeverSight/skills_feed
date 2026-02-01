---
name: mcp-transfer-pix
description: Guide for creating Pix transfers using the kobana-mcp-transfer MCP server. Use when the user wants to send Pix transfers or manage transfer batches using MCP tools instead of direct API calls.
license: Complete terms in LICENSE.txt
metadata:
  author: Kobana
  version: "1.0"
compatibility: Requires kobana-mcp-transfer MCP server configured
---

# Kobana Pix Transfer via MCP

Create and manage Pix transfers using the `kobana-mcp-transfer` MCP server tools.

## Prerequisites

The `kobana-mcp-transfer` MCP server must be configured. See [MCP Server Setup](#mcp-server-setup) below.

## Available MCP Tools

### Pix Transfers
| Tool | Description |
|------|-------------|
| `list_transfer_pix` | List all Pix transfers |
| `create_transfer_pix` | Create a new Pix transfer |
| `get_transfer_pix` | Get a specific Pix transfer |
| `cancel_transfer_pix` | Cancel a pending Pix transfer |

### Pix Transfer Batches
| Tool | Description |
|------|-------------|
| `list_transfer_batches` | List all transfer batches |
| `create_transfer_pix_batch` | Create a Pix transfer batch |
| `get_transfer_batch` | Get a specific batch |
| `approve_transfer_batch` | Approve a batch |
| `reprove_transfer_batch` | Reprove (cancel) a batch |

### Financial Accounts
| Tool | Description |
|------|-------------|
| `list_financial_accounts` | List all financial accounts |
| `get_financial_account` | Get a specific financial account |

## Creating a Pix Transfer

### Step 1: Get the Financial Account UID

First, list available financial accounts to get the source `financial_account_uid`:

```
Use tool: list_financial_accounts
```

### Step 2: Create the Pix Transfer

Use the `create_transfer_pix` tool with the required parameters:

**Transfer by Pix Key:**
```json
{
  "amount": 150.00,
  "financial_account_uid": "018df180-7208-727b-...",
  "type": "key",
  "key_type": "email",
  "key": "recipient@example.com",
  "beneficiary": {
    "document_number": "111.321.322-09",
    "name": "João da Silva"
  },
  "external_id": "payment_12345"
}
```

**Transfer by Bank Account:**
```json
{
  "amount": 500.00,
  "financial_account_uid": "018df180-7208-727b-...",
  "type": "bank_account",
  "beneficiary": {
    "document_number": "12.345.678/0001-90",
    "name": "Company LTDA"
  },
  "bank_account": {
    "compe_number": 341,
    "agency_number": "1234",
    "agency_digit": "5",
    "account_number": "12345",
    "account_digit": "6",
    "document_number": "12.345.678/0001-90"
  },
  "scheduled_to": "2026-02-01",
  "transfer_purpose": "20"
}
```

### Step 3: Create a Batch to Send

After creating transfers, you need to create a batch to send them to the bank:

```
Use tool: create_transfer_pix_batch
Parameters: {
  "financial_account_uid": "018df180-7208-727b-...",
  "transfers": [
    { "uid": "019c0cbe-f018-717e-..." }
  ]
}
```

Or create new transfers directly in the batch:
```json
{
  "financial_account_uid": "018df180-7208-727b-...",
  "transfers": [
    {
      "amount": 100.00,
      "type": "key",
      "key_type": "cpf",
      "key": "111.222.333-44",
      "beneficiary": {
        "document_number": "111.222.333-44",
        "name": "João Silva"
      }
    }
  ]
}
```

### Step 4: Check Batch Status

```
Use tool: get_transfer_batch
Parameters: { "uid": "019c0cbe-f018-717e-..." }
```

If the batch is `awaiting_approval`, approve it:
```
Use tool: approve_transfer_batch
Parameters: { "uid": "019c0cbe-f018-717e-..." }
```

## Common Parameters

### Required
| Parameter | Type | Description |
|-----------|------|-------------|
| `amount` | decimal | Transfer amount in BRL |
| `financial_account_uid` | string | UUID of source financial account |
| `type` | string | `key` or `bank_account` |

### For Pix Key (`type: "key"`)
| Parameter | Type | Description |
|-----------|------|-------------|
| `key_type` | string | `cpf`, `cnpj`, `email`, `phone`, `random` |
| `key` | string | The Pix key value |

### For Bank Account (`type: "bank_account"`)
| Parameter | Type | Description |
|-----------|------|-------------|
| `bank_account.compe_number` | integer | Bank COMPE code |
| `bank_account.agency_number` | string | Agency number |
| `bank_account.account_number` | string | Account number |
| `bank_account.account_digit` | string | Account check digit |

### Beneficiary
| Parameter | Type | Description |
|-----------|------|-------------|
| `beneficiary.document_number` | string | CPF or CNPJ |
| `beneficiary.name` | string | Full name or company name |

### Optional
| Parameter | Type | Description |
|-----------|------|-------------|
| `scheduled_to` | date | Schedule date (YYYY-MM-DD) |
| `transfer_purpose` | string | Purpose code (default: "98") |
| `external_id` | string | External ID for tracking |
| `custom_data` | object | Custom metadata (JSON) |
| `tags` | array | Tags for organization |

## Transfer Types

### By Pix Key
- Quick transfers when recipient's key is known
- Key types: `cpf`, `cnpj`, `email`, `phone`, `random`

### By Bank Account
- Transfers using bank account details
- Requires complete bank account information

## Status Reference

### Transfer Status
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
    "kobana-transfer": {
      "command": "npx",
      "args": ["-y", "kobana-mcp-transfer"],
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
    "kobana-transfer": {
      "command": "npx",
      "args": ["-y", "kobana-mcp-transfer"],
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
    "kobana-transfer": {
      "command": "npx",
      "args": ["-y", "kobana-mcp-transfer"],
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
    "kobana-transfer": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://mcp.kobana.com.br/transfer/mcp",
        "--header",
        "Authorization: Bearer your_access_token"
      ]
    }
  }
}
```

## Best Practices

1. **Get financial account first** - Use `list_financial_accounts` to get available accounts
2. **Use batches for efficiency** - Create multiple transfers in a single batch
3. **Check batch status** - Poll `get_transfer_batch` or use webhooks
4. **Approve when needed** - Some accounts require manual approval
5. **Use external_id** - Track transfers in your system
6. **Test in sandbox** - Configure sandbox environment first

## Reference Documentation

See [references/REFERENCE.md](references/REFERENCE.md) for complete MCP server documentation and all available tools.
