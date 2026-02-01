---
name: multiversx-protocol-experts
description: Deep protocol knowledge for MultiversX architecture including sharding, consensus, ESDT standards, and cross-shard transactions. Use when reviewing protocol-level code, designing complex dApp architectures, or troubleshooting cross-shard issues.
---

# MultiversX Protocol Expertise

Deep technical knowledge of the MultiversX protocol architecture, utilized for reviewing protocol-level changes, designing complex dApp architectures involving cross-shard logic, and sovereign chain integrations.

## When to Use

- Reviewing protocol-level code changes
- Designing cross-shard smart contract interactions
- Troubleshooting async transaction issues
- Understanding token standard implementations
- Working with sovereign chain integrations
- Optimizing for sharded architecture

## 1. Core Architecture: Adaptive State Sharding

### Sharding Overview

MultiversX implements three types of sharding simultaneously:

| Sharding Type | Description | Implication |
|--------------|-------------|-------------|
| **Network** | Nodes distributed into shards | Each shard has subset of validators |
| **Transaction** | TXs processed by sender's shard | TX execution location is deterministic |
| **State** | Each shard maintains portion of state | Account data is shard-specific |

### Shard Assignment
Accounts are assigned to shards based on address:
```
Shard = last_byte_of_address % num_shards
```

**Practical implication**: Contract address determines which shard processes its transactions.

### The Metachain

The Metachain is a special coordinator shard that:
- Handles validator shuffling between shards
- Processes epoch transitions
- Manages system smart contracts (Staking, ESDT issuance)
- Notarizes shard block headers

**Important**: The Metachain does NOT execute general smart contracts.

```rust
// System contracts live on Metachain:
// - Staking contract
// - ESDT system smart contract
// - Delegation manager
// - Governance

// Regular contracts execute on shard determined by their address
```

## 2. Cross-Shard Transactions

### Transaction Flow

When sender and receiver are on different shards:

```
1. Sender Shard: Process TX, generate Smart Contract Result (SCR)
2. Metachain: Notarize sender block, relay SCR
3. Receiver Shard: Execute SCR, finalize transaction
```

### Atomicity Guarantees

**Key Property**: Cross-shard transactions are atomic but asynchronous.

```rust
// This cross-shard call is atomic
self.tx()
    .to(&other_contract)  // May be on different shard
    .typed(other_contract_proxy::OtherContractProxy)
    .some_endpoint(args)
    .async_call_and_exit();

// Either BOTH sides succeed, or BOTH sides revert
// But there's a delay between sender execution and receiver execution
```

### Callback Handling

```rust
#[endpoint]
fn cross_shard_call(&self) {
    // State changes HERE happen immediately (sender shard)
    self.pending_calls().set(true);

    self.tx()
        .to(&other_contract)
        .typed(proxy::Proxy)
        .remote_function()
        .callback(self.callbacks().on_result())
        .async_call_and_exit();
}

#[callback]
fn on_result(&self, #[call_result] result: ManagedAsyncCallResult<BigUint>) {
    // This executes LATER, back on sender shard
    // AFTER receiver shard has processed

    match result {
        ManagedAsyncCallResult::Ok(value) => {
            // Remote call succeeded
            self.pending_calls().set(false);
        },
        ManagedAsyncCallResult::Err(_) => {
            // Remote call failed
            // Original state changes are NOT auto-reverted!
            // Must manually handle rollback
            self.pending_calls().set(false);
            self.handle_failure();
        }
    }
}
```

## 3. Consensus: Secure Proof of Stake (SPoS)

### Validator Selection

```
Selection factors:
- Stake amount
- Validator rating (performance history)
- Random seed (from previous block)

Result: Deterministic but unpredictable validator selection
```

### Block Production

| Phase | Duration | Description |
|-------|----------|-------------|
| Propose | ~1s | Leader proposes block |
| Validate | ~1s | Validators verify and sign |
| Commit | ~1s | Block committed with BLS multi-sig |

### Finality

- **Intra-shard**: Instant finality (~6 seconds)
- **Cross-shard**: Finality after receiver shard processes (~12-18 seconds)

## 4. Token Standards (ESDT)

### Native Implementation

Unlike ERC-20, ESDT tokens are protocol-level, not smart contracts:

```rust
// ERC-20 (Ethereum): Contract tracks balances
mapping(address => uint256) balances;

// ESDT (MultiversX): Protocol tracks balances
// No contract needed for basic token operations
// Balances stored directly in account state
```

### ESDT Properties

| Property | Description | Security Implication |
|----------|-------------|---------------------|
| CanFreeze | Protocol can freeze assets | Emergency response capability |
| CanWipe | Protocol can wipe assets | Regulatory compliance |
| CanPause | Protocol can pause transfers | Circuit breaker |
| CanMint | Address can mint new tokens | Inflation control |
| CanBurn | Address can burn tokens | Supply control |
| CanChangeOwner | Ownership transferable | Admin key rotation |
| CanUpgrade | Properties can be modified | Flexibility vs immutability |

### ESDT Roles

```rust
// Roles are assigned per address per token
ESDTRoleLocalMint    // Can mint tokens
ESDTRoleLocalBurn    // Can burn tokens
ESDTRoleNFTCreate    // Can create NFT/SFT nonces
ESDTRoleNFTBurn      // Can burn NFT/SFT
ESDTRoleNFTAddQuantity   // Can add SFT quantity
ESDTRoleNFTUpdateAttributes  // Can update NFT attributes
ESDTTransferRole     // Required for restricted transfers
```

