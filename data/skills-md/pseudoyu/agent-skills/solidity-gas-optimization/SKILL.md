---
name: solidity-gas-optimization
description: Solidity smart contract gas optimization guidelines based on RareSkills. Use when writing, reviewing, or auditing Solidity code. Triggers on tasks involving smart contracts, EVM development, gas optimization, or Solidity best practices.
---

# Solidity Gas Optimization

## Overview

Comprehensive gas optimization guide for Solidity smart contracts, containing 80+ techniques across 8 categories. Based on the RareSkills Book of Gas Optimization. Rules are prioritized by impact and safety.

## When to Apply

Reference these guidelines when:

- Writing new Solidity smart contracts
- Reviewing or auditing existing contracts
- Optimizing gas costs for deployment or execution
- Refactoring contract storage layouts
- Implementing cross-contract interactions
- Choosing between design patterns (ERC721 vs ERC1155, etc.)

## Priority-Ordered Categories

| Priority | Category | Impact | Risk |
|----------|----------|--------|------|
| 1 | Storage Optimization | CRITICAL | LOW |
| 2 | Deployment Optimization | HIGH | LOW |
| 3 | Calldata Optimization | HIGH | LOW |
| 4 | Design Patterns | HIGH | MEDIUM |
| 5 | Cross-Contract Calls | MEDIUM-HIGH | MEDIUM |
| 6 | Compiler Optimizations | MEDIUM | LOW |
| 7 | Assembly Tricks | MEDIUM | HIGH |
| 8 | Dangerous Techniques | LOW | CRITICAL |

## Quick Reference

### Critical: Storage Optimization (Apply First)

**Zero-to-One Writes:**

- Avoid zero-to-one storage writes (costs 22,100 gas)
- Use 1/2 instead of 0/1 for boolean-like values
- Keep minimum balances in ERC20 contracts

**Variable Packing:**

```solidity
// Bad: 3 slots
struct Unpacked {
    uint64 time;      // slot 1
    uint256 amount;   // slot 2
    address user;     // slot 3
}

// Good: 2 slots
struct Packed {
    uint64 time;      // slot 1 (with address)
    address user;     // slot 1
    uint256 amount;   // slot 2
}
```

**Caching:**

```solidity
// Bad: reads storage twice
function increment() public {
    require(count < 10);
    count = count + 1;
}

// Good: reads storage once
function increment() public {
    uint256 _count = count;
    require(_count < 10);
    count = _count + 1;
}
```

**Constants & Immutables:**

```solidity
uint256 constant MAX = 100;        // No storage slot
address immutable owner;           // Set in constructor, no storage
```

### High: Deployment Optimization

**Custom Errors:**

```solidity
// Bad: ~64+ bytes
require(amount <= limit, "Amount exceeds limit");

// Good: ~4 bytes
error ExceedsLimit();
if (amount > limit) revert ExceedsLimit();
```

**Payable Constructors:**

```solidity
// Saves ~200 gas on deployment
constructor() payable {}
```

**Clone Patterns:**

- Use EIP-1167 minimal proxies for repeated deployments
- Use UUPS over Transparent Proxy for upgradeable contracts

### High: Calldata Optimization

**Calldata vs Memory:**

```solidity
// Bad: copies to memory
function process(bytes memory data) external {}

// Good: reads directly from calldata
function process(bytes calldata data) external {}
```

**Avoid Signed Integers:**

- Small negative numbers are expensive (e.g., -1 = 0xffff...)
- Use unsigned integers in function parameters

### High: Design Patterns

**Token Standards:**

- Prefer ERC1155 over ERC721 for NFTs (no balanceOf overhead)
- Consider consolidating multiple ERC20s into one ERC1155

**Signature vs Merkle:**

- Prefer ECDSA signatures over Merkle trees for allowlists
- Implement ERC20Permit for approve + transfer in one tx

**Alternative Libraries:**

- Consider Solmate/Solady over OpenZeppelin for gas efficiency

### Medium-High: Cross-Contract Calls

**Reduce Interactions:**

- Use ERC1363 transferAndCall instead of approve + transferFrom
- Implement multicall for batching operations
- Cache external call results (e.g., Chainlink oracles)

**Access Lists:**

- Use ERC2930 access list transactions to pre-warm storage

### Medium: Compiler Optimizations

**Loop Patterns:**

```solidity
// Good: unchecked increment, cached length
uint256 len = arr.length;
for (uint256 i; i < len; ) {
    // logic
    unchecked { ++i; }
}
```

**Named Returns:**

```solidity
// More efficient bytecode
function calc(uint256 x) pure returns (uint256 result) {
    result = x * 2;
}
```

**Bitshifting:**

```solidity
// Cheaper: 3 gas
x << 1   // x * 2
x >> 2   // x / 4

// Expensive: 5 gas
x * 2
x / 4
```

**Short-Circuit Booleans:**

- Place likely-to-fail conditions first in `&&`
- Place likely-to-succeed conditions first in `||`

### Medium: Assembly (Use Carefully)

**Efficient Checks:**

```solidity
// Check address(0) with assembly
assembly {
    if iszero(caller()) { revert(0, 0) }
}

// Even/odd check
x & 1  // instead of x % 2
```

**Memory Reuse:**

- Reuse scratch space (0x00-0x40) for small operations
- Avoid memory expansion in loops

### Avoid: Dangerous Techniques

These are unsafe for production:

- Making all functions payable
- Ignoring send() return values
- Using gasleft() for branching
- Manipulating block.number in tests

## Outdated Patterns

These no longer apply in modern Solidity:

- "external is cheaper than public" - No longer true
- "!= 0 is cheaper than > 0" - Changed around 0.8.12

## References

Full documentation with code examples:

- `references/solidity-gas-guidelines.md` - Complete guide
- `references/rules/` - Individual patterns by category

To look up specific patterns:

```bash
grep -l "storage" references/rules/
grep -l "assembly" references/rules/
grep -l "struct" references/rules/
```

## Rule Categories in `references/rules/`

- `storage-*` - Storage optimization patterns
- `deploy-*` - Deployment gas savings
- `calldata-*` - Calldata optimization
- `design-*` - Design pattern choices
- `crosscall-*` - Cross-contract call optimization
- `compiler-*` - Compiler optimization patterns
- `assembly-*` - Low-level assembly tricks

## Key Principles

1. **Always Benchmark** - Compiler behavior varies by context and version
2. **Balance Readability** - Not all optimizations are worth code complexity
3. **Test Both Approaches** - Counterintuitive optimizations sometimes increase costs
4. **Consider `--via-ir`** - Modern compiler option may obsolete some tricks
5. **Use Alternative Libraries** - Solmate/Solady often beat OpenZeppelin on gas
