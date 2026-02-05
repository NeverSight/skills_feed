---
name: pnp-markets-solana
description: Create, trade, and settle permissionless prediction markets on Solana Mainnet with any SPL token collateral. Use when building prediction market infrastructure, running contests, crowdsourcing probability estimates, adding utility to tokens, creating social media markets (Twitter/YouTube), or tapping into true information finance via market-based forecasting.
compatibility: Requires Node.js 18+, network access (Solana RPC), and a funded Solana wallet with SOL for transaction fees
metadata:
  author: pnp-protocol
  version: "1.0.0"
---

# PNP Markets (Solana)

Create and manage prediction markets on Solana Mainnet with any SPL token collateral. Optimized for high-throughput, low-latency, and permissionless operation.

## When to Use This Skill

Use this skill when the user wants to:
- **Create prediction markets** on Solana (V2 AMM or P2P)
- **Trade on markets** (buy/sell YES/NO outcome tokens)
- **Settle markets** as an oracle after the trading period ends
- **Redeem winning positions** after settlement
- **Create social media markets** (Twitter engagement, YouTube views)
- **Use custom tokens** as prediction market collateral
- **Build info finance infrastructure** with autonomous market resolution

## Prerequisites

Before running any scripts, ensure you have:

1. **Solana Wallet**: Base58-encoded private key with SOL for fees (~0.05 SOL minimum)
2. **USDC Tokens**: Mainnet USDC (`EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v`) for market liquidity
3. **RPC Endpoint**: Mainnet RPC URL (public or dedicated like Helius/QuickNode)

> [!CAUTION]
> **MAINNET ONLY**: All scripts are configured for Solana Mainnet. Never use devnet. RPC defaults to `https://api.mainnet-beta.solana.com`.

> [!IMPORTANT]
> **ALWAYS USE USDC**: All markets must be created with USDC as collateral. Mint: `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v` (6 decimals).

```bash
# Install dependencies
cd scripts && npm install

# Set environment variables
export PRIVATE_KEY=<base58_private_key>
export RPC_URL=https://api.mainnet-beta.solana.com  # or dedicated RPC
```

---

## Market Creation Flow

Solana prediction markets support two primary architectures:

1. **V2 AMM Markets (Default)**: Use Automated Market Makers with virtual liquidity. Best for publicly traded markets.
2. **P2P Markets**: Direct peer-to-peer betting where the creator takes one side. Best for private or specific bets.

### Standard V2 AMM Market Creation

**Function**: `client.market.createMarket(params)`

Creates a standard prediction market using PNP's global oracle for resolution.

```typescript
import 'dotenv/config';
import { PublicKey } from '@solana/web3.js';
import { PNPClient } from 'pnp-sdk';

const RPC_URL = process.env.RPC_URL || 'https://api.mainnet-beta.solana.com';
const PRIVATE_KEY = process.env.PRIVATE_KEY || '';

async function main() {
  const secretKey = PNPClient.parseSecretKey(PRIVATE_KEY);
  const client = new PNPClient(RPC_URL, secretKey);

  const result = await client.market.createMarket({
    question: 'Will Bitcoin reach $100K by end of 2025?',
    initialLiquidity: 1_000_000n,  // 1 USDC (6 decimals)
    endTime: BigInt(Math.floor(Date.now() / 1000) + 30 * 24 * 60 * 60),
    baseMint: new PublicKey('EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v'),
  });

  console.log('Market Address:', result.market.toBase58());
}

main().catch(console.error);
```

**Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `question` | `string` | ✅ | The prediction question |
| `initialLiquidity` | `bigint` | ✅ | Initial liquidity in raw units |
| `endTime` | `bigint` | ✅ | Unix timestamp when trading ends |
| `baseMint` | `PublicKey` | ✅ | Collateral token mint address |

**Returns**: `{ signature: string, market: PublicKey }`

---

## Custom Oracle Markets (For AI Agents)

Custom oracles let AI agents become their own market resolvers—bypassing PNP's global oracle entirely. This is the key primitive for autonomous agent-driven prediction markets.

### Why Custom Oracles?

