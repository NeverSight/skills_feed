---
name: solidity-gas-optimization
description: Gas optimization patterns for Solidity smart contracts. Use when optimizing contract deployment costs, runtime gas usage, or storage efficiency. Covers storage packing, custom errors, immutable variables, calldata optimization, loop patterns, assembly usage, and Solady gas-optimized alternatives. Triggers on tasks involving gas optimization, storage layout, deployment cost reduction, or EVM efficiency.
license: MIT
metadata:
  author: whackur
  version: "0.5.3"
---

# Solidity Gas Optimization

## When to Apply

- During contract development to reduce deployment and runtime costs.
- When hitting the 24KB contract size limit.
- When optimizing high-frequency functions (e.g., swaps, transfers).
- When designing storage-heavy protocols.
- Before final security audits to ensure efficiency doesn't compromise safety.

## Critical Optimizations

### Storage Layout Packing

EVM reads and writes in 32-byte (256-bit) slots. Variables smaller than 32 bytes that are declared consecutively share a slot, reducing SSTORE operations. A new SSTORE costs 20,000 gas; packing avoids additional slot allocations.

**What to verify**: Consecutive variables of the same or smaller combined size (≤32 bytes) are grouped together. Place `uint128` next to `uint128`, not separated by a `uint256`.

### Custom Errors vs Revert Strings

Custom errors are encoded as 4-byte selectors, whereas revert strings store the full string in contract bytecode and in memory at runtime. Custom errors save gas on both deployment (smaller bytecode) and execution (cheaper encoding).

**What to verify**: All `require` statements with string messages are replaced with `if (...) revert CustomError()` patterns.

### Immutable and Constant Variables

`constant` values are inlined at compile time — zero storage reads. `immutable` values are stored in contract bytecode (set once in constructor), costing ~3 gas to read instead of ~2,100 gas for a cold SLOAD.

**What to verify**: Values known at compile time use `constant`. Values set once in the constructor use `immutable`. Neither uses a storage slot.

## High Impact Optimizations

### Calldata vs Memory

`calldata` is read-only and avoids the ABI decode copy into memory. For external functions with array or struct parameters that are only read (not modified), `calldata` saves the entire memory copy cost.

**What to verify**: External function parameters that are not modified use `calldata` instead of `memory`.

### Unchecked Arithmetic

Solidity 0.8+ adds overflow/underflow checks on every arithmetic operation (~30 gas each). For loop counters where overflow is mathematically impossible (e.g., `i < length` where `length ≤ type(uint256).max`), wrapping the increment in `unchecked` safely removes this overhead.

**What to verify**: Loop increment operations (`++i`) are inside `unchecked` blocks where overflow is provably impossible.

### Short-Circuit Evaluation

Solidity evaluates `&&` and `||` left-to-right, stopping at the first decisive result. Placing cheap conditions (storage reads < external calls) and high-failure-probability conditions first reduces average gas cost.

**What to verify**: Conditions in `&&` expressions are ordered cheapest/most-likely-to-fail first.

## Medium Impact Optimizations

### Loop Optimizations

Accessing `.length` on a storage array costs a SLOAD each iteration. Caching the length in a local variable converts repeated SLOADs to near-free MLOAD operations.

**What to verify**: Array length is cached in a local variable before the loop. No storage reads inside the loop body that could be cached.

### Efficient Data Types

The EVM operates on 256-bit words natively. Smaller types (`uint8`, `uint32`) require additional masking operations when used in isolation. Use `uint256` for math and smaller types only when packing into a single storage slot. For short strings (≤32 bytes), `bytes32` avoids dynamic allocation overhead.

**What to verify**: `uint256` is the default for standalone math. Smaller types are used only for storage packing. Short constant strings use `bytes32`.

### Minimize Storage Writes

SSTORE is the most expensive EVM operation (20,000 gas new, 5,000 update, 2,900 refund for clearing). Batch updates to write once instead of multiple times. For same-transaction temporary state, EIP-1153 transient storage (TSTORE/TLOAD at 100 gas each) eliminates the need for storage writes entirely.

**What to verify**: State variables are not written multiple times in the same function. Temporary state within a single transaction uses transient storage (Solidity ≥0.8.24).

## Advanced Optimizations

### Assembly (Yul)

Inline assembly bypasses Solidity's safety checks and memory management for direct EVM opcode access. Use for gas-critical operations like efficient transfers, custom encoding, or storage manipulation. The readability tradeoff is significant — every assembly block must be heavily documented.

**What to verify**: Assembly is used only where measurable gas savings justify the readability cost. All assembly blocks have detailed comments.

### Solady Library

Solady provides gas-optimized alternatives to OpenZeppelin contracts (SafeTransferLib, Ownable, ERC20, etc.) using assembly-level optimizations. Typical savings: 20-50% gas reduction on common operations.

**What to verify**: For gas-critical applications, Solady alternatives are evaluated for standard patterns (token transfers, ownership, ERC implementations).

### EIP-1167 Minimal Proxy (Clones)

The Clone pattern deploys a 45-byte proxy that delegates all calls to a single implementation contract. Deployment cost drops from ~500k gas (full contract) to ~42k gas (proxy). Use when deploying many instances of the same logic.

**What to verify**: Contracts deployed in bulk (e.g., per-user vaults, per-pair pools) use the clone pattern instead of full deployment.

## Optimization Checklist

1. Are variables packed into 32-byte slots?
2. Are all revert strings replaced with custom errors?
3. Are `constant` and `immutable` used where possible?
4. Are function parameters `calldata` instead of `memory`?
5. Are loop increments `unchecked`?
6. Is array length cached before loops?
7. Are `uint256` used instead of smaller types for math?
8. Are `bytes32` used instead of `string` for short data?
9. Are storage writes minimized/batched?
10. Is `short-circuiting` applied to complex conditionals?
11. Are `external` functions used instead of `public` where possible?
12. Is `Solady` used for standard utilities?
13. Are `TSTORE`/`TLOAD` used for transient state?
14. Is the contract size within the 24KB limit?

## Enhanced with MCP

Leverage `solidity-agent-toolkit` MCP tools for precise optimization analysis:

**Measure and compare:**

- `gas_snapshot` — Generate gas reports and compare across different implementations
- `estimate_gas` — Get function-level gas estimates for specific calls
- `inspect_storage` — Visualize storage layout and identify packing opportunities

**Automate optimization review:**

- Use the `optimize_gas` prompt for a structured, MCP-guided optimization workflow

**Check for optimization-related vulnerabilities:**

- `match_vulnerability_patterns` — Detect patterns where optimization may compromise security (e.g., unchecked usage in non-loop contexts)

## References

- For security implications of optimizations: Security Best Practices skill
- For auditing optimized code: Code Review skill
