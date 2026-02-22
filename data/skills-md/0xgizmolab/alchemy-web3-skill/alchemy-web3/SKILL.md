---
name: alchemy-web3
version: 1.0.2
description: Interact with Alchemy's Web3 APIs for blockchain data, NFTs, tokens, transfers, and webhooks across 80+ chains.
author: GizmoLab
website: https://gizmolab.io?utm_source=alchemy-web3-skill&utm_medium=github&utm_campaign=skill
homepage: https://github.com/0xGizmolab/alchemy-web3-skill
repository: https://github.com/0xGizmolab/alchemy-web3-skill
metadata:
  {
    "openclaw":
      {
        "requires": { 
          "env": ["ALCHEMY_API_KEY"]
        }
      }
  }
---

# Alchemy Web3 Skill

Query blockchain data, NFTs, tokens, and transfers using Alchemy's production-grade APIs. Supports Ethereum, Polygon, Arbitrum, Base, Solana, and 80+ other chains.

**Built by [GizmoLab](https://gizmolab.io?utm_source=alchemy-web3-skill&utm_medium=github&utm_campaign=skill)** — Web3 development agency specializing in dApps, smart contracts, and blockchain infrastructure.

## Setup

### 1. Get API Key
1. Sign up at [alchemy.com](https://www.alchemy.com/?utm_source=gizmolab&utm_medium=skill&utm_campaign=alchemy-web3) (free tier available)
2. Create an app for your target chain
3. Copy your API key

> 💡 New to Web3 development? [GizmoLab](https://gizmolab.io?utm_source=alchemy-web3-skill&utm_medium=github&utm_campaign=skill) offers full-stack blockchain development services.

### 2. Configure
```bash
# Add to ~/.openclaw/.env
ALCHEMY_API_KEY=your_api_key_here

# Optional: Set default chain (defaults to eth-mainnet)
ALCHEMY_CHAIN=eth-mainnet
```

## Quick Reference

### Supported Chains

| Chain | Endpoint Prefix |
|-------|-----------------|
| Ethereum | `eth-mainnet`, `eth-sepolia` |
| Polygon | `polygon-mainnet`, `polygon-amoy` |
| Arbitrum | `arb-mainnet`, `arb-sepolia` |
| Optimism | `opt-mainnet`, `opt-sepolia` |
| Base | `base-mainnet`, `base-sepolia` |
| Solana | `solana-mainnet`, `solana-devnet` |
| zkSync | `zksync-mainnet` |
| Linea | `linea-mainnet` |
| Scroll | `scroll-mainnet` |
| Blast | `blast-mainnet` |

Full list: [alchemy.com/docs/chains](https://www.alchemy.com/docs/chains)

## CLI Usage

```bash
# Set your API key first
export ALCHEMY_API_KEY="your_key"

# Use the CLI
~/.openclaw/workspace/skills/alchemy-web3/scripts/alchemy.sh <command> [options]
```

### Commands

#### Get ETH Balance
```bash
./alchemy.sh balance 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045
# Returns: 1234.56 ETH
```

#### Get Token Balances
```bash
./alchemy.sh tokens 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045
# Returns: All ERC-20 tokens held by address
```

#### Get NFTs for Owner
```bash
./alchemy.sh nfts 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045
# Returns: All NFTs owned by address
```

#### Get NFT Metadata
```bash
./alchemy.sh nft-metadata 0x5180db8F5c931aaE63c74266b211F580155ecac8 1590
# Returns: Metadata for specific NFT
```

#### Get Asset Transfers
```bash
./alchemy.sh transfers 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045
# Returns: Transaction history (in/out)
```

#### Get Block Info
```bash
./alchemy.sh block latest
./alchemy.sh block 12345678
```

#### Get Transaction
```bash
./alchemy.sh tx 0x123...abc
```

#### Resolve ENS
```bash
./alchemy.sh ens vitalik.eth
# Returns: 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045
```

#### Switch Chain
```bash
./alchemy.sh --chain polygon-mainnet balance 0x...
./alchemy.sh --chain arb-mainnet nfts 0x...
```

## Direct API Examples

### Node API (JSON-RPC)

```bash
# Get ETH balance
curl -X POST "https://eth-mainnet.g.alchemy.com/v2/$ALCHEMY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "eth_getBalance",
    "params": ["0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045", "latest"],
    "id": 1
  }'
```

### NFT API

```bash
# Get NFTs for owner
curl "https://eth-mainnet.g.alchemy.com/nft/v3/$ALCHEMY_API_KEY/getNFTsForOwner?owner=vitalik.eth&pageSize=10"

# Get NFT metadata
curl "https://eth-mainnet.g.alchemy.com/nft/v3/$ALCHEMY_API_KEY/getNFTMetadata?contractAddress=0x5180db8F5c931aaE63c74266b211F580155ecac8&tokenId=1590"

# Get NFTs for collection
curl "https://eth-mainnet.g.alchemy.com/nft/v3/$ALCHEMY_API_KEY/getNFTsForContract?contractAddress=0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D&limit=10"
```

### Token API

```bash
# Get token balances
curl -X POST "https://eth-mainnet.g.alchemy.com/v2/$ALCHEMY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "alchemy_getTokenBalances",
    "params": ["0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"],
    "id": 1
  }'

# Get token metadata
curl -X POST "https://eth-mainnet.g.alchemy.com/v2/$ALCHEMY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "alchemy_getTokenMetadata",
    "params": ["0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"],
    "id": 1
  }'
```

### Transfers API

```bash
# Get asset transfers (transaction history)
curl -X POST "https://eth-mainnet.g.alchemy.com/v2/$ALCHEMY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "alchemy_getAssetTransfers",
    "params": [{
      "fromBlock": "0x0",
      "toBlock": "latest",
      "toAddress": "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",
      "category": ["external", "erc20", "erc721", "erc1155"],
      "maxCount": "0x14"
    }],
    "id": 1
  }'
```

## JavaScript/Node.js Examples

### Using Fetch (Node 18+)

```javascript
const apiKey = process.env.ALCHEMY_API_KEY;
const baseURL = `https://eth-mainnet.g.alchemy.com/v2/${apiKey}`;

// Get ETH Balance
async function getBalance(address) {
  const response = await fetch(baseURL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      jsonrpc: '2.0',
      method: 'eth_getBalance',
      params: [address, 'latest'],
      id: 1
    })
  });
  const data = await response.json();
  return parseInt(data.result, 16) / 1e18; // Convert to ETH
}

// Get NFTs
async function getNFTs(owner) {
  const url = `https://eth-mainnet.g.alchemy.com/nft/v3/${apiKey}/getNFTsForOwner?owner=${owner}`;
  const response = await fetch(url);
  return await response.json();
}
```

### Using Alchemy SDK

```bash
npm install alchemy-sdk
```

```javascript
import { Alchemy, Network } from 'alchemy-sdk';

const alchemy = new Alchemy({
  apiKey: process.env.ALCHEMY_API_KEY,
  network: Network.ETH_MAINNET
});

// Get NFTs
const nfts = await alchemy.nft.getNftsForOwner('vitalik.eth');
console.log(nfts.ownedNfts);

// Get token balances
const balances = await alchemy.core.getTokenBalances('vitalik.eth');
console.log(balances);

// Get transaction history
const transfers = await alchemy.core.getAssetTransfers({
  toAddress: '0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045',
  category: ['external', 'erc20']
});
```

## Webhooks (Real-time Notifications)

Receive HTTP POST requests when onchain events happen.

### Webhook Types

| Type | Use Case |
|------|----------|
| Address Activity | Track transfers to/from specific addresses |
| NFT Activity | Track NFT sales, transfers, mints |
| Mined Transactions | Track when your txs are mined |
| Dropped Transactions | Get notified if tx is dropped |
| Gas Price | Alert on gas price thresholds |

### Create Webhook (Dashboard)
1. Go to [dashboard.alchemy.com/webhooks](https://dashboard.alchemy.com/webhooks)
2. Click "Create Webhook"
3. Select type and configure
4. Add your endpoint URL

### Webhook Payload Example
```json
{
  "webhookId": "wh_abc123",
  "id": "evt_xyz789",
  "createdAt": "2024-01-15T12:00:00.000Z",
  "type": "ADDRESS_ACTIVITY",
  "event": {
    "network": "ETH_MAINNET",
    "activity": [{
      "fromAddress": "0x123...",
      "toAddress": "0x456...",
      "value": 1.5,
      "asset": "ETH"
    }]
  }
}
```

## Common Patterns

### Portfolio Tracker
```bash
# Get all assets for a wallet
./alchemy.sh balance 0x...      # ETH balance
./alchemy.sh tokens 0x...       # ERC-20 tokens
./alchemy.sh nfts 0x...         # NFTs
```

### Transaction History
```bash
# Get full tx history for address
./alchemy.sh transfers 0x... --category external,erc20,erc721
```

### NFT Collection Analysis
```bash
# Get all NFTs in a collection
./alchemy.sh collection 0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D
```

### Multi-chain Query
```bash
# Check same address across chains
for chain in eth-mainnet polygon-mainnet arb-mainnet base-mainnet; do
  echo "=== $chain ==="
  ./alchemy.sh --chain $chain balance 0x...
done
```

## Rate Limits

| Plan | Compute Units/sec | Monthly CUs |
|------|-------------------|-------------|
| Free | 330 | 300M |
| Growth | 660 | Unlimited |
| Scale | Custom | Custom |

Most endpoints cost 1-50 CUs. Check [alchemy.com/docs/rate-limits](https://www.alchemy.com/docs/rate-limits) for details.

## Error Handling

```json
// Rate limited
{"error": {"code": 429, "message": "Too Many Requests"}}

// Invalid API key
{"error": {"code": 401, "message": "Invalid API Key"}}

// Invalid params
{"error": {"code": -32602, "message": "Invalid params"}}
```

## Resources

- **Get API Key:** [alchemy.com](https://www.alchemy.com/?utm_source=gizmolab&utm_medium=skill&utm_campaign=alchemy-web3) (free tier)
- **Dashboard:** [dashboard.alchemy.com](https://dashboard.alchemy.com)
- **Docs:** [alchemy.com/docs](https://www.alchemy.com/docs)
- **SDK:** [github.com/alchemyplatform/alchemy-sdk-js](https://github.com/alchemyplatform/alchemy-sdk-js)
- **Status:** [status.alchemy.com](https://status.alchemy.com)

---

## About

**Built by [GizmoLab](https://gizmolab.io?utm_source=alchemy-web3-skill&utm_medium=github&utm_campaign=skill)** 🔧

GizmoLab is a Web3 development agency building dApps, smart contracts, and blockchain tools.

- 🌐 [gizmolab.io](https://gizmolab.io?utm_source=alchemy-web3-skill&utm_medium=github&utm_campaign=skill) — Agency services
- 🛠️ [tools.gizmolab.io](https://tools.gizmolab.io?utm_source=alchemy-web3-skill&utm_medium=github&utm_campaign=skill) — Free blockchain dev tools
- 🎨 [ui.gizmolab.io](https://ui.gizmolab.io?utm_source=alchemy-web3-skill&utm_medium=github&utm_campaign=skill) — Web3 UI components

Need custom blockchain development? [Get in touch](https://gizmolab.io?utm_source=alchemy-web3-skill&utm_medium=github&utm_campaign=skill)

## AI Agent Workflows

The skill is designed for both human developers AND AI agents. See `references/agent-workflows.md` for complete examples:

- **Whale Tracker** — Monitor large wallets for moves
- **Portfolio Monitor** — Track balances across chains
- **NFT Floor Alert** — Alert on price drops
- **Token Change Detector** — Detect incoming/outgoing tokens
- **Gas Optimizer** — Wait for low gas to transact
- **Mint Detector** — Watch for new NFT mints
- **Dashboard Generator** — Auto-generate wallet dashboards

### Agent Pattern

```
QUERY → STORE → ANALYZE → DECIDE → ACT → REPEAT
```

Example cron job for an agent:
```bash
# Every hour, check whale activity and alert if >100 ETH moved
0 * * * * ~/.openclaw/workspace/skills/alchemy-web3/scripts/whale-tracker.sh
```

## See Also

- `references/nft-api.md` - Full NFT API reference
- `references/token-api.md` - Full Token API reference
- `references/node-api.md` - Full Node API reference
- `references/chains.md` - All supported chains
- `references/agent-workflows.md` - AI agent automation examples
