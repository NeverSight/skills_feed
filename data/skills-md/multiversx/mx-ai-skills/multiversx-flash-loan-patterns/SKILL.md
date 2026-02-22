---
name: multiversx-flash-loan-patterns
description: Atomic lend-execute-verify pattern for MultiversX smart contracts. Use when building flash loans, atomic swaps, temporary grants, or any operation that lends assets, executes a callback, and verifies repayment within a single transaction.
---

# MultiversX Atomic Lend-Execute-Verify Pattern

A pattern for operations that temporarily lend assets, execute an external callback, and verify repayment — all atomically within a single transaction.

## What Problem Does This Solve?

You want to lend tokens to a contract, let it execute arbitrary logic, and guarantee repayment (plus fee) before the transaction completes. If repayment fails, the entire transaction reverts.

## When to Use

| Scenario | Use This Pattern? |
|---|---|
| Flash loans | Yes — the canonical use case |
| Atomic swaps with verification | Yes — send tokens, verify counterparty sent back |
| Temporary grants (execute-then-return) | Yes — lend tokens for computation, verify return |
| Cross-shard operations | No — atomicity requires same-shard |
| Simple transfers | No — overkill |

## Security Checklist

1. **Reentrancy guard** — prevent nested operations
2. **Shard validation** — caller must be same shard (atomicity requirement)
3. **Endpoint validation** — callback must not be a built-in function
4. **Repayment verification** — check contract balance after callback
5. **Guard cleanup** — always clear the reentrancy flag

## Core Flow: Guard → Send → Execute → Verify → Clear

```rust
#[endpoint(atomicOperation)]
fn atomic_operation(
    &self,
    asset: TokenId,
    amount: BigUint,
    target_contract: ManagedAddress,
    callback_endpoint: ManagedBuffer,
) {
    // 1. Reentrancy guard
    self.require_not_ongoing();

    // 2. Shard validation (atomicity requires same shard)
    self.require_same_shard(&target_contract);

    // 3. Endpoint validation
    self.require_valid_endpoint(&callback_endpoint);

    // 4. Calculate expected repayment
    let fee = &amount * self.fee_bps().get() / 10_000u64;
    let balance_before = self.blockchain().get_sc_balance(&asset.clone().into(), 0);

    // 5. Set guard
    self.operation_ongoing().set(true);

    // 6. Send tokens and call target
    self.tx()
        .to(&target_contract)
        .raw_call(callback_endpoint)
        .single_esdt(&asset, 0, &amount)
        .sync_call();

    // 7. Verify repayment
    let balance_after = self.blockchain().get_sc_balance(&asset.into(), 0);
    require!(
        balance_after >= balance_before + &fee,
        "Repayment insufficient"
    );

    // 8. Clear guard
    self.operation_ongoing().set(false);
}
```

## Reentrancy Guard

```rust
#[storage_mapper("operationOngoing")]
fn operation_ongoing(&self) -> SingleValueMapper<bool>;

fn require_not_ongoing(&self) {
    require!(
        !self.operation_ongoing().get(),
        "Operation already in progress"
    );
}
```

**Why**: Without this, a malicious callback could re-enter the operation endpoint, creating nested operations that bypass repayment checks.

## Shard Validation

```rust
fn require_same_shard(&self, target_address: &ManagedAddress) {
    let target_shard = self.blockchain().get_shard_of_address(target_address);
    let contract_shard = self.blockchain().get_shard_of_address(
        &self.blockchain().get_sc_address()
    );
    require!(
        target_shard == contract_shard,
        "Target must be on same shard"
    );
}
```

**Why**: Cross-shard calls execute in different blocks/rounds, breaking atomicity. The callback would run in a separate transaction, allowing manipulation between the send and verification.

## Endpoint Validation

```rust
fn require_valid_endpoint(&self, endpoint: &ManagedBuffer<Self::Api>) {
    require!(
        !endpoint.is_empty() && !self.blockchain().is_builtin_function(endpoint),
        "Invalid callback endpoint"
    );
}
```

**Why**: Built-in functions (token transfers, ESDT operations) could redirect tokens without executing the expected callback, bypassing repayment logic.

## Reentrancy Guard Examples

### Bad
```rust
// DON'T: No reentrancy guard — malicious callback re-enters and borrows again
#[endpoint(flashLoan)]
fn flash_loan(&self, asset: TokenId, amount: BigUint, target: ManagedAddress) {
    let balance_before = self.blockchain().get_sc_balance(&asset.clone().into(), 0);
    self.tx().to(&target).raw_call("execute").single_esdt(&asset, 0, &amount).sync_call();
    let balance_after = self.blockchain().get_sc_balance(&asset.into(), 0);
    require!(balance_after >= balance_before, "Not repaid"); // Bypassed by re-entry!
}
```

### Good
```rust
// DO: Set reentrancy guard before send, clear after verification
#[endpoint(flashLoan)]
fn flash_loan(&self, asset: TokenId, amount: BigUint, target: ManagedAddress) {
    self.require_not_ongoing(); // Blocks nested calls
    self.operation_ongoing().set(true);

    let balance_before = self.blockchain().get_sc_balance(&asset.clone().into(), 0);
    self.tx().to(&target).raw_call("execute").single_esdt(&asset, 0, &amount).sync_call();
    let balance_after = self.blockchain().get_sc_balance(&asset.into(), 0);
    require!(balance_after >= balance_before, "Not repaid");

    self.operation_ongoing().set(false);
}
```

## Anti-Patterns

### 1. Forgetting to Clear the Guard
```rust
// WRONG — if verification fails, guard stays set forever
self.operation_ongoing().set(true);
self.tx().to(&target).raw_call(endpoint).sync_call();
// If this require fails, the guard is never cleared!
require!(balance_after >= expected, "Not repaid");
self.operation_ongoing().set(false);
```

Note: In MultiversX, if `require!` fails the transaction reverts, so the guard is also reverted. But in callback-based flows, be careful about which execution context you're in.

### 2. Checking Balance Incorrectly
```rust
// WRONG — checking a specific storage value instead of actual contract balance
let repaid = self.deposits(&asset).get();

// CORRECT — check actual on-chain balance
let balance_after = self.blockchain().get_sc_balance(&asset.into(), 0);
```

### 3. No Shard Validation
```rust
// WRONG — cross-shard calls break atomicity silently
fn flash_loan(&self, borrower: ManagedAddress, /* ... */) {
    // If borrower is on different shard, sync_call becomes async
    self.tx().to(&borrower).raw_call(endpoint).sync_call();
}
```

## Template

```rust
#[multiversx_sc::module]
pub trait AtomicOperationModule {
    #[storage_mapper("operationOngoing")]
    fn operation_ongoing(&self) -> SingleValueMapper<bool>;

    #[storage_mapper("feeBps")]
    fn fee_bps(&self) -> SingleValueMapper<u64>;

    fn require_not_ongoing(&self) {
        require!(!self.operation_ongoing().get(), "Operation already in progress");
    }

    fn require_same_shard(&self, target: &ManagedAddress) {
        let target_shard = self.blockchain().get_shard_of_address(target);
        let self_shard = self.blockchain().get_shard_of_address(&self.blockchain().get_sc_address());
        require!(target_shard == self_shard, "Must be same shard");
    }

    fn require_valid_endpoint(&self, endpoint: &ManagedBuffer<Self::Api>) {
        require!(
            !endpoint.is_empty() && !self.blockchain().is_builtin_function(endpoint),
            "Invalid endpoint"
        );
    }
}
```
