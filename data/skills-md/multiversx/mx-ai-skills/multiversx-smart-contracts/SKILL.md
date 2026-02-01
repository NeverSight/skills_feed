---
name: multiversx-smart-contracts
description: Build MultiversX smart contracts with Rust. Use when app needs blockchain logic, token creation, NFT minting, staking, crowdfunding, or any on-chain functionality requiring custom smart contracts.
---

# MultiversX Smart Contract Development

Build, test, and deploy MultiversX smart contracts using Rust, sc-meta, and mxpy.

## Prerequisites

Tools available on the VM:
- **Rust** (version 1.83.0+)
- **sc-meta** - Smart contract meta tool
- **mxpy** - MultiversX Python CLI for deployment

If sc-meta is not installed:
```bash
cargo install multiversx-sc-meta --locked
```

## Creating a New Contract

Use sc-meta to scaffold a new contract from templates:

```bash
# List available templates
sc-meta templates

# Create from template
sc-meta new --template adder --name my-contract

# Available templates:
# - empty: Minimal contract structure
# - adder: Basic arithmetic operations
# - crypto-zombies: NFT game example
```

## Project Structure

After creating a contract, you get this structure:

```
my-contract/
├── Cargo.toml           # Dependencies
├── src/
│   └── lib.rs           # Contract code
├── meta/
│   ├── Cargo.toml       # Meta crate dependencies
│   └── src/
│       └── main.rs      # Build tooling entry
├── wasm/
│   ├── Cargo.toml       # WASM output config
│   └── src/
│       └── lib.rs       # WASM entry point
└── scenarios/           # Test files (optional)
```

## Cargo.toml Configuration

```toml
[package]
name = "my-contract"
version = "0.0.0"
edition = "2021"

[lib]
path = "src/lib.rs"

[dependencies.multiversx-sc]
version = "0.54.0"

[dev-dependencies.multiversx-sc-scenario]
version = "0.54.0"
```

## Basic Contract Structure

```rust
#![no_std]

use multiversx_sc::imports::*;

#[multiversx_sc::contract]
pub trait MyContract {
    #[init]
    fn init(&self, initial_value: BigUint) {
        self.stored_value().set(initial_value);
    }

    #[upgrade]
    fn upgrade(&self) {
        // Called when contract is upgraded
    }

    #[endpoint]
    fn add(&self, value: BigUint) {
        self.stored_value().update(|v| *v += value);
    }

    #[view(getValue)]
    fn get_value(&self) -> BigUint {
        self.stored_value().get()
    }

    #[storage_mapper("storedValue")]
    fn stored_value(&self) -> SingleValueMapper<BigUint>;
}
```

## Core Annotations

### Contract & Module Level

| Annotation | Purpose |
|------------|---------|
| `#[multiversx_sc::contract]` | Marks trait as main contract (one per crate) |
| `#[multiversx_sc::module]` | Marks trait as reusable module |
| `#[multiversx_sc::proxy]` | Creates proxy for calling other contracts |

### Method Level

| Annotation | Purpose |
|------------|---------|
| `#[init]` | Constructor, called on deploy |
| `#[upgrade]` | Called when contract is upgraded |
| `#[endpoint]` | Public callable method |
| `#[view]` | Read-only public method |
| `#[endpoint(customName)]` | Endpoint with custom ABI name |
| `#[view(customName)]` | View with custom ABI name |

### Payment Annotations

| Annotation | Purpose |
|------------|---------|
| `#[payable("*")]` | Accepts any token payment |
| `#[payable("EGLD")]` | Accepts only EGLD |
| `#[payable("TOKEN-ID")]` | Accepts specific token |

### Event Annotations

| Annotation | Purpose |
|------------|---------|
| `#[event("eventName")]` | Defines contract event |
| `#[indexed]` | Marks event field as searchable topic |

## Storage Mappers

### SingleValueMapper
Stores a single value.

```rust
#[storage_mapper("owner")]
fn owner(&self) -> SingleValueMapper<ManagedAddress>;

// Usage
self.owner().set(caller);
let owner = self.owner().get();
self.owner().is_empty();
self.owner().clear();
self.owner().update(|v| *v = new_value);
```

### VecMapper
Stores indexed array (1-indexed).

