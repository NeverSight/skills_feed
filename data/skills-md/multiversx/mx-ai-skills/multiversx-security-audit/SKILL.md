---
name: multiversx-security-audit
description: Complete security audit methodology for MultiversX smart contracts. Covers context building, entry point analysis, static analysis patterns, and automated Semgrep scanning. Use when performing security audits, code reviews, or setting up automated vulnerability detection.
---

# MultiversX Security Audit Methodology

A sequential workflow for auditing MultiversX smart contracts, from initial reconnaissance through automated scanning.

## When to Use

- Starting a new security audit engagement
- Performing security code reviews
- Setting up automated vulnerability scanning
- Mapping attack surface for penetration testing
- Training new security reviewers

---

## Phase 1: Context Building

Rapidly build a comprehensive mental model of the codebase before diving into vulnerability hunting.

### 1.1 Reconnaissance Checklist

- [ ] **Core logic**: `#[multiversx_sc::contract]`, `#[payable]`, value-moving functions, access control patterns
- [ ] **Externalities**: cross-contract calls, hardcoded addresses (`sc:` literals), oracle dependencies, bridge contracts
- [ ] **Documentation**: `README.md`, `specs/`, `sc-config.toml`, `multiversx.yaml`, `snippets.sh`, `scenarios/` tests

### 1.2 System Mapping

#### Roles and Permissions
| Role | Capabilities | How Assigned |
|------|-------------|--------------|
| Owner | Full admin access | Deploy-time, transferable |
| Admin | Limited admin functions | Owner grants |
| User | Public endpoints | Anyone |
| Whitelisted | Special access | Admin grants |

#### Asset Inventory
| Asset Type | Examples | Risk Level |
|------------|----------|------------|
| EGLD | Native currency | Critical |
| Fungible ESDT | Custom tokens | High |
| NFT/SFT | Non-fungible tokens | Medium-High |
| Meta-ESDT | Tokens with metadata | Medium-High |

#### State Analysis
Document all storage mappers and their purposes:

```rust
// Example state inventory
#[storage_mapper("owner")]           // SingleValueMapper - access control
#[storage_mapper("balances")]        // MapMapper - user funds (CRITICAL)
#[storage_mapper("whitelist")]       // SetMapper - privileged users
```

### 1.3 Entry Point Enumeration (Initial)

List all `#[endpoint]` functions with their risk classification:

```
HIGH RISK:
- deposit() - #[payable("*")] - accepts value
- withdraw() - moves funds out
- upgrade() - can change contract logic

MEDIUM RISK:
- setConfig() - owner only, changes behavior
- addWhitelist() - expands permissions

LOW RISK:
- getBalance() - #[view] - read only
```

### 1.4 Threat Modeling (Initial)

#### Asset at Risk Analysis
- **Direct Loss**: What funds can be stolen if the contract fails?
- **Indirect Loss**: What downstream systems depend on this contract?
- **Reputation Loss**: What non-financial damage could occur?

#### Attacker Profiles
| Attacker | Motivation | Capabilities |
|----------|------------|--------------|
| External User | Profit | Public endpoints only |
| Malicious Admin | Insider threat | Admin functions |
| Reentrant Contract | Exploit callbacks | Cross-contract calls |
| Front-runner | MEV extraction | Transaction ordering |

### 1.4 Environment Check

#### Dependency Audit
- **Framework Version**: Check `Cargo.toml` for `multiversx-sc` version
- **Known Vulnerabilities**: Compare against security advisories
- **Deprecated APIs**: Look for usage of deprecated functions

#### Test Suite Assessment
- **Coverage**: Does `scenarios/` exist with comprehensive tests?
- **Edge Cases**: Are failure paths tested?
- **Freshness**: Run `sc-meta test-gen` to verify tests match current code

### 1.5 Context Building Output

After completing context building, document:

1. **System Overview**: One-paragraph summary of what the contract does
2. **Trust Boundaries**: Who trusts whom, what assumptions exist
3. **Critical Paths**: The most security-sensitive code paths
4. **Initial Concerns**: Preliminary list of areas requiring deep review
5. **Questions for Team**: Clarifications needed from developers

