---
name: smart-contract-security
description: Master smart contract security with auditing, vulnerability detection, and incident response
sasmp_version: "1.3.0"
version: "2.0.0"
updated: "2025-01"
bonded_agent: 06-smart-contract-security
bond_type: PRIMARY_BOND

# Skill Configuration
atomic: true
single_responsibility: security_auditing

# Parameter Validation
parameters:
  topic:
    type: string
    required: true
    enum: [vulnerabilities, auditing, tools, incidents]
  severity:
    type: string
    default: all
    enum: [critical, high, medium, low, all]

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

# Smart Contract Security Skill

> Master smart contract security with vulnerability detection, auditing methodology, and incident response procedures.

## Quick Start

```python
# Invoke this skill for security analysis
Skill("smart-contract-security", topic="vulnerabilities", severity="high")
```

## Topics Covered

### 1. Common Vulnerabilities
Recognize and prevent:
- **Reentrancy**: CEI pattern violation
- **Access Control**: Missing modifiers
- **Oracle Manipulation**: Flash loan attacks
- **Integer Issues**: Precision loss

### 2. Auditing Methodology
Systematic review process:
- **Manual Review**: Line-by-line analysis
- **Static Analysis**: Automated tools
- **Fuzzing**: Property-based testing
- **Formal Verification**: Mathematical proofs

### 3. Security Tools
Essential tooling:
- **Slither**: Fast static analysis
- **Mythril**: Symbolic execution
- **Foundry**: Fuzzing, invariants
- **Certora**: Formal verification

### 4. Incident Response
Handle security events:
- **Triage**: Assess severity
- **Mitigation**: Emergency actions
- **Post-mortem**: Root cause analysis
- **Disclosure**: Responsible reporting

## Vulnerability Quick Reference

### Critical: Reentrancy
```solidity
// VULNERABLE
function withdraw(uint256 amount) external {
    (bool ok,) = msg.sender.call{value: amount}("");
    require(ok);
    balances[msg.sender] -= amount;  // After call!
}

// FIXED: CEI Pattern
function withdraw(uint256 amount) external {
    balances[msg.sender] -= amount;  // Before call
    (bool ok,) = msg.sender.call{value: amount}("");
    require(ok);
}
```

### High: Missing Access Control
```solidity
// VULNERABLE
function setAdmin(address newAdmin) external {
    admin = newAdmin;  // Anyone can call!
}

// FIXED
function setAdmin(address newAdmin) external onlyOwner {
    admin = newAdmin;
}
```

### High: Unchecked Return Value
```solidity
// VULNERABLE
IERC20(token).transfer(to, amount);  // Ignored!

// FIXED: Use SafeERC20
using SafeERC20 for IERC20;
IERC20(token).safeTransfer(to, amount);
```

### Medium: Precision Loss
```solidity
// VULNERABLE: Division before multiplication
uint256 fee = (amount / 1000) * rate;

// FIXED: Multiply first
uint256 fee = (amount * rate) / 1000;
```

## Audit Checklist

### Pre-Audit
- [ ] Code compiles without warnings
- [ ] Tests pass with good coverage
- [ ] Documentation reviewed

### Core Security
- [ ] CEI pattern followed
- [ ] Reentrancy guards present
- [ ] Access control on admin functions
- [ ] Input validation complete

### DeFi Specific
- [ ] Oracle staleness checks
- [ ] Slippage protection
- [ ] Flash loan resistance
- [ ] Sandwich prevention

## Security Tools

### Static Analysis
```bash
# Slither - Fast vulnerability detection
slither . --exclude-dependencies

# Mythril - Symbolic execution
myth analyze src/Contract.sol

# Semgrep - Custom rules
semgrep --config "p/smart-contracts" .
```

### Fuzzing
```solidity
// Foundry fuzz test
function testFuzz_Withdraw(uint256 amount) public {
    amount = bound(amount, 1, type(uint128).max);

    vm.deal(address(vault), amount);
    vault.deposit{value: amount}();

    uint256 before = address(this).balance;
    vault.withdraw(amount);

    assertEq(address(this).balance, before + amount);
}
```

### Invariant Testing
```solidity
function invariant_BalancesMatchTotalSupply() public {
    uint256 sum = 0;
    for (uint i = 0; i < actors.length; i++) {
        sum += token.balanceOf(actors[i]);
    }
    assertEq(token.totalSupply(), sum);
}
```

## Severity Classification

| Severity | Impact | Examples |
|----------|--------|----------|
| Critical | Direct fund loss | Reentrancy, unprotected init |
| High | Significant damage | Access control, oracle manipulation |
| Medium | Conditional impact | Precision loss, timing issues |
| Low | Minor issues | Missing events, naming |

## Incident Response

### 1. Detection
```bash
# Monitor for suspicious activity
cast logs --address $CONTRACT --from-block latest
```

### 2. Mitigation
```solidity
// Emergency pause
function pause() external onlyOwner {
    _pause();
}
```

### 3. Recovery
- Assess damage scope
- Coordinate disclosure
- Deploy fixes with audit

## Common Pitfalls

| Pitfall | Risk | Prevention |
|---------|------|------------|
| Only testing happy path | Missing edge cases | Fuzz test boundaries |
| Ignoring integrations | External call risks | Review all dependencies |
| Trusting block.timestamp | Miner manipulation | Use for long timeframes only |

## Cross-References

- **Bonded Agent**: `06-smart-contract-security`
- **Related Skills**: `solidity-development`, `defi-protocols`

## Resources

- SWC Registry: Common weakness enumeration
- Rekt News: Hack post-mortems
- Immunefi: Bug bounties

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.0.0 | 2025-01 | Production-grade with tools, methodology |
| 1.0.0 | 2024-12 | Initial release |
