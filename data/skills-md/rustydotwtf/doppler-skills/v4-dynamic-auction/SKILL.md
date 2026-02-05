---
name: v4-dynamic-auction
description: Reference for Doppler V4 dynamic auctions. Use when working with the Doppler hook, epoch-based rebalancing, tick accumulator, or V4-based token launches. Covers gamma, slug types, dynamic auction modes, and exit conditions.
metadata:
  author: doppler
  version: "1.0"
---

> **Source References**: Code citations link to raw GitHub files pinned to commit `988dab4`. To fetch specific lines: `curl -s "<url>" | sed -n 'START,ENDp'`

# V4 Dynamic Auction

A V4 dynamic auction uses a **Uniswap V4 hook** to automatically rebalance the bonding curve every epoch based on actual sales performance. Unlike V3 static auctions, the price curve actively adjusts.

## Key Contracts

| Contract | Path | Purpose |
|----------|------|---------|
| Doppler | `src/initializers/Doppler.sol` | Main V4 dynamic auction hook |
| UniswapV4Initializer | `src/initializers/UniswapV4Initializer.sol` | V4 pool initialization |

## Dynamic vs Static

| Aspect | V3 Static | V4 Dynamic |
|--------|-----------|------------|
| Rebalancing | None | Every epoch via `beforeSwap` |
| Position count | Fixed at init | 3 slug types, repositioned |
| Price discovery | Passive (swaps move price) | Active (tick accumulator) |
| Dynamic auction | N/A | Max, Relative, or Oversold |
| Exit condition | Price at far tick | Proceeds thresholds or time |

## Quick Facts

| Fact | Value | Source |
|------|-------|--------|
| Precision constant | `WAD = 1e18` | `Doppler.sol:153` |
| Max tick spacing | 30 | `Doppler.sol:159` |
| Max price discovery slugs | 15 | `Doppler.sol:162` |
| Default slug count | 3 (Lower, Upper, PD) | `Doppler.sol:165` |

## Parameters Reference

| Parameter | Type | Description |
|-----------|------|-------------|
| `gamma` | `int24` | Max tick change for entire curve |
| `epochLength` | `uint256` | Rebalance frequency (seconds) |
| `numTokensToSell` | `uint256` | Total tokens for sale |
| `minimumProceeds` | `uint256` | Refund threshold |
| `maximumProceeds` | `uint256` | Early exit threshold |
| `startingTick` | `int24` | Initial price tick |
| `endingTick` | `int24` | Final price after full auction |
| `numPDSlugs` | `uint256` | Price discovery positions (1-15) |

[Detailed parameters](references/PARAMETERS.md)

## Three Slug Types

| Slug | Purpose | Token Type | Range |
|------|---------|------------|-------|
| **Lower** | Refund support at average price | Numeraire | tickLower → currentTick |
| **Upper** | Current epoch liquidity | Asset | currentTick → currentTick + upperSlugRange |
| **Price Discovery** | Future epoch liquidity | Asset | Above upper slug → tickUpper |

[Source: Doppler.sol](https://raw.githubusercontent.com/whetstoneresearch/doppler/988dab4/src/initializers/Doppler.sol) (lines 167-171, salt constants)

**Note: No Tail Positions**

V4 dynamic auctions do **not** use tail positions (unlike V3 static and V4 multicurve auctions). The 3 dynamic slug types replace this concept:

- **Price Discovery slugs** extend toward the far tick dynamically
- **Epoch-based rebalancing** continuously redistributes liquidity
- **Proceeds-based exit** eliminates the need for tick-based tail positions

See [v3-static-auction](../v3-static-auction/references/FORMULAS.md#tail-position) or [v4-multicurve-auction](../v4-multicurve-auction/references/FORMULAS.md#tail-position) for tail position details.

## Dynamic Auction Modes

| Scenario | Condition | Action |
|----------|-----------|--------|
| **Max Adjustment** | No sales + behind schedule | Full `_getMaxTickDeltaPerEpoch()` |
| **Relative Adjustment** | Some sales but undersold | `delta * (1 - actualSold/expectedSold)` |
| **Oversold** | Ahead of schedule | Move curve UP (worse prices) |

[Source: Doppler.sol](https://raw.githubusercontent.com/whetstoneresearch/doppler/988dab4/src/initializers/Doppler.sol) (lines 630-665)

## Three Exit Paths

| Path | Condition | Behavior |
|------|-----------|----------|
| **Early Exit** | `proceeds >= maximumProceeds` | Immediate migration available |
| **Success** | `proceeds >= minimumProceeds` at `endingTime` | Migration available |
| **Insufficient** | `proceeds < minimumProceeds` at `endingTime` | Refund phase (sell back at avg price) |

[Source: Doppler.sol](https://raw.githubusercontent.com/whetstoneresearch/doppler/988dab4/src/initializers/Doppler.sol) (lines 400, 412-467, 574-577)

## Epoch System

```
Epoch = (block.timestamp - startingTime) / epochLength + 1
```

- Epochs are 1-indexed
- Rebalance triggers in `beforeSwap` when entering a new epoch
- Only one rebalance per epoch (check: `_getCurrentEpoch() <= state.lastEpoch`)

[Source: Doppler.sol](https://raw.githubusercontent.com/whetstoneresearch/doppler/988dab4/src/initializers/Doppler.sol) (lines 791-794, 404-407)

## State Tracking

```solidity
struct State {
    uint40 lastEpoch;              // Last rebalanced epoch
    int256 tickAccumulator;        // Cumulative price adjustment
    uint256 totalTokensSold;       // Tokens sold to date
    uint256 totalProceeds;         // Numeraire earned
    uint256 totalTokensSoldLastEpoch;
    BalanceDelta feesAccrued;      // Accumulated fees
}
```

[Source: Doppler.sol](https://raw.githubusercontent.com/whetstoneresearch/doppler/988dab4/src/initializers/Doppler.sol) (lines 44-51)

## Common Tasks

- **Understanding parameters**: See [PARAMETERS.md](references/PARAMETERS.md)
- **Understanding the lifecycle**: See [FLOW.md](references/FLOW.md)
- **Understanding the math**: See [FORMULAS.md](references/FORMULAS.md)
- **Avoiding pitfalls**: See [GOTCHAS.md](references/GOTCHAS.md)

## Related Skills

- [fee-architecture](../fee-architecture/SKILL.md) - Fee collection and distribution
- [token-lifecycle](../token-lifecycle/SKILL.md) - Vesting and inflation mechanics
- [v4-multicurve-auction](../v4-multicurve-auction/SKILL.md) - Multicurve V4 auctions with farTick
- [uniswap-fundamentals](../uniswap-fundamentals/SKILL.md) - Tick math and V4 architecture
