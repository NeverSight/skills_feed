---
name: rs-soroban-sdk
description: Expert guidance for building smart contracts on Stellar using the Soroban Rust SDK. Use this skill when working with Soroban smart contracts for tasks including (1) creating new contracts with [contract] and [contractimpl] attributes, (2) implementing storage with Persistent, Temporary, or Instance storage types, (3) working with auth contexts and authorization, (4) handling tokens and Stellar Asset Contracts, (5) writing tests with testutils, (6) deploying contracts, (7) working with events and logging, (8) using crypto functions, (9) debugging contract errors, (10) security best practices and vulnerability prevention, (11) avoiding common security pitfalls like missing authorization, integer overflow, or reinitialization attacks.
---

# Soroban SDK Skill

Soroban SDK is the Rust SDK for building smart contracts on the Stellar blockchain's Wasm-powered Soroban runtime.

## Prerequisites

- **Rust**: v1.84.0 or higher
- **Target**: Install with `rustup target add wasm32v1-none`
- **Stellar CLI**: v25.1.0+ (recommended for building and testing)
  - Install: `curl -fsSL https://github.com/stellar/stellar-cli/raw/main/install.sh | sh`
  - Or: `brew install stellar-cli`

## ⚠️ Security First

Smart contracts handle valuable assets. Follow these rules to prevent vulnerabilities:

**Do:**

- ✅ Call `require_auth()` **before** any state changes
- ✅ Validate all inputs (amounts, addresses, array lengths)
- ✅ Use checked arithmetic (`.checked_add()`, `.checked_mul()`)
- ✅ Extend TTL on all persistent/instance storage writes
- ✅ Initialize contract only once with a guard flag
- ✅ Test authorization, overflow, and edge cases

**Don't:**

- ❌ Skip authorization checks
- ❌ Use unchecked arithmetic (can overflow/underflow)
- ❌ Allow reinitialization
- ❌ Forget to extend TTL on storage writes
- ❌ Trust external addresses without validation

See [references/security.md](references/security.md) for complete security guidance.

## Core Contract Structure

Every Soroban contract follows this pattern:

```rust
#![no_std]  // Required: excludes Rust std library (too large for contracts)

use soroban_sdk::{contract, contractimpl, Env};

#[contract]
pub struct MyContract;

#[contractimpl]
impl MyContract {
    pub fn function_name(env: Env, param: Type) -> ReturnType {
        // Implementation
    }
}
```

**Key requirements:**

- `#![no_std]` - Must be first line (standard library not available)
- All contracts export as a single contract when compiled to WASM
- Function names max 32 characters
- Contract inputs must not be references

**Key attributes:**

- `#[contract]` - Marks the struct as a contract type
- `#[contractimpl]` - Exports public functions as contract functions
- `#[contracttype]` - Converts custom types to/from `Val` for storage
- `#[contracterror]` - Defines error enums with `repr(u32)`
- `#[contractevent]` - Marks structs as publishable events

## Environment (Env)

The `Env` type provides access to the contract execution environment. It's always the first parameter in contract functions.

```rust
pub fn my_function(env: Env) {
    // Access storage
    env.storage().persistent();
    env.storage().temporary();
    env.storage().instance();

    // Get contract address
    let contract_id = env.current_contract_address();

    // Get ledger info
    let ledger = env.ledger().sequence();
    let timestamp = env.ledger().timestamp();
}
```

## Storage Types

Soroban provides three storage types with different lifetimes and costs. See [references/storage.md](references/storage.md) for detailed patterns.

**Quick reference:**

- `Persistent` - Long-lived data (user balances, state)
- `Temporary` - Short-lived data (caching, temporary locks)
- `Instance` - Contract-wide configuration/metadata

## Data Types

### Core Types

- `Address` - Universal identifier (contracts or accounts)
- `Symbol` - Short strings with limited charset (max 32 chars)
- `Vec<T>` - Growable array type
- `Map<K, V>` - Ordered key-value dictionary
- `Bytes` - Growable byte array
- `BytesN<N>` - Fixed-size byte array
- `String` - UTF-8 string type
- `U256`, `I256` - 256-bit integers

### Type Macros

- `vec![&env, item1, item2]` - Create Vec
- `map![&env, (key1, val1), (key2, val2)]` - Create Map
- `symbol_short!("text")` - Create Symbol constant
- `bytes!(&env, 0x010203)` - Create Bytes
- `bytesn!(&env, 0x010203)` - Create BytesN

## Authorization

⚠️ **Critical**: Authorization vulnerabilities are the #1 cause of smart contract exploits. Always call `require_auth()` **before** any state changes.

When a function requires authorization, use `Address::require_auth()`:

```rust
pub fn transfer(env: Env, from: Address, to: Address, amount: i128) {
    from.require_auth();  // ✅ ALWAYS FIRST
    // Now authorized to proceed
}
```

**Common mistake**: Authorizing the wrong address

```rust
// ❌ WRONG: Authorizing recipient
pub fn transfer(env: Env, from: Address, to: Address, amount: i128) {
    to.require_auth();  // Anyone can receive!
}

// ✅ CORRECT: Authorize sender
pub fn transfer(env: Env, from: Address, to: Address, amount: i128) {
    from.require_auth();  // Sender must approve
}
```

For custom auth logic, see [references/auth.md](references/auth.md).

## Testing

Use `testutils` feature for testing. Tests use `Env::default()` and register contracts:

```rust
#[test]
fn test() {
    let env = Env::default();
    let contract_id = env.register(MyContract, ());
    let client = MyContractClient::new(&env, &contract_id);

    let result = client.my_function(&param);
    assert_eq!(result, expected);
}
```

For advanced testing patterns, see [references/testing.md](references/testing.md).

## Tokens

Work with tokens using the `token` module:

```rust
use soroban_sdk::token::{TokenClient, StellarAssetClient};

pub fn use_token(env: Env, token_address: Address, amount: i128) {
    let token = TokenClient::new(&env, &token_address);
    token.transfer(&from, &to, &amount);
}
```

See [references/tokens.md](references/tokens.md) for token integration patterns.

## Events and Logging

Publish events for off-chain tracking:

```rust
env.events().publish((symbol_short!("transfer"), from, to), amount);
```

During development, use logging:

```rust
use soroban_sdk::log;
log!(&env, "Debug message: {}", value);
```

## Error Handling

Define custom errors with `#[contracterror]`:

```rust
#[contracterror]
#[derive(Copy, Clone, Debug, Eq, PartialEq)]
#[repr(u32)]
pub enum Error {
    InvalidAmount = 1,
    Unauthorized = 2,
    InsufficientBalance = 3,
}
```

Use with `panic_with_error!` or `assert_with_error!`:

```rust
// Validate before operations
assert_with_error!(&env, amount > 0, Error::InvalidAmount);
assert_with_error!(&env, balance >= amount, Error::InsufficientBalance);

// Or panic directly
if amount == 0 {
    panic_with_error!(&env, Error::InvalidAmount);
}
```

⚠️ **Security**: Always validate inputs to prevent:

- Integer overflow/underflow (use checked arithmetic)
- Invalid addresses or amounts
- Array length mismatches
- Division by zero

## Deployment

Contracts can deploy other contracts:

```rust
use soroban_sdk::deploy::{Deployer, ContractIdPreimage};

let deployer = env.deployer();
let contract_id = deployer.deploy_wasm(&wasm_hash, &salt);
```

## Common Patterns

### State Management

Store contract state in Instance storage for contract-wide config:

```rust
const STATE_KEY: Symbol = symbol_short!("STATE");

pub fn init(env: Env, admin: Address) {
    env.storage().instance().set(&STATE_KEY, &admin);
}

pub fn get_admin(env: Env) -> Address {
    env.storage().instance().get(&STATE_KEY).unwrap()
}
```

### Iterating Over Collections

Use iterator methods on Vec and Map:

```rust
let total: i128 = amounts
    .iter()
    .map(|x| x.unwrap())
    .sum();
```

### Cross-Contract Calls

Import contracts with `contractimport!` or create manual clients:

```rust
let other_contract = OtherContractClient::new(&env, &contract_address);
let result = other_contract.function(&args);
```

## Project Setup

### Requirements

- Rust toolchain **v1.84.0 or higher** (required for `wasm32v1-none` target)
- Stellar CLI v25.1.0 or higher
- Install target: `rustup target add wasm32v1-none`

### Cargo.toml Configuration

Workspace-level Cargo.toml:

```toml
[workspace]
resolver = "2"
members = ["contracts/*"]

[workspace.dependencies]
soroban-sdk = "25"

[profile.release]
opt-level = "z"
overflow-checks = true
debug = 0
strip = "symbols"
debug-assertions = false
panic = "abort"
codegen-units = 1
lto = true

[profile.release-with-logs]
inherits = "release"
debug-assertions = true
```

Contract-level Cargo.toml:

```toml
[package]
name = "my-contract"
version = "0.0.0"
edition = "2021"

[lib]
crate-type = ["cdylib"]
doctest = false

[dependencies]
soroban-sdk = { workspace = true }

[dev-dependencies]
soroban-sdk = { workspace = true, features = ["testutils"] }
```

### Building Contracts

**Recommended**: Use Stellar CLI (automatically sets correct target and profile):

```bash
stellar contract build
```

**Equivalent manual command**:

```bash
cargo build --target wasm32v1-none --release
```

Output: `target/wasm32v1-none/release/contract_name.wasm`

**Optimize for production**:

```bash
stellar contract optimize --wasm target/wasm32v1-none/release/contract_name.wasm
```

Produces: `contract_name.optimized.wasm`

## Additional Resources

For detailed information on specific topics, see:

- [Storage patterns and TTL management](references/storage.md)
- [Authorization and auth context](references/auth.md)
- [Testing strategies and utilities](references/testing.md)
- [Token integration and Stellar Asset Contracts](references/tokens.md)
- [Common contract patterns and examples](references/patterns.md)
- **[Security best practices and vulnerabilities](references/security.md)** ⚠️ CRITICAL

Official documentation: https://developers.stellar.org/docs/build/smart-contracts

## Security Quick Reference

**Critical rules to prevent vulnerabilities:**

1. ✅ **Always authorize first**: Call `require_auth()` before any state changes
2. ✅ **Validate all inputs**: Check amounts, addresses, array lengths
3. ✅ **Prevent overflow**: Use checked arithmetic for all math operations
4. ✅ **Initialize once**: Use initialization flag to prevent reinitialization
5. ✅ **Extend TTL**: Always extend TTL on persistent/instance storage writes
6. ✅ **Choose storage wisely**: Persistent for critical data, Temporary for cache
7. ✅ **Test thoroughly**: Cover authorization, overflows, edge cases

See [references/security.md](references/security.md) for complete security guidance.
