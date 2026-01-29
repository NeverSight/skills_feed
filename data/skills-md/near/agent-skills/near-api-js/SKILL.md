---
name: near-api-js
description: >-
  Guide for developing with near-api-js v7 - the JavaScript/TypeScript library for NEAR blockchain interaction. 
  Use when: (1) building apps that interact with NEAR blockchain, (2) creating/signing transactions, 
  (3) calling smart contracts, (4) managing accounts and keys, (5) working with NEAR RPC API, 
  (6) handling FT/NFT tokens on NEAR, (7) using NEAR cryptographic operations (KeyPair, signing), 
  (8) converting between NEAR units (yocto, gas), (9) gasless/meta transactions with relayers,
  (10) wallet integration and session management, (11) NEP-413 message signing for authentication,
  (12) storage deposit management for FT contracts. Triggers on any NEAR blockchain development tasks.
---

# near-api-js Skill

JavaScript/TypeScript library for NEAR blockchain interaction. Works in browser and Node.js.

## Quick Start

```typescript
import { Account, JsonRpcProvider, KeyPair } from "near-api-js"
import { NEAR } from "near-api-js/tokens"

// Connect to testnet
const provider = new JsonRpcProvider({ url: "https://test.rpc.fastnear.com" })

// Create account with signer
const account = new Account("my-account.testnet", provider, "ed25519:...")
```

## Import Cheatsheet

```typescript
// Core
import { Account, actions, JsonRpcProvider, FailoverRpcProvider } from "near-api-js"
import { KeyPair, PublicKey, KeyType } from "near-api-js"

// Tokens
import { NEAR, FungibleToken, NFTContract } from "near-api-js/tokens"
import { USDC, wNEAR } from "near-api-js/tokens/mainnet"

// Seed phrases
import { generateSeedPhrase, parseSeedPhrase } from "near-api-js/seed-phrase"

// Signers
import { KeyPairSigner, MultiKeySigner, Signer } from "near-api-js"

// Units
import { nearToYocto, yoctoToNear, teraToGas, gigaToGas } from "near-api-js"

// Transactions
import { createTransaction, signTransaction } from "near-api-js"

// Error handling
import { TypedError, parseTransactionExecutionError } from "near-api-js"
```

## Core Modules

### Account

Main class for account operations.

```typescript
const account = new Account(accountId, provider, privateKey)

// Get state
const state = await account.getState()  // { balance: { total, available, locked }, storageUsage }

// Transfer NEAR
await account.transfer({ receiverId: "bob.testnet", amount: NEAR.toUnits("1"), token: NEAR })

// Call contract
await account.callFunction({
  contractId: "contract.testnet",
  methodName: "set_greeting",
  args: { message: "Hello" },
  deposit: 0n,
  gas: 30_000_000_000_000n
})

// Sign and send transaction
await account.signAndSendTransaction({
  receiverId: "contract.testnet",
  actions: [
    actions.functionCall("method", { arg: "value" }, 30_000_000_000_000n, 0n),
    actions.transfer(1_000_000_000_000_000_000_000_000n)
  ]
})
```

### Provider

RPC client for querying blockchain.

```typescript
const provider = new JsonRpcProvider({ url: "https://rpc.mainnet.near.org" })

// Failover provider
const failover = new FailoverRpcProvider([
  new JsonRpcProvider({ url: "https://rpc.mainnet.near.org" }),
  new JsonRpcProvider({ url: "https://rpc.mainnet.pagoda.co" })
])

// Query methods
await provider.viewAccount({ accountId: "alice.near" })
await provider.viewAccessKey({ accountId, publicKey })
await provider.callFunction({ contractId, method: "get_greeting", args: {} })
await provider.viewBlock({ finality: "final" })
await provider.sendTransaction(signedTx)
```

### Crypto

Key management and cryptographic operations.

```typescript
import { KeyPair, PublicKey } from "near-api-js"

// Generate random keypair
const keyPair = KeyPair.fromRandom("ed25519")

// From string
const keyPair = KeyPair.fromString("ed25519:5Fg2...")

// Sign and verify
const { signature, publicKey } = keyPair.sign(data)
const verified = keyPair.verify(message, signature)
```

