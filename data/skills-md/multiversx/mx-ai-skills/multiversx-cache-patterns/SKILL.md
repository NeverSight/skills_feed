---
name: multiversx-cache-patterns
description: Gas-optimized cache patterns for MultiversX smart contracts using Drop-based write-back caches. Use when building contracts that read/write multiple storage values per transaction, DeFi protocols, or any gas-sensitive contract.
---

# MultiversX Cache Patterns

## Why Cache?
- Storage reads/writes are the most expensive operations in MultiversX smart contracts
- A single endpoint that reads 5 storage values and writes 3 back costs 8 storage operations
- With a cache: 5 reads on entry + 3 writes on exit = same, BUT intermediate reads within the function are FREE (in-memory)

## Pattern 1: Write-Back Cache with Drop Trait

The core pattern: load state into a struct on entry, mutate in memory, commit on scope exit via `Drop`.

```rust
multiversx_sc::imports!();
use multiversx_sc::derive_imports::*;

pub struct StorageCache<'a, C>
where
    C: crate::storage::StorageModule,
{
    sc_ref: &'a C,
    pub field_a: BigUint<C::Api>,
    pub field_b: BigUint<C::Api>,
    pub field_c: BigUint<C::Api>,
}

impl<'a, C> StorageCache<'a, C>
where
    C: crate::storage::StorageModule,
{
    pub fn new(sc_ref: &'a C) -> Self {
        StorageCache {
            field_a: sc_ref.field_a().get(),
            field_b: sc_ref.field_b().get(),
            field_c: sc_ref.field_c().get(),
            sc_ref,
        }
    }
}

impl<C> Drop for StorageCache<'_, C>
where
    C: crate::storage::StorageModule,
{
    fn drop(&mut self) {
        // Commit ALL mutable fields back to storage
        self.sc_ref.field_a().set(&self.field_a);
        self.sc_ref.field_b().set(&self.field_b);
        self.sc_ref.field_c().set(&self.field_c);
    }
}
```

### Usage in Endpoints

```rust
#[endpoint]
fn deposit(&self) {
    let payment = self.call_value().single();
    let mut cache = StorageCache::new(self);

    // All reads/writes are in-memory - FREE after initial load
    cache.field_a += payment.amount.as_big_uint();
    cache.field_b += &self.calculate_shares(&cache, payment.amount.as_big_uint());

    // cache.drop() called automatically here - writes to storage
}
```

## Pattern 2: Read-Only Cache (No Drop)

For view functions or read-heavy operations where you don't need write-back:

```rust
pub struct ReadCache<'a, C: crate::storage::StorageModule> {
    sc_ref: &'a C,
    pub total_supply: BigUint<C::Api>,
    pub total_reserve: BigUint<C::Api>,
    pub config_params: YourConfigType<C::Api>,
}

impl<'a, C: crate::storage::StorageModule> ReadCache<'a, C> {
    pub fn new(sc_ref: &'a C) -> Self {
        ReadCache {
            total_supply: sc_ref.total_supply().get(),
            total_reserve: sc_ref.total_reserve().get(),
            config_params: sc_ref.config_params().get(),
            sc_ref,
        }
    }
    // No Drop impl - nothing written back
}
```

## Pattern 3: Cache with Computed Methods

When your cache needs derived values computed from the cached fields, add methods directly on the cache struct:

```rust
pub struct StateCache<'a, C>
where
    C: crate::storage::StorageModule + crate::math::MathModule,
{
    sc_ref: &'a C,
    pub total_deposited: BigUint<C::Api>,
    pub total_shares: BigUint<C::Api>,
    pub fee_rate_bps: u64,
}

impl<C> StateCache<'_, C>
where
    C: crate::storage::StorageModule + crate::math::MathModule,
{
    /// Computed from cached fields — no extra storage reads
    pub fn exchange_rate(&self) -> BigUint<C::Api> {
        if self.total_shares == 0u64 {
            return BigUint::from(1u64);
        }
        &self.total_deposited / &self.total_shares
    }

    /// Compute using both cached data and the contract's math module
    pub fn calculate_fee(&self, amount: &BigUint<C::Api>) -> BigUint<C::Api> {
        (amount * self.fee_rate_bps) / 10_000u64
    }
}
```

