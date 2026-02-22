---
name: near-contract-audit
description: Comprehensive security audit skill for NEAR Protocol smart contracts written in Rust. Use when auditing NEAR contracts, reviewing security vulnerabilities, or analyzing contract code for issues like reentrancy, unhandled promises, unsafe math, access control flaws, and callback security.
---

# NEAR Contract Audit

Security audit skill for NEAR smart contracts in Rust.

## Audit Workflow

### Phase 1: Automated Analysis

Run your preferred Rust static analysis and NEAR-focused security tools on the contract to:

- Scan for common vulnerability patterns (reentrancy, unsafe math, unhandled promises, access control issues, etc.)
- Highlight potentially risky patterns for deeper manual review

### Phase 2: Manual Review

After automated analysis, perform manual review for:

- Business logic vulnerabilities
- Access control patterns
- Economic attack vectors
- Cross-contract interaction safety

### Phase 3: Code-Specific Analysis

For each finding, verify:

1. Is it a true positive?
2. What is the exploitability?
3. What is the recommended fix?

### Phase 4: Report Generation

Document findings with severity, location, description, and remediation.

## Vulnerability Quick Reference

| Severity   | Detector ID                      | Description                                     |
| ---------- | -------------------------------- | ----------------------------------------------- |
| **High**   | `non-private-callback`           | Callback missing `#[private]` macro             |
| **High**   | `reentrancy`                     | State change after cross-contract call          |
| **High**   | `incorrect-argument-or-return-types` | Using native integer types in JSON interfaces |
| **High**   | `unsaved-changes`                | Collection modifications not persisted          |
| **High**   | `owner-check`                    | Missing caller/owner verification               |
| **High**   | `yocto-attach`                   | Missing `assert_one_yocto` on sensitive functions |
| **High**   | `storage-collision`              | Same storage prefix for different collections   |
| **High**   | `required-initialization-macro`  | Missing `#[init]` on initialization method      |
| **Medium** | `gas-griefing`                   | Unbounded loops causing DoS                     |
| **Medium** | `insecure-random`                | Predictable randomness from block data          |
| **Medium** | `prepaid-gas`                    | Insufficient gas reserved for callbacks         |
| **Low**    | `cover-storage-cost`             | Missing storage deposit verification            |
| **Low**    | `unsafe-math`                    | Arithmetic without overflow checks              |
| **Low**    | `float-math`                     | Using floating point types for financial math   |

## Reference Files

For detailed vulnerability documentation with code examples:

- [high-severity.md](references/high-severity.md) - Critical vulnerabilities (8 detectors)
- [medium-severity.md](references/medium-severity.md) - Medium vulnerabilities (4 detectors)
- [low-severity.md](references/low-severity.md) - Low severity findings (3 detectors)
