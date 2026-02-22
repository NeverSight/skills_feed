---
name: multiversx-payment-handling
description: Handle payments in MultiversX smart contracts. Use when receiving, validating, or routing EGLD/ESDT payments via self.call_value(), Payment types, or payable endpoints. Covers single, multi, optional, and mixed payment patterns.
---

# MultiversX Payment Handling — `self.call_value()` API Reference

Complete reference for receiving and validating payments in MultiversX smart contracts (SDK v0.64+).

## Payment Type Hierarchy

```
Payment<M>              ← v0.64+ preferred, uses NonZeroBigUint (amount guaranteed > 0)
├── token_identifier: TokenId<M>           (unified: EGLD + ESDT)
├── token_nonce: u64
└── amount: NonZeroBigUint<M>

EsdtTokenPayment<M>     ← ESDT-only (no EGLD), BigUint amount (can be 0 in theory)
├── token_identifier: EsdtTokenIdentifier<M>
├── token_nonce: u64
└── amount: BigUint<M>

EgldOrEsdtTokenPayment<M> ← Legacy mixed type
├── token_identifier: EgldOrEsdtTokenIdentifier<M>
├── token_nonce: u64
└── amount: BigUint<M>

PaymentVec<M> = ManagedVec<M, Payment<M>>  ← List of payments
FungiblePayment<M>                          ← Payment with nonce == 0 guaranteed
```

### Payment Methods
```rust
// Payment<M>
payment.is_fungible() -> bool
payment.fungible_or_panic() -> FungiblePayment<M>
payment.into_tuple() -> (TokenId<M>, u64, NonZeroBigUint<M>)
payment.as_egld_or_esdt_payment() -> &EgldOrEsdtTokenPayment<M>
payment.map_egld_or_esdt(ctx, for_egld, for_esdt) -> U

// NonZeroBigUint<M>
NonZeroBigUint::new(bu: BigUint<M>) -> Option<Self>      // None if zero
NonZeroBigUint::new_or_panic(bu: BigUint<M>) -> Self      // panics if zero
nzbu.into_big_uint() -> BigUint<M>
nzbu.as_big_uint() -> &BigUint<M>
```

## `self.call_value()` Methods

### EGLD-Only

| Method | Returns | Behavior |
|--------|---------|----------|
| `.egld()` | `ManagedRef<BigUint>` | Accepts EGLD only, panics if ESDT sent. Handles both direct and multi-transfer EGLD. |
| `.egld_decimal()` | `ManagedDecimal<EgldDecimals>` | EGLD as 18-decimal `ManagedDecimal` |
| `.egld_direct_non_strict()` | `ManagedRef<BigUint>` | Raw EGLD from VM. Returns 0 even if ESDT was sent. Low-level, rarely needed. |

### Single Token (Any Type)

| Method | Returns | Behavior |
|--------|---------|----------|
| `.single()` | `Ref<Payment>` | Exactly 1 transfer (EGLD or ESDT). Panics if 0 or 2+. **Preferred for v0.64+.** |
| `.single_optional()` | `Option<Ref<Payment>>` | 0 or 1 transfer. Panics if 2+. |
| `.single_esdt()` | `Ref<EsdtTokenPayment>` | Exactly 1 ESDT. Panics if EGLD or count != 1. |
| `.single_fungible_esdt()` | `(ManagedRef<EsdtTokenIdentifier>, ManagedRef<BigUint>)` | Exactly 1 fungible ESDT (nonce == 0). |
| `.egld_or_single_esdt()` | `EgldOrEsdtTokenPayment` | 0 or 1 transfer. Returns EGLD(0) if nothing sent. |
| `.egld_or_single_fungible_esdt()` | `(EgldOrEsdtTokenIdentifier, BigUint)` | Like above but panics if non-fungible. |

### Multi-Token

| Method | Returns | Behavior |
|--------|---------|----------|
| `.all()` | `ManagedRef<PaymentVec>` | **Recommended.** All transfers as `Payment` list. Handles EGLD + ESDT uniformly. |
| `.all_transfers()` | `ManagedRef<ManagedVec<EgldOrEsdtTokenPayment>>` | All transfers as legacy type. |
| `.all_esdt_transfers()` | `ManagedRef<ManagedVec<EsdtTokenPayment>>` | ESDT only. Panics if EGLD present in multi-transfer. |

