---
name: solidity-development
description: Master Solidity smart contract development with patterns, testing, and best practices
sasmp_version: "1.3.0"
version: "2.0.0"
updated: "2025-01"
bonded_agent: 03-solidity-expert
bond_type: PRIMARY_BOND

# Skill Configuration
atomic: true
single_responsibility: solidity_development

# Parameter Validation
parameters:
  topic:
    type: string
    required: true
    enum: [syntax, patterns, testing, upgrades, security]
  solidity_version:
    type: string
    default: "0.8.24"

# Retry & Error Handling
retry_config:
  max_attempts: 3
  backoff: exponential
  initial_delay_ms: 1000

# Logging & Observability
logging:
  level: info
  include_timestamps: true
  track_usage: true
---

# Solidity Development Skill

> Master Solidity smart contract development with design patterns, testing strategies, and production best practices.

## Quick Start

```python
# Invoke this skill for Solidity development
Skill("solidity-development", topic="patterns", solidity_version="0.8.24")
```

## Topics Covered

### 1. Language Features (0.8.x)
Modern Solidity essentials:
- **Data Types**: Value, reference, mappings
- **Functions**: Visibility, modifiers, overloading
- **Inheritance**: Diamond problem, C3 linearization
- **Custom Errors**: Gas-efficient error handling

### 2. Design Patterns
Battle-tested patterns:
- **CEI**: Checks-Effects-Interactions
- **Factory**: Contract deployment patterns
- **Proxy**: Upgradeable contracts
- **Access Control**: RBAC, Ownable

### 3. Testing
Comprehensive test strategies:
- **Unit Tests**: Foundry, Hardhat
- **Fuzz Testing**: Property-based testing
- **Invariant Testing**: System-wide properties
- **Fork Testing**: Mainnet simulation

### 4. Upgradability
Safe upgrade patterns:
- **UUPS**: Self-upgrading proxy
- **Transparent**: Admin separation
- **Beacon**: Shared implementation
- **Diamond**: Multi-facet

## Code Examples

### CEI Pattern
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

contract SecureVault {
    mapping(address => uint256) public balances;

    error InsufficientBalance();
    error TransferFailed();

    function withdraw(uint256 amount) external {
        // 1. CHECKS
        if (balances[msg.sender] < amount) revert InsufficientBalance();

        // 2. EFFECTS
        balances[msg.sender] -= amount;

        // 3. INTERACTIONS
        (bool ok,) = msg.sender.call{value: amount}("");
        if (!ok) revert TransferFailed();
    }
}
```

### Factory Pattern
```solidity
contract TokenFactory {
    event TokenCreated(address indexed token, address indexed owner);

    function createToken(
        string memory name,
        string memory symbol
    ) external returns (address) {
        Token token = new Token(name, symbol, msg.sender);
        emit TokenCreated(address(token), msg.sender);
        return address(token);
    }
}
```

### Foundry Test
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "forge-std/Test.sol";

contract VaultTest is Test {
    Vault vault;
    address alice = makeAddr("alice");

    function setUp() public {
        vault = new Vault();
        vm.deal(alice, 10 ether);
    }

    function test_Deposit() public {
        vm.prank(alice);
        vault.deposit{value: 1 ether}();

        assertEq(vault.balances(alice), 1 ether);
    }

    function testFuzz_Withdraw(uint256 amount) public {
        amount = bound(amount, 0.01 ether, 10 ether);

        vm.startPrank(alice);
        vault.deposit{value: amount}();
        vault.withdraw(amount);
        vm.stopPrank();

        assertEq(vault.balances(alice), 0);
    }

    function test_RevertWhen_InsufficientBalance() public {
        vm.prank(alice);
        vm.expectRevert(Vault.InsufficientBalance.selector);
        vault.withdraw(1 ether);
    }
}
```

## Pattern Reference

| Pattern | Use Case | Complexity |
|---------|----------|------------|
| CEI | All state changes | Low |
| Factory | Multiple instances | Low |
| Clone (1167) | Gas-efficient copies | Medium |
| UUPS | Upgradeable | Medium |
| Diamond | Unlimited size | High |

## Common Pitfalls

| Pitfall | Issue | Solution |
|---------|-------|----------|
| Stack too deep | >16 variables | Use structs or helpers |
| Contract too large | >24KB | Split into libraries |
| Reentrancy | State after call | Use CEI pattern |
| Missing access | Anyone can call | Add modifiers |

## Troubleshooting

### "Stack too deep"
```solidity
// Solution 1: Use struct
struct Params { uint256 a; uint256 b; uint256 c; }

// Solution 2: Block scoping
{ uint256 temp = x + y; }

// Solution 3: Internal function
function _helper(uint256 a) internal { }
```

### "Contract size exceeds limit"
```bash
# Check contract sizes
forge build --sizes
```
Solutions: Split into libraries, use Diamond pattern.

## Security Checklist

- [ ] CEI pattern on all withdrawals
- [ ] Access control on admin functions
- [ ] Input validation (zero address, bounds)
- [ ] Reentrancy guards on external calls
- [ ] Event emission for state changes
- [ ] Custom errors for gas efficiency

## CLI Commands

```bash
# Development workflow
forge init                    # New project
forge build                   # Compile
forge test -vvv               # Run tests
forge coverage                # Coverage report
forge fmt                     # Format code
forge snapshot                # Gas snapshot
```

## Cross-References

- **Bonded Agent**: `03-solidity-expert`
- **Related Skills**: `ethereum-development`, `smart-contract-security`

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.0.0 | 2025-01 | Production-grade with Foundry, patterns |
| 1.0.0 | 2024-12 | Initial release |
