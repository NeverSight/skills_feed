---
name: multiversx-code-analysis
description: Comprehensive code analysis toolkit for MultiversX smart contracts. Covers differential review (version comparison, upgrade safety), fix verification (validate patches, regression testing), and variant analysis (find similar bugs across codebase). Use when reviewing PRs, verifying security patches, or hunting for bug variants.
---

# MultiversX Code Analysis

Toolkit for analyzing MultiversX smart contract code changes, verifying fixes, and finding bug variants across codebases.

## When to Use

- Reviewing pull requests with contract changes
- Auditing upgrade proposals before deployment
- Verifying security patches and bug fixes
- Finding similar vulnerabilities across the codebase
- Creating comprehensive vulnerability reports

---

## Section 1: Differential Review

Analyze differences between two versions of a MultiversX codebase, focusing on security implications of changes, storage layout compatibility, and upgrade safety.

### 1.1 Upgradeability Checks (MultiversX-Specific)

#### Storage Layout Compatibility

**CRITICAL**: Storage layout changes can corrupt existing data.

##### Struct Field Ordering
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

##### Storage Mapper Key Changes
```rust
// v1
#[storage_mapper("user_balance")]
fn user_balance(&self, user: &ManagedAddress) -> SingleValueMapper<BigUint>;

// v2 - DANGEROUS: Changed storage key
#[storage_mapper("userBalance")]  // Different key = new empty storage!
fn user_balance(&self, user: &ManagedAddress) -> SingleValueMapper<BigUint>;
```

#### Initialization on Upgrade

**CRITICAL**: `#[init]` is NOT called on upgrade. Only `#[upgrade]` runs.

```rust
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

#### Breaking Changes Checklist

| Change Type | Risk | Mitigation |
|------------|------|------------|
| Struct field reorder | Critical | Never reorder, only append |
| Storage key rename | Critical | Keep old key, migrate data |
| New required storage | High | Initialize in `#[upgrade]` |
| Removed endpoint | Medium | Ensure no external dependencies |
| Changed endpoint signature | Medium | Version API or maintain compatibility |
| New validation rules | Medium | Consider existing state validity |

### 1.2 Regression Analysis

#### New Features Impact
- Do new features break existing invariants?
- Are there new attack vectors introduced?
- Do gas costs change significantly?

#### Deleted Code Analysis
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

#### Modified Logic Analysis
For changed code, verify:
- Edge cases still handled correctly
- Error messages updated appropriately
- Related code paths updated consistently

### 1.3 Review Workflow

#### Step 1: Generate Clean Diff
```bash
# Between git tags/commits
git diff v1.0.0..v2.0.0 -- src/

# Ignore formatting changes
git diff -w v1.0.0..v2.0.0 -- src/

# Focus on specific file
git diff v1.0.0..v2.0.0 -- src/lib.rs
```

#### Step 2: Categorize Changes

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

#### Step 3: Trace Data Flow

For each changed data structure:
1. Find all read locations
2. Find all write locations
3. Verify consistency across changes

#### Step 4: Verify Test Coverage

```bash
# Check if new code paths are tested
sc-meta test

# Generate test coverage report
cargo tarpaulin --out Html
```

### 1.4 Security-Specific Diff Checks

#### Access Control Changes
```rust
// v1 - Owner only
#[only_owner]
#[endpoint]
fn sensitive_action(&self) { }

// v2 - DANGEROUS: Removed access control
#[endpoint]  // Now public! Was this intentional?
fn sensitive_action(&self) { }
```

#### Payment Handling Changes
```rust
// v1 - Validated token
#[payable]
fn deposit(&self) {
    let payment = self.call_value().single();
    require!(payment.token_identifier == self.accepted_token().get(), "Wrong token");
}

// v2 - DANGEROUS: Removed validation
#[payable]
fn deposit(&self) {
    let payment = self.call_value().single();
    // Missing token validation! Accepts any token now
}
```

#### Arithmetic Changes
```rust
// v1 - Safe arithmetic
let result = a.checked_add(&b).unwrap_or_else(|| sc_panic!("Overflow"));

// v2 - DANGEROUS: Removed overflow protection
let result = a + b;  // Can overflow!
```

### 1.5 Differential Review Output Template

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

### Common Pitfalls

- **Assuming init runs on upgrade**: Always check `#[upgrade]` function
- **Missing storage migration**: Renamed keys lose existing data
- **Removed validations**: Could be intentional security fix or accidental vulnerability
- **Changed math precision**: Can affect existing calculations
- **Modified access control**: Could expose sensitive functions

---

## Section 2: Fix Verification

Rigorously verify that a reported vulnerability has been eliminated without introducing regressions or new issues.

### 2.1 The Verification Loop