### Context Building Checklist

- [ ] All entry points identified and classified
- [ ] Storage layout documented
- [ ] External dependencies mapped
- [ ] Role/permission model understood
- [ ] Test coverage assessed
- [ ] Framework version noted
- [ ] Initial threat model drafted

---

## Phase 2: Entry Point Analysis

Identify the complete attack surface by enumerating all public interaction points and classifying their risk levels.

### 2.1 Entry Point Identification

#### MultiversX Macros That Expose Functions

| Macro | Visibility | Risk Level | Description |
|-------|-----------|------------|-------------|
| `#[endpoint]` | Public write | High | State-changing public function |
| `#[view]` | Public read | Low | Read-only public function |
| `#[payable]` | Accepts any token | Critical | Handles value transfers |
| `#[payable("EGLD")]` | Accepts EGLD only | Critical | Handles native currency |
| `#[init]` | Deploy only | Medium | Constructor (runs once) |
| `#[upgrade]` | Upgrade only | Critical | Migration logic |
| `#[callback]` | Internal | High | Async call response handler |
| `#[only_owner]` | Owner restricted | Medium | Admin functions |

#### Scanning Commands
```bash
# Find all endpoints
grep -n "#\[endpoint" src/*.rs

# Find all payable endpoints
grep -n "#\[payable" src/*.rs

# Find all views
grep -n "#\[view" src/*.rs

# Find callbacks
grep -n "#\[callback" src/*.rs

# Find init and upgrade
grep -n "#\[init\]\|#\[upgrade\]" src/*.rs
```

### 2.2 Risk Classification

#### Category A: Payable Endpoints (Critical Risk)

Functions receiving value require the most scrutiny.

```rust
#[payable]
#[endpoint]
fn deposit(&self) {
    // MUST CHECK:
    // 1. Token identifier validation
    // 2. Amount > 0 validation
    // 3. Correct handling of multi-token transfers
    // 4. State updates before external calls

    let payment = self.call_value().single();
    require!(
        payment.token_identifier == self.accepted_token().get(),
        "Wrong token"
    );

    // Process deposit...
}
```

**Checklist for Payable Endpoints:**
- [ ] Token ID validated against expected token(s)
- [ ] Amount checked for minimum/maximum bounds
- [ ] Multi-transfer handling if `all()` used
- [ ] Nonce validation for NFT/SFT
- [ ] Reentrancy protection (Checks-Effects-Interactions)

#### Category B: Non-Payable State-Changing Endpoints (High Risk)

```rust
#[endpoint]
fn update_config(&self, new_value: BigUint) {
    // MUST CHECK:
    // 1. Who can call this? (access control)
    // 2. Input validation
    // 3. State transition validity

    self.require_caller_is_admin();
    require!(new_value > 0, "Invalid value");
    self.config().set(new_value);
}
```

**Checklist for State-Changing Endpoints:**
- [ ] Access control implemented and correct
- [ ] Input validation for all parameters
- [ ] State transitions are valid
- [ ] Events emitted for important changes
- [ ] No DoS vectors (unbounded loops, etc.)

#### Category C: View Functions (Low Risk)

```rust
#[view(getBalance)]
fn get_balance(&self, user: ManagedAddress) -> BigUint {
    // SHOULD CHECK:
    // 1. Does it actually modify state? (interior mutability)
    // 2. Does it leak sensitive information?
    // 3. Is the calculation expensive (DoS via gas)?

    self.balances(&user).get()
}
```

**Checklist for View Functions:**
- [ ] No state modification (verify no storage writes)
- [ ] No sensitive data exposure
- [ ] Bounded computation (no unbounded loops)
- [ ] Block info usage appropriate (`get_block_timestamp_millis()` / `get_block_timestamp_seconds()` may differ off-chain)

#### Category D: Init and Upgrade (Critical Risk)

