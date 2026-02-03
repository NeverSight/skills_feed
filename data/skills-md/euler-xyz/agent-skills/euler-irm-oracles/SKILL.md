---
name: euler-irm-oracles
description: Oracle and Interest Rate Model guide for Euler Finance V2. This skill should be used when deploying oracle adapters, configuring price resolution, querying prices, or understanding IRM types. Triggers on tasks involving Chainlink, Pyth, Chronicle, price feeds, Linear Kink IRM, Adaptive Curve IRM, or interest rate configuration.
license: MIT
metadata:
  author: Euler Labs
  version: "1.0.0"
---

# Euler IRM & Oracles Agent Skill

Oracle integration and Interest Rate Model guide for Euler Finance V2 protocol. Covers oracle adapters, price routing, and IRM configuration.

## When to Apply

Reference these guidelines when:
- Deploying oracle adapters (Chainlink, Pyth, Chronicle, RedStone)
- Configuring EulerRouter for price resolution
- Setting up cross-currency pricing with CrossAdapter
- Querying asset prices from oracles
- Understanding Interest Rate Model types and selection
- Configuring IRM parameters for vaults

## Rule Categories

| Rule | Impact | Description |
|------|--------|-------------|
| `oracle-deploy` | HIGH | Deploy oracle adapters for various price sources |
| `oracle-configure-router` | HIGH | Configure EulerRouter for price resolution |
| `oracle-get-price` | HIGH | Query asset prices from oracles |
| `irm-models` | HIGH | Understand and configure Interest Rate Models |

## Quick Reference

### Oracle Adapters

- **ChainlinkOracle** - For major pairs (ETH/USD, BTC/USD)
- **PythOracle** - Pull-based, requires price updates before use
- **ChronicleOracle** - MakerDAO ecosystem (requires whitelisting)
- **FixedRateOracle** - For stablecoins (1:1 rates)
- **CrossAdapter** - Chain through intermediate assets
- **LidoOracle** - For wstETH/stETH exchange rate
- **RateProviderOracle** - For Balancer Rate Providers

### Interest Rate Models

- **Linear Kink IRM** - Standard two-slope model with utilization-based rates
- **Linear Kinky IRM** - Non-linear acceleration after kink using shape parameter
- **Adaptive Curve IRM** - Self-adjusting based on market conditions
- **Fixed Cyclical Binary** - For binary rate transitions

## Companion Skills

- `euler-vaults` - Core vault operations, EVC, risk management
- `euler-earn` - Yield aggregation vaults
- `euler-advanced` - Hooks, flash loans, fee flow
- `euler-data` - Lens contracts and data querying

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/oracle-deploy.md
rules/oracle-configure-router.md
rules/oracle-get-price.md
rules/irm-models.md
```

## Full Compiled Document

For the complete guide with all rules expanded: `AGENTS.md`
