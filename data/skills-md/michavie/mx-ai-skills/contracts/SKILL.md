---
name: contracts
description: Expert MultiversX Smart Contract Development (Rust). Use for writing, testing, optimizing, and auditing smart contracts.
---

# MultiversX Smart Contract Expert

This skill provides comprehensive capabilities for developing secure, gas-efficient smart contracts on MultiversX using Rust.

## Core Capabilities

1.  **Smart Contract Implementation**
    *   **Framework**: `multiversx-sc`
    *   **Standards**: ESDT (Tokens), SFT/NFTs, Digital ID
    *   **Patterns**: Data storage, Upgradability, Pausability

2.  **Testing & Verification**
    *   **Rust Scenario Tests**: Preferred method for end-to-end blockchain simulation using the `multiversx-sc-scenario` crate.
    *   **RustVM**: High-speed unit testing.
    *   **Property Testing**: Fuzzing for edge cases.

3.  **Security & Auditing**
    *   **Static Analysis**: Detecting common vulnerabilities.
    *   **Gas Optimization**: Efficient storage and execution.
    *   **Audit Readiness**: Code structure and best practices.

## 🛠️ Development Workflow

### 1. New Contract Setup
When creating a new contract, use `sc-meta` or `mxpy` templates.
*   **Structure**:
    ```text
    /meta          # Build tool (meta-crate) - manages code generation and ABI
    /src           # Source code - the contract logic trait
    /wasm          # WASM entry point - links the logic to the VM interface
    /tests         # Pure Rust tests (Unit & Scenario)
    /output        # GENERATED after build (.wasm, .abi.json, .mxsc.json)
    mxpy.json      # Python CLI configuration
    ```

### 2. Coding Standards (Critical)
*   **Arithmetic**: ALWAYS use `checked_add`, `checked_mul`, etc. NEVER use standard operators (`+`, `-`, `*`) on user input.
*   **Storage**:
    *   `SingleValueMapper`: Single items.
    *   `VecMapper`: Lists (careful with iteration).
    *   `UnorderedSetMapper`: O(1) checks.
    *   **Optimization**: Do not use `VecMapper` for large datasets; use `MapMapper` or `UnorderedSetMapper`.
*   **Naming**: Endpoints and views MUST use **camelCase**.
*   **Reentrancy**: Use `#[reentrancy_lock]` on potentially dangerous endpoints.
*   **Payment**: ALWAYS specify `#[payable("*")]` or `#[payable("EGLD")]` if expecting tokens.

### 3. Testing
*   **Rust Scenarios**: Use Rust-based tests (`multiversx-sc-scenario`) instead of legacy JSON Mandos tests.
*   **RustVM**: Use `multiversx_sc_scenario::imports::*` for unit tests in `src/lib.rs` or `tests/`.

## 📚 Expert Resources (Deep Dive)

For specialized tasks, referencing these expert modules:
*   **Security Audit Guidelines**: `skills/expert/mvx_dapp_audit/SKILL.md`
*   **Gas Optimization**: `skills/expert/mvx_sc_best_practices/SKILL.md`
*   **Testing Handbook**: `skills/expert/mvx_testing_handbook/SKILL.md`
*   **Sharp Edges/Gotchas**: `skills/expert/mvx_sharp_edges/SKILL.md`
*   **Static Analysis**: `skills/expert/mvx_static_analysis/SKILL.md`

## ⚡ Common Operations

### Token Transfers
```rust
self.send().direct_esdt(&to, &token_id, 0, &amount);
```

### Storage Mapping
```rust
#[view(getMyValue)]
#[storage_mapper("myValue")]
fn my_value(&self) -> SingleValueMapper<BigUint>;
```

### Event Logs
```rust
#[event("deposit")]
fn deposit_event(&self, #[indexed] user: &ManagedAddress, amount: &BigUint);
```


# Smart Contracts Base

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
└── tests/               # Rust-based tests (Unit & Scenarios)
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

    #[endpoint(add)]
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
#[endpoint(depositEgld)]
fn deposit_egld(&self) {
    let payment = self.call_value().egld_value();
    let amount = payment.clone_value();
    // process payment...
}
```

### Receiving Any Single Token

```rust
#[payable("*")]
#[endpoint(deposit)]
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
#[endpoint(flexibleDeposit)]
fn flexible_deposit(&self) {
    let payment = self.call_value().egld_or_single_esdt();
    // Returns EgldOrEsdtTokenPayment
}
```

### Receiving Multiple Tokens

```rust
#[payable("*")]
#[endpoint(multiDeposit)]
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
#[endpoint(withdraw)]
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
After building, find outputs in the `output/` folder.
*   **`.wasm`**: The binary deployed to the blockchain.
*   **`.abi.json`**: Interface definition for frontends and interaction tools.
*   **`.mxsc.json`**: Metadata used by the Rust scenario framework to locate the contract.
*   **`.imports.json`**: (Generated) lists dependencies for the VM.

> [!TIP]
> **First Build**: The first `sc-meta all build` will download a specific Rust toolchain and perform a full compile. This can take several minutes. Subsequent builds are incremental and much faster.

## Contract Lifecycle

### 1. Creation
Always start from a template to ensure the cargo workspace is correctly linked:
```bash
sc-meta new --template empty --name my-contract
```

### 2. Deployment
Deployment installs the code at a new address and runs `#[init]`.
```bash
mxpy contract deploy \
    --bytecode output/my-contract.wasm \
    --proxy https://devnet-api.multiversx.com --chain D \
    --pem wallet.pem --gas-limit 60000000 \
    --arguments 1000 "hex:0011" \
    --send
```

### 3. Upgrading
Upgrading replaces the binary but **preserves all storage**.
*   **Storage Reuse**: The new contract must use the same storage keys (`#[storage_mapper("key")]`) to access existing data.
*   **Init is NOT called**: Upgrades trigger the `#[upgrade]` function, NOT `#[init]`.

```rust
#[upgrade]
fn upgrade(&self, new_param: Option<BigUint>) {
    if let Some(val) = new_param {
        self.config_val().set(val);
    }
}
```

```bash
mxpy contract upgrade <ADDRESS> \
    --bytecode output/my-contract.wasm \
    --proxy https://devnet-api.multiversx.com --chain D \
    --pem wallet.pem --gas-limit 60000000 \
    --send
```

## Testing Lifecycle (Deployment Tests)
Don't just test endpoints; test the deployment flow in Rust:

```rust
#[test]
fn test_lifecycle() {
    let mut world = ScenarioWorld::new();
    world.register_contract("mxsc:output/my-contract.mxsc.json", MyContract::ContractBuilder);

    // Deploy
    world.tx()
        .from("address:owner")
        .typed(my_contract_proxy::MyContractProxy)
        .init(initial_value)
        .code("file:output/my-contract.wasm")
        .new_address("address:contract")
        .run();

    // Call
    world.tx()
        .from("address:user")
        .to("address:contract")
        .typed(my_contract_proxy::MyContractProxy)
        .my_endpoint(param)
        .run();
}
```

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
    // world.run("scenarios/deploy.scen.json"); // Legacy JSON format

    // Preferred: Pure Rust-based scenario
    world.sc_deploy()
        .from("address:owner")
        .code("file:output/my-contract.wasm")
        .expect(ExpectStatus::ok());
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
    #[endpoint(fund)]
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

    #[endpoint(claim)]
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


# SC Best Practices

---
name: mvx_sc_best_practices
description: Expert guidelines for developing, auditing, and optimizing MultiversX Smart Contracts (Rust).
---

# MultiversX Smart Contract Best Practices

This skill provides expert-level guidance on writing secure, gas-efficient, and idiomatic Smart Contracts on MultiversX using the `multiversx-sc` framework.

## 1. Storage Optimization (Critical)
Storage is the most expensive resource.

- **`SingleValueMapper`**: Use for individual items (flags, configs, IDs).
    - *Gas*: Cheapest (~1 slot write).
    - *Pattern*: `#[storage_mapper("myValue")] fn my_value(&self) -> SingleValueMapper<MyType>;`
- **`VecMapper`**: Use for ordered lists where you need index access.
    - *Warning*: **NEVER iterate** a `VecMapper` on-chain if it can grow indefinitely. This is a DoS vector (Gas Loop).
    - *Gas*: Medium.
- **`UnorderedSetMapper`**: Use for unique collections or whitelists.
    - *Gas*: Checks existence before insert. Good for `O(1)` membership checks.
- **`MapMapper`**: **AVOID** unless strictly necessary.
    - *Why*: It uses a linked-list structure (4 storage writes per entry). It is ~4x more expensive than `SingleValueMapper`.
    - *Alternative*: If you don't need to iterate keys, use a `SingleValueMapper` keyed by a hash or composite key.

## 2. Security Patterns

### Arithmetic Safety
- **Always use `BigUint`** for tokens, prices, and financial math.
    - *Why*: Prevents overflow/underflow and matches the VM's native big int implementation.
- Avoid `u64`/`u32` for money. Only use them for loop counters or small IDs.

### Reentrancy Protection
- **Checks-Effects-Interactions**:
    1.  **Checks**: Validate inputs (`require!`).
    2.  **Effects**: Update storage (deduct balance, update state).
    3.  **Interactions**: Send tokens or call other contracts.
- **Async Calls**: MultiversX async calls are safer than synchronous calls regarding reentrancy of the *same* execution context, but state changes happen in a separate transaction (callback).
- **Callback Verification**: Always validate the state in the `#[callback]` function. Do not assume the async call succeeded just because it was sent.

### Access Control
- Use `#[only_owner]` for admin functions.
- For fine-grained control, use the `only_admin` module from the `multiversx-sc-modules` crate. It provides a standard implementation for managing multiple admins.

## 3. Data Flow & Testing

### Transfer-Execute Pattern
- When sending tokens to a contract, prefer **`MultiESDTNFTTransfer`** (built-in function) over 2 transactions (Approve + TransferFrom).
- In the contract, use `#[payable("*")]` to accept tokens and `self.call_value().all_esdt_transfers()` to inspect them.

### Testing (Mandos/Scenarios)
- **Mandos (`.scen.json`)** are mandatory for integration testing.
- Cover all pathways:
    - Happy path.
    - Error path (expect status `4`).
- **Whitebox Testing**: Use `#[cfg(test)]` modules with `multiversx_sc_scenario::imports::*` to test internal functions without deploying.

## 4. Code Structure
- **Endpoints**: Public functions `#[endpoint]`.
- **Views**: Read-only `#[view]`.
- **Private**: Helper functions (no annotation, or pure Rust).
- **Events**: `#[event]` for indexing, but don't store critical data solely in events.

## 5. Common Pitfalls / "Sharp Edges"
- **Token Identifier Validation**: Always validate `token_id`. Don't assume the user sent the correct token.
- **Gas Limit**: Be aware of the block gas limit (1.5B gas). Large loops will revert.
- **Managed Types**: Use `ManagedBuffer`, `ManagedAddress`, `ManagedVec` instead of standard Rust `Vec`, `String` to avoid serialization overhead.


# Audit Context

---
name: multiversx-audit-context
description: Build mental models of MultiversX codebases before security auditing. Use when starting a new audit, onboarding to unfamiliar code, or mapping system architecture for vulnerability research.
---

# Audit Context Building

Rapidly build a comprehensive mental model of a MultiversX codebase before diving into vulnerability hunting. This skill ensures you understand the system holistically before searching for specific issues.

## When to Use

- Starting a new security audit engagement
- Onboarding to an unfamiliar MultiversX project
- Mapping attack surface for penetration testing
- Preparing for code review sessions

## 1. Reconnaissance

### Identify the Core
Locate where critical logic and value flows reside:

- **Smart Contracts**: Look for `#[multiversx_sc::contract]`, `#[payable("*")]`, and `impl` blocks
- **Value Handlers**: Functions that move EGLD/ESDT tokens
- **Access Control**: Owner-only functions, whitelists, role systems

### Identify Externalities
Map external dependencies and interactions:

- **Cross-Contract Calls**: Which other contracts does this interact with?
- **Hardcoded Addresses**: Look for `sc:` smart contract literals
- **Oracle Dependencies**: External data sources the contract relies on
- **Bridge Contracts**: Any cross-chain or cross-shard communication

### Identify Documentation
Gather all available context:

- **Standard Files**: `README.md`, `specs/`, `whitepaper.pdf`
- **MultiversX Specific**: `mxpy.json` (build config), `multiversx.yaml`, `snippets.sh`
- **Test Scenarios**: `scenarios/` directory with Mandos tests

## 2. System Mapping

Create a structured map of the system architecture:

### Roles and Permissions
| Role | Capabilities | How Assigned |
|------|-------------|--------------|
| Owner | Full admin access | Deploy-time, transferable |
| Admin | Limited admin functions | Owner grants |
| User | Public endpoints | Anyone |
| Whitelisted | Special access | Admin grants |

### Asset Inventory
| Asset Type | Examples | Risk Level |
|------------|----------|------------|
| EGLD | Native currency | Critical |
| Fungible ESDT | Custom tokens | High |
| NFT/SFT | Non-fungible tokens | Medium-High |
| Meta-ESDT | Tokens with metadata | Medium-High |

### State Analysis
Document all storage mappers and their purposes:

```rust
// Example state inventory
#[storage_mapper("owner")]           // SingleValueMapper - access control
#[storage_mapper("balances")]        // MapMapper - user funds (CRITICAL)
#[storage_mapper("whitelist")]       // SetMapper - privileged users
```

## 3. Threat Modeling (Initial)

### Asset at Risk Analysis
- **Direct Loss**: What funds can be stolen if the contract fails?
- **Indirect Loss**: What downstream systems depend on this contract?
- **Reputation Loss**: What non-financial damage could occur?

### Attacker Profiles
| Attacker | Motivation | Capabilities |
|----------|------------|--------------|
| External User | Profit | Public endpoints only |
| Malicious Admin | Insider threat | Admin functions |
| Reentrant Contract | Exploit callbacks | Cross-contract calls |
| Front-runner | MEV extraction | Transaction ordering |

### Entry Point Enumeration
List all `#[endpoint]` functions with their risk classification:

```
HIGH RISK:
- deposit() - #[payable("*")] - accepts value
- withdraw() - moves funds out
- upgrade() - can change contract logic

MEDIUM RISK:
- setConfig() - owner only, changes behavior
- addWhitelist() - expands permissions

LOW RISK:
- getBalance() - #[view] - read only
```

## 4. Environment Check

### Dependency Audit
- **Framework Version**: Check `Cargo.toml` for `multiversx-sc` version
- **Known Vulnerabilities**: Compare against security advisories
- **Deprecated APIs**: Look for usage of deprecated functions

### Test Suite Assessment
- **Coverage**: Does `scenarios/` exist with comprehensive tests?
- **Edge Cases**: Are failure paths tested?
- **Freshness**: Run `sc-meta test-gen` to verify tests match current code

### Build Configuration
- **Optimization Level**: Check for debug vs release builds
- **WASM Size**: Large binaries may indicate bloat or complexity

## 5. Output Deliverable

After completing context building, document:

