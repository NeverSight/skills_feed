---
name: evm-balance
description: Comprehensive guide for the EVM Balance project, including CLI usage, SDK integration, and development workflow. Use when working with EVM balance fetching, configuring the CLI, or integrating the SDK.
---

# EVM Balance Skill

## Overview

The `evm-balance` project is a high-performance library and CLI for fetching EVM balances across multiple chains using Multicall3. It supports native and ERC20 token balances, address generation (XPUB, CREATE2), and batch processing.

**Key Components:**
- **SDK** (`@evm-balance/sdk`): Core library for fetching balances.
- **CLI** (`@evm-balance/cli`): Command-line interface for easy interaction.
- **Contracts**: Solidity contracts for Multicall3 interactions.

## Project Structure

```
evm-balance/
├── packages/
│   ├── sdk/              # Core library
│   │   ├── src/
│   │   │   ├── index.ts     # Main exports
│   │   │   ├── types.ts     # TypeScript interfaces
│   │   │   ├── balance.ts   # Balance fetching logic
│   │   │   ├── multicall.ts # Multicall3 encoding/decoding
│   │   │   ├── chains.ts    # Chain utilities
│   │   │   └── utils.ts     # Range parsing, formatting
│   │   └── package.json
│   └── cli/              # CLI tool
│       ├── src/
│       │   └── index.ts     # CLI implementation
│       └── package.json
├── src/                  # Solidity contracts
│   └── Multicall3.sol
├── script/               # Deployment scripts
│   └── DeployTest.s.sol
└── package.json          # Workspace root
```

## CLI Usage

The CLI provides a powerful interface for fetching balances.

### Quick Start

```bash
# Query multiple chains
evm-balance 0-100 --chain mainnet,optimism,arbitrum --xpub $XPUB

# Query specific tokens
evm-balance 0-100 -c mainnet -t 0xA0b86991...USDC,0xdAC17F9...USDT -X $XPUB

# Filter by minimum balance
evm-balance 0-1000 -c mainnet -t 0xUSDT,0xUSDC --min 0.1

# Output as JSON
evm-balance 0-100 -c mainnet -f json -o balances.json
```

### Common Options

- `-c, --chains`: Comma-separated chain names or IDs (e.g., `mainnet,optimism`).
- `-t, --tokens`: Comma-separated ERC20 token addresses.
- `-m, --min`: Minimum balance filter.
- `-f, --format`: Output format (`table`, `json`, `csv`).
- `-X, --xpub`: Extended public key for BIP-44 address generation.
- `--mode`: Address generation mode (`xpub` or `factory`).

## SDK Usage

The SDK allows programmatically fetching balances.

### Basic Example

```typescript
import { createBalanceFetcher, parseRange, mainnet } from "@evm-balance/sdk";

const fetcher = createBalanceFetcher({ chain: mainnet });

const results = await fetcher.fetchBalances({
  config: { chain: mainnet },
  mode: { type: "xpub", xpub: process.env.XPUB! },
  indices: parseRange("0-100"),
  options: {
    tokens: ["0xA0b86991..."], // USDC
    includeNative: true,
  },
});
```

**For detailed API documentation, see [sdk_api.md](references/sdk_api.md).**

## Development Workflow

### Prerequisites
- `bun`
- `foundry` (forge, anvil)

### Commands

```bash
# Install dependencies
bun install

# Build all packages
bun run build

# Run tests
bun run test

# Run Solidity tests (requires Anvil)
bun run test:sol

# Type check
bun run typecheck

# Format code
bun run fmt
```

### Testing with Anvil

```bash
# 1. Start Anvil
anvil

# 2. Deploy test contracts
forge script script/DeployTest.s.sol:DeployTest --rpc-url http://127.0.0.1:8545 --broadcast

# 3. Run tests
bun run test
```