```rust
#[storage_mapper("items")]
fn items(&self) -> VecMapper<BigUint>;

// Usage
self.items().push(&value);
let item = self.items().get(1); // 1-indexed!
self.items().set(1, &new_value);
let len = self.items().len();
for item in self.items().iter() { }
self.items().swap_remove(1);
```

### SetMapper
Unique collection with O(1) lookup, preserves insertion order.

```rust
#[storage_mapper("whitelist")]
fn whitelist(&self) -> SetMapper<ManagedAddress>;

// Usage
self.whitelist().insert(address); // Returns false if duplicate
self.whitelist().contains(&address); // O(1)
self.whitelist().remove(&address);
for addr in self.whitelist().iter() { }
```

### UnorderedSetMapper
Like SetMapper but more efficient when order doesn't matter.

```rust
#[storage_mapper("participants")]
fn participants(&self) -> UnorderedSetMapper<ManagedAddress>;
```

### MapMapper
Key-value pairs. **Expensive - avoid when iteration not needed.**

```rust
#[storage_mapper("balances")]
fn balances(&self) -> MapMapper<ManagedAddress, BigUint>;

// Usage
self.balances().insert(address, amount);
let balance = self.balances().get(&address); // Returns Option
self.balances().contains_key(&address);
self.balances().remove(&address);
for (addr, bal) in self.balances().iter() { }
```

### LinkedListMapper
Doubly-linked list for queue operations.

```rust
#[storage_mapper("queue")]
fn queue(&self) -> LinkedListMapper<BigUint>;

// Usage
self.queue().push_back(value);
self.queue().push_front(value);
self.queue().pop_front();
self.queue().pop_back();
```

### FungibleTokenMapper
Manages fungible token with built-in ESDT operations.

```rust
#[storage_mapper("token")]
fn token(&self) -> FungibleTokenMapper;

// Usage
self.token().issue_and_set_all_roles(...);
self.token().mint(amount);
self.token().burn(amount);
self.token().get_balance();
```

### NonFungibleTokenMapper
Manages NFT/SFT/META-ESDT tokens.

```rust
#[storage_mapper("nft")]
fn nft(&self) -> NonFungibleTokenMapper;

// Usage
self.nft().nft_create(amount, &attributes);
self.nft().nft_add_quantity(nonce, amount);
self.nft().get_all_token_data(nonce);
```

## Data Types

### Core Types

| Type | Description |
|------|-------------|
| `BigUint` | Unsigned arbitrary-precision integer |
| `BigInt` | Signed arbitrary-precision integer |
| `ManagedBuffer` | Byte array (strings, raw data) |
| `ManagedAddress` | 32-byte address |
| `TokenIdentifier` | Token ID (e.g., "EGLD", "TOKEN-abc123") |
| `EgldOrEsdtTokenIdentifier` | Either EGLD or ESDT token ID |
| `EsdtTokenPayment` | Token ID + nonce + amount |

### Creating Values

```rust
// BigUint
let amount = BigUint::from(1000u64);
let zero = BigUint::zero();

// ManagedBuffer (strings)
let buffer = ManagedBuffer::from("hello");

// Address
let caller = self.blockchain().get_caller();

// Token identifier
let token = TokenIdentifier::from("TOKEN-abc123");
```

## Payment Handling

### Receiving EGLD

```rust
#[payable("EGLD")]
#[endpoint]
fn deposit_egld(&self) {
    let payment = self.call_value().egld_value();
    let amount = payment.clone_value();
    // process payment...
}
```

### Receiving Any Single Token

```rust
#[payable("*")]
#[endpoint]
fn deposit(&self) {
    let payment = self.call_value().single_esdt();
    let token_id = payment.token_identifier;
    let nonce = payment.token_nonce;
    let amount = payment.amount;
}
```

### Receiving EGLD or Single ESDT

```rust
#[payable("*")]
#[endpoint]
fn flexible_deposit(&self) {
    let payment = self.call_value().egld_or_single_esdt();
    // Returns EgldOrEsdtTokenPayment
}
```

### Receiving Multiple Tokens

```rust
#[payable("*")]
#[endpoint]
fn multi_deposit(&self) {
    let payments = self.call_value().all_esdt_transfers();
    for payment in payments.iter() {
        // process each payment
    }
}
```

### Sending Tokens