### Fixed-Count Arrays

| Method | Returns | Behavior |
|--------|---------|----------|
| `.array::<N>()` | `[Ref<Payment>; N]` | Exactly N transfers (any type). Panics if count != N. |
| `.multi_esdt::<N>()` | `[Ref<EsdtTokenPayment>; N]` | Exactly N ESDT transfers. Rejects EGLD. |
| `.multi_egld_or_esdt::<N>()` | `[Ref<EgldOrEsdtTokenPayment>; N]` | Exactly N transfers (legacy type). |

## Deprecated — Do NOT Use

| Deprecated | Replacement | Since |
|-----------|-------------|-------|
| `.egld_value()` | `.egld()` | v0.55 — doesn't handle multi-transfer EGLD properly |
| `.any_payment()` | `.all()` | v0.64 — legacy EGLD-or-multi split no longer meaningful |

## Common Patterns

### Single Payment Endpoint
```rust
#[payable]
#[endpoint(deposit)]
fn deposit(&self) {
    let payment = self.call_value().single();
    // payment.token_identifier, payment.token_nonce, payment.amount (NonZeroBigUint)
    self.deposits(&self.blockchain().get_caller())
        .update(|total| *total += payment.amount.as_big_uint());
}
```

### EGLD-Only Endpoint
```rust
#[payable("EGLD")]
#[endpoint(delegate)]
fn delegate(&self) {
    let payment = self.call_value().egld().clone_value();
    require!(payment >= MIN_EGLD, "Below minimum");
}
```

### Multi-Payment with Validation
```rust
#[payable]
#[endpoint(repay)]
fn repay(&self) {
    let payments = self.call_value().all();
    for payment in payments.iter() {
        require!(
            self.is_accepted_token(&payment.token_identifier),
            "Token not accepted"
        );
        self.process_repayment(&payment);
    }
}
```

### Fixed Two-Token Swap
```rust
#[payable]
#[endpoint(addLiquidity)]
fn add_liquidity(&self) {
    let [token_a, token_b] = self.call_value().array::<2>();
    require!(token_a.token_identifier != token_b.token_identifier, "Same token");
}
```

### Optional Payment (Claim or Deposit)
```rust
#[payable]
#[endpoint(interact)]
fn interact(&self) {
    match self.call_value().single_optional() {
        Some(payment) => self.handle_deposit(&payment),
        None => self.handle_claim(),
    }
}
```

### EGLD-or-ESDT with Token Routing
```rust
#[payable]
#[endpoint(addRewards)]
fn add_reward(&self) {
    let payment = self.call_value().egld_or_single_esdt();
    let pool = self.pool_for_token(&payment.token_identifier);
    self.tx().to(&pool)
        .typed(PoolProxy)
        .deposit()
        .payment(payment)
        .returns(ReturnsResult)
        .sync_call();
}
```

### Payment to Transfer Syntax
```rust
// Transfer single Payment to caller
let caller = self.blockchain().get_caller();
self.tx().to(&caller).payment(payment.clone()).transfer();

// Transfer EGLD
self.tx().to(&caller).egld(&amount).transfer();
```

## Anti-Patterns

```rust
// BAD: using deprecated egld_value — misses EGLD in multi-transfer
let value = self.call_value().egld_value(); // ← DEPRECATED since v0.55

// GOOD: use egld() which handles both direct and multi-transfer
let value = self.call_value().egld();

// BAD: using any_payment — legacy split
let payment = self.call_value().any_payment(); // ← DEPRECATED since v0.64

// GOOD: use all() for uniform handling
let payments = self.call_value().all();

// BAD: not validating token before processing
let payment = self.call_value().single();
self.do_something(&payment); // What if wrong token?

// GOOD: validate token identity
let payment = self.call_value().single();
require!(
    payment.token_identifier == self.accepted_token().get(),
    "Wrong token"
);
```
