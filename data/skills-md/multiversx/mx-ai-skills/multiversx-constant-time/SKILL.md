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