```rust
#[init]
fn init(&self, admin: ManagedAddress) {
    // MUST CHECK:
    // 1. All required state initialized
    // 2. No way to re-initialize
    // 3. Admin/owner properly set

    self.admin().set(admin);
}

#[upgrade]
fn upgrade(&self) {
    // MUST CHECK:
    // 1. New storage mappers initialized
    // 2. Storage layout compatibility
    // 3. Migration logic correct
}
```

#### Category E: Callbacks (High Risk)

```rust
#[callback]
fn transfer_callback(
    &self,
    #[call_result] result: ManagedAsyncCallResult<()>
) {
    // MUST CHECK:
    // 1. Error handling (don't assume success)
    // 2. State reversion on failure
    // 3. Correct identification of original call

    match result {
        ManagedAsyncCallResult::Ok(_) => {
            // Success path
        },
        ManagedAsyncCallResult::Err(_) => {
            // CRITICAL: Must handle failure!
            // Revert any state changes from original call
        }
    }
}
```

### 2.3 Analysis Workflow

#### Step 1: List All Entry Points

```markdown
| Endpoint | Type | Payable | Access | Storage Touched | Risk |
|----------|------|---------|--------|-----------------|------|
| deposit | endpoint | * | Public | balances | Critical |
| withdraw | endpoint | No | Public | balances | Critical |
| setAdmin | endpoint | No | Owner | admin | High |
| getBalance | view | No | Public | balances (read) | Low |
| init | init | No | Deploy | admin, config | Medium |
```

#### Step 2: Tag Access Control

```rust
// Public - anyone can call
#[endpoint]
fn public_function(&self) { }

// Owner only - blockchain owner
#[only_owner]
#[endpoint]
fn owner_function(&self) { }

// Admin only - custom access control
#[endpoint]
fn admin_function(&self) {
    self.require_caller_is_admin();
}

// Whitelisted - address in set
#[endpoint]
fn whitelist_function(&self) {
    let caller = self.blockchain().get_caller();
    require!(self.whitelist().contains(&caller), "Not whitelisted");
}
```

#### Step 3: Tag Value Handling

| Tag | Meaning | Example |
|-----|---------|---------|
| Refusable | Rejects payments | Default (no `#[payable]`) |
| EGLD Only | Accepts EGLD | `#[payable("EGLD")]` |
| Token Only | Specific ESDT | `#[payable("TOKEN-abc123")]` |
| Any Token | Any payment | `#[payable]` |
| Multi-Token | Multiple payments | Uses `all()` |

#### Step 4: Graph Data Flow

```
deposit() ──writes──▶ balances
          ──writes──▶ total_deposited
          ──reads───▶ accepted_token

withdraw() ──reads/writes──▶ balances
           ──reads────────▶ withdrawal_fee

getBalance() ──reads──▶ balances
```

### 2.4 Specific Attack Vectors

#### Privilege Escalation
```rust
// VULNERABLE: Missing access control
#[endpoint]
fn set_admin(&self, new_admin: ManagedAddress) {
    self.admin().set(new_admin);  // Anyone can become admin!
}

// CORRECT: Protected
#[only_owner]
#[endpoint]
fn set_admin(&self, new_admin: ManagedAddress) {
    self.admin().set(new_admin);
}
```

#### DoS via Unbounded Growth
```rust
// VULNERABLE: Public endpoint adds to unbounded set
#[endpoint]
fn register(&self) {
    let caller = self.blockchain().get_caller();
    self.participants().insert(caller);  // Grows forever!
}
```

#### Missing Payment Validation

**Bad:**
```rust
// DON'T: Accept any token without validation — attacker sends worthless tokens
#[payable]
#[endpoint]
fn stake(&self) {
    let payment = self.call_value().single();
    self.staked().update(|s| *s += payment.amount.as_big_uint()); // Fake tokens accepted!
}
```

**Good:**
```rust
// DO: Validate token identity and optionally enforce minimum amount
#[payable]
#[endpoint]
fn stake(&self) {
    let payment = self.call_value().single();
    require!(
        payment.token_identifier == self.staking_token().get(),
        "Wrong token"
    );
    self.staked().update(|s| *s += payment.amount.as_big_uint());
}
```