| Use Case | Description |
|----------|-------------|
| **AI Agents** | Build autonomous agents that create and resolve markets based on real-world data feeds |
| **Private Forecasting** | Run internal prediction markets with proprietary resolution logic |
| **Custom Data Sources** | Integrate any API—sports feeds, weather data, on-chain events, social metrics |

### Custom Oracle Functions

#### `createMarketWithCustomOracle`

**When to use**: Call this when you want your AI agent to have full control over market resolution. Your agent's wallet becomes the oracle—only it can settle the market.

**Why**: Bypasses PNP's global AI oracle. Essential for autonomous agents that need to resolve markets based on their own data sources or logic.

```typescript
await client.createMarketWithCustomOracle({
  question: 'Will BTC hit $150K by Dec 2026?',
  initialLiquidity: 10_000_000n,  // 10 USDC (6 decimals)
  endTime: BigInt(Math.floor(Date.now() / 1000) + 30 * 24 * 60 * 60),
  collateralMint: USDC_MINT,
  settlerAddress: ORACLE_WALLET,  // Your agent's wallet
  yesOddsBps: 5000,  // Optional: 50/50 odds (range: 100-9900)
});
```

#### `setMarketResolvable`

**When to use**: Call this immediately after creating a custom oracle market—within 15 minutes.

**Why**: Markets are created in a frozen state. This activates trading. If not called within 15 minutes, the market is permanently untradeable.

```typescript
await client.setMarketResolvable(marketAddress, true);
```

#### `settleMarket`

**When to use**: Call this after the market's end time when you (as the oracle) know the outcome.

**Why**: Only the designated oracle can settle. This determines which side (YES/NO) wins and allows winners to redeem.

```typescript
await client.settleMarket({
  market: marketAddress,
  yesWinner: true,  // false if NO wins
});
```

> **Critical**: After market creation, you have a **15-minute buffer window** to call `setMarketResolvable(true)`. If not activated, the market is permanently frozen.

---

## Social Media Markets

PNP provides native support for creating prediction markets linked to Twitter/X and YouTube content—ideal for social AI agents.

### Twitter Markets

#### `createMarketTwitter`

**When to use**: Call this when creating a prediction market about tweet engagement (replies, likes, retweets, views).

**Why**: Automatically links the market to a specific tweet. PNP's oracle can track tweet metrics for resolution.

```typescript
await client.createMarketTwitter({
  question: 'Will this tweet cross 5000 replies?',
  tweetUrl: 'https://x.com/username/status/123456789',
  initialLiquidity: 1_000_000n,  // 1 USDC
  endTime: BigInt(Math.floor(Date.now() / 1000) + 30 * 24 * 60 * 60),
  collateralTokenMint: USDC_MINT,
});
```

**Supported URL formats:**
- `https://x.com/username/status/123456789`
- `https://twitter.com/username/status/123456789`

### YouTube Markets

#### `createMarketYoutube`

**When to use**: Call this when creating a prediction market about video performance (views, likes, subscribers).

**Why**: Automatically links the market to a specific YouTube video. PNP's oracle can track video metrics for resolution.

```typescript
await client.createMarketYoutube({
  question: 'Will this video cross 1B views?',
  youtubeUrl: 'https://youtu.be/VIDEO_ID',
  initialLiquidity: 1_000_000n,  // 1 USDC
  endTime: BigInt(Math.floor(Date.now() / 1000) + 30 * 24 * 60 * 60),
  collateralTokenMint: USDC_MINT,
});
```

**Supported URL formats:**
- `https://youtu.be/VIDEO_ID`
- `https://youtube.com/watch?v=VIDEO_ID`
- `https://www.youtube.com/watch?v=VIDEO_ID`

### Social Market Use Cases

- **Engagement Prediction**: Bet on whether a tweet will go viral
- **Content Performance**: Predict video view counts
- **Influencer Markets**: Create markets around creator milestones
- **Trend Detection**: Use market prices as signals for trending content

---

## Programmatic SDK Usage (For AI Agents)

This section provides the complete programmatic reference for AI agents to discover, analyze, trade, and settle markets **without running CLI commands**.

### 1. Client Initialization

