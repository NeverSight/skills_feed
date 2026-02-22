---
name: solidity-code-review
description: Smart contract code review and security audit methodology for Solidity. Use when reviewing, auditing, or assessing the security of Solidity code. Provides structured review process, severity classification, key inspection areas, and OWASP SCWE integration. Triggers on tasks involving code review, security audit, vulnerability assessment, smart contract review, or best practices check.
license: MIT
metadata:
  author: whackur
  version: "0.5.3"
---

# Solidity Code Review Guide

## When to Apply

Apply this methodology when performing a security audit, peer review, or general assessment of Solidity smart contracts. It is designed to identify vulnerabilities, ensure adherence to best practices, and verify the robustness of the contract logic.

## Pre-Review Checklist

Before beginning the manual review, ensure the following items are addressed:

- **Compilation**: Verify the code compiles without errors using the project's build system (Foundry, Hardhat, etc.).
- **Test Suite**: Run the existing test suite. Ensure tests pass and review coverage reports to identify untested logic.
- **Dependencies**: Identify all external libraries and inherited contracts. Verify versions are pinned and trusted.
- **Documentation**: Review technical specifications and NatSpec comments to understand intended behavior.
- **Known Issues**: Check for previous audit reports or documented "known risks" provided by the developers.
- **Scope**: Define the exact list of contracts and functions that are within the audit scope.

## Review Methodology

1. **Step 1: Scope & Architecture**: Map out the contract inheritance, external dependencies, and system architecture.
2. **Step 2: Manual Line-by-Line Review**: Perform a deep dive into critical functions, focusing on state changes and value transfers.
3. **Step 3: Automated Analysis**: Run static analysis tools (Slither, Aderyn, Solhint) to catch common patterns and style violations.
4. **Step 4: Vulnerability Pattern Matching**: Specifically check for known SCWE patterns (Reentrancy, Access Control, etc.).
5. **Step 5: Integration & Edge Cases**: Analyze how contracts interact and test boundary conditions (e.g., zero values, max integers).

## Severity Classification

| Severity     | Criteria                                                                              | Examples                                                              |
| :----------- | :------------------------------------------------------------------------------------ | :-------------------------------------------------------------------- |
| **Critical** | Direct loss of funds, permanent contract lock, or total compromise.                   | Reentrancy, Unprotected `withdraw`, Logic error in `transfer`.        |
| **High**     | Significant impact on system functionality or exploitable under realistic conditions. | Access control bypass, Unchecked external calls, Oracle manipulation. |
| **Medium**   | Limited impact or requires specific, difficult-to-achieve conditions.                 | Timestamp dependence, Front-running, Denial of Service (DoS).         |
| **Low**      | Best practice violations, informational findings, or minor optimizations.             | Missing events, Floating pragma, Unused variables.                    |

## Key Inspection Areas

### Access Control & Authorization

- Verify `onlyOwner` or role-based access on all sensitive state-changing functions.
- Ensure initializers are protected and can only be called once.
- Check for `tx.origin` usage instead of `msg.sender`.

### External Call Safety

- Follow the Check-Effects-Interactions (CEI) pattern strictly.
- Use `call()` instead of `transfer()` or `send()` for ETH transfers.
- Handle return values of all external calls.

### State Management & Reentrancy

- Use `ReentrancyGuard` for functions making external calls.
- Check for cross-contract reentrancy where state is shared.
- Ensure state variables are updated before external interactions.

### Arithmetic & Type Safety

- For Solidity <0.8.0, ensure `SafeMath` is used.
- Check for precision loss in divisions (multiply before dividing).
- Verify safe casting between types (e.g., `uint256` to `uint8`).

### Token Handling (ERC20/721)

- Use `SafeERC20` for `transfer` and `transferFrom`.
- Account for "fee-on-transfer" tokens if applicable.
- Verify `approve` race condition handling.

### Upgrade Mechanisms

- Check for storage gaps in logic contracts to prevent collisions.
- Ensure logic contracts do not use `selfdestruct` or `delegatecall`.
- Verify the proxy admin has restricted access.

### Event Emissions

- Emit events for all significant state changes (ownership, parameters, transfers).
- Use `indexed` parameters for efficient off-chain filtering.

### NatSpec Documentation

- Ensure `@notice`, `@param`, and `@return` are accurate.
- Use `@dev` to document complex logic or security assumptions.

### Style Guide Compliance

- Code follows the official Solidity style guide conventions.
- Naming conventions: PascalCase (contracts), camelCase (functions), UPPER_CASE (constants).
- Function ordering: by visibility (external → public → internal → private), then by mutability (state-changing → view → pure) within each group.
- Function modifier order: visibility, mutability, virtual, override, custom.
- See the [Solidity Style Guide Reference](./references/solidity-style-guide.md) for the full checklist.

## Reporting Format

Findings should be documented using the following template:

### [SEVERITY] Finding Title

**ID**: SCWE-XXX _(replace with actual SCWE ID, e.g., SCWE-046 — see `search_vulnerabilities`)_
**Location**: `ContractName.sol:L42`
**Description**: Detailed explanation of the vulnerability and how it can be triggered.
**Impact**: What happens if this is exploited (e.g., "User funds can be stolen").
**Remediation**: Specific code changes or architectural adjustments to fix the issue.

## Enhanced with MCP

When using the `solidity-agent-toolkit`, leverage these tools in a structured review workflow:

**Step 1 — Static Analysis:**

- `run_slither` — Comprehensive static analysis with SCWE-mapped findings
- `run_aderyn` — Fast Rust-based vulnerability scanner
- `run_solhint` — Linting and style enforcement

**Step 2 — Pattern Detection:**

- `match_vulnerability_patterns` — Regex-based detection of 32+ common vulnerability patterns

**Step 3 — Vulnerability Lookup:**

- `search_vulnerabilities` — Search the OWASP SCWE database by keyword
- `get_remediation` — Get specific fix guidance with code examples for any SCWE ID
- `check_vulnerability` — Check if code matches a known SCWE pattern

**Step 4 — Style & Quality:**

- `check_style` — Automated Solidity style guide compliance (12 rules)
- `format_code` — Auto-format Solidity code
- `validate_natspec` — Verify NatSpec documentation completeness

**Step 5 — Full Audit:**

- Use the `security_audit` prompt for a structured, guided audit process
- Use the `code_review` prompt for comprehensive code quality assessment

## References

- [Smart Contract Audit Checklist](./references/audit-checklist.md)
- [Solidity Style Guide Reference](./references/solidity-style-guide.md)
