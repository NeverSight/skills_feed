---
name: multiversx-cross-contract-storage
description: Read another contract's storage directly without async calls using storage_mapper_from_address. Use when building aggregators, controllers, or any contract that needs to read state from other same-shard contracts without proxy call overhead.
---

# MultiversX Cross-Contract Storage Reads

> **Note**: This skill uses `TokenIdentifier` (ESDT-only alias). For unified EGLD+ESDT identifiers, use `TokenId`.

Read another contract's storage mappers directly — zero gas overhead from proxy calls, no async complexity.

## What Problem Does This Solve?

When your contract needs to read state from another same-shard contract, you have two options:
1. **Proxy call** — executes a view on the target, costs execution gas, requires ABI knowledge
2. **Direct storage read** — reads the raw storage key, costs only a storage read, requires knowing the key name

`storage_mapper_from_address` gives you option 2.

## When to Use

| Criteria | `storage_mapper_from_address` | Proxy Call |
|---|---|---|
| Same shard only | Yes (required) | Works cross-shard |
| Read-only | Yes | Read + Write |
| Needs computation on target | No | Yes |
| Gas cost | ~storage read cost | ~execution + storage |
| Requires knowing storage keys | Yes | No (uses ABI) |
| Data freshness | Current block state | Current block state |

## Core Pattern

```rust
#[multiversx_sc::module]
pub trait ExternalStorageModule {
    // Read a simple value from another contract
    #[storage_mapper_from_address("total_supply")]
    fn external_total_supply(
        &self,
        contract_address: ManagedAddress,
    ) -> SingleValueMapper<BigUint, ManagedAddress>;

    // Read a value with a composite key (token-specific balance)
    #[storage_mapper_from_address("balance")]
    fn external_balance(
        &self,
        contract_address: ManagedAddress,
        token_id: &TokenIdentifier,
    ) -> SingleValueMapper<BigUint, ManagedAddress>;

    // Read a boolean flag (module-prefixed key)
    #[storage_mapper_from_address("pause_module:paused")]
    fn external_paused(
        &self,
        contract_address: ManagedAddress,
    ) -> SingleValueMapper<bool, ManagedAddress>;
}
```

### Key Syntax Rules

1. The string in `#[storage_mapper_from_address("key")]` must EXACTLY match the storage key in the target contract
2. First parameter must be `ManagedAddress` — the target contract address
3. Return type's second generic must be `ManagedAddress` (e.g., `SingleValueMapper<BigUint, ManagedAddress>`)
4. Additional parameters after the address become part of the composite storage key (same as normal storage mappers with parameters)

## Generic Examples

### Example 1: Reading a Token Balance
```rust
#[storage_mapper_from_address("balance")]
fn external_token_balance(
    &self,
    contract_address: ManagedAddress,
    token_id: &TokenIdentifier,
) -> SingleValueMapper<BigUint, ManagedAddress>;

fn get_external_balance(&self, addr: &ManagedAddress, token: &TokenIdentifier) -> BigUint {
    let mapper = self.external_token_balance(addr.clone(), token);
    if mapper.is_empty() { BigUint::zero() } else { mapper.get() }
}
```

### Example 2: Reading a Config Flag
```rust
#[storage_mapper_from_address("is_active")]
fn external_is_active(
    &self,
    contract_address: ManagedAddress,
) -> SingleValueMapper<bool, ManagedAddress>;
```

### Example 3: Reading a Composite Key (Multi-Parameter)
```rust
// Target contract has: #[storage_mapper("rate")] fn rate(&self, asset: &TokenIdentifier, tier: u32) -> ...
#[storage_mapper_from_address("rate")]
fn external_rate(
    &self,
    contract_address: ManagedAddress,
    asset: &TokenIdentifier,
    tier: u32,
) -> SingleValueMapper<BigUint, ManagedAddress>;
```

## How to Discover Storage Keys

1. **Read the source code**: Look for `#[storage_mapper("key")]` in the target contract
2. **Check the ABI**: The `.abi.json` file lists all storage keys
3. **Composite keys**: Storage mappers with parameters encode the key as `key` + nested-encoded parameters
4. **Module keys**: Some modules use prefixed keys like `pause_module:paused`

## Security Considerations

### 1. Same-Shard Only
`storage_mapper_from_address` only works when both contracts are on the SAME shard. Cross-shard reads return empty/default values silently — no error!

```rust
// DANGER: If target_address is on a different shard, this returns 0 silently
let value = self.external_total_supply(target_address).get();
```

### 2. Stale Data Awareness
The data is as fresh as the current block. But if the target contract hasn't been called this block, its state reflects the last block it was active.

### 3. Storage Key Collisions
If the target contract changes its storage key names in an upgrade, your reads will break silently (return defaults).

### 4. No Write Access
This pattern is READ-ONLY. You cannot write to another contract's storage.

## Anti-Patterns

### 1. Not Validating Empty Results
```rust
// WRONG — if the key doesn't exist, you get a default (0, false, empty)
let value = self.external_balance(addr, &token).get();

// CORRECT — check if the mapper has a value
let mapper = self.external_balance(addr, &token);
require!(!mapper.is_empty(), "External value not set");
let value = mapper.get();
```

### 2. Assuming Cross-Shard Works
```rust
// WRONG — no validation
let balance = self.external_balance(unknown_address, &token).get();

// CORRECT — validate shard first
let my_shard = self.blockchain().get_shard_of_address(&self.blockchain().get_sc_address());
let target_shard = self.blockchain().get_shard_of_address(&target_address);
require!(my_shard == target_shard, "Cross-shard read not supported");
```

## Template

```rust
multiversx_sc::imports!();

#[multiversx_sc::module]
pub trait ExternalStorageModule {
    // Define one mapper per external storage key you need
    #[storage_mapper_from_address("storage_key_name")]
    fn external_value(
        &self,
        contract_address: ManagedAddress,
    ) -> SingleValueMapper<YourType, ManagedAddress>;

    // Helper to read with validation
    fn read_external_value(&self, addr: &ManagedAddress) -> YourType {
        let mapper = self.external_value(addr.clone());
        require!(!mapper.is_empty(), "External value not set");
        mapper.get()
    }
}
```