#### Step 1: Reproduce the Bug
Create a test scenario that demonstrates the vulnerability:

```json
// scenarios/exploit_before_fix.scen.json
{
    "name": "Demonstrate vulnerability - should fail before fix",
    "steps": [
        {
            "step": "scCall",
            "comment": "Attacker exploits the vulnerability",
            "tx": {
                "from": "address:attacker",
                "to": "sc:vulnerable_contract",
                "function": "vulnerable_endpoint",
                "arguments": ["...exploit_payload..."],
                "gasLimit": "5,000,000"
            },
            "expect": {
                "status": "0",
                "message": "*"
            }
        }
    ]
}
```

#### Step 2: Apply the Fix
Review the code modification that addresses the vulnerability.

#### Step 3: Verify Fix Effectiveness
Run the exploit scenario — it MUST now fail (or behave correctly):

```bash
# The exploit scenario should now pass (exploit blocked)
sc-meta test --scenario scenarios/exploit_before_fix.scen.json
```

#### Step 4: Run Regression Suite
ALL existing tests must still pass:

```bash
# Full test suite
sc-meta test

# Or with cargo
cargo test
```

### 2.2 Common Fix Failures

#### Partial Fix
The fix addresses one path but misses variants:

```rust
// VULNERABILITY: Missing amount validation
#[endpoint]
fn deposit(&self) {
    let amount = self.call_value().egld();
    // No check for amount > 0
}

// PARTIAL FIX: Only fixed deposit, not transfer
#[endpoint]
fn deposit(&self) {
    let amount = self.call_value().egld();
    require!(amount > 0, "Amount must be positive");  // Fixed!
}

#[endpoint]
fn transfer(&self, amount: BigUint) {
    // Still missing amount > 0 check!  <- VARIANT NOT FIXED
}
```

**Verification**: Use variant analysis (Section 3) to find all similar code paths.

#### Moved Bug (Fix Creates New Issue)

```rust
// VULNERABILITY: Reentrancy
#[endpoint]
fn withdraw(&self) {
    let balance = self.balance().get();
    self.tx().to(&caller).egld(&balance).transfer();  // External call before state update
    self.balance().clear();
}

// BAD FIX: Prevents reentrancy but creates DoS
#[endpoint]
fn withdraw(&self) {
    self.locked().set(true);  // Lock added
    let balance = self.balance().get();
    self.tx().to(&caller).egld(&balance).transfer();
    self.balance().clear();
    // Missing: self.locked().set(false);  <- LOCK NEVER RELEASED!
}

// CORRECT FIX: Checks-Effects-Interactions pattern
#[endpoint]
fn withdraw(&self) {
    let balance = self.balance().get();
    self.balance().clear();  // State update BEFORE external call
    self.tx().to(&caller).egld(&balance).transfer();
}
```

#### Incomplete Validation

```rust
// VULNERABILITY: Integer overflow
let total = amount1 + amount2;  // Can overflow

// INCOMPLETE FIX: Checks one but not both
require!(amount1 < MAX_AMOUNT, "Amount1 too large");
let total = amount1 + amount2;  // Still overflows if amount2 is large!

// CORRECT FIX: BigUint is arbitrary precision (no overflow), but validate bounds
let total = &amount1 + &amount2;
require!(total <= BigUint::from(MAX_ALLOWED), "Amount exceeds maximum");
```

### 2.3 Verification Checklist

#### Code Review
- [ ] Fix addresses the root cause, not just symptoms
- [ ] All code paths with similar patterns are fixed (variant analysis)
- [ ] No new vulnerabilities introduced by the fix
- [ ] Fix follows MultiversX best practices

#### Testing
- [ ] Exploit scenario created that fails on vulnerable code
- [ ] Exploit scenario passes (blocked) on fixed code
- [ ] All existing tests pass (no regressions)
- [ ] Edge cases tested (boundary values, empty inputs, max values)

#### Documentation
- [ ] Fix commit clearly describes the vulnerability
- [ ] Test scenario documents the attack vector
- [ ] Any behavioral changes documented

### 2.4 Test Scenario Template

```json
{
    "name": "Verify fix for [VULNERABILITY_ID]",
    "comment": "This scenario verifies that [DESCRIPTION] is properly fixed",
    "steps": [
        {
            "step": "setState",
            "comment": "Setup vulnerable state",
            "accounts": {
                "address:attacker": { "nonce": "0", "balance": "1000" },
                "sc:contract": { "code": "file:output/contract.wasm" }
            }
        },
        {
            "step": "scCall",
            "comment": "Attempt exploit - should fail after fix",
            "tx": {
                "from": "address:attacker",
                "to": "sc:contract",
                "function": "vulnerable_function",
                "arguments": ["exploit_input"]
            },
            "expect": {
                "status": "4",
                "message": "str:Expected error message"
            }
        },
        {
            "step": "checkState",
            "comment": "Verify state unchanged (exploit blocked)",
            "accounts": {
                "sc:contract": {
                    "storage": {
                        "str:sensitive_value": "original_value"
                    }
                }
            }
        }
    ]
}
```

