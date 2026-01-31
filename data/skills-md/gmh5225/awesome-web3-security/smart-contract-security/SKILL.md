---
name: smart-contract-security
description: "Guide for EVM/solidity smart contract security work: vulnerability taxonomy, review workflow, and where to place resources in README.md."
---

# Smart Contract Security (EVM / Solidity)

## Scope

Use this skill when working on:

- Solidity/EVM auditing resources
- EVM vulnerability categories and examples
- Tooling for contract analysis (static, dynamic, fuzzing)

## Common Vulnerabilities (Cheat Sheet)

- Reentrancy
- Access control bugs
- Price oracle manipulation
- MEV / sandwich / frontrunning
- Flash loan enabled logic flaws
- Precision / rounding / decimal mismatch
- Signature and permit mistakes (EIP-2612 / Permit2)
- Upgradeability mistakes (UUPS / Transparent)

## Recommended Review Workflow

1. **Threat model**: assets, trust boundaries, privileged roles
2. **State machine**: invariants, transitions, edge cases
3. **Access control**: ownership, roles, upgrade admin
4. **External calls**: reentrancy, callback surfaces, token hooks
5. **Economic analysis**: pricing, liquidity, oracle, incentives
6. **Testing**: unit tests + fuzzing + invariant tests
7. **Reporting**: severity, exploitability, PoC, remediation

## Where to Add Links in README

- New analyzers/fuzzers: `Development → Tools` or `Security` (choose primary)
- Audit methodologies/standards: `Security`
- Practice labs/CTFs: `Security Starter Pack → CTFs / Practice`
- Audit report portfolios: `Security Starter Pack → Audit Reports`

## Notes

Keep additions:

- English descriptions
- Non-duplicated URLs
- Minimal structural changes

## Data Source

For detailed and up-to-date resources, fetch the full list from:
```
https://raw.githubusercontent.com/gmh5225/awesome-web3-security/refs/heads/main/README.md
```

