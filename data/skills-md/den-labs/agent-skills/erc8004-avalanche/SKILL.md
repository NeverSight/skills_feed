---
name: erc8004-avalanche
description: Register and manage AI agent identities on Avalanche C-Chain using ERC-8004 (Trustless Agents). Use this skill when the user wants to register an AI agent on-chain, give or read reputation feedback, request validation, or interact with ERC-8004 identity/reputation/validation registries on Avalanche mainnet or Fuji testnet.
---

# ERC-8004: Trustless Agents on Avalanche

Register your AI agent on Avalanche C-Chain with a verifiable on-chain identity, making it discoverable and enabling trust signals through reputation and validation.

## What is ERC-8004?

ERC-8004 is an Ethereum standard for trustless agent identity and reputation, deployed on Avalanche:

- **Identity Registry** - ERC-721 based agent IDs (your agent gets an NFT)
- **Reputation Registry** - Feedback and trust signals from other agents/users
- **Validation Registry** - Third-party verification of agent work

Website: https://www.8004.org | Spec: https://eips.ethereum.org/EIPS/eip-8004

## Contract Addresses

| Chain | Identity Registry | Reputation Registry |
|---|---|---|
| Avalanche Mainnet (43114) | `0x8004A169FB4a3325136EB29fA0ceB6D2e539a432` | `0x8004BAa17C55a88189AE136b182e5fdA19dE9b63` |
| Avalanche Fuji (43113) | `0x8004A818BFB912233c491871b3d84c89A494BD9e` | `0x8004B663056A597Dffe9eCcC1965A193B7388713` |

Explorer links:
- Mainnet: https://snowtrace.io/address/0x8004A169FB4a3325136EB29fA0ceB6D2e539a432
- Fuji: https://testnet.snowtrace.io/address/0x8004A818BFB912233c491871b3d84c89A494BD9e

## Quick Start

### 1. Register Your Agent

```bash
# Set environment variables
export AVALANCHE_RPC_URL="https://api.avax.network/ext/bc/C/rpc"
export PRIVATE_KEY="your-private-key"

# Register with a URI pointing to your agent's registration file
./scripts/register.sh "https://myagent.xyz/agent.json"

# Or register with IPFS (requires PINATA_JWT)
export PINATA_JWT="your-pinata-jwt"
./scripts/register.sh "ipfs"
```

### 2. Check Agent Registration

```bash
# Check if an agent is registered and get its info
./scripts/check-agent.sh <agent-id>
```

### 3. Give Feedback

```bash
# Give reputation feedback to an agent
./scripts/give-feedback.sh <agent-id> <value> <tag1> <tag2>
```

## Registration File Format

Your agent's registration file (see `assets/templates/registration.json`):

```json
{
  "type": "https://eips.ethereum.org/EIPS/eip-8004#registration-v1",
  "name": "My Avalanche Agent",
  "description": "An AI agent operating on Avalanche",
  "image": "https://example.com/avatar.png",
  "services": [
    { "name": "web", "endpoint": "https://myagent.xyz/" },
    { "name": "A2A", "endpoint": "https://myagent.xyz/.well-known/agent-card.json", "version": "0.3.0" },
    { "name": "MCP", "endpoint": "https://mcp.myagent.xyz/", "version": "2025-06-18" }
  ],
  "x402Support": false,
  "active": true,
  "registrations": [
    {
      "agentId": 1,
      "agentRegistry": "eip155:43114:0x8004A169FB4a3325136EB29fA0ceB6D2e539a432"
    }
  ],
  "supportedTrust": ["reputation"]
}
```

## Key Concepts

### Agent Identity (ERC-721 NFT)
- Each agent gets a unique `agentId` (tokenId) on registration
- The NFT owner controls the agent's profile and metadata
- Agents are globally identified by `eip155:43114:0x8004A169FB4a3325136EB29fA0ceB6D2e539a432` + `agentId`