### 2.5 Verification Report Template

```markdown
# Fix Verification Report

## Vulnerability Reference
- **ID**: [CVE/Internal ID]
- **Severity**: [Critical/High/Medium/Low]
- **Description**: [Brief description]

## Fix Details
- **Commit**: [git commit hash]
- **Files Changed**: [list of files]
- **Approach**: [Description of fix approach]

## Verification Results

### Exploit Reproduction
- [ ] Exploit scenario created: `scenarios/[name].scen.json`
- [ ] Scenario fails on vulnerable code (commit: [hash])
- [ ] Scenario passes on fixed code (commit: [hash])

### Regression Testing
- [ ] All existing tests pass
- [ ] No new warnings from `cargo clippy`
- [ ] Gas costs within acceptable range

### Variant Analysis
- [ ] Searched for similar patterns using variant analysis
- [ ] All variants addressed: [list or "none found"]

## Conclusion
**Status**: [VERIFIED / NEEDS WORK / REJECTED]

**Notes**: [Any additional observations]

**Signed**: [Reviewer name, date]
```

### 2.6 Red Flags During Verification

- Fix is overly complex for the issue
- Fix changes unrelated code
- No test added for the specific vulnerability
- Fix relies on external assumptions
- Gas cost increased significantly
- Access control modified without clear justification

---

## Section 3: Variant Analysis

Multiply the value of a single vulnerability finding by systematically locating similar issues elsewhere in the codebase.

### 3.1 The Variant Analysis Process

```
1. Find Initial Bug → Specific vulnerability instance
2. Abstract Pattern → What makes this a bug?
3. Create Search    → Grep/Semgrep queries
4. Find Variants    → All similar occurrences
5. Verify Each      → Confirm true positives
6. Report All       → Document the bug class
```

### 3.2 Common MultiversX Variant Patterns

#### Pattern: Missing Payment Validation

**Variant Search:**
```bash
# Find all payable endpoints
grep -rn "#\[payable" src/

# Check for missing token validation
grep -A 30 "#\[payable" src/*.rs > payable_endpoints.txt
# Manually review each for token_identifier validation
```

**Semgrep Rule:**
```yaml
rules:
  - id: mvx-payable-no-token-check
    patterns:
      - pattern: |
          #[payable]
          $ANNOTATIONS
          fn $FUNC(&self, $...PARAMS) {
              $...BODY
          }
      - pattern-not: |
          #[payable]
          $ANNOTATIONS
          fn $FUNC(&self, $...PARAMS) {
              <... token_identifier ...>
          }
```

#### Pattern: Unbounded Iteration

```bash
# Find all .iter() calls on storage mappers
grep -rn "\.iter()" src/

# Find all for loops over storage
grep -rn "for.*in.*self\." src/
```

**Checklist for Each:**
- [ ] Is iteration bounded?
- [ ] Can a user grow the collection?
- [ ] Is there pagination?

#### Pattern: Callback State Assumptions

```bash
# Find all callbacks
grep -rn "#\[callback\]" src/

# Check for proper result handling
grep -A 20 "#\[callback\]" src/*.rs | grep -c "ManagedAsyncCallResult"
```

**All Callbacks Need:**
```rust
#[callback]
fn any_callback(&self, #[call_result] result: ManagedAsyncCallResult<T>) {
    match result {
        ManagedAsyncCallResult::Ok(_) => { /* success */ },
        ManagedAsyncCallResult::Err(_) => { /* handle failure! */ }
    }
}
```

#### Pattern: Missing Access Control

```bash
# Find functions that modify admin-like storage
grep -rn "admin\|owner\|config\|fee" src/ | grep "\.set("

# Cross-reference with access control
grep -B 10 "admin.*\.set\|config.*\.set" src/*.rs | grep -v "only_owner"
```

#### Pattern: Arithmetic Without Checks

```bash
# Find all arithmetic operations
grep -rn " + \| - \| \* " src/*.rs

# Exclude test files and comments
grep -rn " + \| - \| \* " src/*.rs | grep -v "test\|//"
```

### 3.3 Systematic Variant Hunting

#### Step 1: Characterize the Bug

Answer these questions:
1. What is the vulnerable code pattern?
2. What makes it exploitable?
3. What would a fix look like?

#### Step 2: Create Detection Queries

**Grep-based:**
```bash
# Pattern: [specific code pattern]
grep -rn "[pattern]" src/

# Negative pattern (should be present but isn't)
grep -L "[expected_pattern]" src/*.rs
```

