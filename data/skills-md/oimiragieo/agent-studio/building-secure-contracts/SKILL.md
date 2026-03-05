---
name: building-secure-contracts
description: Smart contract and secure API contract security analysis — invariant checking, access control, reentrancy, and integer overflow patterns. Implements Checks-Effects-Interactions pattern, formal invariant verification, and OpenSCV vulnerability taxonomy for Solidity/EVM and Rust/Solana contracts.
version: 1.1.0
model: sonnet
invoked_by: both
user_invocable: true
tools: [Read, Write, Grep, Bash, WebFetch]
args: '<target-path> [--chain evm|solana] [--focus reentrancy|access-control|overflow|invariants|all]'
best_practices:
  - Apply Checks-Effects-Interactions (CEI) pattern before any external call
  - Verify access control modifiers on every state-mutating function
  - Track integer arithmetic boundaries explicitly (overflow, underflow, precision loss)
  - Document all contract invariants and verify them with formal or property-based tests
  - Trace reentrancy paths across all external calls including ERC20 hooks
error_handling: graceful
streaming: supported
agents: [security-architect, developer, penetration-tester]
category: security
verified: true
lastVerifiedAt: 2026-03-01T00:00:00.000Z
---

# Building Secure Contracts Skill

<!-- Agent: skill-updater | Task: #6 | Session: 2026-03-01 -->

<identity>
Smart contract and secure API contract security analysis skill. Implements Trail of Bits and OpenSCV-aligned methodology for detecting reentrancy attacks, access control failures, integer overflows, and invariant violations in Solidity (EVM) and Rust (Solana) contracts. Addresses the $1.8B+ DeFi exploit landscape (Q3 2025) through systematic vulnerability analysis.
</identity>

<capabilities>
- Checks-Effects-Interactions (CEI) pattern enforcement and verification
- Reentrancy attack surface mapping (cross-function, cross-contract, read-only)
- Access control audit: missing modifiers, privilege escalation, role confusion
- Integer arithmetic analysis: overflow, underflow, precision loss, rounding direction
- Contract invariant identification and formal verification setup
- Storage collision and proxy upgrade security analysis
- Oracle manipulation and price feed dependency analysis
- Flash loan attack surface enumeration
- EVM vs Solana security model comparison and platform-specific risk identification
- OpenSCV vulnerability taxonomy classification for all findings
</capabilities>

## Overview

This skill applies systematic security analysis to smart contracts and secure API contracts. The core principle: **every state mutation must be proven safe through invariant verification before an external call executes**. It covers both EVM (Solidity) and Solana (Rust) ecosystems with platform-specific vulnerability patterns.

**Vulnerability taxonomy**: OpenSCV (94 classified security issues)
**Critical patterns**: CEI, reentrancy guards, access modifiers, SafeMath equivalents
**Risk landscape**: $1.8B+ in DeFi exploits Q3 2025 (access control: $953M, reentrancy: $420M)

## When to Use

- Before deploying any smart contract to mainnet
- When auditing existing contracts for security vulnerabilities
- When reviewing API contracts for invariant violations
- When adding new entry points or external calls to existing contracts
- When upgrading proxy contracts (storage slot collision risk)
- When integrating oracles, flash loans, or third-party DeFi protocols

## Iron Laws

1. **NEVER make external calls before updating state** — Checks-Effects-Interactions (CEI) is non-negotiable; any external call before state update is a reentrancy vector regardless of perceived safety.
2. **NEVER assume access control is correct without reading every modifier** — access control failures account for ~53% of 2024 DeFi losses; verify every `onlyOwner`, `onlyRole`, and custom guard.
3. **NEVER trust integer arithmetic without explicit bounds checking** — Solidity 0.8+ has native overflow protection but custom assembly, unchecked blocks, and Rust/Solana code require explicit verification.
4. **ALWAYS enumerate all contract invariants before analysis** — invariants are the ground truth for correctness; a violation is always a bug; document them in NatSpec before reviewing the implementation.
5. **ALWAYS test reentrancy across full call chains, not just single functions** — cross-function reentrancy (withdraw + transfer sharing state) is as dangerous as direct reentrancy.

## Phase 1: Contract Reconnaissance

**Goal**: Map the attack surface before deep analysis.

