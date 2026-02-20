---
name: learn-moralis
description: Learn about Moralis and Web3 development. Invoked without a question, gives a friendly platform walkthrough — what's available, what data you can fetch, and how everything fits together. Invoked with a question, answers it directly. Use for "what is Moralis", "can Moralis do X", "what chains are supported", "how do I get started", "which API should I use", pricing, feature comparisons, or any exploratory questions. Routes to the correct technical skill (@moralis-data-api or @moralis-streams-api) after answering.
license: MIT
compatibility: No dependencies required - knowledge-only skill
metadata:
  version: "1.0.0"
  author: MoralisWeb3
allowed-tools: Read Grep Glob
---

# Learn Moralis

## Behavior

**If the user invokes `/learn-moralis` with no question** (or just says "learn moralis"), respond with a friendly platform overview. Walk them through:

1. What Moralis is (enterprise Web3 data platform)
2. The two skills available and when to use each:
   - **@moralis-data-api** (135 endpoints) — query wallet balances, tokens, NFTs, DeFi positions, prices, transactions, analytics. Use for "what is the current/historical state?"
   - **@moralis-streams-api** (20 endpoints, EVM only) — real-time EVM event monitoring via webhooks. Use for "notify me when something happens"
3. Supported chains: 40+ EVM chains for both skills, Solana for Data API only
4. How to get started: set `MORALIS_API_KEY` in `.env`, then use the skill that fits their need

Keep it conversational and concise — think "onboarding tour", not "dump the docs". End by asking what they'd like to build so you can point them to the right skill.

**If the user invokes `/learn-moralis` with a specific question**, answer that question directly using the knowledge below, then route them to the appropriate technical skill.

## What is Moralis?

Moralis is an enterprise-grade Web3 data infrastructure platform providing:

- **Data APIs** - Query wallet balances, tokens, NFTs, DeFi positions, prices, transactions
- **Streams** - Real-time EVM event monitoring via webhooks (EVM chains only, no Solana)
- **Datashare** - Export historical data to Snowflake, BigQuery, S3
- **Data Indexer** - Custom enterprise indexing pipelines
- **RPC Nodes** - Direct blockchain node access

**Key Stats:** Powers 100M+ end users, 2B+ monthly API requests, 50+ supported chains.

---

## Routing to Technical Skills

After answering a general question, route users to the appropriate skill:

| User Need | Route To |
|-----------|----------|
| Query wallet data (balances, tokens, NFTs, history) | @moralis-data-api |
| Get token prices, metadata, analytics | @moralis-data-api |
| Query NFT metadata, traits, floor prices | @moralis-data-api |
| Get DeFi positions, protocol data | @moralis-data-api |
| Query blocks, transactions | @moralis-data-api |
| **Real-time** wallet monitoring (EVM) | @moralis-streams-api |
| **Real-time** contract events (EVM) | @moralis-streams-api |
| Webhooks for EVM on-chain events | @moralis-streams-api |
| Track EVM transfers as they happen | @moralis-streams-api |

**Rule of thumb:**
- **Data API** = "What is the current/historical state?"
- **Streams** = "Notify me when something happens"

---

## Quick Capability Reference

### Can Moralis Do This?

| Question | Answer | Skill |
|----------|--------|-------|
| Get wallet token balances? | Yes, with USD prices | @moralis-data-api |
| Get wallet NFTs? | Yes, with metadata | @moralis-data-api |
| Get wallet transaction history? | Yes, decoded | @moralis-data-api |
| Get token prices? | Yes, real-time + OHLCV | @moralis-data-api |
| Get NFT floor prices? | Yes (ETH, Base, Sei) | @moralis-data-api |
| Get DeFi positions? | Yes (major chains) | @moralis-data-api |
| Monitor wallets in real-time? | Yes (EVM only) | @moralis-streams-api |
| Track contract events live? | Yes (EVM only) | @moralis-streams-api |
| Get historical events? | Use Data API queries | @moralis-data-api |
| ENS/Unstoppable domain lookup? | Yes | @moralis-data-api |
| Token security scores? | Yes | @moralis-data-api |
| Detect snipers/bots? | Yes | @moralis-data-api |

### What Moralis Cannot Do

- Execute transactions (read-only APIs)
- Provide private node access (use RPC Nodes product separately)
- Index custom smart contracts (use Data Indexer product)
- Store user data (you handle storage)
- Provide testnet price data (only mainnet prices)

---

## Supported Chains

### Full API Support

| Chain | Chain ID | Notes |
|-------|----------|-------|
| Ethereum | 0x1 | All APIs including floor prices |
| Base | 0x2105 | All APIs including floor prices |
| Polygon | 0x89 | Missing only floor prices |
| BSC | 0x38 | No profitability, no floor prices |
| Arbitrum | 0xa4b1 | No profitability, no floor prices |
| Optimism | 0xa | No profitability, no floor prices |
| Avalanche | 0xa86a | No profitability, no floor prices |
| Sei | 0x531 | New chain, full support |
| Monad | 0x8f | New chain, good support |

