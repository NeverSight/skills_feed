---
name: solidity-security-audit
description: >
  Comprehensive Solidity smart contract security auditing and vulnerability analysis skill.
  Based on methodologies from Trail of Bits, OpenZeppelin, Consensys Diligence, Sherlock,
  CertiK, Cyfrin, Spearbit, Halborn, and other leading Web3 security firms.
  This skill should be used whenever the user asks to "audit a smart contract",
  "review Solidity code for security", "find vulnerabilities", "check for reentrancy",
  "analyze gas optimization", "review access control", "check proxy patterns",
  "analyze DeFi protocol security", "review ERC20/ERC721 implementation",
  "check oracle manipulation risks", "review upgrade patterns", or mentions any
  security review of EVM-compatible smart contracts. Also triggers for keywords like
  "slither", "echidna", "foundry fuzz", "formal verification", "invariant testing",
  "flash loan attack", "MEV", "sandwich attack", "front-running", "delegatecall",
  "selfdestruct", "reentrancy guard", "access control vulnerability",
  "storage collision", "proxy upgrade security", "smart contract exploit",
  "L2 security", "cross-chain", "bridge security", "sequencer", "LayerZero", "CCIP",
  "account abstraction", "ERC-4337", "smart account", "paymaster", "bundler", "UserOperation",
  "re-audit", "diff audit", "remediation review", "fix verification", "Uniswap v4 hooks",
  "Chainlink integration", "Aave integration", "flash loan receiver", "ERC-4626 vault",
  "restaking", "EigenLayer", "severity classification", "severity decision".
  Even if the user simply pastes Solidity code and asks "is this safe?" or
  "any issues here?", use this skill.
---

# Solidity Security Audit Skill

## Purpose

Perform professional-grade smart contract security audits following methodologies
established by the world's leading Web3 security firms. Produce actionable,
severity-classified findings with remediation guidance.

## Audit Mode Selection

Before starting, identify the audit mode:

| Mode | When to Use | Entry Point |
|------|-------------|-------------|
| **Full Audit** | First-time review of a codebase | Phases 1–5 below |
| **Re-audit / Diff** | Previous audit exists; team applied fixes or added features | `references/diff-audit.md` |
| **Integration Review** | Contract integrates Uniswap, Chainlink, Aave, Curve, etc. | `references/defi-integrations.md` + Phase 3 |
| **Quick Scan** | Rapid assessment, limited time | `references/quick-reference.md` |

For severity classification guidance at any point, consult `references/severity-decision-tree.md`.

---

## Full Audit Workflow

Execute audits in this order. Each phase builds on the previous one.

### Phase 1 — Reconnaissance

1. Identify the Solidity version, compiler settings, and framework (Hardhat/Foundry)
2. Map the contract architecture: inheritance tree, library usage, external dependencies
3. Identify the protocol type (DeFi lending, AMM, NFT, governance, bridge, vault, etc.)
4. Determine the trust model: who are the privileged roles? What can they do?
5. List all external integrations (oracles, other protocols, token standards)

### Phase 2 — Automated Analysis

If tools are available in the environment, run them in this order:

```
# Static analysis
slither . --json slither-report.json

# Compile and test
forge build
forge test --gas-report

# Custom detectors (if Aderyn is available)
aderyn .
```

If tools are NOT available, perform manual static analysis covering the same
categories these tools check. Read `references/tool-integration.md` for details.

### Phase 3 — Manual Review (Core)

This is where the highest-value findings come from. Follow the vulnerability
taxonomy in `references/vulnerability-taxonomy.md` systematically:

**CRITICAL PRIORITY — Check these first:**
- Reentrancy (all variants: cross-function, cross-contract, read-only)
- Access control flaws (missing modifiers, incorrect role checks, unprotected initializers)
- Price oracle manipulation (spot price usage, single oracle dependency, TWAP bypass)
- Flash loan attack vectors
- Proxy/upgrade vulnerabilities (storage collision, uninitialized implementation, UUPS gaps)
- Unchecked external calls and return values

**HIGH PRIORITY:**
- Integer overflow/underflow (pre-0.8.x or unchecked blocks)
- Logic errors in business rules (token minting, reward calculations, fee distribution)
- Front-running and MEV exposure (sandwich attacks, transaction ordering dependence)
- Denial of Service vectors (gas griefing, unbounded loops, block gas limit)
- Signature replay and malleability
- Delegatecall to untrusted contracts

**MEDIUM PRIORITY:**
- Gas optimization issues that affect usability
- Missing event emissions for state changes
- Centralization risks and single points of failure
- Timestamp dependence
- Floating pragma versions
- Missing zero-address checks