```typescript
import { PNPClient } from 'pnp-sdk';
import { PublicKey } from '@solana/web3.js';

// Initialize with RPC and Private Key (Uint8Array or Base58)
const client = new PNPClient(
  'https://api.mainnet-beta.solana.com',
  Uint8Array.from([/* 64-byte array */]) 
);

> [!TIP]
> Use `const secretKey = PNPClient.parseSecretKey(process.env.PRIVATE_KEY)` to automatically handle both Base58 strings and Uint8Array formats.
```

### 2. Market Discovery

AI agents should use these methods to find active markets before trading or analyzing.

| Method | Purpose |
|--------|---------|
| `client.fetchMarketAddresses()` | Returns an array of V2 AMM market addresses from the proxy server. |
| `client.fetchV3MarketAddresses()` | Returns an array of P2P (V3) market addresses. |
| `client.fetchMarkets()` | Fetches on-chain data for all markets (higher latency, use sparingly). |
| `client.fetchMarket(pubkey)` | Fetches detailed on-chain data for a specific market. |

```typescript
// Example: Find all P2P markets
const p2pAddresses = await client.fetchV3MarketAddresses();
console.log(`Found ${p2pAddresses.length} P2P markets.`);
```

### 3. Market Intelligence & Data Fetching

AI agents need comprehensive market data for decision-making. Use these SDK methods for analysis.

#### Price & Multiplier Analysis (Read-Only)

**Function**: `client.getMarketPriceV2(marketAddress)`

Returns real-time AMM pricing data with implied probabilities and payout multipliers.

```typescript
const priceData = await client.getMarketPriceV2(marketAddress);

// Response structure:
// {
//   yesPrice: 0.65,           // YES token price (0-1 range)
//   noPrice: 0.35,            // NO token price (0-1 range)
//   yesMultiplier: 1.54,      // Payout ratio if YES wins
//   noMultiplier: 2.85,       // Payout ratio if NO wins
//   marketReserves: 1000.0,   // Total USDC locked
//   yesTokenSupply: 650.0,    // YES tokens minted
//   noTokenSupply: 350.0      // NO tokens minted
// }

// Calculate implied probabilities
const yesProbability = priceData.yesPrice * 100; // e.g., 65%
const noProbability = priceData.noPrice * 100;   // e.g., 35%

// Calculate potential returns
const betAmount = 10; // $10 USDC
const yesProfit = betAmount * (priceData.yesMultiplier - 1); // e.g., $5.40
const noProfit = betAmount * (priceData.noMultiplier - 1);   // e.g., $18.50
```

#### Comprehensive Market Data Analysis

**Utility**: Use the `market-data.ts` pattern to fetch complete market intelligence:

```typescript
async function getComprehensiveMarketInfo(marketId: string) {
  const client = new PNPClient(RPC_URL); // Read-only
  
  // 1. Fetch on-chain market account data
  const { account: marketData } = await client.fetchMarket(new PublicKey(marketId));
  
  // Market account fields:
  // - question: string
  // - creator: PublicKey
  // - resolvable: boolean (can it be settled?)
  // - resolved: boolean (is it settled?)
  // - end_time: bigint (Unix timestamp)
  // - winning_token_id: 'yes' | 'no' | null
  // - yes_token_mint: PublicKey
  // - no_token_mint: PublicKey
  // - collateral_token: PublicKey
  
  // 2. Fetch settlement criteria from proxy server
  const criteria = await client.fetchSettlementCriteria(marketId);
  
  // Settlement criteria fields:
  // - resolvable: boolean
  // - winning_token_id: 'yes' | 'no' | undefined
  // - reasoning: string (AI explanation)
  // - category: string (e.g., 'coin-predictions')
  // - resolution_plan: Array<{step, action, fallback}>
  // - resolution_sources: string[] (API endpoints)
  
  // 3. Fetch settlement decision from proxy
  const settlementData = await client.fetchSettlementData(marketId);
  
  // Settlement data fields:
  // - answer: 'YES' | 'NO'
  // - reasoning: string (detailed explanation)
  
  // 4. Determine market state
  let state: string;
  if (marketData.resolved) {
    state = 'RESOLVED';
  } else if (!marketData.resolvable) {
    state = 'NOT RESOLVABLE';
  } else if (Date.now() > Number(marketData.end_time) * 1000) {
    state = 'ENDED (pending resolution)';
  } else {
    state = 'ACTIVE';
  }
  
  return { marketData, criteria, settlementData, state };
}
```