**Key insight**: The cache can hold a reference to the contract (`sc_ref`) and call its module methods. This lets you compute derived values using both cached fields and shared math traits — without additional storage reads.

## Selective Write-Back

When only some fields are mutable, avoid writing back unchanged fields:

```rust
impl<C> Drop for StorageCache<'_, C>
where
    C: crate::storage::StorageModule,
{
    fn drop(&mut self) {
        // Only write back fields that can change
        self.sc_ref.balance().set(&self.balance);
        self.sc_ref.total_shares().set(&self.total_shares);
        // DON'T write back: self.config_params (read-only, never changes in this context)
    }
}
```

## When to Use vs Direct Storage

| Scenario | Approach |
|---|---|
| Endpoint reads 3+ storage values | Use cache |
| Single storage read/write | Direct access is fine |
| View function reading multiple values | Read-only cache (no Drop) |
| Multiple endpoints share same state | Create shared cache struct |
| Async call boundary | Manually drop cache BEFORE async call |

## Anti-Patterns

### 1. Caching Across Async Boundaries
```rust
// WRONG - async_call_and_exit() terminates execution, drop() never runs!
// Cached writes are LOST, not stale.
fn bad_async(&self) {
    let mut cache = StorageCache::new(self);
    cache.balance += &deposit;

    // This terminates execution — cache.drop() NEVER fires!
    self.tx().to(&other).typed(Proxy).call()
        .callback(self.callbacks().on_done())
        .async_call_and_exit();
    // cache is never dropped — balance change is lost!
}

// CORRECT - manually drop cache before async call
fn good_async(&self) {
    let deposit = self.call_value().egld_value().clone_value();

    {
        let mut cache = StorageCache::new(self);
        cache.balance += &deposit;
        // cache.drop() fires here at end of scope — writes committed
    }

    // Now safe to make async call
    self.tx().to(&other).typed(Proxy).call()
        .callback(self.callbacks().on_done())
        .async_call_and_exit();
}
```

### Bad — Holding Cache Across Async Boundary
```rust
// DON'T: Cache is never dropped — writes are silently lost
fn bad(&self) {
    let mut cache = StorageCache::new(self);
    cache.balance += &amount;
    self.tx().to(&other).typed(Proxy).call()
        .callback(self.callbacks().on_done())
        .async_call_and_exit(); // Execution stops — drop() never runs!
}
```

### Good — Clone/Scope Before Async
```rust
// DO: Scope the cache so drop() fires before the async call
fn good(&self) {
    {
        let mut cache = StorageCache::new(self);
        cache.balance += &amount;
    } // drop() fires here — writes committed to storage

    self.tx().to(&other).typed(Proxy).call()
        .callback(self.callbacks().on_done())
        .async_call_and_exit();
}
```

### 2. Forgetting Fields in Drop
```rust
// WRONG - forgot to write back field_c
impl<C> Drop for StorageCache<'_, C> {
    fn drop(&mut self) {
        self.sc_ref.field_a().set(&self.field_a);
        self.sc_ref.field_b().set(&self.field_b);
        // BUG: field_c changes are lost!
    }
}
```

### 3. Writing Back Immutable Config
```rust
// WRONG - config rarely changes, don't write it back every time
impl<C> Drop for Cache<'_, C> {
    fn drop(&mut self) {
        self.sc_ref.config_params().set(&self.config_params); // Unnecessary write!
    }
}
```

## Template: Starter Cache

```rust
multiversx_sc::imports!();
use multiversx_sc::derive_imports::*;

pub struct StorageCache<'a, C>
where
    C: crate::storage::StorageModule,
{
    sc_ref: &'a C,
    // Add your cached fields here
    pub field_a: BigUint<C::Api>,
    pub field_b: BigUint<C::Api>,
}

impl<'a, C> StorageCache<'a, C>
where
    C: crate::storage::StorageModule,
{
    pub fn new(sc_ref: &'a C) -> Self {
        StorageCache {
            field_a: sc_ref.field_a().get(),
            field_b: sc_ref.field_b().get(),
            sc_ref,
        }
    }
}

impl<C> Drop for StorageCache<'_, C>
where
    C: crate::storage::StorageModule,
{
    fn drop(&mut self) {
        self.sc_ref.field_a().set(&self.field_a);
        self.sc_ref.field_b().set(&self.field_b);
    }
}
```