#### Callback State Assumptions
```rust
// VULNERABLE: Assumes success
#[callback]
fn on_transfer_complete(&self) {
    // This runs even if transfer FAILED!
    self.transfer_count().update(|c| *c += 1);
}
```

### 2.5 Entry Point Analysis Output Template

```markdown
# Entry Point Analysis: [Contract Name]

## Summary
- Total Endpoints: X
- Payable Endpoints: Y (Critical)
- State-Changing: Z (High)
- Views: W (Low)

## Access Control Matrix

| Endpoint | Public | Owner | Admin | Whitelist |
|----------|--------|-------|-------|-----------|
| deposit | Yes | - | - | - |
| setAdmin | - | Yes | - | - |

## Recommended Focus Areas
1. [Highest priority endpoint and why]
2. [Second priority]
3. [Third priority]
```

---

## Phase 3: Static Analysis Patterns

Manual and automated static analysis for finding vulnerabilities in MultiversX Rust and Go code.

### 3.1 Rust Smart Contracts (`multiversx-sc`)

#### Critical Grep Patterns

##### Unsafe Code
```bash
# Unsafe blocks - valid only for FFI or specific optimizations
grep -rn "unsafe" src/
```
**Risk**: Memory corruption, undefined behavior
**Action**: Require justification for each `unsafe` block

##### Panic Inducers
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

##### Floating Point Arithmetic
```bash
grep -rn "f32" src/
grep -rn "f64" src/
grep -rn "as f32\|as f64" src/
```
**Risk**: Non-deterministic behavior, consensus failure
**Action**: Use `BigUint`/`BigInt` for all calculations

##### Unchecked Arithmetic
```bash
grep -rn "[^_a-zA-Z]\+ [^_a-zA-Z]" src/  # Addition
grep -rn "[^_a-zA-Z]\- [^_a-zA-Z]" src/  # Subtraction
grep -rn "[^_a-zA-Z]\* [^_a-zA-Z]" src/  # Multiplication
```
**Risk**: Integer overflow/underflow
**Action**: Use `BigUint` or checked arithmetic for all financial calculations

##### Map Iteration (DoS Risk)
```bash
grep -rn "\.iter()" src/
grep -rn "for.*in.*\.iter()" src/
grep -rn "\.collect()" src/
```
**Risk**: Gas exhaustion DoS
**Action**: Add pagination or bounds checking

#### Logical Pattern Analysis (Manual Review)

##### Token ID Validation
```bash
grep -rn "call_value()" src/
grep -rn "\.single()" src/
grep -rn "\.all()" src/
grep -rn "\.array()" src/
grep -rn "\.single_optional()" src/
# Legacy patterns (may still be in older code)
grep -rn "all_esdt_transfers" src/
grep -rn "single_esdt" src/
```

For each occurrence, verify:
- [ ] Token ID checked against expected value (using `TokenId` comparison)
- [ ] Token nonce validated (for NFT/SFT)
- [ ] Amount validated (within bounds — non-zero is guaranteed by `NonZeroBigUint` in `Payment`)

```rust
// VULNERABLE
#[payable]
fn deposit(&self) {
    let payment = self.call_value().single();
    self.balances().update(|b| *b += payment.amount.as_big_uint());
    // No token ID check! Accepts any token
}

// SECURE
#[payable]
fn deposit(&self) {
    let payment = self.call_value().single();
    require!(
        payment.token_identifier == self.accepted_token().get(),
        "Wrong token"
    );
    // Note: amount > 0 check is no longer needed — Payment.amount is NonZeroBigUint
    self.balances().update(|b| *b += payment.amount.as_big_uint());
}
```

##### Callback State Assumptions
```bash
grep -rn "#\[callback\]" src/
```

For each callback, verify:
- [ ] Does NOT assume async call succeeded
- [ ] Handles error case explicitly
- [ ] Reverts state changes on failure if needed

##### Access Control
```bash
grep -rn "#\[endpoint\]" src/
grep -rn "#\[only_owner\]" src/
```

