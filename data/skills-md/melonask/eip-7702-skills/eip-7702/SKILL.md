---
name: eip-7702
description: Expert guide for EIP-7702 implementation, implementing sponsored transactions, creating delegated smart contracts, and interacting via Viem v2. Use when needing to implement `gasless` token transfers via EIP-7702, create batching contracts, or understand the EIP-7702 transaction flow with Viem.
---

# EIP-7702 Implementation Guide

## Overview

EIP-7702 enables Externally Owned Accounts (EOAs) to temporarily delegate their code to a smart contract during a transaction. This allows EOAs to function as smart contracts, enabling features like:

- **Sponsored Transactions**: A relayer pays gas for the EOA.
- **Batching**: Multiple operations in one atomic transaction.
- **Key Rotation/Recovery**: Programmable access control.

## 1. Smart Contract Development

To use EIP-7702, you need an implementation contract. This contract will be the code that the EOA "borrows".

**Key Requirement**: The contract must handle authentication (ensure the EOA signed the intent) and replay protection (nonce), as the EIP-7702 authorization only delegates code, it doesn't inherently validate the _payload_ of the function call if anyone can call it.

### Reference Implementation

A robust example supporting Batching and Sponsorship is available in `assets/BatchCallAndSponsor.sol`.

**Features:**

- `execute(calls, signature)`: For sponsored transactions. Requires an inner signature from the EOA verifying the batch and nonce.
- `execute(calls)`: For direct execution (when `msg.sender == address(this)`).

## 2. Testing with Foundry

Foundry supports EIP-7702 via the `prague` EVM version and specific cheatcodes.

**Key Cheatcodes:**

- `signDelegation`: Creates the EIP-7702 authorization signature.
- `attachDelegation`: Attaches the authorization to the next transaction.

See [Foundry Guide](references/foundry-guide.md) for detailed test patterns and configuration.
See `assets/test/BatchCallAndSponsor.t.sol` for a complete test suite.

## 3. Client Interaction (Viem v2)

Viem v2 provides first-class support for EIP-7702 via `signAuthorization` and `sendTransaction`/`writeContract` with `authorizationList`.

**Best Practices:**

- Use `writeContract` with strongly typed ABIs (`as const`) for safer interactions.
- Ensure correct signing of raw hashes using `signMessage({ message: { raw: ... } })`.
- No experimental extensions are required in modern Viem versions.

See [Viem Guide](references/viem-guide.md) for code snippets and TypeScript patterns.
