---
name: multiversx-sharp-edges
description: Catalog of non-obvious behaviors, gotchas, and platform-specific quirks in MultiversX that often lead to bugs. Use when debugging unexpected behavior, reviewing code for subtle issues, or learning platform-specific pitfalls.
---

# MultiversX Sharp Edges

A catalog of non-obvious behaviors, "gotchas," and platform-specific quirks that frequently lead to bugs in MultiversX smart contracts and dApps. Understanding these sharp edges is essential for writing correct code.

## When to Use

- Debugging unexpected contract behavior
- Reviewing code for subtle platform-specific issues
- Onboarding to MultiversX development
- Checking if a bug might be caused by a known quirk
- Preparing for security audits

## 1. Async Callbacks & Reverts

### The Sharp Edge
When an async call fails, the `#[callback]` is still executed, but state changes from the original transaction are **NOT automatically reverted**.

### The Problem
```rust
#[endpoint]
fn transfer_and_update(&self, recipient: ManagedAddress, amount: BigUint) {
    // State change happens IMMEDIATELY
    self.total_sent().update(|t| *t += &amount);

    // Async call to another contract
    self.tx()
        .to(&recipient)
        .egld(&amount)
        .callback(self.callbacks().on_transfer())
        .async_call_and_exit();
}

#[callback]
fn on_transfer(&self) {
    // If transfer FAILED, total_sent is STILL updated!
    // This is inconsistent state!
}
```

### The Solution
```rust
#[endpoint]
fn transfer_and_update(&self, recipient: ManagedAddress, amount: BigUint) {
    // DON'T update state before async call
    self.tx()
        .to(&recipient)
        .egld(&amount)
        .callback(self.callbacks().on_transfer(amount.clone()))
        .async_call_and_exit();
}

#[callback]
fn on_transfer(&self, amount: BigUint, #[call_result] result: ManagedAsyncCallResult<()>) {
    match result {
        ManagedAsyncCallResult::Ok(_) => {
            // Only update state on SUCCESS
            self.total_sent().update(|t| *t += &amount);
        },
        ManagedAsyncCallResult::Err(_) => {
            // Handle failure explicitly
            // Funds return to contract automatically
        }
    }
}
```

## 2. Gas Limits & Out of Gas (OOG)

### The Sharp Edge
OOG can leave cross-shard transactions in partial states.

### Cross-Shard OOG Scenario
```
1. Sender shard processes transaction (state changed)
2. Receiver shard runs out of gas
3. Receiver execution fails
4. Sender state changes PERSIST
5. Callback triggered with error
```

### The Solution
```rust
// Always reserve enough gas for callbacks
const CALLBACK_GAS: u64 = 10_000_000;

#[endpoint]
fn safe_cross_shard(&self) {
    self.tx()
        .to(&other_contract)
        .typed(proxy::Proxy)
        .function()
        .with_gas_limit(50_000_000)
        .callback(self.callbacks().handle_result())
        .with_extra_gas_for_callback(CALLBACK_GAS)
        .async_call_and_exit();
}
```

## 3. Storage Mappers vs Rust Types

### The Sharp Edge
`VecMapper` is NOT a `Vec`. They have fundamentally different memory models.

### The Problem
```rust
// VecMapper: Each element is a separate storage slot
// Accessing element = 1 storage read
// Iterating N elements = N storage reads
#[storage_mapper("users")]
fn users(&self) -> VecMapper<ManagedAddress>;

// If you load into a Vec, you load EVERYTHING into WASM memory
fn bad_function(&self) {
    let all_users: Vec<ManagedAddress> = self.users().iter().collect();
    // With 10,000 users = 10,000 storage reads + massive memory allocation
    // WILL run out of gas
}
```

### The Solution
```rust
// Paginate operations
fn process_users_paginated(&self, start: usize, count: usize) {
    let len = self.users().len();
    let end = (start + count).min(len);

    for i in start..end {
        let user = self.users().get(i + 1);  // VecMapper is 1-indexed!
        self.process_user(&user);
    }
}

// Or use appropriate mapper for the use case
// SetMapper for O(1) contains checks
// UnorderedSetMapper for efficient removal
```

## 4. Token Decimal Precision

### The Sharp Edge
ESDTs can have 0-18 decimals. Hardcoding decimal assumptions breaks contracts.

### The Problem
```rust
// WRONG: Assumes 18 decimals
fn convert_to_usd(&self, token_amount: BigUint) -> BigUint {
    let price = self.price().get();  // Price in 10^18
    &token_amount * &price / BigUint::from(10u64.pow(18))  // Assumes 18 decimals!
}
```

### The Solution
```rust
fn convert_to_usd(&self, token_amount: BigUint, token_decimals: u8) -> BigUint {
    let price = self.price().get();
    let decimal_factor = BigUint::from(10u64).pow(token_decimals as u32);
    &token_amount * &price / &decimal_factor
}

// Or require specific decimals
fn require_standard_decimals(&self, token_id: &TokenIdentifier) {
    let properties = self.blockchain().get_esdt_token_data(
        &self.blockchain().get_sc_address(),
        token_id,
        0
    );
    require!(properties.decimals == 18, "Token must have 18 decimals");
}
```

## 5. Upgradeability Pitfalls

### The Sharp Edge
`#[init]` is NOT called on upgrade. Only `#[upgrade]` runs.