### Reputation System
- Anyone can give feedback (except the agent owner themselves)
- Feedback includes a value (int128) with decimals (0-18) plus optional tags
- Common tags: `starred` (quality 0-100), `reachable` (binary), `uptime` (percentage)
- Feedback can be revoked by the original submitter
- Agents can append responses to feedback

### Validation
- Agents request validation from validator contracts
- Validators respond with a score (0-100)
- Supports stake-secured re-execution, zkML, TEE attestation

## Environment Variables

| Variable | Description | Required |
|---|---|---|
| `AVALANCHE_RPC_URL` | Avalanche C-Chain RPC endpoint | Yes (defaults to public RPC) |
| `PRIVATE_KEY` | Wallet private key for signing transactions | Yes |
| `PINATA_JWT` | Pinata API JWT for IPFS uploads | No (only for IPFS registration) |
| `AGENT_NAME` | Agent display name | No |
| `AGENT_DESCRIPTION` | Agent description | No |
| `AGENT_IMAGE` | Avatar URL | No |
| `SNOWTRACE_API_KEY` | Snowtrace API key for verification | No |

## Avalanche Network Details

| Parameter | Mainnet | Fuji Testnet |
|---|---|---|
| Chain ID | 43114 | 43113 |
| RPC URL | `https://api.avax.network/ext/bc/C/rpc` | `https://api.avax-test.network/ext/bc/C/rpc` |
| Explorer | https://snowtrace.io | https://testnet.snowtrace.io |
| Currency | AVAX | AVAX (test) |
| Faucet | - | https://faucet.avax.network |

## Workflow

1. **Get AVAX** - You need AVAX for gas fees (~0.01-0.05 AVAX for registration)
2. **Create Registration File** - Generate a JSON following the registration format
3. **Upload to IPFS** (optional) - Pin via Pinata or host at any URL
4. **Register On-Chain** - Call `register(agentURI)` on the Identity Registry
5. **Set Metadata** - Optionally set on-chain metadata and agent wallet
6. **Receive Feedback** - Other agents/users can give reputation signals
7. **Request Validation** - Optionally request third-party verification

## Using with cast (Foundry)

```bash
# Register an agent with a URI
cast send 0x8004A169FB4a3325136EB29fA0ceB6D2e539a432 \
  "register(string)" "https://myagent.xyz/agent.json" \
  --rpc-url https://api.avax.network/ext/bc/C/rpc \
  --private-key $PRIVATE_KEY

# Read agent URI
cast call 0x8004A169FB4a3325136EB29fA0ceB6D2e539a432 \
  "tokenURI(uint256)" 1 \
  --rpc-url https://api.avax.network/ext/bc/C/rpc

# Give feedback (value=85, decimals=0, tag1="starred")
cast send 0x8004BAa17C55a88189AE136b182e5fdA19dE9b63 \
  "giveFeedback(uint256,int128,uint8,string,string,string,string,bytes32)" \
  1 85 0 "starred" "" "" "" 0x0000000000000000000000000000000000000000000000000000000000000000 \
  --rpc-url https://api.avax.network/ext/bc/C/rpc \
  --private-key $PRIVATE_KEY

# Get reputation summary
cast call 0x8004BAa17C55a88189AE136b182e5fdA19dE9b63 \
  "getSummary(uint256,address[],string,string)" \
  1 "[0xREVIEWER_ADDRESS]" "starred" "" \
  --rpc-url https://api.avax.network/ext/bc/C/rpc
```

## Using with viem/ethers.js

See `references/api-reference.md` for complete TypeScript examples.

## Links

- [ERC-8004 Spec](https://eips.ethereum.org/EIPS/eip-8004)
- [8004.org](https://www.8004.org)
- [GitHub: erc-8004-contracts](https://github.com/agent0-labs/erc-8004-contracts)
- [Snowtrace Explorer](https://snowtrace.io)
