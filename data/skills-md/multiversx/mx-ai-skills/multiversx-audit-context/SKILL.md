---
name: multiversx-audit-context
description: Build mental models of MultiversX codebases before security auditing. Use when starting a new audit, onboarding to unfamiliar code, or mapping system architecture for vulnerability research.
---

# Audit Context Building

Rapidly build a comprehensive mental model of a MultiversX codebase before diving into vulnerability hunting. This skill ensures you understand the system holistically before searching for specific issues.

## When to Use

- Starting a new security audit engagement
- Onboarding to an unfamiliar MultiversX project
- Mapping attack surface for penetration testing
- Preparing for code review sessions

## 1. Reconnaissance

### Identify the Core
Locate where critical logic and value flows reside:

- **Smart Contracts**: Look for `#[multiversx_sc::contract]`, `#[payable("*")]`, and `impl` blocks
- **Value Handlers**: Functions that move EGLD/ESDT tokens
- **Access Control**: Owner-only functions, whitelists, role systems

### Identify Externalities
Map external dependencies and interactions:

- **Cross-Contract Calls**: Which other contracts does this interact with?
- **Hardcoded Addresses**: Look for `sc:` smart contract literals
- **Oracle Dependencies**: External data sources the contract relies on
- **Bridge Contracts**: Any cross-chain or cross-shard communication

### Identify Documentation
Gather all available context:

- **Standard Files**: `README.md`, `specs/`, `whitepaper.pdf`
- **MultiversX Specific**: `mxpy.json` (build config), `multiversx.yaml`, `snippets.sh`
- **Test Scenarios**: `scenarios/` directory with Mandos tests

## 2. System Mapping

Create a structured map of the system architecture:

### Roles and Permissions
| Role | Capabilities | How Assigned |
|------|-------------|--------------|
| Owner | Full admin access | Deploy-time, transferable |
| Admin | Limited admin functions | Owner grants |
| User | Public endpoints | Anyone |
| Whitelisted | Special access | Admin grants |

### Asset Inventory
| Asset Type | Examples | Risk Level |
|------------|----------|------------|
| EGLD | Native currency | Critical |
| Fungible ESDT | Custom tokens | High |
| NFT/SFT | Non-fungible tokens | Medium-High |
| Meta-ESDT | Tokens with metadata | Medium-High |

### State Analysis
Document all storage mappers and their purposes:

```rust
// Example state inventory
#[storage_mapper("owner")]           // SingleValueMapper - access control
#[storage_mapper("balances")]        // MapMapper - user funds (CRITICAL)
#[storage_mapper("whitelist")]       // SetMapper - privileged users
```

## 3. Threat Modeling (Initial)

### Asset at Risk Analysis
- **Direct Loss**: What funds can be stolen if the contract fails?
- **Indirect Loss**: What downstream systems depend on this contract?
- **Reputation Loss**: What non-financial damage could occur?

### Attacker Profiles
| Attacker | Motivation | Capabilities |
|----------|------------|--------------|
| External User | Profit | Public endpoints only |
| Malicious Admin | Insider threat | Admin functions |
| Reentrant Contract | Exploit callbacks | Cross-contract calls |
| Front-runner | MEV extraction | Transaction ordering |

### Entry Point Enumeration
List all `#[endpoint]` functions with their risk classification:

```
HIGH RISK:
- deposit() - #[payable("*")] - accepts value
- withdraw() - moves funds out
- upgrade() - can change contract logic

MEDIUM RISK:
- setConfig() - owner only, changes behavior
- addWhitelist() - expands permissions

LOW RISK:
- getBalance() - #[view] - read only
```

## 4. Environment Check

### Dependency Audit
- **Framework Version**: Check `Cargo.toml` for `multiversx-sc` version
- **Known Vulnerabilities**: Compare against security advisories
- **Deprecated APIs**: Look for usage of deprecated functions

### Test Suite Assessment
- **Coverage**: Does `scenarios/` exist with comprehensive tests?
- **Edge Cases**: Are failure paths tested?
- **Freshness**: Run `sc-meta test-gen` to verify tests match current code

### Build Configuration
- **Optimization Level**: Check for debug vs release builds
- **WASM Size**: Large binaries may indicate bloat or complexity

## 5. Output Deliverable

After completing context building, document:

1. **System Overview**: One-paragraph summary of what the contract does
2. **Trust Boundaries**: Who trusts whom, what assumptions exist
3. **Critical Paths**: The most security-sensitive code paths
4. **Initial Concerns**: Preliminary list of areas requiring deep review
5. **Questions for Team**: Clarifications needed from developers

## Checklist

Before proceeding to detailed audit:

- [ ] All entry points identified and classified
- [ ] Storage layout documented
- [ ] External dependencies mapped
- [ ] Role/permission model understood
- [ ] Test coverage assessed
- [ ] Framework version noted
- [ ] Initial threat model drafted
