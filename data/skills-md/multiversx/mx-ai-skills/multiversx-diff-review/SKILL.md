---
name: multiversx-diff-review
description: Review changes between smart contract versions with focus on upgradeability and security implications. Use when reviewing PRs, upgrade proposals, or analyzing differences between deployed and new code.
---

# Differential Review

Analyze differences between two versions of a MultiversX codebase, focusing on security implications of changes, storage layout compatibility, and upgrade safety.

## When to Use

- Reviewing pull requests with contract changes
- Auditing upgrade proposals before deployment
- Analyzing differences between deployed code and proposed updates
- Verifying fix implementations don't introduce regressions

## 1. Upgradeability Checks (MultiversX-Specific)

### Storage Layout Compatibility

**CRITICAL**: Storage layout changes can corrupt existing data.

#### Struct Field Ordering
```rust
// v1 - Original struct
#[derive(TopEncode, TopDecode, TypeAbi)]
pub struct UserData {
    pub balance: BigUint,      // Offset 0
    pub last_claim: u64,       // Offset 1
}

// v2 - DANGEROUS: Reordered fields
pub struct UserData {
    pub last_claim: u64,       // Now at Offset 0 - BREAKS EXISTING DATA
    pub balance: BigUint,      // Now at Offset 1 - CORRUPTED
}

// v2 - SAFE: Append new fields only
pub struct UserData {
    pub balance: BigUint,      // Offset 0 - unchanged
    pub last_claim: u64,       // Offset 1 - unchanged
    pub new_field: bool,       // Offset 2 - NEW (safe)
}
```

#### Storage Mapper Key Changes
```rust
// v1
#[storage_mapper("user_balance")]
fn user_balance(&self, user: &ManagedAddress) -> SingleValueMapper<BigUint>;

// v2 - DANGEROUS: Changed storage key
#[storage_mapper("userBalance")]  // Different key = new empty storage!
fn user_balance(&self, user: &ManagedAddress) -> SingleValueMapper<BigUint>;
```

### Initialization on Upgrade

**CRITICAL**: `#[init]` is NOT called on upgrade. Only `#[upgrade]` runs.

```rust
// v1 - Original contract
#[init]
fn init(&self) {
    self.config().set(DefaultConfig::new());
}

// v2 - Added new storage mapper
#[storage_mapper("newFeatureEnabled")]
fn new_feature_enabled(&self) -> SingleValueMapper<bool>;

// WRONG: Assuming init runs
#[init]
fn init(&self) {
    self.config().set(DefaultConfig::new());
    self.new_feature_enabled().set(true);  // Never runs on upgrade!
}

// CORRECT: Initialize in upgrade
#[upgrade]
fn upgrade(&self) {
    self.new_feature_enabled().set(true);  // Properly initializes
}
```

### Breaking Changes Checklist

| Change Type | Risk | Mitigation |
|------------|------|------------|
| Struct field reorder | Critical | Never reorder, only append |
| Storage key rename | Critical | Keep old key, migrate data |
| New required storage | High | Initialize in `#[upgrade]` |
| Removed endpoint | Medium | Ensure no external dependencies |
| Changed endpoint signature | Medium | Version API or maintain compatibility |
| New validation rules | Medium | Consider existing state validity |

## 2. Regression Analysis

### New Features Impact
- Do new features break existing invariants?
- Are there new attack vectors introduced?
- Do gas costs change significantly?

### Deleted Code Analysis
When code is removed, verify:
- Was this an intentional security fix?
- Was a validation check removed (potential vulnerability)?
- Are there other code paths that depended on this?

```rust
// v1 - Had balance check
fn withdraw(&self, amount: BigUint) {
    require!(amount <= self.balance().get(), "Insufficient balance");
    // ... withdrawal logic
}

// v2 - Check removed - WHY?
fn withdraw(&self, amount: BigUint) {
    // Missing balance check! Was this intentional?
    // ... withdrawal logic
}
```

### Modified Logic Analysis
For changed code, verify:
- Edge cases still handled correctly
- Error messages updated appropriately
- Related code paths updated consistently

## 3. Review Workflow

### Step 1: Generate Clean Diff
```bash
# Between git tags/commits
git diff v1.0.0..v2.0.0 -- src/

# Ignore formatting changes
git diff -w v1.0.0..v2.0.0 -- src/

# Focus on specific file
git diff v1.0.0..v2.0.0 -- src/lib.rs
```

### Step 2: Categorize Changes

Create a change inventory:

```markdown
## Change Summary

### Storage Changes
- [ ] user_data struct: Added `reward_multiplier` field (SAFE - appended)
- [ ] New mapper: `feature_flags` (VERIFY: initialized in upgrade)

### Endpoint Changes
- [ ] deposit(): Added token validation (SECURITY FIX)
- [ ] withdraw(): Changed gas calculation (VERIFY: no DoS vector)

### Removed Code
- [ ] legacy_claim(): Removed entire endpoint (VERIFY: no external callers)

### New Code
- [ ] batch_transfer(): New endpoint (FULL REVIEW NEEDED)
```

### Step 3: Trace Data Flow

For each changed data structure:
1. Find all read locations
2. Find all write locations
3. Verify consistency across changes

### Step 4: Verify Test Coverage

```bash
# Check if new code paths are tested
sc-meta test

# Generate test coverage report
cargo tarpaulin --out Html
```

## 4. Security-Specific Diff Checks

### Access Control Changes
```rust
// v1 - Owner only
#[only_owner]
#[endpoint]
fn sensitive_action(&self) { }

// v2 - DANGEROUS: Removed access control
#[endpoint]  // Now public! Was this intentional?
fn sensitive_action(&self) { }
```

### Payment Handling Changes
```rust
// v1 - Validated token
#[payable("*")]
fn deposit(&self) {
    let payment = self.call_value().single_esdt();
    require!(payment.token_identifier == self.accepted_token().get(), "Wrong token");
}

// v2 - DANGEROUS: Removed validation
#[payable("*")]
fn deposit(&self) {
    let payment = self.call_value().single_esdt();
    // Missing token validation! Accepts any token now
}
```

### Arithmetic Changes
```rust
// v1 - Safe arithmetic
let result = a.checked_add(&b).unwrap_or_else(|| sc_panic!("Overflow"));

// v2 - DANGEROUS: Removed overflow protection
let result = a + b;  // Can overflow!
```

## 5. Deliverable Template

```markdown
# Differential Review Report

**Versions Compared**: v1.0.0 → v2.0.0
**Reviewer**: [Name]
**Date**: [Date]

## Summary
[One paragraph overview of changes]

## Critical Findings
1. [Finding with severity and recommendation]

## Storage Compatibility
- [ ] No struct field reordering
- [ ] New mappers initialized in #[upgrade]
- [ ] Storage keys unchanged

## Breaking Changes
| Change | Impact | Migration Required |
|--------|--------|-------------------|
| ... | ... | ... |

## Recommendations
1. [Specific actionable recommendation]
```

## Common Pitfalls

- **Assuming init runs on upgrade**: Always check `#[upgrade]` function
- **Missing storage migration**: Renamed keys lose existing data
- **Removed validations**: Could be intentional security fix or accidental vulnerability
- **Changed math precision**: Can affect existing calculations
- **Modified access control**: Could expose sensitive functions
