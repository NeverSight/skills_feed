---
name: hydric-liquidity-pools-indexer-user
description: Comprehensive guide for interacting with the Hydric Liquidity Pools Indexer (Envio/HyperIndex). Use this skill when you need to (1) Query real-time Liquidity Pool data like TVL, Volume, Fees, or Yields/APY, (2) Fetch cross-chain token metadata and prices, (3) Aggregate protocol data (Uniswap, etc.), (4) Retrieve historical time-series data for generic analytics, or (5) Understand the specific 'tracked' vs 'untracked' value safety rules of the indexer.
---

## Liquidity Pools Indexer Overview

The Hydric Liquidity Pools Indexer is a high-performance indexer built on **Envio HyperIndex**. It aggregates liquidity data across multiple blockchains into a unified Postgres database, accessible via a **Hasura-style GraphQL API**.

**Endpoint**: The indexer endpoint is typically provided in the environment variables (e.g., `INDEXER_URL`).
**Schema**: The schema is available at https://github.com/hydric-org/liquidity-pools-indexer/blob/main/schema.graphql.

---

## Core Entities & Schema

The schema is strongly typed. The primary entry points are:

### 1. `Pool`

Represents a text-book liquidity pool (e.g., Uniswap V3 USDC/ETH).

- **Key Fields**: `id`, `chainId`, `poolAddress`, `totalValueLockedUsd`, `token0`, `token1`, `protocol`.
- **Stats**: `totalStats24h`, `totalStats7d`, `totalStats30d`, `totalStats90d` (pre-calculated rolling windows).
- **Type-Specific Data**: `v3PoolData`, `v4PoolData`, `algebraPoolData`, `slipstreamPoolData`.

### 2. `SingleChainToken`

Represents a token deployed on a specific blockchain.

- **Key Fields**: `id`, `tokenAddress`, `symbol`, `name`, `decimals`.
- **Metrics**: `trackedUsdPrice`, `trackedTotalValuePooledUsd` (Liquidity), `trackedSwapVolumeUsd`.
- **Search**: `normalizedSymbol`, `normalizedName` (for fuzzy matching).

### 3. `PoolHistoricalData`

Time-series snapshots for charting.

- **Granularity**: `interval` (e.g., `DAILY`, `HOURLY`).
- **Fields**: `timestampAtStart`, `trackedTotalValueLockedUsdAtStart`, `accumulatedVolume`, `accumulatedFees`.

---

## IDs & Network Reference

**Global ID Format**:
Entities follow a strict globally unique ID pattern: `<chainId>-<lowercase_address>`.

- **Example**: USDC on Ethereum -> `1-0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48`
- **Rule**: Always lowercase addresses when constructing IDs manually.

**Supported Chain IDs**:

- **Ethereum**: `1`
- **Base**: `8453`
- **Scroll**: `534352`
- **Polygon**: `137`
- **Monad**: `143`
- **Unichain**: `130`

---

## Data Handling & Best Practices

### 1. "Tracked" vs "Untracked" Values

The indexer computes values raw (Untracked) and with safety filters (Tracked).

- **⚠️ Untracked**: `totalValueLockedUsd`. Computed simply as `balance * price`. Vulnerable to fake tokens or bad price manipulation.
- **✅ Tracked**: `trackedTotalValueLockedUsd`. **ALWAYS PREFER THIS**. It uses filtered prices and whitelisted tokens to ensure the TVL is real.

### 2. Normalized Search

For search functionality, never query only `symbol` directly, use `normalizedSymbol`, `normalizedName`, `symbol` and `name` to ensure maximum coverage.

- **Use**: `normalizedSymbol` and `normalizedName`.
- **Why**: Handles "USD₮" -> "USDT" conversion and ignores emojis/special chars.
- **Pattern**: `where: { normalizedSymbol: { _ilike: "%USDT%" } }`

### 3. Numbers are Strings

**CRITICAL**: All financial values (TVL, Volume, Prices) are returned as **Strings** in GraphQL to preserve BigInt/Decimal precision.

- **Action**: Use `Number()` or `BigInt()` parsing in your code after fetching.

---

## Specific Entity Patterns

### Querying Different Pool Types (Polymorphism)

Pools can be V3, V4, Algebra, etc. Request the specific nested object to get type-specific data.

```graphql
query GetPoolsWithMetadata {
  Pool(limit: 10) {
    id
    poolType # e.g., "V3", "ALGEBRA", "SLIPSTREAM"
    # Request all possible internal data structures
    v3PoolData {
      tickSpacing
      sqrtPriceX96
    }
    algebraPoolData {
      communityFeePercentage
      plugin
    }
    v4PoolData {
      hooks
      stateView
    }
  }
}
```

### Retrieving Token Prices & Liquidity

Use the `SingleChainToken` entity to get pricing.

```graphql
query GetTokenPricing {
  SingleChainToken(where: { symbol: { _eq: "WETH" } }) {
    id
    chainId
    trackedUsdPrice # Current price in USD
    trackedTotalValuePooledUsd # Total liquidity across all indexed pools
  }
}
```

---

## Example Queries (Copy & Paste)

### 1. Top Pools by TVL (The Standard Leaderboard)

```graphql
query GetTopPools {
  Pool(
    limit: 20
    offset: 0
    order_by: { trackedTotalValueLockedUsd: desc }
    where: { trackedTotalValueLockedUsd: { _gt: "10000" } } # Dust filter
  ) {
    id
    poolAddress
    chainId
    trackedTotalValueLockedUsd
    currentFeeTierPercentage
    token0 {
      symbol
      decimals
    }
    token1 {
      symbol
      decimals
    }
    protocol {
      name
      logo
    }
    totalStats24h {
      yearlyYield
      swapVolumeUsd
      feesUsd
    }
  }
}
```

### 2. Search Tokens Fuzzy

```graphql
query SearchTokens($search: String!) {
  SingleChainToken(
    limit: 10
    where: {
      _or: [
        { normalizedSymbol: { _ilike: $search } }
        { normalizedName: { _ilike: $search } }
      ]
    }
    order_by: { trackedTotalValuePooledUsd: desc }
  ) {
    id
    name
    symbol
    tokenAddress
    chainId
    logoUrl # Note: This might need to be constructed client-side as per skill context
  }
}
```

### 3. Historical Chart Data (Daily Volume/TVL)

```graphql
query GetPoolHistory($poolId: String!) {
  PoolHistoricalData(
    limit: 90
    order_by: { timestampAtStart: asc }
    where: { poolId: { _eq: $poolId }, interval: { _eq: DAILY } }
  ) {
    timestampAtStart
    trackedTotalValueLockedUsdAtStart
    accumulatedVolume
    accumulatedFees
    open
    high
    low
    close
  }
}
```
