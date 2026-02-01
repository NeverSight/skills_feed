---
name: multiversx-variant-analysis
description: Multiply audit findings by systematically locating similar vulnerabilities elsewhere in the codebase. Use after finding an initial bug to discover variants, or when creating comprehensive vulnerability reports.
---

# Variant Analysis

Multiply the value of a single vulnerability finding by systematically locating similar issues elsewhere in the codebase. Once you find one bug, this skill helps you find all its "cousins."

## When to Use

- After discovering an initial vulnerability
- During comprehensive security audits
- When creating detection patterns for CI/CD
- Before claiming a bug class is fully remediated
- When assessing the extent of a vulnerability pattern

## 1. The Variant Analysis Process

### From Finding to Pattern

```
1. Find Initial Bug → Specific vulnerability instance
2. Abstract Pattern → What makes this a bug?
3. Create Search    → Grep/Semgrep queries
4. Find Variants    → All similar occurrences
5. Verify Each      → Confirm true positives
6. Report All       → Document the bug class
```

### Example Transformation

**Initial Bug:**
```rust
// Found: Missing payment validation in deposit()
#[payable("*")]
fn deposit(&self) {
    let payment = self.call_value().single_esdt();
    self.balances().update(|b| *b += payment.amount);
    // Bug: No token ID validation!
}
```

**Abstract Pattern:**
- `#[payable("*")]` endpoint
- Uses `call_value()` to get payment
- Does NOT validate `token_identifier`

**Search Query:**
```bash
# Find all payable endpoints
grep -n "#\[payable" src/*.rs

# Then check each for token validation
grep -A 20 "#\[payable" src/*.rs | grep -v "token_identifier"
```

## 2. Common MultiversX Variant Patterns

### Pattern: Missing Payment Validation

**Initial Finding:**
One endpoint accepts payment but doesn't validate the token.

**Variant Search:**
```bash
# Find all payable endpoints
grep -rn "#\[payable" src/

# Check for missing token validation
# Look for call_value() without subsequent token_identifier check
grep -A 30 "#\[payable" src/*.rs > payable_endpoints.txt
# Manually review each for token_identifier validation
```

**Semgrep Rule:**
```yaml
rules:
  - id: mvx-payable-no-token-check
    patterns:
      - pattern: |
          #[payable("*")]
          $ANNOTATIONS
          fn $FUNC(&self, $...PARAMS) {
              $...BODY
          }
      - pattern-not: |
          #[payable("*")]
          $ANNOTATIONS
          fn $FUNC(&self, $...PARAMS) {
              <... token_identifier ...>
          }
```

### Pattern: Unbounded Iteration

**Initial Finding:**
One function iterates over a `VecMapper` without bounds.

**Variant Search:**
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

### Pattern: Callback State Assumptions

**Initial Finding:**
One callback doesn't handle the error case.

**Variant Search:**
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

### Pattern: Missing Access Control

**Initial Finding:**
One admin function lacks `#[only_owner]`.

**Variant Search:**
```bash
# Find functions that modify admin-like storage
grep -rn "admin\|owner\|config\|fee" src/ | grep "\.set("

# Cross-reference with access control
grep -B 10 "admin.*\.set\|config.*\.set" src/*.rs | grep -v "only_owner"
```

### Pattern: Arithmetic Without Checks

**Initial Finding:**
One calculation uses raw `+` instead of `checked_add`.

**Variant Search:**
```bash
# Find all arithmetic operations
grep -rn " + \| - \| \* " src/*.rs

# Exclude test files and comments
grep -rn " + \| - \| \* " src/*.rs | grep -v "test\|//"
```

## 3. Systematic Variant Hunting

### Step 1: Characterize the Bug

Answer these questions:
1. What is the vulnerable code pattern?
2. What makes it exploitable?
3. What would a fix look like?

### Step 2: Create Detection Queries

**Grep-based:**
```bash
# Pattern: [specific code pattern]
grep -rn "[pattern]" src/

# Negative pattern (should be present but isn't)
grep -L "[expected_pattern]" src/*.rs
```

**Semgrep-based:**
```yaml
# See multiversx-semgrep-creator skill for details
rules:
  - id: variant-pattern
    patterns:
      - pattern: <vulnerable pattern>
      - pattern-not: <fixed pattern>
```

### Step 3: Triage Results

For each potential variant:

| Result | Classification | Action |
|--------|----------------|--------|
| Clearly vulnerable | True Positive | Report |
| Needs context | Investigate | Manual review |
| Has mitigation | False Positive | Document why |
| Different pattern | Not a variant | Skip |

### Step 4: Document Findings

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

## 4. Automation for Future Prevention

### Convert to CI/CD Check

After finding variants, create automated detection:

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

### Create Semgrep Rule

See `multiversx-semgrep-creator` skill:

```yaml
rules:
  - id: mvx-[bug-class]-[id]
    languages: [rust]
    message: "[Description of bug class]"
    severity: ERROR
    patterns:
      - pattern: <vulnerable pattern>
```

## 5. Variant Analysis Checklist

After finding any bug:

- [ ] Abstract the pattern (what makes it a bug?)
- [ ] Create search queries (grep, semgrep)
- [ ] Search entire codebase
- [ ] Triage each result (TP/FP/needs investigation)
- [ ] Verify true positives are exploitable
- [ ] Document all variants
- [ ] Create prevention rule for CI/CD
- [ ] Recommend fix for all instances

## 6. Common Variant Categories

### Input Validation Variants
- Missing in one endpoint → Check ALL endpoints
- Missing for one parameter → Check ALL parameters

### Access Control Variants
- Missing on one admin function → Check ALL admin functions
- Inconsistent role checks → Audit entire role system

### State Management Variants
- Reentrancy in one function → Check ALL external calls
- Missing callback handling → Check ALL callbacks

### Arithmetic Variants
- Overflow in one calculation → Check ALL math operations
- Precision loss in one formula → Check ALL division operations

## 7. Reporting Multiple Variants

### Consolidated Report

When multiple variants exist, consolidate:

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

...

## Recommended Fix
[Generic fix pattern]

```rust
// Before (vulnerable)
[vulnerable code]

// After (fixed)
[fixed code]
```

## Prevention
[How to prevent this class of bugs in the future]
```

### Severity Aggregation

| Individual Severity | Count | Aggregate Severity |
|---------------------|-------|-------------------|
| Critical | 3+ | Critical |
| High | 5+ | Critical |
| Medium | 10+ | High |
| Low | Any | Low |

## 8. Example: Complete Variant Analysis

**Initial Bug: Missing amount validation in stake()**

```rust
// Found in stake.rs:45
#[payable("EGLD")]
fn stake(&self) {
    let payment = self.call_value().egld_value();
    // Bug: No check for amount > 0
    self.staked().update(|s| *s += payment.clone_value());
}
```

**Pattern: Missing amount > 0 check on payable endpoint**

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
    let payment = self.call_value().egld_value();
    require!(payment.clone_value() > 0, "Amount must be positive");
    self.staked().update(|s| *s += payment.clone_value());
}
```

**CI Rule Created:** `rules/mvx-amount-validation.yaml`
