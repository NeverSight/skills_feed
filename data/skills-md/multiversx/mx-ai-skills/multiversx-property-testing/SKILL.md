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