**Key SDK Functions for Data Fetching:**

| Function | Returns | Use Case |
|----------|---------|----------|
| `client.fetchMarket(pubkey)` | Market account data | Get on-chain market state |
| `client.getMarketPriceV2(address)` | Price & multiplier data | Calculate trading outcomes |
| `client.fetchSettlementCriteria(address)` | AI resolution criteria | Check if market can be settled |
| `client.fetchSettlementData(address)` | AI settlement decision | Get suggested outcome |
| `client.trading.getMarketInfo(pubkey)` | Extended market info | Get detailed trading data |

### 4. Market Creation Lifecycle

Markets must follow a strict lifecycle, especially **Custom Oracle** markets.

#### V2 / Social Markets
- `client.createMarketTwitter(params)`
- `client.createMarketYoutube(params)`
- `client.market.createMarket(params)` (Standard V2)

#### Custom Oracle (Agent-Controlled)
**Step 1: Create**
```typescript
const result = await client.createMarketWithCustomOracle({
  question: '...',
  initialLiquidity: 10_000_000n,
  endTime: daysFromNow(7),
  collateralMint: USDC_MINT,
  settlerAddress: AGENT_WALLET, // You are the oracle
});
```

**Step 2: Activate (Critical 15-Minute Buffer)**
> [!WARNING]
> You must call this within 15 minutes of creation, or the market is permanently frozen.
```typescript
await client.setMarketResolvable(result.market, true);
```

#### P2P (V3) Markets
- `client.createP2PMarketGeneral(params)`
- `client.createP2PMarketTwitter(params)`
- `client.createP2PMarketYoutube(params)`

### 5. Trading Operations

AI agents can execute trades programmatically on both AMM and P2P markets.

#### V2 AMM Trading Functions

**Buy Tokens**: `client.trading.buyTokensUsdc(params)`

Purchases YES or NO outcome tokens using USDC collateral. AMM automatically calculates token price.

```typescript
const result = await client.trading.buyTokensUsdc({
  market: marketPubkey,
  buyYesToken: true,  // true = YES, false = NO
  amountUsdc: 10,     // Amount in USDC units (not raw)
});

// Returns: { signature: string, tokensReceived?: bigint }
console.log('Transaction:', result.signature);
```

**Sell Tokens (Method 1)**: `client.trading.sellTokensUsdc(params)`

```typescript
const result = await client.trading.sellTokensUsdc({
  market: marketPubkey,
  sellYesToken: true,          // true = YES, false = NO
  tokenAmount: 5_000_000_000_000_000_000n,  // Raw units (18 decimals)
});

// Returns: { signature: string, usdcReceived?: bigint }
```

**Sell Tokens (Method 2)**: `client.trading.burnDecisionTokensDerived(params)`

Lower-level burn function used by scripts. Converts raw token amount to collateral.

```typescript
const amountRaw = BigInt(Math.floor(sellAmount * 1e18)); // 18 decimals

const result = await client.trading.burnDecisionTokensDerived({
  market: marketPubkey,
  amount: amountRaw,
  burnYesToken: true,  // true = YES, false = NO
});

// Returns: { signature: string }
```

#### P2P Trading Function

**Trade P2P Market**: `client.tradeP2PMarket(params)`

Takes the opposite position from the market creator. If creator bet YES, you bet NO (and vice versa).

```typescript
const result = await client.tradeP2PMarket({
  market: marketPubkey,
  side: 'yes',         // 'yes' or 'no'
  amount: 1_000_000n,  // Raw collateral units (e.g., 1 USDC = 1_000_000)
});

// Returns: { signature: string, market: string }
```