1. **System Overview**: One-paragraph summary of what the contract does
2. **Trust Boundaries**: Who trusts whom, what assumptions exist
3. **Critical Paths**: The most security-sensitive code paths
4. **Initial Concerns**: Preliminary list of areas requiring deep review
5. **Questions for Team**: Clarifications needed from developers

## Checklist

Before proceeding to detailed audit:

- [ ] All entry points identified and classified
- [ ] Storage layout documented
- [ ] External dependencies mapped
- [ ] Role/permission model understood
- [ ] Test coverage assessed
- [ ] Framework version noted
- [ ] Initial threat model drafted


# Audit Context (Legacy)

---
name: audit_context
description: Guidelines for establishing context before an audit.
---

# Audit Context Building

This skill helps you rapidly build a mental model of a codebase before diving into vulnerability hunting.

## 1. Reconnaissance
- **Identify the Core**: Where is the money / critical logic?
    - *MultiversX*: Look for `#[multiversx_sc::contract]`, `#[payable("*")]`, and `impl` blocks.
- **Identify Externalities**:
    - Which other contracts does this interact with?
    - Are there hardcoded addresses? (e.g., `sc:` smart contract literals).
- **Identify Documentation**:
    - `README.md`, `specs/`, `whitepaper.pdf`.
    - *MultiversX*: `mxpy.json` (build config), `multiversx.yaml`, `snippets.sh`.

## 2. System Mapping
Create a mental (or written) map of the system.
- **Roles**: Who can do what? (`Owner`, `Admin`, `User`, `Whitelisted`).
- **Assets**: What tokens are flowing? (EGLD, ESDT, NFT, SFT).
- **State**: What is stored? (`SingleValueMapper`, `VecMapper`).

## 3. Threat Modeling (Initial)
- **Asset at Risk**: If this contract fails, what is lost?
- **Attacker Profile**: External user? Malicious admin? Reentrant contract?
- **Entry Points**: List all `#[endpoint]` functions. Which ones are unchecked?

## 4. Environment Check
- **Language Version**: Is `cargo.toml` using a recent `multiversx-sc` version?
- **Test Suite**: Does `scenarios/` exist? Run `sc-meta test-gen` to see if tests are up to date.


# Entry Points

---
name: multiversx-entry-points
description: Systematically identify and analyze all smart contract entry points for attack surface mapping. Use when starting security reviews, documenting contract interfaces, or assessing access control coverage.
---

# MultiversX Entry Point Analyzer

Identify the complete attack surface of a MultiversX smart contract by enumerating all public interaction points and classifying their risk levels. This is typically the first step in any security review.

## When to Use

- Starting a new security audit
- Documenting contract public interface
- Assessing access control coverage
- Mapping data flow through the contract
- Identifying high-risk endpoints for focused review

## 1. Entry Point Identification

### MultiversX Macros That Expose Functions

| Macro | Visibility | Risk Level | Description |
|-------|-----------|------------|-------------|
| `#[endpoint]` | Public write | High | State-changing public function |
| `#[view]` | Public read | Low | Read-only public function |
| `#[payable("*")]` | Accepts any token | Critical | Handles value transfers |
| `#[payable("EGLD")]` | Accepts EGLD only | Critical | Handles native currency |
| `#[init]` | Deploy only | Medium | Constructor (runs once) |
| `#[upgrade]` | Upgrade only | Critical | Migration logic |
| `#[callback]` | Internal | High | Async call response handler |
| `#[only_owner]` | Owner restricted | Medium | Admin functions |

### Scanning Commands
```bash
# Find all endpoints
grep -n "#\[endpoint" src/*.rs

# Find all payable endpoints
grep -n "#\[payable" src/*.rs

# Find all views
grep -n "#\[view" src/*.rs

# Find callbacks
grep -n "#\[callback" src/*.rs

# Find init and upgrade
grep -n "#\[init\]\|#\[upgrade\]" src/*.rs
```

## 2. Risk Classification

### Category A: Payable Endpoints (Critical Risk)

Functions receiving value require the most scrutiny.

```rust
#[payable("*")]
#[endpoint]
fn deposit(&self) {
    // MUST CHECK:
    // 1. Token identifier validation
    // 2. Amount > 0 validation
    // 3. Correct handling of multi-token transfers
    // 4. State updates before external calls

    let payment = self.call_value().single_esdt();
    require!(
        payment.token_identifier == self.accepted_token().get(),
        "Wrong token"
    );
    require!(payment.amount > 0, "Zero amount");

    // Process deposit...
}
```

**Checklist for Payable Endpoints:**
- [ ] Token ID validated against expected token(s)
- [ ] Amount checked for minimum/maximum bounds
- [ ] Multi-transfer handling if `all_esdt_transfers()` used
- [ ] Nonce validation for NFT/SFT
- [ ] Reentrancy protection (Checks-Effects-Interactions)

### Category B: Non-Payable State-Changing Endpoints (High Risk)

Functions that modify state without payment.

```rust
#[endpoint]
fn update_config(&self, new_value: BigUint) {
    // MUST CHECK:
    // 1. Who can call this? (access control)
    // 2. Input validation
    // 3. State transition validity

    self.require_caller_is_admin();
    require!(new_value > 0, "Invalid value");
    self.config().set(new_value);
}
```

**Checklist for State-Changing Endpoints:**
- [ ] Access control implemented and correct
- [ ] Input validation for all parameters
- [ ] State transitions are valid
- [ ] Events emitted for important changes
- [ ] No DoS vectors (unbounded loops, etc.)

### Category C: View Functions (Low Risk)

Read-only functions, but still need review.

```rust
#[view(getBalance)]
fn get_balance(&self, user: ManagedAddress) -> BigUint {
    // SHOULD CHECK:
    // 1. Does it actually modify state? (interior mutability)
    // 2. Does it leak sensitive information?
    // 3. Is the calculation expensive (DoS via gas)?

    self.balances(&user).get()
}
```

**Checklist for View Functions:**
- [ ] No state modification (verify no storage writes)
- [ ] No sensitive data exposure
- [ ] Bounded computation (no unbounded loops)
- [ ] Block info usage appropriate (`get_block_timestamp()` may differ off-chain)

### Category D: Init and Upgrade (Critical Risk)

Lifecycle functions with special considerations.

```rust
#[init]
fn init(&self, admin: ManagedAddress) {
    // MUST CHECK:
    // 1. All required state initialized
    // 2. No way to re-initialize
    // 3. Admin/owner properly set

    self.admin().set(admin);
}

#[upgrade]
fn upgrade(&self) {
    // MUST CHECK:
    // 1. New storage mappers initialized
    // 2. Storage layout compatibility
    // 3. Migration logic correct
}
```

### Category E: Callbacks (High Risk)

Async call handlers with specific vulnerabilities.

```rust
#[callback]
fn transfer_callback(
    &self,
    #[call_result] result: ManagedAsyncCallResult<()>
) {
    // MUST CHECK:
    // 1. Error handling (don't assume success)
    // 2. State reversion on failure
    // 3. Correct identification of original call

    match result {
        ManagedAsyncCallResult::Ok(_) => {
            // Success path
        },
        ManagedAsyncCallResult::Err(_) => {
            // CRITICAL: Must handle failure!
            // Revert any state changes from original call
        }
    }
}
```

## 3. Analysis Workflow

### Step 1: List All Entry Points

Create an inventory table:

```markdown
| Endpoint | Type | Payable | Access | Storage Touched | Risk |
|----------|------|---------|--------|-----------------|------|
| deposit | endpoint | * | Public | balances | Critical |
| withdraw | endpoint | No | Public | balances | Critical |
| setAdmin | endpoint | No | Owner | admin | High |
| getBalance | view | No | Public | balances (read) | Low |
| init | init | No | Deploy | admin, config | Medium |
```

### Step 2: Tag Access Control

For each endpoint, document who can call it:

```rust
// Public - anyone can call
#[endpoint]
fn public_function(&self) { }

// Owner only - blockchain owner
#[only_owner]
#[endpoint]
fn owner_function(&self) { }

// Admin only - custom access control
#[endpoint]
fn admin_function(&self) {
    self.require_caller_is_admin();
}

// Whitelisted - address in set
#[endpoint]
fn whitelist_function(&self) {
    let caller = self.blockchain().get_caller();
    require!(self.whitelist().contains(&caller), "Not whitelisted");
}
```

### Step 3: Tag Value Handling

Classify how each endpoint handles value:

| Tag | Meaning | Example |
|-----|---------|---------|
| Refusable | Rejects payments | Default (no `#[payable]`) |
| EGLD Only | Accepts EGLD | `#[payable("EGLD")]` |
| Token Only | Specific ESDT | `#[payable("TOKEN-abc123")]` |
| Any Token | Any payment | `#[payable("*")]` |
| Multi-Token | Multiple payments | Uses `all_esdt_transfers()` |

### Step 4: Graph Data Flow

Map which storage mappers each endpoint reads/writes:

```
deposit() ──writes──▶ balances
          ──writes──▶ total_deposited
          ──reads───▶ accepted_token

withdraw() ──reads/writes──▶ balances
           ──reads────────▶ withdrawal_fee

getBalance() ──reads──▶ balances
```

## 4. Specific Attack Vectors

### Privilege Escalation
Is a sensitive endpoint accidentally public?

```rust
// VULNERABLE: Missing access control
#[endpoint]
fn set_admin(&self, new_admin: ManagedAddress) {
    self.admin().set(new_admin);  // Anyone can become admin!
}

// CORRECT: Protected
#[only_owner]
#[endpoint]
fn set_admin(&self, new_admin: ManagedAddress) {
    self.admin().set(new_admin);
}
```

### DoS via Unbounded Growth
Can public endpoints cause unbounded storage growth?

```rust
// VULNERABLE: Public endpoint adds to unbounded set
#[endpoint]
fn register(&self) {
    let caller = self.blockchain().get_caller();
    self.participants().insert(caller);  // Grows forever!
}

// Attack: Call register() with many addresses until
// any function iterating participants() runs out of gas
```

### Missing Payment Validation
Does a payable endpoint verify what it receives?

```rust
// VULNERABLE: Accepts any token
#[payable("*")]
#[endpoint]
fn stake(&self) {
    let payment = self.call_value().single_esdt();
    self.staked().update(|s| *s += payment.amount);  // Fake tokens accepted!
}
```

### Callback State Assumptions
Does a callback assume the async call succeeded?

```rust
// VULNERABLE: Assumes success
#[callback]
fn on_transfer_complete(&self) {
    // This runs even if transfer FAILED!
    self.transfer_count().update(|c| *c += 1);
}
```

## 5. Output Template

```markdown
# Entry Point Analysis: [Contract Name]

## Summary
- Total Endpoints: X
- Payable Endpoints: Y (Critical)
- State-Changing: Z (High)
- Views: W (Low)

## Detailed Inventory

### Critical Risk (Payable)
| Endpoint | Accepts | Access | Concerns |
|----------|---------|--------|----------|
| deposit | * | Public | Token validation needed |

### High Risk (State-Changing)
| Endpoint | Access | Storage Modified | Concerns |
|----------|--------|------------------|----------|
| withdraw | Public | balances | Amount validation |

### Medium Risk (Admin)
| Endpoint | Access | Storage Modified | Concerns |
|----------|--------|------------------|----------|
| setConfig | Owner | config | Privilege escalation if misconfigured |

### Low Risk (Views)
| Endpoint | Storage Read | Concerns |
|----------|--------------|----------|
| getBalance | balances | None |

## Access Control Matrix

| Endpoint | Public | Owner | Admin | Whitelist |
|----------|--------|-------|-------|-----------|
| deposit | Yes | - | - | - |
| setAdmin | - | Yes | - | - |

## Recommended Focus Areas
1. [Highest priority endpoint and why]
2. [Second priority]
3. [Third priority]
```


# Entry Points (Expert)

