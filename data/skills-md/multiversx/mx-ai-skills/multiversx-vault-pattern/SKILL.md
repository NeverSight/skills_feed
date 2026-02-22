---
name: multiversx-vault-pattern
description: In-memory token ledger pattern for tracking intermediate balances during multi-step operations within a single transaction. Use when building any contract that processes sequential token operations — aggregators, batch processors, atomic swaps, or multi-step DeFi flows.
---

# MultiversX In-Memory Token Ledger

## What Problem Does This Solve?

When a contract executes multiple token operations in a single transaction (e.g., swap A→B, then B→C), you need to track intermediate balances without writing to storage. Storage writes are expensive and unnecessary for temporary state that only lives within one call.

## When to Use

| Scenario | Use Ledger? |
|---|---|
| Multi-step token operations in one tx | Yes |
| Need to track balances across sequential operations | Yes |
| Single deposit/withdraw | No — overkill |
| State that must persist across transactions | No — use storage |

## Core Pattern: Dual Data Structure

The ledger uses two structures working together:
- **ManagedMapEncoded** — O(1) lookup for balance checks and updates
- **ManagedVec** — ordered iteration for settlement (returning all tokens)

```rust
use multiversx_sc::api::VMApi;

pub struct TokenLedger<M: VMApi> {
    balances: ManagedMapEncoded<M, TokenId<M>, BigUint<M>>,
    tokens: ManagedVec<M, TokenId<M>>,  // Tracks insertion order for iteration
}

impl<M: VMApi> TokenLedger<M> {
    pub fn new() -> Self {
        Self {
            balances: ManagedMapEncoded::new(),
            tokens: ManagedVec::new(),
        }
    }

    /// Initialize from incoming payments
    pub fn from_payments(payments: &PaymentVec<M>) -> Self {
        let mut ledger = Self::new();
        for payment in payments.iter() {
            ledger.deposit(&payment.token_identifier, payment.amount.as_big_uint());
        }
        ledger
    }

    /// Credit a token balance
    pub fn deposit(&mut self, token: &TokenId<M>, amount: &BigUint<M>) {
        if !self.balances.contains(token) {
            self.tokens.push(token.clone());
            self.balances.put(token, amount);
        } else {
            let current = self.balances.get(token);
            self.balances.put(token, &(current + amount));
        }
    }

    /// Debit an exact amount
    pub fn withdraw(&mut self, token: &TokenId<M>, amount: &BigUint<M>) -> BigUint<M> {
        let current = self.balance_of(token);
        require!(current >= *amount, "Insufficient ledger balance");
        let new_balance = &current - amount;
        if new_balance == 0u64 {
            self.remove_token(token);
        } else {
            self.balances.put(token, &new_balance);
        }
        amount.clone()
    }

    /// Debit a percentage (parts per million)
    pub fn withdraw_percentage(&mut self, token: &TokenId<M>, ppm: u32) -> BigUint<M> {
        let balance = self.balance_of(token);
        let amount = (&balance * ppm) / 1_000_000u64;
        if amount > 0u64 { self.withdraw(token, &amount) } else { BigUint::zero() }
    }

    /// Debit entire balance (avoids dust)
    pub fn withdraw_all(&mut self, token: &TokenId<M>) -> BigUint<M> {
        let amount = self.balance_of(token);
        if amount > 0u64 { self.remove_token(token); }
        amount
    }

    /// Check balance
    pub fn balance_of(&self, token: &TokenId<M>) -> BigUint<M> {
        if !self.balances.contains(token) {
            return BigUint::zero();
        }
        self.balances.get(token)
    }

    /// Settle — convert all balances to payment objects for transfer
    pub fn settle_all(&self) -> ManagedVec<M, Payment<M>> {
        let mut payments = ManagedVec::new();
        for token in self.tokens.iter() {
            let amount = self.balances.get(&token);
            if let Some(non_zero_amount) = NonZeroBigUint::new(amount) {
                payments.push(Payment::new(token.clone_value(), 0u64, non_zero_amount));
            }
        }
        payments
    }

    fn remove_token(&mut self, token: &TokenId<M>) {
        self.balances.remove(token);
        // O(N) scan — acceptable for small token sets (typically < 10)
        for (i, t) in self.tokens.iter().enumerate() {
            if t.as_managed_buffer() == token.as_managed_buffer() {
                self.tokens.remove(i);
                break;
            }
        }
    }
}
```