For each endpoint, verify:
- [ ] Appropriate access control applied
- [ ] Sensitive operations restricted
- [ ] Admin functions documented

##### Reentrancy (CEI Pattern)
```bash
grep -rn "\.send()\." src/
grep -rn "\.tx()" src/
grep -rn "async_call" src/
```

Verify Checks-Effects-Interactions pattern:
- [ ] All checks (require!) before state changes
- [ ] State changes before external calls
- [ ] No state changes after external calls in same function

### 3.2 Go Protocol Code (`mx-chain-go`)

#### Concurrency Issues

##### Goroutine Loop Variable Capture
```bash
grep -rn "go func" *.go
```

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

##### Map Race Conditions
```bash
grep -rn "map\[" *.go | grep -v "sync.Map"
```

#### Determinism Issues

##### Map Iteration Order
```bash
grep -rn "for.*range.*map" *.go
```

Map iteration in Go is random. Never use for generating hashes, creating consensus data, or any deterministic output.

##### Time Functions
```bash
grep -rn "time.Now()" *.go
```

`time.Now()` is forbidden in block processing — use `block.Header.TimeStamp` instead.

### 3.3 Analysis Checklist

#### Smart Contract Review Checklist

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

#### Protocol Review Checklist

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

### 3.4 Vulnerability Categories Quick Reference

| Category | Grep Pattern | Severity |
|----------|-------------|----------|
| Unsafe code | `unsafe` | Critical |
| Float arithmetic | `f32\|f64` | Critical |
| Panic inducers | `unwrap()\|expect(` | High |
| Unbounded iteration | `\.iter()` | High |
| Missing access control | `#[endpoint]` without `#[only_owner]` | High |
| Token validation | `call_value().single()` without token ID require | High |
| Callback assumptions | `#[callback]` without error handling | Medium |
| Raw arithmetic | `+ \| - \| *` on u64 | Medium |

---

## Phase 4: Automated Scanning with Semgrep

Create custom Semgrep rules to automatically detect MultiversX-specific security patterns and best practice violations.

### 4.1 Semgrep Basics for Rust

#### Rule Structure
```yaml
rules:
  - id: rule-identifier
    languages: [rust]
    message: "Description of the issue and why it matters"
    severity: ERROR  # ERROR, WARNING, INFO
    patterns:
      - pattern: <code pattern to match>
    metadata:
      category: security
      technology:
        - multiversx
```

#### Pattern Syntax

| Syntax | Meaning | Example |
|--------|---------|---------|
| `$VAR` | Any expression | `$X + $Y` matches `a + b` |
| `...` | Zero or more statements | `{ ... }` matches any block |
| `$...VAR` | Zero or more arguments | `func($...ARGS)` |
| `<... $X ...>` | Contains expression | `<... panic!(...) ...>` |

### 4.2 Common MultiversX Rules

#### Unsafe Arithmetic Detection

```yaml
rules:
  - id: mvx-unsafe-addition
    languages: [rust]
    message: "Potential arithmetic overflow. Use BigUint or checked arithmetic for financial calculations."
    severity: ERROR
    patterns:
      - pattern: $X + $Y
      - pattern-not: $X.checked_add($Y)
      - pattern-not: BigUint::from($X) + BigUint::from($Y)
    paths:
      include:
        - "*/src/*.rs"
    metadata:
      category: security
      subcategory: arithmetic
      cwe: "CWE-190: Integer Overflow"

  - id: mvx-unsafe-multiplication
    languages: [rust]
    message: "Potential multiplication overflow. Use BigUint or checked_mul."
    severity: ERROR
    patterns:
      - pattern: $X * $Y
      - pattern-not: $X.checked_mul($Y)
      - pattern-not: BigUint::from($X) * BigUint::from($Y)
```

#### Floating Point Detection