### Steps

1. **Enumerate entry points**: All external/public functions, fallback, receive
2. **Identify state-mutating functions**: Functions that modify storage
3. **Map access control boundaries**: Roles, modifiers, ownership checks
4. **Catalog external calls**: `call()`, `transfer()`, ERC20 hooks, interface calls
5. **Identify trust boundaries**: User input, oracle feeds, cross-contract calls

### Output Format

```markdown
## Contract Reconnaissance

### Entry Points

- [ ] `withdraw(uint256 amount)` — external, state-mutating, calls msg.sender
- [ ] `deposit()` — payable, updates balances mapping

### Access Control Map

- [ ] `onlyOwner`: [list of functions]
- [ ] `onlyRole(ADMIN_ROLE)`: [list of functions]
- [ ] No modifier (verify intent): [list of functions]

### External Calls

- [ ] `msg.sender.call{value: amount}("")` at withdraw():L45
- [ ] `token.transferFrom(...)` at deposit():L23

### Trust Boundaries

- [ ] User-supplied amount at withdraw():L40
- [ ] Oracle price feed at getPrice():L67 — manipulation risk
```

## Phase 2: Reentrancy Analysis

**Goal**: Identify all reentrancy vectors (direct, cross-function, read-only).

### Checks-Effects-Interactions Verification

For each function with external calls:

````markdown
### Function: withdraw(uint256 amount)

#### CEI Order Analysis

- L40: CHECK — require(balances[msg.sender] >= amount) ✓
- L45: EXTERNAL CALL — msg.sender.call{value: amount}("") ← VIOLATION
- L48: EFFECT — balances[msg.sender] -= amount ← STATE AFTER CALL

**FINDING**: Classic reentrancy — balance updated after external call.
**Fix**: Move L48 before L45 (CEI pattern)
**Severity**: Critical

#### Fixed Pattern

```solidity
require(balances[msg.sender] >= amount);
balances[msg.sender] -= amount;  // Effect BEFORE external call
(bool success, ) = msg.sender.call{value: amount}("");
require(success);
```
````

### Cross-Function Reentrancy Check

Identify shared state between functions that both make external calls:

```markdown
### Shared State: balances mapping

- withdraw() reads + writes balances + makes external call
- emergencyWithdraw() reads + writes balances + makes external call
  **RISK**: Reentrancy from withdraw() into emergencyWithdraw() bypasses checks
```

## Phase 3: Access Control Audit

**Goal**: Verify every state-mutating function has appropriate guards.

### Access Control Checklist

For each function:

```markdown
### Function Audit: updateTreasury(address newTreasury)

- [ ] Has access modifier? → NO ← FINDING: Missing onlyOwner
- [ ] Modifier verified in contract? → N/A (not present)
- [ ] Owner transferable safely? → N/A
- [ ] Time lock for critical changes? → NO

**Severity**: Critical — anyone can redirect protocol treasury
**Fix**: Add `onlyOwner` modifier and time-lock for parameter changes
```

### Role Confusion Patterns

```markdown
### Role Check: PAUSER_ROLE vs ADMIN_ROLE

- pause() requires: PAUSER_ROLE
- unpause() requires: PAUSER_ROLE (RISK: pauser can also unpause)
- grantRole() requires: ADMIN_ROLE

**Issue**: Pauser can unilaterally pause and unpause — should require separate roles
**Severity**: Medium
```

## Phase 4: Integer Arithmetic Analysis

**Goal**: Identify overflow, underflow, precision loss, and rounding direction bugs.

### Arithmetic Boundary Analysis

```markdown
### Function: calculateReward(uint256 principal, uint256 rate)

- L88: `uint256 reward = principal * rate / 1e18`
  - Multiplication before division: OK (avoids precision loss)
  - Overflow check: principal \* rate could overflow if both > sqrt(uint256.max)
  - Rounding: truncates toward zero — check if favors protocol or user
  - `unchecked` block? → NO → Solidity 0.8+ protects this

### Unchecked Block Analysis

- L102-108: `unchecked { ... }`
  - Why unchecked? Check comment and verify mathematician's claim
  - Is the claimed impossibility of overflow actually proven?
  - [UNVERIFIED] claim: "amount < balance guarantees no underflow"
```