**Semgrep-based:**
```yaml
rules:
  - id: variant-pattern
    patterns:
      - pattern: <vulnerable pattern>
      - pattern-not: <fixed pattern>
```

#### Step 3: Triage Results

| Result | Classification | Action |
|--------|----------------|--------|
| Clearly vulnerable | True Positive | Report |
| Needs context | Investigate | Manual review |
| Has mitigation | False Positive | Document why |
| Different pattern | Not a variant | Skip |

#### Step 4: Document Findings

```markdown
## Variant Analysis: [Bug Class Name]

### Initial Finding
- Location: [file:line]
- Description: [what's wrong]

### Pattern Description
[Abstract description of what makes this a bug]

### Search Method
```bash
[grep/semgrep commands used]
```

### Variants Found

| Location | Status | Notes |
|----------|--------|-------|
| file1.rs:23 | Confirmed | Same pattern |
| file2.rs:45 | Confirmed | Slight variation |
| file3.rs:67 | FP | Has validation elsewhere |

### Remediation
[How to fix all instances]
```

### 3.4 Automation for Future Prevention

#### Convert to CI/CD Check

```yaml
# .github/workflows/security.yml
- name: Check for vulnerability patterns
  run: |
    # Run semgrep with custom rules
    semgrep --config rules/mvx-security.yaml src/

    # Grep-based checks
    if grep -rn "unsafe_pattern" src/; then
      echo "Found potential vulnerability"
      exit 1
    fi
```

### 3.5 Variant Analysis Checklist

After finding any bug:

- [ ] Abstract the pattern (what makes it a bug?)
- [ ] Create search queries (grep, semgrep)
- [ ] Search entire codebase
- [ ] Triage each result (TP/FP/needs investigation)
- [ ] Verify true positives are exploitable
- [ ] Document all variants
- [ ] Create prevention rule for CI/CD
- [ ] Recommend fix for all instances

### 3.6 Common Variant Categories

#### Input Validation Variants
- Missing in one endpoint → Check ALL endpoints
- Missing for one parameter → Check ALL parameters

#### Access Control Variants
- Missing on one admin function → Check ALL admin functions
- Inconsistent role checks → Audit entire role system

#### State Management Variants
- Reentrancy in one function → Check ALL external calls
- Missing callback handling → Check ALL callbacks

#### Arithmetic Variants
- Overflow in one calculation → Check ALL math operations
- Precision loss in one formula → Check ALL division operations

### 3.7 Reporting Multiple Variants

#### Consolidated Report

```markdown
# Bug Class: [Name]

## Summary
Found [N] instances of [bug description] across the codebase.

## Root Cause
[Why this pattern is vulnerable]

## Instances

### Instance 1 (file1.rs:23)
[Details]

### Instance 2 (file2.rs:45)
[Details]

## Recommended Fix
[Generic fix pattern]

## Prevention
[How to prevent this class of bugs in the future]
```

#### Severity Aggregation

| Individual Severity | Count | Aggregate Severity |
|---------------------|-------|-------------------|
| Critical | 3+ | Critical |
| High | 5+ | Critical |
| Medium | 10+ | High |
| Low | Any | Low |

### 3.8 Example: Complete Variant Analysis

**Initial Bug: Missing amount validation in stake()**

```rust
// Found in stake.rs:45
#[payable("EGLD")]
fn stake(&self) {
    let payment = self.call_value().egld();
    // Bug: No check for amount > 0
    self.staked().update(|s| *s += payment.amount.as_big_uint());
}
```

**Pattern: Missing amount > 0 check on payable endpoint**

> **Note**: With SDK v0.64+ Payment type, `amount` is `NonZeroBigUint` — the `> 0` check is redundant for typed payments. The pattern below applies to older SDK versions or raw `call_value()` usage.

**Search:**
```bash
grep -rn "#\[payable" src/ | cut -d: -f1 | sort -u | while read file; do
    echo "=== $file ==="
    grep -A 30 "#\[payable" "$file" | head -40
done > payable_review.txt
```

**Variants Found:**
1. `stake.rs:45` - stake() - CONFIRMED
2. `stake.rs:78` - add_stake() - CONFIRMED
3. `rewards.rs:23` - deposit_rewards() - CONFIRMED
4. `fees.rs:12` - pay_fee() - FALSE POSITIVE (has check on line 15)

**Fix Applied to All:**
```rust
#[payable("EGLD")]
fn stake(&self) {
    let payment = self.call_value().egld();
    require!(payment.amount.as_big_uint() > 0, "Amount must be positive");
    self.staked().update(|s| *s += payment.amount.as_big_uint());
}
```

**CI Rule Created:** `rules/mvx-amount-validation.yaml`
