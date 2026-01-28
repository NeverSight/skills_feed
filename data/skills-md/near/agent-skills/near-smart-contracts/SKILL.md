---
name: near-smart-contracts
description: NEAR Protocol smart contract development in Rust. Use when writing, reviewing, or deploying NEAR smart contracts. Covers contract structure, state management, cross-contract calls, testing, security, and optimization patterns.
license: MIT
metadata:
  author: near
  version: "1.0.0"
---

# NEAR Smart Contracts Development

Comprehensive guide for developing secure and efficient smart contracts on NEAR Protocol using Rust and the NEAR SDK.

## When to Apply

Reference these guidelines when:
- Writing new NEAR smart contracts in Rust
- Reviewing existing contract code for security and optimization
- Implementing cross-contract calls and callbacks
- Managing contract state and storage
- Testing and deploying NEAR contracts
- Optimizing gas usage and performance

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Security & Safety | CRITICAL | `security-` |
| 2 | Contract Structure | HIGH | `structure-` |
| 3 | State Management | HIGH | `state-` |
| 4 | Cross-Contract Calls | MEDIUM-HIGH | `xcc-` |
| 5 | Gas Optimization | MEDIUM | `gas-` |
| 6 | Testing | MEDIUM | `testing-` |
| 7 | Best Practices | MEDIUM | `best-` |

## Quick Reference

### 1. Security & Safety (CRITICAL)

- `security-storage-checks` - Always validate storage operations
- `security-access-control` - Implement proper access control for sensitive functions
- `security-reentrancy` - Protect against reentrancy attacks
- `security-overflow` - Use checked arithmetic to prevent overflow
- `security-callback-validation` - Validate callback results and handle failures
- `security-private-callbacks` - Mark callbacks as private
- `security-yoctonear-validation` - Validate attached deposits

### 2. Contract Structure (HIGH)

- `structure-near-bindgen` - Use #[near_bindgen] macro for contract struct
- `structure-initialization` - Implement proper initialization patterns
- `structure-versioning` - Plan for contract upgrades with versioning
- `structure-events` - Emit events for important state changes
- `structure-standards` - Follow NEAR Enhancement Proposals (NEPs)

### 3. State Management (HIGH)

- `state-collections` - Use NEAR SDK collections (Vector, LookupMap, UnorderedMap, etc.)
- `state-serialization` - Use efficient serialization (Borsh)
- `state-lazy-loading` - Load state lazily to save gas
- `state-pagination` - Implement pagination for large datasets
- `state-migration` - Plan state migration strategies

### 4. Cross-Contract Calls (MEDIUM-HIGH)

- `xcc-promise-chaining` - Chain promises correctly
- `xcc-callback-handling` - Handle all callback scenarios (success, failure)
- `xcc-gas-management` - Allocate appropriate gas for cross-contract calls
- `xcc-error-handling` - Implement robust error handling
- `xcc-result-unwrap` - Never unwrap promise results without checks

### 5. Gas Optimization (MEDIUM)

- `gas-batch-operations` - Batch operations to reduce transaction costs
- `gas-minimal-state-reads` - Minimize state reads and writes
- `gas-efficient-collections` - Choose appropriate collection types
- `gas-view-functions` - Mark read-only functions as view
- `gas-avoid-cloning` - Avoid unnecessary cloning of large data

### 6. Testing (MEDIUM)

- `testing-unit-tests` - Write comprehensive unit tests
- `testing-integration-tests` - Use workspaces-rs for integration tests
- `testing-simulation-tests` - Test with near-sdk-sim or workspaces
- `testing-edge-cases` - Test boundary conditions and edge cases
- `testing-gas-profiling` - Profile gas usage in tests

### 7. Best Practices (MEDIUM)

- `best-panic-messages` - Provide clear panic messages
- `best-logging` - Use env::log_str for debugging
- `best-documentation` - Document public methods and complex logic
- `best-error-types` - Define custom error types
- `best-constants` - Use constants for magic numbers

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/security-storage-checks.md
rules/structure-near-bindgen.md
```

Each rule file contains:
- Brief explanation of why it matters
- Incorrect code example with explanation
- Correct code example with explanation
- Additional context and NEAR-specific considerations

## Resources

- NEAR Documentation: https://docs.near.org
- NEAR SDK Rust: https://docs.near.org/sdk/rust/introduction
- NEAR Examples: https://github.com/near-examples
- NEAR Standards (NEPs): https://github.com/near/NEPs
- Security Best Practices: https://docs.near.org/develop/contracts/security/welcome

## Full Compiled Document

For the complete guide with all rules expanded: `AGENTS.md`