### The Problem
```rust
// V1 contract
#[init]
fn init(&self) {
    self.version().set(1);
}

// V2 contract - added new storage
#[init]
fn init(&self) {
    self.version().set(2);
    self.new_feature_enabled().set(true);  // NEVER RUNS ON UPGRADE!
}

// After upgrade: version is still 1, new_feature_enabled is empty!
```

### The Solution
```rust
#[upgrade]
fn upgrade(&self) {
    // Initialize new storage here
    self.version().set(2);
    self.new_feature_enabled().set(true);

    // Migrate existing data if needed
    self.migrate_storage();
}
```

### Storage Layout Changes

**NEVER reorder struct fields:**
```rust
// V1
struct UserData {
    balance: BigUint,    // Encoded at position 0
    timestamp: u64,      // Encoded at position 1
}

// V2 - BREAKS EXISTING DATA
struct UserData {
    timestamp: u64,      // Now at position 0 - reads old balance bytes!
    balance: BigUint,    // Now at position 1 - reads old timestamp bytes!
    new_field: bool,     // This is fine (appended)
}
```

## 6. Block Info in Views

### The Sharp Edge
`get_block_timestamp()` and similar in `#[view]` functions may return different values off-chain vs on-chain.

### The Problem
```rust
#[view(isExpired)]
fn is_expired(&self) -> bool {
    let deadline = self.deadline().get();
    let current_time = self.blockchain().get_block_timestamp();
    // Off-chain simulation may return 0 or stale value!
    current_time > deadline
}
```

### The Solution
```rust
// Option 1: Don't rely on block info in views
#[view(getDeadline)]
fn get_deadline(&self) -> u64 {
    self.deadline().get()
    // Let client compare with their known current time
}

// Option 2: Accept timestamp as parameter for queries
#[view(isExpiredAt)]
fn is_expired_at(&self, check_time: u64) -> bool {
    let deadline = self.deadline().get();
    check_time > deadline
}
```

## 7. VecMapper Indexing

### The Sharp Edge
`VecMapper` is **1-indexed**, not 0-indexed like Rust `Vec`.

### The Problem
```rust
fn get_first_user(&self) -> ManagedAddress {
    self.users().get(0)  // PANIC! Index 0 doesn't exist
}
```

### The Solution
```rust
fn get_first_user(&self) -> ManagedAddress {
    require!(!self.users().is_empty(), "No users");
    self.users().get(1)  // First element is at index 1
}

fn iterate_users(&self) {
    for i in 1..=self.users().len() {  // 1 to len, inclusive
        let user = self.users().get(i);
        // process user
    }
}
```

## 8. EGLD vs ESDT Transfer Limitations

### The Sharp Edge
You cannot send EGLD and ESDT in the same transaction.

### The Problem
```rust
// This is IMPOSSIBLE on MultiversX
self.tx()
    .to(&recipient)
    .egld(&egld_amount)
    .single_esdt(&token_id, 0, &esdt_amount)  // Can't combine!
    .transfer();
```

### The Solution
```rust
// Separate transactions
self.tx().to(&recipient).egld(&egld_amount).transfer();
self.tx().to(&recipient).single_esdt(&token_id, 0, &esdt_amount).transfer();

// Or design around the limitation
// e.g., use wrapped EGLD (WEGLD) as ESDT
```

## 9. MapMapper Memory Model

### The Sharp Edge
`MapMapper` stores `4*N + 1` storage entries, making it very expensive.

### The Problem
```rust
// For 1000 users, this creates 4001 storage entries!
#[storage_mapper("balances")]
fn balances(&self) -> MapMapper<ManagedAddress, BigUint>;
```

### The Solution
```rust
// Use SingleValueMapper with address key when you don't need to iterate
#[storage_mapper("balance")]
fn balance(&self, user: &ManagedAddress) -> SingleValueMapper<BigUint>;

// Only use MapMapper when you MUST iterate over all entries
```

## 10. Require vs SC Panic

### The Sharp Edge
`require!` generates larger WASM than `sc_panic!` when the message is dynamic.

### The Problem
```rust
// Each unique string increases WASM size
require!(condition1, "Error message one");
require!(condition2, "Error message two");
require!(condition3, "Error message three");
```

### The Solution
```rust
// Use static error constants
const ERR_INVALID_AMOUNT: &str = "Invalid amount";
const ERR_UNAUTHORIZED: &str = "Unauthorized";

require!(amount > 0, ERR_INVALID_AMOUNT);
require!(caller == owner, ERR_UNAUTHORIZED);

// Reuse same constant for same error type
require!(amount1 > 0, ERR_INVALID_AMOUNT);
require!(amount2 > 0, ERR_INVALID_AMOUNT);
```

## Quick Reference: Common Gotchas

| Issue | Wrong | Right |
|-------|-------|-------|
| VecMapper index | `.get(0)` | `.get(1)` |
| Callback state | Update before async | Update in callback on success |
| Upgrade init | Rely on `#[init]` | Use `#[upgrade]` |
| Decimals | Hardcode `10^18` | Fetch from token properties |
| MapMapper | Use for per-user data | Use SingleValueMapper with key |
| Block info in view | Direct use | Pass as parameter |
| EGLD + ESDT | Same transaction | Separate transactions |
| Struct fields | Reorder | Only append |
