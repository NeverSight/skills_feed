---
name: solidity-security-best-practices
description: Smart contract security best practices for Solidity development. Use when writing, reviewing, or auditing Solidity code. Covers reentrancy prevention, access control patterns, safe external calls, input validation, upgrade safety, and OWASP Smart Contract Top 10 vulnerabilities. Triggers on tasks involving security, vulnerability detection, access control, CEI pattern, ReentrancyGuard, SafeERC20, or smart contract auditing.
license: MIT
metadata:
  author: whackur
  version: "0.5.3"
---

# Solidity Security Best Practices

## When to Apply

- Reviewing smart contract code for common vulnerabilities.
- Implementing critical patterns like Checks-Effects-Interactions.
- Auditing access control and upgradeability logic.
- Preparing for a security audit or bug bounty.
- Debugging unexpected behavior in external contract interactions.

## Security Thinking Framework

When reviewing or writing Solidity code, apply these foundational principles as a mental checklist. Each principle addresses a category of vulnerability and guides your reasoning.

### Core Principles

| Principle                             | What It Means                                                  | What to Verify                                             |
| :------------------------------------ | :------------------------------------------------------------- | :--------------------------------------------------------- |
| **Checks-Effects-Interactions (CEI)** | Validate inputs, update state, then interact externally        | State changes complete before any external call            |
| **Least Privilege**                   | Every function and role has the minimum access required        | Sensitive functions have appropriate access modifiers      |
| **Defense in Depth**                  | Multiple layers of protection, no single points of failure     | Combine CEI + ReentrancyGuard + SafeERC20 where applicable |
| **Fail-Safe Defaults**                | The default state is secure; access must be explicitly granted | Functions default to restricted, not open                  |
| **Complete Mediation**                | Every access to every resource is validated                    | No code paths bypass access control checks                 |

### Security Decision Process

When you encounter a function, ask these questions in order:

1. **Who can call this?** — Check access control (onlyOwner, hasRole, msg.sender validation)
2. **What inputs does it accept?** — Validate all parameters (zero address, bounds, empty values)
3. **What state does it change?** — Ensure state updates happen before external interactions
4. **Does it interact externally?** — Apply CEI, use SafeERC20, check return values
5. **Can it be called recursively?** — Add ReentrancyGuard if external calls are present
6. **Is the state change visible?** — Emit events for off-chain tracking
7. **Can it be paused?** — Implement circuit breakers for critical operations

## SCSVS-Based Audit Workflow

Organize your review by OWASP SCSVS categories. For each category, focus on the specific threat model.

### Architecture & Design (SCSVS-ARCH)

- Proxy patterns: correct admin separation, storage gaps, initializer protection
- Contract boundaries: minimal surface area, no circular dependencies
- Delegatecall: only to trusted, immutable targets

### Code Quality (SCSVS-CODE)

- Explicit visibility on all functions
- Fixed pragma (no floating versions)
- No deprecated functions (`throw`, `suicide`, `constant` for functions)
- No unused code, no variable shadowing

### Authorization (SCSVS-AUTH)

- Access control on ALL state-changing functions
- No `tx.origin` for authentication — use `msg.sender`
- Protected initializers (callable once only)
- Privileged roles require multi-sig or timelock

### Communication (SCSVS-COMM)

- Return values of external calls checked and handled
- No `delegatecall` to untrusted contracts
- Pull-over-push pattern for payments
- CEI pattern or ReentrancyGuard on all functions with external calls

### Cryptography (SCSVS-CRYPTO)

- No on-chain randomness (`block.timestamp`, `blockhash`)
- EIP-712 for structured data signatures
- `abi.encode` instead of `abi.encodePacked` for dynamic types in hashing
- Signature malleability protection
- `ecrecover` result validated (not `address(0)`)

### DeFi-Specific (SCSVS-DEFI)

- Slippage protection on swaps and liquidity operations
- Flash loan resistance in price-sensitive logic
- Oracle manipulation protection (TWAP, multiple sources)
- No reliance on `address(this).balance` for internal accounting
- Fee-on-transfer and rebasing token compatibility

### Blockchain-Specific (SCSVS-BLOCK)

- No block property dependence for critical logic (timestamp, difficulty)
- Front-running protection (commit-reveal, slippage limits)
- Gas griefing protection for relayer patterns

### Bridge & Cross-Chain (SCSVS-BRIDGE)

- Message validation across chains
- Replay protection for cross-chain messages
- Trust model verification for bridge relayers

### Governance (SCSVS-GOV)

- Timelock on governance actions
- Proposal execution safety
- Flash loan governance attack protection

### Component Security (SCSVS-COMP)

- Dependency audit (OpenZeppelin version pinning)
- Known vulnerability checks against dependencies
- Interface compliance verification

## Security Patterns by Priority

### Critical

- **CEI Pattern**: Always update state before external calls to prevent reentrancy. The most common vulnerability source is performing state changes after an external call.
- **Reentrancy Guard**: Use mutex locks (OpenZeppelin ReentrancyGuard) for functions with external interactions. Protects against both same-function and cross-function reentrancy.
- **Access Control**: Restrict sensitive functions with role-based modifiers (Ownable, AccessControl). Every state-changing function must have explicit authorization.
- **Safe External Calls**: Use SafeERC20 for token transfers to handle non-standard return values. Always check `.call()` return values with `require`.

### High

- **Input Validation**: Validate all parameters — zero address, bounds, empty arrays, zero amounts. Use custom errors (`revert InvalidAmount()`) for gas-efficient validation.
- **Upgrade Safety**: Protect initializers with `initializer` modifier, verify storage compatibility across upgrades, restrict upgrade admin access.
- **Circuit Breakers**: Implement Pausable functionality (OpenZeppelin) for emergency response. Critical for DeFi protocols handling user funds.

### Medium

- **Signature Security**: Use nonces + EIP-712 domain separators to prevent replay attacks. Validate `ecrecover` does not return `address(0)`.
- **Randomness**: Never use on-chain data (`block.timestamp`, `blockhash`) for randomness. Use Chainlink VRF or commit-reveal schemes.
- **Event Emission**: Emit events for all significant state changes. Use `indexed` parameters for efficient off-chain filtering.

## Enhanced with MCP

If you have the `solidity-agent-toolkit` MCP server configured, use these tools to augment your manual review:

**Suspect a known vulnerability?**

- `search_vulnerabilities` — Search the OWASP SCWE database by keyword or category
- `get_remediation` — Get specific fix guidance with vulnerable and fixed code examples for any SCWE ID
- `check_vulnerability` — Check if code matches a known SCWE pattern

**Want automated scanning?**

- `match_vulnerability_patterns` — Regex-based detection of 32+ common vulnerability patterns
- `run_slither` — Comprehensive static analysis with SCWE-mapped findings
- `run_aderyn` — Fast Rust-based vulnerability scanner

**Need reference data?**

- `scwe://{id}` — Full vulnerability details including description, remediation, and code examples
- `scwe://category/{category}` — Browse all vulnerabilities by SCSVS category
- `sctop10://list` — OWASP Smart Contract Top 10 overview

**Full audit workflow?**

- Use the `security_audit` prompt for a structured, guided audit process
- Use the `vulnerability_fix` prompt for step-by-step remediation assistance

## References

- [OWASP Smart Contract Top 10 (2026)](references/owasp-scwe-top10.md)