### Also Supported

Linea, Fantom, Cronos, Gnosis, Chiliz, Moonbeam, Moonriver, Flow, Ronin, Lisk, Pulse

### Solana

Mainnet and Devnet supported via **@moralis-data-api only**. Streams does not support Solana. Use `__solana` suffix endpoints.

### Coming Soon

Blast, zkSync, Mantle, opBNB, Polygon zkEVM, Zetachain

---

## Pricing Overview

| Plan | Monthly CUs | Throughput | Price |
|------|-------------|------------|-------|
| Free | 40K/day | 1,000 CU/s | $0 |
| Starter | 2M | 1,000 CU/s | $49/mo |
| Pro | 100M | 2,000 CU/s | $199/mo |
| Business | 500M | 5,000 CU/s | $490/mo |
| Enterprise | Custom | Custom | Contact |

**Compute Units (CUs):** Each API call costs CUs based on complexity. Simple queries ~1-5 CUs, complex queries ~10-50 CUs.

**Overages:** Starter $11.25/M, Pro $5/M, Business $4/M

**Free tier includes:** All APIs (Wallet, Token, NFT, Price, DeFi, Blockchain, Streams)

---

## Getting Started

1. **Sign up:** https://admin.moralis.com/register
2. **Get API key:** Dashboard → API Keys
3. **Set up `.env`:** Add `MORALIS_API_KEY=your_key` to your `.env` file (the skill will help you create it)
4. **Use skill:** Ask what you want to build — the skill will check for your key and guide you

---

## Common Use Cases

### Wallet/Portfolio Tracker

**Need:** Display user's tokens, NFTs, balances, and transaction history.

**Solution:** @moralis-data-api endpoints:
- `getWalletTokenBalancesPrice` - Token balances with prices
- `getWalletNFTs` - NFT holdings
- `getWalletHistory` - Decoded transaction history
- `getWalletNetWorth` - Total portfolio value

### Crypto Tax/Compliance

**Need:** Export transaction history with cost basis.

**Solution:** @moralis-data-api endpoints:
- `getWalletHistory` - All transactions decoded
- `getWalletProfitability` - Realized gains/losses

### NFT Marketplace

**Need:** Display NFT metadata, traits, prices, and ownership.

**Solution:** @moralis-data-api endpoints:
- `getNFTMetadata` - Full metadata + traits
- `getNFTFloorPriceByContract` - Floor price
- `getNFTOwners` - Current holders
- `getNFTTrades` - Sale history

### DeFi Dashboard

**Need:** Show user's DeFi positions across protocols.

**Solution:** @moralis-data-api endpoints:
- `getDefiPositionsSummary` - All positions
- `getDefiPositionsByProtocol` - Protocol-specific data

### Trading Bot / Alerts

**Need:** React to on-chain events in real-time.

**Solution:** @moralis-streams-api:
- Create stream with `topic0` for target events
- Receive webhook when event occurs
- Process and act on data

### Token Analytics Platform

**Need:** Token prices, holders, trading volume, security scores.

**Solution:** @moralis-data-api endpoints:
- `getTokenPrice` - Current price
- `getTokenAnalytics` - Volume, liquidity
- `getTokenHolders` - Holder distribution
- `getTokenScore` - Security analysis

---

## Data API vs Streams: When to Use

| Scenario | Use |
|----------|-----|
| Display current wallet balance | Data API |
| Alert when balance changes | Streams |
| Show transaction history | Data API |
| Log every new transaction | Streams |
| Get NFT metadata | Data API |
| Notify on NFT transfer | Streams |
| Query token price | Data API |
| Track DEX swaps live | Streams |

---

## Reference Documentation

For detailed information:

- [references/FAQ.md](references/FAQ.md) - Common questions and answers
- [references/ProductComparison.md](references/ProductComparison.md) - Detailed feature comparison
- [references/UseCaseGuide.md](references/UseCaseGuide.md) - Implementation patterns by use case

---

## Support Resources

- **Docs:** https://docs.moralis.com
- **Discord:** Community support
- **Forum:** https://forum.moralis.io
- **Stack Overflow:** Tag `moralis`

---

## Next Steps

After answering a question, always suggest the next action:

1. **If user needs to query data:** "Use @moralis-data-api — make sure your `MORALIS_API_KEY` is set in your `.env` file, then I can help you fetch the data."

2. **If user needs real-time events:** "Use @moralis-streams-api — make sure your `MORALIS_API_KEY` is set in your `.env` file and have your webhook URL ready, then I can help set up the stream."

3. **If user is exploring:** Suggest specific endpoints based on their use case.