```yaml
rules:
  - id: mvx-float-forbidden
    languages: [rust]
    message: "Floating point arithmetic is non-deterministic and forbidden in smart contracts."
    severity: ERROR
    pattern-either:
      - pattern: "let $X: f32 = ..."
      - pattern: "let $X: f64 = ..."
      - pattern: "$X as f32"
      - pattern: "$X as f64"
    metadata:
      category: security
      subcategory: determinism
```

#### Payable Endpoint Without Value Check

```yaml
rules:
  - id: mvx-payable-no-check
    languages: [rust]
    message: "Payable endpoint does not check payment value. Verify token ID and amount."
    severity: WARNING
    patterns:
      - pattern: |
          #[payable]
          #[endpoint]
          fn $FUNC(&self, $...PARAMS) {
              $...BODY
          }
      - pattern-not: |
          #[payable]
          #[endpoint]
          fn $FUNC(&self, $...PARAMS) {
              <... self.call_value() ...>
          }
    metadata:
      category: security
      subcategory: input-validation
```

#### Unsafe Unwrap Usage

```yaml
rules:
  - id: mvx-unsafe-unwrap
    languages: [rust]
    message: "unwrap() can panic. Use unwrap_or_else with sc_panic! or proper error handling."
    severity: ERROR
    patterns:
      - pattern: $EXPR.unwrap()
      - pattern-not-inside: |
          #[test]
          fn $FUNC() { ... }
    fix: "$EXPR.unwrap_or_else(|| sc_panic!(\"Error message\"))"
    metadata:
      category: security
      subcategory: error-handling
```

#### Missing Owner Check

```yaml
rules:
  - id: mvx-sensitive-no-owner-check
    languages: [rust]
    message: "Sensitive operation without owner check. Add #[only_owner] or explicit verification."
    severity: ERROR
    patterns:
      - pattern: |
          #[endpoint]
          fn $FUNC(&self, $...PARAMS) {
              <... self.$MAPPER().set(...) ...>
          }
      - pattern-not: |
          #[only_owner]
          #[endpoint]
          fn $FUNC(&self, $...PARAMS) { ... }
      - pattern-not: |
          #[endpoint]
          fn $FUNC(&self, $...PARAMS) {
              <... self.blockchain().get_owner_address() ...>
          }
      - metavariable-regex:
          metavariable: $MAPPER
          regex: "(admin|owner|config|fee|rate)"
```

### 4.3 Advanced Patterns

#### Callback Without Error Handling

```yaml
rules:
  - id: mvx-callback-no-error-handling
    languages: [rust]
    message: "Callback does not handle error case. Async call failures will silently proceed."
    severity: ERROR
    patterns:
      - pattern: |
          #[callback]
          fn $FUNC(&self, $...PARAMS) {
              $...BODY
          }
      - pattern-not: |
          #[callback]
          fn $FUNC(&self, #[call_result] $RESULT: ManagedAsyncCallResult<$TYPE>) {
              ...
          }
```

#### Unbounded Iteration

```yaml
rules:
  - id: mvx-unbounded-iteration
    languages: [rust]
    message: "Iterating over storage mapper without bounds. Can cause DoS via gas exhaustion."
    severity: ERROR
    pattern-either:
      - pattern: self.$MAPPER().iter()
      - pattern: |
          for $ITEM in self.$MAPPER().iter() {
              ...
          }
    metadata:
      category: security
      subcategory: dos
      cwe: "CWE-400: Uncontrolled Resource Consumption"
```

#### Storage Key Collision Risk

```yaml
rules:
  - id: mvx-storage-key-short
    languages: [rust]
    message: "Storage key is very short, increasing collision risk. Use descriptive keys."
    severity: WARNING
    patterns:
      - pattern: '#[storage_mapper("$KEY")]'
      - metavariable-regex:
          metavariable: $KEY
          regex: "^.{1,3}$"
```

#### Reentrancy Pattern Detection

```yaml
rules:
  - id: mvx-reentrancy-risk
    languages: [rust]
    message: "External call before state update. Follow Checks-Effects-Interactions pattern."
    severity: ERROR
    patterns:
      - pattern: |
          fn $FUNC(&self, $...PARAMS) {
              ...
              self.send().$SEND_METHOD(...);
              ...
              self.$STORAGE().set(...);
              ...
          }
      - pattern: |
          fn $FUNC(&self, $...PARAMS) {
              ...
              self.tx().to(...).transfer();
              ...
              self.$STORAGE().set(...);
              ...
          }
```

