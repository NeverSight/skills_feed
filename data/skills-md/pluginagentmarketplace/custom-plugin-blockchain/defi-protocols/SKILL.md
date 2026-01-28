---
name: defi-protocols
description: Master DeFi protocol development including AMMs, lending, yield, and oracles
sasmp_version: "1.3.0"
version: "2.0.0"
updated: "2025-01"
bonded_agent: 04-defi-specialist
bond_type: PRIMARY_BOND

# Skill Configuration
atomic: true
single_responsibility: defi_development

# Parameter Validation
parameters:
  protocol_type:
    type: string
    required: true
    enum: [amm, lending, yield, oracle, flash_loan]
  chain:
    type: string
    default: ethereum

# Retry & Error Handling
retry_config:
  max_attempts: 3
  backoff: exponential
  initial_delay_ms: 1000

# Logging & Observability
logging:
  level: info
  include_timestamps: true
  track_usage: true
---

# DeFi Protocols Skill

> Master DeFi protocol development including AMM mechanics, lending systems, yield optimization, and oracle integration.

## Quick Start

```python
# Invoke this skill for DeFi development
Skill("defi-protocols", protocol_type="amm", chain="ethereum")
```

## Topics Covered

### 1. AMM (Automated Market Makers)
Build decentralized exchanges:
- **Constant Product**: x * y = k (Uniswap V2)
- **Concentrated Liquidity**: Tick-based (Uniswap V3)
- **Stable Swaps**: Curve invariant
- **TWAP**: Time-weighted average price

### 2. Lending Protocols
Create lending markets:
- **Overcollateralized**: Aave/Compound model
- **Interest Rates**: Utilization-based curves
- **Liquidation**: Health factor, incentives
- **Isolated Markets**: Risk segmentation

### 3. Yield Optimization
Maximize returns:
- **Auto-compounding**: Vault strategies
- **Liquidity Mining**: Reward distribution
- **veTokens**: Vote-escrowed governance
- **Bribes**: Gauge voting incentives

### 4. Oracle Integration
Secure price feeds:
- **Chainlink**: Decentralized oracles
- **TWAP**: Manipulation resistant
- **Staleness Checks**: Price freshness
- **Fallbacks**: Multi-oracle setups

## Code Examples

### AMM Swap Calculation
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

library SwapMath {
    uint256 constant FEE_NUMERATOR = 997;
    uint256 constant FEE_DENOMINATOR = 1000;

    /// @notice Calculate output amount for constant product AMM
    function getAmountOut(
        uint256 amountIn,
        uint256 reserveIn,
        uint256 reserveOut
    ) internal pure returns (uint256) {
        uint256 amountInWithFee = amountIn * FEE_NUMERATOR;
        uint256 numerator = amountInWithFee * reserveOut;
        uint256 denominator = reserveIn * FEE_DENOMINATOR + amountInWithFee;
        return numerator / denominator;
    }

    /// @notice Calculate price impact percentage (basis points)
    function getPriceImpact(
        uint256 amountIn,
        uint256 reserveIn
    ) internal pure returns (uint256) {
        return (amountIn * 10000) / (reserveIn + amountIn);
    }
}
```

### Chainlink Oracle
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

contract PriceOracle {
    AggregatorV3Interface public immutable priceFeed;
    uint256 public constant STALENESS_THRESHOLD = 1 hours;

    error StalePrice();
    error InvalidPrice();

    constructor(address feed) {
        priceFeed = AggregatorV3Interface(feed);
    }

    function getPrice() external view returns (uint256) {
        (, int256 price,, uint256 updatedAt,) = priceFeed.latestRoundData();

        if (block.timestamp - updatedAt > STALENESS_THRESHOLD) {
            revert StalePrice();
        }
        if (price <= 0) revert InvalidPrice();

        return uint256(price);
    }
}
```

### Flash Loan Callback
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "@aave/v3-core/contracts/flashloan/base/FlashLoanSimpleReceiverBase.sol";

contract Arbitrage is FlashLoanSimpleReceiverBase {
    function executeOperation(
        address asset,
        uint256 amount,
        uint256 premium,
        address,
        bytes calldata
    ) external override returns (bool) {
        // Execute arbitrage logic here

        // Repay: amount + premium
        IERC20(asset).approve(address(POOL), amount + premium);
        return true;
    }
}
```

## DeFi Math Formulas

### Constant Product AMM
```
Invariant: x * y = k
Output: dy = y - k/(x + dx)
Price: p = y/x
Slippage: dx/(x + dx) * 100%
```

### Interest Rates
```
Utilization: U = borrows / (deposits + borrows)
Borrow Rate: R = base + slope * U  (when U < optimal)
Supply Rate: R_supply = R_borrow * U * (1 - reserve_factor)
```

### Health Factor
```
HF = (collateral * liquidation_threshold) / debt
Liquidation when HF < 1
```

## Common Pitfalls

| Pitfall | Risk | Prevention |
|---------|------|------------|
| Spot price oracle | Flash loan manipulation | Use TWAP |
| No slippage check | Sandwich attacks | Enforce min output |
| Stale prices | Wrong liquidations | Check updatedAt |
| Reentrancy | Fund drainage | CEI + guards |

## Security Checklist

- [ ] Oracle staleness validation
- [ ] Slippage protection
- [ ] Flash loan attack resistance
- [ ] Reentrancy guards
- [ ] Access control on admin
- [ ] Emergency pause mechanism
- [ ] Timelock on parameters

## Troubleshooting

### "Oracle price deviation"
```bash
# Compare oracle vs DEX price
cast call $ORACLE "latestRoundData()" --rpc-url $RPC
cast call $POOL "slot0()" --rpc-url $RPC
```

### "Sandwich attack detected"
Add minimum output enforcement:
```solidity
require(amountOut >= minAmountOut, "Slippage exceeded");
```

## Protocol Addresses (Mainnet)

| Protocol | Contract |
|----------|----------|
| Uniswap V3 Router | 0xE592427A0AEce92De3Edee1F18E0157C05861564 |
| Aave V3 Pool | 0x87870Bca3F3fD6335C3F4ce8392D69350B4fA4E2 |
| Chainlink ETH/USD | 0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419 |

## Cross-References

- **Bonded Agent**: `04-defi-specialist`
- **Related Skills**: `solidity-development`, `smart-contract-security`

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.0.0 | 2025-01 | Production-grade with math, security |
| 1.0.0 | 2024-12 | Initial release |
