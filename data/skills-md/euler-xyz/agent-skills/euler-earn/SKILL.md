---
name: euler-earn
description: EulerEarn yield aggregation guide for Euler Finance. This skill should be used when creating yield aggregation vaults, managing strategies, configuring roles, or using PublicAllocator. Triggers on tasks involving EulerEarn vaults, strategy allocation, yield optimization, or meta-vault management.
license: MIT
metadata:
  author: Euler Labs
  version: "1.0.0"
---

# EulerEarn Agent Skill

EulerEarn yield aggregation guide for Euler Finance. Covers vault creation, strategy management, and role-based governance.

## When to Apply

Reference these guidelines when:
- Creating EulerEarn yield aggregation vaults
- Managing strategies (caps, queues, reallocation)
- Configuring roles (owner, curator, guardian, allocator)
- Using PublicAllocator for permissionless reallocation
- Setting up timelocked governance
- Monitoring strategy APYs and allocation

## Rule Categories

| Rule | Impact | Description |
|------|--------|-------------|
| `earn-create-vault` | MEDIUM | Deploy EulerEarn yield aggregation vaults |
| `earn-manage-strategies` | MEDIUM | Manage strategies and allocations |

## Quick Reference

### Role Permissions

| Role | Capabilities |
|------|-------------|
| Owner | All actions, set other roles, set fee |
| Curator | Manage caps, submit removals, allocator actions |
| Guardian | Revoke pending changes, emergency stops |
| Allocator | Set queues, reallocate funds |

### Key Concepts

1. **Meta-Vaults** - ERC-4626 vaults that allocate across strategies
2. **Supply Queue** - Order for depositing into strategies
3. **Withdraw Queue** - Order for withdrawing from strategies
4. **Timelocked Governance** - Cap increases require timelock
5. **PublicAllocator** - Permissionless reallocation with flow caps

## Companion Skills

- `euler-vaults` - Core vault operations, EVC, risk management
- `euler-irm-oracles` - Oracle adapters and interest rate models
- `euler-advanced` - Hooks, flash loans, fee flow
- `euler-data` - Lens contracts and data querying

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/earn-create-vault.md
rules/earn-manage-strategies.md
```

## Full Compiled Document

For the complete guide with all rules expanded: `AGENTS.md`
