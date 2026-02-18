---
name: aave
description: Manage Aave V3 DeFi positions on Base — supply, borrow, repay, withdraw, and check account health. Includes liquidation safety checks.
license: MIT
compatibility: Requires Node.js 18+ and npx. Works with fibx CLI v0.3.2+.
metadata:
    version: 0.3.2
    author: ahmetenesdur
    category: defi-management
allowed-tools:
    - Bash(npx fibx@latest aave *)
    - Bash(npx fibx@latest status)
    - Bash(npx fibx@latest balance *)
    - Bash(npx fibx@latest balance)
---

# Aave V3 Management

Interact with the Aave V3 lending protocol on **Base only**. Supply assets to earn yield, borrow against collateral, repay debt, or withdraw.

## Prerequisites

- Active session required.
- Sufficient ETH on Base for gas fees.

## Rules

1. This skill ONLY works on **Base**. NEVER attempt Aave operations on Citrea, HyperEVM, or Monad. If requested, refuse and explain.
2. BEFORE any action, run `npx fibx@latest balance` to verify enough ETH for gas.
3. BEFORE `borrow`, you MUST run `npx fibx@latest aave status` to check the Health Factor:
    - Health Factor < **1.5** → WARN the user about liquidation risk.
    - Health Factor < **1.1** → DO NOT proceed without explicit double-confirmation from the user.
4. When the user wants to fully close a position, ALWAYS use `max` as the amount for `repay` and `withdraw`. This sends `MAX_UINT256` to the contract and prevents dust residuals.
5. When supplying or withdrawing ETH, the CLI handles the ETH ↔ WETH conversion automatically. Use `ETH` as the token symbol.

## Commands

```bash
npx fibx@latest aave <action> [amount] [token] [--json]
```

## Actions

| Action     | Description                    | Example                                  |
| ---------- | ------------------------------ | ---------------------------------------- |
| `status`   | Account health, LTV, net worth | `npx fibx@latest aave status`            |
| `supply`   | Deposit assets to earn yield   | `npx fibx@latest aave supply 100 USDC`   |
| `borrow`   | Borrow against collateral      | `npx fibx@latest aave borrow 0.5 ETH`    |
| `repay`    | Repay borrowed position        | `npx fibx@latest aave repay max USDC`    |
| `withdraw` | Withdraw supplied assets       | `npx fibx@latest aave withdraw max USDC` |

## Parameters

| Parameter | Type   | Description                                          | Required              |
| --------- | ------ | ---------------------------------------------------- | --------------------- |
| `action`  | string | `status`, `supply`, `borrow`, `repay`, or `withdraw` | Yes                   |
| `amount`  | string | Amount or `max` (for full repay/withdraw)            | Yes (except `status`) |
| `token`   | string | Token symbol (`USDC`, `ETH`, `DAI`, etc.)            | Yes (except `status`) |
| `json`    | flag   | Output as JSON                                       | No                    |

## Dust Handling

When repaying or withdrawing, **always prefer `max`** if the user wants to fully close a position.

Passing `max` sends `MAX_UINT256` to the Aave contract, which covers all accrued interest and prevents tiny residual balances (e.g. `0.000001 USDC`) from remaining.

```bash
npx fibx@latest aave repay max USDC      # Repays all debt including accrued interest
npx fibx@latest aave withdraw max USDC   # Withdraws entire supplied position
```

## Examples

**User:** "How is my Aave position doing?"

```bash
npx fibx@latest aave status
```

**User:** "Supply 100 USDC to Aave"

```bash
npx fibx@latest balance
npx fibx@latest aave supply 100 USDC
```

**User:** "Borrow 0.5 ETH from Aave"

```bash
npx fibx@latest aave status
# If Health Factor > 1.5:
npx fibx@latest aave borrow 0.5 ETH
```

**User:** "Repay all my USDC debt"

```bash
npx fibx@latest aave repay max USDC
```

## Error Handling

| Error                     | Action                                                         |
| ------------------------- | -------------------------------------------------------------- |
| `Health Factor too low`   | Blocked to prevent liquidation. Suggest repaying or supplying. |
| `Insufficient collateral` | Cannot borrow without supplying first.                         |
| `Insufficient balance`    | Check `balance` — user may need to swap for the token first.   |
| `Not authenticated`       | Run `authenticate-wallet` skill first.                         |

## Related Skills

- Use `trade` to swap tokens before supplying (e.g. swap ETH → USDC, then supply USDC).
- Use `balance` to verify available assets before any Aave operation.
