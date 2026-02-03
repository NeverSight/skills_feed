---
name: euler-advanced
description: Advanced features guide for Euler Finance V2 protocol. This skill should be used when implementing vault hooks, flash loans, debt transfer, fee flow mechanics, or EUL rewards. Triggers on tasks involving hooks, pause guardians, access control, flash loans, pullDebt, FeeFlowController, or RewardToken.
license: MIT
metadata:
  author: Euler Labs
  version: "1.0.0"
---

# Euler Advanced Features Agent Skill

Advanced features guide for Euler Finance V2 protocol. Covers hooks, flash loans, fee flow, and rewards.

## When to Apply

Reference these guidelines when:
- Implementing vault hooks (pause, access control, custom logic)
- Using flash loans for arbitrage or liquidations
- Transferring debt between accounts with pullDebt
- Understanding fee flow and Dutch auctions
- Working with locked EUL reward tokens
- Implementing access control hooks

## Rule Categories

| Rule | Impact | Description |
|------|--------|-------------|
| `adv-hooks` | MEDIUM | Vault hooks for custom logic and access control |
| `adv-flashloan-pulldebt` | HIGH | Flash loans and debt transfer operations |
| `adv-fee-flow` | MEDIUM | Fee flow controller and Dutch auctions |
| `adv-rewards-eul` | MEDIUM | EUL reward token vesting and distribution |

## Quick Reference

### Key Concepts

1. **Hooks** - Custom logic before vault operations
2. **Flash Loans** - Borrow and repay in same transaction (FREE)
3. **pullDebt** - Take on another account's debt
4. **FeeFlowController** - Dutch auction for protocol fees
5. **RewardToken** - Locked EUL with 20% immediate, 80% over 6 months

## Companion Skills

- `euler-vaults` - Core vault operations, EVC, risk management
- `euler-irm-oracles` - Oracle adapters and interest rate models
- `euler-earn` - Yield aggregation vaults
- `euler-data` - Lens contracts and data querying

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/adv-hooks.md
rules/adv-flashloan-pulldebt.md
rules/adv-fee-flow.md
rules/adv-rewards-eul.md
```

## Full Compiled Document

For the complete guide with all rules expanded: `AGENTS.md`
