---
name: blockchain-engineer
description: Use when architecturalizing protocols, developing smart contracts, or auditing security for blockchain systems.
license: MIT
metadata:
  version: "2.0"
---

# Blockchain Engineering Standards

This skill provides expert guidelines for building the decentralized layer with a focus on security, scalability, and economic robustness.

## Core Responsibilities

1.  **Protocol Architecture**: Design tokenomics, governance structures, and ensuring incentive alignment across the network.
2.  **Smart Contract Mastery**: End-to-end lifecycle management of smart contracts on EVM (Solidity/Yul) and SVM (Rust/Anchor).
3.  **Advanced Security**: Protect value through formal verification, fuzzing, and rigorous audit preparation.
4.  **Scaling Solutions**: Architect solutions using L2s, Optimistic/ZK Rollups, and AppChains.

## Technical Standards & Best Practices

### Development Lifecycle

- **Environment**: Master usage of Hardhat and Foundry (Forge/Cast/Anvil) for EVM; Anchor for Solana.
- **Testing**: Beyond unit tests—implement invariant testing, fuzzing (Echo/Medusa), and fork testing.
- **CI/CD**: Automated pipelines for linting, testing, and deterministic deployments.

### Optimization & Quality

- **Gas Golfing**: Optimize for gas efficiency using Yul/Assembly, storage layout packing, and calldata mastery.
- **Code Quality**: Enforce NatSpec documentation, strict linting (Solhint/Clippy), and clean code patterns.

### Deployment & Ops

- **Patterns**: Use deterministic deployment (Create2) and manage upgrades via standard proxies (Transparent, UUPS, Diamond/EIP-2535).
- **Security**: Manage keys via Multi-sig (Gnosis Safe) and Timelocks. Automate ops with scripting.

## Architecture Patterns

- **Upgradeability**: Future-proof contracts using Transparent, UUPS, or Diamond patterns.
- **Interoperability**: Connect chains using Bridges, Atomic Swaps, and CCIP.
- **Data Integration**: Index data with Subgraphs (The Graph) and secure external feeds via Oracles (Chainlink, Pyth).

## Dynamic Stack Loading

- **EVM (Ethereum/Polygon/Arbitrum)**:
  - [EVM Overview](references/evm.md)
  - [Solidity Development](references/solidity.md)
  - [Deployment & Ops](references/deployment.md)
  - [Mechanisms & Internals](references/mechanisms.md)
- **Solana**: (Create `references/solana.md` if needed)
- **ZK & Privacy**: Focus on ZK-SNARKs/STARKs for privacy and scaling.
