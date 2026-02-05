---
name: proxy-pay-mcp
description: Proxy Pay MCP server integration for AI agent payments. Use Proxy's Model Context Protocol tools to create payment intents, provision virtual cards, check balances, and track transactions. Requires Proxy account and agent token.
---

# Proxy Pay MCP Integration

Connect to Proxy Pay's MCP server for AI agent payments.

## MCP Server Setup

### Option 1: NPX (Recommended)

```json
{
  "mcpServers": {
    "proxy": {
      "command": "npx",
      "args": ["-y", "proxy-mcp-server"],
      "env": {
        "PROXY_AGENT_TOKEN": "your-agent-token"
      }
    }
  }
}
```

### Option 2: HTTP Transport

```json
{
  "mcpServers": {
    "proxy": {
      "transport": "http",
      "url": "https://api.useproxy.ai/mcp",
      "headers": {
        "Authorization": "Bearer your-agent-token"
      }
    }
  }
}
```

## All 13 MCP Tools

### User & Onboarding
- `proxy.user.get` - Get user profile and account info
- `proxy.kyc.status` - Check KYC verification status
- `proxy.kyc.link` - Get KYC completion URL

### Balance & Funding
- `proxy.balance.get` - Get available spending power
- `proxy.funding.get` - Get ACH/wire/crypto deposit instructions

### Intents (Core Flow)
- `proxy.intents.create` - Create payment intent (triggers card issuance)
- `proxy.intents.list` - List all intents for this agent
- `proxy.intents.get` - Get intent details including card info

### Cards
- `proxy.cards.get` - Get card details (masked PAN)
- `proxy.cards.get_sensitive` - Get full card number, CVV, expiry

### Transactions
- `proxy.transactions.list_for_card` - List transactions for a card
- `proxy.transactions.get` - Get detailed transaction info

### Utility
- `proxy.tools.list` - List all available Proxy tools

## Core Payment Flow

```
proxy.balance.get → proxy.intents.create → proxy.cards.get_sensitive → Pay
```

## Error Response Format

```json
{
  "success": false,
  "error": {
    "code": "POLICY_REQUIRED",
    "message": "No policy configured",
    "hint": "Assign a policy to this agent",
    "context": "intents.create"
  }
}
```

## Error Codes

| Code | Meaning |
|------|---------|
| `POLICY_REQUIRED` | Agent needs policy assigned |
| `ONBOARDING_INCOMPLETE` | Complete KYC first |
| `INSUFFICIENT_BALANCE` | Add funds |
| `AGENT_NOT_FOUND` | Invalid token |
| `FORBIDDEN` | Permission denied |
| `INTENT_NOT_FOUND` | Bad intent ID |
| `CARD_NOT_FOUND` | Bad card ID |

## Getting Started

1. Sign up at [useproxy.ai](https://useproxy.ai)
2. Complete KYC verification
3. Create Agent in dashboard
4. Assign a Policy (spending limits)
5. Generate Agent Token
6. Add MCP config above