## Usage: Multi-Step Operation

```rust
#[endpoint(execute_steps)]
#[payable]
fn execute_steps(&self, steps: ManagedVec<YourStep<Self::Api>>) {
    let payments = self.call_value().all();
    let mut ledger = TokenLedger::from_payments(&payments);

    for step in &steps {
        // Withdraw input from ledger
        let input_amount = ledger.withdraw(&step.input_token, &step.amount);

        // Execute operation (swap, stake, etc.)
        let output = self.execute_step(&step, input_amount);

        // Deposit result back into ledger
        ledger.deposit(&output.token_identifier, output.amount.as_big_uint());
    }

    // Return all remaining tokens to caller
    let remaining = ledger.settle_all();
    if !remaining.is_empty() {
        self.tx().to(&self.blockchain().get_caller()).payment(&remaining).transfer();
    }
}
```

## Settlement with Proper Types

### Bad
```rust
// DON'T: Use legacy types for settlement — BigUint allows zero-amount payments
fn settle_bad(&self) -> ManagedVec<EsdtTokenPayment> {
    let mut payments = ManagedVec::new();
    for token in self.tokens.iter() {
        let amount = self.balances.get(&token);
        payments.push(EsdtTokenPayment::new(token.into(), 0, amount)); // Zero amounts sent!
    }
    payments
}
```

### Good
```rust
// DO: Use TokenId + NonZeroBigUint — skips zero balances at the type level
fn settle_good(&self) -> ManagedVec<Payment> {
    let mut payments = ManagedVec::new();
    for token in self.tokens.iter() {
        let amount = self.balances.get(&token);
        if let Some(nz) = NonZeroBigUint::new(amount) {
            payments.push(Payment::new(token.clone_value(), 0u64, nz));
        }
    }
    payments
}
```

## Anti-Patterns

### 1. Using Storage for Temporary Balances
```rust
// WRONG — expensive storage writes for state that lives within one tx
#[storage_mapper("tempBalance")]
fn temp_balance(&self, token: &TokenId) -> SingleValueMapper<BigUint>;
```

### 2. Not Cleaning Up Zero Balances
```rust
// WRONG — zero-balance tokens waste gas during settle_all iteration
pub fn withdraw(&mut self, token: &TokenId<M>, amount: &BigUint<M>) {
    let new_balance = &self.balance_of(token) - amount;
    self.balances.put(token, &new_balance); // Leaves zero entries!
}
```

### 3. Using Only ManagedVec (No Map)
```rust
// WRONG — O(N) lookup for every balance check
pub fn balance_of(&self, token: &TokenId<M>) -> BigUint<M> {
    for (i, t) in self.tokens.iter().enumerate() {
        if t == token { return self.amounts.get(i); }
    }
    BigUint::zero()
}
```

## Gas Optimization Notes

1. **ManagedMapEncoded** — uses heap memory, not storage. No gas for reads/writes.
2. **O(N) token removal** — acceptable for < 10 tokens in typical multi-step flows.
3. **Zero-balance cleanup** — automatically removes tokens to keep the ledger compact.
4. **Batch initialization** — `from_payments` efficiently loads all incoming tokens.

## Variations

Production repos extend this pattern with:
- **Result chaining** — passing previous step output as next step input
- **Percentage modes** — PPM-based withdrawals for partial amounts
- **Selective settlement** — returning only specific tokens, keeping the rest as protocol revenue
- **Amount mode enums** — Fixed / Percentage / All / PreviousResult for flexible step definitions
