---
name: multiversx-fix-verification
description: Rigorously verify that reported vulnerabilities are properly fixed without introducing regressions. Use when reviewing security patches, validating bug fixes, or confirming remediation completeness.
---

# Fix Verification

Rigorously verify that a reported vulnerability has been eliminated without introducing regressions or new issues. This skill ensures fixes are complete, tested, and safe to deploy.

## When to Use

- Reviewing security patches before deployment
- Validating bug fix implementations
- Confirming audit finding remediations
- Re-testing after fix iterations

## 1. The Verification Loop

### Step 1: Reproduce the Bug
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

### Step 2: Apply the Fix
Review the code modification that addresses the vulnerability.

### Step 3: Verify Fix Effectiveness
Run the exploit scenario - it MUST now fail (or behave correctly):

```bash
# The exploit scenario should now pass (exploit blocked)
sc-meta test --scenario scenarios/exploit_before_fix.scen.json
```

### Step 4: Run Regression Suite
ALL existing tests must still pass:

```bash
# Full test suite
sc-meta test

# Or with cargo
cargo test
```

## 2. Common Fix Failures

### Partial Fix
The fix addresses one path but misses variants:

```rust
// VULNERABILITY: Missing amount validation
#[endpoint]
fn deposit(&self) {
    let amount = self.call_value().egld_value();
    // No check for amount > 0
}

// PARTIAL FIX: Only fixed deposit, not transfer
#[endpoint]
fn deposit(&self) {
    let amount = self.call_value().egld_value();
    require!(amount > 0, "Amount must be positive");  // Fixed!
}

#[endpoint]
fn transfer(&self, amount: BigUint) {
    // Still missing amount > 0 check!  <- VARIANT NOT FIXED
}
```

**Verification**: Use `multiversx-variant-analysis` to find all similar code paths.

### Moved Bug (Fix Creates New Issue)
The fix prevents the original exploit but introduces a new vulnerability:

```rust
// VULNERABILITY: Reentrancy
#[endpoint]
fn withdraw(&self) {
    let balance = self.balance().get();
    self.send_egld(&caller, &balance);  // External call before state update
    self.balance().clear();
}

// BAD FIX: Prevents reentrancy but creates DoS
#[endpoint]
fn withdraw(&self) {
    self.locked().set(true);  // Lock added
    let balance = self.balance().get();
    self.send_egld(&caller, &balance);
    self.balance().clear();
    // Missing: self.locked().set(false);  <- LOCK NEVER RELEASED!
}

// CORRECT FIX: Checks-Effects-Interactions pattern
#[endpoint]
fn withdraw(&self) {
    let balance = self.balance().get();
    self.balance().clear();  // State update BEFORE external call
    self.send_egld(&caller, &balance);
}
```

### Incomplete Validation
The fix adds validation but with incorrect conditions:

```rust
// VULNERABILITY: Integer overflow
let total = amount1 + amount2;  // Can overflow

// INCOMPLETE FIX: Checks one but not both
require!(amount1 < MAX_AMOUNT, "Amount1 too large");
let total = amount1 + amount2;  // Still overflows if amount2 is large!

// CORRECT FIX: Checked arithmetic
let total = amount1.checked_add(&amount2)
    .unwrap_or_else(|| sc_panic!("Overflow"));
```

## 3. Verification Checklist

### Code Review
- [ ] Fix addresses the root cause, not just symptoms
- [ ] All code paths with similar patterns are fixed (variant analysis)
- [ ] No new vulnerabilities introduced by the fix
- [ ] Fix follows MultiversX best practices

### Testing
- [ ] Exploit scenario created that fails on vulnerable code
- [ ] Exploit scenario passes (blocked) on fixed code
- [ ] All existing tests pass (no regressions)
- [ ] Edge cases tested (boundary values, empty inputs, max values)

### Documentation
- [ ] Fix commit clearly describes the vulnerability
- [ ] Test scenario documents the attack vector
- [ ] Any behavioral changes documented

## 4. Test Scenario Template

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

## 5. Deliverable: Verification Report

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
- [ ] Searched for similar patterns using `multiversx-variant-analysis`
- [ ] All variants addressed: [list or "none found"]

## Conclusion
**Status**: [VERIFIED / NEEDS WORK / REJECTED]

**Notes**: [Any additional observations]

**Signed**: [Reviewer name, date]
```

## 6. Red Flags During Verification

- Fix is overly complex for the issue
- Fix changes unrelated code
- No test added for the specific vulnerability
- Fix relies on external assumptions
- Gas cost increased significantly
- Access control modified without clear justification
