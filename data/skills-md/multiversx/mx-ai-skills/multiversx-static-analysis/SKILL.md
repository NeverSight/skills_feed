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