**Key Differences**:
- **V2 AMM**: Uses `amountUsdc` in human-readable units (e.g., `10` for 10 USDC)
- **P2P**: Uses `amount` in raw base units (e.g., `1_000_000n` for 1 USDC with 6 decimals)
- **Token Decimals**: Outcome tokens use 18 decimals, collateral varies (USDC = 6, SOL = 9)

### 6. Settlement & Proxy Integration

**Settlement Functions** (Oracle-only operations)

**Settle Market**: `client.settleMarket(params)`

Resolves a market by declaring the winning outcome. Only callable by the designated oracle.

```typescript
const result = await client.settleMarket({
  market: marketPubkey,
  yesWinner: true,  // true = YES wins, false = NO wins
});

// Returns: { signature: string }
console.log('Market settled:', result.signature);
```

**Prerequisites**:
- Current time must be past market's `end_time`
- Oracle wallet must match the market's designated oracle
- For custom oracle markets: Must have called `setMarketResolvable(true)` beforehand

**Automated Settlement Flow**:
```typescript
// Fetch AI-suggested resolution from proxy
const criteria = await client.getSettlementCriteria(marketPubkey);

if (criteria.resolvable) {
  await client.settleMarket({
    market: marketPubkey,
    yesWinner: criteria.winning_token_id === 'yes',
  });
}
```

**Check Market Settlement Status**:
```typescript
const { account: market } = await client.fetchMarket(marketPubkey);

if (market.resolved) {
  console.log('Winner:', market.winning_token_id); // 'yes' | 'no' | null
} else {
  const now = Math.floor(Date.now() / 1000);
  const ended = now > Number(market.end_time);
  console.log('Can settle:', ended && market.resolvable);
}
```

### 7. Redemption & Refunds

**Redeem Winnings**: `client.redeemPosition(marketPubkey)`

Converts winning outcome tokens back to collateral after market settlement.

```typescript
// First check if market is settled
const { account: market } = await client.fetchMarket(marketPubkey);

if (!market.resolved) {
  throw new Error('Market not settled yet');
}

// Redeem winning position
const result = await client.redeemPosition(marketPubkey);

// Returns: { signature: string }
console.log('Redeemed:', result.signature);
```

**Claim Creator Refund**: 

For markets that can't be resolved, creators can reclaim their initial liquidity.

**V2/Custom Oracle Markets**: `client.claimMarketRefund(marketPubkey)`

```typescript
const result = await client.claimMarketRefund(marketPubkey);
// Returns: { signature: string }
```

**P2P Markets**: `client.claimP2PMarketRefund(marketPubkey)`

```typescript
const result = await client.claimP2PMarketRefund(marketPubkey);
// Returns: { signature: string }
```

**Refund Eligibility**:
- Market must be unresolvable (checked via proxy or on-chain flag)
- Caller must be the market creator
- For custom oracle markets: 15-minute buffer period must have expired without activation

- **V2/Custom Oracle**: `await client.claimMarketRefund(marketPubkey)`
- **P2P Markets**: `await client.claimP2PMarketRefund(marketPubkey)`

---

### Core Data Types

AI agents should understand these response structures:

**MarketAccount (`MarketType`)**
- `account.resolved`: boolean - Is trading over?
- `account.resolvable`: boolean - Can it be settled now?
- `account.end_time`: bigint - Unix timestamp.
- `account.winning_token_id`: string ('yes'|'no'|null) - The winner.

**PriceData (`MarketPriceV2Data`)**
- `yesPrice`: number (0-1)
- `noPrice`: number (0-1)
- `yesMultiplier`: number (e.g., 2.0)
- `marketReserves`: number (Total USDC locked)

---

### Common Token Mints (Ready-to-Use)

```typescript
const USDC_MINT = new PublicKey('EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v');
const USDT_MINT = new PublicKey('Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB');
const WSOL_MINT = new PublicKey('So11111111111111111111111111111111111111112');
```

### Helper Functions

```typescript
// Liquidity (USDC 6 decimals)
const usdcToRaw = (amount: number) => BigInt(amount * 1_000_000);

// End Time
const daysFromNow = (days: number) => BigInt(Math.floor(Date.now() / 1000) + days * 86400);
```

---

## Supported Collateral

