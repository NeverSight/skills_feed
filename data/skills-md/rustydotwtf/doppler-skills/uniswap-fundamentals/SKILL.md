---
name: uniswap-fundamentals
description: Reference for Uniswap protocol concepts used in Doppler development. Covers tick math, sqrtPriceX96, liquidity formulas (V3+V4), and V4-specific features like hooks and singleton architecture. Each section clearly marks which version it applies to.
metadata:
  author: uniswap
  version: "1.0"
  source: docs.uniswap.org
---

# Uniswap Fundamentals

Core Uniswap concepts needed for Doppler development. **Each section clearly indicates which version(s) it applies to.**

## Version Legend

| Tag | Meaning |
|-----|---------|
| **[V2]** | Uniswap V2 only |
| **[V3]** | Uniswap V3 only |
| **[V4]** | Uniswap V4 only |
| **[V3+V4]** | Applies to both V3 and V4 (concentrated liquidity) |

## Version Comparison

| Feature | V2 | V3 | V4 |
|---------|----|----|-----|
| Liquidity type | Full range | Concentrated | Concentrated |
| Position representation | ERC-20 LP tokens | NFT | Via PoolManager |
| Price representation | Reserves ratio | sqrtPriceX96 | sqrtPriceX96 |
| Tick system | N/A | Yes | Yes |
| Fee tiers | Fixed 0.3% | 0.01%, 0.05%, 0.30%, 1% | Dynamic |
| Pool architecture | Factory + Pair contracts | Factory + Pool contracts | Singleton PoolManager |
| Hooks | N/A | N/A | Yes |
| Native ETH | No (WETH only) | No (WETH only) | Yes |

[Source: Uniswap Docs](https://docs.uniswap.org)

## Quick Reference

| Concept | Version | Reference |
|---------|---------|-----------|
| sqrtPriceX96 / Q notation | V3+V4 | [TICK-MATH.md](references/TICK-MATH.md) |
| Tick-to-price conversion | V3+V4 | [TICK-MATH.md](references/TICK-MATH.md) |
| Tick spacing by fee tier | V3 only | [TICK-MATH.md](references/TICK-MATH.md) |
| Tick spacing (dynamic) | V4 only | [TICK-MATH.md](references/TICK-MATH.md) |
| Liquidity formulas | V3+V4 | [LIQUIDITY.md](references/LIQUIDITY.md) |
| Concentrated positions | V3+V4 | [LIQUIDITY.md](references/LIQUIDITY.md) |
| Singleton architecture | V4 only | [V4-ARCHITECTURE.md](references/V4-ARCHITECTURE.md) |
| Flash accounting | V4 only | [V4-ARCHITECTURE.md](references/V4-ARCHITECTURE.md) |
| Hooks system | V4 only | [V4-HOOKS.md](references/V4-HOOKS.md) |

## Doppler Usage Map

| Doppler Skill | Uniswap Concepts Used |
|---------------|----------------------|
| v3-static-auction | [V3] tick spacing, LiquidityAmounts, tick alignment |
| v4-dynamic-auction | [V3+V4] sqrtPriceX96, TickMath, [V4] hooks (beforeSwap, afterSwap) |
| v4-multicurve-auction | [V3+V4] sqrtPriceX96, LiquidityAmounts, tick alignment |

## Critical: Token Ordering **[V2+V3+V4]**

**All Uniswap versions** enforce `token0 < token1` ordering by address.

This affects:
- Which token is "token0" vs "token1"
- Tick direction interpretation
- Price direction interpretation
- The `isToken0` flag in Doppler contracts

See [TICK-MATH.md](references/TICK-MATH.md) for how this affects calculations.

## References

- [TICK-MATH.md](references/TICK-MATH.md) - sqrtPriceX96, Q notation, tick conversions
- [LIQUIDITY.md](references/LIQUIDITY.md) - Liquidity formulas, concentrated positions
- [V4-ARCHITECTURE.md](references/V4-ARCHITECTURE.md) - Singleton, flash accounting, dynamic fees
- [V4-HOOKS.md](references/V4-HOOKS.md) - Hook lifecycle, permissions, patterns
