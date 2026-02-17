---
name: defi-security
description: "[AUTO-INVOKE] MUST be invoked BEFORE deploying DeFi contracts (DEX, lending, staking, LP, token). Covers anti-whale, anti-MEV, flash loan protection, launch checklists, and emergency response. Trigger: any deployment or security review of DeFi-related contracts."
---

# DeFi Security Principles

## Language Rule

- **Always respond in the same language the user is using.** If the user asks in Chinese, respond in Chinese. If in English, respond in English.

> **Scope**: Only applicable to DeFi projects (DEX, lending, staking, LP, yield). Non-DeFi projects can ignore this skill.

## Protection Decision Rules

| Threat | Required Protection |
|--------|-------------------|
| Whale manipulation | Daily transaction caps + per-tx amount limits + cooldown window |
| MEV / sandwich attack | EOA-only checks (`msg.sender == tx.origin`), or use commit-reveal pattern |
| Arbitrage | Referral binding + liquidity distribution + fixed yield model + lock period |
| Reentrancy | `ReentrancyGuard` on all external-call functions (see solidity-security skill) |
| Flash loan attack | Check `block.number` change between operations, or use TWAP pricing |
| Price manipulation | Chainlink oracle or TWAP — never rely on spot AMM reserves for pricing |
| Approval exploit | Use `safeIncreaseAllowance` / `safeDecreaseAllowance`, never raw `approve` for user flows |
| Governance attack | Voting requires snapshot + minimum token holding period; timelock ≥ 48h on proposal execution |
| ERC4626 inflation attack | First deposit must enforce minimum amount or use virtual shares to prevent share dilution via rounding |

## Anti-Whale Implementation Rules

- Maximum single transaction amount: configurable via `onlyOwner` setter
- Daily cumulative limit per address: track with `mapping(address => mapping(uint256 => uint256))` (address → day → amount)
- Cooldown between transactions: enforce minimum time gap with `block.timestamp` check
- Whitelist for exempt addresses (deployer, LP pair, staking contract)

## Flash Loan Protection Rules

- For price-sensitive operations: require that `block.number` has changed since last interaction
- For oracle-dependent calculations: use time-weighted average (TWAP) over minimum 30 minutes
- For critical state changes: add minimum holding period before action (e.g., must hold tokens for N blocks)

## Launch Checklist

Before mainnet deployment, verify all items:

- [ ] All `onlyOwner` functions transferred to multisig (e.g., Gnosis Safe)
- [ ] Timelock contract deployed and configured (minimum 24h delay for critical changes)
- [ ] `Pausable` emergency switch tested — both `pause()` and `unpause()` work correctly
- [ ] Daily limit parameters documented and set to reasonable values
- [ ] Third-party security audit completed and all critical/high findings resolved
- [ ] Testnet deployment running for minimum 7 days with no issues
- [ ] Slippage, fee, and lock period parameters reviewed and documented
- [ ] Initial liquidity plan documented (amount, lock duration, LP token handling)
- [ ] `forge test --fuzz-runs 10000` passes on all DeFi-critical functions

## Emergency Response Procedure

| Step | Action |
|------|--------|
| 1. Detect | Monitor alerts trigger (on-chain monitoring, community reports) |
| 2. Pause | Designated address calls `pause()` — must respond within minutes |
| 3. Assess | Technical lead analyzes root cause, estimates fund impact |
| 4. Communicate | Post incident notice to community channels (Discord, Twitter, Telegram) |
| 5. Fix | Deploy fix or prepare recovery plan |
| 6. Resume | Call `unpause()` after fix verified on fork — or migrate to new contract |
| 7. Post-mortem | Publish detailed incident report within 48 hours |

## DeFi Testing Commands

```bash
# Fuzz test fund flows with high iterations
forge test --match-contract StakingTest --fuzz-runs 10000

# Fork mainnet to test against real state
forge test --fork-url $MAINNET_RPC -vvvv

# Simulate whale transaction on fork
cast send <CONTRACT> "stake(uint256)" 1000000000000000000000000 \
  --rpc-url $FORK_RPC --private-key $TEST_KEY
```
