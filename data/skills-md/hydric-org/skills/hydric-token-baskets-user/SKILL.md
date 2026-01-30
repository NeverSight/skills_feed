---
name: hydric-token-baskets-user
description: Comprehensive guide for interacting with the hydric Token Baskets system. Use this skill when you need to discover, fetch, or validate curated lists of tokens (baskets) like Stablecoins, LSTs, or Pegged Assets across various blockchain networks.
---

# hydric Token Baskets User Guide

The **hydric Token Baskets** repository is a source of truth for curated collections of tokens sharing specific characteristics (e.g., "USD Stablecoins", "BTC Pegged Tokens"). These baskets are maintained across multiple networks and are publicly accessible via CDN.

## 1. Quick Start

**Base URL Pattern:**

```
https://cdn.jsdelivr.net/gh/hydric-org/token-baskets/baskets/{basketId}.json
```

**Global List:**
`https://cdn.jsdelivr.net/gh/hydric-org/token-baskets/baskets/all.json`

**Example: Get the USD Stablecoins basket:**
`https://cdn.jsdelivr.net/gh/hydric-org/token-baskets/baskets/usd-stablecoins.json`

## 2. Core Concepts

### 2.1 Supported Basket IDs

These IDs allow you to select the _category_ of tokens you are interested in.

**Source of Truth:**
For the most up-to-date list of available baskets, criteria, and IDs, please refer to the `BasketsRegistry` in the official repository:
[src/baskets-registry.ts](https://github.com/hydric-org/token-baskets/blob/main/src/baskets-registry.ts)

### 2.2 Supported Network (Chain) IDs

Use these IDs to access the specific addresses within a basket.

**Source of Truth:**
For the list of supported networks and their Chain IDs, strictly refer to:
[src/domain/enums/chain-id.ts](https://github.com/hydric-org/token-baskets/blob/main/src/domain/enums/chain-id.ts)

## 3. Data Schema

When you fetch a basket JSON file, the response follows the `IBasket` interface:

```typescript
interface IBasket {
  id: string; // The Basket ID (e.g., "usd-stablecoins")
  name: string; // Human-readable name (e.g., "USD Stablecoins")
  logo: string; // URL to the basket's logo image
  description: string; // Description of the basket's criteria
  lastUpdated: string; // ISO 8601 Timestamp of the last update
  addresses: {
    [chainId: string]: string[]; // Map of Chain ID to Array of Token Addresses (lowercase)
  };
}
```

**Note:** The zero address (`0x0000000000000000000000000000000000000000`) is explicitly used to represent the Native Coin of the network (e.g., ETH on ID 1, MATIC on ID 137).

### Response Example

```json
{
  "id": "usd-stablecoins",
  "name": "USD Stablecoins",
  "logo": "https://cdn.jsdelivr.net/...",
  "description": "A curated list of multiple USD Stablecoins...",
  "lastUpdated": "2024-10-24T10:00:00Z",
  "addresses": {
    "1": [
      "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
      "0xdac17f958d2ee523a2206206994597c13d831ec7"
    ],
    "8453": ["0x833589fcd6edb6e08f4c7c32d4f71b54bda02913"]
  }
}
```

## 4. Usage Patterns

### Scenario: Finding Safe Asset Tokens

If you are building a DeFi application and need to verify if a user's token is a recognized stablecoin on a specific chain (e.g., Ethereum ID 1).

**Implementation Logic (Pseudo-code):**

```javascript
async function isVerifiedStablecoin(chainId, tokenAddress) {
  const basketId = "usd-stablecoins";
  // Fetch the consolidated basket file
  const url = `https://cdn.jsdelivr.net/gh/hydric-org/token-baskets/baskets/${basketId}.json`;

  try {
    const response = await fetch(url);
    if (!response.ok) return false;

    const data = await response.json();
    // Access addresses for the specific chain
    const chainAddresses = data.addresses[chainId.toString()] || [];

    // Normalize to lowercase for comparison
    const allowedTokens = new Set(chainAddresses.map((t) => t.toLowerCase()));

    return allowedTokens.has(tokenAddress.toLowerCase());
  } catch (error) {
    console.error("Failed to fetch basket", error);
    return false;
  }
}
```

### Scenario: Displaying Token Options

When a user selects a chain, you can offer them curated lists of tokens to swap or deposit.

1.  **Select Chain**: User selects Base (8453).
2.  **Fetch Lists**: Fetch `usd-stablecoins.json` and `eth-pegged-tokens.json` (or just `all.json` to get everything in one request).
3.  **Display**: Look up `addresses["8453"]` in each basket. If the array is not empty, display the basket using its `name` and `logo`.

### Scenario: Discovering Sector-Specific Liquidity Pools

You can use the tokens in a basket to filter for relevant liquidity pools.

**Implementation Logic (Pseudo-code):**

```javascript
async function getGoldPools(chainId) {
  // 1. Get the authoritative list of Gold tokens for all chains
  const goldBasketUrl = `https://cdn.jsdelivr.net/gh/hydric-org/token-baskets/baskets/xau-stablecoins.json`;
  const basketResponse = await fetch(goldBasketUrl);
  const basketData = await basketResponse.json();

  // 2. Extract tokens for the target chain
  const goldTokens = basketData.addresses[chainId.toString()] || [];

  if (goldTokens.length === 0) return [];

  // 3. Query your Indexer/API for pools containing ANY of these tokens
  const pools = await indexerApi.query({
    where: {
      chainId: chainId,
      tokens: { containsAny: goldTokens },
    },
  });

  return pools;
}
```

## 5. Best Practices

1.  **Caching**: The baskets are static files served via CDN. Cache them! Now that files contain all chains, valid data for one chain is valid for all.
2.  **Data size**: Since files now contain all chains, they are slightly larger but reduce the number of HTTP requests needed.
3.  **Error Handling**: If a fetch returns a 404, the basket ID is invalid. If `addresses[chainId]` is undefined or empty, the basket has no tokens for that network.
4.  **Case Sensitivity**: addresses are **lowercase**.

## 6. How Baskets are Curated

The baskets are generated by an automated agentic system that:

1.  **Scans**: Finds potential tokens based on keywords and market data.
2.  **Validates**: Uses LLMs (`validationPrompt`) to verify project legitimacy and price peg.
3.  **Filters**: Excludes scams, unpegged assets (checked against `blocklist.json`), and malicious impersonators.
4.  **Updates**: Commits changes to the repo, which are then reflected on the CDN.