### Token Transfer Types

| Transfer Type | Function | Use Case |
|---------------|----------|----------|
| ESDTTransfer | Fungible token transfer | Simple token send |
| ESDTNFTTransfer | Single NFT/SFT transfer | NFT marketplace |
| MultiESDTNFTTransfer | Batch transfer | Contract calls with multiple tokens |

## 5. Built-in Functions

### Transfer Functions
```
ESDTTransfer@<token_id>@<amount>
ESDTNFTTransfer@<token_id>@<nonce>@<amount>@<receiver>
MultiESDTNFTTransfer@<receiver>@<num_tokens>@<token1_id>@<nonce1>@<amount1>@...
```

### Contract Call with Payment
```
MultiESDTNFTTransfer@<contract>@<num_tokens>@<token_data>...@<function>@<args>...
```

### Direct ESDT Operations
```
ESDTLocalMint@<token_id>@<amount>
ESDTLocalBurn@<token_id>@<amount>
ESDTNFTCreate@<token_id>@<initial_quantity>@<name>@<royalties>@<hash>@<attributes>@<uris>
```

## 6. Sovereign Chains & Interoperability

### Sovereign Chain Architecture

```
MultiversX Mainchain (L1)
    │
    ├── Sovereign Chain A (L2)
    │       └── Gateway Contract
    │
    └── Sovereign Chain B (L2)
            └── Gateway Contract
```

### Cross-Chain Communication

```rust
// Mainchain → Sovereign: Deposit flow
1. User deposits tokens to Gateway Contract on Mainchain
2. Gateway emits deposit event
3. Sovereign Chain validators observe event
4. Tokens minted on Sovereign Chain

// Sovereign → Mainchain: Withdrawal flow
1. User initiates withdrawal on Sovereign Chain
2. Sovereign validators create proof
3. Proof submitted to Mainchain Gateway
4. Tokens released on Mainchain
```

### Security Considerations

| Risk | Mitigation |
|------|------------|
| Bridge funds theft | Multi-sig validators, time locks |
| Invalid proofs | Cryptographic verification |
| Reorg attacks | Wait for finality before processing |
| Validator collusion | Slashing, stake requirements |

## 7. Critical Checks for Protocol Developers

### Intra-shard vs Cross-shard Awareness

```rust
// WRONG: Assuming synchronous execution
#[endpoint]
fn process_and_transfer(&self) {
    let result = self.external_contract().compute_value();  // May be async!
    self.storage().set(result);  // result may be callback, not value
}

// CORRECT: Handle async explicitly
#[endpoint]
fn process_and_transfer(&self) {
    self.tx()
        .to(&self.external_contract().get())
        .typed(proxy::Proxy)
        .compute_value()
        .callback(self.callbacks().handle_result())
        .async_call_and_exit();
}

#[callback]
fn handle_result(&self, #[call_result] result: ManagedAsyncCallResult<BigUint>) {
    match result {
        ManagedAsyncCallResult::Ok(value) => {
            self.storage().set(value);
        },
        ManagedAsyncCallResult::Err(_) => {
            // Handle failure
        }
    }
}
```

### Reorg Handling for Microservices

```typescript
// WRONG: Process immediately
async function handleTransaction(tx: Transaction) {
    await processPayment(tx);  // What if block is reverted?
}

// CORRECT: Wait for finality
async function handleTransaction(tx: Transaction) {
    // Wait for finality (configurable rounds)
    await waitForFinality(tx.hash, { rounds: 3 });

    // Or subscribe to finalized blocks only
    const status = await getTransactionStatus(tx.hash);
    if (status === 'finalized') {
        await processPayment(tx);
    }
}
```

### Gas Considerations for Cross-Shard

```rust
// Cross-shard calls consume gas on BOTH shards
// Sender: Gas for initiating call + callback execution
// Receiver: Gas for executing the called function

// Reserve enough gas for callback
const GAS_FOR_CALLBACK: u64 = 10_000_000;
const GAS_FOR_REMOTE: u64 = 20_000_000;

#[endpoint]
fn cross_shard_call(&self) {
    self.tx()
        .to(&other_contract)
        .typed(proxy::Proxy)
        .remote_function()
        .with_gas_limit(GAS_FOR_REMOTE)
        .callback(self.callbacks().on_result())
        .with_extra_gas_for_callback(GAS_FOR_CALLBACK)
        .async_call_and_exit();
}
```

## 8. MIP Standards Reference

Monitor MultiversX Improvement Proposals for standard implementations:

| MIP | Topic | Status |
|-----|-------|--------|
| MIP-2 | Fractional NFTs (SFT standard) | Implemented |
| MIP-3 | Dynamic NFTs | Implemented |
| MIP-4 | Token Royalties | Implemented |

## 9. Network Constants

| Constant | Value | Notes |
|----------|-------|-------|
| Max shards | 3 + Metachain | Current mainnet configuration |
| Round duration | ~6 seconds | Block time |
| Epoch duration | ~24 hours | Validator reshuffling period |
| Max TX size | 256 KB | Transaction data limit |
| Max gas limit | 600,000,000 | Per transaction |