```rust
// Send EGLD
self.tx()
    .to(&recipient)
    .egld(amount)
    .transfer();

// Send ESDT
self.tx()
    .to(&recipient)
    .single_esdt(&token_id, nonce, &amount)
    .transfer();

// Send EGLD or ESDT (Unified)
self.tx()
    .to(&recipient)
    .payment((token_id, nonce, amount))
    .transfer();
```

**CRITICAL:** You cannot send both EGLD and ESDT in the same transaction.

## Events

```rust
#[event("deposit")]
fn deposit_event(
    &self,
    #[indexed] caller: &ManagedAddress,
    #[indexed] token: &TokenIdentifier,
    amount: &BigUint,
);

// Emit event
self.deposit_event(&caller, &token_id, &amount);
```

## Modules

Split large contracts into modules:

```rust
// In src/storage.rs
#[multiversx_sc::module]
pub trait StorageModule {
    #[storage_mapper("owner")]
    fn owner(&self) -> SingleValueMapper<ManagedAddress>;
}

// In src/lib.rs
mod storage;

#[multiversx_sc::contract]
pub trait MyContract: storage::StorageModule {
    #[init]
    fn init(&self) {
        self.owner().set(self.blockchain().get_caller());
    }
}
```

## Error Handling

```rust
// Using require!
#[endpoint]
fn withdraw(&self, amount: BigUint) {
    let caller = self.blockchain().get_caller();
    require!(
        caller == self.owner().get(),
        "Only owner can withdraw"
    );
    require!(amount > 0, "Amount must be positive");
}

// Using sc_panic!
if condition_failed {
    sc_panic!("Operation failed");
}
```

## Building Contracts

### Build All Contracts in Workspace

```bash
sc-meta all build
```

### Build Single Contract

```bash
cd my-contract/meta
cargo run build
```

### Build with Options

```bash
# Build with locked dependencies
sc-meta all build --locked

# Debug build with WAT output
cd meta && cargo run build-dbg
```

### Build Output

After building, find outputs in `output/`:
- `my-contract.wasm` - Contract bytecode
- `my-contract.abi.json` - Contract ABI

## Testing

### Rust-Based Tests

Create tests in `tests/` folder:

```rust
use multiversx_sc_scenario::*;

fn world() -> ScenarioWorld {
    let mut blockchain = ScenarioWorld::new();
    blockchain.register_contract(
        "mxsc:output/my-contract.mxsc.json",
        my_contract::ContractBuilder,
    );
    blockchain
}

#[test]
fn test_deploy() {
    let mut world = world();
    world.run("scenarios/deploy.scen.json");
}
```

### Running Tests

```bash
# Run all tests
sc-meta test

# Run specific test
cargo test test_deploy
```

## Deploying with mxpy

### Deploy New Contract

```bash
mxpy contract deploy \
    --bytecode output/my-contract.wasm \
    --proxy https://devnet-api.multiversx.com \
    --chain D \
    --pem wallet.pem \
    --gas-limit 60000000 \
    --arguments 1000 \
    --send
```

### Upgrade Existing Contract

```bash
mxpy contract upgrade <contract-address> \
    --bytecode output/my-contract.wasm \
    --proxy https://devnet-api.multiversx.com \
    --chain D \
    --pem wallet.pem \
    --gas-limit 60000000 \
    --send
```

### Call Contract Endpoint

```bash
mxpy contract call <contract-address> \
    --proxy https://devnet-api.multiversx.com \
    --chain D \
    --pem wallet.pem \
    --gas-limit 5000000 \
    --function "add" \
    --arguments 100 \
    --send
```

### Query View Function

```bash
mxpy contract query <contract-address> \
    --proxy https://devnet-api.multiversx.com \
    --function "getValue"
```

### Network Endpoints

| Network | Proxy URL | Chain ID |
|---------|-----------|----------|
| Devnet | `https://devnet-api.multiversx.com` | D |
| Testnet | `https://testnet-api.multiversx.com` | T |
| Mainnet | `https://api.multiversx.com` | 1 |

## Advanced Patterns

### Cross-Contract Calls with Proxy

```rust
// Define proxy trait
#[multiversx_sc::proxy]
pub trait OtherContract {
    #[endpoint]
    fn some_endpoint(&self, value: BigUint);
}

// Use proxy
#[endpoint]
fn call_other(&self, other_address: ManagedAddress, value: BigUint) {
    self.tx()
        .to(&other_address)
        .typed(other_contract_proxy::OtherContractProxy)
        .some_endpoint(value)
        .sync_call();
}
```