---
name: mvx_entry_points
description: Identify and analyze MultiversX Smart Contract entry points (#[endpoint], #[view], #[payable]).
---

# MultiversX Entry Point Analyzer

This skill helps you identify the attack surface of a smart contract by enumerating all public interaction points.

## 1. Identification
Scan for `multiversx_sc` macros that expose functions:
- **`#[endpoint]`**: Public write function. **High Risk**.
- **`#[view]`**: Public read function. Low risk (unless used on-chain).
- **`#[payable("*")]`**: Accepts EGLD/ESDT. **Critical Risk** (value handling).
- **`#[init]`**: Constructor.
- **`#[upgrade]`**: Upgrade handler. **Critical Risk** (migration logic).

## 2. Risk Classification

### A. Non-Payable Endpoints
Functions that change state but don't accept value.
- *Check*: Is there `require!`? Who can call this (Owner only?)?
- *Risk*: Unauthorized state change.

### B. Payable Endpoints (`#[payable("*")]`)
Functions receiving money.
- *Check*:
    - Does it use `self.call_value().all_esdt_transfers()`?
    - Is `amount > 0` checked?
    - Are token IDs validated?
- *Risk*: Stealing funds, accepted fake tokens.

### C. Views
- *Check*: Does it modify state? (It shouldn't, but Rust allows interior mutability or misuse).

## 3. Analysis Workflow
1.  **List all Entry Points**.
2.  **Tag Access Control**: `OnlyOwner`, `Whitelisted`, `Public`.
3.  **Tag Value handling**: `Refusable`, `Payable`.
4.  **Graph Data Flow**: Which storage mappers do they touch?

## 4. Specific Attacks
- **Privilege Escalation**: Is a sensitive endpoint accidentally public?
- **DoS**: public endpoint inserting into UnorderedSetMapper (unbounded growth).


# Static Analysis

---
name: multiversx-static-analysis
description: Manual and automated static analysis patterns for finding vulnerabilities in MultiversX Rust and Go code. Use when performing security reviews, setting up code scanning, or creating analysis checklists.
---

# MultiversX Static Analysis

Comprehensive static analysis guide for MultiversX codebases, covering both Rust smart contracts (`multiversx-sc`) and Go protocol code (`mx-chain-go`). This skill provides grep patterns, manual review techniques, and tool recommendations.

## When to Use

- Starting security code reviews
- Setting up automated vulnerability scanning
- Creating analysis checklists for audits
- Training new security reviewers
- Investigating specific vulnerability classes

## 1. Rust Smart Contracts (`multiversx-sc`)

### Critical Grep Patterns

#### Unsafe Code
```bash
# Unsafe blocks - valid only for FFI or specific optimizations
grep -rn "unsafe" src/

# Generally forbidden in smart contracts unless justified
```
**Risk**: Memory corruption, undefined behavior
**Action**: Require justification for each `unsafe` block

#### Panic Inducers
```bash
# Direct unwrap - can panic
grep -rn "\.unwrap()" src/

# Expect - also panics
grep -rn "\.expect(" src/

# Index access - can panic on out of bounds
grep -rn "\[.*\]" src/ | grep -v "storage_mapper"
```
**Risk**: Contract halts, potential DoS
**Action**: Replace with `unwrap_or_else(|| sc_panic!(...))` or proper error handling

#### Floating Point Arithmetic
```bash
# f32 type
grep -rn "f32" src/

# f64 type
grep -rn "f64" src/

# Float casts
grep -rn "as f32\|as f64" src/
```
**Risk**: Non-deterministic behavior, consensus failure
**Action**: Use `BigUint`/`BigInt` for all calculations

#### Unchecked Arithmetic
```bash
# Direct arithmetic operators
grep -rn "[^_a-zA-Z]\+ [^_a-zA-Z]" src/  # Addition
grep -rn "[^_a-zA-Z]\- [^_a-zA-Z]" src/  # Subtraction
grep -rn "[^_a-zA-Z]\* [^_a-zA-Z]" src/  # Multiplication

# Without checked variants
grep -rn "checked_add\|checked_sub\|checked_mul" src/
```
**Risk**: Integer overflow/underflow
**Action**: Use `BigUint` or checked arithmetic for all financial calculations

#### Map Iteration (DoS Risk)
```bash
# Iterating storage mappers
grep -rn "\.iter()" src/

# Especially dangerous patterns
grep -rn "for.*in.*\.iter()" src/
grep -rn "\.collect()" src/
```
**Risk**: Gas exhaustion DoS
**Action**: Add pagination or bounds checking

### Logical Pattern Analysis (Manual Review)

#### Token ID Validation
Search for payment handling:
```bash
grep -rn "call_value()" src/
grep -rn "all_esdt_transfers" src/
grep -rn "single_esdt" src/
```

For each occurrence, verify:
- [ ] Token ID checked against expected value
- [ ] Token nonce validated (for NFT/SFT)
- [ ] Amount validated (non-zero, within bounds)

```rust
// VULNERABLE
#[payable("*")]
fn deposit(&self) {
    let payment = self.call_value().single_esdt();
    self.balances().update(|b| *b += payment.amount);
    // No token ID check! Accepts any token
}

// SECURE
#[payable("*")]
fn deposit(&self) {
    let payment = self.call_value().single_esdt();
    require!(
        payment.token_identifier == self.accepted_token().get(),
        "Wrong token"
    );
    require!(payment.amount > 0, "Zero amount");
    self.balances().update(|b| *b += payment.amount);
}
```

#### Callback State Assumptions
Search for callbacks:
```bash
grep -rn "#\[callback\]" src/
```

For each callback, verify:
- [ ] Does NOT assume async call succeeded
- [ ] Handles error case explicitly
- [ ] Reverts state changes on failure if needed

```rust
// VULNERABLE - assumes success
#[callback]
fn on_transfer(&self) {
    self.transfer_count().update(|c| *c += 1);
}

// SECURE - handles both cases
#[callback]
fn on_transfer(&self, #[call_result] result: ManagedAsyncCallResult<()>) {
    match result {
        ManagedAsyncCallResult::Ok(_) => {
            self.transfer_count().update(|c| *c += 1);
        },
        ManagedAsyncCallResult::Err(_) => {
            // Handle failure - funds returned automatically
        }
    }
}
```

#### Access Control
Search for endpoints:
```bash
grep -rn "#\[endpoint\]" src/
grep -rn "#\[only_owner\]" src/
```

For each endpoint, verify:
- [ ] Appropriate access control applied
- [ ] Sensitive operations restricted
- [ ] Admin functions documented

```rust
// VULNERABLE - public sensitive function
#[endpoint]
fn set_fee(&self, new_fee: BigUint) {
    self.fee().set(new_fee);
}

// SECURE - restricted
#[only_owner]
#[endpoint]
fn set_fee(&self, new_fee: BigUint) {
    self.fee().set(new_fee);
}
```

#### Reentrancy (CEI Pattern)
Search for external calls:
```bash
grep -rn "\.send()\." src/
grep -rn "\.tx()" src/
grep -rn "async_call" src/
```

Verify Checks-Effects-Interactions pattern:
- [ ] All checks (require!) before state changes
- [ ] State changes before external calls
- [ ] No state changes after external calls in same function

## 2. Go Protocol Code (`mx-chain-go`)

### Concurrency Issues

#### Goroutine Loop Variable Capture
```bash
grep -rn "go func" *.go
```

Check for loop variable capture bug:
```go
// VULNERABLE
for _, item := range items {
    go func() {
        process(item)  // item may have changed!
    }()
}

// SECURE
for _, item := range items {
    item := item  // Create local copy
    go func() {
        process(item)
    }()
}
```

#### Map Race Conditions
```bash
grep -rn "map\[" *.go | grep -v "sync.Map"
```

Verify maps accessed from goroutines are protected:
```go
// VULNERABLE
var balances = make(map[string]int)
// Accessed from multiple goroutines without mutex

// SECURE
var balances = sync.Map{}
// Or use mutex protection
```

### Determinism Issues

#### Map Iteration Order
```bash
grep -rn "for.*range.*map" *.go
```

Map iteration in Go is random. Never use for:
- Generating hashes
- Creating consensus data
- Any deterministic output

```go
// VULNERABLE - non-deterministic
func hashAccounts(accounts map[string]int) []byte {
    var data []byte
    for k, v := range accounts {  // Random order!
        data = append(data, []byte(k)...)
    }
    return hash(data)
}

// SECURE - sort keys first
func hashAccounts(accounts map[string]int) []byte {
    keys := make([]string, 0, len(accounts))
    for k := range accounts {
        keys = append(keys, k)
    }
    sort.Strings(keys)

    var data []byte
    for _, k := range keys {
        data = append(data, []byte(k)...)
    }
    return hash(data)
}
```

#### Time Functions
```bash
grep -rn "time.Now()" *.go
```

`time.Now()` is forbidden in block processing:
```go
// VULNERABLE
func processBlock(block *Block) {
    timestamp := time.Now().Unix()  // Non-deterministic!
}

// SECURE
func processBlock(block *Block) {
    timestamp := block.Header.TimeStamp  // Deterministic
}
```

## 3. Analysis Checklist

### Smart Contract Review Checklist

**Access Control**
- [ ] All endpoints have appropriate access restrictions
- [ ] Owner/admin functions use `#[only_owner]` or explicit checks
- [ ] No privilege escalation paths

**Payment Handling**
- [ ] Token IDs validated in all `#[payable]` endpoints
- [ ] Amounts validated (non-zero, bounds)
- [ ] NFT nonces validated where applicable

**Arithmetic**
- [ ] No raw arithmetic on u64/i64 with external inputs
- [ ] BigUint used for financial calculations
- [ ] No floating point

**State Management**
- [ ] Checks-Effects-Interactions pattern followed
- [ ] Callbacks handle failure cases
- [ ] Storage layout upgrade-safe

**Gas & DoS**
- [ ] No unbounded iterations
- [ ] Storage growth is bounded
- [ ] Pagination for large data sets

**Error Handling**
- [ ] No `unwrap()` without justification
- [ ] Meaningful error messages
- [ ] Consistent error handling patterns

### Protocol Review Checklist

**Concurrency**
- [ ] All shared state properly synchronized
- [ ] No goroutine loop variable capture bugs
- [ ] Channel usage is correct

**Determinism**
- [ ] No map iteration for consensus data
- [ ] No `time.Now()` in block processing
- [ ] No random number generation without deterministic seed

**Memory Safety**
- [ ] Bounds checking on slices
- [ ] No nil pointer dereferences
- [ ] Proper error handling

## 4. Automated Tools

### Semgrep Rules
See `multiversx-semgrep-creator` skill for custom rule creation.

### Clippy (Rust)
```bash
cargo clippy -- -D warnings

# Useful lints:
# - clippy::arithmetic_side_effects
# - clippy::indexing_slicing
# - clippy::unwrap_used
```

### Go Vet & Staticcheck
```bash
go vet ./...
staticcheck ./...

# Race detection
go build -race
```

## 5. Vulnerability Categories Quick Reference

| Category | Grep Pattern | Severity |
|----------|-------------|----------|
| Unsafe code | `unsafe` | Critical |
| Float arithmetic | `f32\|f64` | Critical |
| Panic inducers | `unwrap()\|expect(` | High |
| Unbounded iteration | `\.iter()` | High |
| Missing access control | `#[endpoint]` without `#[only_owner]` | High |
| Token validation | `call_value()` without require | High |
| Callback assumptions | `#[callback]` without error handling | Medium |
| Raw arithmetic | `+ \| - \| *` on u64 | Medium |


# Static Analysis (Expert)

---
name: mvx_static_analysis
description: Manual and automated static analysis patterns for Rust/Go (unsafe usage, unverified unwrap, float arithmetic).
---

# MultiversX Static Analysis

This skill guides you through static analysis of MultiversX codebases, focusing on patterns that often indicate vulnerabilities.

## 1. Rust Smart Contracts (`multiversx-sc`)

### Critical Grep Patterns
- **Unsafe Code**:
    - `grep -r "unsafe"`: Valid only for FFI or specific optimizations. Generally forbidden in SCs.
- **Panic Inducers**:
    - `grep -r "unwrap()"`: **High Risk**. Should be `sc_panic!` or `unwrap_or_else`.
    - `grep -r "expect("`: **High Risk**.
- **Floating Point**:
    - `grep -r "f32"` / `grep -r "f64"`: **Critical**. Floats are non-deterministic and forbidden in consensus.
- **Map Iteration**:
    - `grep -r "iter()"` on `MapMapper` or `VecMapper`: Potential Gas DoS.

### Logical Patterns (Manual Review)
- **Token ID Validation**:
    - Search for `call_value().all_esdt_transfers()`.
    - Verify: Is the `token_id` checked against a storage variable (e.g., `wanted_token_id`)?
- **Callback State**:
    - Search for `#[callback]`.
    - Verify: Does it assume the async call succeeded? (It shouldn't).

## 2. Go Protocol (`mx-chain-go`)

### Concurrency
- **Goroutines**: `grep -r "go func"`.
    - Check: Is the loop variable captured correctly? (Common Go pitfall).
- **Races**: `grep -r "map\\["` written in goroutines without Mutex.

### Determinism
- **Map Iteration**: Iterating over Go maps is non-deterministic.
    - *Rule*: Never iterate a map to produce a hash or consensus data.
- **Time**: `time.Now()` is forbidden in block processing. Use `header.TimeStamp`.

## 3. Semgrep Rule Creation
If a pattern is complex, create a Semgrep rule.

```yaml
rules:
  - id: mvx-float-arithmetic
    patterns:
      - pattern: $X + $Y
      - metavariable-type:
          metavariable: $X
          type: f64
    message: "Floating point arithmetic detected. Use BigUint."
    languages: [rust]
    severity: ERROR
```


# Constant Time

---
name: multiversx-constant-time
description: Verify cryptographic operations execute in constant time to prevent timing attacks. Use when auditing custom crypto implementations, secret comparisons, or security-sensitive algorithms in smart contracts.
---

# Constant Time Analysis

Verify that cryptographic secrets are handled in constant time to prevent timing attacks. This skill is essential when reviewing any code that processes sensitive data where execution time could leak information.

## When to Use

- Auditing custom cryptographic implementations
- Reviewing secret comparison logic (hashes, signatures, keys)
- Analyzing authentication or verification code
- Checking password/PIN handling
- Reviewing any code where timing could leak secrets

## 1. Understanding Timing Attacks

### The Threat Model
An attacker measures how long operations take to infer secret values:

```
Comparison: secret[i] == input[i]
- If mismatch at i=0: ~100ns (returns immediately)
- If mismatch at i=5: ~150ns (checked 5 bytes first)
- If all match: ~200ns (checked all bytes)

Attack: Try all values for byte 0, find fastest rejection = wrong guess
        Repeat for each byte position
```

### Why It Matters on MultiversX
- Gas metering can leak execution path information
- Cross-shard timing differences observable
- VM-level optimizations may vary execution time

## 2. Patterns to Avoid (Variable Time)

### Early Exit Comparisons
```rust
// VULNERABLE: Early exit leaks position of first mismatch
fn compare_secrets(secret: &[u8], input: &[u8]) -> bool {
    if secret.len() != input.len() {
        return false;  // Length leak!
    }
    for i in 0..secret.len() {
        if secret[i] != input[i] {
            return false;  // Position leak!
        }
    }
    true
}
```

### Short-Circuit Boolean Operators
```rust
// VULNERABLE: && and || short-circuit
fn verify_auth(token_valid: bool, signature_valid: bool) -> bool {
    token_valid && signature_valid  // If token_valid is false, signature not checked
}
```

### Conditional Branching on Secrets
```rust
// VULNERABLE: Different code paths based on secret value
fn process_key(key: &[u8]) {
    if key[0] == 0x00 {
        // Fast path
    } else {
        // Slow path with more operations
    }
}
```

### Data-Dependent Memory Access
```rust
// VULNERABLE: Cache timing based on secret value
fn lookup(secret_index: usize, table: &[u8]) -> u8 {
    table[secret_index]  // Cache hit/miss depends on secret_index
}
```

## 3. MultiversX-Safe Solutions

### Use VM Cryptographic Functions
**BEST PRACTICE**: Always prefer built-in VM crypto operations:

```rust
// CORRECT: Use VM-provided verification
fn verify_signature(&self, message: &ManagedBuffer, signature: &ManagedBuffer) -> bool {
    let signer = self.expected_signer().get();
    self.crypto().verify_ed25519(
        signer.as_managed_buffer(),
        message,
        signature
    )
}

// CORRECT: Use VM-provided hashing
fn hash_data(&self, data: &ManagedBuffer) -> ManagedBuffer {
    self.crypto().sha256(data)
}
```

### ManagedBuffer Comparison
The MultiversX VM's `ManagedBuffer` comparison is typically constant-time:

```rust
// CORRECT: ManagedBuffer == uses VM comparison
fn verify_hash(&self, input_hash: &ManagedBuffer) -> bool {
    let stored_hash = self.secret_hash().get();
    stored_hash == *input_hash  // VM handles comparison
}
```

### Manual Constant-Time Comparison (When Necessary)
If you must compare raw bytes:

```rust
// CORRECT: Constant-time byte comparison
fn constant_time_compare(a: &[u8], b: &[u8]) -> bool {
    if a.len() != b.len() {
        return false;
    }

    let mut result: u8 = 0;
    for i in 0..a.len() {
        result |= a[i] ^ b[i];  // Accumulate differences
    }
    result == 0  // Check all at once
}
```

### Using the `subtle` Crate
For Rust code that needs constant-time operations:

```rust
use subtle::ConstantTimeEq;

fn verify_secret(stored: &[u8; 32], provided: &[u8; 32]) -> bool {
    stored.ct_eq(provided).into()  // Constant-time comparison
}
```

**Note**: Verify `subtle` crate is compatible with `no_std` and WASM.

## 4. Verification Techniques

### Code Review Checklist
- [ ] No early returns based on secret comparisons
- [ ] No `&&` or `||` with secret-dependent operands
- [ ] No branching (`if`/`match`) on secret values
- [ ] No array indexing with secret indices
- [ ] VM crypto functions used where available

### Static Analysis Patterns
Search for potentially vulnerable patterns:

```bash
# Find early returns in comparison-like functions
grep -n "return false" src/*.rs | grep -i "compare\|verify\|check"

# Find short-circuit operators with sensitive names
grep -n "&&\|\\|\\|" src/*.rs | grep -i "secret\|key\|hash\|signature"

# Find conditional branches on common secret variable names
grep -n "if.*secret\|if.*key\|if.*hash" src/*.rs
```

### Gas Analysis
On MultiversX, gas consumption can indicate timing:

```rust
// Check if gas varies with input
#[view]
fn gas_test(&self, input: ManagedBuffer) -> u64 {
    let before = self.blockchain().get_gas_left();
    // ... operation to test ...
    let after = self.blockchain().get_gas_left();
    before - after
}
```

**Warning**: This is approximate. True constant-time requires VM-level guarantees.

## 5. Common Vulnerable Scenarios

### Authentication Token Verification
```rust
// VULNERABLE
fn verify_token(&self, token: &ManagedBuffer) -> bool {
    let valid_token = self.auth_token().get();
    for i in 0..token.len() {
        if token.load_byte(i) != valid_token.load_byte(i) {
            return false;  // Timing leak!
        }
    }
    true
}

// CORRECT
fn verify_token(&self, token: &ManagedBuffer) -> bool {
    let valid_token = self.auth_token().get();
    valid_token == *token  // ManagedBuffer equality
}
```

### HMAC Verification
```rust
// VULNERABLE: Using == on computed HMAC
fn verify_hmac(&self, message: &ManagedBuffer, provided_mac: &ManagedBuffer) -> bool {
    let computed_mac = self.compute_hmac(message);
    computed_mac == *provided_mac  // Potentially variable time!
}

// CORRECT: Use VM crypto or constant-time comparison
fn verify_hmac(&self, message: &ManagedBuffer, provided_mac: &ManagedBuffer) -> bool {
    let computed_mac = self.compute_hmac(message);
    self.constant_time_eq(&computed_mac, provided_mac)
}
```

### Password/PIN Comparison
```rust
// VULNERABLE
fn check_pin(&self, entered_pin: u32) -> bool {
    entered_pin == self.stored_pin().get()  // Comparison may short-circuit
}

// CORRECT: Always compare all bits
fn check_pin(&self, entered_pin: u32) -> bool {
    let stored = self.stored_pin().get();
    (entered_pin ^ stored) == 0  // XOR and check
}
```

## 6. Audit Report Template

```markdown
## Constant-Time Analysis

### Scope
Files reviewed: [list]
Crypto operations found: [count]

### Findings

| Location | Operation | Status | Notes |
|----------|-----------|--------|-------|
| lib.rs:45 | Hash comparison | Safe | Uses ManagedBuffer == |
| auth.rs:23 | Token verify | VULNERABLE | Early return pattern |
| crypto.rs:89 | Signature | Safe | Uses self.crypto() |

### Recommendations
1. [Specific fix for each vulnerable location]
```

## 7. Key Principles

1. **Prefer VM Functions**: `self.crypto().*` methods are optimized and likely constant-time
2. **Avoid DIY Crypto**: Custom implementations are rarely necessary and often wrong
3. **Assume Timing Leaks**: Any branching on secrets is a potential vulnerability
4. **Test with Gas**: Gas consumption can reveal timing variations
5. **Document Assumptions**: Note which operations you assume are constant-time


# Constant Time (Expert)

---
name: mvx_constant_time
description: Verifying constant-time operations in crypto implementations.
---

# MultiversX Constant Time Analysis

This skill helps you verify that cryptographic secrets are handled in constant time to prevent timing attacks.

## 1. When to Use
- **Custom Crypto**: If the contract implements Elliptic Curve math, ZK verification, or signatures manually (not using the API).
- **Comparison**: Checking secrets (e.g., comparing user-provided HASH against stored HASH).

## 2. Patterns to Avoid (Variable Time)
- **Early Exit**: `if byte[i] != other[i] { return false }`. This leaks the index of the first difference.
- **Short-circuiting**: `&&` or `||` on secrets.

## 3. MultiversX Solution
- **Managed Types**: Use `ManagedBuffer` comparison provided by the API (often constant time implementation in the VM).
- **Subtle crate**: Use `subtle::ConstantTimeEq` for manual `u8` slice comparisons.

## 4. Verification
- **Measurement**: Difficult on-chain due to Gas Metering. Gas usually leaks the execution trace roughly.
- **Rule**: Rely on the VM's crypto functions (`self.crypto().verify_signature(...)`) instead of implementing it in WASM.


# WASM Debug

---
name: multiversx-wasm-debug
description: Analyze compiled WASM binaries for size optimization, panic analysis, and debugging with DWARF symbols. Use when troubleshooting contract deployment issues, optimizing binary size, or debugging runtime errors.
---

# MultiversX WASM Debugging

Analyze compiled `output.wasm` files for size optimization, panic investigation, and source-level debugging. This skill helps troubleshoot deployment issues and runtime errors.

## When to Use

- Contract deployment fails due to size limits
- Investigating panic/trap errors at runtime
- Optimizing WASM binary size
- Understanding what's in your compiled contract
- Mapping WASM errors back to Rust source code

## 1. Binary Size Analysis

### Using Twiggy

Twiggy analyzes WASM binaries to identify what consumes space:

```bash
# Install twiggy
cargo install twiggy

# Top consumers of space
twiggy top output/my-contract.wasm

# Dominators analysis (what keeps what in the binary)
twiggy dominators output/my-contract.wasm

# Paths to specific functions
twiggy paths output/my-contract.wasm "function_name"

# Full call graph
twiggy callgraph output/my-contract.wasm > graph.dot
```

### Sample Twiggy Output
```
 Shallow Bytes │ Shallow % │ Item
───────────────┼───────────┼─────────────────────────────────
         12847 │    18.52% │ data[0]
          8291 │    11.95% │ "function names" subsection
          5738 │     8.27% │ core::fmt::Formatter::pad
          4521 │     6.52% │ alloc::string::String::push_str
```

### Common Size Bloat Causes

| Cause | Size Impact | Solution |
|-------|-------------|----------|
| Panic messages | High | Use `sc_panic!` or strip in release |
| Format strings | High | Avoid `format!`, use static strings |
| JSON serialization | Very High | Use binary encoding |
| Large static arrays | High | Generate at runtime or store off-chain |
| Unused dependencies | Variable | Audit `Cargo.toml` |
| Debug symbols | High | Build in release mode |

### Size Reduction Techniques

```toml
# Cargo.toml - optimize for size
[profile.release]
opt-level = "z"        # Optimize for size
lto = true             # Link-time optimization
codegen-units = 1      # Better optimization, slower compile
panic = "abort"        # Smaller panic handling
strip = true           # Strip symbols
```

```bash
# Build optimized release
sc-meta all build --release

# Further optimize with wasm-opt
wasm-opt -Oz output/contract.wasm -o output/contract.opt.wasm
```

## 2. Panic Analysis

### Understanding Contract Traps

When a contract traps (panics), you see:
```
error: execution terminated with signal: abort
```

### Common Trap Causes

| Symptom | Likely Cause | Investigation |
|---------|--------------|---------------|
| `unreachable` | Panic without message | Check `unwrap()`, `expect()` |
| `out of gas` | Computation limit hit | Check loops, storage access |
| `memory access` | Buffer overflow | Check array indexing |
| `integer overflow` | Math operation | Check arithmetic |

### Finding Panics in WASM

```bash
# List all functions in WASM
wasm-objdump -x output/contract.wasm | grep "func\["

# Disassemble to find unreachable instructions
wasm-objdump -d output/contract.wasm | grep -B5 "unreachable"

# Count panic-related code
wasm-objdump -d output/contract.wasm | grep -c "panic"
```

### Panic Message Stripping

By default, `sc_panic!` includes message strings. In production:

```rust
// Development - full messages
sc_panic!("Detailed error: invalid amount {}", amount);

// Production - stripped messages
// Build with --release and wasm-opt removes strings
```

Or use error codes:
```rust
const ERR_INVALID_AMOUNT: u32 = 1;
const ERR_UNAUTHORIZED: u32 = 2;

// Smaller binary, less descriptive
if amount == 0 {
    sc_panic!(ERR_INVALID_AMOUNT);
}
```

## 3. DWARF Debug Information

### Building with Debug Symbols

```bash
# Build debug version with source mapping
sc-meta all build --wasm-symbols

# Or using mxpy
mxpy contract build --debug
```

### Debug Build Output

Debug builds produce:
- `contract.wasm` - Contract bytecode
- `contract.wasm.map` - Source map (if available)
- Larger file size with DWARF sections

### Using Debug Information

```bash
# View DWARF info
wasm-objdump --debug output/contract.wasm

# List debug sections
wasm-objdump -h output/contract.wasm | grep "debug"
```

### Source-Level Debugging

With debug symbols, you can:
1. Map WASM instruction addresses to Rust source lines
2. Set breakpoints at source locations
3. Inspect variable values (in compatible debuggers)

```bash
# Using wasmtime for debugging
wasmtime run --invoke function_name -g output/contract.wasm
```

## 4. WASM Structure Analysis

### Examining Contract Structure

```bash
# Full WASM dump
wasm-objdump -x output/contract.wasm

# Sections overview
wasm-objdump -h output/contract.wasm

# Export functions (endpoints)
wasm-objdump -j Export -x output/contract.wasm

# Import functions (VM API calls)
wasm-objdump -j Import -x output/contract.wasm
```

### Understanding WASM Sections

| Section | Purpose | Audit Focus |
|---------|---------|-------------|
| Type | Function signatures | API surface |
| Import | VM API functions used | Capabilities |
| Function | Internal functions | Code size |
| Export | Public endpoints | Attack surface |
| Code | Actual bytecode | Logic |
| Data | Static data | Embedded secrets? |
| Name | Debug names | Information leak |

### Checking Exports

```bash
# List all exported functions
wasm-objdump -j Export -x output/contract.wasm | grep "func"

# Expected exports for MultiversX:
# - init: Constructor
# - upgrade: Upgrade handler
# - callBack: Callback handler
# - <endpoint_names>: Your endpoints
```

## 5. Gas Profiling

### Estimating Gas Costs

```bash
# Deploy to devnet and call endpoints
mxpy contract deploy \
    --bytecode output/contract.wasm \
    --proxy https://devnet-gateway.multiversx.com \
    --chain D \
    --pem wallet.pem \
    --gas-limit 60000000 \
    --send

# Check transaction gas used
mxpy tx get --hash <tx_hash> --proxy https://devnet-gateway.multiversx.com
```

### Identifying Gas-Heavy Code

Common gas-intensive patterns:
1. Storage reads/writes
2. Cryptographic operations
3. Large data serialization
4. Loop iterations

```rust
// Gas-expensive
for item in self.large_list().iter() {  // N storage reads
    self.process(item);
}

// Gas-optimized
let batch_size = 10;
for i in 0..batch_size {
    let item = self.large_list().get(start_index + i);
    self.process(item);
}
```

## 6. Common Debugging Scenarios

### Scenario: Contract Deployment Fails

```bash
# Check binary size
ls -la output/contract.wasm
# Max size is typically 256KB for deployment

# If too large, analyze and optimize
twiggy top output/contract.wasm
```

### Scenario: Transaction Fails with `unreachable`

1. Check for `unwrap()` calls
2. Check for array index out of bounds
3. Check for division by zero
4. Build with debug and check DWARF info

### Scenario: Gas Exceeded

```bash
# Build with debug to get better error location
sc-meta all build --wasm-symbols

# Profile the specific function
# Add logging to identify which loop/storage access is expensive
```

### Scenario: Unexpected Behavior

```rust
// Add debug logging (remove in production)
#[endpoint]
fn debug_function(&self, input: BigUint) {
    // Log to events for debugging
    self.debug_event(&input);

    // Your logic
    let result = self.compute(input);

    self.debug_event(&result);
}

#[event("debug")]
fn debug_event(&self, value: &BigUint);
```

## 7. Tools Summary

| Tool | Purpose | Install |
|------|---------|---------|
| `twiggy` | Size analysis | `cargo install twiggy` |
| `wasm-objdump` | WASM inspection | Part of wabt |
| `wasm-opt` | Size optimization | Part of binaryen |
| `wasmtime` | WASM runtime/debug | `cargo install wasmtime` |
| `sc-meta` | MultiversX build tool | `cargo install multiversx-sc-meta` |

## 8. Best Practices

1. **Always check release size** before deployment
2. **Profile on devnet** before mainnet deployment
3. **Use events for debugging** instead of storage (cheaper)
4. **Strip debug info** in production builds
5. **Monitor gas costs** as contract evolves
6. **Keep twiggy reports** to track size changes over time


# WASM Debug (Expert)

---
name: mvx_wasm_debug
description: Analyzing WASM binaries and debugging via DWARF.
---

# MultiversX WASM Debugging

This skill helps you analyze the compiled `output.wasm` file.

## 1. Binary Size Analysis
- **Twiggy**: Use `twiggy top output.wasm` to see what takes up space.
- **Bloat**: Heavy JSON deserialization code? Large static strings?

## 2. Panic Analysis
- **Abort Messages**: By default, `sc_panic!` adds a string message.
- **Optimization**: `wasm-opt` removes these in production builds (`--opt-level z`).
- **Debugging**: If the contract traps with `unreachable`, check if it ran out of gas or hit a panic without a message.

## 3. DWARF Info
- MultiversX supports building with debug symbols (`mxpy contract build --debug`).
- This allows mapping WASM instructions back to Rust source lines in the debugger.


# Property Testing

---
name: multiversx-property-testing
description: Use property-based testing and fuzzing to find edge cases in smart contract logic. Use when writing comprehensive tests, verifying invariants, or searching for unexpected behavior with random inputs.
---

# MultiversX Property Testing

Use property-based testing (fuzzing) to automatically discover edge cases and invariant violations in MultiversX smart contract logic. This approach generates random inputs to find bugs that manual testing misses.

## When to Use

- Writing comprehensive test suites
- Verifying mathematical invariants hold
- Testing complex state machines
- Finding edge cases in business logic
- Validating input handling across ranges

## 1. Tools and Setup

### Rust Property Testing Libraries

**proptest** - Most commonly used:
```toml
# Cargo.toml (dev-dependencies)
[dev-dependencies]
proptest = "1.4"
```

**cargo-fuzz** - LLVM-based fuzzing:
```bash
# Install
cargo install cargo-fuzz

# Initialize fuzz targets
cargo fuzz init
```

### MultiversX Test Environment
```toml
[dev-dependencies]
multiversx-sc-scenario = "0.54"
```

## 2. Defining Invariants

Invariants are properties that must ALWAYS hold, regardless of inputs or state.

### Common Smart Contract Invariants

| Invariant | Description | Example |
|-----------|-------------|---------|
| Conservation | Sum of parts equals total | Total supply == sum of all balances |
| Monotonicity | Value only moves one direction | Stake amount never decreases without explicit unstake |
| Bounds | Values stay within limits | User balance <= total supply |
| Consistency | Related values stay in sync | Whitelist count == whitelist set length |
| Idempotency | Repeated calls have same effect | Double-claim returns 0 second time |

### Defining Invariants in Code
```rust
// Invariant: Total supply equals sum of all balances
fn check_supply_invariant(state: &ContractState) -> bool {
    let total_supply = state.total_supply;
    let sum_of_balances: BigUint = state.balances.values().sum();
    total_supply == sum_of_balances
}

// Invariant: User balance never exceeds total supply
fn check_balance_bounds(state: &ContractState, user: &Address) -> bool {
    let user_balance = state.balances.get(user).unwrap_or_default();
    user_balance <= state.total_supply
}
```

## 3. Property Testing with proptest

### Basic Property Test
```rust
use proptest::prelude::*;

proptest! {
    #[test]
    fn test_deposit_increases_balance(amount in 1u64..1_000_000u64) {
        let mut setup = TestSetup::new();
        let initial_balance = setup.get_balance();

        setup.deposit(amount);

        let final_balance = setup.get_balance();
        prop_assert_eq!(final_balance, initial_balance + amount);
    }
}
```

### Testing with Multiple Inputs
```rust
proptest! {
    #[test]
    fn test_transfer_conservation(
        sender_initial in 1000u64..1_000_000u64,
        amount in 1u64..1000u64
    ) {
        prop_assume!(amount <= sender_initial);  // Precondition

        let mut setup = TestSetup::new();
        setup.set_balance(SENDER, sender_initial);
        setup.set_balance(RECEIVER, 0);

        let total_before = sender_initial;

        setup.transfer(SENDER, RECEIVER, amount);

        let sender_after = setup.get_balance(SENDER);
        let receiver_after = setup.get_balance(RECEIVER);
        let total_after = sender_after + receiver_after;

        // Conservation invariant
        prop_assert_eq!(total_before, total_after);
    }
}
```

### Custom Strategies
```rust
use proptest::strategy::Strategy;

// Generate valid MultiversX addresses
fn arb_address() -> impl Strategy<Value = String> {
    "[a-f0-9]{64}".prop_map(|hex| format!("erd1{}", &hex[..62]))
}

// Generate valid token amounts (avoiding overflow)
fn arb_token_amount() -> impl Strategy<Value = BigUint> {
    (0u64..u64::MAX / 2).prop_map(BigUint::from)
}

// Generate valid token identifiers
fn arb_token_id() -> impl Strategy<Value = String> {
    "[A-Z]{3,10}-[a-f0-9]{6}".prop_map(|s| s.to_uppercase())
}

proptest! {
    #[test]
    fn test_with_custom_strategies(
        addr in arb_address(),
        amount in arb_token_amount()
    ) {
        // Test logic here
    }
}
```

## 4. Stateful Property Testing

Test sequences of operations, not just individual calls.

```rust
use proptest::prelude::*;
use proptest_state_machine::*;

// Define possible operations
#[derive(Debug, Clone)]
enum Operation {
    Deposit { user: usize, amount: u64 },
    Withdraw { user: usize, amount: u64 },
    Transfer { from: usize, to: usize, amount: u64 },
}

// Model the expected state
#[derive(Debug, Clone, Default)]
struct ModelState {
    balances: HashMap<usize, u64>,
    total_supply: u64,
}

impl ModelState {
    fn apply(&mut self, op: &Operation) -> Result<(), &'static str> {
        match op {
            Operation::Deposit { user, amount } => {
                *self.balances.entry(*user).or_default() += amount;
                self.total_supply += amount;
                Ok(())
            }
            Operation::Withdraw { user, amount } => {
                let balance = self.balances.get(user).copied().unwrap_or(0);
                if balance < *amount {
                    return Err("Insufficient balance");
                }
                *self.balances.get_mut(user).unwrap() -= amount;
                self.total_supply -= amount;
                Ok(())
            }
            Operation::Transfer { from, to, amount } => {
                let from_balance = self.balances.get(from).copied().unwrap_or(0);
                if from_balance < *amount {
                    return Err("Insufficient balance");
                }
                *self.balances.get_mut(from).unwrap() -= amount;
                *self.balances.entry(*to).or_default() += amount;
                Ok(())
            }
        }
    }

    fn check_invariants(&self) -> bool {
        // Conservation: sum of balances == total supply
        let sum: u64 = self.balances.values().sum();
        sum == self.total_supply
    }
}

proptest! {
    #[test]
    fn test_operation_sequence(ops in prop::collection::vec(arb_operation(), 0..100)) {
        let mut model = ModelState::default();
        let mut contract = TestContract::new();

        for op in ops {
            let model_result = model.apply(&op);
            let contract_result = contract.execute(&op);

            // Model and contract should agree on success/failure
            prop_assert_eq!(model_result.is_ok(), contract_result.is_ok());

            // Invariants should hold after every operation
            prop_assert!(model.check_invariants());
            prop_assert!(contract.check_invariants());
        }
    }
}
```

## 5. Fuzzing with cargo-fuzz

### Setup Fuzz Target
```rust
// fuzz/fuzz_targets/deposit_fuzz.rs
#![no_main]
use libfuzzer_sys::fuzz_target;
use my_contract::*;

fuzz_target!(|data: &[u8]| {
    if data.len() < 8 {
        return;
    }

    let amount = u64::from_le_bytes(data[..8].try_into().unwrap());

    let mut setup = TestSetup::new();

    // This should never panic regardless of input
    let _ = setup.try_deposit(amount);

    // Invariants should always hold
    assert!(setup.check_invariants());
});
```

### Running Fuzzer
```bash
# Run fuzzing
cargo +nightly fuzz run deposit_fuzz

# Run for specific duration
cargo +nightly fuzz run deposit_fuzz -- -max_total_time=300

# Run with specific seed corpus
cargo +nightly fuzz run deposit_fuzz corpus/deposit_fuzz
```

## 6. Integration with Mandos Scenarios

Generate Mandos scenarios from property tests:

```rust
fn generate_mandos_scenario(ops: &[Operation]) -> String {
    let mut steps = vec![];

    for (i, op) in ops.iter().enumerate() {
        let step = match op {
            Operation::Deposit { user, amount } => {
                format!(r#"{{
                    "step": "scCall",
                    "id": "step-{}",
                    "tx": {{
                        "from": "address:user{}",
                        "to": "sc:contract",
                        "function": "deposit",
                        "egldValue": "{}",
                        "gasLimit": "5,000,000"
                    }}
                }}"#, i, user, amount)
            }
            // ... other operations
        };
        steps.push(step);
    }

    format!(r#"{{
        "name": "Generated property test",
        "steps": [{}]
    }}"#, steps.join(",\n"))
}
```

## 7. Common Testing Patterns

### Overflow Testing
```rust
proptest! {
    #[test]
    fn test_no_overflow_on_addition(a in 0u64..u64::MAX, b in 0u64..u64::MAX) {
        let mut setup = TestSetup::new();

        // Should handle overflow gracefully
        let result = setup.try_add(a, b);

        if a.checked_add(b).is_some() {
            prop_assert!(result.is_ok());
        } else {
            prop_assert!(result.is_err());
        }
    }
}
```

### Boundary Testing
```rust
proptest! {
    #[test]
    fn test_boundaries(amount in prop_oneof![
        Just(0u64),           // Zero
        Just(1u64),           // Minimum positive
        Just(u64::MAX - 1),   // Near maximum
        Just(u64::MAX),       // Maximum
        0u64..u64::MAX        // Random
    ]) {
        let mut setup = TestSetup::new();
        let result = setup.try_process(amount);

        // Verify correct behavior at boundaries
        if amount == 0 {
            prop_assert!(result.is_err());  // Should reject zero
        } else {
            prop_assert!(result.is_ok());
        }
    }
}
```

### Idempotency Testing
```rust
proptest! {
    #[test]
    fn test_claim_idempotency(user_id in 0usize..10) {
        let mut setup = TestSetup::new();
        setup.add_rewards(user_id, 1000);

        let first_claim = setup.claim(user_id);
        let second_claim = setup.claim(user_id);

        // First claim gets rewards, second gets nothing
        prop_assert_eq!(first_claim, 1000);
        prop_assert_eq!(second_claim, 0);
    }
}
```

## 8. Best Practices

1. **Start with simple invariants**: Begin with obvious properties like conservation
2. **Use shrinking**: proptest automatically shrinks failing cases to minimal examples
3. **Seed your corpus**: Add known edge cases to fuzz corpus
4. **Run continuously**: Property tests should run in CI on every commit
5. **Document invariants**: Each invariant should have a comment explaining why it must hold
6. **Test failure modes**: Verify that invalid inputs are rejected correctly


# Property Testing (Expert)

---
name: mvx_property_testing
description: Using fuzz tests in Rust for invariants.
---

# MultiversX Property Testing

This skill guides you in using property-based testing (fuzzing) to find edge cases in Smart Contract logic.

## 1. Tools
- **`cargo fuzz`**: Standard Rust fuzzer.
- **`proptest`**: Property testing framework for Rust.

## 2. Methodology
Defining Invariants:
- "Total Supply MUST equal sum of all balances."
- "User balance MUST NOT decrease if deposit fails."

## 3. Implementation (RustVM)
Write a test that:
1.  Takes random input (random amounts, random user IDs).
2.  Executes the contract logic via `blockchain_mock`.
3.  Asserts the invariant holds.

## 4. Example
```rust
proptest! {
    #[test]
    fn test_deposit_always_increases_balance(amount in 0u64..1_000_000u64) {
        let mut setup = Setup::new();
        setup.deposit(amount);
        assert_eq!(setup.balance(), amount);
    }
}
```


# Spec Compliance

---
name: multiversx-spec-compliance
description: Verify smart contract implementations match their specifications, whitepapers, and MIP standards. Use when auditing for specification adherence, validating tokenomics implementations, or checking MIP compliance.
---

# Specification Compliance Verification

Ensure that MultiversX smart contract implementations match their intended design as specified in whitepapers, technical specifications, and MultiversX Improvement Proposals (MIPs). This skill bridges the gap between documentation and code.

## When to Use

- Auditing contracts against their whitepapers
- Verifying tokenomics implementations
- Checking MIP standard compliance
- Validating economic formulas and constraints
- Reviewing upgrade proposals against specs

## 1. Verification Process Overview

### Inputs Required

| Input | Description | Source |
|-------|-------------|--------|
| Code | Rust implementation | `src/*.rs` |
| Specification | Design document | `whitepaper.pdf`, `README.md`, `specs/` |
| MIP Reference | Standard requirements | MultiversX MIPs |

### Process Flow

```
1. Extract Claims → List all requirements from spec
2. Map to Code   → Find implementing code for each claim
3. Verify Logic  → Confirm implementation matches spec
4. Document      → Record findings and deviations
```

## 2. Claim Extraction

### Specification Language Keywords

Extract statements containing these keywords:

| Keyword | Meaning | Example |
|---------|---------|---------|
| MUST | Required | "Users MUST stake minimum 100 tokens" |
| MUST NOT | Forbidden | "Admin MUST NOT withdraw user funds" |
| SHOULD | Recommended | "Contract SHOULD emit events" |
| SHALL | Obligation | "Rewards SHALL be calculated daily" |
| MAY | Optional | "Users MAY delegate to multiple validators" |

### Example Claim Extraction

**From Whitepaper:**
> "The staking contract MUST enforce a minimum stake of 1000 EGLD.
> Rewards MUST be calculated using APY = base_rate * (1 + boost_factor).
> Users MUST NOT be able to withdraw during the lock period."

**Extracted Claims:**
```markdown
1. [MUST] Minimum stake: 1000 EGLD
2. [MUST] Reward formula: APY = base_rate * (1 + boost_factor)
3. [MUST NOT] Withdrawal during lock period
```

### Claim Documentation Template

```markdown
| ID | Type | Claim | Source | Code Location | Status |
|----|------|-------|--------|---------------|--------|
| C1 | MUST | Min stake 1000 EGLD | WP §3.1 | stake.rs:45 | Verified |
| C2 | MUST | APY formula | WP §4.2 | rewards.rs:78 | Deviation |
| C3 | MUST NOT | Lock withdrawal | WP §3.3 | withdraw.rs:23 | Verified |
```

## 3. Code Mapping

### Finding Implementing Code

For each claim, locate the relevant code:

```rust
// Claim C1: Min stake 1000 EGLD
// Location: src/stake.rs:45

const MIN_STAKE: u64 = 1000_000000000000000000u64;  // 1000 EGLD in wei

#[payable("EGLD")]
#[endpoint]
fn stake(&self) {
    let payment = self.call_value().egld_value();
    require!(
        payment.clone_value() >= BigUint::from(MIN_STAKE),
        "Minimum stake is 1000 EGLD"  // ← Implements C1
    );
    // ...
}
```

### Mapping Checklist

For each claim:
- [ ] Code location identified
- [ ] Implementation logic understood
- [ ] Constants/values match spec
- [ ] Edge cases handled per spec

## 4. Verification Techniques

### Formula Verification

**Spec:**
> "APY = base_rate * (1 + boost_factor)"

**Code Review:**
```rust
fn calculate_apy(&self, base_rate: BigUint, boost_factor: BigUint) -> BigUint {
    // Verify this matches: APY = base_rate * (1 + boost_factor)

    let one = BigUint::from(PRECISION);  // Check: What is PRECISION?
    let boost_multiplier = &one + &boost_factor;
    let apy = &base_rate * &boost_multiplier / &one;

    // QUESTION: Is division by PRECISION correct? Spec doesn't mention it.
    // FINDING: Precision handling not in spec - potential deviation

    apy
}
```

### Constraint Verification

**Spec:**
> "Users MUST NOT withdraw during the lock period of 7 days"

**Code Review:**
```rust
#[endpoint]
fn withdraw(&self) {
    let stake_time = self.stake_timestamp(&caller).get();
    let current_time = self.blockchain().get_block_timestamp();
    let lock_period = self.lock_period().get();  // Check: Is this 7 days?

    require!(
        current_time >= stake_time + lock_period,
        "Lock period not elapsed"
    );
    // ...
}

// VERIFICATION NEEDED:
// 1. Is lock_period initialized to 7 days (604800 seconds)?
// 2. Is lock_period immutable or can admin change it?
// 3. Can this be bypassed through any other endpoint?
```

### State Transition Verification

**Spec:**
> "State transitions: INACTIVE → ACTIVE → COMPLETED"

**Code Review:**
```rust
#[derive(TopEncode, TopDecode, TypeAbi, PartialEq)]
pub enum State {
    Inactive,
    Active,
    Completed,
}

fn activate(&self) {
    let current = self.state().get();
    require!(current == State::Inactive, "Can only activate from Inactive");
    self.state().set(State::Active);
}

fn complete(&self) {
    let current = self.state().get();
    require!(current == State::Active, "Can only complete from Active");
    self.state().set(State::Completed);
}

// VERIFICATION:
// ✓ Inactive → Active (activate)
// ✓ Active → Completed (complete)
// ? Is there a way to go backwards? (Should not be allowed)
// ? Can state be set directly? (Search for .set(State::))
```

## 5. MultiversX MIP Compliance

### Common MIPs to Verify

| MIP | Topic | Key Requirements |
|-----|-------|------------------|
| MIP-2 | Semi-Fungible Tokens | SFT metadata format, royalties |
| MIP-3 | Dynamic NFTs | Attribute update mechanisms |
| MIP-4 | Royalties | Royalty calculation and distribution |

### MIP-2 SFT Compliance Example

**Requirements:**
- Token type must be SFT (nonce > 0, quantity > 1 allowed)
- Metadata format follows standard
- Royalties encoded correctly

**Verification:**
```rust
// Check NFT creation follows MIP-2

#[endpoint]
fn create_sft(&self, ...) -> u64 {
    // VERIFY: Using NonFungibleTokenMapper correctly
    let nonce = self.sft_token().nft_create(
        initial_quantity,  // MIP-2: Must allow quantity > 1
        &SftAttributes {
            // MIP-2: Required attributes
            name: ...,
            royalties: ...,  // In basis points (0-10000)
            hash: ...,
            attributes: ...,
            uris: ...,
        }
    );
    nonce
}
```

## 6. Tokenomics Verification

### Common Tokenomics Claims

| Claim Type | Example | Verification |
|------------|---------|--------------|
| Total Supply | Max 1B tokens | Check mint constraints |
| Inflation Rate | 5% annually | Verify mint formula |
| Burn Rate | 1% per transfer | Check fee calculation |
| Distribution | 40% community | Verify initial allocation |

### Example: Inflation Verification

**Spec:**
> "Annual inflation rate is 5%, calculated per epoch"

**Code Review:**
```rust
const ANNUAL_INFLATION_BPS: u64 = 500;  // 5% = 500 basis points
const EPOCHS_PER_YEAR: u64 = 365;       // Assuming daily epochs

fn calculate_epoch_inflation(&self) -> BigUint {
    let total_supply = self.total_supply().get();
    let epoch_rate = ANNUAL_INFLATION_BPS / EPOCHS_PER_YEAR;

    // VERIFICATION:
    // 500 / 365 = 1.369... but integer division = 1
    // This is LESS than 5% annually (365 * 1 = 365 bps = 3.65%)
    // FINDING: Integer precision loss causes ~27% less inflation than spec

    &total_supply * BigUint::from(epoch_rate) / BigUint::from(10000u64)
}
```

## 7. Deviation Handling

### Deviation Categories

| Category | Severity | Action |
|----------|----------|--------|
| Critical | Breaks core functionality | Must fix |
| Major | Significant difference | Should fix |
| Minor | Slight variation | Document |
| Enhancement | Beyond spec | Document |

### Deviation Report Template

```markdown
## Deviation Report

### DEV-001: Inflation Calculation Precision Loss

**Claim**: Annual inflation rate is 5%
**Source**: Whitepaper §5.2
**Code**: rewards.rs:calculate_epoch_inflation()

**Expected**: 5.00% annual inflation
**Actual**: 3.65% annual inflation

**Root Cause**: Integer division of basis points by epochs
loses precision (500/365 = 1, not 1.369)

**Impact**: ~27% less inflation than documented

**Recommendation**: Use scaled arithmetic
```rust
// Instead of:
let epoch_rate = ANNUAL_INFLATION_BPS / EPOCHS_PER_YEAR;

// Use:
let scaled_annual = BigUint::from(ANNUAL_INFLATION_BPS) * &total_supply;
let epoch_inflation = scaled_annual / BigUint::from(EPOCHS_PER_YEAR) / BigUint::from(10000u64);
```

**Severity**: Major
**Status**: Open
```

## 8. Compliance Report Template

```markdown
# Specification Compliance Report

**Project**: [Name]
**Specification Version**: [Version]
**Code Version**: [Commit/Tag]
**Date**: [Date]
**Auditor**: [Name]

## Executive Summary
[Brief overview of compliance status]

## Specification Coverage

| Section | Claims | Verified | Deviations | Not Found |
|---------|--------|----------|------------|-----------|
| §3 Staking | 12 | 10 | 1 | 1 |
| §4 Rewards | 8 | 7 | 1 | 0 |
| §5 Governance | 5 | 5 | 0 | 0 |
| **Total** | **25** | **22** | **2** | **1** |

## Verified Claims
[List of all verified claims with code references]

## Deviations
[Detailed deviation reports]

## Unimplemented Claims
[Claims from spec not found in code]

## MIP Compliance
| MIP | Status | Notes |
|-----|--------|-------|
| MIP-2 | Compliant | - |
| MIP-4 | Partial | Royalty distribution differs |

## Recommendations
1. [Priority recommendation]
2. [Second priority]

## Conclusion
[Overall compliance assessment]
```

## 9. Best Practices

1. **Get the right spec version**: Ensure code and spec versions match
2. **Document assumptions**: When spec is ambiguous, document interpretation
3. **Test boundary values**: Verify spec limits are correctly implemented
4. **Check units**: EGLD vs wei, seconds vs epochs, basis points vs percentages
5. **Verify precision**: BigUint calculations should maintain precision
6. **Review change history**: Check if spec evolved and code was updated


# Spec Compliance (Legacy)

---
name: spec_compliance
description: Verifying code against Whitepapers or MIPs (MultiversX Improvement Proposals).
---

# Specification Compliance

This skill ensures the implemented Smart Contract matches the intended design documents (Whitepaper, MIP, Spec).

## 1. Inputs
- **Code**: The Rust implementation.
- **Spec**: `whitepaper.pdf`, `MIP-XX.md`, or `README.md`.

## 2. Process
1.  **Extract Claims**: List every "MUST", "SHOULD", and formula in the Spec.
2.  **Map to Code**: Find the exact lines implementing each claim.
3.  **Verify**: Does the math match? Are the constraints enforced?

## 3. MultiversX Specifics
- **MIP Compliance**: If the project claims to implement `MIP-2` (Fractional NFT), verify it adheres to the SFT metadata standard defined in that MIP.
- **Economics**: Verify tokenomics (inflation, burn rates) match the whitepaper exactly (BigUint precision matters!).


# Testing Handbook

---
name: mvx_testing_handbook
description: Guide to mandos (scenarios), rust-vm unit tests, and chain-simulator.
---

# MultiversX Testing Handbook

This skill provides expert guidance on the 3 layers of MultiversX testing: RustVM Unit Tests, Mandos Integration Tests, and Chain Simulation.

## 1. RustVM Unit Tests
- **Location**: `#[cfg(test)]` modules within contract files or `tests/` directory.
- **Speed**: Instant.
- **Scope**: Internal logic, strict math, private functions.
- **Mocking**: Use `multiversx_sc_scenario::imports::*` to mock the blockchain environment (`blockchain_mock.set_caller(addr)`).

## 2. Mandos Scenarios (`.scen.json`)
- **Location**: `scenarios/` directory.
- **Requirement**: "If it's an endpoint, it MUST have a Mandos test."
- **Execution**:
    - `cargo test-gen` generates Rust wrappers for scenarios.
    - `cargo test` runs them.
- **Key Concepts**:
    - `step: setState`: Initialize accounts and balances.
    - `step: scCall`: Execute endpoint.
    - `step: checkState`: Verify storage matches expected values.

## 3. Chain Simulator (`mx-chain-simulator-go`)
- **Location**: Separate system test suite (often Go or Python).
- **Scope**: Interaction with Node API, complex cross-shard reorgs, off-chain indexing.
- **Tool**: Use `POST /simulator/generate-blocks` to force execution.

## 4. Coverage Strategy
- **Money In/Out**: 100% Mandos coverage required.
- **View Functions**: Unit test coverage sufficient.
- **Access Control**: Explicit negative tests (expect error 4) for unauthorized calls.


# Semgrep Creator

---
name: multiversx-semgrep-creator
description: Write custom Semgrep rules to automatically detect MultiversX-specific security patterns and best practice violations. Use when creating automated code scanning, enforcing coding standards, or scaling security reviews.
---

# Semgrep Rule Creator for MultiversX

Create custom Semgrep rules to automatically detect MultiversX-specific security patterns, coding violations, and best practice issues. This skill enables scalable security scanning across codebases.

## When to Use

- Setting up automated security scanning for CI/CD
- Enforcing MultiversX coding standards across teams
- Scaling security reviews with automated pattern detection
- Creating custom rules after finding manual vulnerabilities
- Building organizational security rule libraries

## 1. Semgrep Basics for Rust

### Rule Structure
```yaml
rules:
  - id: rule-identifier
    languages: [rust]
    message: "Description of the issue and why it matters"
    severity: ERROR  # ERROR, WARNING, INFO
    patterns:
      - pattern: <code pattern to match>
    metadata:
      category: security
      technology:
        - multiversx
```

### Pattern Syntax

| Syntax | Meaning | Example |
|--------|---------|---------|
| `$VAR` | Any expression | `$X + $Y` matches `a + b` |
| `...` | Zero or more statements | `{ ... }` matches any block |
| `$...VAR` | Zero or more arguments | `func($...ARGS)` |
| `<... $X ...>` | Contains expression | `<... panic!(...) ...>` |

## 2. Common MultiversX Patterns

### Unsafe Arithmetic Detection

```yaml
rules:
  - id: mvx-unsafe-addition
    languages: [rust]
    message: "Potential arithmetic overflow. Use BigUint or checked arithmetic for financial calculations."
    severity: ERROR
    patterns:
      - pattern: $X + $Y
      - pattern-not: $X.checked_add($Y)
      - pattern-not: BigUint::from($X) + BigUint::from($Y)
    paths:
      include:
        - "*/src/*.rs"
    metadata:
      category: security
      subcategory: arithmetic
      cwe: "CWE-190: Integer Overflow"

  - id: mvx-unsafe-multiplication
    languages: [rust]
    message: "Potential multiplication overflow. Use BigUint or checked_mul."
    severity: ERROR
    patterns:
      - pattern: $X * $Y
      - pattern-not: $X.checked_mul($Y)
      - pattern-not: BigUint::from($X) * BigUint::from($Y)
```

### Floating Point Detection

```yaml
rules:
  - id: mvx-float-forbidden
    languages: [rust]
    message: "Floating point arithmetic is non-deterministic and forbidden in smart contracts."
    severity: ERROR
    pattern-either:
      - pattern: "let $X: f32 = ..."
      - pattern: "let $X: f64 = ..."
      - pattern: "$X as f32"
      - pattern: "$X as f64"
    metadata:
      category: security
      subcategory: determinism
```

### Payable Endpoint Without Value Check

```yaml
rules:
  - id: mvx-payable-no-check
    languages: [rust]
    message: "Payable endpoint does not check payment value. Verify token ID and amount."
    severity: WARNING
    patterns:
      - pattern: |
          #[payable("*")]
          #[endpoint]
          fn $FUNC(&self, $...PARAMS) {
              $...BODY
          }
      - pattern-not: |
          #[payable("*")]
          #[endpoint]
          fn $FUNC(&self, $...PARAMS) {
              <... self.call_value() ...>
          }
    metadata:
      category: security
      subcategory: input-validation
```

### Unsafe Unwrap Usage

```yaml
rules:
  - id: mvx-unsafe-unwrap
    languages: [rust]
    message: "unwrap() can panic. Use unwrap_or_else with sc_panic! or proper error handling."
    severity: ERROR
    patterns:
      - pattern: $EXPR.unwrap()
      - pattern-not-inside: |
          #[test]
          fn $FUNC() { ... }
    fix: "$EXPR.unwrap_or_else(|| sc_panic!(\"Error message\"))"
    metadata:
      category: security
      subcategory: error-handling
```

### Missing Owner Check

```yaml
rules:
  - id: mvx-sensitive-no-owner-check
    languages: [rust]
    message: "Sensitive operation without owner check. Add #[only_owner] or explicit verification."
    severity: ERROR
    patterns:
      - pattern: |
          #[endpoint]
          fn $FUNC(&self, $...PARAMS) {
              <... self.$MAPPER().set(...) ...>
          }
      - pattern-not: |
          #[only_owner]
          #[endpoint]
          fn $FUNC(&self, $...PARAMS) { ... }
      - pattern-not: |
          #[endpoint]
          fn $FUNC(&self, $...PARAMS) {
              <... self.blockchain().get_owner_address() ...>
          }
      - metavariable-regex:
          metavariable: $MAPPER
          regex: "(admin|owner|config|fee|rate)"
```

## 3. Advanced Patterns

### Callback Without Error Handling

```yaml
rules:
  - id: mvx-callback-no-error-handling
    languages: [rust]
    message: "Callback does not handle error case. Async call failures will silently proceed."
    severity: ERROR
    patterns:
      - pattern: |
          #[callback]
          fn $FUNC(&self, $...PARAMS) {
              $...BODY
          }
      - pattern-not: |
          #[callback]
          fn $FUNC(&self, #[call_result] $RESULT: ManagedAsyncCallResult<$TYPE>) {
              ...
          }
```

### Unbounded Iteration

```yaml
rules:
  - id: mvx-unbounded-iteration
    languages: [rust]
    message: "Iterating over storage mapper without bounds. Can cause DoS via gas exhaustion."
    severity: ERROR
    pattern-either:
      - pattern: self.$MAPPER().iter()
      - pattern: |
          for $ITEM in self.$MAPPER().iter() {
              ...
          }
    metadata:
      category: security
      subcategory: dos
      cwe: "CWE-400: Uncontrolled Resource Consumption"
```

### Storage Key Collision Risk

```yaml
rules:
  - id: mvx-storage-key-short
    languages: [rust]
    message: "Storage key is very short, increasing collision risk. Use descriptive keys."
    severity: WARNING
    patterns:
      - pattern: '#[storage_mapper("$KEY")]'
      - metavariable-regex:
          metavariable: $KEY
          regex: "^.{1,3}$"
```

### Reentrancy Pattern Detection

```yaml
rules:
  - id: mvx-reentrancy-risk
    languages: [rust]
    message: "External call before state update. Follow Checks-Effects-Interactions pattern."
    severity: ERROR
    patterns:
      - pattern: |
          fn $FUNC(&self, $...PARAMS) {
              ...
              self.send().$SEND_METHOD(...);
              ...
              self.$STORAGE().set(...);
              ...
          }
      - pattern: |
          fn $FUNC(&self, $...PARAMS) {
              ...
              self.tx().to(...).transfer();
              ...
              self.$STORAGE().set(...);
              ...
          }
```

## 4. Creating Rules from Findings

### Workflow

1. **Find a bug manually** during audit
2. **Abstract the pattern** - what makes this a bug?
3. **Write a Semgrep rule** to catch similar issues
4. **Test on the codebase** - find all variants
5. **Refine to reduce false positives**

### Example: From Bug to Rule

**Bug Found:**
```rust
#[endpoint]
fn withdraw(&self, amount: BigUint) {
    let caller = self.blockchain().get_caller();
    self.send().direct_egld(&caller, &amount);  // Sends before balance check!
    self.balances(&caller).update(|b| *b -= &amount);  // Can underflow
}
```

**Pattern Abstracted:**
- Send/transfer before state update
- No balance validation before deduction

**Rule Created:**
```yaml
rules:
  - id: mvx-withdraw-pattern-unsafe
    languages: [rust]
    message: "Withdrawal sends funds before updating balance. Risk of reentrancy and underflow."
    severity: ERROR
    patterns:
      - pattern: |
          fn $FUNC(&self, $...PARAMS) {
              ...
              self.send().$METHOD(...);
              ...
              self.$BALANCE(...).update(|$B| *$B -= ...);
              ...
          }
      - pattern: |
          fn $FUNC(&self, $...PARAMS) {
              ...
              self.tx().to(...).transfer();
              ...
              self.$BALANCE(...).update(|$B| *$B -= ...);
              ...
          }
```

## 5. Running Semgrep

### Command Line Usage
```bash
# Run single rule
semgrep --config rules/mvx-unsafe-arithmetic.yaml src/

# Run all rules in directory
semgrep --config rules/ src/

# Output JSON for processing
semgrep --config rules/ --json -o results.json src/

# Ignore test files
semgrep --config rules/ --exclude="*_test.rs" --exclude="tests/" src/
```

### CI/CD Integration
```yaml
# GitHub Actions example
- name: Run Semgrep
  uses: returntocorp/semgrep-action@v1
  with:
    config: >-
      rules/mvx-security.yaml
      rules/mvx-best-practices.yaml
```

## 6. Rule Library Organization

```
semgrep-rules/
├── security/
│   ├── mvx-arithmetic.yaml      # Overflow/underflow
│   ├── mvx-access-control.yaml  # Auth issues
│   ├── mvx-reentrancy.yaml      # CEI violations
│   └── mvx-input-validation.yaml
├── best-practices/
│   ├── mvx-storage.yaml         # Storage patterns
│   ├── mvx-gas.yaml             # Gas optimization
│   └── mvx-error-handling.yaml
└── style/
    ├── mvx-naming.yaml          # Naming conventions
    └── mvx-documentation.yaml   # Doc requirements
```

## 7. Testing Rules

### Test File Format
```yaml
# test/mvx-unsafe-unwrap.test.yaml
rules:
  - id: mvx-unsafe-unwrap
    # ... rule definition ...

# Test cases
test_cases:
  - name: "Should match unwrap"
    code: |
      fn test() {
          let x = some_option.unwrap();
      }
    should_match: true

  - name: "Should not match unwrap_or_else"
    code: |
      fn test() {
          let x = some_option.unwrap_or_else(|| sc_panic!("Error"));
      }
    should_match: false
```

### Running Tests
```bash
semgrep --test rules/
```

## 8. Best Practices for Rule Writing

1. **Start specific, then generalize**: Begin with exact pattern, relax constraints carefully
2. **Include fix suggestions**: Use `fix:` field when automated fixes are safe
3. **Document the "why"**: Message should explain impact, not just what's detected
4. **Include CWE references**: Link to standard vulnerability classifications
5. **Test with real codebases**: Validate against actual MultiversX projects
6. **Version your rules**: Rules evolve as framework APIs change
7. **Categorize by severity**: ERROR for security, WARNING for best practices


# Semgrep Creator (Expert)

---
name: mvx_semgrep_creator
description: Writing custom Semgrep rules to enforce MultiversX best practices.
---

# Semgrep Rule Creator (MX)

This skill guides you in writing Semgrep rules to catch MultiversX-specific patterns automatically.

## 1. Common Patterns
- **Unsafe Math**: `x + y` where `x` is `u64`.
- **Floating Point**: `f64`.
- **Endpoint without Payment Check**: `#[payable("*")]` function without `call_value()`.

## 2. Template
```yaml
rules:
  - id: mvx-unsafe-addition
    languages: [rust]
    message: "Potential arithmetic overflow. Use checked_add or BigUint."
    severity: ERROR
    patterns:
      - pattern: $X + $Y
      - pattern-not: $X.checked_add($Y)
      - pattern-inside: |
          #[multiversx_sc::contract]
          trait Contract {
            ...
          }
```

## 3. Workflow
1.  **Identify Pattern**: See `mvx_variant_analysis`.
2.  **Write Rule**: Use the template.
3.  **Test**: Run on the codebase using `semgrep --config rules.yaml .`
4.  **Refine**: Reduce false positives.


# Diff Review

---
name: multiversx-diff-review
description: Review changes between smart contract versions with focus on upgradeability and security implications. Use when reviewing PRs, upgrade proposals, or analyzing differences between deployed and new code.
---

# Differential Review

Analyze differences between two versions of a MultiversX codebase, focusing on security implications of changes, storage layout compatibility, and upgrade safety.

## When to Use

- Reviewing pull requests with contract changes
- Auditing upgrade proposals before deployment
- Analyzing differences between deployed code and proposed updates
- Verifying fix implementations don't introduce regressions

## 1. Upgradeability Checks (MultiversX-Specific)

### Storage Layout Compatibility

**CRITICAL**: Storage layout changes can corrupt existing data.

#### Struct Field Ordering
```rust
// v1 - Original struct
#[derive(TopEncode, TopDecode, TypeAbi)]
pub struct UserData {
    pub balance: BigUint,      // Offset 0
    pub last_claim: u64,       // Offset 1
}

// v2 - DANGEROUS: Reordered fields
pub struct UserData {
    pub last_claim: u64,       // Now at Offset 0 - BREAKS EXISTING DATA
    pub balance: BigUint,      // Now at Offset 1 - CORRUPTED
}

// v2 - SAFE: Append new fields only
pub struct UserData {
    pub balance: BigUint,      // Offset 0 - unchanged
    pub last_claim: u64,       // Offset 1 - unchanged
    pub new_field: bool,       // Offset 2 - NEW (safe)
}
```

#### Storage Mapper Key Changes
```rust
// v1
#[storage_mapper("user_balance")]
fn user_balance(&self, user: &ManagedAddress) -> SingleValueMapper<BigUint>;

// v2 - DANGEROUS: Changed storage key
#[storage_mapper("userBalance")]  // Different key = new empty storage!
fn user_balance(&self, user: &ManagedAddress) -> SingleValueMapper<BigUint>;
```

### Initialization on Upgrade

**CRITICAL**: `#[init]` is NOT called on upgrade. Only `#[upgrade]` runs.

```rust
// v1 - Original contract
#[init]
fn init(&self) {
    self.config().set(DefaultConfig::new());
}

// v2 - Added new storage mapper
#[storage_mapper("newFeatureEnabled")]
fn new_feature_enabled(&self) -> SingleValueMapper<bool>;

// WRONG: Assuming init runs
#[init]
fn init(&self) {
    self.config().set(DefaultConfig::new());
    self.new_feature_enabled().set(true);  // Never runs on upgrade!
}

// CORRECT: Initialize in upgrade
#[upgrade]
fn upgrade(&self) {
    self.new_feature_enabled().set(true);  // Properly initializes
}
```

### Breaking Changes Checklist

| Change Type | Risk | Mitigation |
|------------|------|------------|
| Struct field reorder | Critical | Never reorder, only append |
| Storage key rename | Critical | Keep old key, migrate data |
| New required storage | High | Initialize in `#[upgrade]` |
| Removed endpoint | Medium | Ensure no external dependencies |
| Changed endpoint signature | Medium | Version API or maintain compatibility |
| New validation rules | Medium | Consider existing state validity |

## 2. Regression Analysis

### New Features Impact
- Do new features break existing invariants?
- Are there new attack vectors introduced?
- Do gas costs change significantly?

### Deleted Code Analysis
When code is removed, verify:
- Was this an intentional security fix?
- Was a validation check removed (potential vulnerability)?
- Are there other code paths that depended on this?

```rust
// v1 - Had balance check
fn withdraw(&self, amount: BigUint) {
    require!(amount <= self.balance().get(), "Insufficient balance");
    // ... withdrawal logic
}

// v2 - Check removed - WHY?
fn withdraw(&self, amount: BigUint) {
    // Missing balance check! Was this intentional?
    // ... withdrawal logic
}
```

### Modified Logic Analysis
For changed code, verify:
- Edge cases still handled correctly
- Error messages updated appropriately
- Related code paths updated consistently

## 3. Review Workflow

### Step 1: Generate Clean Diff
```bash
# Between git tags/commits
git diff v1.0.0..v2.0.0 -- src/

# Ignore formatting changes
git diff -w v1.0.0..v2.0.0 -- src/

# Focus on specific file
git diff v1.0.0..v2.0.0 -- src/lib.rs
```

### Step 2: Categorize Changes

Create a change inventory:

```markdown
## Change Summary

### Storage Changes
- [ ] user_data struct: Added `reward_multiplier` field (SAFE - appended)
- [ ] New mapper: `feature_flags` (VERIFY: initialized in upgrade)

### Endpoint Changes
- [ ] deposit(): Added token validation (SECURITY FIX)
- [ ] withdraw(): Changed gas calculation (VERIFY: no DoS vector)

### Removed Code
- [ ] legacy_claim(): Removed entire endpoint (VERIFY: no external callers)

### New Code
- [ ] batch_transfer(): New endpoint (FULL REVIEW NEEDED)
```

### Step 3: Trace Data Flow

For each changed data structure:
1. Find all read locations
2. Find all write locations
3. Verify consistency across changes

### Step 4: Verify Test Coverage

```bash
# Check if new code paths are tested
sc-meta test

# Generate test coverage report
cargo tarpaulin --out Html
```

## 4. Security-Specific Diff Checks

### Access Control Changes
```rust
// v1 - Owner only
#[only_owner]
#[endpoint]
fn sensitive_action(&self) { }

// v2 - DANGEROUS: Removed access control
#[endpoint]  // Now public! Was this intentional?
fn sensitive_action(&self) { }
```

### Payment Handling Changes
```rust
// v1 - Validated token
#[payable("*")]
fn deposit(&self) {
    let payment = self.call_value().single_esdt();
    require!(payment.token_identifier == self.accepted_token().get(), "Wrong token");
}

// v2 - DANGEROUS: Removed validation
#[payable("*")]
fn deposit(&self) {
    let payment = self.call_value().single_esdt();
    // Missing token validation! Accepts any token now
}
```

### Arithmetic Changes
```rust
// v1 - Safe arithmetic
let result = a.checked_add(&b).unwrap_or_else(|| sc_panic!("Overflow"));

// v2 - DANGEROUS: Removed overflow protection
let result = a + b;  // Can overflow!
```

## 5. Deliverable Template

```markdown
# Differential Review Report

**Versions Compared**: v1.0.0 → v2.0.0
**Reviewer**: [Name]
**Date**: [Date]

## Summary
[One paragraph overview of changes]

## Critical Findings
1. [Finding with severity and recommendation]

## Storage Compatibility
- [ ] No struct field reordering
- [ ] New mappers initialized in #[upgrade]
- [ ] Storage keys unchanged

## Breaking Changes
| Change | Impact | Migration Required |
|--------|--------|-------------------|
| ... | ... | ... |

## Recommendations
1. [Specific actionable recommendation]
```

## Common Pitfalls

- **Assuming init runs on upgrade**: Always check `#[upgrade]` function
- **Missing storage migration**: Renamed keys lose existing data
- **Removed validations**: Could be intentional security fix or accidental vulnerability
- **Changed math precision**: Can affect existing calculations
- **Modified access control**: Could expose sensitive functions


# Diff Review (Legacy)

---
name: diff_review
description: Reviewing changes between versions of SCs (Upgradeability checks).
---

# Differential Review

This skill helps you analyze the difference between two versions of a codebase, focusing on security implications of changes.

## 1. Upgradeability Checks (MultiversX)
When reviewing a diff between `v1` and `v2` of a Smart Contract:
- **Storage Layout**:
    - *Critical*: Did the order of fields in a `struct` stored in a `VecMapper` or `SingleValueMapper` change?
    - *Result*: Usage of existing data will interpret bytes incorrectly (Memory Corruption).
    - *Fix*: Append new fields to the end of structs, never reorder.
- **Initialization**:
    - *Critical*: Does `v2` introduce new Storage Mappers?
    - *Check*: Are they initialized in `#[upgrade]`? (Remember `#[init]` is NOT called on upgrade).

## 2. Regression Testing
- **New Features**: Do they break old invariants?
- **Deleted Code**: Was a check removed? Why?

## 3. Workflow
1.  **Generate Diff**: `git diff v1..v2`.
2.  **Filter Noise**: Ignore formatting/style changes.
3.  **Trace Data**: Follow the flow of changed data structures.


# Fix Verification

---
name: multiversx-fix-verification
description: Rigorously verify that reported vulnerabilities are properly fixed without introducing regressions. Use when reviewing security patches, validating bug fixes, or confirming remediation completeness.
---

# Fix Verification

Rigorously verify that a reported vulnerability has been eliminated without introducing regressions or new issues. This skill ensures fixes are complete, tested, and safe to deploy.

## When to Use

- Reviewing security patches before deployment
- Validating bug fix implementations
- Confirming audit finding remediations
- Re-testing after fix iterations

## 1. The Verification Loop

### Step 1: Reproduce the Bug
Create a test scenario that demonstrates the vulnerability:

```json
// scenarios/exploit_before_fix.scen.json
{
    "name": "Demonstrate vulnerability - should fail before fix",
    "steps": [
        {
            "step": "scCall",
            "comment": "Attacker exploits the vulnerability",
            "tx": {
                "from": "address:attacker",
                "to": "sc:vulnerable_contract",
                "function": "vulnerable_endpoint",
                "arguments": ["...exploit_payload..."],
                "gasLimit": "5,000,000"
            },
            "expect": {
                "status": "0",
                "message": "*"
            }
        }
    ]
}
```

### Step 2: Apply the Fix
Review the code modification that addresses the vulnerability.

### Step 3: Verify Fix Effectiveness
Run the exploit scenario - it MUST now fail (or behave correctly):

```bash
# The exploit scenario should now pass (exploit blocked)
sc-meta test --scenario scenarios/exploit_before_fix.scen.json
```

### Step 4: Run Regression Suite
ALL existing tests must still pass:

```bash
# Full test suite
sc-meta test

# Or with cargo
cargo test
```

## 2. Common Fix Failures

### Partial Fix
The fix addresses one path but misses variants:

```rust
// VULNERABILITY: Missing amount validation
#[endpoint]
fn deposit(&self) {
    let amount = self.call_value().egld_value();
    // No check for amount > 0
}

// PARTIAL FIX: Only fixed deposit, not transfer
#[endpoint]
fn deposit(&self) {
    let amount = self.call_value().egld_value();
    require!(amount > 0, "Amount must be positive");  // Fixed!
}

#[endpoint]
fn transfer(&self, amount: BigUint) {
    // Still missing amount > 0 check!  <- VARIANT NOT FIXED
}
```

**Verification**: Use `multiversx-variant-analysis` to find all similar code paths.

### Moved Bug (Fix Creates New Issue)
The fix prevents the original exploit but introduces a new vulnerability:

```rust
// VULNERABILITY: Reentrancy
#[endpoint]
fn withdraw(&self) {
    let balance = self.balance().get();
    self.send_egld(&caller, &balance);  // External call before state update
    self.balance().clear();
}

// BAD FIX: Prevents reentrancy but creates DoS
#[endpoint]
fn withdraw(&self) {
    self.locked().set(true);  // Lock added
    let balance = self.balance().get();
    self.send_egld(&caller, &balance);
    self.balance().clear();
    // Missing: self.locked().set(false);  <- LOCK NEVER RELEASED!
}

// CORRECT FIX: Checks-Effects-Interactions pattern
#[endpoint]
fn withdraw(&self) {
    let balance = self.balance().get();
    self.balance().clear();  // State update BEFORE external call
    self.send_egld(&caller, &balance);
}
```

### Incomplete Validation
The fix adds validation but with incorrect conditions:

```rust
// VULNERABILITY: Integer overflow
let total = amount1 + amount2;  // Can overflow

// INCOMPLETE FIX: Checks one but not both
require!(amount1 < MAX_AMOUNT, "Amount1 too large");
let total = amount1 + amount2;  // Still overflows if amount2 is large!

// CORRECT FIX: Checked arithmetic
let total = amount1.checked_add(&amount2)
    .unwrap_or_else(|| sc_panic!("Overflow"));
```

## 3. Verification Checklist

### Code Review
- [ ] Fix addresses the root cause, not just symptoms
- [ ] All code paths with similar patterns are fixed (variant analysis)
- [ ] No new vulnerabilities introduced by the fix
- [ ] Fix follows MultiversX best practices

### Testing
- [ ] Exploit scenario created that fails on vulnerable code
- [ ] Exploit scenario passes (blocked) on fixed code
- [ ] All existing tests pass (no regressions)
- [ ] Edge cases tested (boundary values, empty inputs, max values)

### Documentation
- [ ] Fix commit clearly describes the vulnerability
- [ ] Test scenario documents the attack vector
- [ ] Any behavioral changes documented

## 4. Test Scenario Template

```json
{
    "name": "Verify fix for [VULNERABILITY_ID]",
    "comment": "This scenario verifies that [DESCRIPTION] is properly fixed",
    "steps": [
        {
            "step": "setState",
            "comment": "Setup vulnerable state",
            "accounts": {
                "address:attacker": { "nonce": "0", "balance": "1000" },
                "sc:contract": { "code": "file:output/contract.wasm" }
            }
        },
        {
            "step": "scCall",
            "comment": "Attempt exploit - should fail after fix",
            "tx": {
                "from": "address:attacker",
                "to": "sc:contract",
                "function": "vulnerable_function",
                "arguments": ["exploit_input"]
            },
            "expect": {
                "status": "4",
                "message": "str:Expected error message"
            }
        },
        {
            "step": "checkState",
            "comment": "Verify state unchanged (exploit blocked)",
            "accounts": {
                "sc:contract": {
                    "storage": {
                        "str:sensitive_value": "original_value"
                    }
                }
            }
        }
    ]
}
```

## 5. Deliverable: Verification Report

```markdown
# Fix Verification Report

## Vulnerability Reference
- **ID**: [CVE/Internal ID]
- **Severity**: [Critical/High/Medium/Low]
- **Description**: [Brief description]

## Fix Details
- **Commit**: [git commit hash]
- **Files Changed**: [list of files]
- **Approach**: [Description of fix approach]

## Verification Results

### Exploit Reproduction
- [ ] Exploit scenario created: `scenarios/[name].scen.json`
- [ ] Scenario fails on vulnerable code (commit: [hash])
- [ ] Scenario passes on fixed code (commit: [hash])

### Regression Testing
- [ ] All existing tests pass
- [ ] No new warnings from `cargo clippy`
- [ ] Gas costs within acceptable range

### Variant Analysis
- [ ] Searched for similar patterns using `multiversx-variant-analysis`
- [ ] All variants addressed: [list or "none found"]

## Conclusion
**Status**: [VERIFIED / NEEDS WORK / REJECTED]

**Notes**: [Any additional observations]

**Signed**: [Reviewer name, date]
```

## 6. Red Flags During Verification

- Fix is overly complex for the issue
- Fix changes unrelated code
- No test added for the specific vulnerability
- Fix relies on external assumptions
- Gas cost increased significantly
- Access control modified without clear justification


# Fix Verification (Legacy)

---
name: fix_verification
description: Verifying if a reported bug is truly fixed.
---

# Fix Verification

This skill helps you rigorous verify that a reported vulnerability has been eliminated without introducing regressions.

## 1. The Verification Loop
1.  **Reproduce**: Create a `mandos` scenario that fails (demonstrates the bug).
2.  **Apply Fix**: Modification to Rust code.
3.  **Verify**: Run the failing mandos. It MUST pass now.
4.  **Regression Check**: Run ALL other mandos. They MUST still pass.

## 2. Common Fix Failures
- **Partial Fix**: Fixing one path but missing a variant (e.g., fixed `deposit` but not `transfer`).
- **Moved Bug**: The fix prevents the exploit but creates a DoS vector (e.g., adding a lock that never unlocks).

## 3. Deliverable
A "Verification Report" stating:
- Commit ID of the fix.
- Test case used to verify.
- Confirmation of regression suite success.


# Variant Analysis

---
name: multiversx-variant-analysis
description: Multiply audit findings by systematically locating similar vulnerabilities elsewhere in the codebase. Use after finding an initial bug to discover variants, or when creating comprehensive vulnerability reports.
---

# Variant Analysis

Multiply the value of a single vulnerability finding by systematically locating similar issues elsewhere in the codebase. Once you find one bug, this skill helps you find all its "cousins."

## When to Use

- After discovering an initial vulnerability
- During comprehensive security audits
- When creating detection patterns for CI/CD
- Before claiming a bug class is fully remediated
- When assessing the extent of a vulnerability pattern

## 1. The Variant Analysis Process

### From Finding to Pattern

```
1. Find Initial Bug → Specific vulnerability instance
2. Abstract Pattern → What makes this a bug?
3. Create Search    → Grep/Semgrep queries
4. Find Variants    → All similar occurrences
5. Verify Each      → Confirm true positives
6. Report All       → Document the bug class
```

### Example Transformation

**Initial Bug:**
```rust
// Found: Missing payment validation in deposit()
#[payable("*")]
fn deposit(&self) {
    let payment = self.call_value().single_esdt();
    self.balances().update(|b| *b += payment.amount);
    // Bug: No token ID validation!
}
```

**Abstract Pattern:**
- `#[payable("*")]` endpoint
- Uses `call_value()` to get payment
- Does NOT validate `token_identifier`

**Search Query:**
```bash
# Find all payable endpoints
grep -n "#\[payable" src/*.rs

# Then check each for token validation
grep -A 20 "#\[payable" src/*.rs | grep -v "token_identifier"
```

## 2. Common MultiversX Variant Patterns

### Pattern: Missing Payment Validation

**Initial Finding:**
One endpoint accepts payment but doesn't validate the token.

**Variant Search:**
```bash
# Find all payable endpoints
grep -rn "#\[payable" src/

# Check for missing token validation
# Look for call_value() without subsequent token_identifier check
grep -A 30 "#\[payable" src/*.rs > payable_endpoints.txt
# Manually review each for token_identifier validation
```

**Semgrep Rule:**
```yaml
rules:
  - id: mvx-payable-no-token-check
    patterns:
      - pattern: |
          #[payable("*")]
          $ANNOTATIONS
          fn $FUNC(&self, $...PARAMS) {
              $...BODY
          }
      - pattern-not: |
          #[payable("*")]
          $ANNOTATIONS
          fn $FUNC(&self, $...PARAMS) {
              <... token_identifier ...>
          }
```

### Pattern: Unbounded Iteration

**Initial Finding:**
One function iterates over a `VecMapper` without bounds.

**Variant Search:**
```bash
# Find all .iter() calls on storage mappers
grep -rn "\.iter()" src/

# Find all for loops over storage
grep -rn "for.*in.*self\." src/
```

**Checklist for Each:**
- [ ] Is iteration bounded?
- [ ] Can a user grow the collection?
- [ ] Is there pagination?

### Pattern: Callback State Assumptions

**Initial Finding:**
One callback doesn't handle the error case.

**Variant Search:**
```bash
# Find all callbacks
grep -rn "#\[callback\]" src/

# Check for proper result handling
grep -A 20 "#\[callback\]" src/*.rs | grep -c "ManagedAsyncCallResult"
```

**All Callbacks Need:**
```rust
#[callback]
fn any_callback(&self, #[call_result] result: ManagedAsyncCallResult<T>) {
    match result {
        ManagedAsyncCallResult::Ok(_) => { /* success */ },
        ManagedAsyncCallResult::Err(_) => { /* handle failure! */ }
    }
}
```

### Pattern: Missing Access Control

**Initial Finding:**
One admin function lacks `#[only_owner]`.

**Variant Search:**
```bash
# Find functions that modify admin-like storage
grep -rn "admin\|owner\|config\|fee" src/ | grep "\.set("

# Cross-reference with access control
grep -B 10 "admin.*\.set\|config.*\.set" src/*.rs | grep -v "only_owner"
```

### Pattern: Arithmetic Without Checks

**Initial Finding:**
One calculation uses raw `+` instead of `checked_add`.

**Variant Search:**
```bash
# Find all arithmetic operations
grep -rn " + \| - \| \* " src/*.rs

# Exclude test files and comments
grep -rn " + \| - \| \* " src/*.rs | grep -v "test\|//"
```

## 3. Systematic Variant Hunting

### Step 1: Characterize the Bug

Answer these questions:
1. What is the vulnerable code pattern?
2. What makes it exploitable?
3. What would a fix look like?

### Step 2: Create Detection Queries

**Grep-based:**
```bash
# Pattern: [specific code pattern]
grep -rn "[pattern]" src/

# Negative pattern (should be present but isn't)
grep -L "[expected_pattern]" src/*.rs
```

**Semgrep-based:**
```yaml
# See multiversx-semgrep-creator skill for details
rules:
  - id: variant-pattern
    patterns:
      - pattern: <vulnerable pattern>
      - pattern-not: <fixed pattern>
```

### Step 3: Triage Results

For each potential variant:

| Result | Classification | Action |
|--------|----------------|--------|
| Clearly vulnerable | True Positive | Report |
| Needs context | Investigate | Manual review |
| Has mitigation | False Positive | Document why |
| Different pattern | Not a variant | Skip |

### Step 4: Document Findings

```markdown
## Variant Analysis: [Bug Class Name]

### Initial Finding
- Location: [file:line]
- Description: [what's wrong]

### Pattern Description
[Abstract description of what makes this a bug]

### Search Method
```bash
[grep/semgrep commands used]
```

### Variants Found

| Location | Status | Notes |
|----------|--------|-------|
| file1.rs:23 | Confirmed | Same pattern |
| file2.rs:45 | Confirmed | Slight variation |
| file3.rs:67 | FP | Has validation elsewhere |

### Remediation
[How to fix all instances]
```

## 4. Automation for Future Prevention

### Convert to CI/CD Check

After finding variants, create automated detection:

```yaml
# .github/workflows/security.yml
- name: Check for vulnerability patterns
  run: |
    # Run semgrep with custom rules
    semgrep --config rules/mvx-security.yaml src/

    # Grep-based checks
    if grep -rn "unsafe_pattern" src/; then
      echo "Found potential vulnerability"
      exit 1
    fi
```

### Create Semgrep Rule

See `multiversx-semgrep-creator` skill:

```yaml
rules:
  - id: mvx-[bug-class]-[id]
    languages: [rust]
    message: "[Description of bug class]"
    severity: ERROR
    patterns:
      - pattern: <vulnerable pattern>
```

## 5. Variant Analysis Checklist

After finding any bug:

- [ ] Abstract the pattern (what makes it a bug?)
- [ ] Create search queries (grep, semgrep)
- [ ] Search entire codebase
- [ ] Triage each result (TP/FP/needs investigation)
- [ ] Verify true positives are exploitable
- [ ] Document all variants
- [ ] Create prevention rule for CI/CD
- [ ] Recommend fix for all instances

## 6. Common Variant Categories

### Input Validation Variants
- Missing in one endpoint → Check ALL endpoints
- Missing for one parameter → Check ALL parameters

### Access Control Variants
- Missing on one admin function → Check ALL admin functions
- Inconsistent role checks → Audit entire role system

### State Management Variants
- Reentrancy in one function → Check ALL external calls
- Missing callback handling → Check ALL callbacks

### Arithmetic Variants
- Overflow in one calculation → Check ALL math operations
- Precision loss in one formula → Check ALL division operations

## 7. Reporting Multiple Variants

### Consolidated Report

When multiple variants exist, consolidate:

```markdown
# Bug Class: [Name]

## Summary
Found [N] instances of [bug description] across the codebase.

## Root Cause
[Why this pattern is vulnerable]

## Instances

### Instance 1 (file1.rs:23)
[Details]

### Instance 2 (file2.rs:45)
[Details]

...

## Recommended Fix
[Generic fix pattern]

```rust
// Before (vulnerable)
[vulnerable code]

// After (fixed)
[fixed code]
```

## Prevention
[How to prevent this class of bugs in the future]
```

### Severity Aggregation

| Individual Severity | Count | Aggregate Severity |
|---------------------|-------|-------------------|
| Critical | 3+ | Critical |
| High | 5+ | Critical |
| Medium | 10+ | High |
| Low | Any | Low |

## 8. Example: Complete Variant Analysis

**Initial Bug: Missing amount validation in stake()**

```rust
// Found in stake.rs:45
#[payable("EGLD")]
fn stake(&self) {
    let payment = self.call_value().egld_value();
    // Bug: No check for amount > 0
    self.staked().update(|s| *s += payment.clone_value());
}
```

**Pattern: Missing amount > 0 check on payable endpoint**

**Search:**
```bash
grep -rn "#\[payable" src/ | cut -d: -f1 | sort -u | while read file; do
    echo "=== $file ==="
    grep -A 30 "#\[payable" "$file" | head -40
done > payable_review.txt
```

**Variants Found:**
1. `stake.rs:45` - stake() - CONFIRMED
2. `stake.rs:78` - add_stake() - CONFIRMED
3. `rewards.rs:23` - deposit_rewards() - CONFIRMED
4. `fees.rs:12` - pay_fee() - FALSE POSITIVE (has check on line 15)

**Fix Applied to All:**
```rust
#[payable("EGLD")]
fn stake(&self) {
    let payment = self.call_value().egld_value();
    require!(payment.clone_value() > 0, "Amount must be positive");
    self.staked().update(|s| *s += payment.clone_value());
}
```

**CI Rule Created:** `rules/mvx-amount-validation.yaml`


# Variant Analysis (Legacy)

---
name: variant_analysis
description: Finding "variants" of known bugs in other parts of the codebase.
---

# Variant Analysis

This skill helps you multiply the value of a single finding by locating similar vulnerabilities elsewhere.

## 1. The Pivot
Once you find a bug (e.g., "Missing usage of `checked_add` in function A"):
- **Abstract the Pattern**: "Arithmetic operation on user input without checks".
- **Search**: `grep` for other occurrences of the same pattern.

## 2. Common MultiversX Variants
- **Missing Payable Check**:
    - Found: One endpoint accepts payment but doesn't check `call_value()`.
    - Variant Search: Check ALL `#[payable("*")]` endpoints.
- **Unbounded Iteration**:
    - Found: Iterating a `VecMapper` in `compute_reward`.
    - Variant Search: `grep -r "iter()"` on all mappers.
- **Async Callback Revert**:
    - Found: Callback `X` doesn't revert state on failure.
    - Variant Search: Check ALL `#[callback]` functions.

## 3. Automation
- Use `mvx_static_analysis` (Semgrep) to create a temporary rule for the variant.