### 4.4 Creating Rules from Findings

#### Workflow

1. **Find a bug manually** during audit
2. **Abstract the pattern** - what makes this a bug?
3. **Write a Semgrep rule** to catch similar issues
4. **Test on the codebase** - find all variants
5. **Refine to reduce false positives**

#### Example: From Bug to Rule

**Bug Found:**
```rust
#[endpoint]
fn withdraw(&self, amount: BigUint) {
    let caller = self.blockchain().get_caller();
    self.send().direct_egld(&caller, &amount);  // Sends before balance check!
    self.balances(&caller).update(|b| *b -= &amount);  // Can underflow
}
```

**Rule Created:**
```yaml
rules:
  - id: mvx-withdraw-pattern-unsafe
    languages: [rust]
    message: "Withdrawal sends funds before updating balance. Risk of reentrancy and underflow."
    severity: ERROR
    patterns:
      - pattern: |
          fn $FUNC(&self, $...PARAMS) {
              ...
              self.send().$METHOD(...);
              ...
              self.$BALANCE(...).update(|$B| *$B -= ...);
              ...
          }
      - pattern: |
          fn $FUNC(&self, $...PARAMS) {
              ...
              self.tx().to(...).transfer();
              ...
              self.$BALANCE(...).update(|$B| *$B -= ...);
              ...
          }
```

### 4.5 Running Semgrep

```bash
# Run single rule
semgrep --config rules/mvx-unsafe-arithmetic.yaml src/

# Run all rules in directory
semgrep --config rules/ src/

# Output JSON for processing
semgrep --config rules/ --json -o results.json src/

# Ignore test files
semgrep --config rules/ --exclude="*_test.rs" --exclude="tests/" src/
```

#### CI/CD Integration
```yaml
# GitHub Actions example
- name: Run Semgrep
  uses: returntocorp/semgrep-action@v1
  with:
    config: >-
      rules/mvx-security.yaml
      rules/mvx-best-practices.yaml
```

### 4.6 Rule Library Organization

```
semgrep-rules/
├── security/
│   ├── mvx-arithmetic.yaml      # Overflow/underflow
│   ├── mvx-access-control.yaml  # Auth issues
│   ├── mvx-reentrancy.yaml      # CEI violations
│   └── mvx-input-validation.yaml
├── best-practices/
│   ├── mvx-storage.yaml         # Storage patterns
│   ├── mvx-gas.yaml             # Gas optimization
│   └── mvx-error-handling.yaml
└── style/
    ├── mvx-naming.yaml          # Naming conventions
    └── mvx-documentation.yaml   # Doc requirements
```

### 4.7 Testing Rules

#### Test File Format
```yaml
# test/mvx-unsafe-unwrap.test.yaml
rules:
  - id: mvx-unsafe-unwrap
    # ... rule definition ...

# Test cases
test_cases:
  - name: "Should match unwrap"
    code: |
      fn test() {
          let x = some_option.unwrap();
      }
    should_match: true

  - name: "Should not match unwrap_or_else"
    code: |
      fn test() {
          let x = some_option.unwrap_or_else(|| sc_panic!("Error"));
      }
    should_match: false
```

#### Running Tests
```bash
semgrep --test rules/
```

### 4.8 Best Practices for Rule Writing

1. **Start specific, then generalize**: Begin with exact pattern, relax constraints carefully
2. **Include fix suggestions**: Use `fix:` field when automated fixes are safe
3. **Document the "why"**: Message should explain impact, not just what's detected
4. **Include CWE references**: Link to standard vulnerability classifications
5. **Test with real codebases**: Validate against actual MultiversX projects
6. **Version your rules**: Rules evolve as framework APIs change
7. **Categorize by severity**: ERROR for security, WARNING for best practices
