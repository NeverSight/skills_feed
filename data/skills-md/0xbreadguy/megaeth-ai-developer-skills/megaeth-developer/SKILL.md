---
name: megaeth-developer
description: End-to-end MegaETH development playbook (Feb 2026). Covers wallet operations, token swaps (Kyber Network), eth_sendRawTransactionSync (EIP-7966) for instant receipts, JSON-RPC batching, real-time mini-block subscriptions, storage-aware contract patterns (Solady RedBlackTreeLib), MegaEVM gas model, WebSocket keepalive, bridging from Ethereum, and debugging with mega-evme. Use when building on MegaETH, managing wallets, sending transactions, or deploying contracts.
---

# MegaETH Development Skill

## What this Skill is for
Use this Skill when the user asks for:
- Wallet setup and management on MegaETH
- Sending transactions, checking balances, token operations
- Token swaps via Kyber Network aggregator
- MegaETH dApp frontend (React / Next.js with real-time updates)
- RPC configuration and transaction flow optimization
- Smart contract development with MegaEVM considerations
- Storage optimization (avoiding expensive SSTORE costs)
- Gas estimation and fee configuration
- Testing and debugging MegaETH transactions
- WebSocket subscriptions and mini-block streaming
- Bridging ETH from Ethereum to MegaETH

## Chain Configuration

| Network | Chain ID | RPC | Explorer |
|---------|----------|-----|----------|
| Mainnet | 4326 | `https://mainnet.megaeth.com/rpc` | `https://mega.etherscan.io` |
| Testnet | 6343 | `https://carrot.megaeth.com/rpc` | `https://megaeth-testnet-v2.blockscout.com` |

## Default stack decisions (opinionated)

### 1. Transaction submission: eth_sendRawTransactionSync first
- Use `eth_sendRawTransactionSync` (EIP-7966) — returns receipt in <10ms
- Eliminates polling for `eth_getTransactionReceipt`
- Docs: https://docs.megaeth.com/realtime-api

### 2. RPC: JSON-RPC batching over Multicall
- Prefer `client.request([...])` batch calls
- Multicall (`aggregate3`) harder to cache, weaker consistency
- Never batch slow methods (`eth_getLogs`) with fast ones (`eth_call`)

### 3. WebSocket: keepalive required
- Send `eth_chainId` every 30 seconds
- 50 connections per VIP endpoint, 10 subscriptions per connection
- Use `miniBlocks` subscription for real-time data

### 4. Storage: slot reuse patterns
- SSTORE 0→non-zero costs 2M gas × multiplier (expensive)
- Use Solady's RedBlackTreeLib instead of Solidity mappings
- Design for slot reuse, not constant allocation

### 5. Gas: skip estimation when possible
- Base fee stable at 0.001 gwei, no EIP-1559 adjustment
- Ignore `eth_maxPriorityFeePerGas` (returns 0)
- Hardcode gas limits to save round-trip
- Always use remote `eth_estimateGas` (MegaEVM costs differ from standard EVM)

### 6. Debugging: mega-evme CLI
- Replay transactions with full traces
- Profile gas by opcode
- https://github.com/megaeth-labs/mega-evm

## Operating procedure

### 1. Classify the task layer
- Frontend/WebSocket layer
- RPC/transaction layer
- Smart contract layer
- Testing/debugging layer

### 2. Pick the right patterns
- Frontend: single WebSocket → broadcast to users (not per-user connections)
- Transactions: sign locally → `eth_sendRawTransactionSync` → done
- Contracts: check SSTORE patterns, avoid volatile data access limits
- Testing: use mega-evme for replay, Foundry with `--skip-simulation`

### 3. Implement with MegaETH-specific correctness
Always be explicit about:
- Chain ID (4326 mainnet, 6343 testnet)
- Gas limit (hardcode when possible)
- Base fee (0.001 gwei, no buffer)
- Storage costs (new slots are expensive)
- Volatile data limits (20M gas after block.timestamp access)

### 4. Deliverables expectations
When implementing changes, provide:
- Exact files changed + diffs
- Commands to build/test/deploy
- Gas cost notes for storage-heavy operations
- RPC optimization notes if applicable

## Progressive disclosure (read when needed)
- Wallet operations: [wallet-operations.md](wallet-operations.md)
- Frontend patterns: [frontend-patterns.md](frontend-patterns.md)
- RPC methods reference: [rpc-methods.md](rpc-methods.md)
- Smart contract patterns: [smart-contracts.md](smart-contracts.md)
- Storage optimization: [storage-optimization.md](storage-optimization.md)
- Gas model: [gas-model.md](gas-model.md)
- Testing & debugging: [testing.md](testing.md)
- Security considerations: [security.md](security.md)
- Reference links: [resources.md](resources.md)