**LOW / INFORMATIONAL:**
- Code style and readability
- Unused variables and imports
- Missing NatSpec documentation
- Redundant code patterns

### Phase 4 — DeFi-Specific Analysis

When auditing DeFi protocols, apply the specialized checklist from
`references/defi-checklist.md`. Key areas:

- **Lending protocols**: Liquidation logic, collateral factor manipulation, bad debt scenarios
- **AMMs/DEXs**: Slippage protection, price impact calculations, LP token accounting
- **Vaults/Yield**: Share price manipulation (inflation attack), withdrawal queue logic
- **Bridges**: Message verification, replay protection, validator trust assumptions
- **Governance**: Vote manipulation, flash loan governance attacks, timelock bypass
- **Staking**: Reward calculation precision, stake/unstake timing attacks

### Phase 5 — Report Generation

Structure every finding using this format:

```
## [SEVERITY-ID] Title

**Severity**: Critical | High | Medium | Low | Informational
**Category**: (from vulnerability taxonomy)
**Location**: `ContractName.sol#L42-L58`

### Description
Clear explanation of the vulnerability, why it exists, and what an attacker could do.

### Impact
Concrete description of damage: funds at risk, protocol disruption, data corruption.

### Proof of Concept
Step-by-step exploit scenario or code demonstrating the issue.

### Recommendation
Specific code changes to fix the vulnerability. Include example code when possible.
```

Classify severity following the standard used by Immunefi, Code4rena, and Sherlock:

| Severity | Criteria |
|----------|----------|
| **Critical** | Direct loss of funds, permanent protocol corruption, bypass of all access controls |
| **High** | Conditional loss of funds, significant protocol disruption, privilege escalation |
| **Medium** | Indirect loss, limited impact requiring specific conditions, griefing with cost |
| **Low** | Minor issues, best practice violations, theoretical edge cases |
| **Informational** | Code quality, gas optimizations, documentation gaps |

## Key Patterns to Enforce

### Checks-Effects-Interactions (CEI)
Every function that modifies state and makes external calls must follow CEI.
Verify state changes happen BEFORE any external call.

### Pull Over Push
Favor withdrawal patterns over direct transfers. Let users claim rather than
pushing funds to them automatically.

### Least Privilege
Every function should have the minimum required access level. Prefer role-based
access control (OpenZeppelin AccessControl) over single-owner patterns.

### Defense in Depth
No single security mechanism should be the only protection. Layer reentrancy
guards, access controls, input validation, and invariant checks.

## Reference Materials

For detailed vulnerability descriptions, exploit examples, and remediation
patterns, consult these reference files:

### Core References
- `references/vulnerability-taxonomy.md` — 40+ vulnerability types with code examples
- `references/defi-checklist.md` — Protocol-specific checklists (lending, AMM, vaults, bridges, tokens)
- `references/industry-standards.md` — SWC Registry, severity classification, security EIPs
- `references/quick-reference.md` — One-page cheat sheet for rapid security assessment

### Audit Guides
- `references/audit-questions.md` — Systematic questions for each function type
- `references/secure-patterns.md` — Secure code patterns to compare against
- `references/report-template.md` — Professional audit report format

### Testing & Tools
- `references/tool-integration.md` — Slither, Echidna, Foundry, Halmos, custom detectors
- `references/automated-detection.md` — Regex patterns for automated scanning
- `references/poc-templates.md` — Foundry templates for proving exploits
- `references/invariants.md` — Protocol invariants for testing

### Specialized
- `references/l2-crosschain.md` — L2 sequencer risks, bridge security, cross-chain patterns
- `references/account-abstraction.md` — ERC-4337 security: accounts, paymasters, bundlers
- `references/exploit-case-studies.md` — Real-world exploits analyzed (DAO, Euler, Curve, etc.)

### New in v2
- `references/diff-audit.md` — Re-audit and change review methodology
- `references/severity-decision-tree.md` — Structured severity classification decision trees
- `references/defi-integrations.md` — Secure integration patterns: Uniswap v3/v4, Chainlink, Aave, Curve, Balancer

Load these files as needed based on the specific audit context.

## Important Notes

- Always state clearly if the review is a limited automated scan vs. a full manual audit
- Never guarantee that code is "100% secure" — audits reduce risk, they don't eliminate it
- Flag centralization risks even if they aren't traditional "vulnerabilities"
- Consider the economic incentives: would the exploit be profitable given gas costs?
- Check interactions with common DeFi primitives (flash loans, MEV, composability)
- When in doubt about severity, read how Sherlock, Code4rena, and Immunefi classify similar findings