Markets can be created with any SPL token. Pre-configured aliases:

| Alias | Mint Address | Decimals |
|-------|--------------|----------|
| **USDC** | `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v` | 6 |
| **SOL** | `So11111111111111111111111111111111111111112` | 9 |
| **USDT** | `Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB` | 6 |

## Script Quick Reference

All scripts are located in `scripts/` and use `dotenv/config` to load environment variables from `.env`.

| Script | Purpose | Run Command |
|--------|---------|-------------|
| `create-market.ts` | Create standard V2 AMM market | `tsx scripts/create-market.ts` |
| `create-market-x.ts` | Create Twitter/X engagement market | `tsx scripts/create-market-x.ts` |
| `create-market-yt.ts` | Create YouTube views market | `tsx scripts/create-market-yt.ts` |
| `create-market-p2p.ts` | Create P2P betting market | `tsx scripts/create-market-p2p.ts` |
| `create-market-custom.ts` | Create custom oracle market | `tsx scripts/create-market-custom.ts` |
| `market-data.ts` | Fetch market info & settlement data | `tsx scripts/market-data.ts` |
| `trade.ts` | Buy/sell outcome tokens | `tsx scripts/trade.ts --buy --market <addr> --outcome YES --amount 10` |
| `settle.ts` | Resolve market as oracle | `tsx scripts/settle.ts --market <addr> --outcome YES` |
| `redeem.ts` | Claim winnings after settlement | `tsx scripts/redeem.ts --market <addr>` |

### Environment Setup

Create a `.env` file in the root directory:

```bash
PRIVATE_KEY="your_base58_private_key_here"
RPC_URL="https://api.mainnet-beta.solana.com"
```

> [!IMPORTANT]
> All scripts require the `PRIVATE_KEY` environment variable. Use `PNPClient.parseSecretKey()` to handle both Base58 strings and Uint8Arrays.

---

## Common Errors & Recovery

| Error | Cause | Solution |
|-------|-------|----------|
| `0x1770 (InvalidLiquidity)` | Liquidity below minimum | Use ≥1 USDC or ≥0.05 SOL |
| `Insufficient funds for rent` | Not enough SOL for account creation | Ensure ≥0.05 SOL in wallet |
| `Blockhash not found` | Transaction expired before confirmation | Retry; use faster RPC (Helius/QuickNode) |
| `15-minute buffer expired` | Didn't call `setMarketResolvable` in time | Market is permanently frozen; create new one |
| `TokenAccountNotFound` | Missing Associated Token Account | SDK auto-creates, but ensure SOL for rent |
| `Oracle mismatch` | Wrong wallet trying to settle | Only designated oracle can settle |
| `Market not ended` | Trying to settle before end time | Wait until market's `endTime` passes |

---

## SDK Quick Reference

| Method | When to Use |
|--------|-------------|
| `createMarketWithCustomOracle({...})` | When your agent needs to be the oracle and control resolution |
| `setMarketResolvable(market, true)` | Immediately after creating custom oracle market (within 15 min) |
| `settleMarket({market, yesWinner})` | After market ends, to declare the winner as oracle |
| `createMarketTwitter({...})` | When creating markets about tweet engagement |
| `createMarketYoutube({...})` | When creating markets about video performance |
| `market.createMarket({...})` | For standard V2 AMM markets (PNP oracle resolves) |
| `createP2PMarketGeneral({...})` | When taking a position on one side of the bet |
| `trading.buyTokensUsdc({...})` | To buy YES/NO outcome tokens |
| `redeemPosition(market)` | After settlement, to convert winning tokens to collateral |
| `getMarketPriceV2(market)` | To fetch current prices (read-only, no wallet needed) |
| `fetchMarket(market)` | To get on-chain market data |

---

## Resources

- **Mainnet Explorer**: [Solscan](https://solscan.io)
- **PNP SDK Docs**: [https://docs.pnp.exchange/pnp-sdk](https://docs.pnp.exchange/pnp-sdk)
- **SDK Documentation**: [references/api-reference.md](references/api-reference.md)
- **Advanced Examples**: [references/examples.md](references/examples.md)