## Phase 5: Invariant Verification

**Goal**: Identify and verify all contract-level invariants.

```markdown
### Contract Invariants: LiquidityPool

1. **Solvency**: sum(balances) == address(this).balance — [VERIFIED L90]
2. **Total supply**: totalSupply == sum(all user shares) — [UNVERIFIED]
3. **Fee bound**: fee <= MAX_FEE (1000 bps) — [VERIFIED by require at L45]
4. **Non-zero denominator**: totalSupply > 0 before share calculation — [VIOLATED at L67, division-by-zero risk on first deposit]

### Invariant Violation Findings

**FINDING**: Invariant 4 violated — first depositor can cause division by zero

- Location: L67 `shares = amount * totalSupply / totalAssets`
- When: totalSupply == 0 on first deposit
- Impact: DoS attack on first deposit; protocol initialization blocked
- Fix: Handle zero totalSupply case separately with initial share ratio
```

## Output: Security Report

```markdown
# Security Report: [Contract Name]

## Summary

- Functions analyzed: N
- Findings: N (Critical: X, High: Y, Medium: Z, Low: W)
- Invariants verified: N of M
- CEI violations: N

## Critical Findings

### [F-01] Reentrancy in withdraw()

- Location: `src/Pool.sol:L45`
- Pattern: External call before state update (CEI violation)
- Impact: Complete fund drainage
- Fix: Apply CEI pattern — update state before external call
- 5 Whys: [root cause chain]

## Invariant Status

| Invariant                  | Status     | Evidence            |
| -------------------------- | ---------- | ------------------- |
| sum(balances) == balance   | VERIFIED   | L90 invariant check |
| totalSupply == sum(shares) | UNVERIFIED | No test coverage    |

## Recommendations

1. [Critical] Fix reentrancy in withdraw() before deployment
2. [High] Add reentrancy guard as defense-in-depth
3. [Medium] Add formal invariant tests via Foundry invariant suite
```

## Integration with Agent-Studio

### Recommended Workflow

1. Invoke `audit-context-building` for initial code reconnaissance
2. Invoke `building-secure-contracts` for contract-specific analysis
3. Feed findings into `security-architect` for threat modeling
4. Use `static-analysis` (Semgrep/CodeQL) for automated confirmation
5. Use `medusa-security` for fuzzing-based invariant testing

### Complementary Skills

| Skill                    | Relationship                                         |
| ------------------------ | ---------------------------------------------------- |
| `audit-context-building` | Builds initial mental model before contract analysis |
| `security-architect`     | Consumes findings for threat modeling and STRIDE     |
| `static-analysis`        | Automated SAST confirmation of manual findings       |
| `medusa-security`        | Fuzzing and property-based testing for invariants    |
| `variant-analysis`       | Finds similar vulnerability patterns across codebase |
| `web3-expert`            | Solidity/Ethereum ecosystem expertise                |

## Anti-Patterns

| Anti-Pattern                                    | Why It Fails                                                   | Correct Approach                                            |
| ----------------------------------------------- | -------------------------------------------------------------- | ----------------------------------------------------------- |
| Auditing only the happy path                    | Reentrancy and access control bugs are invisible in happy path | Explicitly trace every error path and external call         |
| Trusting function name for access control       | `onlyAdmin()` might not check the actual admin role            | Read the modifier implementation, not just its name         |
| Assuming Solidity 0.8 prevents all integer bugs | `unchecked` blocks, assembly, and casting bypass protection    | Audit all `unchecked` blocks and type casts explicitly      |
| Skipping cross-function reentrancy              | Cross-function reentrancy bypasses single-function guards      | Map shared state across ALL functions making external calls |
| Leaving invariants implicit                     | Unwritten invariants are unverified risks                      | Document every invariant in NatSpec before analysis         |

## Memory Protocol

**Before starting**: Check `.claude/context/memory/learnings.md` for prior contract audits of the same protocol or token standard.

**During analysis**: Write incremental findings to context report as discovered. Do not wait until the end.

**After completion**: Record key findings and patterns to `.claude/context/memory/learnings.md`. Record architecture decisions (CEI enforcement patterns, invariant frameworks) to `decisions.md`.
