---
name: stellar-dev
description: End-to-end Stellar development playbook. Covers Soroban smart contracts (Rust SDK), Stellar CLI, JavaScript/Python/Go SDKs for client apps, Stellar RPC (preferred) and Horizon API (legacy), Stellar Assets vs Soroban tokens (SAC bridge), wallet integration (Freighter, Stellar Wallets Kit), smart accounts with passkeys, status-sensitive zero-knowledge proof patterns, testing strategies, security patterns, and common pitfalls. Optimized for payments, asset tokenization, DeFi, privacy-aware applications, and financial applications. Use when building on Stellar, Soroban, or working with XLM, Stellar Assets, trustlines, anchors, SEPs, ZK proofs, or the Stellar RPC/Horizon APIs.
user-invocable: true
argument-hint: "[task-description]"
---

# Stellar Development Skill (Soroban-first)

## What this Skill is for
Use this Skill when the user asks for:
- Soroban smart contract development (Rust)
- Stellar dApp frontend work (React / Next.js / Node.js)
- Wallet connection + signing flows (Freighter, etc.)
- Transaction building / sending / confirmation
- Stellar Asset issuance and management
- Client SDK usage (JavaScript, Python, Go, Rust)
- Zero-knowledge proof verification (where supported by target network/protocol)
- Privacy-preserving applications (privacy pools, confidential tokens)
- Local testing and deployment
- Security hardening and audit-style reviews

## What this Skill is NOT for
- Bitcoin, Ethereum, Solana, or other non-Stellar blockchain development
- Stellar node/validator operation (see [validators docs](https://developers.stellar.org/docs/validators))
- General Rust programming unrelated to Soroban
- Stellar protocol governance or CAP authoring

## Default stack decisions (opinionated)

### 1. Smart Contracts: Soroban (Rust)
- Use Soroban SDK (`soroban-sdk` crate) for all smart contract development
- Contracts compile to WebAssembly (WASM)
- Use `#![no_std]` - standard library not available
- 64KB contract size limit - use release optimizations
- Prefer Stellar Assets over custom token contracts when possible

### 2. Client SDK: stellar-sdk (JavaScript) first
- Use `@stellar/stellar-sdk` for browser and Node.js applications
- Supports both Stellar RPC and legacy Horizon API
- Full transaction building, signing, and submission
- Soroban contract deployment and invocation

### 3. API Access: Stellar RPC first (Horizon legacy-focused)
- **Prefer Stellar RPC** for new projects (JSON-RPC, real-time state)
- **Horizon API** remains available for legacy compatibility and historical-query workflows
- RPC: 7-day history for most methods; `getLedgers` queries back to genesis (Infinite Scroll)
- Use Hubble/Galexie for comprehensive historical data beyond RPC

### 4. Token Strategy: Stellar Assets first
- **Prefer Stellar Assets** (classic issuance + trustlines) for fungible tokens
- Built-in ecosystem support (wallets, exchanges, anchors)
- Stellar Asset Contracts (SAC) provide Soroban interoperability
- Use custom Soroban tokens only for complex logic requirements

### 5. Testing
- **Local**: Use Stellar Quickstart Docker for local network
- **Testnet**: Use Testnet with Friendbot for funding
- **Unit tests**: Compile to native for fast iteration
- **Integration tests**: Deploy to local/testnet

### 6. Wallet Integration
- **Freighter** is the primary browser wallet
- Use Stellar Wallets Kit for multi-wallet support
- Wallet Standard for consistent connection patterns

### 7. Freshness policy
- Verify volatile facts (protocol support, RPC endpoints, CAP/SEP status, SDK API changes) against official docs before asserting them as current.

## Operating procedure (how to execute tasks)

### 1. Classify the task layer
- Smart contract layer (Soroban/Rust)
- Client SDK/scripts layer (JS/Python/Go)
- Frontend/wallet layer
- Asset management layer (issuance, trustlines)
- Testing/CI layer
- Infrastructure (RPC/Horizon/indexing)

### Quick routing
- Need custom on-chain logic? → [contracts-soroban.md](contracts-soroban.md)
- Building a frontend/dApp? → [frontend-stellar-sdk.md](frontend-stellar-sdk.md)
- Issuing or managing tokens? → [stellar-assets.md](stellar-assets.md)
- Zero-knowledge proofs or privacy? → [zk-proofs.md](zk-proofs.md)
- Setting up tests/CI? → [testing.md](testing.md)
- Querying chain data or indexing? → [api-rpc-horizon.md](api-rpc-horizon.md) (also see [Data Docs](https://developers.stellar.org/docs/data))
- Security review? → [security.md](security.md)
- Hit an error? → [common-pitfalls.md](common-pitfalls.md)
- Need upgrade/factory/governance/DeFi architecture patterns? → [advanced-patterns.md](advanced-patterns.md)
- Need SEP/CAP guidance and standards links? → [standards-reference.md](standards-reference.md)

### 2. Pick the right building blocks
- Contracts: Soroban Rust SDK + Stellar CLI
- Frontend: stellar-sdk (JS) + Freighter/Wallets Kit
- Backend: stellar-sdk (JS/Python/Go) + RPC
- Assets: Classic operations or SAC for Soroban interop
- Testing: Quickstart (local) or Testnet

### 3. Implement with Stellar-specific correctness
Always be explicit about:
- Network passphrase (Mainnet vs Testnet vs local)
- Source account + sequence number
- Fee + resource limits (for Soroban)
- Authorization requirements
- Trustline status for assets
- Contract storage types (temporary vs persistent vs instance)

### 4. Add tests
- Unit tests: Native compilation with `#[test]`
- Integration tests: Local Quickstart or Testnet
- Contract tests: Use `Env` from soroban-sdk
- Frontend tests: Mock wallet/RPC interactions

### 5. Deliverables expectations
When you implement changes, provide:
- Exact files changed + diffs
- Commands to install/build/test/deploy
- Network configuration (passphrase, RPC endpoint)
- Risk notes for signing/fees/storage/authorization

## Progressive disclosure (read when needed)
- Smart contracts: [contracts-soroban.md](contracts-soroban.md)
- Frontend + wallets: [frontend-stellar-sdk.md](frontend-stellar-sdk.md)
- Testing strategy: [testing.md](testing.md)
- Stellar Assets: [stellar-assets.md](stellar-assets.md)
- Zero-knowledge proofs: [zk-proofs.md](zk-proofs.md)
- API access (RPC/Horizon): [api-rpc-horizon.md](api-rpc-horizon.md)
- Security checklist: [security.md](security.md)
- Common pitfalls: [common-pitfalls.md](common-pitfalls.md)
- Advanced architecture patterns: [advanced-patterns.md](advanced-patterns.md)
- SEP/CAP standards map: [standards-reference.md](standards-reference.md)
- Ecosystem projects: [ecosystem.md](ecosystem.md)
- Reference links: [resources.md](resources.md)

## Keywords
stellar, soroban, xlm, smart contracts, rust, wasm, webassembly, rpc, horizon,
freighter, stellar-sdk, soroban-sdk, stellar-cli, trustline, anchor, sep, passkey,
smart wallet, sac, stellar asset contract, defi, token, nft, scaffold stellar, constructor, upgrade, factory, governance, standards,
zero-knowledge, zk, zk-snark, groth16, bn254, poseidon, pairing, privacy, confidential, noir, risc zero, privacy pool, merkle tree