### Tokens

FT and NFT support.

```typescript
import { NEAR, FungibleToken } from "near-api-js/tokens"
import { USDC } from "near-api-js/tokens/mainnet"

// Unit conversion
NEAR.toUnits("1.5")  // 1500000000000000000000000n
NEAR.toDecimal(amount)  // "1.5"

// Transfer FT
await account.transfer({ receiverId: "bob.near", amount: USDC.toUnits("50"), token: USDC })

// Custom FT
const token = new FungibleToken("usdt.tether-token.near", { decimals: 6, name: "USDT", symbol: "USDT" })
```

### Actions

All transaction actions.

```typescript
import { actions } from "near-api-js"

actions.transfer(amount)
actions.functionCall(methodName, args, gas, deposit)
actions.createAccount()
actions.deployContract(wasmBytes)
actions.addFullAccessKey(publicKey)
actions.addFunctionAccessKey(publicKey, contractId, methodNames, allowance)
actions.deleteKey(publicKey)
actions.deleteAccount(beneficiaryId)
actions.stake(amount, publicKey)
actions.signedDelegate(signedDelegateAction)  // Meta transactions
```

## RPC Endpoints

| Network | URL |
|---------|-----|
| Mainnet | `https://rpc.mainnet.near.org` |
| Mainnet (Pagoda) | `https://rpc.mainnet.pagoda.co` |
| Mainnet (FastNEAR) | `https://free.rpc.fastnear.com` |
| Testnet | `https://rpc.testnet.near.org` |
| Testnet (FastNEAR) | `https://test.rpc.fastnear.com` |

## Common Patterns

### View Contract State

```typescript
const result = await provider.callFunction({
  contractId: "contract.near",
  method: "get_data",
  args: { key: "value" }
})
```

### Change Contract State

```typescript
await account.callFunction({
  contractId: "contract.near",
  methodName: "set_data",
  args: { key: "new_value" },
  gas: 30_000_000_000_000n,
  deposit: 0n
})
```

### Batch Transactions

```typescript
await account.signAndSendTransactions({
  transactions: [
    { receiverId: "bob.near", actions: [actions.transfer(NEAR.toUnits("1"))] },
    { receiverId: "alice.near", actions: [actions.transfer(NEAR.toUnits("2"))] }
  ]
})
```

### Meta Transactions (Gasless)

```typescript
// Create signed meta tx (user side)
const signedDelegate = await account.createSignedMetaTransaction({
  receiverId: "contract.near",
  actions: [actions.functionCall("method", {}, 30_000_000_000_000n, 0n)]
})

// Submit via relayer
await relayerAccount.signAndSendTransaction({
  receiverId: signedDelegate.delegateAction.senderId,
  actions: [actions.signedDelegate(signedDelegate)]
})
```

### Contract Interface

```typescript
import { Contract } from "near-api-js"

const contract = new Contract(account, "contract.near", {
  viewMethods: ["get_status"],
  changeMethods: ["set_status"]
})

const status = await contract.get_status()
await contract.set_status({ message: "Hello" })
```

## Error Handling

```typescript
import { parseTransactionExecutionError, TypedError, InvalidNonceError } from "near-api-js"

try {
  await account.signAndSendTransaction({ ... })
} catch (error) {
  if (error instanceof TypedError) {
    console.log(error.type, error.message)
  }
  if (error instanceof InvalidNonceError) {
    // Retry with fresh nonce
  }
}
```

## Reference Documentation

For detailed patterns and advanced usage, see:

- [API Patterns Reference](references/api_patterns.md) - Complete Account/Provider method reference, type definitions
- [Tokens Guide](references/tokens_guide.md) - FT/NFT operations, storage deposits, pre-defined tokens
- [Key Management](references/key_management.md) - KeyPair types, seed phrases, signers, access keys
- [Meta Transactions](references/meta_transactions.md) - Gasless transactions, relayer integration
- [Wallet Integration](references/wallet_integration.md) - Browser patterns, NEP-413 signing, sessions
