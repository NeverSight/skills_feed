---
name: evm-address
description: Guide for generating deterministic EVM deposit addresses offline using @evm-address/sdk and CLI. Supports BIP-44 (XPUB) and CREATE2 (Factory) strategies with zero private key exposure. Use when implementing deposit systems, batch sweeping, or offline address generation.
---

# EVM Address Generator

## Overview

The `evm-address` toolkit allows for the offline, deterministic generation of EVM deposit addresses. It supports two primary modes:

1.  **XPUB (BIP-44)**: Generates EOA addresses using an extended public key.
2.  **Factory (CREATE2)**: Generates contract addresses for EIP-1167 minimal proxies.

## Installation

### SDK

```bash
npm install @evm-address/sdk
```

### CLI

```bash
npm install -g @evm-address/cli
```

## Quick Start (SDK)

```typescript
import { createXpubGenerator } from "@evm-address/sdk";

const generator = createXpubGenerator({ xpub: "xpub..." });
const address = generator.generate(0);
```

## Detailed Documentation

- **[SDK Guide](references/sdk.md)**: Full API for programatic address generation.
- **[CLI Guide](references/cli.md)**: Usage patterns for the command-line tool.
- **[Smart Contract Deployment](references/deployment.md)**: How to deploy and verify the required contracts.
- **[Contract Source Code](references/contracts.md)**: Solidity source code for Factory, Delegate, and Permit contracts.

## Strategies Support

| Strategy        | Logic                                         |
| --------------- | --------------------------------------------- |
| **BIP-44**      | Traditional EOA derivation (m/44'/60'/0'/0/i) |
| **CREATE2**     | Counterfactual contracts via `WalletFactory`  |
| **EIP-7702**    | Delegation to `SweeperDelegate`               |
| **Permit/Auth** | Batch sweeping via `PermitSweeper`            |

## Security Note

This tool is designed for **offline use** and **never** requires your private keys. It only uses public information (XPUB or contract addresses) to derive deterministic deposit locations.
