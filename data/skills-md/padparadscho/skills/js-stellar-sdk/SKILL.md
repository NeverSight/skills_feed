---
name: js-stellar-sdk
description: Guide for building applications with the Stellar JS SDK (@stellar/stellar-sdk). Use when working with the Stellar blockchain in JavaScript/TypeScript — including sending payments, creating accounts, issuing assets, managing trustlines, trading on the DEX, querying Horizon, interacting with Stellar RPC, streaming events, building and signing transactions, multisig, claimable balances, sponsored reserves, SEP-10 auth, federation, fee-bump transactions, and interacting with Soroban smart contracts via the JS SDK. Covers all @stellar/stellar-sdk usage patterns (Horizon module, rpc module, contract module, TransactionBuilder, Keypair, Operation, Asset, etc.).
---

# Stellar JS SDK

Build applications on the Stellar network using `@stellar/stellar-sdk` (v14.x, Node 20+).

## Installation

```bash
npm install @stellar/stellar-sdk
```

Import only what you need:

```typescript
import {
  Keypair,
  Horizon,
  rpc,
  TransactionBuilder,
  Networks,
  Operation,
  Asset,
  Memo,
  BASE_FEE,
} from "@stellar/stellar-sdk";
```

Never install `@stellar/stellar-base` separately — the SDK re-exports everything from it.

## Quick Start

```typescript
import {
  Keypair,
  Horizon,
  TransactionBuilder,
  Networks,
  Operation,
  Asset,
  BASE_FEE,
} from "@stellar/stellar-sdk";

// 1. Create keypair and fund on testnet
const keypair = Keypair.random();
await fetch(`https://friendbot.stellar.org?addr=${keypair.publicKey()}`);

// 2. Connect to Horizon
const server = new Horizon.Server("https://horizon-testnet.stellar.org");

// 3. Build, sign, submit a payment
const account = await server.loadAccount(keypair.publicKey());
const tx = new TransactionBuilder(account, {
  fee: BASE_FEE,
  networkPassphrase: Networks.TESTNET,
})
  .addOperation(
    Operation.payment({
      destination: "GABC...",
      asset: Asset.native(),
      amount: "10",
    }),
  )
  .setTimeout(30)
  .build();

tx.sign(keypair);
const result = await server.submitTransaction(tx);
```

## Core Workflow

Every Stellar JS SDK interaction follows this pattern:

1. **Connect** — create `Horizon.Server` or `rpc.Server` instance
2. **Load account** — fetch current sequence number via `server.loadAccount()`
3. **Build transaction** — use `TransactionBuilder` with operations
4. **Sign** — call `transaction.sign(keypair)`
5. **Submit** — call `server.submitTransaction(transaction)`

Always set `.setTimeout(30)` on transactions. Always handle errors by inspecting `error.response.data.extras.result_codes`.

## Key Concepts

- **Stroops**: 1 XLM = 10,000,000 stroops. `BASE_FEE` = 100 stroops.
- **Amounts**: Always strings with up to 7 decimal places (e.g., `'100.1234567'`).
- **Sequence numbers**: Auto-managed when using `server.loadAccount()`.
- **Network passphrase**: Transactions are network-specific. Use `Networks.TESTNET`, `Networks.PUBLIC`, etc.
- **Trustlines**: Required before receiving any non-XLM asset.
- **Base reserve**: 0.5 XLM per account subentry (trustlines, offers, signers, data entries).
- **Max 100 operations** per transaction (1 for smart contract operations).

## When to Use Horizon vs RPC

| Use Case                                               | Module                         |
| ------------------------------------------------------ | ------------------------------ |
| Account balances, payment history, transaction queries | `Horizon.Server`               |
| Streaming payments, transactions, effects              | `Horizon.Server` (`.stream()`) |
| Orderbook, DEX trading, trade history                  | `Horizon.Server`               |
| Asset info, fee stats, ledger data                     | `Horizon.Server`               |
| Smart contract interactions                            | `rpc.Server`                   |
| Transaction simulation (`simulateTransaction`)         | `rpc.Server`                   |
| Contract events                                        | `rpc.Server`                   |
| Preparing contract transactions (`prepareTransaction`) | `rpc.Server`                   |

## Reference Files

- **[API Reference](references/api-reference.md)**: Complete class/method reference for all SDK modules — Keypair, TransactionBuilder, Horizon.Server, rpc.Server, Operations, Assets, contract module, WebAuth, Federation, StellarToml, XDR helpers. Read when you need specific method signatures or parameter details.

- **[Code Examples](references/examples.md)**: Working code examples for all common tasks — payments, path payments, asset issuance, trustlines, DEX trading, streaming, fee-bumps, claimable balances, sponsored reserves, multisig, RPC interactions, SEP-10 auth, federation, error handling. Read when implementing a specific feature.

- **[Networks & Configuration](references/networks.md)**: Network URLs, passphrases, Friendbot, testnet/mainnet switching, CLI bindings generation, browser/React Native setup, key limits. Read when configuring the SDK for a specific environment or deploying to a different network.
