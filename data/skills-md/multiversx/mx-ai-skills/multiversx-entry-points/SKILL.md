---
name: multiversx-entry-points
description: Systematically identify and analyze all smart contract entry points for attack surface mapping. Use when starting security reviews, documenting contract interfaces, or assessing access control coverage.
---

# MultiversX Entry Point Analyzer

Identify the complete attack surface of a MultiversX smart contract by enumerating all public interaction points and classifying their risk levels. This is typically the first step in any security review.

## When to Use

- Starting a new security audit
- Documenting contract public interface
- Assessing access control coverage
- Mapping data flow through the contract
- Identifying high-risk endpoints for focused review

## 1. Entry Point Identification

### MultiversX Macros That Expose Functions

| Macro | Visibility | Risk Level | Description |
|-------|-----------|------------|-------------|
| `#[endpoint]` | Public write | High | State-changing public function |
| `#[view]` | Public read | Low | Read-only public function |
| `#[payable("*")]` | Accepts any token | Critical | Handles value transfers |
| `#[payable("EGLD")]` | Accepts EGLD only | Critical | Handles native currency |
| `#[init]` | Deploy only | Medium | Constructor (runs once) |
| `#[upgrade]` | Upgrade only | Critical | Migration logic |
| `#[callback]` | Internal | High | Async call response handler |
| `#[only_owner]` | Owner restricted | Medium | Admin functions |

### Scanning Commands
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

## 2. Risk Classification

### Category A: Payable Endpoints (Critical Risk)

Functions receiving value require the most scrutiny.

```rust
#[payable("*")]
#[endpoint]
fn deposit(&self) {
    // MUST CHECK:
    // 1. Token identifier validation
    // 2. Amount > 0 validation
    // 3. Correct handling of multi-token transfers
    // 4. State updates before external calls

    let payment = self.call_value().single_esdt();
    require!(
        payment.token_identifier == self.accepted_token().get(),
        "Wrong token"
    );
    require!(payment.amount > 0, "Zero amount");

    // Process deposit...
}
```

**Checklist for Payable Endpoints:**
- [ ] Token ID validated against expected token(s)
- [ ] Amount checked for minimum/maximum bounds
- [ ] Multi-transfer handling if `all_esdt_transfers()` used
- [ ] Nonce validation for NFT/SFT
- [ ] Reentrancy protection (Checks-Effects-Interactions)

### Category B: Non-Payable State-Changing Endpoints (High Risk)

Functions that modify state without payment.

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

### Category C: View Functions (Low Risk)

Read-only functions, but still need review.

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
- [ ] Block info usage appropriate (`get_block_timestamp()` may differ off-chain)

### Category D: Init and Upgrade (Critical Risk)

Lifecycle functions with special considerations.

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

### Category E: Callbacks (High Risk)

Async call handlers with specific vulnerabilities.

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

## 3. Analysis Workflow

### Step 1: List All Entry Points

Create an inventory table:

```markdown
| Endpoint | Type | Payable | Access | Storage Touched | Risk |
|----------|------|---------|--------|-----------------|------|
| deposit | endpoint | * | Public | balances | Critical |
| withdraw | endpoint | No | Public | balances | Critical |
| setAdmin | endpoint | No | Owner | admin | High |
| getBalance | view | No | Public | balances (read) | Low |
| init | init | No | Deploy | admin, config | Medium |
```

### Step 2: Tag Access Control

For each endpoint, document who can call it:

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

### Step 3: Tag Value Handling

Classify how each endpoint handles value:

| Tag | Meaning | Example |
|-----|---------|---------|
| Refusable | Rejects payments | Default (no `#[payable]`) |
| EGLD Only | Accepts EGLD | `#[payable("EGLD")]` |
| Token Only | Specific ESDT | `#[payable("TOKEN-abc123")]` |
| Any Token | Any payment | `#[payable("*")]` |
| Multi-Token | Multiple payments | Uses `all_esdt_transfers()` |

### Step 4: Graph Data Flow

Map which storage mappers each endpoint reads/writes:

```
deposit() ──writes──▶ balances
          ──writes──▶ total_deposited
          ──reads───▶ accepted_token

withdraw() ──reads/writes──▶ balances
           ──reads────────▶ withdrawal_fee

getBalance() ──reads──▶ balances
```

## 4. Specific Attack Vectors

### Privilege Escalation
Is a sensitive endpoint accidentally public?

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

### DoS via Unbounded Growth
Can public endpoints cause unbounded storage growth?

```rust
// VULNERABLE: Public endpoint adds to unbounded set
#[endpoint]
fn register(&self) {
    let caller = self.blockchain().get_caller();
    self.participants().insert(caller);  // Grows forever!
}

// Attack: Call register() with many addresses until
// any function iterating participants() runs out of gas
```

### Missing Payment Validation
Does a payable endpoint verify what it receives?

```rust
// VULNERABLE: Accepts any token
#[payable("*")]
#[endpoint]
fn stake(&self) {
    let payment = self.call_value().single_esdt();
    self.staked().update(|s| *s += payment.amount);  // Fake tokens accepted!
}
```

### Callback State Assumptions
Does a callback assume the async call succeeded?

```rust
// VULNERABLE: Assumes success
#[callback]
fn on_transfer_complete(&self) {
    // This runs even if transfer FAILED!
    self.transfer_count().update(|c| *c += 1);
}
```

## 5. Output Template

```markdown
# Entry Point Analysis: [Contract Name]

## Summary
- Total Endpoints: X
- Payable Endpoints: Y (Critical)
- State-Changing: Z (High)
- Views: W (Low)

## Detailed Inventory

### Critical Risk (Payable)
| Endpoint | Accepts | Access | Concerns |
|----------|---------|--------|----------|
| deposit | * | Public | Token validation needed |

### High Risk (State-Changing)
| Endpoint | Access | Storage Modified | Concerns |
|----------|--------|------------------|----------|
| withdraw | Public | balances | Amount validation |

### Medium Risk (Admin)
| Endpoint | Access | Storage Modified | Concerns |
|----------|--------|------------------|----------|
| setConfig | Owner | config | Privilege escalation if misconfigured |

### Low Risk (Views)
| Endpoint | Storage Read | Concerns |
|----------|--------------|----------|
| getBalance | balances | None |

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
