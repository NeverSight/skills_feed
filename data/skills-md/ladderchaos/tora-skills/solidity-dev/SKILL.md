---
name: solidity-dev
description: Complete Solidity smart contract development - building, testing, gas optimization, and security scanning. Use this skill for .sol files, Foundry commands, deployment scripts, gas analysis, or security review.
---

# Solidity Development

Comprehensive skill for EVM/Solidity smart contract development, combining build/test workflows, gas optimization, and security analysis.

## When This Skill Activates

- Working on `.sol` files
- Running Foundry commands (forge, cast, anvil)
- Contract deployment or testing
- ABI or interface changes
- Gas optimization tasks
- Security review or pre-audit preparation

## Scope

- Solidity contracts (core protocol)
- Foundry tests and scripts
- Deployment scripts
- Contract interfaces and ABIs
- Gas analysis and optimization
- Security scanning (Slither)

---

## Part 1: Development Workflows

### Build & Test

```bash
forge build
forge test
forge test -vvv  # verbose
forge test --match-test "testSpecificFunction"
forge test --match-path test/SomeContract.t.sol
```

### Deploy

```bash
forge script script/Deploy.s.sol --broadcast --rpc-url $RPC_URL
```

### After Contract Changes

1. Update interface if signature changed
2. Rebuild ABIs: `forge build`
3. Run tests: `forge test`
4. Sync to frontend if needed

### Code Standards

- Use OpenZeppelin for standard patterns
- Custom errors over require strings
- Events for all state changes
- NatSpec comments on public functions
- WAD math (1e18) for precision, convert at boundaries

---

## Part 2: Gas Optimization

### Gas Analysis Commands

```bash
# Create baseline snapshot
forge snapshot --snap .gas-baseline

# Run gas report
forge test --gas-report

# Compare against baseline
forge snapshot --diff .gas-baseline

# Check specific function
forge test --match-test test_PlaceOrder --gas-report -vvv

# Storage layout analysis
forge inspect ContractName storage-layout --pretty
```

### Optimization Patterns

| Pattern | Savings | Example |
|---------|---------|---------|
| **Storage Packing** | ~20,000 gas/slot | Combine `uint128 + uint128` into single slot |
| **Calldata vs Memory** | ~60 gas/word | Use `calldata` for read-only arrays |
| **Unchecked Math** | ~40 gas/op | Use `unchecked {}` when overflow impossible |
| **Cache Storage** | ~100 gas/read | `uint256 cached = storageVar;` |
| **Short-circuit** | Variable | Put cheaper checks first in `require` |
| **Avoid Zero Init** | ~3 gas/var | Don't initialize to default values |

### Gas Optimization Checklist

- [ ] Storage variables packed efficiently
- [ ] Hot path functions use `calldata` for arrays
- [ ] Loops have `unchecked` increments
- [ ] Storage reads cached in local variables
- [ ] No redundant zero-initializations
- [ ] Short-circuit conditions ordered by cost

### Anti-Patterns

- Don't optimize cold paths at expense of readability
- Don't use `assembly` unless savings > 1000 gas
- Don't sacrifice security for gas savings

---

## Part 3: Security Analysis

### Slither Commands

```bash
# Full analysis
slither . --config-file slither.config.json

# Target specific contract
slither src/ContractName.sol

# Generate JSON report
slither . --json slither-report.json

# Run specific detector
slither . --detect reentrancy-eth

# Function summary
slither . --print function-summary
```

### High-Severity Detectors

| Detector | Severity | Description |
|----------|----------|-------------|
| `reentrancy-eth` | HIGH | Reentrancy with ETH transfer |
| `reentrancy-no-eth` | HIGH | Reentrancy without ETH |
| `arbitrary-send-eth` | HIGH | Arbitrary ETH destination |
| `controlled-delegatecall` | HIGH | Delegatecall to user input |
| `suicidal` | HIGH | Selfdestruct with user control |
| `uninitialized-state` | HIGH | Uninitialized state variables |

### Security Checklist

#### Access Control
- [ ] All external functions have proper modifiers
- [ ] Owner/admin functions protected
- [ ] Role-based access properly enforced

#### Reentrancy
- [ ] CEI pattern followed (Checks-Effects-Interactions)
- [ ] External calls after state updates
- [ ] ReentrancyGuard on vulnerable functions

#### Math & Validation
- [ ] Arithmetic checked or intentionally unchecked
- [ ] Division by zero protected
- [ ] Zero address checks
- [ ] Array bounds checked

### Common Vulnerability Patterns

#### Reentrancy
```solidity
// VULNERABLE
function withdraw() external {
    uint256 amount = balances[msg.sender];
    (bool success,) = msg.sender.call{value: amount}("");
    balances[msg.sender] = 0; // State update AFTER external call
}

// FIXED
function withdraw() external nonReentrant {
    uint256 amount = balances[msg.sender];
    balances[msg.sender] = 0; // State update BEFORE external call
    (bool success,) = msg.sender.call{value: amount}("");
}
```

#### Access Control
```solidity
// VULNERABLE
function setPrice(uint256 price) external {
    currentPrice = price; // No access control
}

// FIXED
function setPrice(uint256 price) external onlyOwner {
    currentPrice = price;
}
```

### DeFi-Specific Checks

- [ ] No same-block price dependencies (flash loan risk)
- [ ] Slippage protection on swaps
- [ ] Commit-reveal for sensitive ops
- [ ] Deadline parameters respected
- [ ] Oracle manipulation protected (use TWAP/Chainlink)

---

## Audit Preparation Checklist

- [ ] `forge build` compiles without warnings
- [ ] `forge test` passes with >80% coverage
- [ ] Slither runs clean (or issues documented)
- [ ] All external functions documented (NatSpec)
- [ ] Access control matrix documented
- [ ] Invariant tests pass
- [ ] Dependencies audited/pinned