### Async Calls with Callbacks

```rust
#[endpoint]
fn async_call(&self, other_address: ManagedAddress) {
    self.tx()
        .to(&other_address)
        .typed(other_contract_proxy::OtherContractProxy)
        .some_endpoint()
        .callback(self.callbacks().my_callback())
        .async_call_and_exit();
}

#[callback]
fn my_callback(&self, #[call_result] result: ManagedAsyncCallResult<BigUint>) {
    match result {
        ManagedAsyncCallResult::Ok(value) => {
            // Handle success
        }
        ManagedAsyncCallResult::Err(err) => {
            // Handle error
        }
    }
}
```

### Token Issuance (Modular Approach)

The recommended way to handle token issuance is by importing and inheriting the `EsdtModule` from the framework (`multiversx-sc-modules`). This module provides a unified `issue_token` method that can be used to issue any type of token on MultiversX (Fungible, NonFungible, SemiFungible, Meta, Dynamic).

```rust
#[multiversx_sc::contract]
pub trait MyContract: multiversx_sc_modules::esdt::EsdtModule {

    // Note: Only Fungible and Meta tokens have decimals
    // Example: Issuing a Fungible Token
    #[payable("EGLD")]
    #[endpoint(issueFungible)]
    fn issue_fungible(
        &self,
        token_display_name: ManagedBuffer,
        token_ticker: ManagedBuffer,
        num_decimals: usize,
    ) {
        // Calls the inherited issue_token method from EsdtModule
        self.issue_token(
            token_display_name,
            token_ticker,
            EsdtTokenType::Fungible,
            OptionalValue::Some(num_decimals),
        );
    }

    // Example: Issuing an NFT
    #[payable("EGLD")]
    #[endpoint(issueNft)]
    fn issue_nft(
        &self,
        token_display_name: ManagedBuffer,
        token_ticker: ManagedBuffer,
    ) {
        self.issue_token(
            token_display_name,
            token_ticker,
            EsdtTokenType::NonFungible,
            OptionalValue::None,
        );
    }
}
```

### Token Minting

Similarly, the `EsdtModule` provides a `mint` method to create new units of a token that has already been issued by the contract.

```rust
#[multiversx_sc::contract]
pub trait MyContract: multiversx_sc_modules::esdt::EsdtModule {

    #[endpoint(mintTokens)]
    fn mint_tokens(&self, amount: BigUint) {
        // Mints tokens using the inherited mint method from EsdtModule.
        // The token_id is managed by the module's storage.
        // For fungible tokens, the nonce is 0.
        self.mint(0, &amount);
    }
}
```

## Code Examples

### Crowdfunding Contract Pattern

```rust
#![no_std]

use multiversx_sc::imports::*;

#[multiversx_sc::contract]
pub trait Crowdfunding {
    #[init]
    fn init(&self, target: BigUint, deadline: u64, token_id: EgldOrEsdtTokenIdentifier) {
        self.target().set(target);
        self.deadline().set(deadline);
        self.token_identifier().set(token_id);
    }

    #[payable("*")]
    #[endpoint]
    fn fund(&self) {
        require!(
            self.blockchain().get_block_timestamp() < self.deadline().get(),
            "Funding period ended"
        );

        let payment = self.call_value().egld_or_single_esdt();
        require!(
            payment.token_identifier == self.token_identifier().get(),
            "Wrong token"
        );

        let caller = self.blockchain().get_caller();
        self.deposit(&caller).update(|deposit| *deposit += payment.amount);
    }

    #[endpoint]
    fn claim(&self) {
        require!(
            self.blockchain().get_block_timestamp() >= self.deadline().get(),
            "Funding period not ended"
        );

        let caller = self.blockchain().get_caller();
        let deposit = self.deposit(&caller).get();

        if self.get_current_funds() >= self.target().get() {
            // Target reached - owner claims
            require!(caller == self.blockchain().get_owner_address(), "Not owner");
            // Transfer funds to owner...
        } else {
            // Target not reached - refund depositors
            require!(deposit > 0, "No deposit");
            self.deposit(&caller).clear();
            self.send_tokens(&caller, &deposit);
        }
    }

    fn send_tokens(&self, to: &ManagedAddress, amount: &BigUint) {
        let token_id = self.token_identifier().get();
        self.tx()
            .to(to)
            .egld_or_single_esdt(&token_id, 0, amount)
            .transfer();
    }

    #[view(getCurrentFunds)]
    fn get_current_funds(&self) -> BigUint {
        let token_id = self.token_identifier().get();
        self.blockchain().get_sc_balance(&token_id, 0)
    }

    #[storage_mapper("target")]
    fn target(&self) -> SingleValueMapper<BigUint>;

    #[storage_mapper("deadline")]
    fn deadline(&self) -> SingleValueMapper<u64>;

    #[storage_mapper("tokenIdentifier")]
    fn token_identifier(&self) -> SingleValueMapper<EgldOrEsdtTokenIdentifier>;

    #[storage_mapper("deposit")]
    fn deposit(&self, donor: &ManagedAddress) -> SingleValueMapper<BigUint>;
}
```

