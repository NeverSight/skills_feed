---
name: multiversx-spec-compliance
description: Verify smart contract implementations match their specifications, whitepapers, and MIP standards. Use when auditing for specification adherence, validating tokenomics implementations, or checking MIP compliance.
---

# Specification Compliance Verification

Ensure that MultiversX smart contract implementations match their intended design as specified in whitepapers, technical specifications, and MultiversX Improvement Proposals (MIPs). This skill bridges the gap between documentation and code.

## When to Use

- Auditing contracts against their whitepapers
- Verifying tokenomics implementations
- Checking MIP standard compliance
- Validating economic formulas and constraints
- Reviewing upgrade proposals against specs

## 1. Verification Process Overview

### Inputs Required

| Input | Description | Source |
|-------|-------------|--------|
| Code | Rust implementation | `src/*.rs` |
| Specification | Design document | `whitepaper.pdf`, `README.md`, `specs/` |
| MIP Reference | Standard requirements | MultiversX MIPs |

### Process Flow

```
1. Extract Claims → List all requirements from spec
2. Map to Code   → Find implementing code for each claim
3. Verify Logic  → Confirm implementation matches spec
4. Document      → Record findings and deviations
```

## 2. Claim Extraction

### Specification Language Keywords

Extract statements containing these keywords:

| Keyword | Meaning | Example |
|---------|---------|---------|
| MUST | Required | "Users MUST stake minimum 100 tokens" |
| MUST NOT | Forbidden | "Admin MUST NOT withdraw user funds" |
| SHOULD | Recommended | "Contract SHOULD emit events" |
| SHALL | Obligation | "Rewards SHALL be calculated daily" |
| MAY | Optional | "Users MAY delegate to multiple validators" |

### Example Claim Extraction

**From Whitepaper:**
> "The staking contract MUST enforce a minimum stake of 1000 EGLD.
> Rewards MUST be calculated using APY = base_rate * (1 + boost_factor).
> Users MUST NOT be able to withdraw during the lock period."

**Extracted Claims:**
```markdown
1. [MUST] Minimum stake: 1000 EGLD
2. [MUST] Reward formula: APY = base_rate * (1 + boost_factor)
3. [MUST NOT] Withdrawal during lock period
```

### Claim Documentation Template

```markdown
| ID | Type | Claim | Source | Code Location | Status |
|----|------|-------|--------|---------------|--------|
| C1 | MUST | Min stake 1000 EGLD | WP §3.1 | stake.rs:45 | Verified |
| C2 | MUST | APY formula | WP §4.2 | rewards.rs:78 | Deviation |
| C3 | MUST NOT | Lock withdrawal | WP §3.3 | withdraw.rs:23 | Verified |
```

## 3. Code Mapping

### Finding Implementing Code

For each claim, locate the relevant code:

```rust
// Claim C1: Min stake 1000 EGLD
// Location: src/stake.rs:45

const MIN_STAKE: u64 = 1000_000000000000000000u64;  // 1000 EGLD in wei

#[payable("EGLD")]
#[endpoint]
fn stake(&self) {
    let payment = self.call_value().egld_value();
    require!(
        payment.clone_value() >= BigUint::from(MIN_STAKE),
        "Minimum stake is 1000 EGLD"  // ← Implements C1
    );
    // ...
}
```

### Mapping Checklist

For each claim:
- [ ] Code location identified
- [ ] Implementation logic understood
- [ ] Constants/values match spec
- [ ] Edge cases handled per spec

## 4. Verification Techniques

### Formula Verification

**Spec:**
> "APY = base_rate * (1 + boost_factor)"

**Code Review:**
```rust
fn calculate_apy(&self, base_rate: BigUint, boost_factor: BigUint) -> BigUint {
    // Verify this matches: APY = base_rate * (1 + boost_factor)

    let one = BigUint::from(PRECISION);  // Check: What is PRECISION?
    let boost_multiplier = &one + &boost_factor;
    let apy = &base_rate * &boost_multiplier / &one;

    // QUESTION: Is division by PRECISION correct? Spec doesn't mention it.
    // FINDING: Precision handling not in spec - potential deviation

    apy
}
```

### Constraint Verification

**Spec:**
> "Users MUST NOT withdraw during the lock period of 7 days"

**Code Review:**
```rust
#[endpoint]
fn withdraw(&self) {
    let stake_time = self.stake_timestamp(&caller).get();
    let current_time = self.blockchain().get_block_timestamp();
    let lock_period = self.lock_period().get();  // Check: Is this 7 days?

    require!(
        current_time >= stake_time + lock_period,
        "Lock period not elapsed"
    );
    // ...
}

// VERIFICATION NEEDED:
// 1. Is lock_period initialized to 7 days (604800 seconds)?
// 2. Is lock_period immutable or can admin change it?
// 3. Can this be bypassed through any other endpoint?
```

### State Transition Verification

**Spec:**
> "State transitions: INACTIVE → ACTIVE → COMPLETED"

**Code Review:**
```rust
#[derive(TopEncode, TopDecode, TypeAbi, PartialEq)]
pub enum State {
    Inactive,
    Active,
    Completed,
}

fn activate(&self) {
    let current = self.state().get();
    require!(current == State::Inactive, "Can only activate from Inactive");
    self.state().set(State::Active);
}

fn complete(&self) {
    let current = self.state().get();
    require!(current == State::Active, "Can only complete from Active");
    self.state().set(State::Completed);
}

// VERIFICATION:
// ✓ Inactive → Active (activate)
// ✓ Active → Completed (complete)
// ? Is there a way to go backwards? (Should not be allowed)
// ? Can state be set directly? (Search for .set(State::))
```

