---
name: slot-rpc
description: Configure Cartridge RPC endpoints with API token authentication and CORS whitelisting.
---

# Slot RPC

Cartridge provides dedicated RPC endpoints for Starknet with authentication and CORS support.

## Endpoints

- **Mainnet**: `https://api.cartridge.gg/x/starknet/mainnet`
- **Sepolia**: `https://api.cartridge.gg/x/starknet/sepolia`

## Pricing

Free for up to 1M requests/month.
Additional requests: $5/1M, charged to the team.

## Authentication Methods

### API Token

```bash
curl https://api.cartridge.gg/x/starknet/mainnet \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "starknet_chainId",
    "params": [],
    "id": 1
  }'
```

### Domain Whitelisting

For browser apps, whitelist domains to make direct RPC calls without exposing tokens.
Whitelisted domains are rate-limited per IP.

```javascript
const response = await fetch('https://api.cartridge.gg/x/starknet/mainnet', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    jsonrpc: '2.0',
    method: 'starknet_chainId',
    params: [],
    id: 1,
  }),
});
```

## Managing API Tokens

```bash
# Create a token
slot rpc tokens create <KEY_NAME> --team <TEAM_NAME>

# List tokens
slot rpc tokens list --team <TEAM_NAME>

# Delete a token
slot rpc tokens delete <KEY_ID> --team <TEAM_NAME>
```

## Managing CORS Whitelist

Whitelists are specified as root domains; all subdomains are automatically included.

```bash
# Add a domain
slot rpc whitelist add <DOMAIN> --team <TEAM_NAME>

# List whitelisted domains
slot rpc whitelist list --team <TEAM_NAME>

# Remove a domain
slot rpc whitelist remove <ENTRY_ID> --team <TEAM_NAME>
```

## Viewing Logs

```bash
slot rpc logs --team <TEAM_NAME>
```

Options:
- `--after <CURSOR>`: Pagination cursor
- `--limit <NUMBER>`: Entries to return (default: 100)
- `--since <DURATION>`: Time period (`30m`, `1h`, `24h`)

Examples:

```bash
# Last 5 entries from past 30 minutes
slot rpc logs --team my-team --limit 5 --since 30m

# Paginate with cursor
slot rpc logs --team my-team --after <cursor> --limit 5
```