## Critical Knowledge

### WRONG: Using MapMapper when not iterating

```rust
// WRONG - MapMapper is expensive (4*N + 1 storage entries)
#[storage_mapper("balances")]
fn balances(&self) -> MapMapper<ManagedAddress, BigUint>;
```

### CORRECT: Use SingleValueMapper with address key

```rust
// CORRECT - Efficient when you don't need to iterate
#[storage_mapper("balance")]
fn balance(&self, user: &ManagedAddress) -> SingleValueMapper<BigUint>;
```

### WRONG: Large modules and functions

```rust
// WRONG - Everything in one file
#[multiversx_sc::contract]
pub trait MyContract {
    // 500+ lines of code...
}
```

### CORRECT: Split into modules

```rust
// CORRECT - Organized modules
mod storage;
mod logic;
mod events;

#[multiversx_sc::contract]
pub trait MyContract:
    storage::StorageModule +
    logic::LogicModule +
    events::EventsModule
{
    #[init]
    fn init(&self) { }
}
```

### WRONG: Duplicated error messages

```rust
// WRONG - Duplicated strings increase contract size
require!(amount > 0, "Amount must be positive");
require!(other_amount > 0, "Amount must be positive");
```

### CORRECT: Static error messages

```rust
// CORRECT - Single definition
const ERR_AMOUNT_POSITIVE: &str = "Amount must be positive";

require!(amount > 0, ERR_AMOUNT_POSITIVE);
require!(other_amount > 0, ERR_AMOUNT_POSITIVE);
```

### WRONG: Trying to send EGLD + ESDT together

```rust
// WRONG - Impossible on MultiversX
self.tx()
    .to(&recipient)
    .egld(&egld_amount)
    .single_esdt(&token, 0, &esdt_amount) // Cannot combine!
    .transfer();
```

### CORRECT: Separate transactions

```rust
// CORRECT - Separate transfers
self.tx().to(&recipient).egld(&egld_amount).transfer();
self.tx().to(&recipient).single_esdt(&token, 0, &esdt_amount).transfer();
```

## Documentation Links

Always consult official documentation:

- **Smart Contracts Overview**: https://docs.multiversx.com/developers/smart-contracts
- **sc-meta Tool**: https://docs.multiversx.com/developers/meta/sc-meta
- **Storage Mappers**: https://docs.multiversx.com/developers/developer-reference/storage-mappers
- **Annotations**: https://docs.multiversx.com/developers/developer-reference/sc-annotations
- **Payments**: https://docs.multiversx.com/developers/developer-reference/sc-payments
- **Example Contracts**: https://github.com/multiversx/mx-sdk-rs/tree/master/contracts/examples
- **Framework Repository**: https://github.com/multiversx/mx-sdk-rs

## Verification Checklist

Before completion, verify:

- [ ] Contract created with `sc-meta new --template <template> --name <name>`
- [ ] `#![no_std]` at top of lib.rs
- [ ] `#[multiversx_sc::contract]` on main trait
- [ ] `#[init]` function defined for deployment
- [ ] Storage mappers use appropriate types (avoid MapMapper unless iterating)
- [ ] Payment endpoints have `#[payable(...)]` annotation
- [ ] Error messages use `require!` macro
- [ ] Contract builds successfully with `sc-meta all build`
- [ ] Output files exist: `output/<name>.wasm` and `output/<name>.abi.json`
- [ ] Tests pass with `sc-meta test` (if tests exist)
- [ ] Deployment tested on devnet before mainnet