## 5. MultiversX MIP Compliance

### Common MIPs to Verify

| MIP | Topic | Key Requirements |
|-----|-------|------------------|
| MIP-2 | Semi-Fungible Tokens | SFT metadata format, royalties |
| MIP-3 | Dynamic NFTs | Attribute update mechanisms |
| MIP-4 | Royalties | Royalty calculation and distribution |

### MIP-2 SFT Compliance Example

**Requirements:**
- Token type must be SFT (nonce > 0, quantity > 1 allowed)
- Metadata format follows standard
- Royalties encoded correctly

**Verification:**
```rust
// Check NFT creation follows MIP-2

#[endpoint]
fn create_sft(&self, ...) -> u64 {
    // VERIFY: Using NonFungibleTokenMapper correctly
    let nonce = self.sft_token().nft_create(
        initial_quantity,  // MIP-2: Must allow quantity > 1
        &SftAttributes {
            // MIP-2: Required attributes
            name: ...,
            royalties: ...,  // In basis points (0-10000)
            hash: ...,
            attributes: ...,
            uris: ...,
        }
    );
    nonce
}
```

## 6. Tokenomics Verification

### Common Tokenomics Claims

| Claim Type | Example | Verification |
|------------|---------|--------------|
| Total Supply | Max 1B tokens | Check mint constraints |
| Inflation Rate | 5% annually | Verify mint formula |
| Burn Rate | 1% per transfer | Check fee calculation |
| Distribution | 40% community | Verify initial allocation |

### Example: Inflation Verification

**Spec:**
> "Annual inflation rate is 5%, calculated per epoch"

**Code Review:**
```rust
const ANNUAL_INFLATION_BPS: u64 = 500;  // 5% = 500 basis points
const EPOCHS_PER_YEAR: u64 = 365;       // Assuming daily epochs

fn calculate_epoch_inflation(&self) -> BigUint {
    let total_supply = self.total_supply().get();
    let epoch_rate = ANNUAL_INFLATION_BPS / EPOCHS_PER_YEAR;

    // VERIFICATION:
    // 500 / 365 = 1.369... but integer division = 1
    // This is LESS than 5% annually (365 * 1 = 365 bps = 3.65%)
    // FINDING: Integer precision loss causes ~27% less inflation than spec

    &total_supply * BigUint::from(epoch_rate) / BigUint::from(10000u64)
}
```

## 7. Deviation Handling

### Deviation Categories

| Category | Severity | Action |
|----------|----------|--------|
| Critical | Breaks core functionality | Must fix |
| Major | Significant difference | Should fix |
| Minor | Slight variation | Document |
| Enhancement | Beyond spec | Document |

### Deviation Report Template

```markdown
## Deviation Report

### DEV-001: Inflation Calculation Precision Loss

**Claim**: Annual inflation rate is 5%
**Source**: Whitepaper §5.2
**Code**: rewards.rs:calculate_epoch_inflation()

**Expected**: 5.00% annual inflation
**Actual**: 3.65% annual inflation

**Root Cause**: Integer division of basis points by epochs
loses precision (500/365 = 1, not 1.369)

**Impact**: ~27% less inflation than documented

**Recommendation**: Use scaled arithmetic
```rust
// Instead of:
let epoch_rate = ANNUAL_INFLATION_BPS / EPOCHS_PER_YEAR;

// Use:
let scaled_annual = BigUint::from(ANNUAL_INFLATION_BPS) * &total_supply;
let epoch_inflation = scaled_annual / BigUint::from(EPOCHS_PER_YEAR) / BigUint::from(10000u64);
```

**Severity**: Major
**Status**: Open
```

## 8. Compliance Report Template

```markdown
# Specification Compliance Report

**Project**: [Name]
**Specification Version**: [Version]
**Code Version**: [Commit/Tag]
**Date**: [Date]
**Auditor**: [Name]

## Executive Summary
[Brief overview of compliance status]

## Specification Coverage

| Section | Claims | Verified | Deviations | Not Found |
|---------|--------|----------|------------|-----------|
| §3 Staking | 12 | 10 | 1 | 1 |
| §4 Rewards | 8 | 7 | 1 | 0 |
| §5 Governance | 5 | 5 | 0 | 0 |
| **Total** | **25** | **22** | **2** | **1** |

## Verified Claims
[List of all verified claims with code references]

## Deviations
[Detailed deviation reports]

## Unimplemented Claims
[Claims from spec not found in code]

## MIP Compliance
| MIP | Status | Notes |
|-----|--------|-------|
| MIP-2 | Compliant | - |
| MIP-4 | Partial | Royalty distribution differs |

## Recommendations
1. [Priority recommendation]
2. [Second priority]

## Conclusion
[Overall compliance assessment]
```

## 9. Best Practices

1. **Get the right spec version**: Ensure code and spec versions match
2. **Document assumptions**: When spec is ambiguous, document interpretation
3. **Test boundary values**: Verify spec limits are correctly implemented
4. **Check units**: EGLD vs wei, seconds vs epochs, basis points vs percentages
5. **Verify precision**: BigUint calculations should maintain precision
6. **Review change history**: Check if spec evolved and code was updated
